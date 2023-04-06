from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float

try:
    from database import Base
except:
    from ..database import Base
    
class Categories(Base):
    __tablename__ = 'categories'

    id   = Column(Integer, primary_key=True) 
    name = Column(String, nullable=False)
    
    