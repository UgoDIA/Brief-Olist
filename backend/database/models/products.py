from sqlalchemy import Column, Integer, String, ForeignKey, Float

try:
    from database import Base
except:
    from ..database import Base
    
class Products(Base):
    __tablename__ = 'products'

    id          = Column(String, primary_key=True)
    name_length = Column(Integer)
    description_length = Column(Integer)
    photos_qty         = Column(Integer)
    
    category = Column(ForeignKey('categories.id'))
    seller   = Column(ForeignKey('sellers.id'))