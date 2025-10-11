from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.database import create_engine,sessionmaker,declarative_base,get_db
from app.config import settings
from app import schemas,models


@pytest.fixture()
def session():
    print("real")
    SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
    print(SQLALCHEMY_DATABASE_URL)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
    Base=declarative_base()
    db=TestingSessionLocal()
    try:
           
           yield db
    finally:
           db.close()
    
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    
    
@pytest.fixture()
def client(session):    

    def override_get_db():
       
       try:
           yield session
       finally:
           session.close()

    app.dependency_overrides[get_db]=override_get_db
    
    yield TestClient(app)
    


@pytest.fixture()
def test_user(client):
    user_data= {"email":"test@gmail.com" , "password":"test"}
    res = client.post("/users",json={"email":user_data["email"] , "password":user_data["password"]})
    
    assert res.status_code == 201
  
    user=res.json()
    user["password"] = user_data["password"]

    
    return user
    