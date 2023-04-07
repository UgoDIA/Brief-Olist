from sqlalchemy import Column, Integer, String, ForeignKey, Float

try:
    from database import Base
except:
    from ..database import Base
    
class Payments(Base):
    __tablename__ = 'payments'
    
    order = Column(ForeignKey('orders.id'), primary_key=True)
    sequential = Column(Integer, primary_key=True)
    type       = Column(String, nullable=False)
    installments = Column(Integer, nullable=False)
    payment_value = Column(Integer, nullable=False)
