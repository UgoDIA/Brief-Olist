from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.schema import UniqueConstraint

try:
    from database import Base
except:
    from ..database import Base
    
class OrderItems(Base):
    __tablename__ = 'order_items'
#    __table_args__ = ( UniqueConstraint('order', 'item_count'), )

    order   = Column(ForeignKey('orders.id'), primary_key=True)
    product = mapped_column(ForeignKey('products.id'), primary_key=True)

    price  = Column(Float, nullable=False)
    freight = Column(Float, nullable=False, default=0.00)
    qty    = Column(Integer)
    

    