#!/usr/bin/env python3
"""
🔧 PromptForge.ai ROBUST API TESTER
Handles connection issues gracefully and provides actionable bug reports
Based on Swagger spec analysis and real-world testing
"""

import requests
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RobustAPITester:
    def __init__(self, base_url="http://localhost:8000", timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.token = "mock-test-token"
        
        # Session with better configuration
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "PromptForge-RobustTester/1.0",
            "Accept": "application/json",
            "Connection": "keep-alive"
        })
        
        # Configure session for better reliability
        adapter = requests.adapters.HTTPAdapter(
            max_retries=requests.packages.urllib3.util.retry.Retry(
                total=2,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504]
            )
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Test tracking
        self.test_results = []
        self.connection_issues = []
        self.server_errors = []
        self.validation_errors = []
        self.working_endpoints = []
        
        # Test data
        self.test_uid = f"test-{uuid.uuid4().hex[:8]}"
        
    def print_header(self, title: str, emoji: str = "🚀"):
        """Print beautiful header"""
        print(f"\n{'='*80}")
        print(f"{emoji} {title}")
        print(f"{'='*80}")
    
    def print_section(self, title: str, emoji: str = "📋"):
        """Print section header"""
        print(f"\n{'-'*60}")
        print(f"{emoji} {title}")
        print(f"{'-'*60}")
    
    def test_server_connectivity(self):
        """Test basic server connectivity"""
        self.print_section("Server Connectivity Test", "🔌")
        
        try:
            # Test with raw requests first
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is responding to basic requests")
                return True
            else:
                print(f"⚠️  Server responded with status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Connection refused - server may not be running")
            print("💡 Start server with: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
            return False
        except requests.exceptions.Timeout:
            print("❌ Connection timeout - server may be overloaded")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def test_endpoint_robust(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                           expected_status: int = 200, description: str = "") -> Dict:
        """Test endpoint with robust error handling"""
        
        result = {
            "method": method,
            "endpoint": endpoint,
            "description": description,
            "success": False,
            "status_code": 0,
            "response_data": "",
            "error_type": None,
            "error_message": "",
            "execution_time": 0
        }
        
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            # Make request with timeout
            if method.upper() == "GET":
                response = self.session.get(url, timeout=self.timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data or {}, timeout=self.timeout)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data or {}, timeout=self.timeout)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=self.timeout)
            else:
                result["error_type"] = "unsupported_method"
                result["error_message"] = f"Unsupported HTTP method: {method}"
                return result
            
            # Calculate execution time
            result["execution_time"] = round((time.time() - start_time) * 1000, 2)
            result["status_code"] = response.status_code
            
            # Try to get response data
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    result["response_data"] = response.json()
                else:
                    result["response_data"] = response.text[:200]
            except:
                result["response_data"] = response.text[:200]
            
            # Determine success
            if 200 <= expected_status <= 299:
                result["success"] = 200 <= response.status_code <= 299
            else:
                result["success"] = response.status_code == expected_status
            
            # Categorize errors
            if not result["success"]:
                if response.status_code >= 500:
                    result["error_type"] = "server_error"
                    self.server_errors.append(result)
                elif response.status_code == 422:
                    result["error_type"] = "validation_error"
                    self.validation_errors.append(result)
                elif response.status_code == 401:
                    result["error_type"] = "auth_error"
                elif response.status_code == 404:
                    result["error_type"] = "not_found"
                else:
                    result["error_type"] = "client_error"
            else:
                self.working_endpoints.append(result)
            
        except requests.exceptions.ConnectionError as e:
            result["error_type"] = "connection_error"
            result["error_message"] = str(e)
            self.connection_issues.append(result)
        except requests.exceptions.Timeout as e:
            result["error_type"] = "timeout_error"
            result["error_message"] = str(e)
        except requests.exceptions.RequestException as e:
            result["error_type"] = "request_error"
            result["error_message"] = str(e)
        except Exception as e:
            result["error_type"] = "unknown_error"
            result["error_message"] = str(e)
        
        result["execution_time"] = round((time.time() - start_time) * 1000, 2)
        self.test_results.append(result)
        
        # Print result
        self.print_test_result(result)
        return result
    
    def print_test_result(self, result: Dict):
        """Print formatted test result"""
        status = result["status_code"]
        method = result["method"]
        endpoint = result["endpoint"]
        exec_time = result["execution_time"]
        
        if result["success"]:
            icon = "✅"
            details = f"({exec_time}ms)"
        elif result["error_type"] == "connection_error":
            icon = "🔌"
            details = "Connection failed"
        elif result["error_type"] == "timeout_error":
            icon = "⏱️"
            details = f"Timeout ({exec_time}ms)"
        elif result["error_type"] == "server_error":
            icon = "💥"
            details = f"Server error"
        elif result["error_type"] == "validation_error":
            icon = "📝"
            details = f"Validation error"
        elif result["error_type"] == "auth_error":
            icon = "🔐"
            details = f"Auth required"
        else:
            icon = "❌"
            details = f"Error [{status}]"
        
        print(f"{icon} {method:<6} {endpoint:<50} {details}")
        
        # Show error details for server errors
        if result["error_type"] == "server_error" and result["response_data"]:
            error_msg = str(result["response_data"])[:100]
            print(f"   💥 {error_msg}...")
    
    def run_critical_endpoint_tests(self):
        """Test the most critical endpoints for business operations"""
        
        self.print_header("PromptForge.ai ROBUST API Testing", "🔧")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"⏱️  Timeout: {self.timeout}s")
        print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check server connectivity first
        if not self.test_server_connectivity():
            print("\n❌ Cannot proceed with testing - server connectivity issues")
            return
        
        # Test critical health endpoints
        self.print_section("Critical Health Endpoints", "🏥")
        self.test_endpoint_robust("GET", "/", 200, "Root endpoint")
        self.test_endpoint_robust("GET", "/health", 200, "Health check")
        self.test_endpoint_robust("GET", "/api/v1/health", 200, "API health")
        
        # Test user authentication (critical for business)
        self.print_section("User Authentication", "👤")
        user_data = {
            "uid": self.test_uid,
            "email": f"test-{self.test_uid}@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        self.test_endpoint_robust("POST", "/api/v1/users/auth/complete", user_data, 200, "User auth")
        self.test_endpoint_robust("GET", "/api/v1/users/me", 200, "Get user profile")
        self.test_endpoint_robust("GET", "/api/v1/users/credits", 200, "Get credits")
        
        # Test core prompt functionality
        self.print_section("Core Prompt Features", "📝")
        prompt_data = {
            "title": f"Test Prompt {self.test_uid}",
            "content": "You are a helpful assistant. Help with {task}.",
            "category": "general"
        }
        self.test_endpoint_robust("POST", "/api/v1/prompts/prompts/", prompt_data, 201, "Create prompt")
        self.test_endpoint_robust("GET", "/api/v1/prompts/prompts/arsenal", 200, "Get arsenal")
        
        # Test AI features (revenue generating)
        self.print_section("AI Features", "🤖")
        ai_data = {"prompt_text": "Write a professional email"}
        self.test_endpoint_robust("POST", "/api/v1/ai/remix-prompt", ai_data, 200, "Remix prompt")
        self.test_endpoint_robust("POST", "/api/v1/demon/route", {"query": "improve prompt"}, 200, "Demon engine")
        
        # Test marketplace (revenue generating)
        self.print_section("Marketplace", "🛒")
        self.test_endpoint_robust("GET", "/api/v1/marketplace/search?q=test&limit=5", 200, "Search marketplace")
        self.test_endpoint_robust("GET", "/api/v1/marketplace/listings", 200, "Get listings")
        
        # Test billing (critical for revenue)
        self.print_section("Billing System", "💳")
        self.test_endpoint_robust("GET", "/api/v1/billing/tiers", 200, "Get billing tiers")
        self.test_endpoint_robust("GET", "/api/v1/billing/me/entitlements", 200, "Get entitlements")
        
        # Test known broken endpoints
        self.print_section("Known Issues Testing", "🚨")
        bulk_package = {"action": "publish", "package_ids": ["test123"]}
        self.test_endpoint_robust("POST", "/api/v1/packaging/manage-bulk", bulk_package, 200, "Bulk package (KNOWN BROKEN)")
        
        # Generate comprehensive report
        self.generate_comprehensive_report()
    
    def generate_comprehensive_report(self):
        """Generate detailed analysis report"""
        self.print_header("COMPREHENSIVE ANALYSIS REPORT", "📊")
        
        total_tests = len(self.test_results)
        working = len(self.working_endpoints)
        connection_issues = len(self.connection_issues)
        server_errors = len(self.server_errors)
        validation_errors = len(self.validation_errors)
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Working: {working} ({working/total_tests*100:.1f}%)")
        print(f"🔌 Connection Issues: {connection_issues} ({connection_issues/total_tests*100:.1f}%)")
        print(f"💥 Server Errors: {server_errors} ({server_errors/total_tests*100:.1f}%)")
        print(f"📝 Validation Errors: {validation_errors} ({validation_errors/total_tests*100:.1f}%)")
        
        # Detailed issue analysis
        if connection_issues > 0:
            self.print_section("Connection Issues Analysis", "🔌")
            print("🚨 HIGH PRIORITY: Multiple endpoints have connection issues")
            print("💡 Possible causes:")
            print("   - CORS configuration blocking requests")
            print("   - Server timeout settings too low")
            print("   - Network/firewall configuration")
            print("   - Session/connection pool limits")
            
        if server_errors:
            self.print_section("Server Errors Found", "💥")
            for error in self.server_errors[:5]:  # Show first 5
                endpoint = error["endpoint"]
                error_data = str(error.get("response_data", ""))[:100]
                print(f"💥 {error['method']} {endpoint}")
                if error_data:
                    print(f"   Error: {error_data}")
        
        if validation_errors:
            self.print_section("Validation Errors", "📝")
            print("🚨 Input validation issues detected")
            print("💡 Likely causes:")
            print("   - Missing required fields in request schemas")
            print("   - Incorrect data types in Pydantic models")
            print("   - Frontend-backend schema mismatch")
        
        if working:
            self.print_section("Working Endpoints", "✅")
            print("🎉 These endpoints are functioning correctly:")
            for endpoint in self.working_endpoints[:10]:  # Show first 10
                exec_time = endpoint["execution_time"]
                print(f"✅ {endpoint['method']} {endpoint['endpoint']} ({exec_time}ms)")
        
        # Save detailed report
        report_file = f"robust_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "working_endpoints": working,
                "connection_issues": connection_issues,
                "server_errors": server_errors,
                "validation_errors": validation_errors,
                "success_rate": working / total_tests * 100 if total_tests > 0 else 0
            },
            "working_endpoints": self.working_endpoints,
            "connection_issues": self.connection_issues,
            "server_errors": self.server_errors,
            "validation_errors": self.validation_errors,
            "all_results": self.test_results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n📁 Detailed report saved: {report_file}")
        
        # Recommendations
        self.print_section("Immediate Action Required", "🚨")
        if connection_issues > total_tests * 0.5:
            print("🔥 CRITICAL: >50% connection failures")
            print("   1. Check CORS middleware configuration")
            print("   2. Verify server timeout settings")
            print("   3. Test with curl/Postman to isolate issue")
        
        if server_errors > 0:
            print("🔥 CRITICAL: Server errors detected")
            print("   1. Check server logs for detailed error messages")
            print("   2. Fix database connection issues")
            print("   3. Add missing imports and dependencies")
        
        if validation_errors > 0:
            print("⚠️  HIGH: Input validation issues")
            print("   1. Review Pydantic model definitions")
            print("   2. Add proper default values")
            print("   3. Update API documentation")

if __name__ == "__main__":
    print("🔧 PromptForge.ai ROBUST API Tester")
    print("💡 Handles connection issues and provides actionable insights")
    print("🎯 Focus on critical business functionality")
    print("-" * 80)
    
    tester = RobustAPITester(timeout=10)
    tester.run_critical_endpoint_tests()
