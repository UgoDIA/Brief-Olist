from database.database import session
from database.models import Customers, OrderItems, Orders
import re

import datetime

from sqlalchemy import func, desc, types


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
        def chartJSFormater(datas):
            labels = []
            values = []
            for elt in datas:
                for subelt in elt:
                    if isinstance(subelt, str):
                        labels.append(subelt)
                    elif isinstance(subelt, datetime.datetime):
                        pattern = r'(\d{4}-\d{2})'
                        match = re.search(pattern, str(subelt))
                        labels.append(match.group(1))
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

        # ATTENTION Ici les valeurs contenu qui n'ont pas de date (null) ne sont pas envoyé
        # à cause de 'isinstance(date)' dans le formateurChartJS
        def getEvolutionsRegionCA(region, annee):
            if region == None and annee == None:
                datas = session.query(func.date_trunc('month', Orders.delivered_customer_date).label("test"), func.sum(OrderItems.price * OrderItems.qty))\
                    .join(OrderItems, OrderItems.order == Orders.id)\
                    .group_by("test")\
                    .order_by(desc('test'))
                return datas

            elif annee == None:
                datas = session.query(Customers.state, func.date_trunc('month', Orders.delivered_customer_date).label("test"), func.sum(OrderItems.price * OrderItems.qty))\
                    .join(Orders, Orders.customer == Customers.id)\
                    .join(OrderItems, OrderItems.order == Orders.id)\
                    .group_by(Customers.state, "test").where(Customers.state == region)\
                    .order_by(desc('test'))
                return datas

            elif region == None:
                return 'todo'

        dicoDatas = {}

        dicoDatas['TOP10product'] = chartJSFormater(
            getTOP10product(region, annee))

        dicoDatas['TOP10states'] = chartJSFormater(getTOP10states(annee))

        dicoDatas['evolutionsRegionsCA'] = chartJSFormater(
            getEvolutionsRegionCA(region, annee))

        return dicoDatas