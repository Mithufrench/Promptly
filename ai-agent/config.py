"""
Configuration for AI Agent with Cognee Memory Integration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Groq Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "30"))
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    MODEL = os.getenv("MODEL", "mixtral-8x7b-32768")
    
    # Cognee Memory Configuration
    COGNEE_ENABLED = os.getenv("COGNEE_ENABLED", "true").lower() == "true"
    COGNEE_DATASET = os.getenv("COGNEE_DATASET", "promptly_agent")
    
    # LLM Configuration for Cognee (can be different from Groq)
    LLM_API_KEY = os.getenv("LLM_API_KEY") or GROQ_API_KEY
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # For Cognee
    
    # Database Configuration
    DB_PROVIDER = os.getenv("DB_PROVIDER", "postgres")  # postgres, sqlite, etc.
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USERNAME = os.getenv("DB_USERNAME", "cognee")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "cognee")
    DB_NAME = os.getenv("DB_NAME", "cognee_db")
    
    # Vector Database Configuration
    VECTOR_DB_PROVIDER = os.getenv("VECTOR_DB_PROVIDER", "pgvector")  # pgvector, weaviate, etc.
    
    # Graph Database Configuration
    GRAPH_DATABASE_PROVIDER = os.getenv("GRAPH_DATABASE_PROVIDER", "postgres")  # postgres, neo4j, etc.
    
    # Cache Configuration
    CACHE_BACKEND = os.getenv("CACHE_BACKEND", "postgres")  # postgres, redis, etc.
    
    # Data Storage
    DATA_ROOT_DIRECTORY = os.getenv("DATA_ROOT_DIRECTORY", ".cognee_data")
    
    # Server Configuration
    PORT = int(os.getenv("PORT", "8000"))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # Feature Flags
    ENABLE_MEMORY_CONTEXT = os.getenv("ENABLE_MEMORY_CONTEXT", "true").lower() == "true"
    ENABLE_AGENT_LEARNING = os.getenv("ENABLE_AGENT_LEARNING", "true").lower() == "true"
    MEMORY_CONTEXT_LIMIT = int(os.getenv("MEMORY_CONTEXT_LIMIT", "500"))
