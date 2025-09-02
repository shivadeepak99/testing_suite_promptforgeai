#!/usr/bin/env python3
"""
✅ BACKEND FIX VERIFICATION - Quick Test Script
Run this after applying the 4 critical fixes to verify they work
Tests the exact fields that were missing from API responses
"""

import requests
import json
from datetime import datetime

def test_backend_fixes():
    """Test that all 4 critical fixes have been applied"""
    
    base_url = "http://localhost:8000"
    headers = {
        "Authorization": "Bearer mock-test-token",
        "Content-Type": "application/json"
    }
    
    print("✅ BACKEND FIX VERIFICATION")
    print("=" * 50)
    print(f"Testing fixes applied on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Credits endpoint should now have balance, total_spent, total_purchased
    print("1. Testing Credits Endpoint Fix...")
    try:
        response = requests.get(f"{base_url}/api/v1/users/credits", headers=headers)
        data = response.json().get("data", {})
        
        required_fields = ["balance", "total_spent", "total_purchased"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            print(f"   ❌ STILL MISSING: {missing_fields}")
            print(f"   📋 Current response: {data}")
        else:
            balance = data.get("balance", "unknown")
            print(f"   ✅ FIXED! All fields present. Balance: {balance}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 2: User profile should now have display_name
    print("\n2. Testing User Profile Fix...")
    try:
        response = requests.get(f"{base_url}/api/v1/users/me", headers=headers)
        data = response.json().get("data", {})
        
        if "display_name" not in data:
            print(f"   ❌ STILL MISSING: display_name")
            print(f"   📋 Current response keys: {list(data.keys())}")
        else:
            display_name = data.get("display_name", "unknown")
            print(f"   ✅ FIXED! display_name present: '{display_name}'")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 3: Preferences should now have theme
    print("\n3. Testing Preferences Fix...")
    try:
        response = requests.get(f"{base_url}/api/v1/users/preferences", headers=headers)
        data = response.json().get("data", {})
        
        if "theme" not in data:
            print(f"   ❌ STILL MISSING: theme")
            print(f"   📋 Current response: {data}")
        else:
            theme = data.get("theme", "unknown")
            print(f"   ✅ FIXED! theme present: '{theme}'")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 4: Stats should now have prompts_created, ideas_generated, tests_run
    print("\n4. Testing Stats Fix...")
    try:
        response = requests.get(f"{base_url}/api/v1/users/stats", headers=headers)
        data = response.json().get("data", {})
        
        required_fields = ["prompts_created", "ideas_generated", "tests_run"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            print(f"   ❌ STILL MISSING: {missing_fields}")
            print(f"   📋 Current response keys: {list(data.keys())}")
        else:
            prompts = data.get("prompts_created", "unknown")
            print(f"   ✅ FIXED! All stat fields present. Prompts created: {prompts}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 5: Authentication performance
    print("\n5. Testing Authentication Performance...")
    try:
        start_time = datetime.now()
        response = requests.post(
            f"{base_url}/api/v1/users/auth/complete",
            headers=headers,
            json={
                "uid": "test-user-123",
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User"
            }
        )
        end_time = datetime.now()
        auth_time_ms = (end_time - start_time).total_seconds() * 1000
        
        if auth_time_ms > 500:
            print(f"   ⚠️  SLOW: Authentication took {auth_time_ms:.0f}ms (target: <500ms)")
        else:
            print(f"   ✅ FAST: Authentication took {auth_time_ms:.0f}ms")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 FIX VERIFICATION COMPLETE!")
    print("\nIf you see ✅ FIXED for all 4 tests, your backend is 100% ready!")
    print("If you see ❌ STILL MISSING, apply the fixes from BACKEND_IMMEDIATE_FIXES.md")
    print("\nNext: Run the full test suite:")
    print("python test-scripts/realistic_user_tests.py")

if __name__ == "__main__":
    test_backend_fixes()
