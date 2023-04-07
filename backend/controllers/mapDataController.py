from database.database import session
from database.models import Customers, OrderItems, Orders

from sqlalchemy import func

def mapDataController():
    datas = session.query(Customers.state, func.sum(OrderItems.price * OrderItems.qty)).join(Orders, Orders.customer == Customers.id).join(OrderItems, OrderItems.order == Orders.id).group_by(Customers.state)
    # print('==================>', datas.all())
    datas = datas.all()
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
    print(datasList)

    return datasList