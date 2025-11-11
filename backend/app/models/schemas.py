from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Request Models
class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    message: str = Field(..., min_length=1, description="User message to the chatbot")
    model: Optional[str] = Field(None, description="Ollama model to use (default: llama3.2)")
    stream: bool = Field(False, description="Whether to stream the response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Why is the sky blue?",
                "model": "llama3.2",
                "stream": False
            }
        }

class ModelLoadRequest(BaseModel):
    """
    Request model for loading a model
    """
    model: str = Field(..., description="Name of the model to load")
    keep_alive: Optional[str] = Field("5m", description="How long to keep model in memory")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model": "llama3.2",
                "keep_alive": "5m"
            }
        }

class ModelUnloadRequest(BaseModel):
    """
    Request model for unloading a model
    """
    model: str = Field(..., description="Name of the model to unload")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model": "llama3.2"
            }
        }

# Response Models
class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    response: str = Field(..., description="Chatbot response")
    model: str = Field(..., description="Model used for generation")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    processing_time: Optional[float] = Field(None, description="Time taken to generate response (seconds)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "The sky appears blue because of Rayleigh scattering...",
                "model": "llama3.2",
                "timestamp": "2025-11-10T12:00:00Z",
                "processing_time": 2.5
            }
        }

class HealthResponse(BaseModel):
    """
    Response model for health check endpoint
    """
    status: str = Field(..., description="Server status")
    ollama_status: str = Field(..., description="Ollama service status")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "ollama_status": "running",
                "timestamp": "2025-11-10T12:00:00Z"
            }
        }

class ModelInfo(BaseModel):
    """
    Model information
    """
    name: str
    size: Optional[str] = None
    modified_at: Optional[str] = None

class ModelsResponse(BaseModel):
    """
    Response model for listing models
    """
    models: List[ModelInfo]
    count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "models": [
                    {"name": "llama3.2", "size": "2.0GB", "modified_at": "2025-11-05"},
                    {"name": "gemma2_2b", "size": "1.5GB", "modified_at": "2025-11-06"}
                ],
                "count": 2
            }
        }

class ErrorResponse(BaseModel):
    """
    Error response model
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Model not found",
                "detail": "The requested model 'llama3.2' is not available",
                "timestamp": "2025-11-10T12:00:00Z"
            }
        }