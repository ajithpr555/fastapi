from pprint import pprint
from typing import Optional, Union,List
from fastapi import  FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body

from pydantic import BaseModel
from random import randrange

# import psycopg2

# from psycopg2.extras import RealDictCursor


from .database import engine,SessionLocal
from . import models,utils
from .schemas import PostBase,UserCreate,UserOut
from .routers import post,user,auth,vote

from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# try:
#     conn = psycopg2.connect(host='localhost',dbname='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
#     cursor=conn.cursor()
#     print("Database connection was successfull")
# except Exception as error:
#     print("Error",error)
    

    

@app.get("/")
def basic():
     print("hello")



    