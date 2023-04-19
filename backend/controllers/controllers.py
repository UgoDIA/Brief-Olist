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
            # Si pas de régions et pas d'années séléctionné
            if region == None and annee == None:
                datas = session.query(OrderItems.product, func.sum(OrderItems.qty).label("test"))\
                    .group_by(OrderItems.product)\
                    .order_by(desc("test")).limit(10)
                # renvoie => id_produit et volume de ventes
                return datas

            # Si seulement région séléctionné
            elif annee == None:
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
            if annee == None:
                datas = session.query(Customers.state, func.sum(OrderItems.price * OrderItems.qty).label('brl'))\
                    .join(Orders, Orders.customer == Customers.id)\
                    .join(OrderItems, OrderItems.order == Orders.id)\
                    .group_by(Customers.state).order_by(desc('brl')).limit(10)
                return datas
            else:
                return 'todo'

        def getEvolutionsCA(region, annee):
            if region == None and annee == None:
                datas = session.query(func.date_trunc('month', Orders.approved_at).label("test"), func.sum(OrderItems.price * OrderItems.qty))\
                    .join(OrderItems, OrderItems.order == Orders.id)\
                    .group_by("test")\
                    .order_by('test')
                return datas

            elif annee == None:
                datas = session.query(Customers.state, func.date_trunc('month', Orders.approved_at).label("test"), func.sum(OrderItems.price * OrderItems.qty))\
                    .join(Orders, Orders.customer == Customers.id)\
                    .join(OrderItems, OrderItems.order == Orders.id)\
                    .group_by(Customers.state, "test").where(Customers.state == region)\
                    .order_by('test')
                return datas

            elif region == None:
                return 'todo'

        def getEvolutionsVolume(region, annee):
            if region == None and annee == None:
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
    def getDatas():
        # QUERY
        sql = text('''SELECT CONCAT((description_length/1000)*1000,' - ' ,(description_length/1000)*1000+1000) as dl_range, SUM(order_items.qty)
        FROM products
        JOIN order_items ON products.id = order_items.product
        group by dl_range
        order by dl_range''')
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
        labels.append(labels[0])
        labels.pop(0)
        values.append(values[0])
        values.pop(0)

        return {'description': {'labels': labels, 'values': values}}
