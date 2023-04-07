from database.database import session
from database.models import Customers, OrderItems, Orders

from sqlalchemy import func, desc

class map:
    def getData():
        datas =  session.query(Customers.state, func.sum(OrderItems.price * OrderItems.qty)).join(Orders, Orders.customer == Customers.id).join(OrderItems, OrderItems.order == Orders.id).group_by(Customers.state).all()
        datasList = []
        for elt in datas:
            # print(elt)
            i = 1
            for subelt in elt:
                if i == 1:
                    state = 'br-' +  subelt.lower()
                    # print(state)
                    i+=1
                elif i == 2:
                    valueList = [state, round(subelt, 2)]
                    datasList.append(valueList)
                    # print(valueList)
                    i = 1
        return datasList
class evolutions:
    def getDatas(region=None, annee=None):
        def getDataTOP10product(region, annee):
            # Si pas de régions et pas d'années séléctionné
            if region == None and annee == None:
                datas = session.query(OrderItems.product, func.sum(OrderItems.qty).label("test")).group_by(OrderItems.product).order_by(desc("test")).limit(10)
                # renvoie => id_produit et volume de ventes
                return datas

            # Si seulement région séléctionné
            elif annee == None:
                # Ne fonctionnait pas, cause => order_by , pq => import les class dans les modele qd fk
                datas = session.query(OrderItems.product,Customers.state, func.sum(OrderItems.qty).label('qtySum')).join(Orders, Orders.customer == Customers.id).join(OrderItems, OrderItems.order == Orders.id).where(Customers.state == region).group_by(OrderItems.product, Customers.state).order_by(desc('qtySum')).limit(10)
                
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
                datas = session.query(Customers.state, func.sum(OrderItems.price * OrderItems.qty).label('brl')).join(Orders, Orders.customer == Customers.id).join(OrderItems, OrderItems.order == Orders.id).group_by(Customers.state).order_by(desc('brl')).limit(10)
                return datas
            else:
                return 'todo'
        
        dicoDatas = {}

        datas = getDataTOP10product(region, annee)
        dicoDatas['TOP10product'] = datas

        datas = getTOP10states(annee)
        dicoDatas['TOP10states'] = datas

        return dicoDatas