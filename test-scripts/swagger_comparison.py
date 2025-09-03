"""
🔍 Swagger UI vs Comprehensive Batch Tester Comparison
Analyzes differences between Swagger documentation and current test coverage
"""

import json
from typing import Dict, List, Set, Tuple

def get_swagger_endpoints():
    """Define all endpoints from Swagger UI documentation"""
    
    swagger_endpoints = {
        "Debug": [
            ("GET", "/api/v1/debug/auth-headers", "Debug Auth Headers"),
            ("POST", "/api/v1/debug/test-auth", "Test Auth With Mock"),
        ],
        
        "Prompts": [
            ("GET", "/api/v1/prompts/arsenal", "Get User Arsenal"),
            ("POST", "/api/v1/prompts/", "Create New Prompt"),
            ("POST", "/api/v1/prompts/test-drive-by-id", "Test Drive Prompt By Id"),
            ("GET", "/api/v1/prompts/public", "Get Public Prompts"),
            ("GET", "/api/v1/prompts/{prompt_id}", "Get Prompt Details"),
            ("DELETE", "/api/v1/prompts/{prompt_id}", "Delete Prompt"),
            ("PUT", "/api/v1/prompts/{prompt_id}", "Update Prompt"),
            ("GET", "/api/v1/prompts/{prompt_id}/versions", "Get Prompt Versions"),
            ("POST", "/api/v1/prompts/bulk-action", "Bulk Prompt Action"),
        ],
        
        "AI Features": [
            ("POST", "/api/v1/ai/remix-prompt", "Remix Prompt"),
            ("POST", "/api/v1/ai/architect-prompt", "Architect Prompt"),
            ("POST", "/api/v1/ai/fuse-prompts", "Fuse Prompts"),
            ("POST", "/api/v1/ai/generate-enhanced-prompt", "Generate Enhanced Prompt"),
            ("POST", "/api/v1/ai/analyze-prompt", "Analyze Prompt"),
        ],
        
        "Marketplace": [
            ("GET", "/api/v1/marketplace/search", "Search Marketplace"),
            ("GET", "/api/v1/marketplace/my-listings", "Get My Marketplace Listings"),
            ("GET", "/api/v1/marketplace/{id}", "Get Public Prompt Details"),
            ("POST", "/api/v1/marketplace/list-prompt", "List Prompt In Marketplace"),
            ("GET", "/api/v1/marketplace/listings", "Get Marketplace Listings"),
            ("GET", "/api/v1/marketplace/preview/{prompt_id}", "Preview Marketplace Item"),
            ("POST", "/api/v1/marketplace/rate", "Rate Marketplace Prompt"),
            ("GET", "/api/v1/marketplace/{prompt_id}/reviews", "List Marketplace Reviews"),
            ("GET", "/api/v1/marketplace/{prompt_id}/analytics", "Get Marketplace Prompt Analytics"),
        ],
        
        "Users": [
            ("PUT", "/api/v1/users/me/profile", "Update Profile"),
            ("POST", "/api/v1/users/auth/complete", "Auth Complete"),
            ("GET", "/api/v1/users/me", "Get Me"),
            ("GET", "/api/v1/users/credits", "Get User Credits"),
            ("GET", "/api/v1/users/export-data", "Export User Data"),
            ("DELETE", "/api/v1/users/account", "Delete User Account"),
            ("GET", "/api/v1/users/preferences", "Get User Preferences"),
            ("PUT", "/api/v1/users/preferences", "Update User Preferences"),
            ("GET", "/api/v1/users/stats", "Get User Stats"),
            ("GET", "/api/v1/users/me/usage", "Get My Usage"),
            ("POST", "/api/v1/users/usage/track", "Track Usage Event"),
        ],
        
        "Packaging": [
            ("POST", "/api/v1/packaging/{prompt_id}/package", "Package Prompt For Marketplace"),
            ("GET", "/api/v1/packaging/debug", "Debug Packaging"),
            ("GET", "/api/v1/packaging/", "List User Packages"),
            ("POST", "/api/v1/packaging/manage-bulk", "Manage Packages Bulk"),
            ("GET", "/api/v1/packaging/analytics", "Get Package Analytics"),
        ],
        
        "Partnerships": [
            ("POST", "/api/v1/partnerships/request", "Request Partnership Enhanced"),
            ("POST", "/api/v1/partnerships/revenue", "Manage Partner Revenue"),
            ("GET", "/api/v1/partnerships/dashboard", "Get Partner Dashboard"),
        ],
        
        "Analytics": [
            ("POST", "/api/v1/analytics/events", "Log Analytics Events"),
            ("POST", "/api/v1/analytics/performance", "Log Performance Metrics"),
            ("GET", "/api/v1/analytics/dashboard", "Get Analytics Dashboard"),
            ("POST", "/api/v1/analytics/exports/prompts", "Export Prompts Data"),
            ("POST", "/api/v1/analytics/exports/analytics", "Export Analytics Data"),
            ("POST", "/api/v1/analytics/jobs/analytics", "Create Analytics Job"),
            ("GET", "/api/v1/analytics/jobs/analytics/{job_id}/status", "Get Analytics Job Status"),
        ],
        
        "Projects": [
            ("GET", "/api/v1/projects/{project_id}", "Get Project Details"),
            ("DELETE", "/api/v1/projects/{project_id}", "Delete Project"),
            ("GET", "/api/v1/projects/{project_id}/prompts", "Get Project Prompts"),
            ("POST", "/api/v1/projects/{project_id}/prompts", "Manage Project Prompts"),
        ],
        
        "Notifications": [
            ("GET", "/api/v1/notifications/preferences", "Get Notification Preferences"),
            ("PUT", "/api/v1/notifications/preferences", "Update Notification Preferences"),
            ("GET", "/api/v1/notifications/", "Get User Notifications"),
            ("POST", "/api/v1/notifications/", "Create Notification"),
            ("PUT", "/api/v1/notifications/{notification_id}/read", "Mark Notification Read"),
            ("POST", "/api/v1/notifications/mark-all-read", "Mark All Notifications Read"),
            ("POST", "/api/v1/notifications/bulk", "Create Bulk Notifications"),
            ("DELETE", "/api/v1/notifications/{notification_id}", "Delete Notification"),
            ("POST", "/api/v1/notifications/push", "Send Push Notification Endpoint"),
            ("GET", "/api/v1/notifications/analytics", "Get Notification Analytics"),
        ],
        
        "Email Automation": [
            ("POST", "/api/v1/emails/send-welcome-sequence", "Send Welcome Sequence"),
            ("POST", "/api/v1/emails/send-retention-campaign", "Send Retention Campaign"),
            ("POST", "/api/v1/emails/send-milestone-celebration", "Send Milestone Celebration"),
            ("GET", "/api/v1/emails/user-preferences", "Get Email Preferences"),
            ("PUT", "/api/v1/emails/user-preferences", "Update Email Preferences"),
            ("POST", "/api/v1/emails/unsubscribe", "Unsubscribe From Emails"),
            ("GET", "/api/v1/emails/templates", "Get Email Templates"),
            ("POST", "/api/v1/emails/templates", "Create Email Template"),
            ("POST", "/api/v1/emails/automation/trigger-credit-warning", "Trigger Credit Warning"),
            ("POST", "/api/v1/emails/automation/trigger-billing-reminder", "Trigger Billing Reminder"),
            ("POST", "/api/v1/emails/automation/trigger-feature-announcement", "Trigger Feature Announcement"),
        ],
        
        "Billing": [
            ("GET", "/api/v1/billing/tiers", "Get Billing Tiers"),
            ("GET", "/api/v1/billing/me/entitlements", "Get Me Entitlements"),
        ],
        
        "Payments": [
            ("POST", "/api/v1/payments/initiate-payment", "Initiate Payment"),
        ],
        
        "Webhooks": [
            ("GET", "/api/v1/payments/webhooks/health", "Health"),
            ("POST", "/api/v1/payments/webhooks/paddle", "Paddle Webhook"),
            ("POST", "/api/v1/payments/webhooks/razorpay", "Razorpay Webhook"),
        ],
        
        "Search": [
            ("GET", "/api/v1/search/users", "Search Users"),
            ("GET", "/api/v1/search/", "Global Search"),
        ],
        
        "Prompt Engine": [
            ("POST", "/api/v1/prompt/quick_upgrade", "Quick Mode: Upgrade prompt (extension, low-latency)"),
            ("POST", "/api/v1/prompt/upgrade", "Full Mode: Upgrade prompt (deep pipeline, Pro)"),
        ],
        
        "Demon Engine": [
            ("POST", "/api/v1/demon/route", "Route"),
            ("POST", "/api/v1/demon/v2/upgrade", "Upgrade V2"),
        ],
        
        "Prompt Vault": [
            ("GET", "/api/v1/vault/arsenal", "Get Arsenal"),
            ("GET", "/api/v1/vault/search", "Search Prompts"),
            ("POST", "/api/v1/vault/{prompt_id}/test-drive", "Test Drive Prompt"),
            ("POST", "/api/v1/vault/save", "Save Prompt"),
            ("GET", "/api/v1/vault/list", "List Prompts"),
            ("GET", "/api/v1/vault/{prompt_id}/versions", "Get Prompt Versions"),
            ("DELETE", "/api/v1/vault/delete/{prompt_id}", "Delete Prompt"),
        ],
        
        "Ideas": [
            ("POST", "/api/v1/ideas/generate", "Generate Ideas"),
        ],
        
        "Admin": [
            ("GET", "/api/v1/admin/diagnostics", "Diagnostics"),
        ],
        
        "Monitoring": [
            ("GET", "/api/v1/monitoring/health", "Health Check"),
            ("GET", "/api/v1/monitoring/health/detailed", "Detailed Health Check"),
            ("GET", "/api/v1/monitoring/metrics", "Get Metrics"),
            ("GET", "/api/v1/monitoring/trace/{request_id}", "Get Request Trace"),
            ("GET", "/api/v1/monitoring/circuit-breakers", "Get Circuit Breaker Status"),
            ("POST", "/api/v1/monitoring/circuit-breakers/{breaker_name}/reset", "Reset Circuit Breaker"),
        ],
        
        "Credit Management": [
            ("GET", "/api/v1/credits/dashboard", "Get Credit Dashboard"),
            ("GET", "/api/v1/credits/usage/history", "Get Usage History"),
            ("GET", "/api/v1/credits/analytics/routes", "Get Route Analytics"),
            ("GET", "/api/v1/credits/predictions/usage", "Predict Usage"),
            ("GET", "/api/v1/credits/admin/overview", "Admin Credit Overview"),
        ],
        
        "Performance": [
            ("GET", "/api/v1/performance/dashboard", "Get Performance Dashboard"),
            ("GET", "/api/v1/performance/slow-queries", "Get Slow Queries"),
            ("GET", "/api/v1/performance/cache-stats", "Get Cache Statistics"),
            ("POST", "/api/v1/performance/optimize", "Trigger Optimization"),
            ("DELETE", "/api/v1/performance/cache", "Clear Cache"),
            ("GET", "/api/v1/performance/health", "Performance Health Check"),
        ],
        
        "Prompt Intelligence": [
            ("POST", "/api/v1/intelligence/analyze", "Analyze Prompt"),
            ("GET", "/api/v1/intelligence/suggestions/quick", "Get Quick Suggestions"),
            ("GET", "/api/v1/intelligence/templates/personalized", "Get Personalized Templates"),
            ("GET", "/api/v1/intelligence/patterns/user", "Get User Patterns"),
            ("POST", "/api/v1/intelligence/feedback", "Submit Suggestion Feedback"),
            ("GET", "/api/v1/intelligence/analytics/intelligence", "Get Intelligence Analytics"),
        ],
        
        "Context Intelligence": [
            ("POST", "/api/v1/context/analyze", "Analyze Context"),
            ("POST", "/api/v1/context/quick-suggestions", "Get Quick Context Suggestions"),
            ("POST", "/api/v1/context/follow-up-questions", "Generate Follow Up Questions"),
            ("GET", "/api/v1/context/enhancement-templates", "Get Enhancement Templates"),
            ("GET", "/api/v1/context/domain-insights", "Get Domain Insights"),
        ],
        
        "Extension Intelligence": [
            ("POST", "/api/v1/extension/analyze-prompt", "Analyze Extension Prompt"),
            ("POST", "/api/v1/extension/suggestions/contextual", "Get Contextual Suggestions"),
            ("POST", "/api/v1/extension/enhance/selected-text", "Enhance Selected Text"),
            ("POST", "/api/v1/extension/templates/smart", "Get Smart Templates"),
            ("GET", "/api/v1/extension/health", "Extension Health Check"),
            ("GET", "/api/v1/extension/usage-stats", "Get Extension Usage Stats"),
        ],
        
        "Smart Workflows": [
            ("GET", "/api/v1/workflows/templates", "Get Workflow Templates"),
            ("POST", "/api/v1/workflows/templates", "Create Workflow Template"),
            ("GET", "/api/v1/workflows/templates/{template_id}", "Get Workflow Template"),
            ("POST", "/api/v1/workflows/start", "Start Workflow"),
            ("GET", "/api/v1/workflows/status/{instance_id}", "Get Workflow Status"),
            ("GET", "/api/v1/workflows/results/{instance_id}", "Get Workflow Results"),
            ("POST", "/api/v1/workflows/control/{instance_id}/pause", "Pause Workflow"),
            ("POST", "/api/v1/workflows/control/{instance_id}/resume", "Resume Workflow"),
            ("POST", "/api/v1/workflows/control/{instance_id}/cancel", "Cancel Workflow"),
            ("GET", "/api/v1/workflows/my-workflows", "List User Workflows"),
            ("POST", "/api/v1/workflows/quick-start/content-creation", "Quick Start Content Creation"),
            ("POST", "/api/v1/workflows/quick-start/code-review", "Quick Start Code Review"),
            ("GET", "/api/v1/workflows/analytics/usage", "Get Workflow Analytics"),
            ("GET", "/api/v1/workflows/health", "Workflow Service Health"),
        ],
        
        "Default": [
            ("GET", "/", "Root"),
            ("GET", "/health", "Health"),
            ("GET", "/api/v1/health", "Health V1"),
            ("POST", "/analytics/events", "Analytics Events Fallback"),
            ("POST", "//analytics/events", "Analytics Events Double Slash Fix"),
        ],
    }
    
    return swagger_endpoints

