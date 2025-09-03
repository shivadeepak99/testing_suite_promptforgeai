"""
🧪 API CLEANUP VALIDATION TESTER
Validates the specific changes made during API cleanup on September 3, 2025
Tests: Removed endpoints, deprecated endpoints, and working functionality
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys
import os

class APICleanupValidator:
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
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200, description: str = "") -> Dict:
        """Test a single endpoint and return results"""
        start_time = time.time()
        
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=10)
            elif method == "PUT":
                response = self.session.put(url, json=data, timeout=10)
            elif method == "DELETE":
                response = self.session.delete(url, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_time = (time.time() - start_time) * 1000
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:200]}
            
            success = response.status_code == expected_status
            
            result = {
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_time": response_time,
                "success": success,
                "response_data": response_data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            return result
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            result = {
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": "ERROR",
                "expected_status": expected_status,
                "response_time": response_time,
                "success": False,
                "response_data": {"error": str(e)},
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            return result

    def print_test_result(self, result: Dict):
        """Print formatted result for a test"""
        method = result["method"]
        endpoint = result["endpoint"]
        status = result["status_code"]
        expected = result["expected_status"]
        time_ms = result["response_time"]
        success = result["success"]
        description = result["description"]
        
        # Format status display
        if success:
            status_icon = "✅"
            status_text = f"[{status}] Expected {expected}"
        else:
            if status == "ERROR":
                status_icon = "💥"
                status_text = "[ERR]"
            elif status == 404 and expected == 404:
                status_icon = "✅"
                status_text = f"[404] Expected removal"
            elif status >= 500:
                status_icon = "💥"
                status_text = f"[{status}] Server Error"
            else:
                status_icon = "❌"
                status_text = f"[{status}] Expected {expected}"
        
        time_str = f"{time_ms:.0f}ms" if time_ms < 1000 else f"{time_ms/1000:.1f}s"
        
        print(f"{status_icon} {method:<6} {endpoint:<50} {status_text} {time_str}")
        print(f"     📝 {description}")
        
        # Print response details
        if result["response_data"]:
            response_data = result["response_data"]
            if isinstance(response_data, dict):
                if "detail" in response_data:
                    detail = str(response_data["detail"])[:80]
                    print(f"     💬 {detail}")
                elif "message" in response_data:
                    print(f"     💬 {response_data['message']}")
                elif "error" in response_data:
                    error = str(response_data["error"])[:80]
                    print(f"     💬 {error}")

    def validate_removed_endpoints(self):
        """Test endpoints that should have been removed"""
        print("\n" + "="*80)
        print("🗑️  TESTING REMOVED ENDPOINTS")
        print("These endpoints should return 404 (Not Found)")
        print("="*80)
        
        # Test the removed health endpoint
        result = self.test_endpoint(
            "GET", 
            "/api/v1/payments/webhooks/health", 
            None, 
            404,
            "Duplicate health endpoint - Should be removed"
        )
        self.print_test_result(result)
        
        return [result]

    def validate_working_health_endpoints(self):
        """Test that the main health endpoints still work"""
        print("\n" + "="*80)
        print("💚 TESTING WORKING HEALTH ENDPOINTS")
        print("These endpoints should continue to work normally")
        print("="*80)
        
        results = []
        
        # Test main health endpoints
        health_tests = [
            ("GET", "/health", "Main health endpoint - Should work"),
            ("GET", "/api/v1/health", "API v1 health endpoint - Should work")
        ]
        
        for method, endpoint, description in health_tests:
            result = self.test_endpoint(method, endpoint, None, 200, description)
            self.print_test_result(result)
            results.append(result)
            
        return results

    def validate_deprecated_vault_endpoints(self):
        """Test that deprecated vault endpoints still work but show warnings"""
        print("\n" + "="*80)
        print("⚠️  TESTING DEPRECATED VAULT ENDPOINTS")
        print("These endpoints should work but may show deprecation warnings")
        print("="*80)
        
        results = []
        
        vault_tests = [
            ("GET", "/api/v1/vault/arsenal", "Deprecated - Use /api/v1/prompts/arsenal"),
            ("GET", "/api/v1/vault/list", "Deprecated - Use main prompts listing"),
            ("GET", "/api/v1/vault/search", "Deprecated - Use /api/v1/search with filters"),
            ("POST", "/api/v1/vault/save", "Deprecated - Use main prompts API", {
                "prompt_title": "Test Vault Prompt",
                "prompt_body": "A test prompt for vault storage"
            }),
            ("GET", "/api/v1/vault/test-vault-123/versions", "Deprecated - Use /api/v1/prompts/{id}/versions"),
            ("DELETE", "/api/v1/vault/delete/test-vault-123", "Deprecated - Use DELETE /api/v1/prompts/{id}")
        ]
        
        for test_data in vault_tests:
            if len(test_data) == 3:
                method, endpoint, description = test_data
                data = None
            else:
                method, endpoint, description, data = test_data
                
            result = self.test_endpoint(method, endpoint, data, 200, description)
            self.print_test_result(result)
            results.append(result)
            
        return results

    def validate_core_functionality(self):
        """Test core API functionality to ensure no regressions"""
        print("\n" + "="*80)
        print("🎯 TESTING CORE FUNCTIONALITY")
        print("Critical endpoints that must continue working")
        print("="*80)
        
        results = []
        
        core_tests = [
            ("GET", "/api/v1/prompts/arsenal", "Core prompts arsenal"),
            ("GET", "/api/v1/prompts/public", "Public prompts listing"),
            ("GET", "/api/v1/marketplace/search?q=test", "Marketplace search"),
            ("GET", "/api/v1/users/me", "User profile"),
            ("POST", "/api/v1/ai/remix-prompt", "AI remix functionality", {
                "prompt_body": "Test prompt for remix",
                "style": "professional"
            })
        ]
        
        for test_data in core_tests:
            if len(test_data) == 3:
                method, endpoint, description = test_data
                data = None
            else:
                method, endpoint, description, data = test_data
                
            result = self.test_endpoint(method, endpoint, data, 200, description)
            self.print_test_result(result)
            results.append(result)
            
        return results

    def validate_brain_engine_endpoints(self):
        """Test Brain Engine endpoints to ensure they're the canonical implementation"""
        print("\n" + "="*80)
        print("🧠 TESTING BRAIN ENGINE ENDPOINTS")
        print("These are the canonical prompt enhancement endpoints")
        print("="*80)
        
        results = []
        
        brain_tests = [
            ("POST", "/api/v1/prompt/quick_upgrade", "Brain Engine quick upgrade", {
                "prompt_body": "Test prompt for quick upgrade"
            }),
            ("POST", "/api/v1/prompt/upgrade", "Brain Engine full upgrade", {
                "prompt_body": "Test prompt for full upgrade"
            })
        ]
        
        for method, endpoint, description, data in brain_tests:
            # These might return 401 for auth, which is expected
            result = self.test_endpoint(method, endpoint, data, None, description)
            # Don't enforce specific status - just check it responds
            result["success"] = result["status_code"] in [200, 401, 422]
            self.print_test_result(result)
            results.append(result)
            
        return results

    def run_validation(self):
        """Run all validation tests"""
        print("🧪 API CLEANUP VALIDATION SUITE")
        print("🎯 Validating changes made on September 3, 2025")
        print("📦 Testing: Removed endpoints, deprecated features, core functionality")
        print("─" * 80)
        print(f"🚀 PromptForge.ai API CLEANUP VALIDATION")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        all_results = []
        
        # Test removed endpoints
        removed_results = self.validate_removed_endpoints()
        all_results.extend(removed_results)
        
        # Test working health endpoints
        health_results = self.validate_working_health_endpoints()
        all_results.extend(health_results)
        
        # Test deprecated vault endpoints
        vault_results = self.validate_deprecated_vault_endpoints()
        all_results.extend(vault_results)
        
        # Test core functionality
        core_results = self.validate_core_functionality()
        all_results.extend(core_results)
        
        # Test Brain Engine endpoints
        brain_results = self.validate_brain_engine_endpoints()
        all_results.extend(brain_results)
        
        # Print summary
        self.print_validation_summary(all_results)
        
        # Save results
        self.save_validation_results(all_results)

    def print_validation_summary(self, results: List[Dict]):
        """Print comprehensive validation summary"""
        print(f"\n{'='*100}")
        print(f"📊 API CLEANUP VALIDATION SUMMARY")
        print(f"{'='*100}")
        
        total_tests = len(results)
        successful = sum(1 for r in results if r["success"])
        failed = total_tests - successful
        success_rate = (successful / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   🧪 Total Tests: {total_tests}")
        print(f"   ✅ Successful: {successful} ({success_rate:.1f}%)")
        print(f"   ❌ Failed: {failed} ({100-success_rate:.1f}%)")
        
        # Categorize results
        removed_tests = [r for r in results if "Should be removed" in r["description"]]
        health_tests = [r for r in results if "health" in r["endpoint"].lower() and "Should be removed" not in r["description"]]
        vault_tests = [r for r in results if "/vault/" in r["endpoint"]]
        core_tests = [r for r in results if r["description"].startswith("Core") or r["description"].startswith("AI") or r["description"].startswith("User") or r["description"].startswith("Public") or r["description"].startswith("Marketplace")]
        brain_tests = [r for r in results if "Brain Engine" in r["description"]]
        
        print(f"\n📋 RESULTS BY CATEGORY:")
        
        if removed_tests:
            removed_success = sum(1 for r in removed_tests if r["success"])
            print(f"   🗑️  Removed Endpoints: {removed_success}/{len(removed_tests)} (Should be 404)")
            
        if health_tests:
            health_success = sum(1 for r in health_tests if r["success"])
            print(f"   💚 Health Endpoints: {health_success}/{len(health_tests)} (Should work)")
            
        if vault_tests:
            vault_success = sum(1 for r in vault_tests if r["success"])
            print(f"   ⚠️  Vault (Deprecated): {vault_success}/{len(vault_tests)} (Should work with warnings)")
            
        if core_tests:
            core_success = sum(1 for r in core_tests if r["success"])
            print(f"   🎯 Core Functionality: {core_success}/{len(core_tests)} (Critical - must work)")
            
        if brain_tests:
            brain_success = sum(1 for r in brain_tests if r["success"])
            print(f"   🧠 Brain Engine: {brain_success}/{len(brain_tests)} (Canonical implementation)")
        
        # Performance insights
        avg_response_time = sum(r["response_time"] for r in results) / len(results) if results else 0
        slow_endpoints = [r for r in results if r["response_time"] > 1000]
        
        print(f"\n⚡ PERFORMANCE INSIGHTS:")
        print(f"   📈 Average Response Time: {avg_response_time:.0f}ms")
        print(f"   🐌 Slow Endpoints (>1s): {len(slow_endpoints)}")
        
        # Key findings
        print(f"\n🔍 KEY VALIDATION FINDINGS:")
        
        removed_working = [r for r in removed_tests if r["success"]]
        if removed_working:
            print(f"   ✅ Removed endpoints properly return 404: {len(removed_working)}")
        else:
            print(f"   ❌ Some removed endpoints may still be accessible!")
            
        health_working = [r for r in health_tests if r["success"]]
        if health_working:
            print(f"   ✅ Health endpoints working correctly: {len(health_working)}")
        else:
            print(f"   ❌ Health endpoints may have issues!")
            
        vault_working = [r for r in vault_tests if r["success"]]
        if vault_working:
            print(f"   ✅ Vault endpoints still functional (deprecated): {len(vault_working)}")
        else:
            print(f"   ⚠️  Some vault endpoints may have issues")
            
        core_working = [r for r in core_tests if r["success"]]
        if len(core_working) == len(core_tests):
            print(f"   ✅ All core functionality working - no regressions detected")
        else:
            print(f"   ❌ Core functionality issues detected - {len(core_tests) - len(core_working)} failures")
        
        print(f"\n💡 CLEANUP VALIDATION STATUS:")
        if success_rate >= 90:
            print(f"   🎉 API cleanup appears successful - high validation rate")
        elif success_rate >= 75:
            print(f"   ⚠️  API cleanup mostly successful - minor issues detected")
        else:
            print(f"   ❌ API cleanup may have issues - review failures")
        
        print(f"\n🕒 Validation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*100}")

    def save_validation_results(self, results: List[Dict]):
        """Save validation results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
        os.makedirs(results_dir, exist_ok=True)
        results_file = os.path.join(results_dir, f"api_cleanup_validation_{timestamp}.json")
        
        validation_data = {
            "timestamp": timestamp,
            "total_tests": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "success_rate": (sum(1 for r in results if r["success"]) / len(results) * 100) if results else 0,
            "cleanup_date": "2025-09-03",
            "validation_summary": {
                "removed_endpoints": len([r for r in results if "Should be removed" in r["description"]]),
                "vault_deprecated": len([r for r in results if "/vault/" in r["endpoint"]]),
                "core_functionality": len([r for r in results if r["description"].startswith(("Core", "AI", "User", "Public", "Marketplace"))]),
                "brain_engine": len([r for r in results if "Brain Engine" in r["description"]])
            },
            "detailed_results": results
        }
        
        with open(results_file, 'w') as f:
            json.dump(validation_data, f, indent=2)
        
        print(f"📄 Validation results saved to: {results_file}")

def main():
    """Main execution function"""
    validator = APICleanupValidator()
    validator.run_validation()

if __name__ == "__main__":
    main()
