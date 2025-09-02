#!/usr/bin/env python3
"""
🔧 PromptForge API-Database Sync Fix Generator
Generates exact backend code fixes based on database analysis
"""

import json
from datetime import datetime

class APIFixGenerator:
    def __init__(self):
        self.fixes = []
        
    def generate_prompt_model_fix(self):
        """Generate fixed Pydantic model for Prompts"""
        fix = {
            "file": "backend/models/prompt.py",
            "issue": "API expects 'body' field that doesn't exist in database",
            "current_code": """
class PromptCreate(BaseModel):
    body: str  # ❌ This field doesn't exist in database
    title: str
    content: str
            """,
            "fixed_code": """
class PromptCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    content: str  # This is the actual content field from database
    role: Optional[str] = ""
    category: str = "general"
    tags: List[str] = []
    difficulty: str = "beginner"
    type: str = "text"
    visibility: str = "private"
    is_template: bool = False
    is_featured: bool = False
    # Database also has: performance, analytics, collaboration objects
            """,
            "severity": "CRITICAL",
            "test_fix": "This will fix the 422 error on POST /api/v1/prompts/prompts/"
        }
        self.fixes.append(fix)
        
    def generate_idea_model_fix(self):
        """Generate fixed Pydantic model for Ideas"""
        fix = {
            "file": "backend/models/idea.py", 
            "issue": "API expects 'complexity' field that doesn't exist in database",
            "current_code": """
class IdeaGenerate(BaseModel):
    complexity: str  # ❌ This field doesn't exist in database
    prompt: str
            """,
            "fixed_code": """
class IdeaGenerate(BaseModel):
    prompt: str
    categories: List[str]
    count: Optional[int] = 3
    tags: Optional[List[str]] = []
    # Database has quality_score, feasibility, estimated_time_to_market
    # Don't require complexity - it's not in the schema
            """,
            "severity": "CRITICAL", 
            "test_fix": "This will fix the 422 error on POST /api/v1/ideas/generate"
        }
        self.fixes.append(fix)
        
    def generate_user_response_fix(self):
        """Generate fixed User response model"""
        fix = {
            "file": "backend/models/user.py",
            "issue": "API returns camelCase but database uses snake_case",
            "current_code": """
class UserResponse(BaseModel):
    displayName: str  # ❌ Database has display_name
    emailVerified: bool  # ❌ Database has email_verified
    accountStatus: str  # ❌ Database has account_status
            """,
            "fixed_code": """
# Option A: Make API use snake_case (Recommended)
class UserResponse(BaseModel):
    uid: str
    email: str
    display_name: str  # Matches database field
    email_verified: bool  # Matches database field
    account_status: str  # Matches database field
    last_active_at: Optional[datetime]
    login_seq: int
    version: int
    
    class Config:
        # This will automatically convert database snake_case to API snake_case
        orm_mode = True

# Option B: Keep camelCase but add field mapping
class UserResponse(BaseModel):
    uid: str
    email: str
    displayName: str = Field(alias="display_name")
    emailVerified: bool = Field(alias="email_verified") 
    accountStatus: str = Field(alias="account_status")
    lastActiveAt: Optional[datetime] = Field(alias="last_active_at")
    loginSeq: int = Field(alias="login_seq")
    version: int
    
    class Config:
        allow_population_by_field_name = True
            """,
            "severity": "HIGH",
            "test_fix": "This will fix schema mismatches in user endpoints"
        }
        self.fixes.append(fix)
        
    def generate_missing_endpoints_fix(self):
        """Generate fixes for missing endpoints"""
        fix = {
            "file": "backend/routers/users.py",
            "issue": "Missing entitlements endpoint",
            "current_code": "# Endpoint /api/v1/users/me/entitlements returns 404",
            "fixed_code": """
@router.get("/me/entitlements")
async def get_user_entitlements(current_user: User = Depends(get_current_user)):
    '''Get user entitlements/permissions'''
    # Based on database analysis, this should return user permissions
    return {
        "plan": current_user.account_status,
        "features": [], # Add actual features based on plan
        "limits": {
            "prompts_per_month": 100,  # Based on plan
            "ideas_per_month": 50
        }
    }
            """,
            "severity": "MEDIUM",
            "test_fix": "This will fix the 404 error on GET /api/v1/users/me/entitlements"
        }
        
        fix2 = {
            "file": "backend/routers/notifications.py",
            "issue": "Missing notifications list endpoint", 
            "current_code": "# Endpoint /api/v1/notifications/ returns 404",
            "fixed_code": """
@router.get("/")
async def get_notifications(current_user: User = Depends(get_current_user)):
    '''Get user notifications'''
    # This endpoint is referenced but doesn't exist
    return {
        "notifications": [],
        "unread_count": 0
    }
            """,
            "severity": "MEDIUM",
            "test_fix": "This will fix the 404 error on GET /api/v1/notifications/"
        }
        
        self.fixes.extend([fix, fix2])
        
    def generate_all_fixes(self):
        """Generate all required fixes"""
        print("🔧 Generating API-Database sync fixes...")
        
        self.generate_prompt_model_fix()
        self.generate_idea_model_fix() 
        self.generate_user_response_fix()
        self.generate_missing_endpoints_fix()
        
        return self.fixes
        
    def save_fixes_to_file(self):
        """Save all fixes to a JSON file"""
        fixes = self.generate_all_fixes()
        
        output = {
            "generated_at": datetime.now().isoformat(),
            "total_fixes": len(fixes),
            "summary": {
                "critical_fixes": len([f for f in fixes if f["severity"] == "CRITICAL"]),
                "high_priority": len([f for f in fixes if f["severity"] == "HIGH"]),
                "medium_priority": len([f for f in fixes if f["severity"] == "MEDIUM"])
            },
            "fixes": fixes
        }
        
        filename = f"results/api_fixes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
            
        print(f"✅ Generated {len(fixes)} fixes saved to: {filename}")
        return filename

