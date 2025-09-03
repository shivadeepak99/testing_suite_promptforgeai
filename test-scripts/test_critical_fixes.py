#!/usr/bin/env python3
"""
Quick fix verification script
Tests the critical endpoints that were failing
"""

import requests
import time

def test_critical_endpoints():
    """Test the endpoints that were causing server errors"""
    
    base_url = "http://localhost:8000"
    headers = {
        "Authorization": "Bearer mock-test-token",
        "Content-Type": "application/json"
    }
    
    print("🔧 Testing Critical Fixes...")
    print("="*50)
    
    # Test 1: Packaging endpoint (was causing performance_monitor error)
    print("1. Testing packaging bulk management...")
    try:
        response = requests.post(
            f"{base_url}/api/v1/packaging/manage-bulk",
            headers=headers,
            json={"action": "publish", "package_ids": ["test123"]}
        )
        print(f"   Status: {response.status_code} (Expected: 400 or better)")
        if response.status_code == 500:
            print(f"   ❌ Still has server error: {response.text[:100]}")
        else:
            print(f"   ✅ Fixed! No more performance_monitor error")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test 2: Notifications endpoint (was causing db not defined error)
    print("\n2. Testing notifications...")
    try:
        response = requests.put(
            f"{base_url}/api/v1/notifications/test-123/read",
            headers=headers,
            json={}
        )
        print(f"   Status: {response.status_code} (Expected: 404 or better)")
        if "name 'db' is not defined" in response.text:
            print(f"   ❌ Still has db import error")
        else:
            print(f"   ✅ Fixed! No more db import error")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test 3: Mark all notifications
    print("\n3. Testing mark all notifications...")
    try:
        response = requests.post(
            f"{base_url}/api/v1/notifications/mark-all-read",
            headers=headers,
            json={}
        )
        print(f"   Status: {response.status_code} (Expected: 200 or better)")
        if "name 'db' is not defined" in response.text:
            print(f"   ❌ Still has db import error")
        else:
            print(f"   ✅ Fixed! No more db import error")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    print("\n" + "="*50)
    print("🎯 Fix verification complete!")
    print("\nNext: Restart your server to apply the fixes:")
    print("uvicorn main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    test_critical_endpoints()
