import httpx
from typing import Optional, Dict, Any, List
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaService:
    """
    Service class for interacting with Ollama API
    """
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.timeout = settings.OLLAMA_TIMEOUT
        self.default_model = settings.OLLAMA_DEFAULT_MODEL
        
    async def check_health(self) -> bool:
        """
        Check if Ollama service is running
        
        Returns:
            bool: True if Ollama is accessible, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False
    
    async def chat(
        self, 
        message: str, 
        model: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Send a chat message to Ollama
        
        Args:
            message: User message
            model: Model name (default: llama3.2)
            conversation_history: Previous conversation messages
            
        Returns:
            Dict containing the response and metadata
        """
        model = model or self.default_model
        
        # Prepare messages
        messages = conversation_history or []
        messages.append({
            "role": "user",
            "content": message
        })
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    "response": data.get("message", {}).get("content", ""),
                    "model": model,
                    "done": data.get("done", False),
                    "total_duration": data.get("total_duration"),
                    "load_duration": data.get("load_duration"),
                    "prompt_eval_count": data.get("prompt_eval_count"),
                    "eval_count": data.get("eval_count")
                }
                
        except httpx.TimeoutException:
            logger.error(f"Timeout while communicating with Ollama (model: {model})")
            raise Exception(f"Request timeout - model '{model}' took too long to respond")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Ollama: {e}")
            raise Exception(f"Ollama API error: {e.response.text}")
        except Exception as e:
            logger.error(f"Unexpected error communicating with Ollama: {e}")
            raise Exception(f"Failed to communicate with Ollama: {str(e)}")
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available Ollama models
        
        Returns:
            List of model information dictionaries
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
                
                models = []
                for model in data.get("models", []):
                    models.append({
                        "name": model.get("name", ""),
                        "size": self._format_size(model.get("size", 0)),
                        "modified_at": model.get("modified_at", "")
                    })
                
                return models
                
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            raise Exception(f"Failed to retrieve model list: {str(e)}")
    
    async def load_model(self, model: str, keep_alive: str = "5m") -> Dict[str, Any]:
        """
        Load a model into memory
        
        Args:
            model: Model name
            keep_alive: How long to keep model in memory
            
        Returns:
            Dict containing load status
        """
        payload = {
            "model": model,
            "keep_alive": keep_alive
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                
                return {
                    "status": "loaded",
                    "model": model,
                    "keep_alive": keep_alive
                }
                
        except Exception as e:
            logger.error(f"Failed to load model {model}: {e}")
            raise Exception(f"Failed to load model: {str(e)}")
    
    async def unload_model(self, model: str) -> Dict[str, Any]:
        """
        Unload a model from memory
        
        Args:
            model: Model name
            
        Returns:
            Dict containing unload status
        """
        payload = {
            "model": model,
            "keep_alive": 0
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                
                return {
                    "status": "unloaded",
                    "model": model
                }
                
        except Exception as e:
            logger.error(f"Failed to unload model {model}: {e}")
            raise Exception(f"Failed to unload model: {str(e)}")
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """
        Format size in bytes to human-readable format
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}PB"

# Create a singleton instance
ollama_service = OllamaService()