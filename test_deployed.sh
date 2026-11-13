#!/bin/bash

echo "Testing deployed LLM chatbot..."
echo ""

URL="https://renderdeployement.onrender.com"

echo "1. Testing health endpoint..."
curl -s "$URL/health"
echo -e "\n"

echo "2. Testing root endpoint..."
curl -s "$URL/"
echo -e "\n"

echo "3. Testing chat with simple question..."
curl -s -X POST "$URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Python? Answer in one sentence."}' | python3 -m json.tool

echo -e "\nDone!"
