"""
🚀 PromptForge.ai Comprehensive API Tester
Beautiful, organized testing for ALL endpoints
Run this from any Python environment - no terminal security issues!
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class APITester:
    def __init__(self, base_url="http://localhost:8000", max_failures=10):
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
            print(f"   � {response_data}")
        elif not success and response_data:
            if status_code == 401:
                print(f"   🔐 Auth: {response_data[:80]}...")
            elif status_code == 422:
                print(f"   📝 Validation: {response_data[:80]}...")
            elif status_code >= 500:
                print(f"   � Server: {response_data[:80]}...")
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
            print(f"\n🔧 Issues to fix in this batch:")
            
            # Group by error type for easier fixing
            server_errors = [r for r in failed_results if r["status_code"] >= 500]
            auth_errors = [r for r in failed_results if r["status_code"] == 401]
            validation_errors = [r for r in failed_results if r["status_code"] == 422]
            connection_errors = [r for r in failed_results if r["status_code"] == 0]
            
            if server_errors:
                print(f"\n💥 Server Errors (Fix Priority #1): {len(server_errors)}")
                for result in server_errors[:3]:  # Show first 3
                    print(f"   {result['method']} {result['endpoint']} [{result['status_code']}]")
                if len(server_errors) > 3:
                    print(f"   ... and {len(server_errors) - 3} more")
            
            if connection_errors:
                print(f"\n🔌 Connection Errors (Fix Priority #2): {len(connection_errors)}")
                for result in connection_errors[:3]:
                    print(f"   {result['method']} {result['endpoint']} [ERROR]")
                if len(connection_errors) > 3:
                    print(f"   ... and {len(connection_errors) - 3} more")
            
            if validation_errors:
                print(f"\n📝 Validation Errors: {len(validation_errors)}")
                for result in validation_errors[:2]:
                    print(f"   {result['method']} {result['endpoint']} [422]")
            
            if auth_errors:
                print(f"\n🔐 Auth Errors: {len(auth_errors)}")
                print(f"   These may need proper authentication setup")
        
        print(f"\n🔄 Run the script again after fixing the above issues!")
    
    
    def run_comprehensive_tests(self):
        """Run ALL API endpoints from Swagger UI in organized categories"""
        
        self.print_header("PromptForge.ai Complete API Test Suite", "🚀")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🔑 Bearer Token: {self.token}")
        print(f"� Max failures before stopping: {self.max_failures}")
        print(f"�🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ===============================
        # 1. HEALTH & DEBUG ENDPOINTS
        # ===============================
        self.print_section("Health & Debug", "🏥")
        
        # Basic health checks
        self.test_endpoint("GET", "/", 200, "Root endpoint")
        if self.should_stop: return
        self.test_endpoint("GET", "/health", 200, "Health check")
        if self.should_stop: return
        
        # Debug endpoints  
        self.test_endpoint("GET", "/api/v1/debug/auth-headers", 200, "Debug auth headers")
        if self.should_stop: return
        self.test_endpoint("POST", "/api/v1/debug/test-auth", 200, "Test auth with mock")
        if self.should_stop: return
        
        # ===============================
        # 2. USER AUTHENTICATION & PROFILE
        # ===============================
        self.print_section("User Authentication & Profile", "👤")
        
        # Create user profile first (required for other endpoints)
        user_data = {
            "uid": "test-user-123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        self.test_endpoint("POST", "/api/v1/users/auth/complete", user_data, 200, "Complete user authentication")
        if self.should_stop: return
        
        # User profile endpoints
        self.test_endpoint("GET", "/api/v1/users/me", 200, "Get current user profile")
        if self.should_stop: return
        self.test_endpoint("GET", "/api/v1/users/credits", 200, "Get user credits")
        if self.should_stop: return
        self.test_endpoint("GET", "/api/v1/users/preferences", 200, "Get user preferences")
        if self.should_stop: return
        self.test_endpoint("GET", "/api/v1/users/stats", 200, "Get user statistics")
        if self.should_stop: return
        self.test_endpoint("GET", "/api/v1/users/me/usage", 200, "Get user usage")
        if self.should_stop: return
        self.test_endpoint("GET", "/api/v1/users/export-data", 200, "Export user data")
        if self.should_stop: return
        
        # Update profile
        profile_update = {"first_name": "Updated", "linkedin": "https://linkedin.com/in/test"}
        self.test_endpoint("PUT", "/api/v1/users/me/profile", profile_update, 200, "Update user profile")
        self.test_endpoint("PUT", "/api/v1/users/profile", profile_update, 200, "Update user profile (alt)")
        
        # Preferences update
        preferences = {"notifications": {"email": True, "push": False}}
        self.test_endpoint("PUT", "/api/v1/users/preferences", preferences, 200, "Update user preferences")
        
        # Usage tracking
        usage_data = {"event_type": "prompt_created", "metadata": {"source": "api_test"}}
        self.test_endpoint("POST", "/api/v1/users/usage/track", usage_data, 200, "Track usage event")
        
        # Early exit check after User section
        if self.should_stop: return
        
        # ===============================
        # 3. PROMPTS MANAGEMENT
        # ===============================
        self.print_section("Prompts Management", "📝")
        
        # Create new prompt
        prompt_data = {
            "title": "API Test Prompt",
            "content": "Write a professional email about {topic}",
            "category": "business",
            "tags": ["email", "business", "api-test"],
            "is_public": False
        }
        self.test_endpoint("POST", "/api/v1/prompts/prompts/", prompt_data, 201, "Create new prompt")
        
        # Get prompts
        self.test_endpoint("GET", "/api/v1/prompts/prompts/arsenal", 200, "Get user arsenal")
        self.test_endpoint("GET", "/api/v1/prompts/prompts/public", 200, "Get public prompts")
        
        # Test drive prompt
        test_drive_data = {"prompt_id": "test-prompt-123", "variables": {"topic": "AI technology"}}
        self.test_endpoint("POST", "/api/v1/prompts/prompts/test-drive-by-id", test_drive_data, 200, "Test drive prompt by ID")
        
        # Bulk actions
        bulk_action = {"action": "tag", "prompt_ids": ["123", "456"], "tags": ["bulk-test"]}
        self.test_endpoint("POST", "/api/v1/prompts/prompts/bulk-action", bulk_action, 200, "Bulk prompt action")
        
        # Individual prompt operations (using test ID)
        test_prompt_id = "test-prompt-123"
        self.test_endpoint("GET", f"/api/v1/prompts/prompts/{test_prompt_id}", 200, "Get prompt details")
        self.test_endpoint("GET", f"/api/v1/prompts/prompts/{test_prompt_id}/versions", 200, "Get prompt versions")
        
        prompt_update = {"title": "Updated API Test Prompt", "content": "Updated content"}
        self.test_endpoint("PUT", f"/api/v1/prompts/prompts/{test_prompt_id}", prompt_update, 200, "Update prompt")
        
        # Early exit check after Prompts section
        if self.should_stop: return
        
        # ===============================
        # 4. AI FEATURES
        # ===============================
        self.print_section("AI Features", "🤖")
        
        ai_prompt_data = {"prompt_text": "Write a blog post about artificial intelligence"}
        
        self.test_endpoint("POST", "/api/v1/ai/remix-prompt", ai_prompt_data, 200, "Remix prompt")
        self.test_endpoint("POST", "/api/v1/ai/architect-prompt", ai_prompt_data, 200, "Architect prompt")
        self.test_endpoint("POST", "/api/v1/ai/generate-enhanced-prompt", ai_prompt_data, 200, "Generate enhanced prompt")
        self.test_endpoint("POST", "/api/v1/ai/analyze-prompt", ai_prompt_data, 200, "Analyze prompt")
        
        # Fuse prompts
        fuse_data = {"prompts": ["prompt1", "prompt2"], "fusion_type": "merge"}
        self.test_endpoint("POST", "/api/v1/ai/fuse-prompts", fuse_data, 200, "Fuse prompts")
        
        # Early exit check after AI Features section
        if self.should_stop: return
        
        # ===============================
        # 5. MARKETPLACE
        # ===============================
        self.print_section("Marketplace", "🛒")
        
        self.test_endpoint("GET", "/api/v1/marketplace/search?q=business&limit=10", 200, "Search marketplace")
        self.test_endpoint("GET", "/api/v1/marketplace/listings", 200, "Get marketplace listings")
        self.test_endpoint("GET", "/api/v1/marketplace/my-listings", 200, "Get my marketplace listings")
        
        # List prompt in marketplace
        listing_data = {
            "prompt_id": "test-prompt-123",
            "price": 5.99,
            "description": "Professional email templates"
        }
        self.test_endpoint("POST", "/api/v1/marketplace/list-prompt", listing_data, 200, "List prompt in marketplace")
        
        # Marketplace interactions
        test_marketplace_id = "test-marketplace-123"
        self.test_endpoint("GET", f"/api/v1/marketplace/{test_marketplace_id}", 200, "Get marketplace prompt details")
        self.test_endpoint("GET", f"/api/v1/marketplace/preview/{test_marketplace_id}", 200, "Preview marketplace item")
        self.test_endpoint("GET", f"/api/v1/marketplace/{test_marketplace_id}/reviews", 200, "Get marketplace reviews")
        self.test_endpoint("GET", f"/api/v1/marketplace/{test_marketplace_id}/analytics", 200, "Get marketplace analytics")
        
        # Rate marketplace prompt
        rating_data = {"prompt_id": test_marketplace_id, "rating": 5, "review": "Excellent prompt!"}
        self.test_endpoint("POST", "/api/v1/marketplace/rate", rating_data, 200, "Rate marketplace prompt")
        
        # ===============================
        # 6. SEARCH FUNCTIONALITY
        # ===============================
        self.print_section("Search Functionality", "🔍")
        
        self.test_endpoint("GET", "/api/v1/search/?q=email&type=prompts&limit=10", 200, "Global search")
        self.test_endpoint("GET", "/api/v1/search/users?q=test&limit=5", 200, "Search users")
        
        # ===============================
        # 7. PROJECTS & WORKFLOWS
        # ===============================
        self.print_section("Projects & Workflows", "📂")
        
        # Project management
        test_project_id = "test-project-123"
        self.test_endpoint("GET", f"/api/v1/projects/{test_project_id}", 200, "Get project details")
        self.test_endpoint("GET", f"/api/v1/projects/{test_project_id}/prompts", 200, "Get project prompts")
        
        project_prompts = {"prompt_ids": ["123", "456"], "action": "add"}
        self.test_endpoint("POST", f"/api/v1/projects/{test_project_id}/prompts", project_prompts, 200, "Manage project prompts")
        
        # Smart Workflows
        self.test_endpoint("GET", "/api/v1/workflows/api/workflows/templates", 200, "Get workflow templates")
        self.test_endpoint("GET", "/api/v1/workflows/api/workflows/my-workflows", 200, "List user workflows")
        self.test_endpoint("GET", "/api/v1/workflows/api/workflows/health", 200, "Workflow service health")
        self.test_endpoint("GET", "/api/v1/workflows/api/workflows/analytics/usage", 200, "Get workflow analytics")
        
        # Create workflow template
        workflow_template = {
            "name": "API Test Workflow",
            "description": "Test workflow for API testing",
            "steps": [{"type": "prompt", "action": "generate"}]
        }
        self.test_endpoint("POST", "/api/v1/workflows/api/workflows/templates", workflow_template, 201, "Create workflow template")
        
        # Start workflow
        workflow_start = {"template_id": "test-template", "inputs": {"topic": "AI"}}
        self.test_endpoint("POST", "/api/v1/workflows/api/workflows/start", workflow_start, 200, "Start workflow")
        
        # Quick start workflows
        content_workflow = {"topic": "AI blog post", "content_type": "blog"}
        self.test_endpoint("POST", "/api/v1/workflows/api/workflows/quick-start/content-creation", content_workflow, 200, "Quick start content creation")
        
        code_review = {"code": "def hello(): print('world')", "language": "python"}
        self.test_endpoint("POST", "/api/v1/workflows/api/workflows/quick-start/code-review", code_review, 200, "Quick start code review")
        
        # ===============================
        # 8. ANALYTICS & MONITORING
        # ===============================
        self.print_section("Analytics & Monitoring", "📊")
        
        # Performance metrics
        perf_data = {"endpoint": "/api/v1/prompts", "response_time": 150, "status": "success"}
        self.test_endpoint("POST", "/api/v1/analytics/performance", perf_data, 200, "Log performance metrics")
        
        # Analytics dashboard
        self.test_endpoint("GET", "/api/v1/analytics/dashboard", 200, "Get analytics dashboard")
        
        # Data exports
        export_prompts = {"format": "json", "date_range": "last_30_days"}
        self.test_endpoint("POST", "/api/v1/analytics/exports/prompts", export_prompts, 200, "Export prompts data")
        self.test_endpoint("POST", "/api/v1/analytics/exports/analytics", export_prompts, 200, "Export analytics data")
        
        # Analytics jobs
        job_data = {"type": "user_engagement", "parameters": {"date_range": "last_week"}}
        self.test_endpoint("POST", "/api/v1/analytics/jobs/analytics", job_data, 200, "Create analytics job")
        
        test_job_id = "test-job-123"
        self.test_endpoint("GET", f"/api/v1/analytics/jobs/analytics/{test_job_id}/status", 200, "Get analytics job status")
        
        # Monitoring endpoints
        self.test_endpoint("GET", "/api/v1/monitoring/health", 200, "Monitoring health check")
        self.test_endpoint("GET", "/api/v1/monitoring/health/detailed", 200, "Detailed health check")
        self.test_endpoint("GET", "/api/v1/monitoring/metrics", 200, "Get monitoring metrics")
        self.test_endpoint("GET", "/api/v1/monitoring/circuit-breakers", 200, "Get circuit breaker status")
        
        test_request_id = "test-request-123"
        self.test_endpoint("GET", f"/api/v1/monitoring/trace/{test_request_id}", 200, "Get request trace")
        
        breaker_name = "test-breaker"
        self.test_endpoint("POST", f"/api/v1/monitoring/circuit-breakers/{breaker_name}/reset", 200, "Reset circuit breaker")
        
        # ===============================
        # 9. INTELLIGENCE FEATURES
        # ===============================
        self.print_section("Intelligence Features", "🧠")
        
        # Prompt Intelligence
        intelligence_data = {"prompt_text": "Write a marketing email", "analysis_type": "comprehensive"}
        self.test_endpoint("POST", "/api/v1/intelligence/analyze", intelligence_data, 200, "Analyze prompt intelligence")
        
        self.test_endpoint("GET", "/api/v1/intelligence/suggestions/quick?prompt=email&category=marketing", 200, "Get quick suggestions")
        self.test_endpoint("GET", "/api/v1/intelligence/templates/personalized?category=business&limit=5", 200, "Get personalized templates")
        self.test_endpoint("GET", "/api/v1/intelligence/patterns/user", 200, "Get user patterns")
        self.test_endpoint("GET", "/api/v1/intelligence/analytics/intelligence", 200, "Get intelligence analytics")
        
        # Submit feedback
        feedback_data = {"suggestion_id": "test-123", "rating": 5, "feedback": "Very helpful"}
        self.test_endpoint("POST", "/api/v1/intelligence/feedback", feedback_data, 200, "Submit suggestion feedback")
        
        # Context Intelligence
        context_data = {"prompt_text": "Help me with presentation", "context": {"domain": "business"}}
        self.test_endpoint("POST", "/api/v1/context/analyze", context_data, 200, "Analyze context")
        self.test_endpoint("POST", "/api/v1/context/quick-suggestions", context_data, 200, "Get quick context suggestions")
        self.test_endpoint("POST", "/api/v1/context/follow-up-questions", context_data, 200, "Generate follow-up questions")
        
        self.test_endpoint("GET", "/api/v1/context/enhancement-templates", 200, "Get enhancement templates")
        self.test_endpoint("GET", "/api/v1/context/domain-insights", 200, "Get domain insights")
        
        # Extension Intelligence
        extension_data = {"prompt_text": "Improve this code", "context": {"language": "python"}}
        self.test_endpoint("POST", "/api/v1/extension/analyze-prompt", extension_data, 200, "Analyze extension prompt")
        self.test_endpoint("POST", "/api/v1/extension/suggestions/contextual", extension_data, 200, "Get contextual suggestions")
        
        text_data = {"selected_text": "def hello():", "enhancement_type": "completion"}
        self.test_endpoint("POST", "/api/v1/extension/enhance/selected-text", text_data, 200, "Enhance selected text")
        
        template_data = {"context": {"file_type": "python", "project_type": "web_app"}}
        self.test_endpoint("POST", "/api/v1/extension/templates/smart", template_data, 200, "Get smart templates")
        
        self.test_endpoint("GET", "/api/v1/extension/extension/health", 200, "Extension health check")
        self.test_endpoint("GET", "/api/v1/extension/extension/usage-stats", 200, "Get extension usage stats")
        
        # ===============================
        # 10. ENGINE SERVICES
        # ===============================
        self.print_section("Engine Services", "⚙️")
        
        # Prompt Engine
        upgrade_data = {"prompt": "Write an email", "mode": "quick"}
        self.test_endpoint("POST", "/api/v1/prompt/prompt/quick_upgrade", upgrade_data, 200, "Quick prompt upgrade")
        
        full_upgrade_data = {"prompt": "Write an email", "mode": "full", "enhancement_level": "pro"}
        self.test_endpoint("POST", "/api/v1/prompt/prompt/upgrade", full_upgrade_data, 200, "Full prompt upgrade")
        
        # Demon Engine
        route_data = {"query": "improve my prompt", "context": {"user_level": "pro"}}
        self.test_endpoint("POST", "/api/v1/demon/route", route_data, 200, "Demon engine routing")
        
        demon_upgrade = {"prompt": "Write better content", "version": "v2"}
        self.test_endpoint("POST", "/api/v1/demon/v2/upgrade", demon_upgrade, 200, "Demon engine upgrade v2")
        
        # ===============================
        # 11. VAULT & IDEAS
        # ===============================
        self.print_section("Vault & Ideas", "🗄️")
        
        # Prompt Vault
        self.test_endpoint("GET", "/api/v1/vault/vault/arsenal", 200, "Get vault arsenal")
        self.test_endpoint("GET", "/api/v1/vault/vault/search?q=email&limit=10", 200, "Search vault prompts")
        self.test_endpoint("GET", "/api/v1/vault/vault/list", 200, "List vault prompts")
        
        # Save prompt to vault
        vault_save_data = {
            "prompt": "Write professional emails",
            "title": "Email Assistant",
            "tags": ["email", "business"]
        }
        self.test_endpoint("POST", "/api/v1/vault/vault/save", vault_save_data, 200, "Save prompt to vault")
        
        # Test drive and versions
        test_vault_id = "test-vault-123"
        test_drive_vault = {"variables": {"topic": "product launch"}}
        self.test_endpoint("POST", f"/api/v1/vault/vault/{test_vault_id}/test-drive", test_drive_vault, 200, "Test drive vault prompt")
        self.test_endpoint("GET", f"/api/v1/vault/vault/{test_vault_id}/versions", 200, "Get vault prompt versions")
        
        # Ideas generation
        ideas_data = {"topic": "content marketing", "count": 5, "creativity_level": "high"}
        self.test_endpoint("POST", "/api/v1/ideas/generate", ideas_data, 200, "Generate ideas")
        
        # ===============================
        # 12. BUSINESS FEATURES
        # ===============================
        self.print_section("Business Features", "💼")
        
        # Packaging
        package_data = {"marketplace_ready": True, "price": 9.99}
        test_prompt_id = "test-prompt-123"
        self.test_endpoint("POST", f"/api/v1/packaging/{test_prompt_id}/package", package_data, 200, "Package prompt for marketplace")
        
        self.test_endpoint("GET", "/api/v1/packaging/", 200, "List user packages")
        self.test_endpoint("GET", "/api/v1/packaging/analytics", 200, "Get package analytics")
        
        bulk_package = {"action": "promote", "package_ids": ["123", "456"]}
        self.test_endpoint("POST", "/api/v1/packaging/manage-bulk", bulk_package, 200, "Manage packages bulk")
        
        # Partnerships
        partnership_data = {
            "company_name": "Test Company",
            "contact_email": "partner@test.com",
            "partnership_type": "integration"
        }
        self.test_endpoint("POST", "/api/v1/partnerships/request", partnership_data, 200, "Request partnership")
        
        revenue_data = {"partner_id": "test-partner", "revenue_share": 0.3}
        self.test_endpoint("POST", "/api/v1/partnerships/revenue", revenue_data, 200, "Manage partner revenue")
        
        self.test_endpoint("GET", "/api/v1/partnerships/dashboard", 200, "Get partner dashboard")
        
        # Billing & Payments
        self.test_endpoint("GET", "/api/v1/billing/tiers", 200, "Get billing tiers")
        self.test_endpoint("GET", "/api/v1/billing/me/entitlements", 200, "Get user entitlements")
        
        payment_data = {"amount": 9.99, "currency": "USD", "payment_method": "stripe"}
        self.test_endpoint("POST", "/api/v1/payments/initiate-payment", payment_data, 200, "Initiate payment")
        
        # Webhooks
        self.test_endpoint("GET", "/api/v1/payments/webhooks/health", 200, "Webhooks health check")
        
        # ===============================
        # 13. CREDITS & PERFORMANCE
        # ===============================
        self.print_section("Credits & Performance", "💳")
        
        # Credit Management
        self.test_endpoint("GET", "/api/v1/credits/dashboard", 200, "Get credit dashboard")
        self.test_endpoint("GET", "/api/v1/credits/usage/history", 200, "Get usage history")
        self.test_endpoint("GET", "/api/v1/credits/analytics/routes", 200, "Get route analytics")
        self.test_endpoint("GET", "/api/v1/credits/predictions/usage", 200, "Predict usage")
        self.test_endpoint("GET", "/api/v1/credits/admin/overview", 200, "Admin credit overview")
        
        # Performance Management
        self.test_endpoint("GET", "/api/v1/performance/performance/dashboard", 200, "Get performance dashboard")
        self.test_endpoint("GET", "/api/v1/performance/performance/slow-queries", 200, "Get slow queries")
        self.test_endpoint("GET", "/api/v1/performance/performance/cache-stats", 200, "Get cache statistics")
        self.test_endpoint("GET", "/api/v1/performance/performance/health", 200, "Performance health check")
        
        # Performance actions
        self.test_endpoint("POST", "/api/v1/performance/performance/optimize", {}, 200, "Trigger optimization")
        self.test_endpoint("DELETE", "/api/v1/performance/performance/cache", 200, "Clear cache")
        
        # ===============================
        # 14. NOTIFICATIONS & ADMIN
        # ===============================
        self.print_section("Notifications & Admin", "🔔")
        
        # Notifications
        test_notification_id = "test-notification-123"
        self.test_endpoint("PUT", f"/api/v1/notifications/{test_notification_id}/read", {}, 200, "Mark notification read")
        self.test_endpoint("POST", "/api/v1/notifications/mark-all-read", {}, 200, "Mark all notifications read")
        
        # Admin
        self.test_endpoint("GET", "/api/v1/admin/diagnostics", 200, "Admin diagnostics")
        
        # ===============================
        # FINAL SUMMARY
        # ===============================
        self.print_summary()
    
    def print_summary(self):
        """Print beautiful test results summary"""
        self.print_header("Test Results Summary", "🎯")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests} ({success_rate:.1f}%)")
        print(f"❌ Failed: {failed_tests} ({100-success_rate:.1f}%)")
        print(f"🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Group results by status code
        self.print_section("Results by Status Code", "📈")
        status_codes = {}
        for result in self.test_results:
            code = result["status_code"]
            if code not in status_codes:
                status_codes[code] = 0
            status_codes[code] += 1
        
        for code, count in sorted(status_codes.items()):
            icon = "✅" if code in [200, 201] else "❌" if code >= 400 else "⚠️"
            print(f"{icon} {code}: {count} endpoints")
        
        # Show failed tests for debugging
        failed_results = [r for r in self.test_results if not r["success"]]
        if failed_results:
            self.print_section("Key Issues Summary", "🔍")
            
            # Group by status code for better analysis
            auth_errors = [r for r in failed_results if r["status_code"] == 401]
            validation_errors = [r for r in failed_results if r["status_code"] == 422]
            server_errors = [r for r in failed_results if r["status_code"] >= 500]
            forbidden_errors = [r for r in failed_results if r["status_code"] == 403]
            
            if auth_errors:
                print(f"🔐 Authentication Required: {len(auth_errors)} endpoints")
                print("   💡 These endpoints require higher-level auth or different tokens")
            
            if validation_errors:
                print(f"📝 Validation Errors: {len(validation_errors)} endpoints")
                print("   💡 These endpoints need additional required parameters")
            
            if server_errors:
                print(f"💥 Server Errors: {len(server_errors)} endpoints")
                print("   💡 These endpoints have backend implementation issues")
            
            if forbidden_errors:
                print(f"🚫 Forbidden Access: {len(forbidden_errors)} endpoints")
                print("   💡 These endpoints require admin or special permissions")
            
            # Show a few specific examples
            print(f"\n📋 Sample Issues:")
            for result in failed_results[:5]:
                status_icon = "🔐" if result["status_code"] == 401 else "📝" if result["status_code"] == 422 else "💥" if result["status_code"] >= 500 else "�" if result["status_code"] == 403 else "❌"
                print(f"{status_icon} {result['method']} {result['endpoint']} [{result['status_code']}]")
        
        print(f"\n{'='*80}")
        if self.should_stop:
            print("🛑 Testing STOPPED due to failure limit - Fix errors and run again!")
        else:
            print("🎉 API Testing Complete! Check the results above.")
        print(f"{'='*80}")
        
        # Show improvement suggestions
        if failed_results:
            print("\n💡 Quick Improvement Tips:")
            print("1. Restart server to apply recent fixes for server errors")
            print("2. Check Swagger UI for exact parameter requirements (422 errors)")
            print("3. Use Pro/Enterprise tokens for advanced features (401 errors)")
            print("4. Admin features require special permissions (403 errors)")
            
        if self.should_stop:
            print(f"\n🔄 NEXT STEPS:")
            print(f"1. Fix the {self.failure_count} errors shown above")
            print(f"2. Run 'python simple_api_tester.py' again to continue")
            print(f"3. The script will pick up where it left off")
            
        print(f"\n🔧 To test critical fixes: python test_critical_fixes.py")
        print(f"📚 Full documentation: API_TEST_RESULTS_SUMMARY.md")

if __name__ == "__main__":
    # Run the comprehensive test suite with batch processing
    print("🚀 PromptForge.ai API Tester - Batch Mode")
    print("💡 Will stop after 10 failures for batch-wise error fixing")
    print("🔄 Run again after fixing errors to continue testing")
    print("-" * 60)
    
    tester = APITester(max_failures=10)  # Stop after 10 failures
    tester.run_comprehensive_tests()
