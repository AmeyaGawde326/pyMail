import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SMTP Configuration (sensitive data from environment)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    
    # API Security
    API_KEY = os.getenv('API_KEY', 'default-api-key-change-in-production')
    
    # Email Configuration
    EMAIL_VERIFICATION_EXPIRY_HOURS = 1
    PASSWORD_RESET_EXPIRY_HOURS = 24
    ACCESS_KEY_EXPIRY_HOURS = 72
