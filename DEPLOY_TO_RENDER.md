# Deploy Free LLM Chatbot to Render

## What You Get
- ✅ 100% FREE (no credit card required)
- ✅ HTTPS endpoint with custom URL
- ✅ Uses Hugging Face's free inference API
- ✅ Model: Llama 3.2 3B Instruct
- ✅ 750 hours/month free tier

## Step 1: Get Hugging Face Token (FREE)

1. Go to https://huggingface.co/join
2. Create free account
3. Go to https://huggingface.co/settings/tokens
4. Click "New token"
5. Name it: `render-chatbot`
6. Type: **Read**
7. Copy the token (starts with `hf_...`)

## Step 2: Push Code to GitHub

```bash
cd /Users/apple/Desktop/zemoso/madireddyabhinavreddy_ldp/LangChainAndLLM/AI_Agents/deployment/render_free

# Initialize git if not already
git init
git add .
git commit -m "Add Render deployment"

# Create new repo on GitHub: llm-chatbot-render
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/llm-chatbot-render.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

1. Go to https://render.com/
2. Click "Get Started for Free"
3. Sign up with GitHub
4. Click "New +" → "Web Service"
5. Connect your GitHub repo: `llm-chatbot-render`
6. Settings:
   - **Name**: `llm-chatbot-free`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: **Free**

7. Click "Advanced" → "Add Environment Variable"
   - Key: `HF_TOKEN`
   - Value: Paste your Hugging Face token (`hf_...`)

8. Click "Create Web Service"

## Step 4: Wait for Deployment

Render will:
1. Build your app (2-3 minutes)
2. Deploy it
3. Give you a URL like: `https://llm-chatbot-free.onrender.com`

## Step 5: Test It

```bash
# Health check
curl https://llm-chatbot-free.onrender.com/health

# Send a message
curl -X POST https://llm-chatbot-free.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Python?"}'
```

## Important Notes

⚠️ **First request takes 20 seconds** - Hugging Face loads the model on first use
⚠️ **Free tier sleeps after 15 min inactivity** - First request after sleep takes 30 seconds to wake up
✅ **After that, responses are instant**

## Limits

- Render Free: 750 hours/month (enough for testing)
- Hugging Face: 1000 requests/hour (plenty for personal use)
- No credit card needed for either service

## Your Deployment Is Ready!

URL: `https://llm-chatbot-free.onrender.com`
Docs: `https://llm-chatbot-free.onrender.com/docs`
