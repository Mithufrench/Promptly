"""
Configuration for AI Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "30"))
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    MODEL = os.getenv("MODEL", "mixtral-8x7b-32768")
