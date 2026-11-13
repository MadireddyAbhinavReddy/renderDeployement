from fastapi import FastAPI
import requests
import os

app = FastAPI(title="Free LLM Chatbot with Gemini")

@app.get("/")
def root():
    return {
        "message": "Free LLM Chatbot API",
        "status": "running",
        "model": "Google Gemini 2.0 Flash",
        "endpoints": {
            "POST /chat": "Send a message",
            "GET /health": "Health check"
        }
    }

@app.post("/chat")
def chat(request: dict):
    message = request.get("message", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    
    if not gemini_key:
        return {
            "response": "Please set GEMINI_API_KEY environment variable",
            "model": "error"
        }
    
    if not message:
        return {
            "response": "Please provide a message",
            "model": "error"
        }
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={gemini_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": message
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 200
        }
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code != 200:
            return {
                "response": f"API Error: {response.status_code} - {response.text[:200]}",
                "model": "error"
            }
        
        result = response.json()
        
        if "candidates" in result and len(result["candidates"]) > 0:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            text = "No response from Gemini"
        
        return {
            "response": text,
            "model": "gemini-2.0-flash-exp"
        }
    
    except requests.exceptions.Timeout:
        return {
            "response": "Request timed out. Please try again.",
            "model": "error"
        }
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "model": "error"
        }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
