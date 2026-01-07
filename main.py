from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
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
    prompt = f"""
    You are a senior DevOps engineer.
    Analyze the following {req.category} and provide:
    - Short explanation of the issue
    - Possible root causes
    - Actionable fixes
    
    Input:
    {req.content}
    """
    
    response = model.generate_content(prompt)
    
    return {
        "analysis": response.text
    }