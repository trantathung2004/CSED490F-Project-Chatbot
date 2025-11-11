#!/bin/bash

# Raspberry Pi Chatbot Server - Startup Script

echo "========================================"
echo "Starting Raspberry Pi Chatbot Server"
echo "========================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if Ollama is running
echo "Checking Ollama service..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✓ Ollama is running"
else
    echo "✗ Warning: Ollama is not responding on port 11434"
    echo "  Please make sure Ollama is installed and running:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo "  ollama pull llama3.2"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
fi

echo ""
echo "========================================"
echo "Starting FastAPI server..."
echo "========================================"
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/api/health"
echo ""

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload