#!/usr/bin/env python3
"""
Simple API Test for Multi-Agent Attribution System
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("   ✅ Server is healthy")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {str(e)}")
        return False

def test_search_endpoints():
    """Test search endpoints"""
    print("\n🔍 Testing Search Endpoints...")
    
    # Test search insights
    try:
        response = requests.get(f"{BASE_URL}/insights/cust_001")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Search insights retrieved")
            insights = data.get('data', {})
            print(f"      Total searches: {insights.get('total_searches', 0)}")
        else:
            print(f"   ⚠️ Search insights failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Search insights error: {str(e)}")

def test_display_endpoints():
    """Test display endpoints"""
    print("\n🎨 Testing Display Endpoints...")
    
    # Test display insights
    try:
        response = requests.get(f"{BASE_URL}/display-insights/cust_001")
        if response.status_code == 200:
            print("   ✅ Display insights retrieved")
        else:
            print(f"   ⚠️ Display insights failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Display insights error: {str(e)}")

def main():
    print("🚀 Simple API Test")
    print("=" * 40)
    
    if not test_health():
        print("\n❌ Server not running. Start with: python start_server.py")
        return
    
    test_search_endpoints()
    test_display_endpoints()
    
    print("\n" + "=" * 40)
    print("🎉 API Test Completed!")

if __name__ == "__main__":
    main()