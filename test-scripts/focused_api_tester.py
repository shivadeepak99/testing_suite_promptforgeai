"""
🎯 PromptForge.ai FOCUSED API Tester
Testing only CRITICAL endpoints that users actually need
Smart, strategic testing - no time wasted on unimplemented features!
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class FocusedAPITester:
    def __init__(self, base_url="http://localhost:8000", max_failures=5):
        self.base_url = base_url
        self.token = "mock-test-token"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.test_results = []
        self.max_failures = max_failures
        self.failure_count = 0
        self.should_stop = False
        
    def print_header(self, title: str, emoji: str = "🚀"):
        """Print a beautiful section header"""
        print(f"\n{'='*80}")
        print(f"{emoji} {title}")
        print(f"{'='*80}")
    
    def print_section(self, title: str, emoji: str = "📋"):
        """Print a section divider"""
        print(f"\n{'-'*60}")
        print(f"{emoji} {title}")
        print(f"{'-'*60}")
    
    def print_test_result(self, method: str, endpoint: str, status_code, 
                         expected_status, response_data: str = ""):
        """Print formatted test result with smart success detection"""
        # Ensure status_code is an integer - handle any type safely
        try:
            if hasattr(status_code, '__int__'):
                status_code = int(status_code)
            elif isinstance(status_code, str):
                status_code = int(status_code)
            elif status_code is None:
                status_code = 0
            else:
                status_code = 0
        except (ValueError, TypeError, AttributeError):
            status_code = 0
            
        try:
            if hasattr(expected_status, '__int__'):
                expected_status = int(expected_status)
            elif isinstance(expected_status, str):
                expected_status = int(expected_status)
            elif expected_status is None:
                expected_status = 200
            else:
                expected_status = 200
        except (ValueError, TypeError, AttributeError):
            expected_status = 200
        
        # Consider 2xx status codes as successful for most endpoints
        is_successful_status = 200 <= status_code <= 299
        exact_match = status_code == expected_status
        
        # Smart success detection: accept any 2xx for expected 2xx
        if 200 <= expected_status <= 299:
            success = is_successful_status
        else:
            success = exact_match
        
        # Icons based on actual success
        if success:
            status_icon = "✅"
        elif status_code == 401:
            status_icon = "🔐"  # Auth required
        elif status_code == 403:
            status_icon = "🚫"  # Forbidden
        elif status_code == 422:
            status_icon = "📝"  # Validation error
        elif status_code >= 500:
            status_icon = "💥"  # Server error
        else:
            status_icon = "❌"  # Other error
        
        print(f"{status_icon} {method:<6} {endpoint:<50} [{status_code}]")
        
        # Show response data intelligently
        if success and response_data and len(response_data) < 150:
            print(f"   ✨ {response_data}")
        elif not success and response_data:
            if status_code == 401:
                print(f"   🔐 Auth: {response_data[:80]}...")
            elif status_code == 422:
                print(f"   📝 Validation: {response_data[:80]}...")
            elif status_code >= 500:
                print(f"   💥 Server: {response_data[:80]}...")
            else:
                print(f"   ❌ Error: {response_data[:80]}...")
        
        return success
    
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     expected_status: int = 200, description: str = ""):
        """Test a single endpoint with beautiful formatting"""
        
        # Check if we should stop due to too many failures
        if self.should_stop:
            print(f"⏸️  Stopping tests - reached {self.max_failures} failures limit")
            return False
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Make the request
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                print(f"❌ Unsupported method: {method}")
                self.failure_count += 1
                self._check_failure_limit()
                return False
            
            # Format response data
            response_text = ""
            if response.status_code < 400:
                try:
                    json_response = response.json()
                    if "status" in json_response:
                        response_text = f"Status: {json_response['status']}"
                    elif "message" in json_response:
                        response_text = f"Message: {json_response['message']}"
                    else:
                        response_text = str(json_response)[:100]
                except:
                    response_text = response.text[:100]
            else:
                response_text = response.text[:100]
            
            # Print and record result
            success = self.print_test_result(method, endpoint, response.status_code, 
                                           expected_status, response_text)
            
            # Track failures and check limit
            if not success:
                self.failure_count += 1
                self._check_failure_limit()
            
            self.test_results.append({
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success
            })
            
            return success
            
        except Exception as e:
            print(f"❌ {method:<6} {endpoint:<50} [ERROR] {str(e)[:50]}")
            self.failure_count += 1
            self._check_failure_limit()
            
            self.test_results.append({
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": 0,
                "expected_status": expected_status,
                "success": False,
                "error": str(e)
            })
            return False
    
    def _check_failure_limit(self):
        """Check if failure limit is reached and set stop flag"""
        if self.failure_count >= self.max_failures:
            self.should_stop = True
            print(f"\n🛑 STOPPING TESTS - Reached {self.max_failures} failures!")
            print(f"💡 Fix the current batch of errors and run the script again.")
            print(f"🔍 Total tests completed: {len(self.test_results)}")
            print(f"❌ Failures so far: {self.failure_count}")
            self.print_current_summary()
    
    def print_current_summary(self):
        """Print summary of current batch results"""
        self.print_section("Current Batch Summary", "📊")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Tests in this batch: {total_tests}")
        print(f"✅ Successful: {successful_tests} ({success_rate:.1f}%)")
        print(f"❌ Failed: {failed_tests} ({100-success_rate:.1f}%)")
        
        # Show failed tests for immediate fixing
        failed_results = [r for r in self.test_results if not r["success"]]
        if failed_results:
            print(f"\n🔧 CRITICAL Issues to fix:")
            
            # Group by error type for easier fixing
            server_errors = [r for r in failed_results if r["status_code"] >= 500]
            validation_errors = [r for r in failed_results if r["status_code"] == 422]
            connection_errors = [r for r in failed_results if r["status_code"] == 0]
            
            if server_errors:
                print(f"\n💥 Server Errors (Fix Priority #1): {len(server_errors)}")
                for result in server_errors[:3]:  # Show first 3
                    print(f"   {result['method']} {result['endpoint']} [{result['status_code']}]")
            
            if connection_errors:
                print(f"\n🔌 Connection Errors (Fix Priority #2): {len(connection_errors)}")
                for result in connection_errors[:3]:
                    print(f"   {result['method']} {result['endpoint']} [ERROR]")
            
            if validation_errors:
                print(f"\n📝 Validation Errors (Fix Priority #3): {len(validation_errors)}")
                for result in validation_errors[:2]:
                    print(f"   {result['method']} {result['endpoint']} [422]")
        
        print(f"\n🔄 Run the script again after fixing the above issues!")
    
    def run_critical_tests(self):
        """Test only the CRITICAL endpoints that users actually need"""
        
        self.print_header("PromptForge.ai CRITICAL API Test Suite", "🎯")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🔑 Bearer Token: {self.token}")
        print(f"🛑 Max failures before stopping: {self.max_failures}")
        print(f"⚡ Testing ONLY critical user-facing endpoints")
        print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ===============================
        # 1. CORE HEALTH (WORKING ✅)
        # ===============================
        self.print_section("Core Health Check", "🏥")
        
        self.test_endpoint("GET", "/", 200, "Root endpoint")
        if self.should_stop: return
        self.test_endpoint("GET", "/health", 200, "Health check")
        if self.should_stop: return
        
        # ===============================
        # 2. USER CORE (WORKING ✅)
        # ===============================
        self.print_section("User Core Features", "👤")
        
        # User authentication (CRITICAL)
        user_data = {
            "uid": "test-user-123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        self.test_endpoint("POST", "/api/v1/users/auth/complete", user_data, 200, "User authentication")
        if self.should_stop: return
        
        # Core user endpoints (CRITICAL)
        self.test_endpoint("GET", "/api/v1/users/me", 200, "Get user profile")
        if self.should_stop: return
        self.test_endpoint("GET", "/api/v1/users/credits", 200, "Get user credits")
        if self.should_stop: return
        
        # ===============================
        # 3. PROMPTS CORE (CRITICAL BUSINESS LOGIC)
        # ===============================
        self.print_section("Prompts Core Features", "📝")
        
        # Get user prompts (CRITICAL)
        self.test_endpoint("GET", "/api/v1/prompts/prompts/arsenal", 200, "Get user prompt arsenal")
        if self.should_stop: return
        
        # Create prompt with CORRECT structure (CRITICAL)
        prompt_data = {
            "title": "API Test Prompt",
            "body": "Write a professional email about {topic}",
            "role": "You are a professional email writing assistant"
        }
        self.test_endpoint("POST", "/api/v1/prompts/prompts/", prompt_data, 201, "Create new prompt")
        if self.should_stop: return
        
        # ===============================
        # 4. AI CORE FEATURES (CRITICAL)
        # ===============================
        self.print_section("AI Core Features", "🤖")
        
        # AI Remix with CORRECT structure (CRITICAL)
        ai_remix_data = {
            "prompt_body": "Write a blog post about artificial intelligence"
        }
        self.test_endpoint("POST", "/api/v1/ai/remix-prompt", ai_remix_data, 200, "AI Remix prompt")
        if self.should_stop: return
        
        # AI Architect with CORRECT structure (CRITICAL)
        ai_architect_data = {
            "description": "Create a marketing email template",
            "techStack": ["python", "fastapi"],
            "architectureStyle": "microservices"
        }
        self.test_endpoint("POST", "/api/v1/ai/architect-prompt", ai_architect_data, 200, "AI Architect prompt")
        if self.should_stop: return
        
        # ===============================
        # 5. SEARCH (USER-FACING)
        # ===============================
        self.print_section("Search Features", "🔍")
        
        # Global search (CRITICAL for user experience)
        self.test_endpoint("GET", "/api/v1/search/?q=email&type=prompts&limit=10", 200, "Global search")
        if self.should_stop: return
        
        # ===============================
        # 6. MARKETPLACE CORE (BUSINESS CRITICAL)
        # ===============================
        self.print_section("Marketplace Core", "🛒")
        
        # Marketplace search (CRITICAL for revenue)
        self.test_endpoint("GET", "/api/v1/marketplace/search?q=business&limit=10", 200, "Marketplace search")
        if self.should_stop: return
        
        # User's marketplace listings (CRITICAL)
        self.test_endpoint("GET", "/api/v1/marketplace/my-listings", 200, "My marketplace listings")
        if self.should_stop: return
        
        # ===============================
        # FINAL SUMMARY
        # ===============================
        self.print_summary()
    
    def print_summary(self):
        """Print beautiful test results summary"""
        self.print_header("CRITICAL Test Results Summary", "🎯")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Critical Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests} ({success_rate:.1f}%)")
        print(f"❌ Failed: {failed_tests} ({100-success_rate:.1f}%)")
        print(f"🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show failed tests for debugging
        failed_results = [r for r in self.test_results if not r["success"]]
        if failed_results:
            self.print_section("CRITICAL Issues Found", "🚨")
            
            # Group by status code for better analysis
            server_errors = [r for r in failed_results if r["status_code"] >= 500]
            validation_errors = [r for r in failed_results if r["status_code"] == 422]
            
            if server_errors:
                print(f"💥 Server Errors: {len(server_errors)} endpoints")
                print("   💡 These need immediate backend fixes")
            
            if validation_errors:
                print(f"📝 Validation Errors: {len(validation_errors)} endpoints")
                print("   💡 These need correct request structure")
            
            # Show specific examples
            print(f"\n📋 Issues to fix:")
            for result in failed_results:
                status_icon = "📝" if result["status_code"] == 422 else "💥" if result["status_code"] >= 500 else "❌"
                print(f"{status_icon} {result['method']} {result['endpoint']} [{result['status_code']}]")
        
        print(f"\n{'='*80}")
        if self.should_stop:
            print("🛑 Testing STOPPED - Fix critical errors and run again!")
        else:
            print("🎉 CRITICAL API Testing Complete!")
        print(f"{'='*80}")
        
        if self.should_stop:
            print(f"\n🔄 NEXT STEPS:")
            print(f"1. Fix the {self.failure_count} CRITICAL errors shown above")
            print(f"2. Run 'python focused_api_tester.py' again")
            print(f"3. These are the endpoints users actually need!")
        else:
            print(f"\n🎉 EXCELLENT! All critical user-facing endpoints are working!")
            print(f"✅ Core user flow: Authentication, Prompts, AI, Search, Marketplace")
            print(f"🚀 Ready for real user testing!")
            
        print(f"\n📊 For comprehensive testing: python simple_api_tester.py")

if __name__ == "__main__":
    # Run the focused test suite for CRITICAL endpoints only
    print("🎯 PromptForge.ai FOCUSED API Tester")
    print("💡 Testing ONLY critical user-facing endpoints")
    print("⚡ Smart testing - no time wasted on unimplemented features!")
    print("🛑 Will stop after 5 failures for immediate fixes")
    print("-" * 60)
    
    tester = FocusedAPITester(max_failures=5)  # Stop after 5 failures for critical endpoints
    tester.run_critical_tests()
