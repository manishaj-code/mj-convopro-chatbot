from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
import streamlit as st

load_dotenv()

class Settings(BaseSettings):
    """Application settings configuration"""
    
    # MongoDB
    MONGO_DB_URL: str = os.getenv("MONGO_DB_URL", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "chatbot_db")

    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "")

    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **data):
        super().__init__(**data)
        self._load_from_env()
        try:
            self._load_from_secrets()
        except:
            pass

    def _load_from_env(self):
        """Load from .env file"""
        self.MONGO_DB_URL = os.getenv("MONGO_DB_URL", self.MONGO_DB_URL)
        self.MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", self.MONGO_DB_NAME)
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        self.GROQ_MODEL = os.getenv("GROQ_MODEL", "")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "")

    def _load_from_secrets(self):
        """Load from Streamlit secrets (for cloud deployment)"""
        if "GROQ_API_KEY" in st.secrets:
            self.GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
        if "GROQ_MODEL" in st.secrets:
            self.GROQ_MODEL = st.secrets["GROQ_MODEL"]
        if "GEMINI_API_KEY" in st.secrets:
            self.GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
        if "GEMINI_MODEL" in st.secrets:
            self.GEMINI_MODEL = st.secrets["GEMINI_MODEL"]
        if "MONGO_DB_URL" in st.secrets:
            self.MONGO_DB_URL = st.secrets["MONGO_DB_URL"]
        if "MONGO_DB_NAME" in st.secrets:
            self.MONGO_DB_NAME = st.secrets["MONGO_DB_NAME"]

    @property
    def groq_model_list(self) -> list:
        """Get list of Groq models"""
        return [m.strip() for m in self.GROQ_MODEL.split(",") if m.strip()] if self.GROQ_MODEL else []

    @property
    def gemini_model_list(self) -> list:
        """Get list of Gemini models"""
        return [m.strip() for m in self.GEMINI_MODEL.split(",") if m.strip()] if self.GEMINI_MODEL else []

# Global settings instance
get_settings = Settings()