# Free LLM Chatbot - Render Deployment

## 🚀 Truly FREE Deployment (No Credit Card)

This chatbot uses:
- **Render** (free hosting, 750 hours/month)
- **Hugging Face Inference API** (free, 1000 requests/hour)
- **Llama 3.2 3B Instruct** model

## Quick Deploy (5 minutes)

### 1. Get Hugging Face Token
```bash
# Go to: https://huggingface.co/settings/tokens
# Click "New token" → Name: render-chatbot → Type: Read
# Copy the token (hf_...)
```

### 2. Push to GitHub
```bash
cd deployment/render_free
git init
git add .
git commit -m "Free LLM chatbot"

# Create repo on GitHub: llm-chatbot-render
git remote add origin https://github.com/YOUR_USERNAME/llm-chatbot-render.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub (FREE)
3. New + → Web Service
4. Connect your repo
5. Settings:
   - Name: `llm-chatbot-free`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type: Free**
6. Add environment variable:
   - Key: `HF_TOKEN`
   - Value: Your token
7. Click "Create Web Service"

### 4. Test It
```bash
# Your URL: https://llm-chatbot-free.onrender.com

curl https://llm-chatbot-free.onrender.com/chat \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "What is AI?"}'
```

## Features

✅ 100% free (no credit card)
✅ HTTPS endpoint
✅ Auto-scaling
✅ 750 hours/month
✅ Custom domain support (optional)

## Limits

- First request: 20 seconds (model loading)
- Sleeps after 15 min inactivity
- Wake up time: 30 seconds
- After that: instant responses

## API Endpoints

- `GET /` - API info
- `POST /chat` - Send message
- `GET /health` - Health check
- `GET /docs` - Swagger UI

Perfect for learning, testing, and small projects!
