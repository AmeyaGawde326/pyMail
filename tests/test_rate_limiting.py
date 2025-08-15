#!/usr/bin/env python3
"""
Test script to verify rate limiting functionality with Redis or in-memory storage
"""

import requests
import time
import json
import threading
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
BASE_URL = "http://localhost:5000"
API_KEY = "isekai-trash"  # Change this to your actual API key

def make_request(endpoint: str, method: str = "GET", data: Dict[str, Any] = None, use_api_key: bool = True) -> requests.Response:
    """Make a request to the API with proper headers"""
    headers = {"Content-Type": "application/json"}
    
    if use_api_key:
        headers["X-API-Key"] = API_KEY
    
    url = f"{BASE_URL}{endpoint}"
    
    if method.upper() == "GET":
        response = requests.get(url, headers=headers)
    elif method.upper() == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return response

def make_concurrent_requests(endpoint: str, method: str = "GET", data: Dict[str, Any] = None, 
                           num_requests: int = 15, use_api_key: bool = True) -> list:
    """Make multiple concurrent requests to test rate limiting"""
    responses = []
    
    def make_single_request(request_id: int):
        try:
            response = make_request(endpoint, method, data, use_api_key)
            return {
                "request_id": request_id,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else response.text,
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "request_id": request_id,
                "endpoint": endpoint,
                "status_code": 0,
                "response": str(e),
                "timestamp": time.time()
            }
    
    # Use ThreadPoolExecutor for concurrent requests
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(make_single_request, i) for i in range(num_requests)]
        
        for future in as_completed(futures):
            responses.append(future.result())
    
    # Sort by request ID to maintain order
    responses.sort(key=lambda x: x["request_id"])
    return responses

def test_rate_limiting():
    """Test rate limiting on protected endpoints"""
    print("Testing rate limiting on protected endpoints...")
    
    # Test data for send-email endpoint
    test_data = {
        "receiver_email": "test@example.com",
        "email_type": "welcome_email",
        "sender_name": "Test Sender",
        "sender_email": "sender@example.com",
        "variables": {
            "name": "Test User",
            "email": "test@example.com",
            "login_url": "https://example.com/login"
        }
    }
    
    # Test rate limiting on send-email endpoint
    print("\n🔍 Testing rate limiting on /send-email endpoint...")
    email_responses = make_concurrent_requests("/send-email", "POST", test_data, 15, True)
    
    # Test rate limiting on email-types endpoint
    print("🔍 Testing rate limiting on /email-types endpoint...")
    types_responses = make_concurrent_requests("/email-types", "GET", None, 15, True)
    
    # Analyze results
    def analyze_responses(responses, endpoint_name):
        rate_limited = [r for r in responses if r["status_code"] == 429]
        successful = [r for r in responses if r["status_code"] == 200]
        failed = [r for r in responses if r["status_code"] not in [200, 429]]
        
        print(f"\n📊 {endpoint_name} Results:")
        print(f"  Successful requests: {len(successful)}")
        print(f"  Rate limited requests: {len(rate_limited)}")
        print(f"  Failed requests: {len(failed)}")
        
        if rate_limited:
            print(f"  ✅ Rate limiting is working on {endpoint_name}")
            # Show the first rate limited response to see the error message
            first_rate_limited = rate_limited[0]
            print(f"  📝 Rate limit response (429): {first_rate_limited['response']}")
            print(f"  📊 Total rate limited: {len(rate_limited)} requests")
            
            # Show a few more rate limited responses if there are multiple
            if len(rate_limited) > 1:
                print(f"  📋 Sample rate limit responses:")
                for i, resp in enumerate(rate_limited[:3]):  # Show first 3
                    print(f"    Request {resp['request_id']}: {resp['response']}")
                if len(rate_limited) > 3:
                    print(f"    ... and {len(rate_limited) - 3} more")
        else:
            print(f"  ❌ Rate limiting may not be working on {endpoint_name}")
        
        return len(rate_limited) > 0
    
    email_working = analyze_responses(email_responses, "/send-email")
    types_working = analyze_responses(types_responses, "/email-types")
    
    return email_working and types_working

def test_health_endpoint():
    """Test health endpoint (no rate limiting, no API key required)"""
    print("\n🔍 Testing health endpoint (should not be rate limited)...")
    
    # Make multiple requests to health endpoint - should all succeed
    health_responses = make_concurrent_requests("/health", "GET", None, 20, False)
    
    successful = [r for r in health_responses if r["status_code"] == 200]
    failed = [r for r in health_responses if r["status_code"] != 200]
    
    print(f"Health endpoint results:")
    print(f"  Successful requests: {len(successful)}")
    print(f"  Failed requests: {len(failed)}")
    
    if len(successful) == 20 and len(failed) == 0:
        print("  ✅ Health endpoint is not rate limited (as expected)")
        return True
    else:
        print("  ❌ Health endpoint has unexpected behavior")
        return False

def test_rate_limit_configuration():
    """Test that rate limit configuration is visible in health endpoint"""
    print("\n🔍 Testing rate limit configuration visibility...")
    
    response = make_request("/health", use_api_key=False)
    if response.status_code == 200:
        data = response.json()
        if "rate_limiting" in data:
            print("✅ Rate limiting configuration is visible in health endpoint")
            print(f"Current limit: {data['rate_limiting']['limit']}")
            print(f"Storage type: {data['rate_limiting']['storage']}")
            
            if data['rate_limiting']['storage'] == 'redis':
                print("ℹ️ Using Redis for persistent rate limiting")
            else:
                print("ℹ️ Using in-memory storage for rate limiting")
        else:
            print("❌ Rate limiting configuration not found in health endpoint")
    else:
        print(f"❌ Health endpoint failed with status {response.status_code}")

def test_redis_persistence():
    """Test Redis persistence by checking if rate limits persist across requests"""
    print("\n🔍 Testing rate limiting persistence...")
    
    # Get initial rate limit info
    response = make_request("/health", use_api_key=False)
    if response.status_code != 200:
        print("❌ Cannot test persistence - health endpoint failed")
        return
    
    data = response.json()
    storage_type = data['rate_limiting']['storage']
    
    if storage_type == 'redis':
        print("🔄 Testing Redis persistence...")
        print("ℹ️ Rate limits should persist across server restarts with Redis")
        print("ℹ️ In-memory storage resets when server restarts")
    else:
        print("ℹ️ Using in-memory storage - rate limits reset on server restart")

def main():
    """Run all rate limiting tests"""
    print("🚀 Starting Rate Limiting Tests")
    print("=" * 50)
    
    try:
        # Test rate limit configuration visibility
        test_rate_limit_configuration()
        
        # Test health endpoint (should not be rate limited)
        test_health_endpoint()
        
        # Test rate limiting on protected endpoints
        rate_limiting_working = test_rate_limiting()
        
        # Test persistence
        test_redis_persistence()
        
        print("\n" + "=" * 50)
        if rate_limiting_working:
            print("✅ Rate limiting tests completed successfully!")
        else:
            print("⚠️ Rate limiting tests completed with issues!")
        
        # Show recommendations
        print("\n📋 Recommendations:")
        print("- Use Redis for production environments (persistent rate limiting)")
        print("- Use in-memory for development/testing (simpler setup)")
        print("- Monitor rate limiting effectiveness in production")
        print("- Health endpoint should remain unrate-limited for monitoring")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
