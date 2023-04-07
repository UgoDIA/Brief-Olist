from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime

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

    order = Column(ForeignKey('orders.id'))