from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import time
import logging

from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    ModelsResponse,
    ModelInfo,
    ModelLoadRequest,
    ModelUnloadRequest,
    ErrorResponse
)
from app.services.ollama_service import ollama_service

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the server and Ollama service"
)
async def health_check():
    """
    Health check endpoint to verify server and Ollama service status
    """
    try:
        ollama_healthy = await ollama_service.check_health()
        
        return HealthResponse(
            status="healthy" if ollama_healthy else "degraded",
            ollama_status="running" if ollama_healthy else "unavailable",
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            ollama_status="error",
            timestamp=datetime.now()
        )

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with Chatbot",
    description="Send a message to the chatbot and receive a response",
    responses={
        200: {"model": ChatResponse},
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        503: {"model": ErrorResponse, "description": "Ollama service unavailable"}
    }
)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for bi-directional communication with the chatbot
    
    Args:
        request: ChatRequest containing user message and optional model name
        
    Returns:
        ChatResponse with the chatbot's response and metadata
    """
    start_time = time.time()
    
    try:
        # Validate that message is not empty
        if not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )
        
        # Check Ollama service health
        if not await ollama_service.check_health():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Ollama service is not available"
            )
        
        # Get response from Ollama
        result = await ollama_service.chat(
            message=request.message,
            model=request.model
        )
        
        processing_time = time.time() - start_time
        
        logger.info(f"Chat request processed in {processing_time:.2f}s using model {result['model']}")
        
        return ChatResponse(
            response=result["response"],
            model=result["model"],
            timestamp=datetime.now(),
            processing_time=round(processing_time, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )

@router.get(
    "/models",
    response_model=ModelsResponse,
    summary="List Available Models",
    description="Get a list of all available Ollama models"
)
async def list_models():
    """
    List all available models in Ollama
    
    Returns:
        ModelsResponse containing list of available models
    """
    try:
        models_data = await ollama_service.list_models()
        
        models = [
            ModelInfo(
                name=m["name"],
                size=m.get("size"),
                modified_at=m.get("modified_at")
            )
            for m in models_data
        ]
        
        return ModelsResponse(
            models=models,
            count=len(models)
        )
        
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve model list: {str(e)}"
        )

@router.post(
    "/models/load",
    summary="Load Model",
    description="Load a specific model into memory"
)
async def load_model(request: ModelLoadRequest):
    """
    Load a model into memory for faster inference
    
    Args:
        request: ModelLoadRequest with model name and keep_alive duration
        
    Returns:
        Dict with load status
    """
    try:
        result = await ollama_service.load_model(
            model=request.model,
            keep_alive=request.keep_alive
        )
        
        logger.info(f"Model {request.model} loaded successfully")
        return result
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load model: {str(e)}"
        )

@router.post(
    "/models/unload",
    summary="Unload Model",
    description="Unload a model from memory"
)
async def unload_model(request: ModelUnloadRequest):
    """
    Unload a model from memory to free resources
    
    Args:
        request: ModelUnloadRequest with model name
        
    Returns:
        Dict with unload status
    """
    try:
        result = await ollama_service.unload_model(model=request.model)
        
        logger.info(f"Model {request.model} unloaded successfully")
        return result
        
    except Exception as e:
        logger.error(f"Failed to unload model: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unload model: {str(e)}"
        )