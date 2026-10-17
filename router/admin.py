from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database import  SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from router.auth import get_current_user
from models import Todos

router = APIRouter()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



@router.get('/admin/todo')
def read_all(user: user_dependency, db : db_dependency):
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='user not found')
        
    return db.query(Todos).all()


@router.delete('/admin/delete/{todo_id}')
def delete_todos_by_admin(user : user_dependency, db : db_dependency, todo_id : int):
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='user not found')
    
    todo =  db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail='todo id not found')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
       
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Todo deleted successfully'}) 