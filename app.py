from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
from pathlib import Path

app = FastAPI(title="Free LLM Chatbot with Gemini")

@app.get("/", response_class=HTMLResponse)
def root():
    html_path = Path(__file__).parent / "templates" / "index.html"
    return html_path.read_text()

@app.get("/api")
def api_info():
    return {
        "message": "Free LLM Chatbot API with Auto-Failover",
        "status": "running",
        "models": {
            "primary": "Gemini 2.5 Flash",
            "backups": [
                "Gemini 3.8 Flash",
                "Gemini 3.6 Flash", 
                "Gemini 3 Flash",
                "Gemini 4 Hydrogen",
                "Gemini 2.5 Flash Lite",
                "Gemini 3.1 Flash Lite"
            ]
        },
        "endpoints": {
            "GET /": "Chat UI",
            "POST /chat": "Send a message (auto-failover)",
            "GET /health": "Health check",
            "GET /api": "API info"
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
    
    # Backup models in priority order (7 models for maximum reliability)
    models = [
        "gemini-2.5-flash",      # Primary - Best quality
        "gemini-3.8-flash",      # Backup 1
        "gemini-3.6-flash",      # Backup 2
        "gemini-3-flash",        # Backup 3
        "gemini-4-hydrogen",     # Backup 4
        "gemini-2.5-flash-lite", # Backup 5 - Lite but fast
        "gemini-3.1-flash-lite"  # Backup 6 - Last resort
    ]
    
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
    
    last_error = None
    
    for model_name in models:
        try:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
            response = requests.post(api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if "candidates" in result and len(result["candidates"]) > 0:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "response": text,
                        "model": model_name
                    }
            elif response.status_code == 429:
                # Rate limit hit, try next model
                last_error = f"{model_name}: Rate limit exceeded"
                continue
            else:
                last_error = f"{model_name}: API Error {response.status_code}"
                continue
                
        except requests.exceptions.Timeout:
            last_error = f"{model_name}: Timeout"
            continue
        except Exception as e:
            last_error = f"{model_name}: {str(e)}"
            continue
    
    # All models failed
    return {
        "response": f"All models failed. Last error: {last_error}",
        "model": "error"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
