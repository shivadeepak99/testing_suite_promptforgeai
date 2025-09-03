"""
🔍 Endpoint Extractor for Comprehensive Batch Tester
Extracts all endpoints being tested for comparison with Swagger UI docs
"""

import re
import json
from typing import List, Dict, Set

def extract_endpoints_from_tester():
    """Extract all endpoints from the comprehensive batch tester"""
    
    # Read the tester file
    tester_file = "comprehensive_batch_tester.py"
    
    with open(tester_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract endpoints using regex patterns
    endpoints = []
    
    # Pattern 1: Direct endpoint tuples like ("GET", "/api/v1/health", None, 200)
    pattern1 = r'\("(GET|POST|PUT|DELETE)",\s*"([^"]+)"'
    matches1 = re.findall(pattern1, content)
    
    # Pattern 2: self.test_endpoint calls
    pattern2 = r'self\.test_endpoint\s*\(\s*"(GET|POST|PUT|DELETE)",\s*"([^"]+)"'
    matches2 = re.findall(pattern2, content)
    
    # Combine all matches
    all_matches = matches1 + matches2
    
    # Remove duplicates and organize
    unique_endpoints = set()
    for method, endpoint in all_matches:
        # Clean up endpoint paths
        endpoint = endpoint.strip()
        # Remove query parameters for grouping
        base_endpoint = endpoint.split('?')[0]
        unique_endpoints.add((method, base_endpoint))
    
    # Convert to list and sort
    endpoints_list = list(unique_endpoints)
    endpoints_list.sort(key=lambda x: (x[1], x[0]))  # Sort by endpoint, then method
    
    return endpoints_list

def categorize_endpoints(endpoints: List[tuple]) -> Dict[str, List[tuple]]:
    """Categorize endpoints by API section"""
    
    categories = {
        "Health & Debug": [],
        "Users": [],
        "Prompts": [],
        "AI Features": [],
        "Marketplace": [],
        "Search": [],
        "Projects": [],
        "Workflows": [],
        "Analytics": [],
        "Monitoring": [],
        "Performance": [],
        "Intelligence": [],
        "Context": [],
        "Extension": [],
        "Engine Services": [],
        "Vault": [],
        "Ideas": [],
        "Packaging": [],
        "Partnerships": [],
        "Billing": [],
        "Payments": [],
        "Credits": [],
        "Notifications": [],
        "Email": [],
        "Admin": [],
        "Other": []
    }
    
    for method, endpoint in endpoints:
        # Categorize based on endpoint path
        if "/health" in endpoint or "/debug" in endpoint or endpoint == "/":
            categories["Health & Debug"].append((method, endpoint))
        elif "/users" in endpoint:
            categories["Users"].append((method, endpoint))
        elif "/prompts" in endpoint:
            categories["Prompts"].append((method, endpoint))
        elif "/ai/" in endpoint:
            categories["AI Features"].append((method, endpoint))
        elif "/marketplace" in endpoint:
            categories["Marketplace"].append((method, endpoint))
        elif "/search" in endpoint:
            categories["Search"].append((method, endpoint))
        elif "/projects" in endpoint:
            categories["Projects"].append((method, endpoint))
        elif "/workflows" in endpoint:
            categories["Workflows"].append((method, endpoint))
        elif "/analytics" in endpoint:
            categories["Analytics"].append((method, endpoint))
        elif "/monitoring" in endpoint:
            categories["Monitoring"].append((method, endpoint))
        elif "/performance" in endpoint:
            categories["Performance"].append((method, endpoint))
        elif "/intelligence" in endpoint:
            categories["Intelligence"].append((method, endpoint))
        elif "/context" in endpoint:
            categories["Context"].append((method, endpoint))
        elif "/extension" in endpoint:
            categories["Extension"].append((method, endpoint))
        elif "/prompt/" in endpoint or "/demon" in endpoint:
            categories["Engine Services"].append((method, endpoint))
        elif "/vault" in endpoint:
            categories["Vault"].append((method, endpoint))
        elif "/ideas" in endpoint:
            categories["Ideas"].append((method, endpoint))
        elif "/packaging" in endpoint:
            categories["Packaging"].append((method, endpoint))
        elif "/partnerships" in endpoint:
            categories["Partnerships"].append((method, endpoint))
        elif "/billing" in endpoint:
            categories["Billing"].append((method, endpoint))
        elif "/payments" in endpoint:
            categories["Payments"].append((method, endpoint))
        elif "/credits" in endpoint:
            categories["Credits"].append((method, endpoint))
        elif "/notifications" in endpoint:
            categories["Notifications"].append((method, endpoint))
        elif "/emails" in endpoint:
            categories["Email"].append((method, endpoint))
        elif "/admin" in endpoint:
            categories["Admin"].append((method, endpoint))
        else:
            categories["Other"].append((method, endpoint))
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

def generate_endpoint_report():
    """Generate a comprehensive endpoint report"""
    
    print("🔍 EXTRACTING ENDPOINTS FROM COMPREHENSIVE BATCH TESTER")
    print("=" * 80)
    
    # Extract endpoints
    endpoints = extract_endpoints_from_tester()
    
    print(f"📊 Total Unique Endpoints Found: {len(endpoints)}")
    print()
    
    # Categorize endpoints
    categories = categorize_endpoints(endpoints)
    
    # Generate detailed report
    print("📋 ENDPOINTS BY CATEGORY:")
    print("=" * 80)
    
    total_endpoints = 0
    for category, endpoint_list in categories.items():
        print(f"\n🔸 {category} ({len(endpoint_list)} endpoints):")
        print("-" * 60)
        
        for method, endpoint in endpoint_list:
            print(f"   {method:<6} {endpoint}")
        
        total_endpoints += len(endpoint_list)
    
    print(f"\n📊 SUMMARY:")
    print("=" * 80)
    print(f"Total Categories: {len(categories)}")
    print(f"Total Endpoints: {total_endpoints}")
    
    # Generate comparison-friendly lists
    print(f"\n📝 FLAT ENDPOINT LIST (for Swagger comparison):")
    print("=" * 80)
    
    all_endpoints_flat = []
    for method, endpoint in endpoints:
        endpoint_string = f"{method} {endpoint}"
        all_endpoints_flat.append(endpoint_string)
        print(endpoint_string)
    
    # Generate JSON output for easy comparison
    output_data = {
        "total_endpoints": len(endpoints),
        "categories": {},
        "flat_list": all_endpoints_flat,
        "detailed_list": []
    }
    
    for category, endpoint_list in categories.items():
        output_data["categories"][category] = [f"{method} {endpoint}" for method, endpoint in endpoint_list]
    
    for method, endpoint in endpoints:
        output_data["detailed_list"].append({
            "method": method,
            "endpoint": endpoint,
            "full": f"{method} {endpoint}"
        })
    
    # Save to JSON file
    with open("extracted_endpoints.json", "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n💾 Detailed data saved to: extracted_endpoints.json")
    
    # Generate method statistics
    methods_count = {}
    for method, _ in endpoints:
        methods_count[method] = methods_count.get(method, 0) + 1
    
    print(f"\n📊 METHODS BREAKDOWN:")
    print("-" * 40)
    for method, count in sorted(methods_count.items()):
        print(f"{method}: {count} endpoints")
    
    return endpoints, categories

if __name__ == "__main__":
    try:
        endpoints, categories = generate_endpoint_report()
        
        print(f"\n✅ EXTRACTION COMPLETE!")
        print(f"📄 Check 'extracted_endpoints.json' for detailed comparison data")
        print(f"🔍 Ready for Swagger UI comparison!")
        
    except FileNotFoundError:
        print("❌ Error: comprehensive_batch_tester.py not found in current directory")
        print("💡 Make sure you're running this from the test-scripts directory")
    except Exception as e:
        print(f"❌ Error: {e}")
