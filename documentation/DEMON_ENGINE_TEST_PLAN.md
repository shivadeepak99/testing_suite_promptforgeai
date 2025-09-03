# 🧠 **DEMON ENGINE COMPREHENSIVE TEST IMPLEMENTATION PLAN**

**Date**: September 2, 2025  
**System**: PromptForge.ai Demon Engine & Brain Engine Testing Suite  
**Purpose**: Production-ready testing with internal workflow debugging  

---

## 🎯 **TESTING STRATEGY OVERVIEW**

### **Test Categories & Priority**

| **Test Script** | **Purpose** | **Endpoints Covered** | **Priority** |
|-----------------|-------------|----------------------|--------------|
| `user_onboarding.py` | Complete user lifecycle testing | Auth, Profile, Credits, Preferences | 🔴 Critical |
| `features_test.py` | Core AI features with debugging | Brain/Demon Engine, AI Features | 🔴 Critical |
| `marketplace_flow.py` | E-commerce functionality | Marketplace, Billing, Payments | 🟡 High |
| `developer_tools.py` | Extension & developer features | VSCode, Chrome, Extension APIs | 🟡 High |
| `admin_monitoring.py` | System health & performance | Admin, Monitoring, Analytics | 🟢 Medium |
| `security_validation.py` | Security & edge cases | Auth bypass, injection tests | 🔴 Critical |

---

## 🔍 **INTERNAL DEBUGGING STRATEGY**

### **Debug Levels & Logging**

```python
# Debug configuration for all test scripts
DEBUG_LEVELS = {
    "MINIMAL": 1,      # Only test results
    "STANDARD": 2,     # + API responses  
    "DETAILED": 3,     # + Internal engine steps
    "FORENSIC": 4      # + Raw request/response data
}

# Engine-specific debugging
DEMON_ENGINE_DEBUG = {
    "pipeline_selection": True,    # Track which pipeline chosen
    "technique_matching": True,    # Show technique selection logic
    "llm_execution": True,        # LLM calls and responses
    "performance_metrics": True,  # Timing and token usage
    "error_traces": True          # Full error context
}
```

### **Backend Debug Integration**

The backend will output structured debug logs when `DEBUG_BRAIN_ENGINE=1`:

```python
# In demon_engine/services/brain_engine/engine_v2.py
if DEBUG_BRAIN_ENGINE:
    print(f"🎯 [DEMON] Pipeline selected: {pipeline_id}")
    print(f"🧠 [BRAIN] Techniques matched: {technique_ids}")
    print(f"⚡ [LLM] Provider: {provider}, Model: {model}")
    print(f"📊 [METRICS] Tokens: {tokens}, Time: {execution_time}ms")
```

---

## 📋 **DETAILED TEST SCRIPT SPECIFICATIONS**

### **1. user_onboarding.py**

**🎯 Purpose**: Test complete user lifecycle from signup to advanced usage

**🔄 Flow**:
1. **Signup & Authentication**
   - Complete auth flow via `/api/v1/users/auth/complete`
   - Verify user profile creation in database
   - Check initial credit allocation
   - Validate default preferences setup

2. **Profile Management**  
   - Update user profile via `/api/v1/users/me/profile`
   - Test preference modifications
   - Verify data export functionality
   - Check usage tracking initialization

3. **Session Management**
   - Test logout/login cycle
   - Verify token refresh
   - Check session persistence
   - Validate cross-device compatibility

4. **Database Validation**
   - Query MongoDB directly to verify user document structure
   - Check indexes are properly created
   - Validate data consistency
   - Verify audit logs

**🐛 Debug Points**:
- User document creation timestamps
- Credit system initialization
- Auth token generation process
- Database transaction success

---

### **2. features_test.py**

**🎯 Purpose**: Test core AI features with deep engine debugging

**🔄 Flow**:

#### **A. Brain Engine Testing (Legacy)**
```python
# Test Legacy Brain Engine via /api/v1/prompt/
test_cases = [
    {
        "endpoint": "/api/v1/prompt/prompt/quick_upgrade",
        "data": {"text": "Write an email", "mode": "quick"},
        "debug_points": [
            "technique_selection", 
            "pipeline_composition", 
            "groq_api_call"
        ]
    }
]
```

#### **B. Demon Engine Testing (v2)**
```python
# Test Demon Engine via /api/v1/demon/
test_cases = [
    {
        "endpoint": "/api/v1/demon/v2/upgrade", 
        "data": {
            "text": "Create a React component",
            "intent": "code",
            "mode": "pro", 
            "client": "vscode"
        },
        "debug_points": [
            "intent_inference",
            "pipeline_registry_lookup", 
            "technique_matching",
            "fragment_rendering",
            "llm_execution",
            "contract_enforcement"
        ]
    }
]
```

#### **C. AI Features Integration**
- `/api/v1/ai/remix-prompt` - Prompt remixing
- `/api/v1/ai/architect-prompt` - Code architecture
- `/api/v1/ai/fuse-prompts` - Prompt fusion
- `/api/v1/ai/analyze-prompt` - Prompt analysis

**🐛 Debug Points**:
- Pipeline selection logic (`DemonEngineRouter.route`)
- Technique matching confidence scores
- LLM provider selection and fallbacks
- Response contract validation
- Performance metrics (tokens, timing)
- Error handling and fallback execution

