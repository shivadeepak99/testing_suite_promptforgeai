#!/usr/bin/env python3
"""
🔍 Quick API-Database Sync Validation
Tests the critical endpoints to verify fixes have been applied
"""

import requests
import json
from datetime import datetime

class QuickSyncValidator:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "critical_tests": [],
            "summary": {}
        }
        
    def test_prompts_creation(self):
        """Test if prompts API accepts correct schema (no 'body' field)"""
        url = f"{self.base_url}/api/v1/prompts/prompts/"
        
        # Test with correct schema (database fields)
        correct_payload = {
            "title": "Test Sync Fix",
            "description": "Testing if API accepts database schema",
            "content": "This is the actual content field",
            "role": "user",
            "category": "general",
            "tags": ["test", "sync"],
            "difficulty": "beginner",
            "type": "text",
            "visibility": "private"
        }
        
        try:
            response = requests.post(url, json=correct_payload)
            success = response.status_code != 422  # Should not be validation error
            
            self.results["critical_tests"].append({
                "test": "Prompts Creation Schema Fix",
                "endpoint": "POST /api/v1/prompts/prompts/",
                "status_code": response.status_code,
                "success": success,
                "issue": "API should accept database fields (no 'body' required)",
                "fix_applied": success
            })
            
        except Exception as e:
            self.results["critical_tests"].append({
                "test": "Prompts Creation Schema Fix",
                "endpoint": "POST /api/v1/prompts/prompts/",
                "success": False,
                "error": str(e),
                "fix_applied": False
            })
            
    def test_ideas_generation(self):
        """Test if ideas API accepts correct schema (no 'complexity' field)"""
        url = f"{self.base_url}/api/v1/ideas/generate"
        
        # Test with correct schema (database fields)
        correct_payload = {
            "prompt": "Generate test ideas",
            "categories": ["technology", "business"],
            "count": 3
        }
        
        try:
            response = requests.post(url, json=correct_payload)
            success = response.status_code != 422  # Should not be validation error
            
            self.results["critical_tests"].append({
                "test": "Ideas Generation Schema Fix",
                "endpoint": "POST /api/v1/ideas/generate",
                "status_code": response.status_code,
                "success": success,
                "issue": "API should accept database fields (no 'complexity' required)",
                "fix_applied": success
            })
            
        except Exception as e:
            self.results["critical_tests"].append({
                "test": "Ideas Generation Schema Fix", 
                "endpoint": "POST /api/v1/ideas/generate",
                "success": False,
                "error": str(e),
                "fix_applied": False
            })
            
    def test_missing_endpoints(self):
        """Test if missing endpoints have been added"""
        endpoints_to_check = [
            "/api/v1/users/me/entitlements",
            "/api/v1/notifications/"
        ]
        
        for endpoint in endpoints_to_check:
            url = f"{self.base_url}{endpoint}"
            
            try:
                response = requests.get(url)
                success = response.status_code != 404  # Should not be Not Found
                
                self.results["critical_tests"].append({
                    "test": f"Missing Endpoint Fix - {endpoint}",
                    "endpoint": f"GET {endpoint}",
                    "status_code": response.status_code,
                    "success": success,
                    "issue": "Endpoint should exist (not return 404)",
                    "fix_applied": success
                })
                
            except Exception as e:
                self.results["critical_tests"].append({
                    "test": f"Missing Endpoint Fix - {endpoint}",
                    "endpoint": f"GET {endpoint}",
                    "success": False,
                    "error": str(e),
                    "fix_applied": False
                })
                
    def test_user_field_naming(self):
        """Test if user API uses consistent field naming"""
        url = f"{self.base_url}/api/v1/users/me"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for consistent naming (either all snake_case or all camelCase)
                has_snake_case = any(key for key in data.keys() if '_' in key)
                has_camel_case = any(key for key in data.keys() if key != key.lower() and '_' not in key)
                
                consistent_naming = not (has_snake_case and has_camel_case)
                
                self.results["critical_tests"].append({
                    "test": "User Field Naming Consistency",
                    "endpoint": "GET /api/v1/users/me",
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "consistent_naming": consistent_naming,
                    "field_style": "snake_case" if has_snake_case else "camelCase" if has_camel_case else "unknown",
                    "issue": "Field naming should be consistent (all snake_case or all camelCase)",
                    "fix_applied": consistent_naming
                })
            else:
                self.results["critical_tests"].append({
                    "test": "User Field Naming Consistency",
                    "endpoint": "GET /api/v1/users/me", 
                    "status_code": response.status_code,
                    "success": False,
                    "fix_applied": False
                })
                
        except Exception as e:
            self.results["critical_tests"].append({
                "test": "User Field Naming Consistency",
                "endpoint": "GET /api/v1/users/me",
                "success": False,
                "error": str(e),
                "fix_applied": False
            })
            
    def run_validation(self):
        """Run all critical validation tests"""
        print("🔍 Running quick sync validation...")
        print("="*50)
        
        self.test_prompts_creation()
        self.test_ideas_generation()
        self.test_missing_endpoints()
        self.test_user_field_naming()
        
        # Calculate summary
        total_tests = len(self.results["critical_tests"])
        fixes_applied = len([t for t in self.results["critical_tests"] if t.get("fix_applied")])
        
        self.results["summary"] = {
            "total_critical_tests": total_tests,
            "fixes_applied": fixes_applied,
            "fixes_remaining": total_tests - fixes_applied,
            "sync_progress": f"{fixes_applied}/{total_tests} ({fixes_applied/total_tests*100:.1f}%)"
        }
        
        return self.results
        
    def print_results(self):
        """Print validation results"""
        results = self.run_validation()
        
        print(f"\n📊 Sync Validation Results")
        print("="*50)
        
        for test in results["critical_tests"]:
            status = "✅" if test.get("fix_applied") else "❌"
            print(f"{status} {test['test']}")
            print(f"   Endpoint: {test['endpoint']}")
            if 'status_code' in test:
                print(f"   Status: {test['status_code']}")
            if 'error' in test:
                print(f"   Error: {test['error']}")
            print()
            
        summary = results["summary"]
        print(f"🎯 Summary: {summary['sync_progress']} critical fixes applied")
        
        if summary['fixes_remaining'] > 0:
            print(f"⚠️  {summary['fixes_remaining']} critical fixes still needed")
            print("\n🔧 Apply the fixes from:")
            print("   - results/DATABASE_API_SYNC_REPORT.md")
            print("   - results/api_fixes_*.json")
        else:
            print("🎉 All critical fixes have been applied!")
            print("\n🧪 Run full test suite for complete validation:")
            print("   python test-scripts/database_synced_comprehensive_tests.py")
            
        # Save detailed results
        filename = f"results/quick_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📋 Detailed results saved to: {filename}")

if __name__ == "__main__":
    validator = QuickSyncValidator()
    validator.print_results()
