from database.database import session
from database.models import Customers, OrderItems, Orders

from sqlalchemy import func

def mapDataController():
    datas = session.query(Customers.state, func.sum(OrderItems.price * OrderItems.qty)).join(Orders, Orders.customer == Customers.id).join(OrderItems, OrderItems.order == Orders.id).group_by(Customers.state)

    return datas