from fastapi import FastAPI,Path,HTTPException,Query , Body
from pydantic import BaseModel ,Field
from typing import Annotated , Optional
from fastapi.responses import JSONResponse
import json

app = FastAPI()

class Student(BaseModel):
    id: Annotated[str , Field(..., description="The ID of the student", example="S001")]
    name: Annotated[str , Field(..., description="The name of the student", example="John Doe")]
    roll: Annotated[int , Field(..., description="The roll number of the student", example=1)]
    class_: Annotated[str , Field(..., description="The class of the student", example="10A")]
    phn: Annotated[str , Field(..., description="The phone number of the student", example="1234567890")]
    marks: Annotated[dict, Field(..., description="The marks of the student", example={
      "mathematics": 89,
      "physics": 91,
      "chemistry": 86,
      "english": 93,
      "computer_science": 96
    })]


class UpdateStudent(BaseModel):
    id: Annotated[Optional[str] , Field(default=None)]
    name: Annotated[Optional[str] , Field(default=None)]
    roll: Annotated[Optional[int] , Field(default=None)]
    class_: Annotated[Optional[str] , Field(default=None)]
    phn: Annotated[Optional[str] , Field(default=None)]
    marks: Annotated[Optional[dict], Field(default=None)]
    
def load_data():
    with open('students.json','r') as f:
        data = json.load(f)
    return data


def save_data(data):
    with open('students.json','w') as f:
        json.dump(data, f)
        
        


@app.get("/")
def hello():
    return "The is the student record management system"

@app.get("/about")
def about():
    return "This is a student record management system of About Page."

@app.get("/view")
def view_students():
    data = load_data()
    return data


@app.get("/view/{student_id}")
def view_students(student_id: str = Path(..., description="The ID of the student to retrieve", examples=["S002"])):
    data = load_data()
    
    
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code = 404, detail="Student not found")
    
    
    
@app.get("/sort")
def sort_students(sorted_by: str = Query(..., description="The field to sort students by"), order: str = Query("asc", description="Sort by asc or desc")):
    
    vaild_fields = ['roll', 'class', 'phn']
    
    
    if sorted_by not in vaild_fields:
        raise HTTPException(status_code = 404, detail=f"Invalid sort field {vaild_fields}")
    
    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code = 404, detail=f"Invalid order. Choose between asc and desc")
    
    data = load_data()
    
    sort_order = True if order == 'desc' else False
    
    sorted_data = list(data.values())
    sorted_data.sort(key = lambda x: x[sorted_by] , reverse=sort_order)
     
    return sorted_data



@app.post('/create')
def create_student(student: Student):
    data = load_data()
    
    if student.id in data:
        raise HTTPException(status_code = 400, detail="Student with this ID already exists")
    
    student_id = student.id
    data[student_id] = student.model_dump(exclude='id')
    marks = student.marks
    data[student_id]['marks'] = marks
    
    save_data(data)
    return JSONResponse(content={"message": "Student created successfully"}, status_code=201)



@app.put('/edit/{student_id}')
def update_student(student_id: str, student: UpdateStudent):
    data = load_data()
    
    if student_id not in data:
        raise HTTPException(status_code = 404, detail="Student not found")
    
    data[student_id].update(student.model_dump(exclude_unset=True))
    
    save_data(data)
    return JSONResponse(content={"message": "Student updated successfully"}, status_code=200)



@app.delete('/delete/{student_id}')
def delete_student(student_id: str):
    data = load_data()
    
    if student_id not in data:
        raise HTTPException(status_code = 404, detail="Student not found")
    
    del data[student_id]
    save_data(data)
    return JSONResponse(content={"message": "Student deleted successfully"}, status_code=200)