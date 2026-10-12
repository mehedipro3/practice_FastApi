from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from models import Users
from datetime import timedelta, timezone, datetime
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from database import  SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2Bearer = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY ='0bb1e0a5be358d5f97b186f698aadd206ecf5719e55aaca88e728b64bc590070'
ALGORITHM ='HS256'

class CreateUsers(BaseModel):
    email : str 
    username : str
    firstname : str
    lastname : str
    password : str
    role : str
    
    
def auth_user(username, password, db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    
    if bcrypt_context.verify(password, user.hash_password):
        return user
    return False

def create_access_token(user_name: str, user_id: int, expries_delta: timedelta):
    encode = {'sub' : user_name, 'id' : user_id}
    expires = datetime.now(timezone.utc) + expries_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    

def get_current_user(token: Annotated[str, Depends(OAuth2Bearer)]):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get('sub')
        user_id: str = payload.get('id')
        if user_name is None or user_id is None:
            raise HTTPException(status_code=404, detail='user not found')
        return {'username':user_name, 'id':user_id}
    except:
        raise HTTPException(status_code=404, detail='user not found')

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/createUser')
def create_users(db : db_dependency, new_user : CreateUsers):
    user_model = Users(
        email = new_user.email,
        username = new_user.username,
        firstname = new_user.firstname,
        lastname = new_user.lastname,
        hash_password = bcrypt_context.hash(new_user.password),
        is_active = True,
        role = new_user.role
    )
    db.add(user_model)
    db.commit()
    
    return JSONResponse(status_code=201, content={'message' : 'User created successfully'}) 
    
    

@router.post('/login')
def login_user(db : db_dependency, form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user = auth_user(form_data.username, form_data.password, db)
    if not user:
        return 'failed authentication'
    
    token = create_access_token(user.username,user.id,timedelta(minutes=30))
    return {'access_token' : token, 'token_type' : 'bearer'}