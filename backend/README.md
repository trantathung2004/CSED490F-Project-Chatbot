# Raspberry Pi Chatbot Server

A lightweight FastAPI web server for enabling seamless interaction between a local chatbot application running on Raspberry Pi and external clients.

## Features

- ✅ REST API for bi-directional communication with Ollama chatbot
- ✅ Support for multiple LLM models (LLaMA 3.2, Gemma, etc.)
- ✅ Health monitoring and model management
- ✅ Minimal latency design optimized for edge computing
- ✅ Automatic API documentation with Swagger UI
- ✅ CORS enabled for cross-origin requests

## Architecture

```
Client Device → FastAPI Server → Ollama (LLaMA 3.2) → Response
```

## Prerequisites

- Raspberry Pi 4/5 (4GB+ RAM recommended)
- Raspberry Pi OS (64-bit) or Ubuntu Server
- Python 3.10 or higher
- Ollama installed and running

## Installation

### 1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull LLaMA 3.2 Model

```bash
ollama pull llama3.2
```

Verify installation:
```bash
ollama list
```

### 3. Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/trantathung2004/CSED490F-Project-Chatbot
cd CSED490F-Project-Chatbot
```

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Usage

### Start the Server

```bash
./run.sh
```

The server will start on `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/api/health
```

#### 2. Chat with Chatbot
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Why is the sky blue?",
    "model": "llama3.2"
  }'
```

#### 3. List Available Models
```bash
curl http://localhost:8000/api/models
```

#### 4. Load Model into Memory
```bash
curl -X POST http://localhost:8000/api/models/load \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "keep_alive": "5m"
  }'
```

#### 5. Unload Model from Memory
```bash
curl -X POST http://localhost:8000/api/models/unload \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2"}'
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Project Structure

```
project1-chatbot-server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── ollama_service.py   # Ollama integration
│   └── core/
│       ├── __init__.py
│       └── config.py           # Configuration
├── tests/
│   ├── __init__.py
│   └── test_api.py            # API tests
├── requirements.txt
├── .env.example
├── .env
├── run.sh
└── README.md
```

## Configuration

Edit `.env` file to customize settings:

```env
# Server
HOST=0.0.0.0
PORT=8000

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3.2
OLLAMA_TIMEOUT=120
```

## Testing

Run tests:
```bash
source venv/bin/activate
pytest tests/ -v
```

## Performance Optimization

### Keep Model in Memory
To reduce latency, keep the model loaded in memory:
```bash
curl -X POST http://localhost:8000/api/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "keep_alive": "30m"}'
```

### Monitor Performance
Check response times in the API response:
```json
{
  "response": "...",
  "model": "llama3.2",
  "processing_time": 2.5
}
```

## Troubleshooting

### Ollama Not Running
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start Ollama (it should auto-start after installation)
ollama serve
```

### Port Already in Use
Change the port in `.env` or run with custom port:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Model Not Found
List available models:
```bash
ollama list
```

Pull a new model:
```bash
ollama pull llama3.2
```

## Accessing from External Devices

To access from other devices on the same network:

1. Find your Raspberry Pi's IP address:
```bash
hostname -I
```

2. Access from external device:
```
http://<raspberry-pi-ip>:8000
```

Example:
```bash
curl http://192.168.1.100:8000/api/health
```

## Running as System Service

To run the server automatically on boot, create a systemd service:

```bash
sudo nano /etc/systemd/system/chatbot-server.service
```

Add:
```ini
[Unit]
Description=Raspberry Pi Chatbot Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/project1-chatbot-server
ExecStart=/home/pi/project1-chatbot-server/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable chatbot-server
sudo systemctl start chatbot-server
sudo systemctl status chatbot-server
```

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Authors

- Team 13
- Course: CSED490F - Deep Learning Implementation
- Date: November 2025