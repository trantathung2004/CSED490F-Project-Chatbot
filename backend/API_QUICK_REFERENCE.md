# API Quick Reference

## Base URL
```
http://localhost:8000
```

## Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API info |
| `/docs` | GET | Interactive API documentation |
| `/api/health` | GET | Health check |
| `/api/chat` | POST | Send message to chatbot |
| `/api/models` | GET | List available models |
| `/api/models/load` | POST | Load model into memory |
| `/api/models/unload` | POST | Unload model from memory |

---

## 1. Root Endpoint

**GET** `/`

Returns basic API information.

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "Raspberry Pi Chatbot Server API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/api/health"
}
```

---

## 2. Health Check

**GET** `/api/health`

Check server and Ollama status.

```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "ollama_status": "running",
  "timestamp": "2025-11-10T12:00:00Z"
}
```

---

## 3. Chat Endpoint

**POST** `/api/chat`

Send a message to the chatbot and get a response.

### Request Body:
```json
{
  "message": "Why is the sky blue?",
  "model": "llama3.2",
  "stream": false
}
```

### Fields:
- `message` (required): User message (string)
- `model` (optional): Model name (default: "llama3.2")
- `stream` (optional): Stream response (default: false)

### Example:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum computing in simple terms",
    "model": "llama3.2"
  }'
```

### Response:
```json
{
  "response": "Quantum computing is a type of computing that uses quantum bits...",
  "model": "llama3.2",
  "timestamp": "2025-11-10T12:00:00Z",
  "processing_time": 2.5
}
```

---

## 4. List Models

**GET** `/api/models`

Get a list of all available Ollama models.

```bash
curl http://localhost:8000/api/models
```

**Response:**
```json
{
  "models": [
    {
      "name": "llama3.2:latest",
      "size": "2.0GB",
      "modified_at": "2025-11-05T10:30:00Z"
    },
    {
      "name": "phi:latest",
      "size": "1.3GB",
      "modified_at": "2025-11-06T14:20:00Z"
    }
  ],
  "count": 2
}
```

---

## 5. Load Model

**POST** `/api/models/load`

Load a model into memory for faster inference.

### Request Body:
```json
{
  "model": "llama3.2",
  "keep_alive": "5m"
}
```

### Fields:
- `model` (required): Model name (string)
- `keep_alive` (optional): Keep in memory duration (default: "5m")
  - Examples: "5m", "30m", "1h", "0" (unload immediately)

### Example:
```bash
curl -X POST http://localhost:8000/api/models/load \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "keep_alive": "30m"
  }'
```

**Response:**
```json
{
  "status": "loaded",
  "model": "llama3.2",
  "keep_alive": "30m"
}
```

---

## 6. Unload Model

**POST** `/api/models/unload`

Unload a model from memory to free resources.

### Request Body:
```json
{
  "model": "llama3.2"
}
```

### Example:
```bash
curl -X POST http://localhost:8000/api/models/unload \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2"}'
```

**Response:**
```json
{
  "status": "unloaded",
  "model": "llama3.2"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Message cannot be empty"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "detail": "Failed to process chat request: Connection timeout"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Ollama service is not available"
}
```

---

## Testing Examples

### Python Example

```python
import requests

# Chat with the bot
response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "Hello, how are you?"}
)
print(response.json()["response"])
```

### JavaScript Example

```javascript
// Chat with the bot
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'Hello, how are you?',
    model: 'llama3.2'
  })
})
.then(res => res.json())
.then(data => console.log(data.response));
```

### Test Multiple Requests

```bash
#!/bin/bash

# Test script
echo "Testing chat with multiple questions..."

questions=(
  "What is AI?"
  "Explain machine learning"
  "What is deep learning?"
)

for question in "${questions[@]}"; do
  echo -e "\nQ: $question"
  response=$(curl -s -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"$question\"}")
  echo "A: $(echo $response | jq -r '.response')"
  echo "Time: $(echo $response | jq -r '.processing_time')s"
done
```

---

## Performance Optimization

### 1. Pre-load Model
```bash
# Load model at startup to reduce first-request latency
curl -X POST http://localhost:8000/api/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "keep_alive": "60m"}'
```

### 2. Keep Model in Memory
```bash
# Set long keep_alive duration
curl -X POST http://localhost:8000/api/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "keep_alive": "24h"}'
```

---

## Common Use Cases

### 1. Simple Q&A Bot
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'
```

### 2. Code Explanation
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain this Python code: def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"}'
```

### 3. Creative Writing
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a short poem about autumn"}'
```

---

## Monitoring

### Check Server Status
```bash
# Health check
curl http://localhost:8000/api/health

# List loaded models
curl http://localhost:8000/api/models
```

### View API Documentation
Open in browser: `http://localhost:8000/docs`

---

## Rate Limiting & Best Practices

1. **Concurrent Requests**: Server supports async handling
2. **Timeout**: Default 120 seconds for chat requests
3. **Model Management**: Unload unused models to save memory
4. **Error Handling**: Always check response status codes
5. **Keep Alive**: Balance between memory usage and response time

---

## Quick Tips

✅ Use `/docs` for interactive API testing
✅ Pre-load frequently used models
✅ Check `/health` before starting long sessions
✅ Set appropriate `keep_alive` values
✅ Monitor processing times for performance tuning

---

## Need Help?

- Interactive Docs: http://localhost:8000/docs
- GitHub Issues: [Your repo URL]
- Ollama Docs: https://github.com/ollama/ollama
- FastAPI Docs: https://fastapi.tiangolo.com/