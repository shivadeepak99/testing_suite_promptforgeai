"""
🔍 Extract endpoints from ENDPOINT_CLEANUP_ANALYSIS.md
Parse the markdown file to get exact endpoints to test
"""

import re
from typing import List, Tuple, Dict

def extract_endpoints_from_analysis():
    """Extract all endpoints from the ENDPOINT_CLEANUP_ANALYSIS.md file"""
    
    # Read the analysis file
    analysis_file = "../ENDPOINT_CLEANUP_ANALYSIS.md"
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match endpoint definitions like:
    # #### `/api/v1/prompts/arsenal` - GET
    pattern = r'####\s+`([^`]+)`\s+-\s+(GET|POST|PUT|DELETE)'
    
    matches = re.findall(pattern, content)
    
    endpoints = []
    for endpoint, method in matches:
        # Clean up endpoint path
        endpoint = endpoint.strip()
        endpoints.append((method, endpoint))
    
    return endpoints

def categorize_endpoints_from_analysis(endpoints: List[Tuple[str, str]]) -> Dict[str, List[Tuple[str, str]]]:
    """Categorize endpoints based on the analysis file structure"""
    
    categories = {
        "Prompts Core": [],
        "Prompt Engine": [],
        "Brain Engine": [],
        "Demon Engine": [],
        "AI Features": [],
        "Marketplace": [],
        "Users": [],
        "Packaging": [],
        "Partnerships": [],
        "Analytics": [],
        "Projects": [],
        "Notifications": [],
        "Email Automation": [],
        "Other": []
    }
    
    for method, endpoint in endpoints:
        if "/prompts/" in endpoint or endpoint.endswith("/prompts"):
            categories["Prompts Core"].append((method, endpoint))
        elif "/prompt/" in endpoint:
            categories["Prompt Engine"].append((method, endpoint))
        elif "/demon/" in endpoint:
            categories["Demon Engine"].append((method, endpoint))
        elif "/ai/" in endpoint:
            categories["AI Features"].append((method, endpoint))
        elif "/marketplace/" in endpoint:
            categories["Marketplace"].append((method, endpoint))
        elif "/users/" in endpoint:
            categories["Users"].append((method, endpoint))
        elif "/packaging/" in endpoint:
            categories["Packaging"].append((method, endpoint))
        elif "/partnerships/" in endpoint:
            categories["Partnerships"].append((method, endpoint))
        elif "/analytics/" in endpoint:
            categories["Analytics"].append((method, endpoint))
        elif "/projects/" in endpoint:
            categories["Projects"].append((method, endpoint))
        elif "/notifications/" in endpoint:
            categories["Notifications"].append((method, endpoint))
        elif "/emails/" in endpoint:
            categories["Email Automation"].append((method, endpoint))
        else:
            categories["Other"].append((method, endpoint))
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

def generate_test_batches():
    """Generate test batches from analysis file"""
    
    print("🔍 EXTRACTING ENDPOINTS FROM ENDPOINT_CLEANUP_ANALYSIS.md")
    print("=" * 80)
    
    endpoints = extract_endpoints_from_analysis()
    print(f"📊 Total Endpoints Found: {len(endpoints)}")
    
    categories = categorize_endpoints_from_analysis(endpoints)
    
    print(f"\n📋 ENDPOINTS BY CATEGORY:")
    print("=" * 80)
    
    for category, endpoint_list in categories.items():
        print(f"\n🔸 {category} ({len(endpoint_list)} endpoints):")
        print("-" * 60)
        
        for method, endpoint in endpoint_list:
            print(f"   {method:<6} {endpoint}")
    
    return categories

if __name__ == "__main__":
    categories = generate_test_batches()
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"📄 Ready to update comprehensive_batch_tester.py")
