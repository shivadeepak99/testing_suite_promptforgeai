"""
🚨 PromptForge.ai CRITICAL FIXES Tester
Focuses on the highest priority issues identified from batch testing
Run this after fixing critical server errors to validate fixes
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class CriticalFixesTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = "mock-test-token"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "X-Test-Mode": "true"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.results = []
        
    def print_section(self, title: str, emoji: str = "🔧"):
        """Print section header"""
        print(f"\n{'='*80}")
        print(f"{emoji} {title}")
        print(f"{'='*80}")
    
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     description: str = "") -> bool:
        """Test endpoint and return success status"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            start_time = time.time()
            
            if method.upper() == "GET":
                response = self.session.get(url, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=10)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, timeout=10)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=10)
            else:
                print(f"❌ {method} {endpoint} - Unsupported method")
                return False
            
            response_time = (time.time() - start_time) * 1000
            success = 200 <= response.status_code <= 299
            
            # Status icons
            if success:
                icon = "✅"
                status_text = "FIXED" if response.status_code in [200, 201] else "OK"
            elif response.status_code >= 500:
                icon = "💥"
                status_text = "STILL BROKEN"
            elif response.status_code == 422:
                icon = "📝"
                status_text = "VALIDATION"
            elif response.status_code == 401:
                icon = "🔐"
                status_text = "AUTH NEEDED"
            elif response.status_code == 404:
                icon = "🔍"
                status_text = "NOT FOUND"
            else:
                icon = "❌"
                status_text = "ERROR"
            
            # Response preview
            response_preview = ""
            try:
                if response.status_code < 400:
                    json_data = response.json()
                    if isinstance(json_data, dict) and "status" in json_data:
                        response_preview = f"Status: {json_data['status']}"
                    else:
                        response_preview = str(json_data)[:60]
                else:
                    response_preview = response.text[:60]
            except:
                response_preview = response.text[:60] if hasattr(response, 'text') else ""
            
            print(f"{icon} {method:<6} {endpoint:<50} [{response.status_code}] {status_text}")
            if response_preview and len(response_preview) > 10:
                if success:
                    print(f"    💚 {response_preview}")
                elif response.status_code >= 500:
                    print(f"    💥 {response_preview}")
                elif response.status_code == 422:
                    print(f"    📝 {response_preview}")
            
            # Store result
            self.results.append({
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": response.status_code,
                "success": success,
                "response_time": response_time,
                "response_preview": response_preview[:100]
            })
            
            return success
            
        except Exception as e:
            print(f"❌ {method:<6} {endpoint:<50} [ERROR] {str(e)[:40]}")
            self.results.append({
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": 0,
                "success": False,
                "response_time": 0,
                "error": str(e)
            })
            return False
    
    def test_critical_server_errors(self):
        """Test endpoints that had 500/503 server errors"""
        self.print_section("CRITICAL SERVER ERRORS (Priority #1)", "💥")
        print("These endpoints were completely broken and need immediate fixing:")
        
        critical_endpoints = [
            # Marketplace issues
            ("GET", "/api/v1/marketplace/preview/test-123", None, "Marketplace preview failing"),
            ("POST", "/api/v1/marketplace/rate", {"prompt_id": "test-123", "rating": 5, "review": "Test"}, "Rating system broken"),
            ("GET", "/api/v1/marketplace/test-123/reviews", None, "Reviews not loading"),
            ("GET", "/api/v1/marketplace/test-123/analytics", None, "Analytics not working"),
            
            # Packaging system issues
            ("POST", "/api/v1/packaging/test-prompt-123/package", {"marketplace_ready": True, "price": 9.99}, "Packaging system failing"),
            ("GET", "/api/v1/packaging/", None, "Package listing broken"),
            
            # Other server errors
            ("GET", "/api/v1/workflows/analytics/usage", None, "Workflow analytics failing"),
            ("DELETE", "/api/v1/notifications/test-notification-123", None, "Notification deletion broken"),
            ("POST", "/api/v1/payments/webhooks/paddle", {"test": "webhook"}, "Paddle webhook failing"),
        ]
        
        fixed_count = 0
        for method, endpoint, data, description in critical_endpoints:
            success = self.test_endpoint(method, endpoint, data, description)
            if success:
                fixed_count += 1
            time.sleep(0.2)  # Be gentle on the server
        
        print(f"\n📊 SERVER ERRORS SUMMARY:")
        print(f"✅ Fixed: {fixed_count}/{len(critical_endpoints)}")
        print(f"💥 Still Broken: {len(critical_endpoints) - fixed_count}")
        
        if fixed_count == len(critical_endpoints):
            print("🎉 ALL CRITICAL SERVER ERRORS FIXED!")
        elif fixed_count > 0:
            print(f"🔥 Progress! {fixed_count} issues resolved, {len(critical_endpoints) - fixed_count} remaining")
        else:
            print("⚠️  No server errors fixed yet - these need immediate attention")
    
    def test_missing_core_endpoints(self):
        """Test core endpoints that returned 404"""
        self.print_section("MISSING CORE ENDPOINTS (Priority #2)", "🔍")
        print("These core features seem to be missing or not implemented:")
        
        core_endpoints = [
            # Core Prompts functionality
            ("GET", "/api/v1/prompts/arsenal", None, "User prompt arsenal"),
            ("POST", "/api/v1/prompts/", {"title": "Test", "content": "Test prompt"}, "Create new prompt"),
            ("GET", "/api/v1/prompts/public", None, "Public prompts listing"),
            ("POST", "/api/v1/prompts/bulk-action", {"action": "tag", "prompt_ids": ["123"]}, "Bulk prompt actions"),
            
            # Projects system
            ("GET", "/api/v1/projects/test-project-123", None, "Project details"),
            ("GET", "/api/v1/projects/test-project-123/prompts", None, "Project prompts"),
        ]
        
        implemented_count = 0
        for method, endpoint, data, description in core_endpoints:
            success = self.test_endpoint(method, endpoint, data, description)
            if success:
                implemented_count += 1
            time.sleep(0.2)
        
        print(f"\n📊 CORE ENDPOINTS SUMMARY:")
        print(f"✅ Implemented: {implemented_count}/{len(core_endpoints)}")
        print(f"🔍 Missing: {len(core_endpoints) - implemented_count}")
        
        if implemented_count == len(core_endpoints):
            print("🎉 ALL CORE ENDPOINTS ARE NOW AVAILABLE!")
        elif implemented_count > 0:
            print(f"🔥 Progress! {implemented_count} endpoints now working")
        else:
            print("⚠️  Core functionality still missing - check route implementations")
    
    def test_validation_fixes(self):
        """Test endpoints with corrected validation parameters"""
        self.print_section("VALIDATION FIXES (Priority #3)", "📝")
        print("Testing endpoints with correct parameter formats:")
        
        validation_endpoints = [
            # AI Features with proper parameters
            ("POST", "/api/v1/ai/remix-prompt", {
                "prompt_body": "Write a professional email about product launch",
                "style": "professional",
                "enhancement_level": "moderate"
            }, "AI Remix with proper params"),
            
            ("POST", "/api/v1/ai/architect-prompt", {
                "description": "Create a marketing email sequence",
                "target_audience": "SaaS users",
                "tone": "professional"
            }, "AI Architect with proper params"),
            
            ("POST", "/api/v1/ai/fuse-prompts", {
                "prompt_a": "Write emails",
                "prompt_b": "Create marketing content",
                "fusion_style": "merge"
            }, "AI Fuse with proper params"),
            
            # Analytics exports with proper format
            ("POST", "/api/v1/analytics/exports/prompts", {
                "export_type": "json",
                "date_range": "last_30_days",
                "include_metadata": True
            }, "Prompts export with proper params"),
            
            ("POST", "/api/v1/analytics/jobs/analytics", {
                "job_type": "user_engagement",
                "parameters": {
                    "date_range": "last_week",
                    "metrics": ["usage", "creation"]
                }
            }, "Analytics job with proper params"),
            
            # Ideas generation with proper params
            ("POST", "/api/v1/ideas/generate", {
                "categories": ["marketing", "business"],
                "count": 5,
                "creativity_level": "high",
                "context": "SaaS startup"
            }, "Ideas generation with proper params"),
            
            # Search with query parameter
            ("GET", "/api/v1/search/users?query=test&limit=5", None, "User search with query param"),
        ]
        
        fixed_count = 0
        for method, endpoint, data, description in validation_endpoints:
            success = self.test_endpoint(method, endpoint, data, description)
            if success:
                fixed_count += 1
            time.sleep(0.2)
        
        print(f"\n📊 VALIDATION FIXES SUMMARY:")
        print(f"✅ Fixed: {fixed_count}/{len(validation_endpoints)}")
        print(f"📝 Still Invalid: {len(validation_endpoints) - fixed_count}")
        
        if fixed_count == len(validation_endpoints):
            print("🎉 ALL VALIDATION ISSUES RESOLVED!")
        elif fixed_count > 0:
            print(f"🔥 Progress! {fixed_count} validation issues fixed")
        else:
            print("⚠️  Validation errors persist - check Swagger docs for exact requirements")
    
    def test_auth_required_endpoints(self):
        """Test a few key auth-required endpoints to check auth implementation"""
        self.print_section("AUTHENTICATION TEST (Info Only)", "🔐")
        print("Testing key endpoints that require authentication:")
        
        auth_endpoints = [
            ("POST", "/api/v1/demon/route", {
                "query": "improve my prompt",
                "context": {"user_level": "pro"}
            }, "Demon Engine (Premium Feature)"),
            
            ("POST", "/api/v1/intelligence/analyze", {
                "prompt_text": "Write a marketing email",
                "analysis_type": "comprehensive"
            }, "Prompt Intelligence (Premium Feature)"),
            
            ("GET", "/api/v1/credits/dashboard", None, "Credits Dashboard (User Feature)"),
            
            ("GET", "/api/v1/monitoring/metrics", None, "System Metrics (Admin Feature)"),
        ]
        
        auth_working_count = 0
        for method, endpoint, data, description in auth_endpoints:
            success = self.test_endpoint(method, endpoint, data, description)
            if success:
                auth_working_count += 1
            time.sleep(0.2)
        
        print(f"\n📊 AUTHENTICATION SUMMARY:")
        print(f"✅ Auth Working: {auth_working_count}/{len(auth_endpoints)}")
        print(f"🔐 Auth Required: {len(auth_endpoints) - auth_working_count}")
        
        if auth_working_count > 0:
            print("🎉 Some premium features are accessible!")
        else:
            print("💡 These endpoints require proper authentication tokens")
            print("   Use production API keys for full testing")
    
    def test_performance_critical_endpoints(self):
        """Test endpoints that were slow in batch testing"""
        self.print_section("PERFORMANCE CHECK", "⚡")
        print("Testing previously slow endpoints for performance improvements:")
        
        slow_endpoints = [
            ("GET", "/", None, "Root endpoint (was 2.4s)"),
            ("GET", "/api/v1/marketplace/test-123/reviews", None, "Marketplace reviews (was 2.1s)"),
            ("GET", "/api/v1/search/?q=email&type=prompts", None, "Global search (was 2.1s)"),
            ("GET", "/api/v1/vault/list", None, "Vault listing (check performance)"),
        ]
        
        fast_count = 0
        for method, endpoint, data, description in slow_endpoints:
            start_time = time.time()
            success = self.test_endpoint(method, endpoint, data, description)
            response_time = (time.time() - start_time) * 1000
            
            if response_time < 500:  # Under 500ms is good
                fast_count += 1
                print(f"    ⚡ Fast: {response_time:.0f}ms")
            elif response_time < 1000:
                print(f"    🟡 Moderate: {response_time:.0f}ms")
            else:
                print(f"    🐌 Slow: {response_time:.0f}ms")
            
            time.sleep(0.3)
        
        print(f"\n📊 PERFORMANCE SUMMARY:")
        print(f"⚡ Fast (<500ms): {fast_count}/{len(slow_endpoints)}")
        print(f"🐌 Still Slow: {len(slow_endpoints) - fast_count}")
    
    def run_critical_fixes_test(self):
        """Run all critical fixes tests"""
        print("🚨 PROMPTFORGE.AI CRITICAL FIXES VALIDATOR")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nThis will test the highest priority issues from batch testing...")
        
        # Run all test categories
        self.test_critical_server_errors()
        self.test_missing_core_endpoints()
        self.test_validation_fixes()
        self.test_auth_required_endpoints()
        self.test_performance_critical_endpoints()
        
        # Final summary
        self.print_final_summary()
    
    def print_final_summary(self):
        """Print final summary of critical fixes"""
        self.print_section("CRITICAL FIXES SUMMARY", "🎯")
        
        total_tests = len(self.results)
        successful = sum(1 for r in self.results if r.get("success", False))
        failed = total_tests - successful
        success_rate = (successful / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 CRITICAL FIXES RESULTS:")
        print(f"   🧪 Total Critical Tests: {total_tests}")
        print(f"   ✅ Fixed/Working: {successful} ({success_rate:.1f}%)")
        print(f"   ❌ Still Broken: {failed} ({100-success_rate:.1f}%)")
        
        # Categorize remaining issues
        server_errors = [r for r in self.results if not r.get("success", True) and r.get("status_code", 0) >= 500]
        validation_errors = [r for r in self.results if not r.get("success", True) and r.get("status_code", 0) == 422]
        missing_endpoints = [r for r in self.results if not r.get("success", True) and r.get("status_code", 0) == 404]
        auth_required = [r for r in self.results if not r.get("success", True) and r.get("status_code", 0) == 401]
        
        print(f"\n🔍 REMAINING ISSUES:")
        if server_errors:
            print(f"   💥 Server Errors: {len(server_errors)} (CRITICAL - fix immediately)")
        if missing_endpoints:
            print(f"   🔍 Missing Endpoints: {len(missing_endpoints)} (implement core features)")
        if validation_errors:
            print(f"   📝 Validation Errors: {len(validation_errors)} (check parameter requirements)")
        if auth_required:
            print(f"   🔐 Auth Required: {len(auth_required)} (use production tokens)")
        
        print(f"\n💡 NEXT ACTIONS:")
        if server_errors:
            print(f"   1. Fix server errors in marketplace, packaging, and notifications")
            print(f"   2. Check error logs for specific failure details")
        if missing_endpoints:
            print(f"   3. Implement missing core prompt and project endpoints")
        if validation_errors:
            print(f"   4. Review Swagger UI for correct parameter formats")
        if success_rate > 50:
            print(f"   5. 🎉 Good progress! Run full batch test again")
        
        print(f"\n🔄 TO CONTINUE TESTING:")
        print(f"   python comprehensive_batch_tester.py  # Full API test")
        print(f"   python critical_fixes_tester.py       # Re-run this test")
        
        print(f"\n🕒 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save critical results
        self.save_critical_results()
    
    def save_critical_results(self):
        """Save critical fixes results"""
        results_file = f"e:\\GPls\\pfai_backend\\pb\\testing\\results\\critical_fixes_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            "test_run": {
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url,
                "test_type": "critical_fixes"
            },
            "summary": {
                "total_tests": len(self.results),
                "successful": sum(1 for r in self.results if r.get("success", False)),
                "failed": sum(1 for r in self.results if not r.get("success", True)),
                "success_rate": (sum(1 for r in self.results if r.get("success", False)) / len(self.results) * 100) if self.results else 0
            },
            "results": self.results
        }
        
        try:
            with open(results_file, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            print(f"📄 Critical fixes results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")

if __name__ == "__main__":
    print("🚨 CRITICAL FIXES TESTER")
    print("🎯 Tests the highest priority issues from comprehensive batch testing")
    print("🔧 Run this after fixing server errors to validate your fixes")
    print("-" * 80)
    
    tester = CriticalFixesTester()
    tester.run_critical_fixes_test()
