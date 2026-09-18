from fastapi import FastAPI,Path,HTTPException
import json

app = FastAPI()

def load_data():
    with open('students.json','r') as f:
        data = json.load(f)
    return data

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
def view_students(student_id: str = Path(..., description="The ID of the student to retrieve" , example="S002")):
    data = load_data()
    
    
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code = 404, detail="Student not found")