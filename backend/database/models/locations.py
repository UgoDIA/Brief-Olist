from sqlalchemy import Column, Integer, String, ForeignKey, Float

try:
    from database import Base
except:
    from ..database import Base
    
class Locations(Base):
    __tablename__ = 'locations'
    
    state     = Column(String, primary_key=True)