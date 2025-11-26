"""Configuration management for AI Audio Tour Agent"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for managing API keys and settings"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
    def get_gemini_api_key(self) -> str:
        """Get Gemini API key"""
        return self.gemini_api_key
    
    def set_gemini_api_key(self, api_key: str):
        """Set Gemini API key"""
        self.gemini_api_key = api_key
    
    def is_configured(self) -> bool:
        """Check if Gemini API key is configured"""
        return bool(self.gemini_api_key)

# Global config instance
config = Config()
