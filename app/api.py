from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db_models import Base, BookListing, User, BookExchange
from fastapi import status, HTTPException
from datetime import timedelta
from app.oauth2 import authenticate_user, create_access_token, get_current_user
from app.database import engine, get_db
from app.schemas import UserSignUp, AddListing, PurchaseBook, BookListingResponse
from app.utils import get_password_hash
import uuid
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Login functionality
@app.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = authenticate_user(db=db,email=user_credentials.username,password=user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username,"id":user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup")
def create_user(user_info: UserSignUp, db: Session = Depends(get_db)):

    user_id = str(uuid.uuid4())
    hash_pass = get_password_hash(user_info.password)
    new_user = User(user_id=user_id,username=user_info.username,password=hash_pass,email=user_info.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"status":"successfully created new user"}


@app.post("/add_book")
def add_listing(book_info:AddListing, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    listing_id = str(uuid.uuid4())
    user_id = current_user.user_id
    status = "available"

    new_listing = BookListing(user_id=user_id,
                              listing_id=listing_id,
                              title=book_info.title,
                              author=book_info.author,
                              description=book_info.description,
                              status=status
                              )

    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    return {"status":"Book has been added succesfully"}


# Purchase a book add it to book_exchanges and update status of book to avaible
@app.post("/purchase")
def purchase_book(book: PurchaseBook, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    listing = db.query(BookListing).filter(BookListing.title==book.title).first()

    if listing.status != "available":
        return {"status":"Already Sold Out"}
    
    listing_id = listing.listing_id
    seller_id = listing.user_id
    exchange_id = str(uuid.uuid4())
    buyer_id = current_user.user_id
    exchange_date = datetime.now()

    book_purchase = BookExchange(
        exchange_id = exchange_id,
        listing_id = listing_id,
        seller_user_id = seller_id,
        buyer_user_id = buyer_id,
        exchange_date = exchange_date
        
    )

    db.add(book_purchase)
    db.commit()
    db.refresh(book_purchase)

    # Update Status in Book Listing
    listing = db.query(BookListing).filter(BookListing.title==book.title).first()
    listing.status = "sold"
    db.commit()

    return {"status":"Sold"}



    

# Get all books that are available
@app.get("/get_available_books")
def get_all_available_books(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    books = db.query(BookListing).filter(BookListing.status=="available").all()

    available_listings = []
    for book in books:
        available_listings.append(BookListingResponse(
            title=book.title,
            author=book.author,
            description=book.description
        ))
    return available_listings


