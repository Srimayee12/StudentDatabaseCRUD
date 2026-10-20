import ollama
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.crud import get_all_students

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

class AIQueryRequest(BaseModel):
    question: str

@router.post("/query")
async def ask_student_database(payload: AIQueryRequest):
    """Answer natural language questions about student records using local Ollama."""
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
        
        # 3. Call the local Ollama model (ensure Ollama is running locally with 'ollama run llama3.2:1b')
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return {
            "question": payload.question,
            "answer": response['message']['content']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))