import requests
import os

os.environ["HF_TOKEN"] = "your_token_here"

from app import app
import uvicorn

if __name__ == "__main__":
    print("Starting local server on http://localhost:8000")
    print("Test with: curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{\"message\": \"Hello\"}'")
    uvicorn.run(app, host="0.0.0.0", port=8000)
