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

def test_send_account_confirmation():
    """Test sending an account confirmation email"""
    print("Testing send account confirmation email...")
    data = {
        "receiver_email": user_email,
        "email_type": "account_confirmation_email",
        "variables": {
            "name": "Test User",
            "verification_url": "https://example.com/verify?token=abc123",
            "expiry_hours": 1
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

def test_send_password_reset():
    """Test sending a password reset email"""
    print("Testing send password reset email...")
    data = {
        "receiver_email": user_email,
        "email_type": "password_reset_email",
        "variables": {
            "name": "Test User",
            "reset_link": "https://example.com/reset?token=abc123",
            "expiry_hours": 24
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

def test_send_access_key():
    """Test sending an access key email"""
    print("Testing send access key email...")
    
    now = datetime.now()
    expiry_date = now + timedelta(hours=72)
    
    data = {
        "receiver_email": user_email,
        "email_type": "access_key_email",
        "variables": {
            "name": "Test User",
            "service_name": "API Service",
            "access_key": "ak_test_1234567890abcdef",
            "generated_date": now.strftime("%Y-%m-%d %H:%M:%S"),
            "expiry_date": expiry_date.strftime("%Y-%m-%d %H:%M:%S"),
            "expiry_hours": 72
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

def test_send_invoice():
    """Test sending an invoice email"""
    print("Testing send invoice email...")
    data = {
        "receiver_email": user_email,
        "email_type": "invoice_email",
        "variables": {
            "customer_name": "John Doe",
            "customer_email": user_email,
            "invoice_number": "INV-2024-001",
            "invoice_date": "2024-01-15",
            "due_date": "2024-02-15",
            "total_amount": "299.99",
            "company_name": "Example Corp",
            "payment_link": "https://example.com/pay/inv-2024-001",
            "payment_terms": "Net 30",
            "notes": "Thank you for your business!"
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

def test_invalid_email_type():
    """Test sending email with invalid email type"""
    print("Testing invalid email type...")
    data = {
                "receiver_email": user_email,
        "email_type": "invalid_email_type",
        "variables": {
            "name": "Test User"
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

def test_missing_fields():
    """Test sending email with missing required fields"""
    print("Testing missing required fields...")
    data = {
        "email_type": "welcome_email"
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

def test_unauthorized_access():
    """Test accessing protected endpoints without API key"""
    print("Testing unauthorized access...")
    
    endpoints = [
        "/send-email",
        "/email-types"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"test": "data"})
            )
            print(f"{endpoint}: Status {response.status_code} - {'Unauthorized' if response.status_code == 401 else 'Unexpected'}")
        except requests.exceptions.ConnectionError:
            print(f"{endpoint}: Connection Error")
    
    print()

def test_invalid_api_key():
    """Test accessing protected endpoints with invalid API key"""
    print("Testing invalid API key...")
    
    invalid_headers = {"Content-Type": "application/json", "X-API-Key": "invalid-key"}
    
    try:
        response = requests.get(f"{BASE_URL}/email-types", headers=invalid_headers)
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
    test_send_account_confirmation()
    test_send_password_reset()
    test_send_access_key()
    test_send_invoice()
    test_invalid_email_type()
    test_missing_fields()
    test_unauthorized_access()
    test_invalid_api_key()
    
    print("=" * 60)
    print("TESTING COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
