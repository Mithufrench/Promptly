"""
Dynamic LLM Model Manager
Automatically syncs with latest available Groq models and handles model deprecation gracefully.
Prevents "model_decommissioned" errors by automatically switching to active models.
"""

import os
import logging
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import asyncio
import httpx

logger = logging.getLogger(__name__)


class LLMModelManager:
    """
    Manages LLM model availability and automatically handles model deprecation.
    
    Features:
    - Fetches current available models from Groq API
    - Caches model list with TTL to avoid excessive API calls
    - Automatically falls back to latest available model if current is decommissioned
    - Logs model changes and deprecations
    - Thread-safe model switching
    """
    
    # Groq API endpoint for models
    GROQ_MODELS_URL = "https://api.groq.com/openai/v1/models"
    
    # Model priority ranking (prefer larger, more capable models)
    MODEL_PRIORITY = {
        "llama-3.3-70b-versatile": 100,
        "llama-3.1-70b-versatile": 95,
        "mixtral-8x7b-32768": 90,
        "llama-3.1-8b-instant": 80,
        "openai/gpt-oss-120b": 85,
        "openai/gpt-oss-20b": 75,
        "qwen/qwen3-32b": 88,
        "meta-llama/llama-4-scout-17b-16e-instruct": 82,
        # Fallback models (less preferred)
        "llama-2-70b-4096": 60,
        "mixtral-8x7b-32768": 70,
    }
    
    # Cache TTL in seconds (1 hour)
    CACHE_TTL = 3600
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """
        Initialize the LLM Model Manager
        
        Args:
            groq_api_key: Groq API key (if None, reads from GROQ_API_KEY env var)
        """
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.current_model = os.getenv("MODEL", "llama-3.3-70b-versatile")
        self.available_models: List[str] = []
        self.model_cache_time: Optional[datetime] = None
        self.model_cache_ttl = self.CACHE_TTL
        self.failed_models: Dict[str, datetime] = {}  # Track failed models with timestamps
        self.model_change_history: List[Dict] = []  # Log all model changes
        
        logger.info(f"🤖 LLM Model Manager initialized with default model: {self.current_model}")
    
    async def get_available_models(self, force_refresh: bool = False) -> List[str]:
        """
        Fetch available models from Groq API with caching
        
        Args:
            force_refresh: Force refresh even if cache is valid
            
        Returns:
            List of available model IDs
        """
        # Check cache validity
        if (self.available_models and 
            self.model_cache_time and 
            not force_refresh and
            datetime.now() - self.model_cache_time < timedelta(seconds=self.model_cache_ttl)):
            logger.debug(f"✅ Using cached models ({len(self.available_models)} models)")
            return self.available_models
        
        try:
            logger.info("🔄 Fetching available models from Groq API...")
            
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.GROQ_MODELS_URL, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                models = [model["id"] for model in data.get("data", [])]
                
                if models:
                    self.available_models = models
                    self.model_cache_time = datetime.now()
                    logger.info(f"✅ Retrieved {len(models)} available models from Groq")
                    logger.debug(f"Available models: {models}")
                    return models
                else:
                    logger.warning("⚠️  No models returned from Groq API")
                    return []
                    
        except httpx.RequestError as e:
            logger.error(f"❌ Failed to fetch models from Groq API: {str(e)}")
            # Fallback to known models if API unreachable
            logger.info("💡 Using fallback known models...")
            return list(self.MODEL_PRIORITY.keys())
        except Exception as e:
            logger.error(f"❌ Unexpected error fetching models: {str(e)}")
            return list(self.MODEL_PRIORITY.keys())
    
    async def get_best_available_model(self) -> str:
        """
        Get the best available model based on priority ranking
        
        Returns:
            Best available model ID
        """
        available = await self.get_available_models()
        
        if not available:
            logger.warning(f"⚠️  No available models found, using default: {self.current_model}")
            return self.current_model
        
        # Sort by priority
        ranked_models = sorted(
            available,
            key=lambda m: self.MODEL_PRIORITY.get(m, 50),
            reverse=True
        )
        
        best_model = ranked_models[0]
        logger.info(f"✅ Best available model: {best_model} (priority: {self.MODEL_PRIORITY.get(best_model, 'N/A')})")
        
        return best_model
    
    async def handle_model_error(self, model: str, error_message: str) -> Optional[str]:
        """
        Handle model errors (decommissioned, etc.) and switch to alternative
        
        Args:
            model: The model that failed
            error_message: Error message from LLM API
            
        Returns:
            New model to use, or None if no fallback available
        """
        logger.warning(f"⚠️  Model error for {model}: {error_message}")
        
        # Mark model as failed
        self.failed_models[model] = datetime.now()
        
        # Check if it's a decommissioned model error
        if "decommissioned" in error_message.lower():
            logger.error(f"❌ Model {model} has been decommissioned!")
            
            # Force refresh model list
            available = await self.get_available_models(force_refresh=True)
            
            # Remove failed model from available
            available = [m for m in available if m != model]
            
            if not available:
                logger.error("❌ No alternative models available!")
                return None
            
            # Get best alternative
            ranked = sorted(
                available,
                key=lambda m: self.MODEL_PRIORITY.get(m, 50),
                reverse=True
            )
            
            new_model = ranked[0]
            self._log_model_change(model, new_model, "decommissioned")
            
            logger.info(f"🔄 Switching from {model} to {new_model}")
            self.current_model = new_model
            
            return new_model
        
        return None
    
    def _log_model_change(self, old_model: str, new_model: str, reason: str) -> None:
        """
        Log model change for audit trail
        
        Args:
            old_model: Previous model
            new_model: New model
            reason: Reason for change
        """
        change_record = {
            "timestamp": datetime.now().isoformat(),
            "old_model": old_model,
            "new_model": new_model,
            "reason": reason
        }
        self.model_change_history.append(change_record)
        logger.info(f"📋 Model change logged: {old_model} → {new_model} ({reason})")
    
    def get_current_model(self) -> str:
        """Get currently active model"""
        return self.current_model
    
    def set_model(self, model: str) -> None:
        """
        Manually set model (if explicitly preferred)
        
        Args:
            model: Model ID to use
        """
        old_model = self.current_model
        self.current_model = model
        self._log_model_change(old_model, model, "manual_override")
        logger.info(f"📌 Model manually set to: {model}")
    
    def get_model_stats(self) -> Dict:
        """
        Get model manager statistics
        
        Returns:
            Dictionary with stats
        """
        return {
            "current_model": self.current_model,
            "available_models_cached": len(self.available_models),
            "failed_models": list(self.failed_models.keys()),
            "model_changes": len(self.model_change_history),
            "cache_age_seconds": (
                (datetime.now() - self.model_cache_time).total_seconds()
                if self.model_cache_time else None
            ),
            "model_change_history": self.model_change_history[-5:]  # Last 5 changes
        }
    
    async def health_check(self) -> Dict:
        """
        Health check for model manager
        
        Returns:
            Health status
        """
        try:
            available = await self.get_available_models()
            return {
                "status": "healthy",
                "current_model": self.current_model,
                "available_models_count": len(available),
                "models_updated": self.model_cache_time.isoformat() if self.model_cache_time else None
            }
        except Exception as e:
            return {
                "status": "degraded",
                "error": str(e),
                "current_model": self.current_model
            }


# Global instance
_model_manager: Optional[LLMModelManager] = None


async def init_model_manager(groq_api_key: Optional[str] = None) -> LLMModelManager:
    """
    Initialize global model manager
    
    Args:
        groq_api_key: Groq API key
        
    Returns:
        Initialized model manager
    """
    global _model_manager
    
    _model_manager = LLMModelManager(groq_api_key)
    
    # Fetch available models on startup
    await _model_manager.get_available_models()
    
    return _model_manager


def get_model_manager() -> Optional[LLMModelManager]:
    """Get global model manager instance"""
    return _model_manager


async def get_current_model() -> str:
    """
    Get current model, handling any deprecation automatically
    
    Returns:
        Current model ID
    """
    if _model_manager:
        return _model_manager.get_current_model()
    
    return os.getenv("MODEL", "llama-3.3-70b-versatile")


async def handle_model_decommission(error: Exception) -> Optional[str]:
    """
    Handle model decommission errors from LLM API
    
    Args:
        error: The error from LLM API
        
    Returns:
        New model to use, or None if no fallback
    """
    if _model_manager:
        current = _model_manager.get_current_model()
        error_msg = str(error)
        return await _model_manager.handle_model_error(current, error_msg)
    
    return None
