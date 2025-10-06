from datetime import datetime
from pydantic import BaseModel,EmailStr, Field
from typing import Optional, Annotated

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_timestamp: datetime
    class Config:
       from_attributes= True

class PostBase(BaseModel):
    title: str
    content:str 
    published: bool = True
    class Config:
        from_attributes= True
    
#class Post(BaseModel):
#     title: str
#     content:str 
#     published: bool = True
#     class Config:
#         from_attributes= True  
    
    
class PostCreate(PostBase):
    id: int
    owner_id: int
    created_timestamp: datetime
    owner: UserOut
    class Config:
        from_attributes= True
    
class PostOut(BaseModel):
    Post: PostCreate
    votes:int
    class Config:
        from_attributes= True
    


        
class UserCreate(BaseModel):
    email:EmailStr
    password:str


    
       
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
   id : Optional[int] = None
   
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]