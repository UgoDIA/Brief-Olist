from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.schema import UniqueConstraint

try:
    from database import Base
except:
    from ..database import Base
    
class Reviews(Base):
    __tablename__ = 'reviews'
    
    id = Column(String, primary_key=True)
    score = Column(Integer)
    comment_title = Column(String)
    comment_message = Column(String)
    creation_date = Column(DateTime)
    answer_timestamp = Column(DateTime)
    
    order = mapped_column(ForeignKey('orders.id'))