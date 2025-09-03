"""
🚀 PromptForge.ai COMPREHENSIVE BATCH API Tester
Tests ALL 150+ endpoints in organized batches with smart error handling
Run this to systematically validate the entire API surface
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
        
        # Check if we should stop before starting this batch
        if self.should_stop:
            print(f"🛑 STOPPING: Reached {self.max_errors} errors limit!")
            return False
        return True
    
    def print_endpoint_result(self, method: str, endpoint: str, status_code: int, 
                            response_time: float, success: bool, response_preview: str = ""):
        """Print individual endpoint test result"""
        # Status icon based on result
        if success:
            icon = "✅"
        elif status_code == 401:
            icon = "🔐"
        elif status_code == 403:
            icon = "🚫"
        elif status_code == 422:
            icon = "📝"
        elif status_code >= 500:
            icon = "💥"
        elif status_code == 404:
            icon = "🔍"
        else:
            icon = "❌"
        
        # Format timing
        timing = f"{response_time:.0f}ms" if response_time < 1000 else f"{response_time/1000:.1f}s"
        
        print(f"{icon} {method:<6} {endpoint:<60} [{status_code}] {timing}")
        
        # Show response preview for interesting cases
        if response_preview and len(response_preview) < 100:
            if success:
                print(f"     💚 {response_preview}")
            elif not success and status_code not in [401, 403]:
                print(f"     ❌ {response_preview}")
    
    def test_endpoint_safe(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                          expected_status: int = 200) -> Tuple[bool, int, float, str]:
        """Test endpoint with error handling and timing"""
        start_time = time.time()
        
        try:
            url = f"{self.base_url}{endpoint}"
            
            # Make request based on method
            if method.upper() == "GET":
                response = self.session.get(url, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=10)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, timeout=10)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=10)
            else:
                return False, 0, 0, f"Unsupported method: {method}"
            
            response_time = (time.time() - start_time) * 1000
            
            # Check success
            success = 200 <= response.status_code <= 299
            
            # Get response preview
            response_preview = ""
            try:
                if response.status_code < 400:
                    json_data = response.json()
                    if isinstance(json_data, dict):
                        if "status" in json_data:
                            response_preview = f"Status: {json_data['status']}"
                        elif "message" in json_data:
                            response_preview = json_data["message"][:80]
                        else:
                            preview_keys = list(json_data.keys())[:3]
                            response_preview = f"Keys: {', '.join(preview_keys)}"
                    else:
                        response_preview = str(json_data)[:80]
                else:
                    response_preview = response.text[:80]
            except:
                response_preview = response.text[:80] if hasattr(response, 'text') else "No preview"
            
            return success, response.status_code, response_time, response_preview
            
        except requests.exceptions.Timeout:
            response_time = (time.time() - start_time) * 1000
            return False, 0, response_time, "Request timeout"
        except requests.exceptions.ConnectionError:
            response_time = (time.time() - start_time) * 1000
            return False, 0, response_time, "Connection error"
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return False, 0, response_time, f"Error: {str(e)[:50]}"
    
    def run_batch(self, batch_name: str, endpoints: List[Tuple[str, str, Optional[Dict], int]]) -> Dict:
        """Run a batch of endpoints and return results"""
        # Check if we should stop before starting this batch
        if self.should_stop:
            print(f"⏸️  Skipping batch '{batch_name}' - reached error limit")
            return {
                "batch_number": self.current_batch,
                "batch_name": batch_name,
                "skipped": True,
                "total_endpoints": len(endpoints),
                "successful": 0,
                "failed": 0,
                "results": []
            }
            
        if not self.print_batch_header(self.current_batch, batch_name, len(endpoints)):
            return {
                "batch_number": self.current_batch,
                "batch_name": batch_name,
                "skipped": True,
                "total_endpoints": len(endpoints),
                "successful": 0,
                "failed": 0,
                "results": []
            }
        
        batch_results = {
            "batch_number": self.current_batch,
            "batch_name": batch_name,
            "total_endpoints": len(endpoints),
            "successful": 0,
            "failed": 0,
            "results": [],
            "start_time": datetime.now(),
            "avg_response_time": 0
        }
        
        total_response_time = 0
        
        for i, (method, endpoint, data, expected_status) in enumerate(endpoints, 1):
            success, status_code, response_time, response_preview = self.test_endpoint_safe(
                method, endpoint, data, expected_status
            )
            
            self.print_endpoint_result(method, endpoint, status_code, response_time, success, response_preview)
            
            # Record result
            result = {
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code,
                "response_time": response_time,
                "success": success,
                "response_preview": response_preview
            }
            
            batch_results["results"].append(result)
            self.overall_results.append(result)
            
            if success:
                batch_results["successful"] += 1
            else:
                batch_results["failed"] += 1
                self.total_errors += 1
                
                # Check if we should stop testing
                if self.total_errors >= self.max_errors:
                    self.should_stop = True
                    print(f"\n🛑 STOPPING TESTS - Reached {self.max_errors} errors limit!")
                    print(f"🔧 Fix the current batch of errors and run again to continue")
                    break
            
            total_response_time += response_time
            
            # Small delay between requests to be API-friendly
            time.sleep(0.1)
        
        # Calculate batch statistics
        batch_results["end_time"] = datetime.now()
        batch_results["duration"] = (batch_results["end_time"] - batch_results["start_time"]).total_seconds()
        batch_results["avg_response_time"] = total_response_time / len(endpoints) if endpoints else 0
        batch_results["success_rate"] = (batch_results["successful"] / len(endpoints) * 100) if endpoints else 0
        
        self.print_batch_summary(batch_results)
        self.batch_results.append(batch_results)
        self.current_batch += 1
        
        # Stop early if error limit reached
        if self.should_stop:
            print(f"\n🛑 STOPPING ALL TESTING - Error limit reached!")
            print(f"🔧 Fix the {self.total_errors} errors and run again to continue from batch {self.current_batch}")
        
        return batch_results
    
    def print_batch_summary(self, batch_results: Dict):
        """Print summary for completed batch"""
        print(f"\n{'-'*60}")
        print(f"📊 BATCH {batch_results['batch_number']} SUMMARY: {batch_results['batch_name']}")
        print(f"✅ Successful: {batch_results['successful']}/{batch_results['total_endpoints']} ({batch_results['success_rate']:.1f}%)")
        print(f"❌ Failed: {batch_results['failed']}")
        print(f"⏱️  Avg Response: {batch_results['avg_response_time']:.0f}ms")
        print(f"🕒 Duration: {batch_results['duration']:.1f}s")
        
        # Show critical failures
        critical_failures = [r for r in batch_results["results"] if not r["success"] and r["status_code"] >= 500]
        if critical_failures:
            print(f"💥 Critical Server Errors: {len(critical_failures)}")
            for failure in critical_failures[:3]:
                print(f"   {failure['method']} {failure['endpoint']} [{failure['status_code']}]")
        
        print(f"{'-'*60}")
        
        # Pause for large batches to avoid overwhelming
        if batch_results['total_endpoints'] > 10:
            print("⏸️  Pausing 2 seconds before next batch...")
            time.sleep(2)
    
    def run_all_batches(self):
        """Run comprehensive testing in organized batches"""
        print("🚀 PromptForge.ai COMPREHENSIVE BATCH TESTING")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"📦 Batch Size: {self.batch_size} endpoints per batch")
        print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ================================
        # BATCH 1: HEALTH & FUNDAMENTALS
        # ================================
        health_endpoints = [
            ("GET", "/", None, 200),
            ("GET", "/health", None, 200),
            ("GET", "/api/v1/health", None, 200),
            ("GET", "/api/v1/debug/auth-headers", None, 200),
            ("POST", "/api/v1/debug/test-auth", {"test": True}, 200),
        ]
        self.run_batch("Health & Debug", health_endpoints)
        
        # Check if we should stop after first batch
        if self.should_stop:
            self.print_final_summary()
            return
        
        # ================================
        # BATCH 2: USER AUTHENTICATION & PROFILE
        # ================================
        user_endpoints = [
            ("POST", "/api/v1/users/auth/complete", self.test_data["user_data"], 200),
            ("GET", "/api/v1/users/me", None, 200),
            ("PUT", "/api/v1/users/me/profile", {"first_name": "Updated"}, 200),
            ("GET", "/api/v1/users/credits", None, 200),
            ("GET", "/api/v1/users/preferences", None, 200),
            ("PUT", "/api/v1/users/preferences", {"theme": "dark"}, 200),
            ("GET", "/api/v1/users/stats", None, 200),
            ("GET", "/api/v1/users/me/usage", None, 200),
            ("POST", "/api/v1/users/usage/track", self.test_data["analytics_event"], 200),
            ("GET", "/api/v1/users/export-data", None, 200),
        ]
        self.run_batch("User Management", user_endpoints)
        
        # Check if we should stop
        if self.should_stop:
            self.print_final_summary()
            return
        
        # ================================
        # BATCH 3: CORE PROMPTS FUNCTIONALITY
        # ================================
        prompts_endpoints = [
            ("GET", "/api/v1/prompts/arsenal", None, 200),
            ("POST", "/api/v1/prompts/", self.test_data["prompt_data"], 201),
            ("GET", "/api/v1/prompts/public", None, 200),
            ("POST", "/api/v1/prompts/test-drive-by-id", {
                "prompt_id": "actual-prompt-id-here",
                "inputs": {"type": "professional", "topic": "AI technology"}
            }, 200),
            ("GET", "/api/v1/prompts/test-prompt-123", None, 200),
            ("PUT", "/api/v1/prompts/test-prompt-123", {
                "title": "Updated Batch Test Prompt",
                "body": "You are an expert assistant. Write a {type} email about {topic}.",
                "role": "expert assistant"
            }, 200),
            ("GET", "/api/v1/prompts/test-prompt-123/versions", None, 200),
            ("POST", "/api/v1/prompts/bulk-action", {
                "action": "delete",
                "prompt_ids": ["test-prompt-1", "test-prompt-2"],
                "new_status": "archived"
            }, 200),
        ]
        self.run_batch("Core Prompts", prompts_endpoints)
        
        # ================================
        # BATCH 4: AI FEATURES
        # ================================
        ai_endpoints = [
            ("POST", "/api/v1/ai/remix-prompt", {
                "prompt_body": "Write a professional email about product updates",
                "style": "professional",
                "target_audience": "team members",
                "enhancement_level": "medium"
            }, 200),
            ("POST", "/api/v1/ai/architect-prompt", {
                "description": "Build a REST API for user management",
                "techStack": ["python", "fastapi", "mongodb"],
                "architectureStyle": "microservices"
            }, 200),
            ("POST", "/api/v1/ai/fuse-prompts", {
                "prompt_a": "You are a helpful email assistant",
                "prompt_b": "You are a professional writer"
            }, 200),
            ("POST", "/api/v1/ai/generate-enhanced-prompt", {
                "text": "Help me write emails",
                "mode": "pro",
                "client": "web",
                "intent": "email_writing"
            }, 200),
            ("POST", "/api/v1/ai/analyze-prompt", {
                "code": "Write a professional email",
                "analysisType": "prompt",
                "filename": "test-prompt.txt"
            }, 200),
        ]
        self.run_batch("AI Features", ai_endpoints)
        
        # ================================
        # BATCH 5: MARKETPLACE CORE
        # ================================
        marketplace_endpoints = [
            ("GET", "/api/v1/marketplace/search?q=business", None, 200),
            ("GET", "/api/v1/marketplace/listings", None, 200),
            ("GET", "/api/v1/marketplace/my-listings", None, 200),
            ("POST", "/api/v1/marketplace/list-prompt", self.test_data["marketplace_listing"], 200),
            ("GET", "/api/v1/marketplace/test-123", None, 200),
            ("GET", "/api/v1/marketplace/preview/test-prompt-123", None, 200),  # Fixed: prompt_id format
            ("POST", "/api/v1/marketplace/rate", {
                "prompt_id": "test-123",
                "rating": 5,
                "review_title": "Excellent prompt!",
                "review_content": "Very helpful for testing",
                "pros": ["Easy to use"],
                "cons": [],
                "would_recommend": True
            }, 200),
            ("GET", "/api/v1/marketplace/test-prompt-123/reviews", None, 200),  # Fixed: prompt_id format
            ("GET", "/api/v1/marketplace/test-prompt-123/analytics", None, 200),  # Fixed: prompt_id format
        ]
        self.run_batch("Marketplace Core", marketplace_endpoints)
        
        # ================================
        # BATCH 6: SEARCH & DISCOVERY
        # ================================
        search_endpoints = [
            ("GET", "/api/v1/search/?q=email&type=prompts", None, 200),
            ("GET", "/api/v1/search/users?q=test", None, 200),
        ]
        self.run_batch("Search & Discovery", search_endpoints)
        
        # ================================
        # BATCH 7: PROJECTS & WORKFLOWS CORE
        # ================================
        projects_endpoints = [
            ("GET", "/api/v1/projects/test-project-123", None, 200),
            ("GET", "/api/v1/projects/test-project-123/prompts", None, 200),
            ("POST", "/api/v1/projects/test-project-123/prompts", {"prompt_ids": ["123"], "action": "add"}, 200),
            ("DELETE", "/api/v1/projects/test-project-123", None, 200),
        ]
        self.run_batch("Projects Core", projects_endpoints)
        
        # ================================
        # BATCH 8: SMART WORKFLOWS
        # ================================
        workflows_endpoints = [
            ("GET", "/api/v1/workflows/templates", None, 200),
            ("POST", "/api/v1/workflows/templates", self.test_data["workflow_template"], 201),
            ("GET", "/api/v1/workflows/templates/test-template-123", None, 200),
            ("POST", "/api/v1/workflows/start", {"template_id": "test", "inputs": {}}, 200),
            ("GET", "/api/v1/workflows/status/test-instance-123", None, 200),
            ("GET", "/api/v1/workflows/results/test-instance-123", None, 200),
            ("POST", "/api/v1/workflows/control/test-instance-123/pause", None, 200),
            ("POST", "/api/v1/workflows/control/test-instance-123/resume", None, 200),
            ("POST", "/api/v1/workflows/control/test-instance-123/cancel", None, 200),
            ("GET", "/api/v1/workflows/my-workflows", None, 200),
            ("POST", "/api/v1/workflows/quick-start/content-creation", {"topic": "AI"}, 200),
            ("POST", "/api/v1/workflows/quick-start/code-review", {"code": "def hello():"}, 200),
            ("GET", "/api/v1/workflows/analytics/usage", None, 200),
            ("GET", "/api/v1/workflows/health", None, 200),
        ]
        self.run_batch("Smart Workflows", workflows_endpoints)
        
        # ================================
        # BATCH 9: ANALYTICS CORE
        # ================================
        analytics_endpoints = [
            ("POST", "/api/v1/analytics/events", {
                "events": [{
                    "type": "prompt_created",
                    "data": {"prompt_id": "123", "category": "email"},
                    "timestamp": "2025-09-03T15:30:00Z"
                }],
                "session_id": "session-123"
            }, 200),
            ("POST", "/api/v1/analytics/performance", {"endpoint": "/test", "time": 100}, 200),
            ("GET", "/api/v1/analytics/dashboard", None, 200),
            ("POST", "/api/v1/analytics/exports/prompts", {
                "export_type": "csv",
                "date_range": "30d",
                "format": "csv"
            }, 200),
            ("POST", "/api/v1/analytics/exports/analytics", {
                "export_type": "json",
                "date_range": "30d",
                "format": "json"
            }, 200),
            ("POST", "/api/v1/analytics/jobs/analytics", {
                "job_type": "export_user_data",
                "parameters": {"user_id": "user-123", "date_range": "30d", "format": "csv"},
                "job_name": "User Data Export",
                "priority": 10,
                "notification_email": "user@example.com",
                "retention_days": 7
            }, 200),
            ("GET", "/api/v1/analytics/jobs/analytics/test-job-123/status", None, 200),
        ]
        self.run_batch("Analytics Core", analytics_endpoints)
        
        # ================================
        # BATCH 10: MONITORING & PERFORMANCE
        # ================================
        monitoring_endpoints = [
            ("GET", "/api/v1/monitoring/health", None, 200),
            ("GET", "/api/v1/monitoring/health/detailed", None, 200),
            ("GET", "/api/v1/monitoring/metrics", None, 200),
            ("GET", "/api/v1/monitoring/trace/test-request-123", None, 200),
            ("GET", "/api/v1/monitoring/circuit-breakers", None, 200),
            ("POST", "/api/v1/monitoring/circuit-breakers/test-breaker/reset", None, 200),
            ("GET", "/api/v1/performance/dashboard", None, 200),
            ("GET", "/api/v1/performance/slow-queries", None, 200),
            ("GET", "/api/v1/performance/cache-stats", None, 200),
            ("POST", "/api/v1/performance/optimize", None, 200),
            ("DELETE", "/api/v1/performance/cache", None, 200),
            ("GET", "/api/v1/performance/health", None, 200),
        ]
        self.run_batch("Monitoring & Performance", monitoring_endpoints)
        
        # ================================
        # BATCH 11: INTELLIGENCE FEATURES
        # ================================
        intelligence_endpoints = [
            ("POST", "/api/v1/intelligence/analyze", self.test_data["ai_prompt"], 200),
            ("GET", "/api/v1/intelligence/suggestions/quick?prompt=email", None, 200),
            ("GET", "/api/v1/intelligence/templates/personalized?category=business", None, 200),
            ("GET", "/api/v1/intelligence/patterns/user", None, 200),
            ("POST", "/api/v1/intelligence/feedback", {"suggestion_id": "test", "rating": 5}, 200),
            ("GET", "/api/v1/intelligence/analytics/intelligence", None, 200),
        ]
        self.run_batch("Intelligence Features", intelligence_endpoints)
        
        # ================================
        # BATCH 12: CONTEXT INTELLIGENCE
        # ================================
        context_endpoints = [
            ("POST", "/api/v1/context/analyze", {"prompt_text": "Help with presentation", "context": {}}, 200),
            ("POST", "/api/v1/context/quick-suggestions", {"prompt_text": "Email help", "context": {}}, 200),
            ("POST", "/api/v1/context/follow-up-questions", {"prompt_text": "Marketing strategy", "context": {}}, 200),
            ("GET", "/api/v1/context/enhancement-templates", None, 200),
            ("GET", "/api/v1/context/domain-insights", None, 200),
        ]
        self.run_batch("Context Intelligence", context_endpoints)
        
        # ================================
        # BATCH 13: EXTENSION INTELLIGENCE
        # ================================
        extension_endpoints = [
            ("POST", "/api/v1/extension/analyze-prompt", {"prompt_text": "Code review", "context": {}}, 200),
            ("POST", "/api/v1/extension/suggestions/contextual", {"prompt_text": "Help", "context": {}}, 200),
            ("POST", "/api/v1/extension/enhance/selected-text", {"selected_text": "def hello():", "type": "completion"}, 200),
            ("POST", "/api/v1/extension/templates/smart", {"context": {"language": "python"}}, 200),
            ("GET", "/api/v1/extension/health", None, 200),
            ("GET", "/api/v1/extension/usage-stats", None, 200),
        ]
        self.run_batch("Extension Intelligence", extension_endpoints)
        
        # ================================
        # BATCH 14: ENGINE SERVICES
        # ================================
        engine_endpoints = [
            ("POST", "/api/v1/prompt/quick_upgrade", {"prompt": "Write email", "mode": "quick"}, 200),
            ("POST", "/api/v1/prompt/upgrade", {"prompt": "Write email", "mode": "full"}, 200),
            ("POST", "/api/v1/demon/route", {"query": "improve prompt", "context": {}}, 200),
            ("POST", "/api/v1/demon/v2/upgrade", {"prompt": "Better content", "version": "v2"}, 200),
        ]
        self.run_batch("Engine Services", engine_endpoints)
        
        # ================================
        # BATCH 15: VAULT & IDEAS
        # ================================
        vault_endpoints = [
            ("GET", "/api/v1/vault/arsenal", None, 200),
            ("GET", "/api/v1/vault/search?q=email", None, 200),
            ("POST", "/api/v1/vault/save", {"prompt": "Email helper", "title": "Email Assistant"}, 200),
            ("GET", "/api/v1/vault/list", None, 200),
            ("POST", "/api/v1/vault/test-vault-123/test-drive", {"variables": {"topic": "launch"}}, 200),
            ("GET", "/api/v1/vault/test-vault-123/versions", None, 200),
            ("DELETE", "/api/v1/vault/delete/test-vault-123", None, 200),
            ("POST", "/api/v1/ideas/generate", {"topic": "content marketing", "count": 5}, 200),
        ]
        self.run_batch("Vault & Ideas", vault_endpoints)
        
        # ================================
        # BATCH 16: BUSINESS FEATURES
        # ================================
        business_endpoints = [
            ("POST", "/api/v1/packaging/test-prompt-123/package", {
                "marketplace_ready": True,
                "sales_copy": "Professional email writing made easy",
                "tags": ["email", "business"],
                "price_usd": 9.99,
                "sales_title": "Email Pro Assistant"
            }, 200),
            ("GET", "/api/v1/packaging/debug", None, 200),
            ("GET", "/api/v1/packaging/", None, 200),
            ("POST", "/api/v1/packaging/manage-bulk", {
                "action": "update_price",
                "package_ids": ["package-1", "package-2"],
                "new_price": 15.99,
                "bulk_tags": ["premium", "professional"]
            }, 200),
            ("GET", "/api/v1/packaging/analytics", None, 200),
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
            ("GET", "/api/v1/partnerships/dashboard", None, 200),
        ]
        self.run_batch("Business Features", business_endpoints)
        
        # ================================
        # BATCH 17: BILLING & PAYMENTS
        # ================================
        billing_endpoints = [
            ("GET", "/api/v1/billing/tiers", None, 200),
            ("GET", "/api/v1/billing/me/entitlements", None, 200),
            ("POST", "/api/v1/payments/initiate-payment", {"amount": 9.99, "currency": "USD"}, 200),
            ("GET", "/api/v1/payments/webhooks/health", None, 200),
            ("POST", "/api/v1/payments/webhooks/paddle", {"test": "webhook"}, 200),
            ("POST", "/api/v1/payments/webhooks/razorpay", {"test": "webhook"}, 200),
        ]
        self.run_batch("Billing & Payments", billing_endpoints)
        
        # ================================
        # BATCH 18: CREDITS MANAGEMENT
        # ================================
        credits_endpoints = [
            ("GET", "/api/v1/credits/dashboard", None, 200),
            ("GET", "/api/v1/credits/usage/history", None, 200),
            ("GET", "/api/v1/credits/analytics/routes", None, 200),
            ("GET", "/api/v1/credits/predictions/usage", None, 200),
            ("GET", "/api/v1/credits/admin/overview", None, 200),
        ]
        self.run_batch("Credits Management", credits_endpoints)
        
        # ================================
        # BATCH 19: NOTIFICATIONS
        # ================================
        notifications_endpoints = [
            ("GET", "/api/v1/notifications/preferences", None, 200),
            ("PUT", "/api/v1/notifications/preferences", {"email": True, "push": False}, 200),
            ("GET", "/api/v1/notifications/", None, 200),
            ("POST", "/api/v1/notifications/", self.test_data["notification_data"], 201),
            ("PUT", "/api/v1/notifications/test-notification-123/read", None, 200),
            ("POST", "/api/v1/notifications/mark-all-read", None, 200),
            ("POST", "/api/v1/notifications/bulk", {
                "user_ids": ["user1", "user2", "user3"],
                "title": "System Maintenance",
                "message": "Scheduled maintenance tonight",
                "type": "system",
                "priority": "high"
            }, 200),
            ("DELETE", "/api/v1/notifications/test-notification-123", None, 200),
            ("POST", "/api/v1/notifications/push", {
                "user_id": "target-user-id",
                "title": "New Feature Available",
                "body": "Check out our new AI architect feature",
                "icon": "/icons/feature.png",
                "click_action": "/features/architect"
            }, 200),
            ("GET", "/api/v1/notifications/analytics", None, 200),
        ]
        self.run_batch("Notifications", notifications_endpoints)
        
        # ================================
        # BATCH 20: EMAIL AUTOMATION
        # ================================
        email_endpoints = [
            ("POST", "/api/v1/emails/send-welcome-sequence", {"user_id": "test-123"}, 200),
            ("POST", "/api/v1/emails/send-retention-campaign", {"user_id": "test-123"}, 200),
            ("POST", "/api/v1/emails/send-milestone-celebration", {"user_id": "test-123", "milestone": "first_prompt"}, 200),
            ("GET", "/api/v1/emails/user-preferences", None, 200),
            ("PUT", "/api/v1/emails/user-preferences", {"marketing": True, "product": False}, 200),
            ("POST", "/api/v1/emails/unsubscribe", {"email": "test@test.com", "type": "marketing"}, 200),
            ("GET", "/api/v1/emails/templates", None, 200),
            ("POST", "/api/v1/emails/templates", {"name": "Test Template", "content": "Hello {name}"}, 201),
            ("POST", "/api/v1/emails/automation/trigger-credit-warning", {"user_id": "test-123"}, 200),
            ("POST", "/api/v1/emails/automation/trigger-billing-reminder", {"user_id": "test-123"}, 200),
            ("POST", "/api/v1/emails/automation/trigger-feature-announcement", {"feature": "new_ai"}, 200),
        ]
        self.run_batch("Email Automation", email_endpoints)
        
        # ================================
        # BATCH 21: ADMIN & FALLBACKS
        # ================================
        admin_endpoints = [
            ("GET", "/api/v1/admin/diagnostics", None, 200),
            ("POST", "/analytics/events", self.test_data["analytics_event"], 200),
            ("POST", "//analytics/events", self.test_data["analytics_event"], 200),
        ]
        self.run_batch("Admin & Fallbacks", admin_endpoints)
        
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
            print(f"   📊 Completed {len(self.batch_results)} out of 21 total batches")
        
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
                
                if status_code >= 500:
                    server_errors.append(result)
                elif status_code == 401:
                    auth_errors.append(result)
                elif status_code == 422:
                    validation_errors.append(result)
        
        for status_code, count in sorted(error_counts.items()):
            error_type = "✅ Success" if status_code in [200, 201] else "🔐 Auth" if status_code == 401 else "📝 Validation" if status_code == 422 else "💥 Server" if status_code >= 500 else "❌ Other"
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
            if len(server_errors) > 3:
                print(f"      ... and {len(server_errors) - 3} more")
        
        if validation_errors:
            print(f"   2. 📝 Fix {len(validation_errors)} validation errors")
            print(f"      Review required parameters in Swagger UI")
        
        if auth_errors:
            print(f"   3. 🔐 {len(auth_errors)} endpoints need proper authentication")
            print(f"      Consider using production tokens for auth-required endpoints")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if self.should_stop:
            print(f"   🛑 Testing stopped early to prevent overwhelming errors")
            print(f"   � Fix the {self.total_errors} errors shown above first")
            print(f"   �🔄 Run the script again to continue testing from where it stopped")
            print(f"   📊 {21 - len(self.batch_results)} batches remaining to test")
        else:
            print(f"   🔄 Run critical fixes test: python test_critical_fixes.py")
            print(f"   📚 Document API changes in: API_TEST_RESULTS_SUMMARY.md")
            print(f"   🚀 For production testing, use real auth tokens")
            print(f"   📊 Monitor slow endpoints for performance optimization")
        
        print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*100}")
        
        # Save results to file for analysis
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """Save comprehensive results to JSON file"""
        results_file = f"e:\\GPls\\pfai_backend\\pb\\testing\\results\\comprehensive_batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            "test_run": {
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url,
                "total_batches": len(self.batch_results),
                "total_endpoints": len(self.overall_results)
            },
            "overall_stats": {
                "successful": sum(1 for r in self.overall_results if r["success"]),
                "failed": sum(1 for r in self.overall_results if not r["success"]),
                "success_rate": (sum(1 for r in self.overall_results if r["success"]) / len(self.overall_results) * 100) if self.overall_results else 0,
                "avg_response_time": sum(r["response_time"] for r in self.overall_results) / len(self.overall_results) if self.overall_results else 0
            },
            "batch_results": self.batch_results,
            "all_endpoint_results": self.overall_results
        }
        
        try:
            os.makedirs(os.path.dirname(results_file), exist_ok=True)
            with open(results_file, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            print(f"📄 Detailed results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️  Could not save results file: {e}")

if __name__ == "__main__":
    print("🚀 COMPREHENSIVE BATCH API TESTER")
    print("🎯 Testing ALL PromptForge.ai endpoints in organized batches")
    print("📦 Intelligent batching prevents overwhelming failures")
    print("� Stops after 10 errors to allow focused fixing")
    print("�🔄 Each batch provides immediate feedback for quick fixes")
    print("-" * 80)
    
    # Allow custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    tester = ComprehensiveBatchTester(base_url=base_url, batch_size=15, max_errors=10)
    tester.run_all_batches()