def load_tester_endpoints():
    """Load endpoints from the extracted JSON file"""
    try:
        with open("extracted_endpoints.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("❌ extracted_endpoints.json not found. Run endpoint_extractor.py first.")
        return None

def normalize_endpoint(endpoint: str) -> str:
    """Normalize endpoint paths for comparison"""
    # Replace specific IDs with placeholders for comparison
    import re
    
    # Common ID patterns
    patterns = [
        (r'/test-project-123', '/{project_id}'),
        (r'/test-prompt-123', '/{prompt_id}'),
        (r'/test-123', '/{id}'),
        (r'/test-vault-123', '/{prompt_id}'),
        (r'/test-notification-123', '/{notification_id}'),
        (r'/test-job-123', '/{job_id}'),
        (r'/test-instance-123', '/{instance_id}'),
        (r'/test-template-123', '/{template_id}'),
        (r'/test-breaker', '/{breaker_name}'),
        (r'/test-request-123', '/{request_id}'),
    ]
    
    normalized = endpoint
    for pattern, replacement in patterns:
        normalized = re.sub(pattern, replacement, normalized)
    
    return normalized

def compare_endpoints():
    """Compare Swagger endpoints with tester endpoints"""
    
    print("🔍 SWAGGER UI vs COMPREHENSIVE BATCH TESTER COMPARISON")
    print("=" * 80)
    
    # Load data
    swagger_endpoints = get_swagger_endpoints()
    tester_data = load_tester_endpoints()
    
    if not tester_data:
        return
    
    # Create sets for comparison
    swagger_set = set()
    swagger_details = {}
    
    # Process Swagger endpoints
    total_swagger = 0
    for category, endpoints in swagger_endpoints.items():
        for method, endpoint, description in endpoints:
            normalized_endpoint = normalize_endpoint(endpoint)
            key = f"{method} {normalized_endpoint}"
            swagger_set.add(key)
            swagger_details[key] = {
                "category": category,
                "original_endpoint": endpoint,
                "description": description
            }
            total_swagger += 1
    
    # Process tester endpoints
    tester_set = set()
    for endpoint_str in tester_data["flat_list"]:
        method, endpoint = endpoint_str.split(" ", 1)
        normalized_endpoint = normalize_endpoint(endpoint)
        key = f"{method} {normalized_endpoint}"
        tester_set.add(key)
    
    # Find differences
    missing_in_tester = swagger_set - tester_set
    extra_in_tester = tester_set - swagger_set
    common_endpoints = swagger_set & tester_set
    
    print(f"📊 COMPARISON SUMMARY:")
    print("=" * 80)
    print(f"🔸 Total Swagger Endpoints: {total_swagger}")
    print(f"🔸 Total Tester Endpoints: {len(tester_data['flat_list'])}")
    print(f"🔸 Common Endpoints: {len(common_endpoints)}")
    print(f"🔸 Missing in Tester: {len(missing_in_tester)}")
    print(f"🔸 Extra in Tester: {len(extra_in_tester)}")
    print(f"🔸 Coverage: {len(common_endpoints)/total_swagger*100:.1f}%")
    
    # Detailed analysis
    if missing_in_tester:
        print(f"\n❌ MISSING IN TESTER ({len(missing_in_tester)} endpoints):")
        print("=" * 80)
        
        # Group by category
        missing_by_category = {}
        for endpoint in missing_in_tester:
            if endpoint in swagger_details:
                category = swagger_details[endpoint]["category"]
                if category not in missing_by_category:
                    missing_by_category[category] = []
                missing_by_category[category].append(endpoint)
        
        for category, endpoints in missing_by_category.items():
            print(f"\n🔸 {category} ({len(endpoints)} missing):")
            print("-" * 60)
            for endpoint in sorted(endpoints):
                if endpoint in swagger_details:
                    original = swagger_details[endpoint]["original_endpoint"]
                    desc = swagger_details[endpoint]["description"]
                    print(f"   {endpoint}")
                    print(f"      Original: {endpoint.split(' ')[0]} {original}")
                    print(f"      Description: {desc}")
    
    if extra_in_tester:
        print(f"\n➕ EXTRA IN TESTER ({len(extra_in_tester)} endpoints):")
        print("=" * 80)
        for endpoint in sorted(extra_in_tester):
            print(f"   {endpoint}")
    
    # Generate missing endpoints for easy addition
    if missing_in_tester:
        print(f"\n📝 MISSING ENDPOINTS FOR BATCH ADDITION:")
        print("=" * 80)
        
        batch_additions = {}
        for endpoint in missing_in_tester:
            if endpoint in swagger_details:
                category = swagger_details[endpoint]["category"]
                if category not in batch_additions:
                    batch_additions[category] = []
                
                method, norm_endpoint = endpoint.split(" ", 1)
                original = swagger_details[endpoint]["original_endpoint"]
                desc = swagger_details[endpoint]["description"]
                
                # Generate test tuple
                test_tuple = f'("{method}", "{original}", None, 200)  # {desc}'
                batch_additions[category].append(test_tuple)
        
        for category, additions in batch_additions.items():
            print(f"\n# {category} - Missing Endpoints:")
            print("# " + "-" * 50)
            for addition in additions:
                print(f"            {addition}")
    
    # Save detailed comparison
    comparison_data = {
        "summary": {
            "total_swagger": total_swagger,
            "total_tester": len(tester_data["flat_list"]),
            "common": len(common_endpoints),
            "missing_in_tester": len(missing_in_tester),
            "extra_in_tester": len(extra_in_tester),
            "coverage_percentage": len(common_endpoints)/total_swagger*100
        },
        "missing_in_tester": {
            "count": len(missing_in_tester),
            "endpoints": list(missing_in_tester),
            "by_category": missing_by_category if missing_in_tester else {}
        },
        "extra_in_tester": {
            "count": len(extra_in_tester),
            "endpoints": list(extra_in_tester)
        },
        "common_endpoints": list(common_endpoints)
    }
    
    with open("swagger_comparison_results.json", "w") as f:
        json.dump(comparison_data, f, indent=2)
    
    print(f"\n💾 Detailed comparison saved to: swagger_comparison_results.json")
    
    return comparison_data

if __name__ == "__main__":
    try:
        results = compare_endpoints()
        print(f"\n✅ COMPARISON COMPLETE!")
        print(f"📊 Check the detailed analysis above and 'swagger_comparison_results.json'")
        
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
