#!/usr/bin/env python3
"""
🚀 USER ONBOARDING COMPREHENSIVE TEST SUITE
Tests complete user lifecycle: signup → profile → usage → logout → re-login
Validates database state and system integrity at each step
Part of the Demon Engine Testing Framework
"""

import requests
import json
import time
import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorClient
import hashlib
import uuid

class UserOnboardingTester:
    def __init__(self, base_url: str = "http://localhost:8000", debug_level: int = 3):
        """
        Initialize the User Onboarding Test Suite
        
        Args:
            base_url: API base URL
            debug_level: 1=minimal, 2=standard, 3=detailed, 4=forensic
        """
        self.base_url = base_url
        self.debug_level = debug_level
        self.session = requests.Session()
        self.test_results = []
        self.test_user_data = {}
        self.database_snapshots = []
        
        # Test user configuration
        self.test_uid = f"test-user-{uuid.uuid4().hex[:8]}"
        self.test_email = f"test+{self.test_uid}@promptforge.ai"
        
        # MongoDB connection (for direct validation)
        self.mongo_client = None
        self.db = None
        
        # Setup debug mode
        self.setup_debug_environment()
        
    def setup_debug_environment(self):
        """Enable comprehensive backend debugging"""
        os.environ['DEBUG_BRAIN_ENGINE'] = '1'
        os.environ['DEBUG_USER_FLOWS'] = '1' 
        
        # Set session headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'PromptForge-TestSuite/1.0',
            'X-Test-Mode': 'true'
        })
        
    async def setup_database_connection(self):
        """Setup direct MongoDB connection for validation"""
        try:
            self.mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
            self.db = self.mongo_client.promptforge
            await self.db.admin.command('ping')
            self.log_debug("✅ Database connection established", level=2)
        except Exception as e:
            self.log_debug(f"⚠️ Database connection failed: {e}", level=1)
            
    def log_debug(self, message: str, level: int = 3, data: Any = None):
        """Structured debug logging"""
        if level <= self.debug_level:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] {message}")
            if data and self.debug_level >= 4:
                print(f"    📊 Data: {json.dumps(data, indent=2, default=str)}")
                
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     expected_status: int = 200, description: str = "") -> Dict:
        """Execute API test with comprehensive logging"""
        test_start = time.time()
        
        try:
            # Prepare request
            url = f"{self.base_url}{endpoint}"
            self.log_debug(f"🚀 {method} {endpoint} - {description}", level=2)
            
            if self.debug_level >= 4:
                self.log_debug(f"📤 Request data:", level=4, data=data)
            
            # Execute request
            if method.upper() == "GET":
                response = self.session.get(url, params=data)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            # Process response
            response_time = (time.time() - test_start) * 1000
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
                
            success = response.status_code == expected_status
            status_icon = "✅" if success else "❌"
            
            self.log_debug(
                f"{status_icon} {method} {endpoint} [{response.status_code}] - {response_time:.0f}ms", 
                level=2
            )
            
            if self.debug_level >= 3 and not success:
                self.log_debug(f"📥 Response:", level=3, data=response_data)
                
            # Store result
            result = {
                "test_id": f"onboarding_{len(self.test_results)+1:03d}",
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response_time_ms": int(response_time),
                "response_data": response_data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            self.log_debug(f"💥 Request failed: {str(e)}", level=1)
            result = {
                "test_id": f"onboarding_{len(self.test_results)+1:03d}",
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": 0,
                "expected_status": expected_status,
                "success": False,
                "response_time_ms": int((time.time() - test_start) * 1000),
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            self.test_results.append(result)
            return result
            
    async def validate_database_state(self, checkpoint: str) -> Dict:
        """Validate database state at checkpoint"""
        if not self.db:
            return {"status": "skipped", "reason": "no_db_connection"}
            
        try:
            self.log_debug(f"🔍 Database validation: {checkpoint}", level=2)
            
            # Check user document
            user_doc = await self.db.users.find_one({"uid": self.test_uid})
            
            # Check credits document
            credits_doc = await self.db.credits.find_one({"user_id": self.test_uid})
            
            # Check preferences document  
            prefs_doc = await self.db.preferences.find_one({"user_id": self.test_uid})
            
            snapshot = {
                "checkpoint": checkpoint,
                "timestamp": datetime.now().isoformat(),
                "user_exists": user_doc is not None,
                "credits_exists": credits_doc is not None,
                "preferences_exists": prefs_doc is not None,
                "user_data": user_doc,
                "credits_data": credits_doc,
                "preferences_data": prefs_doc
            }
            
            self.database_snapshots.append(snapshot)
            
            if self.debug_level >= 3:
                self.log_debug(f"📊 Database state:", level=3, data={
                    "user_exists": snapshot["user_exists"],
                    "credits_exists": snapshot["credits_exists"], 
                    "preferences_exists": snapshot["preferences_exists"]
                })
                
            return snapshot
            
        except Exception as e:
            self.log_debug(f"💥 Database validation failed: {e}", level=1)
            return {"status": "error", "error": str(e)}
            
    def print_section_header(self, title: str, emoji: str = "📋"):
        """Print beautiful section headers"""
        print(f"\n{'='*80}")
        print(f"{emoji} {title}")
        print(f"{'='*80}")
        
    async def run_signup_flow(self):
        """Test user signup and initial setup"""
        self.print_section_header("USER SIGNUP & AUTHENTICATION", "👤")
        
        # 1. Complete user authentication
        auth_data = {
            "uid": self.test_uid,
            "email": self.test_email,
            "first_name": "Test",
            "last_name": "User",
            "display_name": "Test User",
            "avatar_url": "https://example.com/avatar.jpg"
        }
        
        self.test_user_data = auth_data
        
        result = self.test_endpoint(
            "POST", 
            "/api/v1/users/auth/complete",
            auth_data,
            200,
            "Complete user authentication and create profile"
        )
        
        if result["success"]:
            # Extract auth token if provided
            if "token" in result["response_data"]:
                token = result["response_data"]["token"]
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                self.log_debug(f"🔑 Auth token set: {token[:20]}...", level=2)
                
        # Set mock auth token for testing
        mock_token = f"mock-token-{self.test_uid}"
        self.session.headers.update({"Authorization": f"Bearer {mock_token}"})
        
        # Validate database state after signup
        await self.validate_database_state("after_signup")
        
        # 2. Verify user profile creation
        self.test_endpoint(
            "GET",
            "/api/v1/users/me", 
            None,
            200,
            "Get user profile after signup"
        )
        
        # 3. Check initial credits allocation
        self.test_endpoint(
            "GET",
            "/api/v1/users/credits",
            None, 
            200,
            "Verify initial credits allocation"
        )
        
        # 4. Verify default preferences
        self.test_endpoint(
            "GET",
            "/api/v1/users/preferences",
            None,
            200,
            "Check default user preferences"
        )
        
        await self.validate_database_state("after_initial_setup")
        
    async def run_profile_management_flow(self):
        """Test profile updates and data management"""
        self.print_section_header("PROFILE MANAGEMENT", "⚙️")
        
        # 1. Update user profile
        profile_updates = {
            "first_name": "Updated",
            "last_name": "TestUser", 
            "display_name": "Updated Test User",
            "bio": "Test user for onboarding validation"
        }
        
        self.test_endpoint(
            "PUT",
            "/api/v1/users/me/profile",
            profile_updates,
            200,
            "Update user profile information"
        )
        
        # 2. Update preferences
        preference_updates = {
            "theme": "dark",
            "notifications": {
                "email": True,
                "push": False
            },
            "language": "en"
        }
        
        self.test_endpoint(
            "PUT", 
            "/api/v1/users/preferences",
            preference_updates,
            200,
            "Update user preferences"
        )
        
        # 3. Test data export
        self.test_endpoint(
            "GET",
            "/api/v1/users/export-data",
            None,
            200,
            "Export user data (GDPR compliance)"
        )
        
        # 4. Get user statistics
        self.test_endpoint(
            "GET",
            "/api/v1/users/stats",
            None,
            200,
            "Get user statistics and usage data"
        )
        
        await self.validate_database_state("after_profile_updates")
        
    async def run_usage_tracking_flow(self):
        """Test usage tracking and analytics"""
        self.print_section_header("USAGE TRACKING", "📊")
        
        # 1. Track usage event
        usage_event = {
            "event_type": "prompt_upgrade",
            "metadata": {
                "engine": "demon",
                "mode": "pro",
                "client": "test_suite"
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/users/usage/track",
            usage_event,
            200,
            "Track user usage event"
        )
        
        # 2. Get usage history
        self.test_endpoint(
            "GET",
            "/api/v1/users/me/usage",
            None,
            200,
            "Get user usage history"
        )
        
        await self.validate_database_state("after_usage_tracking")
        
    async def run_session_management_flow(self):
        """Test logout/login cycle"""
        self.print_section_header("SESSION MANAGEMENT", "🔄")
        
        # 1. Test logout (clear token)
        original_token = self.session.headers.get("Authorization")
        self.session.headers.pop("Authorization", None)
        
        self.log_debug("🚪 Simulating logout (removed auth token)", level=2)
        
        # 2. Test unauthenticated access (should fail)
        self.test_endpoint(
            "GET",
            "/api/v1/users/me",
            None,
            401,  # Expect unauthorized
            "Access profile without authentication (should fail)"
        )
        
        # 3. Re-authenticate
        self.session.headers.update({"Authorization": original_token})
        self.log_debug("🔑 Simulating re-login (restored auth token)", level=2)
        
        # 4. Test authenticated access (should succeed)
        self.test_endpoint(
            "GET",
            "/api/v1/users/me",
            None,
            200,
            "Access profile after re-authentication"
        )
        
    async def run_account_cleanup_flow(self):
        """Test account deletion (optional, for testing only)"""
        self.print_section_header("ACCOUNT CLEANUP", "🗑️")
        
        # This is typically destructive, so we'll just test the endpoint availability
        # without actually deleting unless in explicit test mode
        
        if os.getenv("ENABLE_DESTRUCTIVE_TESTS") == "1":
            self.test_endpoint(
                "DELETE",
                "/api/v1/users/account",
                None,
                200,
                "Delete user account (destructive test)"
            )
            
            await self.validate_database_state("after_account_deletion")
        else:
            self.log_debug("⚠️ Skipping destructive account deletion test", level=2)
            self.log_debug("   Set ENABLE_DESTRUCTIVE_TESTS=1 to enable", level=2)
            
    def print_results_summary(self):
        """Print comprehensive test results"""
        self.print_section_header("USER ONBOARDING TEST RESULTS", "📋")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        avg_response_time = sum(r.get("response_time_ms", 0) for r in self.test_results) / total_tests if total_tests > 0 else 0
        
        print(f"📊 SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌") 
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Avg Response Time: {avg_response_time:.0f}ms")
        
        if failed_tests > 0:
            print(f"\n💥 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['method']} {result['endpoint']} [{result['status_code']}]")
                    print(f"      {result['description']}")
                    
        print(f"\n🗃️ DATABASE SNAPSHOTS: {len(self.database_snapshots)}")
        for snapshot in self.database_snapshots:
            print(f"   📸 {snapshot['checkpoint']}: User={snapshot['user_exists']}, Credits={snapshot['credits_exists']}, Prefs={snapshot['preferences_exists']}")
            
        print(f"\n👤 TEST USER: {self.test_uid}")
        print(f"📧 TEST EMAIL: {self.test_email}")
        
    async def run_complete_test_suite(self):
        """Execute the complete user onboarding test suite"""
        start_time = time.time()
        
        print("🚀 PROMPTFORGE.AI USER ONBOARDING TEST SUITE")
        print("=" * 80)
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🐛 Debug Level: {self.debug_level}")
        print(f"👤 Test User: {self.test_uid}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Setup database connection
        await self.setup_database_connection()
        
        # Execute test flows
        await self.run_signup_flow()
        await self.run_profile_management_flow()
        await self.run_usage_tracking_flow()
        await self.run_session_management_flow()
        await self.run_account_cleanup_flow()
        
        # Print results
        total_time = time.time() - start_time
        self.print_results_summary()
        
        print(f"\n⏰ Total execution time: {total_time:.1f}s")
        print(f"🎯 Next: Run 'python features_test.py' to test AI engine features")
        
        # Cleanup
        if self.mongo_client:
            self.mongo_client.close()
            
        return self.test_results

async def main():
    """Main execution function"""
    tester = UserOnboardingTester(debug_level=3)
    results = await tester.run_complete_test_suite()
    return results

if __name__ == "__main__":
    print("🧠 DEMON ENGINE - User Onboarding Test Suite")
    print("=" * 60)
    
    # Run the async test suite
    asyncio.run(main())
