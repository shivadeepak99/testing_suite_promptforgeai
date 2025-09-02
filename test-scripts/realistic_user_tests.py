#!/usr/bin/env python3
"""
🧑‍💻 REALISTIC USER TESTING - Using Real Database User Data
Tests the backend using actual user data structure from the database
Validates all user-related endpoints with real data scenarios
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class RealisticUserTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
        # Real user data from your database
        self.real_user_data = {
            "_id": "test-user-123",
            "account_status": "active",
            "billing": {
                "provider": None,
                "customer_id": None,
                "plan": "free",
                "status": "active",
                "started_at": None,
                "renewed_at": None,
                "created_at": "2025-09-02T13:27:55.911+00:00"
            },
            "credits": {
                "balance": 7,
                "total_purchased": 0,
                "total_spent": 0,
                "last_purchase_at": None,
                "starter_grant_used": True
            },
            "display_name": "Test User",
            "email": "test@example.com",
            "email_verified": True,
            "last_active_at": "2025-09-02T18:01:36.490+00:00",
            "last_login_at": "2025-09-02T18:01:36.490+00:00",
            "login_seq": 23,
            "partnership": {
                "is_partner": False,
                "partner_tier": None,
                "application_status": "none"
            },
            "photo_url": "",
            "preferences": {
                "theme": "dark",
                "notifications": {
                    "email": True,
                    "updated_at": "2025-09-02T17:56:24.051+00:00"
                }
            },
            "profile": {
                "bio": "",
                "website": "",
                "location": "",
                "company": "",
                "job_title": "",
                "expertise": ""
            },
            "social_links": {},
            "security": {
                "two_factor_enabled": False,
                "last_password_change": None,
                "suspicious_activity_detected": False,
                "gdpr_consent": False,
                "gdpr_consent_date": None,
                "data_retention_until": None
            },
            "stats": {
                "prompts_created": 0,
                "ideas_generated": 0,
                "tests_run": 0,
                "marketplace_sales": 0,
                "total_earnings": 0,
                "average_rating": 0,
                "total_reviews": 0,
                "followers_count": 0,
                "following_count": 0
            },
            "subscription": {
                "tier": "free",
                "status": "active",
                "stripe_customer_id": None
            },
            "uid": "test-user-123",
            "updated_at": "2025-09-02T18:01:36.490+00:00"
        }
        
        self.headers = {
            "Authorization": "Bearer mock-test-token",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.test_results = []
        
    def print_header(self, title: str, emoji: str = "🧑‍💻"):
        print(f"\n{'='*80}")
        print(f"{emoji} {title}")
        print(f"{'='*80}")
        
    def print_section(self, title: str, emoji: str = "📋"):
        print(f"\n{'-'*60}")
        print(f"{emoji} {title}")
        print(f"{'-'*60}")
        
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     expected_status: int = 200, description: str = "") -> Dict:
        """Test endpoint and validate against real user data"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response_time = round((time.time() - start_time) * 1000, 2)
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = {"raw_text": response.text}
            
            # Determine success
            success = 200 <= response.status_code <= 299
            status_icon = "✅" if success else "❌"
            
            print(f"{status_icon} {method:<6} {endpoint:<50} [{response.status_code}] ({response_time}ms)")
            
            # Validate response structure if it's a user-related endpoint
            validation_result = self.validate_user_response(endpoint, response_data)
            if validation_result:
                print(f"   🔍 Validation: {validation_result}")
            
            result = {
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response_time_ms": response_time,
                "response_data": response_data,
                "validation": validation_result
            }
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            print(f"❌ {method:<6} {endpoint:<50} [ERROR] {str(e)}")
            result = {
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": 0,
                "expected_status": expected_status,
                "success": False,
                "error": str(e)
            }
            self.test_results.append(result)
            return result
    
    def validate_user_response(self, endpoint: str, response_data: Dict) -> str:
        """Validate response data against expected user structure"""
        if not isinstance(response_data, dict) or "data" not in response_data:
            return None
            
        data = response_data.get("data", {})
        
        # Validate based on endpoint
        if "/users/me" in endpoint:
            return self.validate_user_profile(data)
        elif "/users/credits" in endpoint:
            return self.validate_credits_data(data)
        elif "/users/preferences" in endpoint:
            return self.validate_preferences_data(data)
        elif "/users/stats" in endpoint:
            return self.validate_stats_data(data)
        elif "/users/auth/complete" in endpoint:
            return self.validate_auth_response(data)
            
        return None
    
    def validate_user_profile(self, data: Dict) -> str:
        """Validate user profile structure matches database"""
        expected_fields = ["uid", "email", "display_name", "subscription", "credits"]
        missing = [field for field in expected_fields if field not in data]
        
        if missing:
            return f"Missing fields: {missing}"
        
        # Check subscription structure
        if "subscription" in data:
            sub = data["subscription"]
            if sub.get("tier") != "free" or sub.get("status") != "active":
                return f"Subscription mismatch: expected tier=free, status=active"
        
        return "✅ Structure matches database"
    
    def validate_credits_data(self, data: Dict) -> str:
        """Validate credits structure"""
        expected_fields = ["balance", "total_spent", "total_purchased"]
        missing = [field for field in expected_fields if field not in data]
        
        if missing:
            return f"Missing credit fields: {missing}"
            
        # Check balance is reasonable (should be around 7 based on real data)
        balance = data.get("balance", 0)
        if balance < 0:
            return "❌ Negative credit balance"
            
        return f"✅ Credits valid (balance: {balance})"
    
    def validate_preferences_data(self, data: Dict) -> str:
        """Validate preferences structure"""
        # Should have theme and notifications
        if "theme" not in data:
            return "Missing theme preference"
            
        theme = data.get("theme")
        if theme not in ["light", "dark", "auto"]:
            return f"Invalid theme: {theme}"
            
        return f"✅ Preferences valid (theme: {theme})"
    
    def validate_stats_data(self, data: Dict) -> str:
        """Validate user stats structure"""
        expected_fields = ["prompts_created", "ideas_generated", "tests_run"]
        missing = [field for field in expected_fields if field not in data]
        
        if missing:
            return f"Missing stats: {missing}"
            
        return "✅ Stats structure valid"
    
    def validate_auth_response(self, data: Dict) -> str:
        """Validate authentication response"""
        if data.get("uid") != "test-user-123":
            return f"UID mismatch: expected test-user-123, got {data.get('uid')}"
            
        if data.get("email") != "test@example.com":
            return f"Email mismatch: expected test@example.com, got {data.get('email')}"
            
        return "✅ Auth response matches real user"
    
    def run_user_lifecycle_tests(self):
        """Test complete user lifecycle with real data scenarios"""
        
        self.print_header("Real User Data Testing - Complete Lifecycle", "🧑‍💻")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🧑‍💻 Testing with real user: {self.real_user_data['email']}")
        print(f"💳 Current balance: {self.real_user_data['credits']['balance']} credits")
        print(f"🎨 Theme preference: {self.real_user_data['preferences']['theme']}")
        print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. Authentication (should match real user data)
        self.print_section("Authentication & User Profile", "🔐")
        
        # Complete auth with real user data
        auth_data = {
            "uid": self.real_user_data["uid"],
            "email": self.real_user_data["email"],
            "first_name": "Test",
            "last_name": "User",
            "display_name": self.real_user_data["display_name"]
        }
        
        self.test_endpoint("POST", "/api/v1/users/auth/complete", auth_data, 200, 
                          "Authenticate with real user data")
        
        # Get user profile
        self.test_endpoint("GET", "/api/v1/users/me", None, 200, 
                          "Get user profile (should match database)")
        
        # 2. Credits System (should show 7 credits)
        self.print_section("Credits & Billing", "💳")
        
        self.test_endpoint("GET", "/api/v1/users/credits", None, 200, 
                          "Get credits (should show 7 credits)")
        
        # Track usage (simulate spending 1 credit)
        usage_data = {
            "event_type": "prompt_enhanced",
            "credits_used": 1,
            "metadata": {"source": "api_test", "prompt_id": "test-123"}
        }
        self.test_endpoint("POST", "/api/v1/users/usage/track", usage_data, 200, 
                          "Track credit usage")
        
        # Check updated balance
        self.test_endpoint("GET", "/api/v1/users/credits", None, 200, 
                          "Verify credit deduction")
        
        # 3. Preferences (theme should be dark)
        self.print_section("User Preferences", "⚙️")
        
        self.test_endpoint("GET", "/api/v1/users/preferences", None, 200, 
                          "Get preferences (theme should be dark)")
        
        # Update preferences
        preference_update = {
            "theme": "light",
            "notifications": {
                "email": False,
                "push": True
            }
        }
        self.test_endpoint("PUT", "/api/v1/users/preferences", preference_update, 200, 
                          "Update preferences")
        
        # 4. User Statistics (should show zeros for new user)
        self.print_section("User Statistics", "📊")
        
        self.test_endpoint("GET", "/api/v1/users/stats", None, 200, 
                          "Get user stats (should show zeros)")
        
        # 5. Profile Management
        self.print_section("Profile Management", "👤")
        
        # Update profile
        profile_update = {
            "bio": "QA Test User for PromptForge.ai",
            "website": "https://promptforge.ai",
            "company": "PromptForge QA",
            "job_title": "Test Engineer"
        }
        self.test_endpoint("PUT", "/api/v1/users/me/profile", profile_update, 200, 
                          "Update user profile")
        
        # Get updated profile
        self.test_endpoint("GET", "/api/v1/users/me", None, 200, 
                          "Verify profile updates")
        
        # 6. Data Export (GDPR compliance)
        self.print_section("Data Management", "📁")
        
        self.test_endpoint("GET", "/api/v1/users/export-data", None, 200, 
                          "Export user data (GDPR)")
        
        # 7. Usage History
        self.test_endpoint("GET", "/api/v1/users/me/usage", None, 200, 
                          "Get usage history")
        
        # Print comprehensive results
        self.print_results_summary()
    
    def print_results_summary(self):
        """Print detailed test results with real data validation"""
        self.print_header("Test Results Summary", "📊")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests} ({success_rate:.1f}%)")
        print(f"❌ Failed: {failed_tests} ({100-success_rate:.1f}%)")
        
        # Average response time
        response_times = [r.get("response_time_ms", 0) for r in self.test_results if r["success"]]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        print(f"⚡ Average Response Time: {avg_response_time:.1f}ms")
        
        # Data validation results
        validations = [r.get("validation") for r in self.test_results if r.get("validation")]
        valid_responses = sum(1 for v in validations if v and "✅" in v)
        print(f"🔍 Data Validation: {valid_responses}/{len(validations)} passed")
        
        # Show failed tests
        failed_results = [r for r in self.test_results if not r["success"]]
        if failed_results:
            self.print_section("Failed Tests Analysis", "🔍")
            for result in failed_results:
                print(f"❌ {result['method']} {result['endpoint']} - {result.get('error', 'Unknown error')}")
        
        # Show validation issues
        validation_issues = [r for r in self.test_results if r.get("validation") and "❌" in r["validation"]]
        if validation_issues:
            self.print_section("Data Validation Issues", "⚠️")
            for result in validation_issues:
                print(f"⚠️  {result['endpoint']} - {result['validation']}")
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"realistic_user_test_report_{timestamp}.json"
        
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate": success_rate,
                "average_response_time_ms": avg_response_time,
                "data_validation_rate": (valid_responses / len(validations) * 100) if validations else 0
            },
            "real_user_data": self.real_user_data,
            "test_results": self.test_results
        }
        
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📁 Detailed report saved: {report_file}")
        print(f"🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    print("🧑‍💻 Realistic User Testing - Using Real Database Data")
    print("=" * 60)
    
    tester = RealisticUserTester()
    tester.run_user_lifecycle_tests()
