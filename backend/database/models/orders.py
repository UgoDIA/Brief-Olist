from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from .order_items import OrderItems

try:
    from database import Base
except:
    from ..database import Base
    
class Orders(Base):
    __tablename__ = 'orders'

    id     = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    
    approved_at  = Column(DateTime)
    delivered_carrier_date   = Column(DateTime)
    shipping_limit_date      = Column(DateTime)
    delivered_customer_date = Column(DateTime)
    estimated_delivery_date  = Column(DateTime)
    purchase_timestamps      = Column(DateTime)
    
    customer = mapped_column(ForeignKey('customers.id'))
    items    = relationship(OrderItems, backref='orders')