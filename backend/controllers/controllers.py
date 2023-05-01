from database.database import session
from database.models import Customers, OrderItems, Orders
import re

import datetime

from sqlalchemy import func, desc, types, text


class map:
    def getData():
        datas = session.query(Customers.state, func.sum(OrderItems.price * OrderItems.qty))\
            .join(Orders, Orders.customer == Customers.id)\
            .join(OrderItems, OrderItems.order == Orders.id)\
            .group_by(Customers.state).all()
        datasList = []
        for elt in datas:
            i = 1
            for subelt in elt:
                if i == 1:
                    state = 'br-' + subelt.lower()
                    i += 1
                elif i == 2:
                    valueList = [state, round(subelt, 2)]
                    datasList.append(valueList)
                    i = 1
        return datasList


class evolutions:
    def getDatas(region=None, annee=None):
        def chartJSFormater(datas, region=False):
            regionList = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
                          "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]
            labels = []
            values = []
            for elt in datas:
                for subelt in elt:
                    if isinstance(subelt, str) and region == True or isinstance(subelt, str) and subelt not in regionList:
                        labels.append(subelt)
                    elif isinstance(subelt, datetime.datetime):
                        pattern = r'(\d{4}-\d{2})'
                        match = re.search(pattern, str(subelt))
                        labels.append(match.group(1))
                    elif subelt == None:
                        labels.append(subelt)
                    elif isinstance(subelt, int) or isinstance(subelt, float):
                        values.append(round(subelt, 2))
            return [labels, values]

        def getTOP10product(region, annee):
            print(region, annee)
            # Si pas de régions et pas d'années séléctionné
            if region == None and annee == 'undefined' or annee == None:
                datas = session.query(OrderItems.product, func.sum(OrderItems.qty).label("test"))\
                    .group_by(OrderItems.product)\
                    .order_by(desc("test")).limit(10)
                # renvoie => id_produit et volume de ventes
                print('okokok')
                return datas

            # Si seulement région séléctionné
            elif annee == None or annee == 'undefined':
                # Ne fonctionnait pas, cause => order_by , pq => import les class dans les modele qd fk
                datas = session.query(OrderItems.product, Customers.state, func.sum(OrderItems.qty).label('qtySum'))\
                    .join(Orders, Orders.customer == Customers.id).join(OrderItems, OrderItems.order == Orders.id)\
                    .where(Customers.state == region)\
                    .group_by(OrderItems.product, Customers.state)\
                    .order_by(desc('qtySum')).limit(10)

                # sql = text(
                #     "SELECT order_items.product, sum(order_items.qty) AS qtySum \
                #     FROM customers JOIN orders ON orders.customer = customers.id JOIN order_items ON order_items.\"order\" = orders.id \
                #     WHERE customers.state = \'"+region+"\' \
                #     GROUP BY order_items.product, customers.state \
                #     ORDER BY qtySum DESC \
                #     LIMIT 10"
                # )
                # datas = session.execute(sql)
                # renvoie => id-produit, states et volumes de ventes selon région
                return datas

            # Si seulement annee séléctionné
            elif region == None:
                return 'todo'

            # Régions et année séléctionné
            else:
                return 'todo'

        def getTOP10states(annee):

            # Si pas d'années séléctionné
            if annee == None or annee == 'undefined':
                datas = session.query(Customers.state, func.sum(OrderItems.price * OrderItems.qty).label('brl'))\
                    .join(Orders, Orders.customer == Customers.id)\
                    .join(OrderItems, OrderItems.order == Orders.id)\
                    .group_by(Customers.state).order_by(desc('brl')).limit(10)
                return datas
            else:
                return 'todo'

        def getEvolutionsCA(region, annee):
            if region == None and annee == 'undefined':
                datas = session.query(func.date_trunc('month', Orders.approved_at).label("test"), func.sum(OrderItems.price * OrderItems.qty))\
                    .join(OrderItems, OrderItems.order == Orders.id)\
                    .group_by("test")\
                    .order_by('test')
                return datas

            elif annee == None or annee == 'undefined':
                datas = session.query(Customers.state, func.date_trunc('month', Orders.approved_at).label("test"), func.sum(OrderItems.price * OrderItems.qty))\
                    .join(Orders, Orders.customer == Customers.id)\
                    .join(OrderItems, OrderItems.order == Orders.id)\
                    .group_by(Customers.state, "test").where(Customers.state == region)\
                    .order_by('test')
                return datas

            elif region == None:
                return 'todo'

        def getEvolutionsVolume(region, annee):
            if region == None and annee == 'undefined':
                datas = session.query(func.date_trunc('month', Orders.approved_at).label("month"), func.count(Orders.id))\
                    .group_by("month")\
                    .order_by('month')
                return datas

            elif annee == None:
                datas = session.query(func.date_trunc('month', Orders.approved_at).label("month"), func.count(Orders.id))\
                    .join(Customers, Customers.id == Orders.customer)\
                    .where(Customers.state == region)\
                    .group_by("month")\
                    .order_by('month')
                return datas

            elif region == None:
                return 'todo'

        dicoDatas = {}

        dicoDatas['TOP10product'] = chartJSFormater(
            getTOP10product(region, annee))

        dicoDatas['TOP10states'] = chartJSFormater(getTOP10states(annee), True)

        dicoDatas['evolutionsCA'] = chartJSFormater(
            getEvolutionsCA(region, annee))

        dicoDatas['EvolutionsVolume'] = chartJSFormater(
            getEvolutionsVolume(region, annee))
        
        return dicoDatas


