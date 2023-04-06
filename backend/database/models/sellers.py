from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float

try:
    from database import Base
except:
    from ..database import Base
    
class Sellers(Base):
    __tablename__ = 'sellers'

    id       = Column(Integer, primary_key=True) 
    name     = Column(String)
    location = mapped_column(ForeignKey('locations.state'))
    