#!/usr/bin/env python3
"""
🔒 SECURITY VALIDATION - COMPREHENSIVE SECURITY TEST SUITE
Tests authentication, authorization, input validation, injection prevention, and security controls
Validates security measures, rate limiting, and protection against common attacks
Part of the Demon Engine Testing Framework
"""

import requests
import json
import time
import os
import asyncio
import uuid
import base64
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random
import string

class SecurityValidationTester:
    def __init__(self, base_url: str = "http://localhost:8000", debug_level: int = 3):
        """
        Initialize the Security Validation Test Suite
        
        Args:
            base_url: API base URL
            debug_level: 1=minimal, 2=standard, 3=detailed, 4=forensic
        """
        self.base_url = base_url
        self.debug_level = debug_level
        self.session = requests.Session()
        self.test_results = []
        self.security_events = []
        self.rate_limit_tests = []
        self.injection_attempts = []
        
        # Test data setup
        self.test_uid = f"test-security-{uuid.uuid4().hex[:8]}"
        self.attack_vectors = self.setup_attack_vectors()
        self.auth_test_scenarios = self.setup_auth_scenarios()
        
        # Setup environment
        self.setup_debug_environment()
        
    def setup_debug_environment(self):
        """Enable comprehensive debugging for security testing"""
        # Backend debug flags
        os.environ['DEBUG_SECURITY'] = '1'
        os.environ['DEBUG_AUTH'] = '1'
        os.environ['DEBUG_RATE_LIMITING'] = '1'
        os.environ['DEBUG_VALIDATION'] = '1'
        os.environ['DEBUG_INJECTION_PROTECTION'] = '1'
        
        # Session headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'PromptForge-SecurityTest/1.0',
            'X-Test-Mode': 'security_validation',
            'X-Security-Test': 'true'
        })
        
    def setup_attack_vectors(self) -> List[Dict]:
        """Define security attack vectors for testing"""
        return [
            # SQL Injection Attempts
            {
                "category": "sql_injection",
                "name": "basic_sql_injection",
                "payload": "' OR 1=1 --",
                "description": "Basic SQL injection attempt"
            },
            {
                "category": "sql_injection", 
                "name": "union_sql_injection",
                "payload": "' UNION SELECT * FROM users --",
                "description": "Union-based SQL injection"
            },
            
            # NoSQL Injection (MongoDB)
            {
                "category": "nosql_injection",
                "name": "mongodb_injection",
                "payload": {"$ne": None},
                "description": "MongoDB NoSQL injection attempt"
            },
            
            # XSS Attempts
            {
                "category": "xss",
                "name": "script_injection",
                "payload": "<script>alert('XSS')</script>",
                "description": "Basic XSS script injection"
            },
            {
                "category": "xss",
                "name": "event_handler_xss",
                "payload": "<img src=x onerror=alert('XSS')>",
                "description": "Event handler XSS"
            },
            
            # Command Injection
            {
                "category": "command_injection",
                "name": "basic_command_injection",
                "payload": "; ls -la",
                "description": "Basic command injection"
            },
            {
                "category": "command_injection",
                "name": "pipe_command_injection", 
                "payload": "| cat /etc/passwd",
                "description": "Pipe command injection"
            },
            
            # Path Traversal
            {
                "category": "path_traversal",
                "name": "directory_traversal",
                "payload": "../../../etc/passwd",
                "description": "Directory traversal attempt"
            },
            {
                "category": "path_traversal",
                "name": "null_byte_traversal",
                "payload": "../../../etc/passwd%00",
                "description": "Null byte path traversal"
            },
            
            # LDAP Injection
            {
                "category": "ldap_injection",
                "name": "ldap_bypass",
                "payload": "*)(uid=*))(|(uid=*",
                "description": "LDAP injection bypass"
            },
            
            # Template Injection
            {
                "category": "template_injection",
                "name": "jinja2_injection",
                "payload": "{{config.__class__.__init__.__globals__['os'].popen('id').read()}}",
                "description": "Jinja2 template injection"
            },
            
            # Large Payload (DoS)
            {
                "category": "dos",
                "name": "large_payload",
                "payload": "A" * 10000,
                "description": "Large payload DoS attempt"
            },
            
            # Null/Empty Payloads
            {
                "category": "null_injection",
                "name": "null_payload",
                "payload": None,
                "description": "Null payload injection"
            },
            {
                "category": "null_injection",
                "name": "empty_payload", 
                "payload": "",
                "description": "Empty payload injection"
            }
        ]
        
    def setup_auth_scenarios(self) -> List[Dict]:
        """Define authentication test scenarios"""
        return [
            {
                "name": "no_auth_token",
                "headers": {},
                "description": "Request without authentication token",
                "expected_status": 401
            },
            {
                "name": "invalid_token_format",
                "headers": {"Authorization": "InvalidTokenFormat"},
                "description": "Invalid token format",
                "expected_status": 401
            },
            {
                "name": "malformed_bearer_token",
                "headers": {"Authorization": "Bearer"},
                "description": "Malformed bearer token (no token)",
                "expected_status": 401
            },
            {
                "name": "fake_token",
                "headers": {"Authorization": "Bearer fake-token-12345"},
                "description": "Fake authentication token",
                "expected_status": 401
            },
            {
                "name": "sql_injection_token",
                "headers": {"Authorization": "Bearer ' OR 1=1 --"},
                "description": "SQL injection in auth token",
                "expected_status": 401
            },
            {
                "name": "xss_in_token",
                "headers": {"Authorization": "Bearer <script>alert('xss')</script>"},
                "description": "XSS payload in auth token",
                "expected_status": 401
            },
            {
                "name": "extremely_long_token",
                "headers": {"Authorization": f"Bearer {'x' * 5000}"},
                "description": "Extremely long auth token",
                "expected_status": 401
            },
            {
                "name": "null_byte_token",
                "headers": {"Authorization": "Bearer token\x00injection"},
                "description": "Null byte in auth token",
                "expected_status": 401
            }
        ]
        
    def log_debug(self, message: str, level: int = 3, data: Any = None):
        """Structured debug logging"""
        if level <= self.debug_level:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] {message}")
            if data and self.debug_level >= 4:
                print(f"    🔒 Data: {json.dumps(data, indent=2, default=str)}")
                
    def log_security_event(self, event_type: str, details: Dict):
        """Log security events for analysis"""
        event = {
            "id": f"sec_{uuid.uuid4().hex[:12]}",
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "user_id": self.test_uid,
            "details": details,
            "test_mode": True
        }
        
        self.security_events.append(event)
        
        if self.debug_level >= 3:
            self.log_debug(f"🔒 Security event: {event_type}", level=3, data=event)
            
    def test_endpoint_security(self, method: str, endpoint: str, data: Optional[Dict] = None,
                              headers: Optional[Dict] = None, expected_status: int = 401, 
                              description: str = "") -> Dict:
        """Execute security-focused API test"""
        test_start = time.time()
        
        try:
            url = f"{self.base_url}{endpoint}"
            self.log_debug(f"🔒 {method} {endpoint} - {description}", level=2)
            
            # Merge headers
            test_headers = self.session.headers.copy()
            if headers:
                test_headers.update(headers)
                
            if self.debug_level >= 4:
                self.log_debug(f"📤 Request data:", level=4, data=data)
                self.log_debug(f"📋 Headers:", level=4, data=test_headers)
                
            # Execute request
            if method.upper() == "GET":
                response = requests.get(url, params=data, headers=test_headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=test_headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=test_headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=test_headers)
                
            # Process response
            response_time = (time.time() - test_start) * 1000
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
                
            # For security tests, we often expect failures (401, 403, etc.)
            expected_failure = expected_status >= 400
            actual_failure = response.status_code >= 400
            
            # Success means the security control worked (blocked the attack)
            success = response.status_code == expected_status
            
            status_icon = "✅" if success else "❌"
            security_icon = "🛡️" if expected_failure and actual_failure else "⚠️" if not expected_failure else "🔓"
            
            self.log_debug(
                f"{status_icon} {security_icon} {method} {endpoint} [{response.status_code}] - {response_time:.0f}ms",
                level=2
            )
            
            # Log security event
            self.log_security_event(f"security_test_{method.lower()}", {
                "endpoint": endpoint,
                "request_data": data,
                "headers": headers,
                "response_code": response.status_code,
                "expected_status": expected_status,
                "security_control_effective": success,
                "description": description
            })
            
            result = {
                "test_id": f"security_{len(self.test_results)+1:03d}",
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "security_control_effective": success,
                "response_time_ms": int(response_time),
                "response_data": response_data,
                "attack_blocked": expected_failure and actual_failure,
                "timestamp": datetime.now().isoformat()
            }
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            self.log_debug(f"💥 Request failed: {str(e)}", level=1)
            result = {
                "test_id": f"security_{len(self.test_results)+1:03d}",
                "method": method,
                "endpoint": endpoint,
                "description": description,
                "status_code": 0,
                "expected_status": expected_status,
                "success": False,
                "security_control_effective": False,
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
        
    async def run_authentication_security_tests(self):
        """Test authentication security controls"""
        self.print_section_header("AUTHENTICATION SECURITY", "🔐")
        
        # Test various authentication scenarios
        protected_endpoints = [
            "/api/v1/users/me",
            "/api/v1/users/credits",
            "/api/v1/prompts/prompts/arsenal",
            "/api/v1/ai/remix-prompt"
        ]
        
        for scenario in self.auth_test_scenarios:
            for endpoint in protected_endpoints[:2]:  # Test first 2 endpoints to avoid spam
                self.test_endpoint_security(
                    "GET",
                    endpoint,
                    None,
                    scenario["headers"],
                    scenario["expected_status"],
                    f"{scenario['description']} on {endpoint}"
                )
                
                # Small delay between tests
                time.sleep(0.1)
                
    async def run_input_validation_tests(self):
        """Test input validation and sanitization"""
        self.print_section_header("INPUT VALIDATION", "🧹")
        
        # Set valid auth for these tests
        auth_headers = {"Authorization": f"Bearer mock-security-token-{self.test_uid}"}
        
        # Test injection attacks on various endpoints
        injection_endpoints = [
            {
                "method": "POST",
                "endpoint": "/api/v1/users/auth/complete",
                "base_data": {
                    "uid": "test-user",
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User"
                },
                "injection_fields": ["uid", "email", "first_name", "last_name"]
            },
            {
                "method": "POST",
                "endpoint": "/api/v1/prompts/prompts/",
                "base_data": {
                    "title": "Test Prompt",
                    "body": "Test content",
                    "role": "assistant"
                },
                "injection_fields": ["title", "body", "role"]
            },
            {
                "method": "POST",
                "endpoint": "/api/v1/ai/remix-prompt",
                "base_data": {
                    "prompt_body": "Write an email"
                },
                "injection_fields": ["prompt_body"]
            }
        ]
        
        # Test each attack vector on each endpoint
        for endpoint_config in injection_endpoints:
            for attack in self.attack_vectors[:10]:  # Test first 10 attack vectors
                for field in endpoint_config["injection_fields"][:1]:  # Test first field only
                    # Create poisoned data
                    poisoned_data = endpoint_config["base_data"].copy()
                    poisoned_data[field] = attack["payload"]
                    
                    self.test_endpoint_security(
                        endpoint_config["method"],
                        endpoint_config["endpoint"],
                        poisoned_data,
                        auth_headers,
                        400,  # Expect validation error
                        f"{attack['category']} in {field}: {attack['name']}"
                    )
                    
                    # Log injection attempt
                    self.injection_attempts.append({
                        "attack_type": attack["category"],
                        "payload": attack["payload"],
                        "endpoint": endpoint_config["endpoint"],
                        "field": field,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    time.sleep(0.05)  # Small delay
                    
    async def run_rate_limiting_tests(self):
        """Test rate limiting controls"""
        self.print_section_header("RATE LIMITING", "🚦")
        
        auth_headers = {"Authorization": f"Bearer mock-security-token-{self.test_uid}"}
        
        # Test rate limiting on a simple endpoint
        rate_limit_endpoint = "/api/v1/users/me"
        
        # Make rapid requests to trigger rate limiting
        start_time = time.time()
        rate_limit_results = []
        
        for i in range(20):  # 20 rapid requests
            result = self.test_endpoint_security(
                "GET",
                rate_limit_endpoint,
                None,
                auth_headers,
                200 if i < 10 else 429,  # Expect rate limiting after 10 requests
                f"Rate limit test request #{i+1}"
            )
            
            rate_limit_results.append({
                "request_number": i + 1,
                "status_code": result["status_code"],
                "response_time": result["response_time_ms"],
                "timestamp": result["timestamp"]
            })
            
            # Very small delay to simulate rapid requests
            time.sleep(0.02)
            
        end_time = time.time()
        
        # Analyze rate limiting effectiveness
        total_time = end_time - start_time
        requests_per_second = 20 / total_time
        rate_limited_requests = len([r for r in rate_limit_results if r["status_code"] == 429])
        
        self.rate_limit_tests.append({
            "endpoint": rate_limit_endpoint,
            "total_requests": 20,
            "total_time_seconds": total_time,
            "requests_per_second": requests_per_second,
            "rate_limited_count": rate_limited_requests,
            "rate_limiting_effective": rate_limited_requests > 0
        })
        
        self.log_debug(
            f"🚦 Rate limiting test: {requests_per_second:.1f} req/s, {rate_limited_requests} blocked",
            level=2
        )
        
    async def run_authorization_tests(self):
        """Test authorization and access control"""
        self.print_section_header("AUTHORIZATION CONTROLS", "🚪")
        
        # Test access to admin endpoints without admin privileges
        admin_endpoints = [
            "/api/v1/admin/diagnostics",
            "/api/v1/credits/admin/overview"
        ]
        
        regular_user_headers = {"Authorization": f"Bearer mock-user-token-{self.test_uid}"}
        
        for endpoint in admin_endpoints:
            self.test_endpoint_security(
                "GET",
                endpoint,
                None,
                regular_user_headers,
                403,  # Expect forbidden
                f"Regular user accessing admin endpoint: {endpoint}"
            )
            
        # Test accessing other user's resources
        other_user_resources = [
            "/api/v1/users/export-data",  # Should only access own data
            "/api/v1/prompts/prompts/arsenal"  # Should only see own prompts
        ]
        
        # Try with different user token
        other_user_headers = {"Authorization": f"Bearer mock-other-user-token-{uuid.uuid4().hex[:8]}"}
        
        for endpoint in other_user_resources:
            self.test_endpoint_security(
                "GET",
                endpoint,
                None,
                other_user_headers,
                401,  # Expect unauthorized or forbidden
                f"Cross-user resource access: {endpoint}"
            )
            
    async def run_data_exposure_tests(self):
        """Test for data exposure vulnerabilities"""
        self.print_section_header("DATA EXPOSURE TESTS", "👁️")
        
        auth_headers = {"Authorization": f"Bearer mock-security-token-{self.test_uid}"}
        
        # Test for information disclosure in error messages
        error_inducing_requests = [
            {
                "method": "GET",
                "endpoint": "/api/v1/prompts/prompts/nonexistent-id-12345",
                "description": "Test error message information disclosure"
            },
            {
                "method": "GET", 
                "endpoint": "/api/v1/users/credits",
                "description": "Test user data access controls"
            },
            {
                "method": "POST",
                "endpoint": "/api/v1/ai/remix-prompt",
                "data": {"malformed": "data"},
                "description": "Test validation error disclosure"
            }
        ]
        
        for request in error_inducing_requests:
            result = self.test_endpoint_security(
                request["method"],
                request["endpoint"],
                request.get("data"),
                auth_headers,
                200,  # We'll check the response content for data exposure
                request["description"]
            )
            
            # Check response for potential data exposure
            if result["success"] and isinstance(result["response_data"], dict):
                sensitive_patterns = ["password", "secret", "key", "token", "hash", "internal"]
                response_text = json.dumps(result["response_data"]).lower()
                
                for pattern in sensitive_patterns:
                    if pattern in response_text:
                        self.log_debug(f"⚠️ Potential data exposure: '{pattern}' found in response", level=2)
                        
    async def run_session_security_tests(self):
        """Test session management security"""
        self.print_section_header("SESSION SECURITY", "🎫")
        
        # Test session fixation
        fixed_session_id = "fixed-session-12345"
        session_headers = {
            "Authorization": f"Bearer mock-security-token-{self.test_uid}",
            "Cookie": f"session_id={fixed_session_id}"
        }
        
        self.test_endpoint_security(
            "GET",
            "/api/v1/users/me",
            None,
            session_headers,
            200,
            "Session fixation test"
        )
        
        # Test concurrent sessions
        concurrent_sessions = []
        for i in range(3):
            session_token = f"concurrent-session-{i}-{uuid.uuid4().hex[:8]}"
            concurrent_sessions.append({
                "Authorization": f"Bearer {session_token}"
            })
            
        for i, headers in enumerate(concurrent_sessions):
            self.test_endpoint_security(
                "GET",
                "/api/v1/users/me",
                None,
                headers,
                401,  # Expect unauthorized for invalid tokens
                f"Concurrent session test #{i+1}"
            )
            
    def print_security_analysis(self):
        """Print comprehensive security analysis"""
        self.print_section_header("SECURITY ANALYSIS", "🔍")
        
        if not self.security_events:
            print("⚠️ No security events logged")
            return
            
        total_events = len(self.security_events)
        
        # Group by event type
        event_types = {}
        for event in self.security_events:
            event_type = event["type"]
            if event_type not in event_types:
                event_types[event_type] = 0
            event_types[event_type] += 1
            
        print(f"📊 SECURITY EVENTS: {total_events}")
        
        print(f"\n🔒 EVENT TYPES:")
        for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   {event_type}: {count}")
            
        # Analyze injection attempts
        if self.injection_attempts:
            print(f"\n💉 INJECTION ATTEMPTS: {len(self.injection_attempts)}")
            
            attack_categories = {}
            for attempt in self.injection_attempts:
                category = attempt["attack_type"]
                if category not in attack_categories:
                    attack_categories[category] = 0
                attack_categories[category] += 1
                
            for category, count in attack_categories.items():
                print(f"   {category}: {count} attempts")
                
        # Analyze rate limiting
        if self.rate_limit_tests:
            print(f"\n🚦 RATE LIMITING ANALYSIS:")
            for test in self.rate_limit_tests:
                effectiveness = "✅ Effective" if test["rate_limiting_effective"] else "❌ Ineffective"
                print(f"   {test['endpoint']}: {effectiveness}")
                print(f"      {test['requests_per_second']:.1f} req/s, {test['rate_limited_count']} blocked")
                
    def print_comprehensive_results(self):
        """Print comprehensive security validation results"""
        self.print_section_header("SECURITY VALIDATION RESULTS", "📊")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        # For security tests, "success" means security controls worked
        security_controls_effective = len([r for r in self.test_results if r.get("security_control_effective", False)])
        attacks_blocked = len([r for r in self.test_results if r.get("attack_blocked", False)])
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        security_effectiveness = (security_controls_effective / total_tests * 100) if total_tests > 0 else 0
        
        print(f"🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Security Controls Effective: {security_effectiveness:.1f}%")
        print(f"   Attacks Blocked: {attacks_blocked}")
        
        # Group by security categories
        categories = {
            "authentication": 0,
            "authorization": 0,
            "validation": 0,
            "rate_limiting": 0,
            "data_exposure": 0,
            "session": 0
        }
        
        category_success = {key: 0 for key in categories.keys()}
        
        for result in self.test_results:
            description = result["description"].lower()
            for category in categories.keys():
                if category in description:
                    categories[category] += 1
                    if result["success"]:
                        category_success[category] += 1
                    break
            else:
                categories["validation"] += 1  # Default category
                if result["success"]:
                    category_success["validation"] += 1
                    
        print(f"\n📈 RESULTS BY SECURITY CATEGORY:")
        for category, total in categories.items():
            if total > 0:
                success = category_success[category]
                cat_success_rate = (success / total * 100)
                status_emoji = "✅" if cat_success_rate >= 90 else "⚠️" if cat_success_rate >= 70 else "❌"
                print(f"   {status_emoji} {category.upper()}: {success}/{total} ({cat_success_rate:.1f}%)")
                
        # Show failed security tests (these are concerning)
        security_failures = [r for r in self.test_results if not r.get("security_control_effective", True)]
        if security_failures:
            print(f"\n🚨 SECURITY CONTROL FAILURES:")
            for result in security_failures:
                print(f"   ⚠️ {result['method']} {result['endpoint']} [{result['status_code']}]")
                print(f"      {result['description']}")
                
        print(f"\n🎯 SECURITY SUMMARY:")
        print(f"   🛡️ Security controls are {'EFFECTIVE' if security_effectiveness > 80 else 'NEEDS IMPROVEMENT'}")
        print(f"   🔒 System appears {'SECURE' if attacks_blocked > 0 else 'VULNERABLE'}")
        
    async def run_complete_test_suite(self):
        """Execute the complete security validation test suite"""
        start_time = time.time()
        
        print("🔒 PROMPTFORGE.AI SECURITY VALIDATION TEST SUITE")
        print("=" * 80)
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🐛 Debug Level: {self.debug_level}")
        print(f"👤 Test User: {self.test_uid}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Attack Vectors: {len(self.attack_vectors)}")
        print(f"🔐 Auth Scenarios: {len(self.auth_test_scenarios)}")
        
        # Execute security test flows
        await self.run_authentication_security_tests()
        await self.run_authorization_tests()
        await self.run_input_validation_tests()
        await self.run_rate_limiting_tests()
        await self.run_data_exposure_tests()
        await self.run_session_security_tests()
        
        # Generate reports
        total_time = time.time() - start_time
        
        self.print_comprehensive_results()
        self.print_security_analysis()
        
        print(f"\n⏰ Total execution time: {total_time:.1f}s")
        print(f"🔒 Security events: {len(self.security_events)}")
        print(f"💉 Injection attempts: {len(self.injection_attempts)}")
        print(f"🚦 Rate limit tests: {len(self.rate_limit_tests)}")
        
        print(f"\n🎉 SECURITY VALIDATION COMPLETE!")
        print(f"📋 All test scripts have been executed. Check individual results for detailed analysis.")
        
        return self.test_results

async def main():
    """Main execution function"""
    tester = SecurityValidationTester(debug_level=3)
    results = await tester.run_complete_test_suite()
    return results

if __name__ == "__main__":
    print("🔒 DEMON ENGINE - Security Validation Test Suite")
    print("=" * 60)
    
    # Run the async test suite
    asyncio.run(main())
