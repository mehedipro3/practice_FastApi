from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Todos
from typing import Annotated, Optional
from database import engine, SessionLocal
from fastapi.responses import JSONResponse
from router.auth import get_current_user
from router import auth, admin

app = FastAPI()


class Todo(BaseModel):
    title : str
    description : str = Field(max_length=100)
    priority : int = Field(gt=0, lt=6)
    completed : bool = False

class TodoUpdate(BaseModel):
    id : Optional[int] = Field(default=None)
    title : Optional[str] = Field( default=None)
    description : Optional[str] = Field(default=None, max_length=100)
    priority : Optional[int] = Field(default=None, gt=0, lt=6)
    completed : Optional[bool] = Field( default=None)
    
    

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(admin.router)
    
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get('/')
def read_todos(user: user_dependency, db : db_dependency):
    
    if user is None:
        raise HTTPException(status_code=401, detail='user not found')
        
    return db.query(Todos).filter(Todos.owners_id == user.get('id')).all()


@app.get('/todo/{todo_id}')
def read_specific_todos(user : user_dependency, db : db_dependency, todo_id : int):
    if user is None:
        raise HTTPException(status_code=401, detail='user not found')
    specific_todo =  db.query(Todos).filter(Todos.owners_id == user.get('id')).all().filter(Todos.id == todo_id).first()
    
    if specific_todo is not None:
        return specific_todo
    
    else:
        raise HTTPException(status_code=404, detail='todo id not found')
    
    
    
@app.post('/create/')
def create_todos(user : user_dependency ,db : db_dependency, new_todo : Todo):
    
    if user is None:
        raise HTTPException(status_code=401, detail='user not found')
    
    todo_model = Todos(**new_todo.model_dump(), owners_id = user.get('id'))
    db.add(todo_model)
    db.commit()
    
    return JSONResponse(status_code=201, content={'message' : 'Todo create successfully'}) 
    
    
    
@app.put('/edit/{todo_id}')
def read_specific_todos(user : user_dependency,db : db_dependency, todo_id : int, update_todo : TodoUpdate):
    
    if user is None:
            raise HTTPException(status_code=401, detail='user not found')
    
    todo =  db.query(Todos).filter(Todos.owners_id == user.get('id')).filter(Todos.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail='todo id not found')
    
    
    update_data = update_todo.model_dump(exclude_unset=True) 
    
    for key,value in update_data.items():
        setattr(todo,key,value)
        
        
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Todo updated successfully'}) 
    
    
    


@app.delete('/delete/{todo_id}')
def read_specific_todos(user : user_dependency, db : db_dependency, todo_id : int):
    
    if user is None:
        raise HTTPException(status_code=401, detail='user not found')
    
    todo =  db.query(Todos).filter(Todos.owners_id == user.get('id')).filter(Todos.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail='todo id not found')
    
    db.query(Todos).filter(Todos.owners_id == user.get('id')).filter(Todos.id == todo_id).delete()
       
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Todo deleted successfully'}) 