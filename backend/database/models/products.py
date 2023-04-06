from sqlalchemy.orm import mapped_column, relationship
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
    
    category = mapped_column(ForeignKey('categories.id'))
    seller   = mapped_column(ForeignKey('sellers.id'))