---

### **3. marketplace_flow.py**

**🎯 Purpose**: Test e-commerce and billing workflows

**🔄 Flow**:
1. **Product Listing**
   - Create marketplace listing via `/api/v1/marketplace/list-prompt`
   - Verify pricing and metadata
   - Test search functionality

2. **Purchase Flow**
   - Initiate payment via `/api/v1/payments/initiate-payment`
   - Test Razorpay/Paddle webhooks
   - Verify credit deduction
   - Check transaction logging

3. **Billing Integration**
   - Test tier upgrades via `/api/v1/billing/tiers`
   - Verify entitlements via `/api/v1/billing/me/entitlements`
   - Check subscription management

**🐛 Debug Points**:
- Payment provider selection logic
- Webhook processing success
- Credit system calculations
- Subscription state changes

---

### **4. developer_tools.py**

**🎯 Purpose**: Test extension and developer-focused features

**🔄 Flow**:
1. **Extension Intelligence**
   - Test VSCode extension APIs via `/api/v1/extension/`
   - Chrome extension compatibility
   - Context-aware suggestions

2. **Smart Workflows**
   - Test workflow creation via `/api/v1/workflows/`
   - Template management
   - Execution monitoring

**🐛 Debug Points**:
- Extension client identification
- Context parsing accuracy
- Workflow state management
- Template rendering logic

---

### **5. admin_monitoring.py**

**🎯 Purpose**: Test system health and administrative features

**🔄 Flow**:
1. **Health Monitoring**
   - Test all health endpoints
   - Check circuit breakers
   - Verify metrics collection

2. **Performance Analysis**
   - Test slow query detection
   - Cache statistics
   - Resource utilization

**🐛 Debug Points**:
- System resource consumption
- Database connection health
- Cache hit/miss ratios
- Circuit breaker states

---

### **6. security_validation.py**

**🎯 Purpose**: Test security controls and edge cases

**🔄 Flow**:
1. **Authentication Security**
   - Test token validation
   - Authorization bypass attempts
   - Rate limiting effectiveness

2. **Input Validation**
   - Injection attack prevention
   - Malformed request handling
   - Content filtering

**🐛 Debug Points**:
- Auth middleware execution
- Input sanitization process
- Rate limiter state
- Security event logging

---

## 🏗️ **IMPLEMENTATION ARCHITECTURE**

### **Base Test Framework**

```python
class DemonEngineTestFramework:
    def __init__(self, debug_level=3):
        self.debug_level = debug_level
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()
        self.results = []
        
    def setup_debug_mode(self):
        """Enable backend debug logging"""
        os.environ['DEBUG_BRAIN_ENGINE'] = '1'
        
    def execute_test_with_debug(self, test_case):
        """Execute test with comprehensive debugging"""
        # Pre-test setup
        # Execute request
        # Capture debug output
        # Parse engine internals
        # Store results
        pass
        
    def validate_database_state(self):
        """Direct MongoDB validation"""
        pass
        
    def generate_test_report(self):
        """Create detailed test report"""
        pass
```

### **Debug Output Format**

```json
{
  "test_id": "demon_engine_code_upgrade_001",
  "endpoint": "/api/v1/demon/v2/upgrade",
  "request": {...},
  "response": {...},
  "engine_debug": {
    "pipeline_selected": "vscode_pro_pipeline",
    "techniques_matched": ["code_context", "structure_enhancement"],
    "llm_execution": {
      "provider": "openai",
      "model": "gpt-4",
      "tokens_used": 1247,
      "execution_time_ms": 890
    },
    "performance_metrics": {
      "total_time": 1200,
      "cache_hits": 3,
      "database_queries": 2
    }
  },
  "validation_results": {
    "response_structure": "valid",
    "contract_compliance": "passed",
    "database_consistency": "verified"
  }
}
```

---

## 🚀 **EXECUTION PLAN**

### **Phase 1: Core Infrastructure** (Day 1)
1. Create base test framework
2. Implement `user_onboarding.py`
3. Set up debug logging integration
4. Validate basic flows

### **Phase 2: Engine Testing** (Day 2)  
1. Implement `features_test.py`
2. Deep dive into Demon Engine debugging
3. Test all AI feature endpoints
4. Performance benchmarking

### **Phase 3: Business Logic** (Day 3)
1. Implement `marketplace_flow.py`
2. Test payment integrations
3. Verify billing workflows
4. Credit system validation

### **Phase 4: Developer Tools** (Day 4)
1. Implement `developer_tools.py`
2. Test extension APIs
3. Workflow management
4. Integration testing

### **Phase 5: System Validation** (Day 5)
1. Implement `admin_monitoring.py`
2. Implement `security_validation.py`  
3. Load testing
4. Final report generation

---

## 📊 **SUCCESS CRITERIA**

| **Metric** | **Target** | **Measurement** |
|------------|------------|-----------------|
| **Test Coverage** | 95% of endpoints | Automated tracking |
| **Success Rate** | >98% passing tests | Test execution results |
| **Performance** | <500ms avg response | Response time monitoring |
| **Debug Clarity** | 100% engine steps logged | Debug output validation |
| **Database Integrity** | 0 consistency issues | Direct DB validation |

---

This plan ensures comprehensive testing with deep visibility into the Demon Engine's internal operations, providing the debugging and validation needed for production readiness.
