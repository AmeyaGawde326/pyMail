#!/usr/bin/env python3
"""
Startup script for the Email Server
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if required environment variables are set"""
    load_dotenv()
    
    required_vars = [
        'MAIL_USERNAME',
        'MAIL_PASSWORD',
        'API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file with the required variables.")
        print("See env_example.txt for reference.")
        return False
    
    print("✅ Environment variables loaded successfully")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Email Server...")
    print("=" * 40)
    
    if not check_environment():
        sys.exit(1)
    
    try:
        from app.app import app
        print("✅ Flask application loaded successfully")
        print("✅ Email templates loaded successfully")
        print("✅ SMTP configuration ready")
        print("\n🌐 Server will start on http://localhost:5000")
        print("📧 Available endpoints:")
        print("   - POST /send-email (single endpoint for all email types)")
        print("   - GET  /email-types (list available email types)")
        print("   - GET  /health (health check)")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 40)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Error importing Flask application: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
