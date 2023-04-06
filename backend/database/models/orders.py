from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

try:
    from database import Base
except:
    from ..database import Base
    
class Orders(Base):
    __tablename__ = 'orders'

    id     = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    
    approved_at  = Column(DateTime, nullable=False)
    delivered_carrier_date   = Column(DateTime, nullable=False)
    shipping_limit_date      = Column(DateTime, nullable=False)
    deliverred_customer_date = Column(DateTime, nullable=False)
    estimated_delivery_date  = Column(DateTime, nullable=False)
    purchase_timestamps      = Column(DateTime, nullable=False)
    
    customer   = mapped_column(ForeignKey('customers.id'))
    state   = mapped_column(ForeignKey('locations.state'))
    