def print_priority_fixes():
    """Print the most critical fixes that need immediate attention"""
    print("\n🚨 CRITICAL FIXES NEEDED IMMEDIATELY:")
    print("="*60)
    
    print("\n1. 🔴 Fix Prompts API Schema")
    print("   File: backend/models/prompt.py")
    print("   Issue: Remove 'body' field requirement, add 'description' and 'role'")
    print("   Impact: Fixes 422 error on POST /api/v1/prompts/prompts/")
    
    print("\n2. 🔴 Fix Ideas API Schema") 
    print("   File: backend/models/idea.py")
    print("   Issue: Remove 'complexity' field requirement")
    print("   Impact: Fixes 422 error on POST /api/v1/ideas/generate")
    
    print("\n3. 🟡 Fix Field Naming Consistency")
    print("   File: backend/models/user.py")
    print("   Issue: API returns camelCase, database uses snake_case")
    print("   Impact: Fixes schema validation mismatches")
    
    print("\n4. 🟡 Add Missing Endpoints")
    print("   Files: backend/routers/users.py, backend/routers/notifications.py")
    print("   Issue: entitlements and notifications endpoints return 404")
    print("   Impact: Fixes API completeness")
    
    print("\n💡 After applying these fixes, re-run:")
    print("   python test-scripts/database_synced_comprehensive_tests.py")
    print("\n🎯 Target: 90%+ API success rate, 85%+ schema match rate")

if __name__ == "__main__":
    generator = APIFixGenerator()
    
    # Print immediate priority fixes
    print_priority_fixes()
    
    # Generate detailed fix file
    fix_file = generator.save_fixes_to_file()
    
    print(f"\n📋 Detailed fixes saved to: {fix_file}")
    print("\n🔧 Apply these fixes to synchronize your API with the database!")
