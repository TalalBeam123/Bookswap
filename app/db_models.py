from app.database import Base
from sqlalchemy import Column, Integer, String,Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    email = Column(String, nullable=True)



class BookListing(Base):
    __tablename__ = "book_listings"

    listing_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    title = Column(String(100), index=True)
    author = Column(String(100))
    description = Column(Text, nullable=True)
    status = Column(String(20))



class BookExchange(Base):
    __tablename__ = "book_exchanges"

    exchange_id = Column(String, primary_key=True, index=True)
    listing_id = Column(String, ForeignKey("book_listings.listing_id"))
    seller_user_id = Column(String, ForeignKey("users.user_id"))
    buyer_user_id = Column(String, ForeignKey("users.user_id"))
    exchange_date = Column(DateTime, nullable=False)