class annonce:
    def getDatas(region=None):
        def graphDescription():
            # QUERY
            if region == None:
                sql = text('''SELECT
                                    CASE WHEN products.description_length <= 1000 THEN 'a. 0 - 1000'
                                            WHEN products.description_length <= 2000 THEN 'b. 1001 - 2000'
                                            WHEN products.description_length <= 3000 THEN 'c. 2001 - 3000'
                                            WHEN products.description_length <= 4000 THEN 'd. 3001 - 4000'
                                            WHEN products.description_length > 4000 THEN 'e. 4001+'
                                            ELSE 'Non renseigné' END AS description,
                                    SUM(order_items.qty) AS ventes
                                FROM products
                                JOIN order_items ON products.id = order_items.product
                                group by description
                                order by description''')
            else:
                sql = text(f'''SELECT
                                    CASE WHEN products.description_length <= 1000 THEN 'a. 0 - 1000'
                                            WHEN products.description_length <= 2000 THEN 'b. 1001 - 2000'
                                            WHEN products.description_length <= 3000 THEN 'c. 2001 - 3000'
                                            WHEN products.description_length <= 4000 THEN 'd. 3001 - 4000'
                                            WHEN products.description_length > 4000 THEN 'e. 4001+'
                                            ELSE 'Non renseigné' END AS description,
                                    SUM(order_items.qty) AS ventes
                                FROM products
                                JOIN order_items ON products.id = order_items.product
                                JOIN orders ON orders.id = order_items.order
                                JOIN customers ON customers.id = orders.customer
                                JOIN locations ON locations.state = customers.state
                                WHERE locations.state = '{region}'
                                group by description, locations.state
                                order by description''')
            datas = session.execute(sql)

            # FORMAT for chartjs
            labels = []
            values = []
            for elt in datas:
                i = 1
                for subelt in elt:
                    if i/2 == int(i/2):
                        values.append(subelt)
                    else:
                        if subelt == ' - ':
                            labels.append('Non renseigné')
                        else:
                            labels.append(subelt)
                    i += 1

            return {'labels': labels, 'values': values}

        def graphPhotos():
            # Fléxibiliser => nb de colonnes selon select distinct
            # QUERY
            if region == None:
                sql = text('''SELECT
                                    CASE WHEN products.photos_qty <= 4 THEN 'a. 0 - 4'
                                            WHEN products.photos_qty <= 8 THEN 'b. 5 - 8'
                                            WHEN products.photos_qty <= 12 THEN 'c. 9 - 12'
                                            WHEN products.photos_qty <= 16 THEN 'd. 13 - 16'
                                            WHEN products.photos_qty <= 20 THEN 'e. 17 - 20'
                                            WHEN products.photos_qty > 20 THEN 'f. 20+'
                                            ELSE 'Non renseigné' END AS photos_quantity,
                                    SUM(order_items.qty) AS ventes
                                FROM products
                                JOIN order_items ON products.id = order_items.product
                                group by photos_quantity
                                order by photos_quantity''')
            else:
                sql = text(f'''SELECT
                                    CASE WHEN products.photos_qty <= 4 THEN 'a. 0 - 4'
                                            WHEN products.photos_qty <= 8 THEN 'b. 5 - 8'
                                            WHEN products.photos_qty <= 12 THEN 'c. 9 - 12'
                                            WHEN products.photos_qty <= 16 THEN 'd. 13 - 16'
                                            WHEN products.photos_qty <= 20 THEN 'e. 17 - 20'
                                            WHEN products.photos_qty > 20 THEN 'f. 20+'
                                            ELSE 'Non renseigné' END AS photos_quantity,
                                    SUM(order_items.qty) AS ventes
                                FROM products
                                JOIN order_items ON products.id = order_items.product
                                JOIN orders ON orders.id = order_items.order
                                JOIN customers ON customers.id = orders.customer
                                JOIN locations ON locations.state = customers.state
                                WHERE locations.state = '{region}'
                                group by photos_quantity, locations.state
                                order by photos_quantity''')
            datas = session.execute(sql)
            labels = []
            values = []

            for elt in datas:
                i = 1
                for subelt in elt:
                    if i/2 == int(i/2):
                        values.append(subelt)
                    else:
                        labels.append(subelt)
                    i += 1

            return {'labels': labels, 'values': values}

        dicoDatas = {}
        dicoDatas['description'] = graphDescription()
        dicoDatas['photos'] = graphPhotos()

        return dicoDatas
