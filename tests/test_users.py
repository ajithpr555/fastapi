from app import schemas
import pytest

from jose import jwt
    
from app.oauth2 import ACCESS_TOKEN_EXPIRY_MINUTES,ALGORITHM,SECRET_KEY


def test_root(client):
    res=client.get("/")
    
    assert res.status_code == 200
    
    
# def test_create_user(client):

#     res=client.post("/users",json ={"email":"hello@gmail.com", "password":"password"})
    
#     new_user = schemas.UserOut(**res.json())
#     assert res.status_code == 201
   
 

def test_login_user(client, test_user):
    res=client.post("/login",data ={"username":test_user["email"], "password":test_user["password"]})
    login_res = schemas.Token(**res.json())
    
    payload = jwt.decode(login_res.access_token,SECRET_KEY,algorithms=[ALGORITHM])
    
    id:str = payload.get("user_id")
    
    
    assert res.status_code == 200
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
  
  
  
@pytest.mark.parametrize("username,password,status_code",[
    ("test@gmail.com","tesst",403)
])    
def test_incorrect_user(test_user,client,username,password,status_code):
    res=client.post("/login",data = {"username":username , "password":password})
    
    assert res.status_code == status_code