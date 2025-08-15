import os
import base64
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SMTP Configuration 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    
    # Decode base64 encoded mail password
    mail_password_encoded = os.getenv('MAIL_PASSWORD')
    MAIL_PASSWORD = None
    if mail_password_encoded:
        try:
            MAIL_PASSWORD = base64.b64decode(mail_password_encoded).decode('utf-8')
        except Exception as e:
            print(f"Warning: Failed to decode MAIL_PASSWORD from base64: {e}")
    
    # API Security
    API_KEY = os.getenv('API_KEY', 'default-api-key-change-in-production')
    
    # Rate Limiting Configuration
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', '10'))  # requests per second
    
    # Redis Configuration for Rate Limiting
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    
    # Email Configuration
    EMAIL_VERIFICATION_EXPIRY_HOURS = 1
    PASSWORD_RESET_EXPIRY_HOURS = 24
    ACCESS_KEY_EXPIRY_HOURS = 72
