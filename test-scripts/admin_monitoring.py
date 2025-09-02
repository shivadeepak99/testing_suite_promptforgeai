#!/usr/bin/env python3
"""
🖥️ ADMIN MONITORING - SYSTEM HEALTH & PERFORMANCE TEST SUITE
Tests monitoring, analytics, performance, and administrative features
Validates system health, circuit breakers, metrics collection, and operational monitoring
Part of the Demon Engine Testing Framework
"""

import requests
import json
import time
import os
import asyncio
import uuid
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorClient

class AdminMonitoringTester:
    def __init__(self, base_url: str = "http://localhost:8000", debug_level: int = 3):
        """
        Initialize the Admin Monitoring Test Suite
        
        Args:
            base_url: API base URL
            debug_level: 1=minimal, 2=standard, 3=detailed, 4=forensic
        """
        self.base_url = base_url
        self.debug_level = debug_level
        self.session = requests.Session()
        self.test_results = []
        self.system_metrics = []
        self.performance_snapshots = []
        self.circuit_breaker_states = []
        
        # Test data setup
        self.test_uid = f"test-admin-{uuid.uuid4().hex[:8]}"
        self.test_scenarios = self.setup_monitoring_scenarios()
        
        # System monitoring setup
        self.baseline_metrics = self.capture_system_baseline()
        
        # Setup environment
        self.setup_debug_environment()
        
    def setup_debug_environment(self):
        """Enable comprehensive debugging for admin/monitoring operations"""
        # Backend debug flags
        os.environ['DEBUG_MONITORING'] = '1'
        os.environ['DEBUG_ANALYTICS'] = '1'
        os.environ['DEBUG_PERFORMANCE'] = '1'
        os.environ['DEBUG_ADMIN'] = '1'
        os.environ['DEBUG_METRICS'] = '1'
        
        # Session headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'PromptForge-AdminTest/1.0',
            'X-Test-Mode': 'admin_monitoring',
            'X-Admin-Access': 'true',
            'Authorization': f'Bearer mock-admin-token-{self.test_uid}'
        })
        
    def setup_monitoring_scenarios(self) -> List[Dict]:
        """Define monitoring test scenarios"""
        return [
            {
                "name": "high_load_simulation",
                "description": "Simulate high load to test monitoring alerts",
                "duration_seconds": 30,
                "concurrent_requests": 10,
                "request_interval": 0.1
            },
            {
                "name": "circuit_breaker_test",
                "description": "Test circuit breaker activation and recovery",
                "failure_threshold": 5,
                "recovery_time": 10
            },
            {
                "name": "memory_monitoring",
                "description": "Monitor memory usage during operations",
                "memory_threshold_mb": 100,
                "monitoring_duration": 60
            },
            {
                "name": "database_performance",
                "description": "Monitor database query performance",
                "slow_query_threshold_ms": 1000,
                "query_count": 20
            }
        ]
        
    def capture_system_baseline(self) -> Dict:
        """Capture baseline system metrics"""
        try:
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "process_count": len(psutil.pids()),
                "boot_time": psutil.boot_time()
            }
        except Exception as e:
            self.log_debug(f"⚠️ Could not capture system baseline: {e}", level=2)
            return {"error": str(e)}
            
    def log_debug(self, message: str, level: int = 3, data: Any = None):
        """Structured debug logging"""
        if level <= self.debug_level:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] {message}")
            if data and self.debug_level >= 4:
                print(f"    🖥️ Data: {json.dumps(data, indent=2, default=str)}")
                
    def capture_performance_snapshot(self, checkpoint: str) -> Dict:
        """Capture system performance snapshot"""
        try:
            snapshot = {
                "checkpoint": checkpoint,
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_info": {
                    "percent": psutil.virtual_memory().percent,
                    "available_mb": psutil.virtual_memory().available / (1024 * 1024),
                    "used_mb": psutil.virtual_memory().used / (1024 * 1024)
                },
                "disk_io": psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
                "network_io": psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
            }
            
            self.performance_snapshots.append(snapshot)
            
            if self.debug_level >= 3:
                self.log_debug(f"📊 Performance snapshot: {checkpoint}", level=3, data={
                    "cpu": f"{snapshot['cpu_percent']:.1f}%",
                    "memory": f"{snapshot['memory_info']['percent']:.1f}%",
                    "available_memory": f"{snapshot['memory_info']['available_mb']:.0f}MB"
                })
                
            return snapshot
            
        except Exception as e:
            self.log_debug(f"⚠️ Performance snapshot failed: {e}", level=2)
            return {"error": str(e), "checkpoint": checkpoint}
            
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     expected_status: int = 200, description: str = "") -> Dict:
        """Execute API test with monitoring-specific logging"""
        test_start = time.time()
        
        try:
            url = f"{self.base_url}{endpoint}"
            self.log_debug(f"🖥️ {method} {endpoint} - {description}", level=2)
            
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
            
            # Store metrics for monitoring endpoints
            if any(keyword in endpoint.lower() for keyword in ['metrics', 'health', 'performance', 'analytics']):
                metric = {
                    "endpoint": endpoint,
                    "response_time_ms": response_time,
                    "status_code": response.status_code,
                    "success": success,
                    "timestamp": datetime.now().isoformat(),
                    "data_size": len(json.dumps(response_data)) if isinstance(response_data, dict) else len(str(response_data))
                }
                self.system_metrics.append(metric)
                
            result = {
                "test_id": f"admin_{len(self.test_results)+1:03d}",
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
                "test_id": f"admin_{len(self.test_results)+1:03d}",
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
        
    async def run_health_monitoring_tests(self):
        """Test health monitoring endpoints"""
        self.print_section_header("HEALTH MONITORING", "🏥")
        
        # Capture baseline performance
        self.capture_performance_snapshot("health_tests_start")
        
        # 1. Basic health check
        self.test_endpoint(
            "GET",
            "/health",
            None,
            200,
            "Basic health check endpoint"
        )
        
        # 2. Root endpoint
        self.test_endpoint(
            "GET",
            "/",
            None,
            200,
            "Root endpoint health"
        )
        
        # 3. Detailed health check
        self.test_endpoint(
            "GET",
            "/api/v1/monitoring/health/detailed",
            None,
            200,
            "Detailed system health check"
        )
        
        # 4. Performance health check
        self.test_endpoint(
            "GET",
            "/api/v1/performance/performance/health",
            None,
            200,
            "Performance subsystem health"
        )
        
        # 5. Webhook health check
        self.test_endpoint(
            "GET",
            "/api/v1/payments/webhooks/health",
            None,
            200,
            "Webhook subsystem health"
        )
        
        # 6. Extension health check
        self.test_endpoint(
            "GET",
            "/api/v1/extension/extension/health",
            None,
            200,
            "Extension subsystem health"
        )
        
        # 7. Workflow health check
        self.test_endpoint(
            "GET",
            "/api/v1/workflows/api/workflows/health",
            None,
            200,
            "Workflow subsystem health"
        )
        
        self.capture_performance_snapshot("health_tests_end")
        
    async def run_metrics_collection_tests(self):
        """Test metrics collection and reporting"""
        self.print_section_header("METRICS COLLECTION", "📊")
        
        self.capture_performance_snapshot("metrics_tests_start")
        
        # 1. Get system metrics
        self.test_endpoint(
            "GET",
            "/api/v1/monitoring/metrics",
            None,
            200,
            "Get system metrics"
        )
        
        # 2. Performance dashboard
        self.test_endpoint(
            "GET",
            "/api/v1/performance/performance/dashboard",
            None,
            200,
            "Get performance dashboard"
        )
        
        # 3. Cache statistics
        self.test_endpoint(
            "GET",
            "/api/v1/performance/performance/cache-stats",
            None,
            200,
            "Get cache statistics"
        )
        
        # 4. Slow queries
        self.test_endpoint(
            "GET",
            "/api/v1/performance/performance/slow-queries",
            None,
            200,
            "Get slow query analysis"
        )
        
        # 5. Credit analytics
        self.test_endpoint(
            "GET",
            "/api/v1/credits/analytics/routes",
            None,
            200,
            "Get credit usage analytics by route"
        )
        
        # 6. Analytics dashboard
        self.test_endpoint(
            "GET",
            "/api/v1/analytics/dashboard",
            None,
            200,
            "Get analytics dashboard"
        )
        
        self.capture_performance_snapshot("metrics_tests_end")
        
    async def run_circuit_breaker_tests(self):
        """Test circuit breaker functionality"""
        self.print_section_header("CIRCUIT BREAKERS", "🔌")
        
        self.capture_performance_snapshot("circuit_breaker_tests_start")
        
        # 1. Get circuit breaker status
        result = self.test_endpoint(
            "GET",
            "/api/v1/monitoring/circuit-breakers",
            None,
            200,
            "Get circuit breaker status"
        )
        
        # Store circuit breaker states
        if result["success"] and isinstance(result["response_data"], dict):
            self.circuit_breaker_states.append({
                "timestamp": datetime.now().isoformat(),
                "states": result["response_data"],
                "checkpoint": "initial_state"
            })
            
        # 2. Test circuit breaker reset (if any are available)
        if result["success"] and isinstance(result["response_data"], dict):
            breakers = result["response_data"].get("breakers", {})
            if breakers:
                # Try to reset the first available breaker
                breaker_name = list(breakers.keys())[0]
                self.test_endpoint(
                    "POST",
                    f"/api/v1/monitoring/circuit-breakers/{breaker_name}/reset",
                    {},
                    200,
                    f"Reset circuit breaker: {breaker_name}"
                )
                
                # Check state after reset
                reset_result = self.test_endpoint(
                    "GET",
                    "/api/v1/monitoring/circuit-breakers",
                    None,
                    200,
                    "Get circuit breaker status after reset"
                )
                
                if reset_result["success"]:
                    self.circuit_breaker_states.append({
                        "timestamp": datetime.now().isoformat(),
                        "states": reset_result["response_data"],
                        "checkpoint": "after_reset"
                    })
                    
        self.capture_performance_snapshot("circuit_breaker_tests_end")
        
    async def run_admin_diagnostics_tests(self):
        """Test administrative diagnostic features"""
        self.print_section_header("ADMIN DIAGNOSTICS", "🔧")
        
        self.capture_performance_snapshot("admin_tests_start")
        
        # 1. Admin diagnostics
        self.test_endpoint(
            "GET",
            "/api/v1/admin/diagnostics",
            None,
            200,
            "Get admin diagnostics"
        )
        
        # 2. Credit admin overview
        self.test_endpoint(
            "GET",
            "/api/v1/credits/admin/overview",
            None,
            200,  # May return 403 if not admin
            "Get admin credit overview"
        )
        
        self.capture_performance_snapshot("admin_tests_end")
        
    async def run_analytics_tests(self):
        """Test analytics and reporting functionality"""
        self.print_section_header("ANALYTICS & REPORTING", "📈")
        
        self.capture_performance_snapshot("analytics_tests_start")
        
        # 1. Log analytics events
        analytics_event = {
            "event_type": "test_event",
            "user_id": self.test_uid,
            "metadata": {
                "test_suite": "admin_monitoring",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/analytics/events",
            analytics_event,
            200,
            "Log analytics event"
        )
        
        # 2. Log performance metrics
        performance_metric = {
            "metric_name": "test_response_time",
            "value": 123.45,
            "unit": "milliseconds",
            "tags": {
                "endpoint": "/api/test",
                "method": "GET"
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/analytics/performance",
            performance_metric,
            200,
            "Log performance metric"
        )
        
        # 3. Create analytics job
        analytics_job = {
            "job_type": "usage_report",
            "parameters": {
                "date_range": "last_7_days",
                "metrics": ["response_time", "error_rate", "throughput"]
            }
        }
        
        job_result = self.test_endpoint(
            "POST",
            "/api/v1/analytics/jobs/analytics",
            analytics_job,
            201,
            "Create analytics job"
        )
        
        # 4. Check job status
        if job_result["success"] and "job_id" in job_result["response_data"]:
            job_id = job_result["response_data"]["job_id"]
            self.test_endpoint(
                "GET",
                f"/api/v1/analytics/jobs/analytics/{job_id}/status",
                None,
                200,
                "Check analytics job status"
            )
            
        # 5. Export analytics data
        export_request = {
            "data_type": "analytics",
            "format": "json",
            "date_range": {
                "start": (datetime.now() - timedelta(days=7)).isoformat(),
                "end": datetime.now().isoformat()
            }
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/analytics/exports/analytics",
            export_request,
            200,
            "Export analytics data"
        )
        
        # 6. Export prompts data
        prompts_export = {
            "format": "csv",
            "include_metadata": True
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/analytics/exports/prompts",
            prompts_export,
            200,
            "Export prompts data"
        )
        
        self.capture_performance_snapshot("analytics_tests_end")
        
    async def run_performance_optimization_tests(self):
        """Test performance optimization features"""
        self.print_section_header("PERFORMANCE OPTIMIZATION", "⚡")
        
        self.capture_performance_snapshot("optimization_tests_start")
        
        # 1. Trigger optimization
        self.test_endpoint(
            "POST",
            "/api/v1/performance/performance/optimize",
            {},
            200,
            "Trigger system optimization"
        )
        
        # 2. Clear cache
        self.test_endpoint(
            "DELETE",
            "/api/v1/performance/performance/cache",
            None,
            200,
            "Clear system cache"
        )
        
        # Small delay for optimization to take effect
        time.sleep(2)
        
        # 3. Check performance after optimization
        self.test_endpoint(
            "GET",
            "/api/v1/performance/performance/dashboard",
            None,
            200,
            "Check performance after optimization"
        )
        
        self.capture_performance_snapshot("optimization_tests_end")
        
    async def run_request_tracing_tests(self):
        """Test request tracing and monitoring"""
        self.print_section_header("REQUEST TRACING", "🔍")
        
        # Generate a test request to trace
        test_request_id = f"trace-{uuid.uuid4().hex[:12]}"
        
        # Add trace header for the next request
        self.session.headers.update({"X-Request-ID": test_request_id})
        
        # Make a traceable request
        self.test_endpoint(
            "GET",
            "/api/v1/users/me",
            None,
            200,
            "Traceable request for monitoring"
        )
        
        # Small delay for trace processing
        time.sleep(1)
        
        # Try to get trace information
        self.test_endpoint(
            "GET",
            f"/api/v1/monitoring/trace/{test_request_id}",
            None,
            200,
            "Get request trace information"
        )
        
        # Remove trace header
        self.session.headers.pop("X-Request-ID", None)
        
    def analyze_performance_trends(self):
        """Analyze performance trends across snapshots"""
        if len(self.performance_snapshots) < 2:
            return {}
            
        first = self.performance_snapshots[0]
        last = self.performance_snapshots[-1]
        
        try:
            trends = {
                "cpu_change": last["cpu_percent"] - first["cpu_percent"],
                "memory_change": last["memory_info"]["percent"] - first["memory_info"]["percent"],
                "memory_consumed_mb": first["memory_info"]["available_mb"] - last["memory_info"]["available_mb"],
                "duration_seconds": (
                    datetime.fromisoformat(last["timestamp"]) - 
                    datetime.fromisoformat(first["timestamp"])
                ).total_seconds()
            }
            
            return trends
            
        except Exception as e:
            self.log_debug(f"⚠️ Performance trend analysis failed: {e}", level=2)
            return {"error": str(e)}
            
    def print_performance_analysis(self):
        """Print comprehensive performance analysis"""
        self.print_section_header("PERFORMANCE ANALYSIS", "📊")
        
        if not self.performance_snapshots:
            print("⚠️ No performance snapshots collected")
            return
            
        print(f"📈 PERFORMANCE SNAPSHOTS: {len(self.performance_snapshots)}")
        
        # Show baseline vs current
        if self.baseline_metrics and "error" not in self.baseline_metrics:
            current = self.performance_snapshots[-1] if self.performance_snapshots else {}
            
            print(f"\n🎯 BASELINE vs CURRENT:")
            print(f"   CPU: {self.baseline_metrics.get('cpu_percent', 0):.1f}% → {current.get('cpu_percent', 0):.1f}%")
            print(f"   Memory: {self.baseline_metrics.get('memory_percent', 0):.1f}% → {current.get('memory_info', {}).get('percent', 0):.1f}%")
            
        # Analyze trends
        trends = self.analyze_performance_trends()
        if trends and "error" not in trends:
            print(f"\n📊 PERFORMANCE TRENDS:")
            print(f"   Duration: {trends['duration_seconds']:.1f}s")
            print(f"   CPU Change: {trends['cpu_change']:+.1f}%")
            print(f"   Memory Change: {trends['memory_change']:+.1f}%")
            print(f"   Memory Consumed: {trends['memory_consumed_mb']:+.1f}MB")
            
        # Show key snapshots
        print(f"\n📸 KEY SNAPSHOTS:")
        for snapshot in self.performance_snapshots[::max(1, len(self.performance_snapshots)//5)]:  # Show up to 5 snapshots
            print(f"   {snapshot['checkpoint']}: CPU {snapshot['cpu_percent']:.1f}%, Memory {snapshot['memory_info']['percent']:.1f}%")
            
    def print_circuit_breaker_analysis(self):
        """Print circuit breaker state analysis"""
        self.print_section_header("CIRCUIT BREAKER ANALYSIS", "🔌")
        
        if not self.circuit_breaker_states:
            print("⚠️ No circuit breaker states collected")
            return
            
        print(f"📊 CIRCUIT BREAKER STATES: {len(self.circuit_breaker_states)}")
        
        for state in self.circuit_breaker_states:
            print(f"\n🔌 {state['checkpoint'].upper()}:")
            if "states" in state and isinstance(state["states"], dict):
                breakers = state["states"].get("breakers", {})
                for name, info in breakers.items():
                    status = info.get("state", "unknown")
                    print(f"   {name}: {status}")
            else:
                print("   No breaker data available")
                
    def print_system_metrics_summary(self):
        """Print system metrics summary"""
        self.print_section_header("SYSTEM METRICS SUMMARY", "📋")
        
        if not self.system_metrics:
            print("⚠️ No system metrics collected")
            return
            
        total_metrics = len(self.system_metrics)
        successful_metrics = len([m for m in self.system_metrics if m["success"]])
        
        # Response time analysis
        response_times = [m["response_time_ms"] for m in self.system_metrics]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        
        print(f"📊 METRICS SUMMARY:")
        print(f"   Total Metrics: {total_metrics}")
        print(f"   Success Rate: {(successful_metrics/total_metrics*100):.1f}%")
        print(f"   Avg Response Time: {avg_response_time:.0f}ms")
        print(f"   Response Range: {min_response_time:.0f}ms - {max_response_time:.0f}ms")
        
        # Group by endpoint
        endpoints = {}
        for metric in self.system_metrics:
            endpoint = metric["endpoint"]
            if endpoint not in endpoints:
                endpoints[endpoint] = {"count": 0, "total_time": 0, "success": 0}
            endpoints[endpoint]["count"] += 1
            endpoints[endpoint]["total_time"] += metric["response_time_ms"]
            if metric["success"]:
                endpoints[endpoint]["success"] += 1
                
        print(f"\n📈 ENDPOINT PERFORMANCE:")
        for endpoint, stats in endpoints.items():
            avg_time = stats["total_time"] / stats["count"]
            success_rate = (stats["success"] / stats["count"] * 100)
            print(f"   {endpoint}: {avg_time:.0f}ms avg, {success_rate:.1f}% success")
            
    def print_comprehensive_results(self):
        """Print comprehensive admin monitoring test results"""
        self.print_section_header("ADMIN MONITORING TEST RESULTS", "📊")
        
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
        
        # Group by test categories
        categories = {}
        for result in self.test_results:
            endpoint_parts = result["endpoint"].split("/")
            if len(endpoint_parts) > 3:
                category = endpoint_parts[3]  # e.g., "monitoring", "performance", "analytics", "admin"
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
                    
        print(f"\n🎯 Next: Run 'python security_validation.py' to test security features")
        
    async def run_complete_test_suite(self):
        """Execute the complete admin monitoring test suite"""
        start_time = time.time()
        
        print("🖥️ PROMPTFORGE.AI ADMIN MONITORING TEST SUITE")
        print("=" * 80)
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🐛 Debug Level: {self.debug_level}")
        print(f"👤 Test User: {self.test_uid}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Monitoring Scenarios: {len(self.test_scenarios)}")
        
        if self.baseline_metrics and "error" not in self.baseline_metrics:
            print(f"🎯 Baseline: CPU {self.baseline_metrics['cpu_percent']:.1f}%, Memory {self.baseline_metrics['memory_percent']:.1f}%")
            
        # Execute test flows
        await self.run_health_monitoring_tests()
        await self.run_metrics_collection_tests()
        await self.run_circuit_breaker_tests()
        await self.run_admin_diagnostics_tests()
        await self.run_analytics_tests()
        await self.run_performance_optimization_tests()
        await self.run_request_tracing_tests()
        
        # Generate reports
        total_time = time.time() - start_time
        
        self.print_comprehensive_results()
        self.print_performance_analysis()
        self.print_circuit_breaker_analysis()
        self.print_system_metrics_summary()
        
        print(f"\n⏰ Total execution time: {total_time:.1f}s")
        print(f"📊 Performance snapshots: {len(self.performance_snapshots)}")
        print(f"📋 System metrics: {len(self.system_metrics)}")
        print(f"🔌 Circuit breaker states: {len(self.circuit_breaker_states)}")
        
        return self.test_results

async def main():
    """Main execution function"""
    tester = AdminMonitoringTester(debug_level=3)
    results = await tester.run_complete_test_suite()
    return results

if __name__ == "__main__":
    print("🖥️ DEMON ENGINE - Admin Monitoring Test Suite")
    print("=" * 60)
    
    # Run the async test suite
    asyncio.run(main())
