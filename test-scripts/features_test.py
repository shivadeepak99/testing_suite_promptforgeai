#!/usr/bin/env python3
"""
🧠 FEATURES TEST - DEMON ENGINE & BRAIN ENGINE COMPREHENSIVE SUITE
Tests core AI features with deep internal workflow debugging
Tracks pipeline selection, technique matching, LLM execution, and performance metrics
Part of the Demon Engine Testing Framework
"""

import requests
import json
import time
import os
import asyncio
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from motor.motor_asyncio import AsyncIOMotorClient
import uuid

class FeaturesTestSuite:
    def __init__(self, base_url: str = "http://localhost:8000", debug_level: int = 3):
        """
        Initialize the Features Test Suite
        
        Args:
            base_url: API base URL  
            debug_level: 1=minimal, 2=standard, 3=detailed, 4=forensic
        """
        self.base_url = base_url
        self.debug_level = debug_level
        self.session = requests.Session()
        self.test_results = []
        self.engine_debug_logs = []
        self.performance_metrics = []
        
        # Test user setup
        self.test_uid = f"test-features-{uuid.uuid4().hex[:8]}"
        
        # Engine testing configuration
        self.engine_tests = self.setup_engine_test_matrix()
        
        # Setup debug environment
        self.setup_debug_environment()
        
    def setup_debug_environment(self):
        """Enable comprehensive backend debugging for engines"""
        # Backend debug flags
        os.environ['DEBUG_BRAIN_ENGINE'] = '1'
        os.environ['DEBUG_DEMON_ENGINE'] = '1'
        os.environ['DEBUG_PIPELINE_SELECTION'] = '1'
        os.environ['DEBUG_TECHNIQUE_MATCHING'] = '1'
        os.environ['DEBUG_LLM_EXECUTION'] = '1'
        os.environ['DEBUG_PERFORMANCE'] = '1'
        
        # Session headers for test identification
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'PromptForge-FeatureTest/1.0',
            'X-Test-Mode': 'features',
            'X-Debug-Level': str(self.debug_level),
            'Authorization': f'Bearer mock-features-token-{self.test_uid}'
        })
        
    def setup_engine_test_matrix(self) -> List[Dict]:
        """Define comprehensive test matrix for both engines"""
        return [
            # =========================================
            # LEGACY BRAIN ENGINE TESTS (/api/v1/prompt/)
            # =========================================
            {
                "category": "Legacy Brain Engine",
                "engine": "brain_legacy",
                "tests": [
                    {
                        "name": "quick_upgrade_basic",
                        "endpoint": "/api/v1/prompt/prompt/quick_upgrade",
                        "method": "POST",
                        "data": {
                            "text": "Write an email about meeting",
                            "mode": "quick"
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "signal_extraction",
                            "technique_matching", 
                            "pipeline_composition",
                            "groq_api_call",
                            "response_formatting"
                        ]
                    },
                    {
                        "name": "full_upgrade_advanced",
                        "endpoint": "/api/v1/prompt/prompt/upgrade", 
                        "method": "POST",
                        "data": {
                            "text": "Create a Python function to validate email addresses",
                            "mode": "full",
                            "context": "development"
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "deep_analysis",
                            "technique_selection",
                            "multi_pass_processing",
                            "code_awareness",
                            "optimization_passes"
                        ]
                    }
                ]
            },
            
            # =========================================
            # DEMON ENGINE V2 TESTS (/api/v1/demon/)
            # =========================================
            {
                "category": "Demon Engine v2",
                "engine": "demon_v2",
                "tests": [
                    {
                        "name": "demon_free_mode",
                        "endpoint": "/api/v1/demon/v2/upgrade",
                        "method": "POST", 
                        "data": {
                            "text": "Explain quantum computing",
                            "intent": "chat",
                            "mode": "free",
                            "client": "chrome",
                            "meta": {"lang": "en"},
                            "explain": True
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "intent_inference",
                            "client_identification", 
                            "pipeline_registry_lookup",
                            "free_pipeline_selection",
                            "saint_mode_execution",
                            "contract_enforcement"
                        ]
                    },
                    {
                        "name": "demon_pro_mode",
                        "endpoint": "/api/v1/demon/v2/upgrade",
                        "method": "POST",
                        "data": {
                            "text": "Create a React component for user authentication",
                            "intent": "code", 
                            "mode": "pro",
                            "client": "vscode",
                            "meta": {"lang": "javascript", "framework": "react"},
                            "explain": True
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "intent_inference",
                            "pro_entitlement_check",
                            "vscode_pipeline_selection", 
                            "code_context_analysis",
                            "technique_matching",
                            "fragment_rendering",
                            "llm_execution",
                            "demon_mode_execution",
                            "contract_validation"
                        ]
                    },
                    {
                        "name": "demon_agent_mode",
                        "endpoint": "/api/v1/demon/v2/upgrade",
                        "method": "POST", 
                        "data": {
                            "text": "Build a complete REST API for a todo app",
                            "intent": "agent",
                            "mode": "pro",
                            "client": "cursor",
                            "meta": {"lang": "python", "framework": "fastapi"},
                            "explain": True
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "agent_intent_detection",
                            "cursor_client_handling",
                            "objective_expansion",
                            "step_graph_creation", 
                            "tool_invocation_planning",
                            "multi_stage_execution",
                            "agent_contract_enforcement"
                        ]
                    },
                    {
                        "name": "demon_editor_mode",
                        "endpoint": "/api/v1/demon/v2/upgrade",
                        "method": "POST",
                        "data": {
                            "text": "Refactor this function for better performance",
                            "intent": "editor",
                            "mode": "pro", 
                            "client": "vscode",
                            "meta": {"lang": "python", "context": "optimization"},
                            "explain": True
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "editor_intent_processing",
                            "code_context_extraction",
                            "performance_analysis",
                            "refactoring_suggestions",
                            "editor_contract_compliance"
                        ]
                    }
                ]
            },
            
            # =========================================
            # AI FEATURES INTEGRATION TESTS (/api/v1/ai/)
            # =========================================
            {
                "category": "AI Features",
                "engine": "ai_features",
                "tests": [
                    {
                        "name": "remix_prompt",
                        "endpoint": "/api/v1/ai/remix-prompt",
                        "method": "POST",
                        "data": {
                            "prompt_body": "Write a blog post about artificial intelligence"
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "remix_algorithm_selection",
                            "style_variation_generation",
                            "tone_adjustment",
                            "creativity_injection"
                        ]
                    },
                    {
                        "name": "architect_prompt", 
                        "endpoint": "/api/v1/ai/architect-prompt",
                        "method": "POST",
                        "data": {
                            "description": "Create a microservices architecture for e-commerce",
                            "techStack": ["python", "fastapi", "postgresql", "redis"],
                            "architectureStyle": "microservices"
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "architecture_analysis",
                            "tech_stack_optimization",
                            "pattern_application",
                            "best_practices_injection"
                        ]
                    },
                    {
                        "name": "fuse_prompts",
                        "endpoint": "/api/v1/ai/fuse-prompts", 
                        "method": "POST",
                        "data": {
                            "prompts": [
                                "Write technical documentation",
                                "Focus on user experience", 
                                "Include code examples"
                            ],
                            "fusion_type": "hybrid"
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "prompt_compatibility_analysis",
                            "fusion_strategy_selection",
                            "conflict_resolution",
                            "coherence_optimization"
                        ]
                    },
                    {
                        "name": "analyze_prompt",
                        "endpoint": "/api/v1/ai/analyze-prompt",
                        "method": "POST",
                        "data": {
                            "prompt_body": "Create a machine learning model to predict stock prices using historical data and sentiment analysis"
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "complexity_assessment",
                            "domain_identification",
                            "technique_recommendation",
                            "improvement_suggestions"
                        ]
                    },
                    {
                        "name": "generate_enhanced_prompt",
                        "endpoint": "/api/v1/ai/generate-enhanced-prompt",
                        "method": "POST", 
                        "data": {
                            "base_prompt": "Help me write code",
                            "enhancement_type": "detailed",
                            "domain": "software_development"
                        },
                        "expected_status": 200,
                        "debug_points": [
                            "enhancement_strategy_selection",
                            "domain_expertise_injection",
                            "specificity_improvement",
                            "clarity_optimization"
                        ]
                    }
                ]
            }
        ]
        
    def log_debug(self, message: str, level: int = 3, data: Any = None):
        """Structured debug logging with engine context"""
        if level <= self.debug_level:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] {message}")
            if data and self.debug_level >= 4:
                print(f"    📊 Data: {json.dumps(data, indent=2, default=str)}")
                
    def extract_engine_debug_info(self, response_data: Dict, test_context: Dict) -> Dict:
        """Extract and parse engine debug information from response"""
        debug_info = {
            "test_context": test_context,
            "timestamp": datetime.now().isoformat(),
            "engine_type": test_context.get("engine", "unknown"),
            "pipeline_info": {},
            "technique_info": {},
            "llm_info": {},
            "performance_info": {},
            "errors": []
        }
        
        try:
            # Extract common debug fields
            if isinstance(response_data, dict):
                # Pipeline information
                if "pipeline_id" in response_data:
                    debug_info["pipeline_info"]["id"] = response_data["pipeline_id"]
                if "techniques_used" in response_data:
                    debug_info["technique_info"]["techniques"] = response_data["techniques_used"]
                if "execution_time_ms" in response_data:
                    debug_info["performance_info"]["execution_time"] = response_data["execution_time_ms"]
                if "tokens_used" in response_data:
                    debug_info["performance_info"]["tokens"] = response_data["tokens_used"]
                if "quality_score" in response_data:
                    debug_info["performance_info"]["quality"] = response_data["quality_score"]
                    
                # Demon Engine specific fields
                if "explanation" in response_data:
                    debug_info["pipeline_info"]["explanation"] = response_data["explanation"]
                if "formatted_output" in response_data:
                    debug_info["pipeline_info"]["formatted"] = True
                    
                # Error information
                if "error_message" in response_data:
                    debug_info["errors"].append(response_data["error_message"])
                if "fallback_used" in response_data:
                    debug_info["pipeline_info"]["fallback_used"] = response_data["fallback_used"]
                    
            self.engine_debug_logs.append(debug_info)
            
            if self.debug_level >= 3:
                self.log_debug(f"🧠 Engine Debug Extracted:", level=3, data=debug_info)
                
        except Exception as e:
            self.log_debug(f"⚠️ Debug extraction failed: {e}", level=2)
            debug_info["errors"].append(f"Debug extraction error: {str(e)}")
            
        return debug_info
        
    def analyze_performance_metrics(self, result: Dict, debug_info: Dict):
        """Analyze and store performance metrics"""
        metrics = {
            "test_id": result.get("test_id"),
            "endpoint": result.get("endpoint"),
            "engine": debug_info.get("engine_type", "unknown"),
            "response_time_ms": result.get("response_time_ms", 0),
            "execution_time_ms": debug_info.get("performance_info", {}).get("execution_time", 0),
            "tokens_used": debug_info.get("performance_info", {}).get("tokens", 0),
            "quality_score": debug_info.get("performance_info", {}).get("quality", 0.0),
            "success": result.get("success", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.performance_metrics.append(metrics)
        
        # Log performance insights
        if self.debug_level >= 2:
            quality_emoji = "🎯" if metrics["quality_score"] > 0.8 else "⚠️" if metrics["quality_score"] > 0.5 else "❌"
            speed_emoji = "⚡" if metrics["response_time_ms"] < 1000 else "🐌" if metrics["response_time_ms"] > 3000 else "⏱️"
            
            self.log_debug(
                f"📊 Performance: {speed_emoji} {metrics['response_time_ms']}ms, "
                f"{quality_emoji} Quality: {metrics['quality_score']:.2f}, "
                f"Tokens: {metrics['tokens_used']}", 
                level=2
            )
            
    def test_endpoint_with_engine_debug(self, test_config: Dict, context: Dict) -> Dict:
        """Execute API test with comprehensive engine debugging"""
        test_start = time.time()
        
        try:
            # Prepare request
            method = test_config["method"]
            endpoint = test_config["endpoint"] 
            data = test_config["data"]
            expected_status = test_config["expected_status"]
            description = test_config.get("name", "Unknown test")
            
            url = f"{self.base_url}{endpoint}"
            self.log_debug(f"🚀 {method} {endpoint} - {description}", level=2)
            
            if self.debug_level >= 4:
                self.log_debug(f"📤 Request data:", level=4, data=data)
                
            # Log expected debug points
            debug_points = test_config.get("debug_points", [])
            if debug_points and self.debug_level >= 3:
                self.log_debug(f"🔍 Expected debug points: {', '.join(debug_points)}", level=3)
                
            # Execute request
            if method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "GET":
                response = self.session.get(url, params=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
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
            
            # Store basic result
            result = {
                "test_id": f"features_{len(self.test_results)+1:03d}",
                "name": description,
                "method": method,
                "endpoint": endpoint,
                "engine": context.get("engine", "unknown"),
                "category": context.get("category", "unknown"),
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response_time_ms": int(response_time),
                "response_data": response_data,
                "debug_points_expected": debug_points,
                "timestamp": datetime.now().isoformat()
            }
            
            # Extract engine debug information
            debug_info = self.extract_engine_debug_info(response_data, context)
            result["debug_info"] = debug_info
            
            # Analyze performance
            self.analyze_performance_metrics(result, debug_info)
            
            # Log detailed response for failures
            if not success and self.debug_level >= 2:
                self.log_debug(f"📥 Error Response:", level=2, data=response_data)
                
            self.test_results.append(result)
            return result
            
        except Exception as e:
            self.log_debug(f"💥 Request failed: {str(e)}", level=1)
            result = {
                "test_id": f"features_{len(self.test_results)+1:03d}",
                "name": test_config.get("name", "Unknown test"),
                "method": test_config.get("method", "UNKNOWN"),
                "endpoint": test_config.get("endpoint", "unknown"),
                "engine": context.get("engine", "unknown"),
                "category": context.get("category", "unknown"),
                "status_code": 0,
                "expected_status": test_config.get("expected_status", 200),
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
        
    async def run_engine_test_category(self, category_config: Dict):
        """Run all tests for a specific engine category"""
        category_name = category_config["category"]
        engine_type = category_config["engine"]
        tests = category_config["tests"]
        
        self.print_section_header(f"{category_name.upper()} TESTS", "🧠")
        
        context = {
            "category": category_name,
            "engine": engine_type
        }
        
        for test_config in tests:
            self.log_debug(f"🎯 Running: {test_config['name']}", level=2)
            
            result = self.test_endpoint_with_engine_debug(test_config, context)
            
            # Add a small delay between tests for debug log separation
            if self.debug_level >= 3:
                time.sleep(0.5)
                
    def print_performance_analysis(self):
        """Print comprehensive performance analysis"""
        self.print_section_header("PERFORMANCE ANALYSIS", "📊")
        
        if not self.performance_metrics:
            print("⚠️ No performance metrics collected")
            return
            
        # Calculate aggregate metrics
        total_tests = len(self.performance_metrics)
        successful_tests = len([m for m in self.performance_metrics if m["success"]])
        
        # Response time analysis
        response_times = [m["response_time_ms"] for m in self.performance_metrics if m["response_time_ms"] > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        
        # Token usage analysis
        token_usage = [m["tokens_used"] for m in self.performance_metrics if m["tokens_used"] > 0]
        avg_tokens = sum(token_usage) / len(token_usage) if token_usage else 0
        
        # Quality analysis
        quality_scores = [m["quality_score"] for m in self.performance_metrics if m["quality_score"] > 0]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        print(f"📈 AGGREGATE METRICS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Success Rate: {(successful_tests/total_tests*100):.1f}%")
        print(f"   Avg Response Time: {avg_response_time:.0f}ms")
        print(f"   Response Time Range: {min_response_time:.0f}ms - {max_response_time:.0f}ms")
        print(f"   Avg Token Usage: {avg_tokens:.0f}")
        print(f"   Avg Quality Score: {avg_quality:.2f}")
        
        # Engine comparison
        engines = {}
        for metric in self.performance_metrics:
            engine = metric["engine"]
            if engine not in engines:
                engines[engine] = {"count": 0, "success": 0, "total_time": 0, "total_tokens": 0}
            engines[engine]["count"] += 1
            if metric["success"]:
                engines[engine]["success"] += 1
            engines[engine]["total_time"] += metric["response_time_ms"]
            engines[engine]["total_tokens"] += metric["tokens_used"]
            
        print(f"\n🔀 ENGINE COMPARISON:")
        for engine, stats in engines.items():
            success_rate = (stats["success"] / stats["count"] * 100) if stats["count"] > 0 else 0
            avg_time = stats["total_time"] / stats["count"] if stats["count"] > 0 else 0
            avg_tokens = stats["total_tokens"] / stats["count"] if stats["count"] > 0 else 0
            
            print(f"   🧠 {engine.upper()}:")
            print(f"      Success Rate: {success_rate:.1f}%")
            print(f"      Avg Time: {avg_time:.0f}ms")
            print(f"      Avg Tokens: {avg_tokens:.0f}")
            
    def print_debug_insights(self):
        """Print insights from engine debug logs"""
        self.print_section_header("ENGINE DEBUG INSIGHTS", "🔍")
        
        if not self.engine_debug_logs:
            print("⚠️ No engine debug logs collected")
            return
            
        # Pipeline usage analysis
        pipelines = {}
        techniques = {}
        
        for debug_log in self.engine_debug_logs:
            # Count pipeline usage
            pipeline_id = debug_log.get("pipeline_info", {}).get("id")
            if pipeline_id:
                pipelines[pipeline_id] = pipelines.get(pipeline_id, 0) + 1
                
            # Count technique usage
            techs = debug_log.get("technique_info", {}).get("techniques", [])
            for tech in techs:
                techniques[tech] = techniques.get(tech, 0) + 1
                
        print(f"🎯 PIPELINE USAGE:")
        for pipeline, count in sorted(pipelines.items(), key=lambda x: x[1], reverse=True):
            print(f"   {pipeline}: {count} times")
            
        print(f"\n🛠️ TOP TECHNIQUES:")
        for technique, count in sorted(techniques.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {technique}: {count} times")
            
        # Error analysis
        errors = []
        for debug_log in self.engine_debug_logs:
            errors.extend(debug_log.get("errors", []))
            
        if errors:
            print(f"\n⚠️ ERRORS DETECTED:")
            for error in set(errors):  # Unique errors only
                print(f"   ❌ {error}")
                
    def print_comprehensive_results(self):
        """Print comprehensive test results summary"""
        self.print_section_header("FEATURES TEST RESULTS SUMMARY", "📋")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Group results by category
        categories = {}
        for result in self.test_results:
            category = result.get("category", "Unknown")
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0}
            categories[category]["total"] += 1
            if result["success"]:
                categories[category]["passed"] += 1
                
        print(f"\n📊 RESULTS BY CATEGORY:")
        for category, stats in categories.items():
            success_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            status_emoji = "✅" if success_rate >= 90 else "⚠️" if success_rate >= 70 else "❌"
            print(f"   {status_emoji} {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
            
        # Show failed tests
        if failed_tests > 0:
            print(f"\n💥 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['name']} [{result['status_code']}] - {result['engine']}")
                    if "error" in result:
                        print(f"      Error: {result['error']}")
                        
        print(f"\n🎯 Next: Run 'python marketplace_flow.py' to test e-commerce features")
        
    async def run_complete_test_suite(self):
        """Execute the complete features test suite"""
        start_time = time.time()
        
        print("🧠 PROMPTFORGE.AI FEATURES TEST SUITE - DEMON ENGINE & BRAIN ENGINE")
        print("=" * 80)
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🐛 Debug Level: {self.debug_level}")
        print(f"👤 Test User: {self.test_uid}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🧪 Total Test Categories: {len(self.engine_tests)}")
        
        # Run all engine test categories
        for category_config in self.engine_tests:
            await self.run_engine_test_category(category_config)
            
        # Generate comprehensive analysis
        total_time = time.time() - start_time
        
        self.print_comprehensive_results()
        self.print_performance_analysis()
        self.print_debug_insights()
        
        print(f"\n⏰ Total execution time: {total_time:.1f}s")
        print(f"📊 Debug logs collected: {len(self.engine_debug_logs)}")
        print(f"📈 Performance metrics: {len(self.performance_metrics)}")
        
        return self.test_results

async def main():
    """Main execution function"""
    tester = FeaturesTestSuite(debug_level=3)
    results = await tester.run_complete_test_suite()
    return results

if __name__ == "__main__":
    print("🧠 DEMON ENGINE - Features Test Suite")
    print("=" * 60)
    
    # Run the async test suite
    asyncio.run(main())
