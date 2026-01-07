from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai
from rag import retrieve_context 

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")

app = FastAPI(title="AI DevOps Analyzer")

class AnalyzeRequest(BaseModel):
    category: str
    content: str
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI DevOps Analyzer API!"}
    
@app.post("/analyze")
def analyze_log(req: AnalyzeRequest):
    context = retrieve_context(req.content)
    prompt = f"""
    You are a senior DevOps engineer.
    
    INTERNAL KNOWLEDGE:
    {context}
    
    Analyze the following {req.category} and provide:
    - Short explanation of the issue
    - Possible root causes
    - Actionable fixes
    
    Input:
    {req.content}
    """
    
    response = model.generate_content(prompt)
    
    return {
        "analysis": response.text,
        "used_rag": bool(context)
    }
    
@app.get("/health")
def health_check():
    return {"status": "ok"}