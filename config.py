# File: config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    # Application settings
    APP_NAME = 'FlexiBot'
    
    # Database settings (if applicable)
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///flexibot.db')

    # Storage settings
    STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'json')  # 'json' or 'memory'
    JSON_STORAGE_PATH = os.getenv('JSON_STORAGE_PATH', 'data')

    # Chatbot settings
    DEFAULT_CHATBOT_TYPE = os.getenv('DEFAULT_CHATBOT_TYPE', 'TextChatbot')
    MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', 50))

    # API keys (if applicable)
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    @staticmethod
    def init_app(app):
        pass