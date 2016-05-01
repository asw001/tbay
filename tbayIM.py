from sqlalchemy import Column, create_engine, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('postgresql://ubuntu1:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

bid_table = Table('user_to_item_bid', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('bid_id', Integer, ForeignKey('bid.id'))
)

auction_table = Table('user_to_auction', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('item_id', Integer, ForeignKey('item.id'))
)



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    users_to_item = relationship("Auction_User", secondary=bid_table, backref="users")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    auctions = relationship("Auctions", secondary=auction_table, backref="user")
    
class Bid(Base):
    __tablename__ = "bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    bids_table = relationship("User", secondary=bid_table, backref="users")
    
    
Base.metadata.create_all(engine)
