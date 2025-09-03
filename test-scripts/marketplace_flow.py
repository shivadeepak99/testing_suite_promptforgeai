#!/usr/bin/env python3
"""
🛒 MARKETPLACE FLOW - E-COMMERCE & BILLING COMPREHENSIVE TEST SUITE
Tests marketplace, payments, billing, and credit management with transaction debugging
Validates end-to-end purchase flows and financial integrity
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
from motor.motor_asyncio import AsyncIOMotorClient
import hashlib

class MarketplaceFlowTester:
    def __init__(self, base_url: str = "http://localhost:8000", debug_level: int = 3):
        """
        Initialize the Marketplace Flow Test Suite
        
        Args:
            base_url: API base URL
            debug_level: 1=minimal, 2=standard, 3=detailed, 4=forensic
        """
        self.base_url = base_url
        self.debug_level = debug_level
        self.session = requests.Session()
        self.test_results = []
        self.transaction_logs = []
        self.billing_state_changes = []
        
        # Test data setup
        self.test_uid = f"test-marketplace-{uuid.uuid4().hex[:8]}"
        self.test_prompt_id = f"prompt-{uuid.uuid4().hex[:8]}"
        self.test_listing_id = None
        self.test_payment_id = None
        
        # Financial test data
        self.test_products = self.setup_test_products()
        self.payment_scenarios = self.setup_payment_scenarios()
        
        # Setup environment
        self.setup_debug_environment()
        
    def setup_debug_environment(self):
        """Enable comprehensive debugging for marketplace operations"""
        # Backend debug flags
        os.environ['DEBUG_MARKETPLACE'] = '1'
        os.environ['DEBUG_BILLING'] = '1'
        os.environ['DEBUG_PAYMENTS'] = '1'
        os.environ['DEBUG_CREDITS'] = '1'
        os.environ['DEBUG_TRANSACTIONS'] = '1'
        
        # Session headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'PromptForge-MarketplaceTest/1.0',
            'X-Test-Mode': 'marketplace',
            'Authorization': f'Bearer mock-marketplace-token-{self.test_uid}'
        })
        
    def setup_test_products(self) -> List[Dict]:
        """Define test products for marketplace testing"""
        return [
            {
                "name": "Email Templates Pro",
                "description": "Professional email templates for business communication",
                "price": 9.99,
                "category": "business",
                "tags": ["email", "templates", "professional"],
                "features": ["25 templates", "Customizable", "Industry-specific"]
            },
            {
                "name": "Code Assistant Prompts",
                "description": "Advanced prompts for software development assistance", 
                "price": 19.99,
                "category": "development",
                "tags": ["coding", "development", "ai-assistant"],
                "features": ["50 prompts", "Multiple languages", "Best practices"]
            },
            {
                "name": "Marketing Copy Generator",
                "description": "High-converting marketing copy prompts",
                "price": 14.99,
                "category": "marketing",
                "tags": ["marketing", "copywriting", "conversion"],
                "features": ["30 prompts", "A/B test variations", "ROI focused"]
            }
        ]
        
    def setup_payment_scenarios(self) -> List[Dict]:
        """Define payment testing scenarios"""
        return [
            {
                "name": "razorpay_success",
                "provider": "razorpay",
                "amount": 9.99,
                "currency": "USD",
                "expected_result": "success",
                "webhook_data": {
                    "event": "payment.captured",
                    "entity": "payment",
                    "payload": {
                        "payment": {
                            "entity": {
                                "id": f"pay_{uuid.uuid4().hex[:16]}",
                                "amount": 999,
                                "currency": "USD",
                                "status": "captured"
                            }
                        }
                    }
                }
            },
            {
                "name": "paddle_success", 
                "provider": "paddle",
                "amount": 19.99,
                "currency": "USD",
                "expected_result": "success",
                "webhook_data": {
                    "alert_name": "payment_succeeded",
                    "checkout_id": f"chk_{uuid.uuid4().hex[:16]}",
                    "order_id": f"ord_{uuid.uuid4().hex[:16]}",
                    "sale_gross": "19.99",
                    "currency": "USD"
                }
            },
            {
                "name": "payment_failure",
                "provider": "razorpay", 
                "amount": 14.99,
                "currency": "USD",
                "expected_result": "failure",
                "webhook_data": {
                    "event": "payment.failed",
                    "entity": "payment",
                    "payload": {
                        "payment": {
                            "entity": {
                                "id": f"pay_{uuid.uuid4().hex[:16]}",
                                "amount": 1499,
                                "currency": "USD",
                                "status": "failed",
                                "error_reason": "insufficient_funds"
                            }
                        }
                    }
                }
            }
        ]
        
    def log_debug(self, message: str, level: int = 3, data: Any = None):
        """Structured debug logging"""
        if level <= self.debug_level:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] {message}")
            if data and self.debug_level >= 4:
                print(f"    💰 Data: {json.dumps(data, indent=2, default=str)}")
                
    def log_transaction(self, transaction_type: str, details: Dict):
        """Log financial transactions for audit trail"""
        transaction = {
            "id": f"txn_{uuid.uuid4().hex[:12]}",
            "type": transaction_type,
            "timestamp": datetime.now().isoformat(),
            "user_id": self.test_uid,
            "details": details,
            "test_mode": True
        }
        
        self.transaction_logs.append(transaction)
        
        if self.debug_level >= 3:
            self.log_debug(f"💰 Transaction logged: {transaction_type}", level=3, data=transaction)
            
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     expected_status: int = 200, description: str = "") -> Dict:
        """Execute API test with marketplace-specific logging"""
        test_start = time.time()
        
        try:
            url = f"{self.base_url}{endpoint}"
            self.log_debug(f"🛒 {method} {endpoint} - {description}", level=2)
            
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
            
            # Log transaction if this is a financial operation
            if any(keyword in endpoint.lower() for keyword in ['payment', 'billing', 'purchase', 'checkout']):
                self.log_transaction(f"{method.lower()}_{endpoint.split('/')[-1]}", {
                    "endpoint": endpoint,
                    "request_data": data,
                    "response_code": response.status_code,
                    "response_data": response_data,
                    "success": success
                })
                
            result = {
                "test_id": f"marketplace_{len(self.test_results)+1:03d}",
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
                "test_id": f"marketplace_{len(self.test_results)+1:03d}",
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
        
    async def run_marketplace_listing_tests(self):
        """Test marketplace listing functionality"""
        self.print_section_header("MARKETPLACE LISTING TESTS", "🏪")
        
        # 1. Browse marketplace
        self.test_endpoint(
            "GET",
            "/api/v1/marketplace/listings",
            None,
            200,
            "Get marketplace listings"
        )
        
        # 2. Search marketplace
        self.test_endpoint(
            "GET", 
            "/api/v1/marketplace/search",
            {"q": "email", "limit": 10, "category": "business"},
            200,
            "Search marketplace by keyword and category"
        )
        
        # 3. Create a new listing
        product = self.test_products[0]  # Email Templates Pro
        listing_data = {
            "prompt_id": self.test_prompt_id,
            "title": product["name"],
            "description": product["description"],
            "price": product["price"],
            "category": product["category"],
            "tags": product["tags"],
            "features": product["features"],
            "preview_enabled": True
        }
        
        result = self.test_endpoint(
            "POST",
            "/api/v1/marketplace/list-prompt",
            listing_data,
            200,
            "Create new marketplace listing"
        )
        
        # Extract listing ID for later tests
        if result["success"] and "listing_id" in result["response_data"]:
            self.test_listing_id = result["response_data"]["listing_id"]
            self.log_debug(f"📝 Created listing ID: {self.test_listing_id}", level=2)
            
        # 4. Get my listings
        self.test_endpoint(
            "GET",
            "/api/v1/marketplace/my-listings",
            None,
            200,
            "Get my marketplace listings"
        )
        
        # 5. Preview marketplace item
        if self.test_listing_id:
            self.test_endpoint(
                "GET",
                f"/api/v1/marketplace/preview/{self.test_listing_id}",
                None,
                200,
                "Preview marketplace item"
            )
            
    async def run_billing_tier_tests(self):
        """Test billing tiers and entitlements"""
        self.print_section_header("BILLING TIERS & ENTITLEMENTS", "💳")
        
        # 1. Get available billing tiers
        self.test_endpoint(
            "GET",
            "/api/v1/billing/tiers",
            None,
            200,
            "Get available billing tiers"
        )
        
        # 2. Get current user entitlements
        self.test_endpoint(
            "GET", 
            "/api/v1/billing/me/entitlements",
            None,
            200,
            "Get current user entitlements"
        )
        
        # Log billing state for comparison
        self.billing_state_changes.append({
            "checkpoint": "initial_state",
            "timestamp": datetime.now().isoformat(),
            "user_id": self.test_uid
        })
        
    async def run_payment_initiation_tests(self):
        """Test payment initiation and processing"""
        self.print_section_header("PAYMENT INITIATION", "💰")
        
        # Test payment scenarios
        for scenario in self.payment_scenarios:
            if scenario["expected_result"] == "success":
                # 1. Initiate payment
                payment_data = {
                    "amount": scenario["amount"],
                    "currency": scenario["currency"],
                    "provider": scenario["provider"],
                    "product_id": self.test_listing_id or "test-product-123",
                    "metadata": {
                        "test_scenario": scenario["name"],
                        "user_id": self.test_uid
                    }
                }
                
                result = self.test_endpoint(
                    "POST",
                    "/api/v1/payments/initiate-payment",
                    payment_data,
                    200,
                    f"Initiate {scenario['provider']} payment - {scenario['name']}"
                )
                
                # Extract payment ID for webhook testing
                if result["success"] and "payment_id" in result["response_data"]:
                    self.test_payment_id = result["response_data"]["payment_id"]
                    self.log_debug(f"💳 Payment ID: {self.test_payment_id}", level=2)
                    
                # Small delay between payment initiations
                time.sleep(1)
                
    async def run_webhook_tests(self):
        """Test payment webhook processing"""
        self.print_section_header("PAYMENT WEBHOOKS", "🔗")
        
        # 1. Test webhook health
        self.test_endpoint(
            "GET",
            "/api/v1/payments/webhooks/health",
            None,
            200,
            "Webhook health check"
        )
        
        # 2. Test Razorpay webhook
        razorpay_scenario = next(s for s in self.payment_scenarios if s["provider"] == "razorpay" and s["expected_result"] == "success")
        
        self.test_endpoint(
            "POST",
            "/api/v1/payments/webhooks/payments/webhooks/razorpay",
            razorpay_scenario["webhook_data"],
            200,
            "Process Razorpay webhook - payment success"
        )
        
        # 3. Test Paddle webhook
        paddle_scenario = next(s for s in self.payment_scenarios if s["provider"] == "paddle" and s["expected_result"] == "success")
        
        self.test_endpoint(
            "POST",
            "/api/v1/payments/webhooks/payments/webhooks/paddle",
            paddle_scenario["webhook_data"],
            200,
            "Process Paddle webhook - payment success"
        )
        
        # 4. Test failure webhook
        failure_scenario = next(s for s in self.payment_scenarios if s["expected_result"] == "failure")
        
        self.test_endpoint(
            "POST",
            "/api/v1/payments/webhooks/payments/webhooks/razorpay",
            failure_scenario["webhook_data"],
            200,
            "Process Razorpay webhook - payment failure"
        )
        
    async def run_credit_management_tests(self):
        """Test credit system and management"""
        self.print_section_header("CREDIT MANAGEMENT", "🪙")
        
        # 1. Get credit dashboard
        self.test_endpoint(
            "GET",
            "/api/v1/credits/dashboard",
            None,
            200,
            "Get credit dashboard"
        )
        
        # 2. Get usage history
        self.test_endpoint(
            "GET",
            "/api/v1/credits/usage/history",
            None,
            200,
            "Get credit usage history"
        )
        
        # 3. Get route analytics
        self.test_endpoint(
            "GET",
            "/api/v1/credits/analytics/routes",
            None,
            200,
            "Get credit analytics by route"
        )
        
        # 4. Get usage predictions
        self.test_endpoint(
            "GET", 
            "/api/v1/credits/predictions/usage",
            None,
            200,
            "Get credit usage predictions"
        )
        
        # 5. Admin credit overview (if available)
        self.test_endpoint(
            "GET",
            "/api/v1/credits/admin/overview",
            None,
            200,  # May return 403 if not admin
            "Admin credit overview"
        )
        
    async def run_marketplace_interaction_tests(self):
        """Test marketplace interactions (ratings, reviews, analytics)"""
        self.print_section_header("MARKETPLACE INTERACTIONS", "⭐")
        
        if not self.test_listing_id:
            self.log_debug("⚠️ No listing ID available, using test ID", level=2)
            self.test_listing_id = "test-listing-123"
            
        # 1. Rate a marketplace prompt
        rating_data = {
            "prompt_id": self.test_listing_id,
            "rating": 5,
            "review": "Excellent prompt templates, very helpful for business communication!",
            "would_recommend": True
        }
        
        self.test_endpoint(
            "POST",
            "/api/v1/marketplace/rate",
            rating_data,
            200,
            "Rate marketplace prompt"
        )
        
        # 2. Get marketplace reviews
        self.test_endpoint(
            "GET",
            f"/api/v1/marketplace/{self.test_listing_id}/reviews",
            None,
            200,
            "Get marketplace prompt reviews"
        )
        
        # 3. Get marketplace analytics
        self.test_endpoint(
            "GET",
            f"/api/v1/marketplace/{self.test_listing_id}/analytics",
            None,
            200,
            "Get marketplace prompt analytics"
        )
        
        # 4. Get public prompt details
        self.test_endpoint(
            "GET",
            f"/api/v1/marketplace/{self.test_listing_id}",
            None,
            200,
            "Get public marketplace prompt details"
        )
        
    def print_transaction_summary(self):
        """Print financial transaction summary"""
        self.print_section_header("TRANSACTION AUDIT TRAIL", "💰")
        
        if not self.transaction_logs:
            print("⚠️ No transactions logged")
            return
            
        total_transactions = len(self.transaction_logs)
        successful_transactions = len([t for t in self.transaction_logs if t["details"].get("success", False)])
        
        print(f"📊 TRANSACTION SUMMARY:")
        print(f"   Total Transactions: {total_transactions}")
        print(f"   Successful: {successful_transactions}")
        print(f"   Failed: {total_transactions - successful_transactions}")
        
        # Group by transaction type
        types = {}
        for transaction in self.transaction_logs:
            tx_type = transaction["type"]
            if tx_type not in types:
                types[tx_type] = {"count": 0, "success": 0}
            types[tx_type]["count"] += 1
            if transaction["details"].get("success", False):
                types[tx_type]["success"] += 1
                
        print(f"\n💳 TRANSACTION TYPES:")
        for tx_type, stats in types.items():
            success_rate = (stats["success"] / stats["count"] * 100) if stats["count"] > 0 else 0
            print(f"   {tx_type}: {stats['success']}/{stats['count']} ({success_rate:.1f}%)")
            
        # Show recent transactions
        print(f"\n📋 RECENT TRANSACTIONS:")
        for transaction in self.transaction_logs[-5:]:  # Last 5 transactions
            status = "✅" if transaction["details"].get("success", False) else "❌"
            print(f"   {status} {transaction['type']} - {transaction['timestamp']}")
            
    def print_comprehensive_results(self):
        """Print comprehensive marketplace test results"""
        self.print_section_header("MARKETPLACE TEST RESULTS", "📊")
        
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
            category = endpoint_parts[3] if len(endpoint_parts) > 3 else "unknown"  # e.g., "marketplace", "payments", "billing"
            
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
                    
        print(f"\n🎯 Next: Run 'python developer_tools.py' to test extension features")
        
    async def run_complete_test_suite(self):
        """Execute the complete marketplace flow test suite"""
        start_time = time.time()
        
        print("🛒 PROMPTFORGE.AI MARKETPLACE FLOW TEST SUITE")
        print("=" * 80)
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🐛 Debug Level: {self.debug_level}")
        print(f"👤 Test User: {self.test_uid}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🛍️ Test Products: {len(self.test_products)}")
        print(f"💳 Payment Scenarios: {len(self.payment_scenarios)}")
        
        # Execute test flows
        await self.run_billing_tier_tests()
        await self.run_marketplace_listing_tests()
        await self.run_payment_initiation_tests()
        await self.run_webhook_tests()
        await self.run_credit_management_tests()
        await self.run_marketplace_interaction_tests()
        
        # Generate reports
        total_time = time.time() - start_time
        
        self.print_comprehensive_results()
        self.print_transaction_summary()
        
        print(f"\n⏰ Total execution time: {total_time:.1f}s")
        print(f"💰 Transactions logged: {len(self.transaction_logs)}")
        print(f"📋 Billing state changes: {len(self.billing_state_changes)}")
        
        return self.test_results

async def main():
    """Main execution function"""
    tester = MarketplaceFlowTester(debug_level=3)
    results = await tester.run_complete_test_suite()
    return results

if __name__ == "__main__":
    print("🛒 DEMON ENGINE - Marketplace Flow Test Suite")
    print("=" * 60)
    
    # Run the async test suite
    asyncio.run(main())
