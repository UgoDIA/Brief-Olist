from hug.middleware import CORSMiddleware
import hug
from sqlalchemy import func, desc, text

from database.database import session
from database.models.orders import Orders
from database.models.customers import Customers
from database.models.order_items import OrderItems

from requestFunctions.functions import getDataTOP10product, getTOP10states

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=['*'])) # allow_origins à restreindre pour le déploiement

@hug.get('/api/map')
def getMapData():
    datas = session.query(Customers.state, func.sum(OrderItems.price * OrderItems.qty)).join(Orders, Orders.customer == Customers.id).join(OrderItems, OrderItems.order == Orders.id).group_by(Customers.state)

    return datas


# Non terminé
@hug.get('/api/evolutions/{region}/{annee}')
def getEvolutionsdatas(region,annee):
    dicoDatas = {}

    datas = getDataTOP10product(region, annee)
    dicoDatas['TOP10product'] = datas

    datas = getTOP10states(annee)
    dicoDatas['TOP10states'] = datas
    return dicoDatas