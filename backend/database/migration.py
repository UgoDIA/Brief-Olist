from database import engine

from models.customers import Customers, Base
from models.locations import Locations, Base
from models.categories import Categories, Base
from models.products import Products, Base
from models.sellers import Sellers, Base
from models.orders import Orders, Base
from models.order_items import OrderItems, Base
from models.payments import Payments, Base
from models.reviews import Reviews, Base
''' Create all table'''
Base.metadata.create_all(engine)