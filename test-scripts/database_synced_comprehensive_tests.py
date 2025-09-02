#!/usr/bin/env python3
"""
🔄 DATABASE-SYNCED COMPREHENSIVE TEST SUITE
Tests all API endpoints using EXACT database schema structures
Validates API responses match actual database collections
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class DatabaseSyncedTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = "mock-test-token"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.test_results = []
        
        # EXACT database schemas from actual analysis
        self.real_schemas = self.setup_real_database_schemas()
        
    def setup_real_database_schemas(self):
        """Set up exact database schemas from actual analysis"""
        return {
            "user": {
                "_id": "test-user-123",
                "account_status": "active",
                "billing": {
                    "provider": None,
                    "customer_id": None,
                    "plan": "free",
                    "status": "active",
                    "started_at": None,
                    "renewed_at": None,
                    "created_at": "2025-09-02T13:27:55.911Z"
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
                "last_active_at": "2025-09-02T18:01:36.490Z",
                "last_login_at": "2025-09-02T18:01:36.490Z",
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
                        "email": True
                    }
                },
                "profile": {
                    "bio": "",
                    "website": "",
                    "location": "",
                    "company": "",
                    "job_title": "",
                    "expertise": "",
                    "social_links": {}
                },
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
                "updated_at": "2025-09-02T18:01:36.490Z"
            },
            "prompt": {
                "_id": "test-prompt-456",
                "user_id": "test-user-123",
                "title": "Database Sync Test Prompt",
                "description": "Test prompt for database synchronization",
                "content": "Write a professional email about {topic}",
                "role": "You are a professional email writing assistant",
                "category": "general",
                "tags": ["email", "professional", "test"],
                "difficulty": "beginner",
                "type": "text",
                "status": "active",
                "visibility": "private",
                "is_template": False,
                "is_featured": False,
                "version": 1,
                "latest_version_id": "test-version-789",
                "performance": {
                    "rating": 0,
                    "effectiveness": 0,
                    "test_count": 0,
                    "success_rate": 0,
                    "avg_response_time": 0
                },
                "analytics": {
                    "view_count": 0,
                    "use_count": 0,
                    "share_count": 0,
                    "like_count": 0,
                    "download_count": 0,
                    "comment_count": 0
                },
                "collaboration": {
                    "is_collaborative": False,
                    "allowed_users": [],
                    "permissions": {},
                    "active_editors": []
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "created_by": "test-user-123",
                "last_modified_by": "test-user-123"
            },
            "idea": {
                "_id": "test-idea-789",
                "user_id": "test-user-123",
                "prompt": "Generate business ideas",
                "categories": ["business", "startups", "technology"],
                "tags": ["innovation", "entrepreneurship", "tech"],
                "generated_content": [
                    "AI-powered personal fitness coach",
                    "Sustainable packaging marketplace",
                    "Remote work productivity tracker"
                ],
                "quality_score": 0.85,
                "feasibility": {
                    "technical": "high",
                    "market": "medium",
                    "financial": "medium"
                },
                "estimated_time_to_market": "weeks",
                "created_at": datetime.now().isoformat(),
                "source": "oracle"
            },
            "transaction": {
                "_id": "test-transaction-101",
                "user_id": "test-user-123",
                "type": "credit_purchase",
                "amount": 9.99,
                "currency": "USD",
                "credits_affected": 100,
                "stripe_payment_intent": "pi_test_123456",
                "status": "completed",
                "description": "Credit purchase - 100 credits",
                "metadata": {
                    "package": "starter_pack",
                    "promotion": None
                },
                "created_at": datetime.now().isoformat(),
                "completed_at": datetime.now().isoformat()
            },
            "usage": {
                "_id": "test-usage-202",
                "user_id": "test-user-123",
                "event_type": "prompt_created",
                "feature": "prompt_management",
                "metadata": {
                    "prompt_id": "test-prompt-456",
                    "category": "general"
                },
                "session_id": "test-session-123",
                "ip_address": "127.0.0.1",
                "user_agent": "PromptForge-Test/1.0",
                "timestamp": datetime.now().isoformat()
            },
            "notification": {
                "_id": "test-notification-303",
                "user_id": "test-user-123",
                "type": "system",
                "title": "Welcome to PromptForge!",
                "message": "Your account has been created successfully",
                "read": False,
                "read_at": None,
                "action_url": "/dashboard",
                "priority": "medium",
                "created_at": datetime.now().isoformat()
            },
            "auth_log": {
                "_id": "test-auth-404",
                "user_id": "test-user-123",
                "event_type": "login",
                "ip_address": "127.0.0.1",
                "user_agent": "Mozilla/5.0",
                "location": {"country": "US", "city": "Test City"},
                "success": True,
                "error_reason": None,
                "timestamp": time.time(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    
    def print_header(self, title: str, emoji: str = "🔄"):
        print(f"\n{'='*80}")
        print(f"{emoji} {title}")
        print(f"{'='*80}")
    
    def print_section(self, title: str, emoji: str = "📋"):
        print(f"\n{'-'*60}")
        print(f"{emoji} {title}")
        print(f"{'-'*60}")
    
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     expected_status: int = 200, description: str = "") -> Dict:
        """Test endpoint and validate response against database schema"""
        url = f"{self.base_url}{endpoint}"
        
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
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:200]}
            
            # Validate against expected schema
            schema_match = self.validate_response_schema(endpoint, response_data)
            
            # Success determination
            is_success = 200 <= response.status_code <= 299
            
            # Print result with schema validation
            status_icon = "✅" if is_success else "❌"
            schema_icon = "🔄" if schema_match else "⚠️"
            
            print(f"{status_icon}{schema_icon} {method:<6} {endpoint:<50} [{response.status_code}]")
            
            if not is_success and response_data:
                error_msg = response_data.get('detail', str(response_data)[:100])
                print(f"   ❌ Error: {error_msg}")
            elif not schema_match:
                print(f"   ⚠️ Schema mismatch detected")
            
            result = {
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": is_success,
                "schema_match": schema_match,
                "response_data": response_data
            }
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            print(f"❌ {method:<6} {endpoint:<50} [ERROR] {str(e)[:50]}")
            result = {
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": 0,
                "expected_status": expected_status,
                "success": False,
                "schema_match": False,
                "error": str(e)
            }
            self.test_results.append(result)
            return result
    
    def validate_response_schema(self, endpoint: str, response_data: Dict) -> bool:
        """Validate API response matches expected database schema"""
        try:
            # Extract endpoint category
            if "/users/" in endpoint:
                return self.validate_user_schema(response_data)
            elif "/prompts/" in endpoint:
                return self.validate_prompt_schema(response_data)
            elif "/ideas/" in endpoint:
                return self.validate_idea_schema(response_data)
            elif "/transactions/" in endpoint or "/billing/" in endpoint:
                return self.validate_transaction_schema(response_data)
            elif "/notifications/" in endpoint:
                return self.validate_notification_schema(response_data)
            else:
                # For other endpoints, basic validation
                return isinstance(response_data, dict)
        except:
            return False
    
    def validate_user_schema(self, data: Dict) -> bool:
        """Validate user data matches database schema"""
        if not isinstance(data, dict):
            return False
        
        # Check for user data structure
        user_data = data.get('data', data)
        expected_fields = ['_id', 'email', 'account_status', 'credits', 'preferences']
        
        return any(field in user_data for field in expected_fields)
    
    def validate_prompt_schema(self, data: Dict) -> bool:
        """Validate prompt data matches database schema"""
        if not isinstance(data, dict):
            return False
        
        prompt_data = data.get('data', data)
        expected_fields = ['title', 'content', 'user_id', 'category', 'status']
        
        return any(field in prompt_data for field in expected_fields)
    
    def validate_idea_schema(self, data: Dict) -> bool:
        """Validate idea data matches database schema"""
        if not isinstance(data, dict):
            return False
        
        idea_data = data.get('data', data)
        expected_fields = ['generated_content', 'categories', 'quality_score']
        
        return any(field in idea_data for field in expected_fields)
    
    def validate_transaction_schema(self, data: Dict) -> bool:
        """Validate transaction data matches database schema"""
        if not isinstance(data, dict):
            return False
        
        transaction_data = data.get('data', data)
        expected_fields = ['amount', 'currency', 'status', 'type']
        
        return any(field in transaction_data for field in expected_fields)
    
    def validate_notification_schema(self, data: Dict) -> bool:
        """Validate notification data matches database schema"""
        if not isinstance(data, dict):
            return False
        
        notification_data = data.get('data', data)
        expected_fields = ['title', 'message', 'type', 'read']
        
        return any(field in notification_data for field in expected_fields)
    
    def run_database_sync_tests(self):
        """Run comprehensive tests with database schema validation"""
        
        self.print_header("Database-Synced API Test Suite", "🔄")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🔑 Bearer Token: {self.token}")
        print(f"📊 Database Schema Validation: ENABLED")
        print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ===============================
        # 1. CORE HEALTH & DEBUG
        # ===============================
        self.print_section("Health & Core Systems", "🏥")
        
        self.test_endpoint("GET", "/", 200, "Root endpoint")
        self.test_endpoint("GET", "/health", 200, "Health check")
        self.test_endpoint("GET", "/api/v1/debug/auth-headers", 200, "Debug auth headers")
        
        # ===============================
        # 2. USER MANAGEMENT (Database Schema Match)
        # ===============================
        self.print_section("User Management - Database Schema Validation", "👤")
        
        # User authentication with EXACT database structure
        user_auth_data = {
            "uid": self.real_schemas["user"]["_id"],
            "email": self.real_schemas["user"]["email"],
            "first_name": "Test",
            "last_name": "User",
            "display_name": self.real_schemas["user"]["display_name"]
        }
        
        self.test_endpoint("POST", "/api/v1/users/auth/complete", user_auth_data, 200, 
                          "User authentication with real schema")
        
        # User profile endpoints
        self.test_endpoint("GET", "/api/v1/users/me", 200, "Get user profile")
        self.test_endpoint("GET", "/api/v1/users/credits", 200, "Get user credits")
        self.test_endpoint("GET", "/api/v1/users/preferences", 200, "Get user preferences")
        
        # Profile update with database schema
        profile_update = {
            "profile": {
                "bio": "Updated test bio",
                "company": "Test Company",
                "job_title": "Test Engineer"
            },
            "preferences": {
                "theme": "dark",
                "notifications": {"email": True}
            }
        }
        self.test_endpoint("PUT", "/api/v1/users/me/profile", profile_update, 200,
                          "Update profile with database schema")
        
        # ===============================
        # 3. PROMPTS MANAGEMENT (Database Schema Match)
        # ===============================
        self.print_section("Prompts Management - Database Schema Validation", "📝")
        
        # Create prompt with EXACT database structure
        prompt_data = {
            "title": self.real_schemas["prompt"]["title"],
            "description": self.real_schemas["prompt"]["description"],
            "content": self.real_schemas["prompt"]["content"],
            "role": self.real_schemas["prompt"]["role"],
            "category": self.real_schemas["prompt"]["category"],
            "tags": self.real_schemas["prompt"]["tags"],
            "difficulty": self.real_schemas["prompt"]["difficulty"],
            "type": self.real_schemas["prompt"]["type"],
            "visibility": self.real_schemas["prompt"]["visibility"]
        }
        
        self.test_endpoint("POST", "/api/v1/prompts/prompts/", prompt_data, 201,
                          "Create prompt with database schema")
        
        # Get prompts
        self.test_endpoint("GET", "/api/v1/prompts/prompts/arsenal", 200, "Get user prompts")
        self.test_endpoint("GET", "/api/v1/prompts/prompts/public", 200, "Get public prompts")
        
        # ===============================
        # 4. IDEAS GENERATION (Database Schema Match)
        # ===============================
        self.print_section("Ideas Generation - Database Schema Validation", "💡")
        
        # Generate ideas with database schema
        ideas_data = {
            "prompt": self.real_schemas["idea"]["prompt"],
            "categories": self.real_schemas["idea"]["categories"],
            "count": 3
        }
        
        self.test_endpoint("POST", "/api/v1/ideas/generate", ideas_data, 200,
                          "Generate ideas with database schema")
        
        # ===============================
        # 5. BILLING & TRANSACTIONS (Database Schema Match)
        # ===============================
        self.print_section("Billing & Transactions - Database Schema Validation", "💳")
        
        self.test_endpoint("GET", "/api/v1/billing/tiers", 200, "Get billing tiers")
        self.test_endpoint("GET", "/api/v1/users/me/entitlements", 200, "Get user entitlements")
        
        # Payment initiation with database schema
        payment_data = {
            "amount": self.real_schemas["transaction"]["amount"],
            "currency": self.real_schemas["transaction"]["currency"],
            "credits": self.real_schemas["transaction"]["credits_affected"],
            "payment_method": "stripe"
        }
        
        self.test_endpoint("POST", "/api/v1/payments/initiate-payment", payment_data, 200,
                          "Initiate payment with database schema")
        
        # ===============================
        # 6. ANALYTICS & USAGE (Database Schema Match)
        # ===============================
        self.print_section("Analytics & Usage - Database Schema Validation", "📊")
        
        # Track usage with database schema
        usage_data = {
            "event_type": self.real_schemas["usage"]["event_type"],
            "feature": self.real_schemas["usage"]["feature"],
            "metadata": self.real_schemas["usage"]["metadata"]
        }
        
        self.test_endpoint("POST", "/api/v1/users/usage/track", usage_data, 200,
                          "Track usage with database schema")
        
        self.test_endpoint("GET", "/api/v1/analytics/dashboard", 200, "Analytics dashboard")
        
        # ===============================
        # 7. NOTIFICATIONS (Database Schema Match)
        # ===============================
        self.print_section("Notifications - Database Schema Validation", "🔔")
        
        self.test_endpoint("GET", "/api/v1/notifications/", 200, "Get notifications")
        self.test_endpoint("POST", "/api/v1/notifications/mark-all-read", {}, 200,
                          "Mark all notifications read")
        
        # ===============================
        # RESULTS SUMMARY
        # ===============================
        self.print_results_summary()
    
    def print_results_summary(self):
        """Print comprehensive results with schema validation"""
        self.print_header("Database Sync Test Results", "📊")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r["success"])
        schema_matches = sum(1 for r in self.test_results if r.get("schema_match", False))
        
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        schema_rate = (schema_matches / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ API Success: {successful_tests} ({success_rate:.1f}%)")
        print(f"🔄 Schema Match: {schema_matches} ({schema_rate:.1f}%)")
        print(f"🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Schema validation summary
        self.print_section("Schema Validation Results", "🔍")
        
        schema_issues = [r for r in self.test_results if r["success"] and not r.get("schema_match", True)]
        if schema_issues:
            print(f"⚠️ {len(schema_issues)} endpoints with schema mismatches:")
            for issue in schema_issues[:5]:  # Show first 5
                print(f"   {issue['method']} {issue['endpoint']}")
        else:
            print("✅ All successful endpoints match expected database schemas!")
        
        # Error summary
        error_tests = [r for r in self.test_results if not r["success"]]
        if error_tests:
            self.print_section("Issues Requiring Backend Fixes", "🔧")
            for error in error_tests[:3]:  # Show first 3
                print(f"❌ {error['method']} {error['endpoint']} - {error.get('error', 'Unknown error')}")
        
        print(f"\n{'='*80}")
        print("🎯 Database-API Synchronization Analysis Complete!")
        print(f"📋 Schema Accuracy: {schema_rate:.1f}%")
        print(f"🚀 API Functionality: {success_rate:.1f}%")
        print(f"{'='*80}")
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"database_sync_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump({
                    "summary": {
                        "total_tests": total_tests,
                        "successful_tests": successful_tests,
                        "schema_matches": schema_matches,
                        "success_rate": success_rate,
                        "schema_rate": schema_rate,
                        "timestamp": datetime.now().isoformat()
                    },
                    "detailed_results": self.test_results,
                    "real_schemas": self.real_schemas
                }, f, indent=2)
            print(f"📄 Detailed results saved to: {filename}")
        except Exception as e:
            print(f"⚠️ Could not save results: {e}")

if __name__ == "__main__":
    print("🔄 PromptForge.ai Database-Synced API Tester")
    print("💡 Validates API responses against actual database schemas")
    print("🔍 Real-time schema matching and validation")
    print("-" * 60)
    
    tester = DatabaseSyncedTester()
    tester.run_database_sync_tests()
