# Complete Setup Guide - Raspberry Pi Chatbot Server

## Table of Contents
1. [Hardware Requirements](#hardware-requirements)
2. [Initial Raspberry Pi Setup](#initial-raspberry-pi-setup)
3. [Installing Ollama](#installing-ollama)
4. [Project Setup](#project-setup)
5. [Testing the Server](#testing-the-server)
6. [Accessing from External Devices](#accessing-from-external-devices)
7. [Running as System Service](#running-as-system-service)
8. [Troubleshooting](#troubleshooting)

---

## Hardware Requirements

- **Raspberry Pi 4 or 5** (4GB RAM minimum, 8GB recommended)
- **MicroSD Card**: 32GB minimum (64GB recommended)
- **Power Supply**: Official Raspberry Pi power adapter
- **Network**: Ethernet or WiFi connection
- **Optional**: Monitor, keyboard, mouse for initial setup

---

## Initial Raspberry Pi Setup

### 1. Install Raspberry Pi OS

```bash
# Use Raspberry Pi Imager to install:
# - Raspberry Pi OS (64-bit) - Recommended
# - Or Ubuntu Server 22.04 LTS (64-bit)
```

### 2. First Boot Configuration

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3 python3-pip python3-venv -y

# Install essential tools
sudo apt install curl git build-essential -y

# Verify Python version
python3 --version  # Should be 3.10 or higher
```

### 3. Configure Network (if using WiFi)

```bash
# Edit WiFi configuration
sudo raspi-config
# Navigate to: System Options > Wireless LAN
```

---

## Installing Ollama

### 1. Install Ollama

```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Verify Installation

```bash
# Check Ollama version
ollama --version

# Check if Ollama service is running
curl http://localhost:11434/api/tags
```

### 3. Pull LLaMA 3.2 Model

```bash
# Pull the model (this will download ~2GB)
ollama pull llama3.2

# Verify model is installed
ollama list
```

Expected output:
```
NAME            ID              SIZE    MODIFIED
llama3.2:latest dde5aa3fc5ff    2.0 GB  X minutes ago
```

### 4. Test Ollama

```bash
# Test the model interactively
ollama run llama3.2

# Type a message and press Enter
>>> Hello, who are you?

# Exit with /bye
>>> /bye
```

---

## Project Setup

### 1. Clone or Create Project Directory

```bash
# Navigate to home directory
cd ~

# Create project directory
mkdir project1-chatbot-server
cd project1-chatbot-server
```

### 2. Create Project Structure

```bash
# Create directory structure
mkdir -p app/api app/models app/services app/core tests client screenshots

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
touch app/core/__init__.py
touch tests/__init__.py
```

### 3. Add All Project Files

Copy all the files from the artifacts:
- `requirements.txt`
- `app/main.py`
- `app/core/config.py`
- `app/models/schemas.py`
- `app/services/ollama_service.py`
- `app/api/routes.py`
- `.env.example`
- `run.sh`
- `test_connection.py`
- `.gitignore`
- `README.md`

### 4. Setup Environment

```bash
# Make run.sh executable
chmod +x run.sh
chmod +x test_connection.py

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 5. Configure Environment Variables

Edit `.env` file if needed:
```bash
nano .env
```

Default configuration should work:
```env
HOST=0.0.0.0
PORT=8000
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3.2
```

---

## Testing the Server

### 1. Start the Server

```bash
# Using the run script (recommended)
./run.sh

# Or manually
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Expected output:
```
========================================
Starting Raspberry Pi Chatbot Server
========================================
✓ Ollama is running
========================================
Starting FastAPI server...
========================================
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Test with Browser

Open a browser and navigate to:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### 3. Test with curl

```bash
# In a new terminal

# 1. Health Check
curl http://localhost:8000/api/health

# 2. List Models
curl http://localhost:8000/api/models

# 3. Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Tell me a joke.", "model": "llama3.2"}'
```

### 4. Run Automated Test Script

```bash
# In a new terminal
cd ~/project1-chatbot-server
source venv/bin/activate
python3 test_connection.py
```

---

## Accessing from External Devices

### 1. Find Raspberry Pi IP Address

```bash
hostname -I
```

Example output: `192.168.1.100`

### 2. Test from Another Device

From your laptop/phone on the same network:

```bash
# Replace with your Raspberry Pi's IP
curl http://192.168.1.100:8000/api/health

# Or open in browser
http://192.168.1.100:8000/docs
```

### 3. Firewall Configuration (if needed)

```bash
# Allow port 8000
sudo ufw allow 8000
sudo ufw status
```

---

## Running as System Service

To automatically start the server on boot:

### 1. Create Systemd Service

```bash
# Copy the service file
sudo cp chatbot-server.service /etc/systemd/system/

# Or create it manually
sudo nano /etc/systemd/system/chatbot-server.service
```

### 2. Edit Service File

Make sure paths are correct in the service file:
```ini
WorkingDirectory=/home/pi/project1-chatbot-server
ExecStart=/home/pi/project1-chatbot-server/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable chatbot-server

# Start service now
sudo systemctl start chatbot-server

# Check status
sudo systemctl status chatbot-server
```

### 4. Service Management Commands

```bash
# Stop service
sudo systemctl stop chatbot-server

# Restart service
sudo systemctl restart chatbot-server

# View logs
sudo journalctl -u chatbot-server -f

# Disable auto-start
sudo systemctl disable chatbot-server
```

---

## Troubleshooting

### Problem: Ollama Not Running

```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# If not responding, restart Ollama
sudo systemctl restart ollama

# Or manually start
ollama serve
```

### Problem: Port Already in Use

```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use a different port
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Problem: Module Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: Slow Response Times

```bash
# Keep model loaded in memory
curl -X POST http://localhost:8000/api/models/load \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "keep_alive": "30m"}'

# Use a smaller model
ollama pull phi
# Update .env: OLLAMA_DEFAULT_MODEL=phi
```

### Problem: Out of Memory

```bash
# Check memory usage
free -h

# Add swap space (if not already present)
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# Use a quantized model (already default)
# LLaMA 3.2 uses Q4 quantization
```

### Problem: Can't Access from External Device

```bash
# Check server is listening on 0.0.0.0
netstat -tuln | grep 8000

# Check firewall
sudo ufw status
sudo ufw allow 8000

# Verify network connectivity
ping <raspberry-pi-ip>
```

### View Server Logs

```bash
# If running as service
sudo journalctl -u chatbot-server -f

# If running manually
# Logs will appear in the terminal
```

---

## Performance Tips

1. **Keep Model Loaded**: Use the `/api/models/load` endpoint with `keep_alive: "30m"`
2. **Use Smaller Models**: For faster responses, try `phi` or `tinyllama`
3. **Enable Swap**: Helps with memory-intensive operations
4. **Close Unnecessary Services**: Free up RAM
5. **Use Ethernet**: More stable than WiFi for continuous operation

---

## Next Steps

- Proceed to create a web client (frontend)
- Test with multiple concurrent clients
- Measure latency and performance
- Take screenshots for the report
- Document your implementation details

---

## Useful Commands Reference

```bash
# Server Management
./run.sh                          # Start server
uvicorn app.main:app --reload     # Start with auto-reload
pkill -f uvicorn                  # Stop server

# Ollama Management
ollama list                       # List models
ollama pull <model>              # Download model
ollama rm <model>                # Remove model
ollama serve                     # Start Ollama

# Testing
python3 test_connection.py       # Run test script
pytest tests/ -v                 # Run unit tests
curl http://localhost:8000/docs  # View API docs

# System
hostname -I                      # Get IP address
htop                            # Monitor resources
df -h                           # Check disk space
free -h                         # Check memory
```

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check Ollama documentation: https://github.com/ollama/ollama
4. Review FastAPI documentation: https://fastapi.tiangolo.com/

Good luck with your project! 🚀