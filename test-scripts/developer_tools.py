#!/usr/bin/env python3
"""
⚒️ DEVELOPER TOOLS - EXTENSION & DEVELOPER FEATURES TEST SUITE
Tests VSCode extension, Chrome extension, workflows, and developer-focused features
Validates extension intelligence, context analysis, and development workflow integration
Part of the Demon Engine Testing Framework
"""

import requests
import json
import time
import os
import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re

class DeveloperToolsTester:
    def __init__(self, base_url: str = "http://localhost:8000", debug_level: int = 3):
        """
        Initialize the Developer Tools Test Suite
        
        Args:
            base_url: API base URL
            debug_level: 1=minimal, 2=standard, 3=detailed, 4=forensic
        """
        self.base_url = base_url
        self.debug_level = debug_level
        self.session = requests.Session()
        self.test_results = []
        self.extension_logs = []
        self.workflow_executions = []
        
        # Test data setup
        self.test_uid = f"test-dev-tools-{uuid.uuid4().hex[:8]}"
        self.test_workspace_context = self.setup_workspace_context()
        self.test_code_samples = self.setup_code_samples()
        self.test_workflow_templates = self.setup_workflow_templates()
        
        # Setup environment
        self.setup_debug_environment()
        
    def setup_debug_environment(self):
        """Enable comprehensive debugging for developer tools"""
        # Backend debug flags
        os.environ['DEBUG_EXTENSIONS'] = '1'
        os.environ['DEBUG_WORKFLOWS'] = '1'
        os.environ['DEBUG_CONTEXT_ANALYSIS'] = '1'
        os.environ['DEBUG_INTELLIGENCE'] = '1'
        os.environ['DEBUG_TEMPLATES'] = '1'
        
        # Session headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'PromptForge-DevToolsTest/1.0',
            'X-Test-Mode': 'developer_tools',
            'X-Client': 'test_suite',
            'Authorization': f'Bearer mock-dev-token-{self.test_uid}'
        })
        
    def setup_workspace_context(self) -> Dict:
        """Setup realistic development workspace context"""
        return {
            "project_type": "web_application",
            "language": "typescript",
            "framework": "react",
            "tools": ["vscode", "git", "npm", "webpack"],
            "files": [
                {
                    "path": "src/components/UserProfile.tsx",
                    "type": "component",
                    "language": "typescript",
                    "content": "import React from 'react';\n\ninterface UserProfileProps {\n  userId: string;\n  onUpdate: () => void;\n}\n\nexport const UserProfile: React.FC<UserProfileProps> = ({ userId, onUpdate }) => {\n  return <div>User Profile Component</div>;\n};"
                },
                {
                    "path": "src/api/userService.ts",
                    "type": "service",
                    "language": "typescript", 
                    "content": "export class UserService {\n  async getUserById(id: string) {\n    const response = await fetch(`/api/users/${id}`);\n    return response.json();\n  }\n}"
                },
                {
                    "path": "README.md",
                    "type": "documentation",
                    "language": "markdown",
                    "content": "# User Management System\n\nA React TypeScript application for managing user profiles.\n\n## Features\n- User profile management\n- Authentication\n- Real-time updates"
                }
            ],
            "current_file": "src/components/UserProfile.tsx",
            "cursor_position": {"line": 8, "column": 35},
            "selected_text": "User Profile Component"
        }
        
    def setup_code_samples(self) -> List[Dict]:
        """Setup test code samples for analysis"""
        return [
            {
                "name": "react_component",
                "language": "typescript",
                "content": """
import React, { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  
  useEffect(() => {
    fetchUsers();
  }, []);
  
  const fetchUsers = async () => {
    // TODO: Implement user fetching
  };
  
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
};

export default UserList;
                """,
                "context": "React component needs API integration and error handling"
            },
            {
                "name": "python_function",
                "language": "python",
                "content": """
def calculate_user_score(user_data):
    # Basic score calculation
    score = 0
    if user_data.get('profile_complete'):
        score += 20
    if user_data.get('email_verified'):
        score += 15
    # Need to add more scoring logic
    return score
                """,
                "context": "Python function needs optimization and additional scoring criteria"
            },
            {
                "name": "sql_query",
                "language": "sql",
                "content": """
SELECT u.id, u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
-- Need to optimize this query for large datasets
                """,
                "context": "SQL query optimization needed for performance"
            }
        ]
        
    def setup_workflow_templates(self) -> List[Dict]:
        """Setup test workflow templates"""
        return [
            {
                "name": "Code Review Workflow",
                "description": "Automated code review and improvement suggestions",
                "steps": [
                    {"type": "analyze", "action": "code_analysis"},
                    {"type": "review", "action": "security_check"},
                    {"type": "suggest", "action": "improvements"},
                    {"type": "format", "action": "code_formatting"}
                ],
                "triggers": ["pull_request", "commit"],
                "language": "any"
            },
            {
                "name": "Documentation Generation",
                "description": "Generate comprehensive documentation from code",
                "steps": [
                    {"type": "scan", "action": "extract_functions"},
                    {"type": "analyze", "action": "understand_purpose"},
                    {"type": "generate", "action": "create_docs"},
                    {"type": "format", "action": "markdown_output"}
                ],
                "triggers": ["manual", "ci_cd"],
                "language": "typescript"
            },
            {
                "name": "API Testing Suite",
                "description": "Comprehensive API endpoint testing",
                "steps": [
                    {"type": "discover", "action": "find_endpoints"},
                    {"type": "generate", "action": "create_tests"},
                    {"type": "execute", "action": "run_tests"},
                    {"type": "report", "action": "generate_report"}
                ],
                "triggers": ["api_change", "deployment"],
                "language": "any"
            }
        ]
        
    def log_debug(self, message: str, level: int = 3, data: Any = None):
        """Structured debug logging"""
        if level <= self.debug_level:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] {message}")
            if data and self.debug_level >= 4:
                print(f"    ⚒️ Data: {json.dumps(data, indent=2, default=str)}")
                
    def log_extension_activity(self, activity_type: str, details: Dict):
        """Log extension activity for analysis"""
        activity = {
            "id": f"ext_{uuid.uuid4().hex[:12]}",
            "type": activity_type,
            "timestamp": datetime.now().isoformat(),
            "user_id": self.test_uid,
            "details": details,
            "test_mode": True
        }
        
        self.extension_logs.append(activity)
        
        if self.debug_level >= 3:
            self.log_debug(f"📝 Extension activity: {activity_type}", level=3, data=activity)
            
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     expected_status: int = 200, description: str = "") -> Dict:
        """Execute API test with developer tools specific logging"""
        test_start = time.time()
        
        try:
            url = f"{self.base_url}{endpoint}"
            self.log_debug(f"⚒️ {method} {endpoint} - {description}", level=2)
            
            if self.debug_level >= 4:
                self.log_debug(f"📤 Request data:", level=4, data=data)
                
            # Execute request
            if method.upper() == "GET":
                response = self.session.get(url, params=data)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
                
            # Process response
            response_time = (time.time() - test_start) * 1000
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
                
            success = response.status_code == expected_status
            status_icon = "✅" if success else "❌"
            
            self.log_debug(
                f"{status_icon} {method} {endpoint} [{response.status_code}] - {response_time:.0f}ms",
                level=2
            )
            
            # Log extension activity if relevant
            if any(keyword in endpoint.lower() for keyword in ['extension', 'context', 'template', 'workflow']):
                self.log_extension_activity(f"{method.lower()}_{endpoint.split('/')[-1]}", {
                    "endpoint": endpoint,
                    "request_data": data,
                    "response_code": response.status_code,
                    "response_data": response_data,
                    "success": success
                })
                
            result = {
                "test_id": f"devtools_{len(self.test_results)+1:03d}",
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response_time_ms": int(response_time),
                "response_data": response_data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            self.log_debug(f"💥 Request failed: {str(e)}", level=1)
            result = {
                "test_id": f"devtools_{len(self.test_results)+1:03d}",
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": 0,
                "expected_status": expected_status,
                "success": False,
                "response_time_ms": int((time.time() - test_start) * 1000),
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            self.test_results.append(result)
            return result
            
    def print_section_header(self, title: str, emoji: str = "📋"):
        """Print beautiful section headers"""
        print(f"\n{'='*80}")
        print(f"{emoji} {title}")
        print(f"{'='*80}")
        
    async def run_extension_intelligence_tests(self):
        """Test extension intelligence and analysis features"""
        self.print_section_header("EXTENSION INTELLIGENCE", "🧠")
        
        # 1. Extension health check
        self.test_endpoint(
            "GET",
            "/api/v1/extension/extension/health",
            None,
            200,
            "Extension health check"
        )
        
        # 2. Get extension usage stats
        self.test_endpoint(
            "GET",
            "/api/v1/extension/extension/usage-stats",
            None,
            200,
            "Get extension usage statistics"
        )
        
        # 3. Analyze prompt with context
        code_sample = self.test_code_samples[0]
        analysis_data = {
            "prompt": f"Improve this React component: {code_sample['content']}",
            "context": {
                "language": code_sample["language"],
                "framework": "react",
                "file_type": "component",
                "project_context": self.test_workspace_context
            },
            "analysis_type": "comprehensive"
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/extension/analyze-prompt",
            analysis_data,
            200,
            "Analyze prompt with workspace context"
        )
        
        # 4. Get contextual suggestions
        contextual_data = {
            "current_code": code_sample["content"],
            "language": code_sample["language"],
            "context": code_sample["context"],
            "suggestion_type": "improvement"
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/extension/suggestions/contextual",
            contextual_data,
            200,
            "Get contextual suggestions for code"
        )
        
        # 5. Enhance selected text
        enhancement_data = {
            "selected_text": self.test_workspace_context["selected_text"],
            "context": {
                "file_path": self.test_workspace_context["current_file"],
                "language": self.test_workspace_context["language"],
                "surrounding_code": code_sample["content"]
            },
            "enhancement_type": "clarity"
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/extension/enhance/selected-text",
            enhancement_data,
            200,
            "Enhance selected text with context"
        )
        
        # 6. Get smart templates
        template_data = {
            "context": {
                "language": "typescript",
                "framework": "react",
                "component_type": "functional"
            },
            "template_type": "component",
            "customization": {
                "style": "hooks",
                "typescript": True
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/extension/templates/smart",
            template_data,
            200,
            "Get smart templates based on context"
        )
        
    async def run_context_intelligence_tests(self):
        """Test context analysis and intelligence features"""
        self.print_section_header("CONTEXT INTELLIGENCE", "🔍")
        
        # 1. Analyze context
        context_analysis_data = {
            "text": self.test_code_samples[0]["content"],
            "context_type": "code",
            "metadata": {
                "language": "typescript",
                "file_type": "component",
                "project_info": self.test_workspace_context
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/context/analyze",
            context_analysis_data,
            200,
            "Analyze code context for understanding"
        )
        
        # 2. Get quick context suggestions
        quick_suggestions_data = {
            "input_text": "I need to add error handling to my API calls",
            "context": {
                "current_file": self.test_workspace_context["current_file"],
                "project_type": self.test_workspace_context["project_type"],
                "language": self.test_workspace_context["language"]
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/context/quick-suggestions",
            quick_suggestions_data,
            200,
            "Get quick context-aware suggestions"
        )
        
        # 3. Generate follow-up questions
        followup_data = {
            "original_prompt": "Create a user authentication system",
            "context": {
                "domain": "web_development",
                "technology_stack": ["react", "node.js", "mongodb"],
                "complexity_level": "intermediate"
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/context/follow-up-questions",
            followup_data,
            200,
            "Generate contextual follow-up questions"
        )
        
        # 4. Get enhancement templates
        self.test_endpoint(
            "GET",
            "/api/v1/context/enhancement-templates",
            {"domain": "software_development", "language": "typescript"},
            200,
            "Get context-specific enhancement templates"
        )
        
        # 5. Get domain insights
        self.test_endpoint(
            "GET",
            "/api/v1/context/domain-insights",
            {"domain": "react_development", "experience_level": "intermediate"},
            200,
            "Get domain-specific development insights"
        )
        
    async def run_prompt_intelligence_tests(self):
        """Test prompt intelligence and optimization"""
        self.print_section_header("PROMPT INTELLIGENCE", "🎯")
        
        # 1. Analyze prompt
        prompt_analysis_data = {
            "prompt_body": "Create a function that validates email addresses and phone numbers",
            "analysis_depth": "comprehensive",
            "context": {
                "domain": "validation",
                "language": "javascript"
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/intelligence/analyze",
            prompt_analysis_data,
            200,
            "Analyze prompt for optimization opportunities"
        )
        
        # 2. Get quick suggestions
        self.test_endpoint(
            "GET",
            "/api/v1/intelligence/suggestions/quick",
            {"prompt_type": "code_generation", "language": "python"},
            200,
            "Get quick prompt improvement suggestions"
        )
        
        # 3. Get personalized templates
        self.test_endpoint(
            "GET",
            "/api/v1/intelligence/templates/personalized",
            {"user_preferences": {"style": "concise", "detail_level": "high"}},
            200,
            "Get personalized prompt templates"
        )
        
        # 4. Get user patterns
        self.test_endpoint(
            "GET",
            "/api/v1/intelligence/patterns/user",
            {"analysis_period": "30_days"},
            200,
            "Get user prompt patterns and insights"
        )
        
        # 5. Submit suggestion feedback
        feedback_data = {
            "suggestion_id": f"sugg_{uuid.uuid4().hex[:12]}",
            "feedback_type": "helpful",
            "rating": 5,
            "comments": "Very useful suggestion for improving code clarity"
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/intelligence/feedback",
            feedback_data,
            200,
            "Submit feedback on suggestion quality"
        )
        
        # 6. Get intelligence analytics
        self.test_endpoint(
            "GET",
            "/api/v1/intelligence/analytics/intelligence",
            None,
            200,
            "Get intelligence analytics and metrics"
        )
        
    async def run_workflow_tests(self):
        """Test smart workflow functionality"""
        self.print_section_header("SMART WORKFLOWS", "⚙️")
        
        # 1. Workflow service health
        self.test_endpoint(
            "GET",
            "/api/v1/workflows/api/workflows/health",
            None,
            200,
            "Workflow service health check"
        )
        
        # 2. Get workflow templates
        self.test_endpoint(
            "GET",
            "/api/v1/workflows/api/workflows/templates",
            None,
            200,
            "Get available workflow templates"
        )
        
        # 3. Create workflow template
        template = self.test_workflow_templates[0]
        
        result = self.test_endpoint(
            "POST",
            "/api/v1/workflows/api/workflows/templates",
            template,
            201,
            "Create new workflow template"
        )
        
        # Extract template ID for workflow execution
        template_id = None
        if result["success"] and "template_id" in result["response_data"]:
            template_id = result["response_data"]["template_id"]
            self.log_debug(f"📋 Created template ID: {template_id}", level=2)
            
        # 4. Get specific template
        if template_id:
            self.test_endpoint(
                "GET",
                f"/api/v1/workflows/api/workflows/templates/{template_id}",
                None,
                200,
                "Get specific workflow template details"
            )
            
        # 5. Start workflow
        workflow_start_data = {
            "template_id": template_id or "default-template",
            "inputs": {
                "code_file": self.test_code_samples[0]["content"],
                "language": self.test_code_samples[0]["language"],
                "context": self.test_code_samples[0]["context"]
            },
            "metadata": {
                "user_id": self.test_uid,
                "project": "test_project"
            }
        }
        
        workflow_result = self.test_endpoint(
            "POST",
            "/api/v1/workflows/api/workflows/start",
            workflow_start_data,
            200,
            "Start workflow execution"
        )
        
        # Extract instance ID for monitoring
        instance_id = None
        if workflow_result["success"] and "instance_id" in workflow_result["response_data"]:
            instance_id = workflow_result["response_data"]["instance_id"]
            self.log_debug(f"⚡ Workflow instance ID: {instance_id}", level=2)
            
            # Log workflow execution
            self.workflow_executions.append({
                "instance_id": instance_id,
                "template_id": template_id,
                "started_at": datetime.now().isoformat(),
                "inputs": workflow_start_data["inputs"]
            })
            
        # 6. Check workflow status
        if instance_id:
            self.test_endpoint(
                "GET",
                f"/api/v1/workflows/api/workflows/status/{instance_id}",
                None,
                200,
                "Check workflow execution status"
            )
            
            # Small delay for workflow processing
            time.sleep(2)
            
            # 7. Get workflow results
            self.test_endpoint(
                "GET",
                f"/api/v1/workflows/api/workflows/results/{instance_id}",
                None,
                200,
                "Get workflow execution results"
            )
            
        # 8. Get user workflows
        self.test_endpoint(
            "GET",
            "/api/v1/workflows/api/workflows/my-workflows",
            None,
            200,
            "Get user's workflow history"
        )
        
        # 9. Quick start workflows
        content_workflow_data = {
            "topic": "React testing best practices",
            "content_type": "tutorial",
            "target_audience": "intermediate_developers"
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/workflows/api/workflows/quick-start/content-creation",
            content_workflow_data,
            200,
            "Quick start content creation workflow"
        )
        
        code_review_data = {
            "code": self.test_code_samples[1]["content"],
            "language": self.test_code_samples[1]["language"],
            "review_type": "comprehensive"
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/workflows/api/workflows/quick-start/code-review",
            code_review_data,
            200,
            "Quick start code review workflow"
        )
        
        # 10. Get workflow analytics
        self.test_endpoint(
            "GET",
            "/api/v1/workflows/api/workflows/analytics/usage",
            None,
            200,
            "Get workflow usage analytics"
        )
        
    def print_extension_activity_summary(self):
        """Print extension activity analysis"""
        self.print_section_header("EXTENSION ACTIVITY ANALYSIS", "📝")
        
        if not self.extension_logs:
            print("⚠️ No extension activities logged")
            return
            
        total_activities = len(self.extension_logs)
        
        # Group by activity type
        activity_types = {}
        for activity in self.extension_logs:
            activity_type = activity["type"]
            if activity_type not in activity_types:
                activity_types[activity_type] = 0
            activity_types[activity_type] += 1
            
        print(f"📊 ACTIVITY SUMMARY:")
        print(f"   Total Activities: {total_activities}")
        
        print(f"\n📈 ACTIVITY TYPES:")
        for activity_type, count in sorted(activity_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   {activity_type}: {count}")
            
        print(f"\n⚙️ WORKFLOW EXECUTIONS: {len(self.workflow_executions)}")
        for execution in self.workflow_executions:
            print(f"   🔄 {execution['instance_id']} - {execution['started_at']}")
            
    def print_comprehensive_results(self):
        """Print comprehensive developer tools test results"""
        self.print_section_header("DEVELOPER TOOLS TEST RESULTS", "📊")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        avg_response_time = sum(r.get("response_time_ms", 0) for r in self.test_results) / total_tests if total_tests > 0 else 0
        
        print(f"🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Avg Response Time: {avg_response_time:.0f}ms")
        
        # Group by test categories (API sections)
        categories = {}
        for result in self.test_results:
            endpoint_parts = result["endpoint"].split("/")
            if len(endpoint_parts) > 3:
                category = endpoint_parts[3]  # e.g., "extension", "context", "intelligence", "workflows"
                if category not in categories:
                    categories[category] = {"total": 0, "passed": 0}
                categories[category]["total"] += 1
                if result["success"]:
                    categories[category]["passed"] += 1
                    
        print(f"\n📈 RESULTS BY CATEGORY:")
        for category, stats in categories.items():
            cat_success_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            status_emoji = "✅" if cat_success_rate >= 90 else "⚠️" if cat_success_rate >= 70 else "❌"
            print(f"   {status_emoji} {category.upper()}: {stats['passed']}/{stats['total']} ({cat_success_rate:.1f}%)")
            
        # Show failed tests
        if failed_tests > 0:
            print(f"\n💥 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['method']} {result['endpoint']} [{result['status_code']}]")
                    print(f"      {result['description']}")
                    
        print(f"\n🎯 Next: Run 'python admin_monitoring.py' to test system monitoring")
        
    async def run_complete_test_suite(self):
        """Execute the complete developer tools test suite"""
        start_time = time.time()
        
        print("⚒️ PROMPTFORGE.AI DEVELOPER TOOLS TEST SUITE")
        print("=" * 80)
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🐛 Debug Level: {self.debug_level}")
        print(f"👤 Test User: {self.test_uid}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💻 Code Samples: {len(self.test_code_samples)}")
        print(f"📋 Workflow Templates: {len(self.test_workflow_templates)}")
        
        # Execute test flows
        await self.run_extension_intelligence_tests()
        await self.run_context_intelligence_tests()
        await self.run_prompt_intelligence_tests()
        await self.run_workflow_tests()
        
        # Generate reports
        total_time = time.time() - start_time
        
        self.print_comprehensive_results()
        self.print_extension_activity_summary()
        
        print(f"\n⏰ Total execution time: {total_time:.1f}s")
        print(f"📝 Extension activities: {len(self.extension_logs)}")
        print(f"⚙️ Workflows executed: {len(self.workflow_executions)}")
        
        return self.test_results

async def main():
    """Main execution function"""
    tester = DeveloperToolsTester(debug_level=3)
    results = await tester.run_complete_test_suite()
    return results

if __name__ == "__main__":
    print("⚒️ DEMON ENGINE - Developer Tools Test Suite")
    print("=" * 60)
    
    # Run the async test suite
    asyncio.run(main())
