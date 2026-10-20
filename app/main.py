import ollama
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.models import create_table
from app.crud import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student,
)

app = FastAPI(
    title="Student Database CRUD API",
    description="A REST API to manage student records using FastAPI, SQLite, and optional Ollama AI.",
    version="1.0.0",
)


# Initialize DB table on startup
@app.on_event("startup")
def startup_event():
    create_table()


# --- Pydantic Schemas ---
class StudentInput(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(..., gt=0)
    course: str = Field(..., min_length=1)


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    course: str


class AIQueryRequest(BaseModel):
    question: str


# --- Core CRUD Endpoints ---
@app.get("/", tags=["General"])
def home():
    return {
        "message": "Welcome to the Student Database CRUD API",
        "docs": "/docs",
        "endpoints": {
            "list_students": "GET /students",
            "create_student": "POST /students",
            "get_student": "GET /students/{student_id}",
            "update_student": "PUT /students/{student_id}",
            "delete_student": "DELETE /students/{student_id}",
            "ai_query": "POST /ai/query",
        },
    }


@app.get("/students", response_model=list[StudentResponse], tags=["Students"])
def list_students():
    """List all students ordered by ID."""
    return get_all_students()


@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
def add_student(student: StudentInput):
    """Add a new student record to the database."""
    try:
        student_id = create_student(
            student.name, student.email, student.age, student.course
        )
        return {
            "id": student_id,
            "name": student.name.strip(),
            "email": student.email.strip().lower(),
            "age": student.age,
            "course": student.course.strip(),
        }
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as err:
        if "UNIQUE constraint failed" in str(err):
            raise HTTPException(status_code=400, detail="Email address is already registered.")
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def read_student(student_id: int):
    """Retrieve a single student by ID."""
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@app.put("/students/{student_id}", response_model=dict, tags=["Students"])
def edit_student(student_id: int, student: StudentInput):
    """Update an existing student's details."""
    try:
        success = update_student(
            student_id, student.name, student.email, student.age, student.course
        )
        if not success:
            raise HTTPException(status_code=404, detail="Student not found.")
        return {"message": "Student updated successfully."}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as err:
        if "UNIQUE constraint failed" in str(err):
            raise HTTPException(status_code=400, detail="Email address is already registered.")
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def remove_student(student_id: int):
    """Delete a student record by ID."""
    success = delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found.")
    return None


# --- Optional Bonus: Ollama AI Assistant Endpoint ---
@app.post("/ai/query", tags=["AI Assistant"])
async def ask_student_database(payload: AIQueryRequest):
    """Answer natural-language questions about student records using local Ollama."""
    try:
        # 1. Fetch current database records as context
        students = get_all_students()

        # 2. Construct a prompt providing the database context securely
        prompt = (
            f"You are a helpful assistant for a student database.\n"
            f"Here are the current student records in JSON format:\n{students}\n\n"
            f"User Question: {payload.question}\n"
            f"Answer accurately and concisely based ONLY on the provided records."
        )

        # 3. Call the local Ollama model
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "question": payload.question,
            "answer": response["message"]["content"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query Ollama. Make sure Ollama is running locally: {str(e)}"
        )