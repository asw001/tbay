from sqlalchemy import Column, create_engine, DateTime, desc, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('postgresql://ubuntu1:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_to_bids = relationship("Bid", backref="items")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bids = relationship("Bid", backref="bidder")
    auctions = relationship("Item", backref="seller")
    
class Bid(Base):
    __tablename__ = "bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    
Base.metadata.create_all(engine)


dana = User(username='Dana', password='NotDanaPassword')
jeff = User(username='Jeff', password='PartyDude4Ever')
connie = User(username='Connie', password='ue34zxy11a')

session.add(dana)
session.commit()
session.add(jeff)
session.commit()
session.add(connie)
session.commit()

baseball1 = Item(name="baseball1", description="slightly used baseball, some sentimental value", owner_id=dana.id)
session.add(baseball1)
session.commit()

print("Next for bidding is {}".format(jeff.username))
print("Bidding is on item: {}".format(baseball1.name))
bid = Bid(item_id=baseball1.id, owner_id=jeff.id, price=5.00)
session.add(bid)
session.commit()

print("Next for bidding is {}".format(connie.username))
print("Bidding is on item: {}".format(baseball1.name))
bid = Bid(item_id=baseball1.id, owner_id=connie.id, price=8.00)
session.add(bid)
session.commit()

high_bid = session.query(Bid.id).order_by(desc(Bid.price)).first()

highest_bidder = session.query(User.username).filter(User.id==high_bid[0]).first()

print("The highest bidder is {}".format(highest_bidder[0]))



