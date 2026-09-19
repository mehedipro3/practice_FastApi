from fastapi import FastAPI,Path,HTTPException,Query
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
    
    
    
@app.get("/sort")
def sort_students(sorted_by: str = Query(..., description="The field to sort students by"), order : str = Query(description = "sort by asc or desc")):
    
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