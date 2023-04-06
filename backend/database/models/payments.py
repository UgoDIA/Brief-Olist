from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.schema import UniqueConstraint

try:
    from database import Base
except:
    from ..database import Base
    
class Payments(Base):
    __tablename__ = 'payments'
  #  __table_args__ = ( UniqueConstraint('order', 'sequential'), )
    
    order      = mapped_column(ForeignKey('orders.id'), primary_key=True) 
    sequential = Column(Integer, primary_key=True)
    type       = Column(String, nullable=False)
    installements = Column(Integer, nullable=False)
    payment_value = Column(Integer, nullable=False)
