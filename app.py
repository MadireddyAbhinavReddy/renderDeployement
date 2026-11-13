from fastapi import FastAPI, HTTPException
import httpx
import os
import asyncio

app = FastAPI(title="Free LLM Chatbot")

async def call_hf_api(message: str, token: str):
    api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "inputs": message,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(api_url, headers=headers, json=payload)
        return response

@app.get("/")
def root():
    return {
        "message": "Free LLM Chatbot API",
        "status": "running",
        "endpoints": {
            "POST /chat": "Send a message",
            "GET /health": "Health check"
        }
    }

@app.post("/chat")
async def chat(request: dict):
    message = request.get("message", "")
    hf_token = os.getenv("HF_TOKEN", "")
    
    if not hf_token:
        return {
            "response": "Please set HF_TOKEN environment variable",
            "model": "error"
        }
    
    try:
        response = await call_hf_api(message, hf_token)
        
        if response.status_code == 503:
            return {
                "response": "Model is loading, try again in 20 seconds",
                "model": "llama-3.2-3b"
            }
        
        if response.status_code != 200:
            return {
                "response": f"API Error: {response.status_code} - {response.text[:200]}",
                "model": "error"
            }
        
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            text = result[0].get("generated_text", "No response")
        else:
            text = str(result)
        
        return {
            "response": text,
            "model": "llama-3.2-3b"
        }
    
    except httpx.TimeoutException:
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
