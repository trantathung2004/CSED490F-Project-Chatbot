#!/usr/bin/env python3
"""
Simple script to test the chatbot server connection and functionality
"""

import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Test health check endpoint"""
    print_section("Testing Health Check")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_list_models():
    """Test listing available models"""
    print_section("Testing List Models")
    try:
        response = requests.get(f"{API_URL}/models", timeout=10)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Available Models: {data.get('count', 0)}")
        for model in data.get('models', []):
            print(f"  - {model['name']} ({model.get('size', 'N/A')})")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat(message="Hello! Can you introduce yourself?"):
    """Test chat endpoint"""
    print_section("Testing Chat Endpoint")
    print(f"User Message: {message}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": message, "model": "llama3.2"},
            timeout=120
        )
        end_time = time.time()
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Response received in {end_time - start_time:.2f}s")
            print(f"\nChatbot: {data['response']}")
            print(f"\nModel: {data['model']}")
            print(f"Processing Time: {data.get('processing_time', 'N/A')}s")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_load_model():
    """Test loading a model"""
    print_section("Testing Model Load")
    try:
        response = requests.post(
            f"{API_URL}/models/load",
            json={"model": "llama3.2", "keep_alive": "5m"},
            timeout=60
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  RASPBERRY PI CHATBOT SERVER - CONNECTION TEST")
    print("="*60)
    print(f"\nServer URL: {BASE_URL}")
    print(f"API Documentation: {BASE_URL}/docs")
    
    results = {
        "Health Check": test_health(),
        "List Models": test_list_models(),
        "Load Model": test_load_model(),
        "Chat": test_chat("Why is the sky blue?"),
    }
    
    # Summary
    print_section("Test Summary")
    for test, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test:<20} {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Server is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the server and Ollama status.")

if __name__ == "__main__":
    main()