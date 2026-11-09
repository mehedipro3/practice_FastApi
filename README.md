# 🚀 Todo List API – FastAPI

A simple and efficient **Todo List REST API** built with **FastAPI** as my first hands-on project exploring Python backend development.

This project helped me understand how to build RESTful APIs, perform CRUD operations, validate request data, and deploy a backend application.

## 🌐 Live Demo

- **Live API:** https://practice-fastapi-cp6x.onrender.com/
- **Interactive API Documentation (Swagger UI):** https://practice-fastapi-cp6x.onrender.com/docs
- **GitHub Repository:** https://github.com/mehedipro3/practice_FastApi

## ✨ Features

- Create new todo tasks
- Retrieve todo tasks
- Update existing tasks
- Delete todo tasks
- RESTful API architecture
- Automatic API documentation with Swagger UI
- Request validation using Pydantic
- Cloud deployment using Render

## 🛠️ Technologies Used

- **Python** – Programming language
- **FastAPI** – Backend web framework
- **Pydantic** – Data validation
- **Uvicorn** – ASGI server
- **Render** – Application deployment

## 📂 Project Structure

```text
practice_FastApi/
│
├── main.py
├── requirements.txt
└── README.md
```

*Adjust the structure above if your actual repository contains additional files or folders.*

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mehedipro3/practice_FastApi.git
```

### 2. Navigate to the Project Directory

```bash
cd practice_FastApi
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The application will run locally at:

```text
http://127.0.0.1:8000
```

## 📚 API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

## 🔗 API Endpoints

The following is a conventional CRUD endpoint design. Update the paths and methods to match your actual implementation.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/todos` | Get all todos |
| GET | `/todos/{id}` | Get a specific todo |
| POST | `/todos` | Create a new todo |
| PUT | `/todos/{id}` | Update a todo |
| DELETE | `/todos/{id}` | Delete a todo |

## 🚀 Deployment

This project is deployed using **Render**.

- Live Application: https://fastapi-project-uat0.onrender.com/
- Swagger Documentation: https://fastapi-project-uat0.onrender.com/docs

## 📖 What I Learned

Through this project, I gained practical experience with:

- Understanding FastAPI fundamentals
- Building RESTful APIs
- Implementing CRUD operations
- Working with HTTP methods and status codes
- Validating data using Pydantic
- Exploring automatic API documentation
- Running and deploying Python backend applications

## 🎯 Future Improvements

- Integrate PostgreSQL for persistent data storage
- Implement database migrations using Alembic
- Add JWT-based authentication
- Introduce user-specific todo management
- Improve error handling and API security
- Add automated testing

## 🙌 Acknowledgment

This is my first hands-on project using FastAPI. It was a valuable learning experience, and I'm excited to continue exploring Python backend development and AI engineering.

**Learning, building, and improving every day!** 🚀

---

⭐ If you find this project interesting, feel free to explore the repository and share your feedback!
