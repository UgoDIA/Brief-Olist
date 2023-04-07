from sqlalchemy import Column, Integer, String, ForeignKey, Float

try:
    from database import Base
except:
    from ..database import Base
    
class OrderItems(Base):
    __tablename__ = 'order_items'

    order   = Column(ForeignKey('orders.id'), primary_key=True)
    product = Column(ForeignKey('products.id'), primary_key=True)

    price  = Column(Float, nullable=False)
    freight = Column(Float, nullable=False, default=0.00)
    qty    = Column(Integer)

    