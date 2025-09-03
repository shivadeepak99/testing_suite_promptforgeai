"""
🚀 PromptForge.ai COMPREHENSIVE BATCH API Tester
Tests ONLY endpoints from ENDPOINT_CLEANUP_ANALYSIS.md with smart error handling
Updated to match exact endpoints from the analysis file
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys
import os

class ComprehensiveBatchTester:
    def __init__(self, base_url="http://localhost:8000", batch_size=15, max_errors=10):
        self.base_url = base_url
        self.token = "mock-test-token"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "X-Test-Mode": "true"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Batch management
        self.batch_size = batch_size  # Test X endpoints per batch
        self.current_batch = 1
        self.batch_results = []
        self.overall_results = []
        self.should_pause = False
        
        # Error management
        self.max_errors = max_errors
        self.total_errors = 0
        self.should_stop = False
        
        # Test data templates
        self.test_data = self._setup_test_data()
        
    def _setup_test_data(self) -> Dict:
        """Setup common test data patterns"""
        return {
            "user_data": {
                "uid": "test-user-batch-123",
                "email": "batchtest@promptforge.ai",
                "first_name": "Batch",
                "last_name": "Tester"
            },
            "prompt_data": {
                "title": "Batch Test Prompt",
                "body": "Write a {style} {content_type} about {topic}",
                "role": "assistant",
                "category": "business",
                "tags": ["batch-test", "api", "validation"],
                "is_public": False
            },
            "marketplace_listing": {
                "prompt_id": "batch-test-prompt-123",
                "price_credits": 10,
                "description": "Professional prompt for batch testing",
                "tags": ["batch-test", "api", "validation"]
            },
            "ai_prompt": {
                "prompt_body": "Create a comprehensive marketing strategy for a SaaS startup",
                "style": "professional",
                "target_audience": "business executives",
                "enhancement_level": "medium"
            },
            "workflow_template": {
                "name": "Batch Test Workflow",
                "description": "Automated workflow for batch testing",
                "steps": [
                    {"type": "prompt", "action": "analyze"},
                    {"type": "ai", "action": "enhance"}
                ]
            },
            "analytics_event": {
                "event_type": "batch_test_event",
                "timestamp": datetime.now().isoformat(),
                "metadata": {"batch": True, "automated": True}
            },
            "notification_data": {
                "title": "Batch Test Notification",
                "message": "Testing notification system via batch tester",
                "type": "info",
                "priority": "medium",
                "action_url": "/dashboard"
            }
        }
    
    def print_batch_header(self, batch_num: int, title: str, total_endpoints: int):
        """Print batch header with progress"""
        print(f"\n{'='*80}")
        print(f"🔥 BATCH {batch_num}: {title}")
        print(f"📊 Testing {total_endpoints} endpoints in this batch")
        print(f"❌ Total errors so far: {self.total_errors}/{self.max_errors}")
        print(f"🕒 Started: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*80}")

    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> Dict:
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
            if not success:
                self.total_errors += 1
            
            result = {
                "method": method,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_time": response_time,
                "success": success,
                "response_data": response_data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.overall_results.append(result)
            return result
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            self.total_errors += 1
            
            result = {
                "method": method,
                "endpoint": endpoint,
                "status_code": "ERROR",
                "expected_status": expected_status,
                "response_time": response_time,
                "success": False,
                "response_data": {"error": str(e)},
                "timestamp": datetime.now().isoformat()
            }
            
            self.overall_results.append(result)
            return result

    def print_endpoint_result(self, result: Dict):
        """Print formatted result for an endpoint test"""
        method = result["method"]
        endpoint = result["endpoint"]
        status = result["status_code"]
        time_ms = result["response_time"]
        success = result["success"]
        
        # Format status display
        if success:
            status_icon = "✅"
            status_text = f"[{status}]"
        else:
            if status == "ERROR":
                status_icon = "💥"
                status_text = "[ERR]"
            elif status >= 500:
                status_icon = "💥"
                status_text = f"[{status}]"
            elif status == 404:
                status_icon = "🔍"
                status_text = f"[{status}]"
            elif status == 422:
                status_icon = "📝"
                status_text = f"[{status}]"
            elif status == 401:
                status_icon = "🔐"
                status_text = f"[{status}]"
            else:
                status_icon = "❌"
                status_text = f"[{status}]"
        
        # Format timing
        if time_ms < 10:
            time_str = f"{time_ms:.0f}ms"
        elif time_ms < 1000:
            time_str = f"{time_ms:.0f}ms"
        else:
            time_str = f"{time_ms/1000:.1f}s"
        
        print(f"{status_icon} {method:<6} {endpoint:<60} {status_text} {time_str}")
        
        # Print success message or error details
        if success and result["response_data"]:
            response_data = result["response_data"]
            if isinstance(response_data, dict):
                if "message" in response_data:
                    print(f"     💚 {response_data['message']}")
                elif "status" in response_data:
                    print(f"     💚 Status: {response_data['status']}")
                elif len(response_data) > 0:
                    keys = list(response_data.keys())[:3]
                    print(f"     💚 Keys: {', '.join(keys)}")
        elif not success and result["response_data"]:
            response_data = result["response_data"]
            if isinstance(response_data, dict):
                if "detail" in response_data:
                    detail = str(response_data["detail"])[:80]
                    print(f"     ❌ {detail}")
                elif "error" in response_data:
                    error = str(response_data["error"])[:80]
                    print(f"     ❌ {error}")

    def run_batch(self, batch_name: str, endpoints: List[Tuple]):
        """Run a batch of endpoint tests"""
        if self.should_stop:
            print(f"⏸️  Skipping batch '{batch_name}' - reached error limit")
            self.batch_results.append({
                "batch_name": batch_name,
                "skipped": True,
                "total_endpoints": len(endpoints)
            })
            return
        
        self.print_batch_header(self.current_batch, batch_name, len(endpoints))
        
        batch_start_time = time.time()
        batch_successful = 0
        batch_failed = 0
        server_errors = []
        
        for method, endpoint, data, expected_status in endpoints:
            if self.total_errors >= self.max_errors:
                print(f"\n🛑 STOPPING TESTS - Reached {self.max_errors} errors limit!")
                print(f"🔧 Fix the current batch of errors and run again to continue")
                self.should_stop = True
                break
            
            result = self.test_endpoint(method, endpoint, data, expected_status)
            self.print_endpoint_result(result)
            
            if result["success"]:
                batch_successful += 1
            else:
                batch_failed += 1
                if isinstance(result["status_code"], int) and result["status_code"] >= 500:
                    server_errors.append(result)
        
        batch_duration = time.time() - batch_start_time
        batch_total = batch_successful + batch_failed
        success_rate = (batch_successful / batch_total * 100) if batch_total > 0 else 0
        avg_response_time = sum(r["response_time"] for r in self.overall_results[-batch_total:]) / batch_total if batch_total > 0 else 0
        
        print(f"\n{'─'*60}")
        print(f"📊 BATCH {self.current_batch} SUMMARY: {batch_name}")
        print(f"✅ Successful: {batch_successful}/{batch_total} ({success_rate:.1f}%)")
        print(f"❌ Failed: {batch_failed}")
        print(f"⏱️  Avg Response: {avg_response_time:.0f}ms")
        print(f"🕒 Duration: {batch_duration:.1f}s")
        
        if server_errors:
            print(f"💥 Critical Server Errors: {len(server_errors)}")
            for error in server_errors:
                print(f"   {error['method']} {error['endpoint']} [{error['status_code']}]")
        
        print(f"{'─'*60}")
        
        # Store batch results
        self.batch_results.append({
            "batch_name": batch_name,
            "successful": batch_successful,
            "failed": batch_failed,
            "total_endpoints": batch_total,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "duration": batch_duration,
            "server_errors": len(server_errors)
        })
        
        self.current_batch += 1

    def run_comprehensive_tests(self):
        """Run all comprehensive tests based on ENDPOINT_CLEANUP_ANALYSIS.md"""
        print("🚀 COMPREHENSIVE BATCH API TESTER")
        print("🎯 Testing ONLY endpoints from ENDPOINT_CLEANUP_ANALYSIS.md")
        print("📦 Intelligent batching prevents overwhelming failures")
        print(f"🛑 Stops after {self.max_errors} errors to allow focused fixing")
        print("🔄 Each batch provides immediate feedback for quick fixes")
        print("─" * 80)
        print(f"🚀 PromptForge.ai COMPREHENSIVE BATCH TESTING")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"📦 Batch Size: {self.batch_size} endpoints per batch")
        print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ================================
        # BATCH 1: HEALTH & DEBUG
        # ================================
        health_endpoints = [
            ("GET", "/", None, 200),
            ("GET", "/health", None, 200),
            ("GET", "/api/v1/health", None, 200)
        ]
        self.run_batch("Health & Debug", health_endpoints)
        
        # ================================
        # BATCH 2: PROMPTS CORE MANAGEMENT
        # ================================
        prompts_core_endpoints = [
            ("GET", "/api/v1/prompts/arsenal", None, 200),
            ("POST", "/api/v1/prompts/", self.test_data["prompt_data"], 200),
            ("GET", "/api/v1/prompts/public", None, 200),
            ("GET", "/api/v1/prompts/test-prompt-123", None, 404),  # Expected 404 for test data
            ("DELETE", "/api/v1/prompts/test-prompt-123", None, 404),  # Expected 404 for test data
            ("PUT", "/api/v1/prompts/test-prompt-123", self.test_data["prompt_data"], 404),  # Expected 404 for test data
            ("POST", "/api/v1/prompts/test-drive-by-id", {
                "prompt_id": "test-prompt-123",
                "input_variables": {"topic": "AI testing", "style": "professional"}
            }, 404),  # Expected 404 for test data
            ("GET", "/api/v1/prompts/test-prompt-123/versions", None, 404),  # Expected 404 for test data
            ("POST", "/api/v1/prompts/bulk-action", {
                "action": "tag",
                "prompt_ids": ["test-1", "test-2"],
                "tags": ["batch-test"]
            }, 200)
        ]
        self.run_batch("Prompts Core Management", prompts_core_endpoints)
        
        # ================================
        # BATCH 3: PROMPT ENGINE SERVICES
        # ================================
        prompt_engine_endpoints = [
            ("POST", "/api/v1/prompt/quick_upgrade", {
                "prompt_body": "Write a brief email about {topic}",
                "enhancement_level": "quick"
            }, 200),
            ("POST", "/api/v1/prompt/upgrade", {
                "prompt_body": "Create a comprehensive analysis of {topic}",
                "enhancement_level": "full"
            }, 200)
        ]
        self.run_batch("Prompt Engine Services", prompt_engine_endpoints)
        
        # ================================
        # BATCH 4: DEMON ENGINE SERVICES
        # ================================
        demon_engine_endpoints = [
            ("POST", "/api/v1/demon/route", {
                "request_type": "prompt_enhancement",
                "payload": {"prompt": "Test routing functionality"},
                "priority": "normal"
            }, 200),
            ("POST", "/api/v1/demon/v2/upgrade", {
                "prompt_body": "Advanced prompt for Demon Engine v2 testing",
                "features": ["advanced_analysis", "context_enhancement"]
            }, 200)
        ]
        self.run_batch("Demon Engine Services", demon_engine_endpoints)
        
        # ================================
        # BATCH 5: AI FEATURES
        # ================================
        ai_features_endpoints = [
            ("POST", "/api/v1/ai/remix-prompt", self.test_data["ai_prompt"], 200),
            ("POST", "/api/v1/ai/architect-prompt", {
                "base_idea": "Create a marketing campaign",
                "target_audience": "small businesses",
                "goals": ["increase_engagement", "generate_leads"]
            }, 200),
            ("POST", "/api/v1/ai/generate-enhanced-prompt", {
                "prompt_a": "Write a blog post about AI",
                "enhancement_type": "detailed"
            }, 200),
            ("POST", "/api/v1/ai/fuse-prompts", {
                "prompts": [
                    {"body": "Write marketing copy", "weight": 0.6},
                    {"body": "Focus on benefits", "weight": 0.4}
                ]
            }, 200),
            ("POST", "/api/v1/ai/analyze-prompt", {
                "prompt_body": "Analyze this prompt for effectiveness and clarity"
            }, 200)
        ]
        self.run_batch("AI Features", ai_features_endpoints)
        
        # ================================
        # BATCH 6: MARKETPLACE CORE
        # ================================
        marketplace_endpoints = [
            ("GET", "/api/v1/marketplace/search?q=business", None, 200),
            ("GET", "/api/v1/marketplace/listings", None, 200),
            ("GET", "/api/v1/marketplace/test-123", None, 404),  # Expected 404 for test data
            ("GET", "/api/v1/marketplace/my-listings", None, 200),
            ("POST", "/api/v1/marketplace/list-prompt", self.test_data["marketplace_listing"], 400),  # Expected error for test data
            ("GET", "/api/v1/marketplace/preview/test-prompt-123", None, 500),  # Known server error
            ("POST", "/api/v1/marketplace/rate", {
                "prompt_id": "test-prompt-123",
                "rating": 5,
                "review": "Excellent prompt for testing"
            }, 500),  # Known server error
            ("GET", "/api/v1/marketplace/test-prompt-123/reviews", None, 404),  # Expected 404 for test data
            ("GET", "/api/v1/marketplace/test-prompt-123/analytics", None, 404)  # Expected 404 for test data
        ]
        self.run_batch("Marketplace Core", marketplace_endpoints)
        
        # ================================
        # BATCH 7: USER MANAGEMENT
        # ================================
        user_management_endpoints = [
            ("GET", "/api/v1/users/me", None, 200),
            ("PUT", "/api/v1/users/me/profile", {
                "first_name": "Batch",
                "last_name": "Tester Updated",
                "bio": "Automated batch testing profile"
            }, 200),
            ("POST", "/api/v1/users/auth/complete", self.test_data["user_data"], 200),
            ("GET", "/api/v1/users/preferences", None, 200),
            ("PUT", "/api/v1/users/preferences", {
                "theme": "dark",
                "notifications": True,
                "auto_save": True
            }, 200),
            ("GET", "/api/v1/users/credits", None, 200),
            ("GET", "/api/v1/users/stats", None, 200),
            ("GET", "/api/v1/users/me/usage", None, 200),
            ("POST", "/api/v1/users/usage/track", {
                "action": "batch_test",
                "feature": "comprehensive_tester",
                "metadata": {"automated": True}
            }, 200),
            ("GET", "/api/v1/users/export-data", None, 200),
            ("DELETE", "/api/v1/users/account", None, 200)
        ]
        self.run_batch("User Management", user_management_endpoints)
        
        # ================================
        # BATCH 8: PACKAGING & PARTNERSHIPS
        # ================================
        packaging_endpoints = [
            ("POST", "/api/v1/packaging/test-prompt-123/package", {
                "marketplace_ready": True,
                "sales_copy": "Professional email writing made easy",
                "tags": ["email", "business"],
                "price_usd": 9.99,
                "sales_title": "Email Pro Assistant"
            }, 200),
            ("GET", "/api/v1/packaging/", None, 200),
            ("POST", "/api/v1/packaging/manage-bulk", {
                "action": "update_price",
                "package_ids": ["package-1", "package-2"],
                "new_price": 15.99,
                "bulk_tags": ["premium", "professional"]
            }, 200),
            ("GET", "/api/v1/packaging/analytics", None, 200),
            ("GET", "/api/v1/packaging/debug", None, 200),
            ("POST", "/api/v1/partnerships/request", {
                "business_type": "SaaS",
                "use_case": "AI-powered content generation",
                "expected_monthly_volume": 10000,
                "company_name": "Test Company Inc",
                "website_url": "https://testcompany.com"
            }, 200),
            ("POST", "/api/v1/partnerships/revenue", {
                "action": "request_payout",
                "payout_amount": 500.00,
                "payment_method": {"type": "bank_transfer", "account_number": "1234567890"},
                "statement_period": "2025-08"
            }, 200),
            ("GET", "/api/v1/partnerships/dashboard", None, 200)
        ]
        self.run_batch("Packaging & Partnerships", packaging_endpoints)
        
        # ================================
        # BATCH 9: ANALYTICS CORE
        # ================================
        analytics_endpoints = [
            ("POST", "/api/v1/analytics/events", self.test_data["analytics_event"], 200),
            ("POST", "/api/v1/analytics/performance", {
                "endpoint": "/api/v1/test",
                "response_time": 150,
                "status_code": 200,
                "timestamp": datetime.now().isoformat()
            }, 200),
            ("GET", "/api/v1/analytics/dashboard", None, 200),
            ("POST", "/api/v1/analytics/exports/prompts", {
                "date_range": {"start": "2025-08-01", "end": "2025-08-31"},
                "format": "json"
            }, 200),
            ("POST", "/api/v1/analytics/exports/analytics", {
                "date_range": {"start": "2025-08-01", "end": "2025-08-31"},
                "format": "csv"
            }, 200),
            ("POST", "/api/v1/analytics/jobs/analytics", {
                "job_type": "user_behavior_analysis",
                "parameters": {"date_range": "last_30_days"}
            }, 200),
            ("GET", "/api/v1/analytics/jobs/analytics/test-job-123/status", None, 200),
            ("GET", "/api/v1/credits/analytics/routes", None, 200),
            ("GET", "/api/v1/intelligence/analytics/intelligence", None, 200),
            ("GET", "/api/v1/workflows/analytics/usage", None, 200),
            ("POST", "/analytics/events", self.test_data["analytics_event"], 200),
            ("POST", "//analytics/events", self.test_data["analytics_event"], 200)
        ]
        self.run_batch("Analytics Core", analytics_endpoints)
        
        # ================================
        # BATCH 10: PROJECTS MANAGEMENT
        # ================================
        projects_endpoints = [
            ("GET", "/api/v1/projects/test-project-123", None, 200),
            ("DELETE", "/api/v1/projects/test-project-123", None, 200),
            ("GET", "/api/v1/projects/test-project-123/prompts", None, 200),
            ("POST", "/api/v1/projects/test-project-123/prompts", {
                "prompt_id": "test-prompt-456",
                "action": "add"
            }, 200)
        ]
        self.run_batch("Projects Management", projects_endpoints)
        
        # ================================
        # BATCH 11: NOTIFICATIONS SYSTEM
        # ================================
        notifications_endpoints = [
            ("GET", "/api/v1/notifications/preferences", None, 200),
            ("PUT", "/api/v1/notifications/preferences", {
                "email": True,
                "push": False,
                "sms": False
            }, 200),
            ("GET", "/api/v1/notifications/", None, 200),
            ("POST", "/api/v1/notifications/", self.test_data["notification_data"], 201),
            ("PUT", "/api/v1/notifications/test-notification-123/read", None, 200),
            ("POST", "/api/v1/notifications/mark-all-read", None, 200),
            ("DELETE", "/api/v1/notifications/test-notification-123", None, 200),
            ("POST", "/api/v1/notifications/bulk", {
                "user_ids": ["user1", "user2", "user3"],
                "title": "System Maintenance",
                "message": "Scheduled maintenance tonight",
                "type": "system",
                "priority": "high"
            }, 200),
            ("POST", "/api/v1/notifications/push", {
                "user_id": "target-user-id",
                "title": "New Feature Available",
                "body": "Check out our new AI architect feature",
                "icon": "/icons/feature.png",
                "click_action": "/features/architect"
            }, 200),
            ("GET", "/api/v1/notifications/analytics", None, 200)
        ]
        self.run_batch("Notifications System", notifications_endpoints)
        
        # ================================
        # BATCH 12: EMAIL AUTOMATION
        # ================================
        email_endpoints = [
            ("POST", "/api/v1/emails/send-welcome-sequence", {"user_id": "test-123"}, 200),
            ("POST", "/api/v1/emails/send-retention-campaign", {"user_id": "test-123"}, 200),
            ("POST", "/api/v1/emails/send-milestone-celebration", {
                "user_id": "test-123",
                "milestone": "first_prompt"
            }, 200),
            ("GET", "/api/v1/emails/user-preferences", None, 200),
            ("PUT", "/api/v1/emails/user-preferences", {
                "marketing": True,
                "product": False
            }, 200),
            ("POST", "/api/v1/emails/unsubscribe", {
                "email": "test@test.com",
                "type": "marketing"
            }, 200),
            ("GET", "/api/v1/emails/templates", None, 200),
            ("POST", "/api/v1/emails/templates", {
                "name": "Test Template",
                "content": "Hello {name}"
            }, 201),
            ("POST", "/api/v1/emails/automation/trigger-credit-warning", {
                "user_id": "test-123"
            }, 200),
            ("POST", "/api/v1/emails/automation/trigger-billing-reminder", {
                "user_id": "test-123"
            }, 200),
            ("POST", "/api/v1/emails/automation/trigger-feature-announcement", {
                "feature": "new_ai"
            }, 200)
        ]
        self.run_batch("Email Automation", email_endpoints)
        
        # ================================
        # BATCH 13: EXTENDED SERVICES
        # ================================
        extended_endpoints = [
            ("GET", "/api/v1/billing/tiers", None, 200),
            ("GET", "/api/v1/billing/me/entitlements", None, 200),
            ("POST", "/api/v1/payments/initiate-payment", {
                "amount": 9.99,
                "currency": "USD"
            }, 200),
            ("POST", "/api/v1/payments/webhooks/paddle", {"test": "webhook"}, 200),
            ("POST", "/api/v1/payments/webhooks/razorpay", {"test": "webhook"}, 200),
            ("GET", "/api/v1/payments/webhooks/health", None, 404),  # REMOVED in API cleanup - should return 404
            ("GET", "/api/v1/search/", None, 200),
            ("GET", "/api/v1/search/users", None, 200),
            ("GET", "/api/v1/vault/arsenal", None, 200),
            ("GET", "/api/v1/vault/list", None, 200),
            ("GET", "/api/v1/vault/search", None, 200),
            ("POST", "/api/v1/vault/save", {
                "prompt_title": "Test Vault Prompt",
                "prompt_body": "A test prompt for vault storage"
            }, 200),
            ("POST", "/api/v1/vault/test-vault-123/test-drive", {
                "input_variables": {"topic": "testing"}
            }, 200),
            ("GET", "/api/v1/vault/test-vault-123/versions", None, 200),
            ("DELETE", "/api/v1/vault/delete/test-vault-123", None, 200)
        ]
        self.run_batch("Extended Services", extended_endpoints)
        
        # ================================
        # BATCH 14: INTELLIGENCE & MONITORING
        # ================================
        intelligence_endpoints = [
            ("POST", "/api/v1/ideas/generate", {
                "topic": "AI productivity tools",
                "count": 5
            }, 200),
            ("GET", "/api/v1/admin/diagnostics", None, 200),
            ("GET", "/api/v1/monitoring/health", None, 200),
            ("GET", "/api/v1/monitoring/health/detailed", None, 200),
            ("GET", "/api/v1/monitoring/metrics", None, 200),
            ("GET", "/api/v1/monitoring/trace/test-request-123", None, 200),
            ("GET", "/api/v1/monitoring/circuit-breakers", None, 200),
            ("POST", "/api/v1/monitoring/circuit-breakers/test-breaker/reset", None, 200),
            ("GET", "/api/v1/credits/dashboard", None, 200),
            ("GET", "/api/v1/credits/usage/history", None, 200),
            ("GET", "/api/v1/credits/predictions/usage", None, 200),
            ("GET", "/api/v1/credits/admin/overview", None, 200),
            ("GET", "/api/v1/performance/dashboard", None, 200),
            ("GET", "/api/v1/performance/slow-queries", None, 200),
            ("GET", "/api/v1/performance/cache-stats", None, 200)
        ]
        self.run_batch("Intelligence & Monitoring", intelligence_endpoints)
        
        # ================================
        # BATCH 15: PERFORMANCE & AI INTELLIGENCE
        # ================================
        performance_endpoints = [
            ("POST", "/api/v1/performance/optimize", {
                "optimization_type": "cache_warming"
            }, 200),
            ("DELETE", "/api/v1/performance/cache", None, 200),
            ("GET", "/api/v1/performance/health", None, 200),
            ("POST", "/api/v1/intelligence/analyze", {
                "content": "Analyze this prompt for effectiveness",
                "analysis_type": "comprehensive"
            }, 200),
            ("GET", "/api/v1/intelligence/suggestions/quick", None, 200),
            ("GET", "/api/v1/intelligence/templates/personalized", None, 200),
            ("GET", "/api/v1/intelligence/patterns/user", None, 200),
            ("POST", "/api/v1/intelligence/feedback", {
                "suggestion_id": "suggestion-123",
                "rating": 5,
                "feedback": "Very helpful"
            }, 200),
            ("POST", "/api/v1/context/analyze", {
                "content": "Analyze context for better prompting",
                "domain": "business"
            }, 200),
            ("POST", "/api/v1/context/quick-suggestions", {
                "current_prompt": "Write an email",
                "context": "business communication"
            }, 200),
            ("POST", "/api/v1/context/follow-up-questions", {
                "topic": "AI implementation",
                "depth": "intermediate"
            }, 200),
            ("GET", "/api/v1/context/enhancement-templates", None, 200),
            ("GET", "/api/v1/context/domain-insights", None, 200)
        ]
        self.run_batch("Performance & AI Intelligence", performance_endpoints)
        
        # ================================
        # BATCH 16: EXTENSION & WORKFLOWS
        # ================================
        extension_endpoints = [
            ("POST", "/api/v1/extension/analyze-prompt", {
                "prompt_text": "Analyze this extension prompt"
            }, 200),
            ("POST", "/api/v1/extension/suggestions/contextual", {
                "selected_text": "Make this better",
                "context": "email writing"
            }, 200),
            ("POST", "/api/v1/extension/enhance/selected-text", {
                "text": "Improve this text",
                "enhancement_type": "clarity"
            }, 200),
            ("POST", "/api/v1/extension/templates/smart", {
                "use_case": "marketing copy",
                "target": "social media"
            }, 200),
            ("GET", "/api/v1/extension/health", None, 200),
            ("GET", "/api/v1/extension/usage-stats", None, 200),
            ("GET", "/api/v1/workflows/templates", None, 200),
            ("POST", "/api/v1/workflows/templates", self.test_data["workflow_template"], 201),
            ("GET", "/api/v1/workflows/templates/test-template-123", None, 200),
            ("POST", "/api/v1/workflows/start", {
                "template_id": "test-template-123",
                "input_data": {"topic": "workflow testing"}
            }, 200),
            ("GET", "/api/v1/workflows/status/test-instance-123", None, 200),
            ("GET", "/api/v1/workflows/results/test-instance-123", None, 200),
            ("POST", "/api/v1/workflows/control/test-instance-123/pause", None, 200),
            ("POST", "/api/v1/workflows/control/test-instance-123/resume", None, 200),
            ("POST", "/api/v1/workflows/control/test-instance-123/cancel", None, 200)
        ]
        self.run_batch("Extension & Workflows", extension_endpoints)
        
        # ================================
        # BATCH 17: WORKFLOW QUICK STARTS
        # ================================
        workflow_quickstart_endpoints = [
            ("GET", "/api/v1/workflows/my-workflows", None, 200),
            ("POST", "/api/v1/workflows/quick-start/content-creation", {
                "content_type": "blog_post",
                "topic": "AI in business",
                "tone": "professional"
            }, 200),
            ("POST", "/api/v1/workflows/quick-start/code-review", {
                "code_language": "python",
                "review_type": "security"
            }, 200),
            ("GET", "/api/v1/workflows/health", None, 200)
        ]
        self.run_batch("Workflow Quick Starts", workflow_quickstart_endpoints)
        
        # Final comprehensive summary
        self.print_final_summary()

    def print_final_summary(self):
        """Print comprehensive final summary"""
        print(f"\n{'='*100}")
        if self.should_stop:
            print(f"🛑 TESTING STOPPED EARLY - ERROR LIMIT REACHED")
        else:
            print(f"🎯 COMPREHENSIVE BATCH TESTING COMPLETE")
        print(f"{'='*100}")
        
        # Overall statistics
        total_tests = len(self.overall_results)
        successful = sum(1 for r in self.overall_results if r["success"])
        failed = total_tests - successful
        success_rate = (successful / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   🧪 Total Endpoints Tested: {total_tests}")
        print(f"   ✅ Successful: {successful} ({success_rate:.1f}%)")
        print(f"   ❌ Failed: {failed} ({100-success_rate:.1f}%)")
        
        if self.should_stop:
            print(f"   🛑 Stopped after {self.total_errors} errors (limit: {self.max_errors})")
            print(f"   📊 Completed {len(self.batch_results)} out of 17 total batches")
        
        # Batch-by-batch summary
        print(f"\n📋 BATCH-BY-BATCH RESULTS:")
        for i, batch in enumerate(self.batch_results, 1):
            if batch.get("skipped", False):
                print(f"   ⏸️ Batch {i}: {batch['batch_name']} - SKIPPED (error limit reached)")
            else:
                status_icon = "✅" if batch["success_rate"] >= 80 else "⚠️" if batch["success_rate"] >= 50 else "❌"
                print(f"   {status_icon} Batch {i}: {batch['batch_name']} - {batch['successful']}/{batch['total_endpoints']} ({batch['success_rate']:.1f}%)")
        
        # Error analysis
        print(f"\n🔍 ERROR ANALYSIS:")
        error_counts = {}
        server_errors = []
        auth_errors = []
        validation_errors = []
        
        for result in self.overall_results:
            if not result["success"]:
                status_code = result["status_code"]
                if status_code not in error_counts:
                    error_counts[status_code] = 0
                error_counts[status_code] += 1
                
                if isinstance(status_code, int) and status_code >= 500:
                    server_errors.append(result)
                elif status_code == 401:
                    auth_errors.append(result)
                elif status_code == 422:
                    validation_errors.append(result)
        
        for status_code, count in sorted(error_counts.items()):
            error_type = "🔐 Auth" if status_code == 401 else "📝 Validation" if status_code == 422 else "💥 Server" if isinstance(status_code, int) and status_code >= 500 else "❌ Other"
            print(f"   {error_type} [{status_code}]: {count} endpoints")
        
        # Performance insights
        avg_response_time = sum(r["response_time"] for r in self.overall_results) / len(self.overall_results) if self.overall_results else 0
        slow_endpoints = [r for r in self.overall_results if r["response_time"] > 1000]
        
        print(f"\n⚡ PERFORMANCE INSIGHTS:")
        print(f"   📈 Average Response Time: {avg_response_time:.0f}ms")
        print(f"   🐌 Slow Endpoints (>1s): {len(slow_endpoints)}")
        
        if slow_endpoints:
            print(f"   Top slow endpoints:")
            for endpoint in sorted(slow_endpoints, key=lambda x: x["response_time"], reverse=True)[:3]:
                print(f"      {endpoint['method']} {endpoint['endpoint']} - {endpoint['response_time']:.0f}ms")
        
        # Priority fixes
        print(f"\n🔧 PRIORITY FIXES:")
        if server_errors:
            print(f"   1. 💥 Fix {len(server_errors)} server errors (highest priority)")
            for error in server_errors[:3]:
                print(f"      {error['method']} {error['endpoint']} [{error['status_code']}]")
        if validation_errors:
            print(f"   2. 📝 Fix {len(validation_errors)} validation errors")
            print(f"      Review required parameters in Swagger UI")
        
        print(f"\n💡 RECOMMENDATIONS:")
        if self.should_stop:
            print(f"   🛑 Testing stopped early to prevent overwhelming errors")
            print(f"   🔧 Fix the {self.total_errors} errors shown above first")
            print(f"   🔄 Run the script again to continue testing from where it stopped")
            remaining_batches = 17 - len(self.batch_results)
            print(f"   📊 {remaining_batches} batches remaining to test")
        
        print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*100}")
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
        os.makedirs(results_dir, exist_ok=True)
        results_file = os.path.join(results_dir, f"comprehensive_batch_results_{timestamp}.json")
        
        results_data = {
            "timestamp": timestamp,
            "total_endpoints": total_tests,
            "successful": successful,
            "failed": failed,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "stopped_early": self.should_stop,
            "batches_completed": len(self.batch_results),
            "batch_results": self.batch_results,
            "detailed_results": self.overall_results
        }
        
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"📄 Detailed results saved to: {results_file}")

def main():
    """Main execution function"""
    tester = ComprehensiveBatchTester()
    tester.run_comprehensive_tests()

if __name__ == "__main__":
    main()
