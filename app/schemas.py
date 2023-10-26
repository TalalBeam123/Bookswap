from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str
    username: str

    
class User(BaseModel):
    email: str
    password: str
    

class UserLogin(User):
    pass

class UserSignUp(User):
    username: str


class PurchaseBook(BaseModel):
    title: str


class AddListing(BaseModel):
    title: str
    author: str
    description: str

class BookListingResponse(AddListing):
    pass