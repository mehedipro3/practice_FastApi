from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Todos
from typing import Annotated, Optional
from database import engine, SessionLocal
from fastapi.responses import JSONResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class Todo(BaseModel):
    id : int
    title : str
    description : str = Field(max_length=100)
    priority : int = Field(gt=0, lt=6)
    completed : bool

class TodoUpdate(BaseModel):
    id : Optional[int] = Field(default=None)
    title : Optional[str] = Field( default=None)
    description : Optional[str] = Field(default=None, max_length=100)
    priority : Optional[int] = Field(default=None, gt=0, lt=6)
    completed : Optional[bool] = Field( default=None)
    
    
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/')
def read_todos(db : db_dependency):
    return db.query(Todos).all()


@app.get('/todo/{todo_id}')
def read_specific_todos(db : db_dependency, todo_id : int):
    specific_todo =  db.query(Todos).filter(Todos.id == todo_id).first()
    
    if specific_todo is not None:
        return specific_todo
    
    else:
        raise HTTPException(status_code=404, detail='todo id not found')
    
    
    
@app.post('/create/')
def create_todos(db : db_dependency, new_todo : Todo):
    todo_model = Todos(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()
    
    return JSONResponse(status_code=201, content={'message' : 'Todo create successfully'}) 
    
    
    
@app.put('/edit/{todo_id}')
def read_specific_todos(db : db_dependency, todo_id : int, update_todo : TodoUpdate):
    
    todo =  db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail='todo id not found')
    
    
    update_data = update_todo.model_dump(exclude_unset=True) 
    
    for key,value in update_data.items():
        setattr(todo,key,value)
        
        
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Todo updated successfully'}) 
    
    
    


@app.delete('/delete/{todo_id}')
def read_specific_todos(db : db_dependency, todo_id : int):
    
    todo =  db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail='todo id not found')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
       
    db.commit()
    return JSONResponse(status_code=200, content={'message' : 'Todo deleted successfully'}) 