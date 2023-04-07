from sqlalchemy import Column, Integer, String, ForeignKey

try:
    from database import Base
except:
    from ..database import Base
    
from .orders import Orders

class Customers(Base):
    __tablename__ = 'customers'

    id       = Column(String, primary_key=True) 
    
    state  = Column(ForeignKey('locations.state'))