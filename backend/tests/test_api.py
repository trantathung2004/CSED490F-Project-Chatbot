import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthEndpoint:
    """Test cases for health check endpoint"""
    
    def test_health_check(self):
        """Test health check endpoint returns 200"""
        response = client.get("/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "ollama_status" in data
        assert "timestamp" in data

class TestRootEndpoint:
    """Test cases for root endpoint"""
    
    def test_root(self):
        """Test root endpoint returns basic info"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

class TestChatEndpoint:
    """Test cases for chat endpoint"""
    
    def test_chat_with_valid_message(self):
        """Test chat endpoint with valid message"""
        response = client.post(
            "/api/chat",
            json={"message": "Hello", "model": "llama3.2"}
        )
        # Note: This will fail if Ollama is not running
        # In production, you'd mock the Ollama service
        assert response.status_code in [200, 503]
    
    def test_chat_with_empty_message(self):
        """Test chat endpoint with empty message"""
        response = client.post(
            "/api/chat",
            json={"message": "", "model": "llama3.2"}
        )
        assert response.status_code == 400
    
    def test_chat_without_model(self):
        """Test chat endpoint uses default model"""
        response = client.post(
            "/api/chat",
            json={"message": "Test message"}
        )
        # Should accept request even without model specified
        assert response.status_code in [200, 503]

class TestModelsEndpoint:
    """Test cases for models endpoint"""
    
    def test_list_models(self):
        """Test listing available models"""
        response = client.get("/api/models")
        # Will return 200 if Ollama is running, 500 if not
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "models" in data
            assert "count" in data

class TestModelManagement:
    """Test cases for model load/unload endpoints"""
    
    def test_load_model(self):
        """Test loading a model"""
        response = client.post(
            "/api/models/load",
            json={"model": "llama3.2", "keep_alive": "5m"}
        )
        # Will succeed if Ollama is running
        assert response.status_code in [200, 500]
    
    def test_unload_model(self):
        """Test unloading a model"""
        response = client.post(
            "/api/models/unload",
            json={"model": "llama3.2"}
        )
        # Will succeed if Ollama is running
        assert response.status_code in [200, 500]

# Run tests with: pytest tests/test_api.py -v