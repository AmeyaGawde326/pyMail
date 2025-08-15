import requests
import json
import os
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"
user_email = "kaistack00@gmail.com"

# Load API key from environment
API_KEY = os.getenv('API_KEY','isekai-trash')
if not API_KEY:
    print("API_KEY not found in environment variables")
    exit(1)

HEADERS = {"Content-Type": "application/json", "X-API-Key": API_KEY}

def test_health_check():
    """Test the health check endpoint (no API key required)"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure the server is running.")
        print()

def test_get_email_types():
    """Test getting available email types"""
    print("Testing get email types...")
    try:
        response = requests.get(f"{BASE_URL}/email-types", headers=HEADERS)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Available Email Types:")
            email_types = response.json()
            for email_type, info in email_types.items():
                print(f"  - {email_type}")
                print(f"    Description: {info['description']}")
        else:
            print(f"Error: {response.json()}")
        print()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure the server is running.")
        print()

def test_send_welcome_email():
    """Test sending a welcome email"""
    print("Testing send welcome email...")
    data = {
        "receiver_email": user_email,
        "email_type": "welcome_email",
        "sender_name": "Test App",
        "sender_email": "noreply@example.com",
        "variables": {
            "name": "Test User",
            "email": user_email,
            "login_url": "https://example.com/login"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/send-email",
            headers=HEADERS,
            data=json.dumps(data)
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure the server is running.")
        print()

def main():
    """Run all tests"""
    print("=" * 60)
    print("EMAIL SERVER API TESTING - SINGLE ENDPOINT VERSION")
    print("=" * 60)
    print()
    
    test_health_check()
    test_get_email_types()
    test_send_welcome_email()

    
    print("=" * 60)
    print("TESTING COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
