from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float

try:
    from database import Base
except:
    from ..database import Base
    
class Products(Base):
    __tablename__ = 'products'

    id          = Column(Integer, primary_key=True)
    name_length = Column(Integer, nullable=False)
    description_length = Column(Integer, nullable=False)
    photos_qty         = Column(Integer, nullable=False)
    
    categorie   = mapped_column(ForeignKey('categories.id'))
    seller      = mapped_column(ForeignKey('sellers.id'))