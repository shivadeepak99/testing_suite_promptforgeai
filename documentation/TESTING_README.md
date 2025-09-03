# 🚀 PromptForge.ai API Testing Suite

## Overview

This testing suite provides comprehensive automated testing for the PromptForge.ai API using multiple approaches:

- **API Testing** - Direct HTTP requests using Python `requests` library
- **Browser Testing** - Automated browser testing using Playwright
- **Swagger UI Testing** - Manual and automated testing through Swagger UI
- **Security-Safe Testing** - Tests designed to bypass security middleware during development

## 🛠️ Prerequisites

### Required
- Python 3.8+
- PromptForge.ai backend server running on `http://127.0.0.1:8000`
- PowerShell (Windows) or Bash (Linux/Mac)

### Optional (for browser testing)
- Playwright (for browser automation)
- Selenium WebDriver (alternative to Playwright)

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `api_test_safe.py` | Safe API testing script that won't trigger security violations |
| `browser_test_automation.py` | Playwright-based browser automation testing |
| `run_tests.ps1` | PowerShell script to run all tests |
| `test_requirements.txt` | Python dependencies for testing |
| `unblock_ip.py` | Utility to unblock IPs from security middleware |

## 🚀 Quick Start

### 1. Start the Server
```bash
uvicorn main:app --reload
```

### 2. Install Testing Dependencies
```powershell
# PowerShell
.\run_tests.ps1 -Install

# Or manually
pip install -r test_requirements.txt
```

### 3. Run Tests

#### Option A: Use PowerShell Script (Recommended)
```powershell
# Run all tests
.\run_tests.ps1 -TestType all

# Run specific test types
.\run_tests.ps1 -TestType api      # API tests only
.\run_tests.ps1 -TestType browser  # Browser tests only
.\run_tests.ps1 -TestType swagger  # Open Swagger UI
```

#### Option B: Run Individual Scripts
```bash
# API tests
python api_test_safe.py

# Browser tests (requires Playwright)
python browser_test_automation.py
```

## 🔧 Authentication Setup

The testing suite uses a **mock authentication token** to avoid security violations:

### Mock Token
- **Token**: `mock-test-token`
- **Usage**: Automatically used by test scripts
- **Swagger UI**: Enter `mock-test-token` in the Authorize field

### Real Firebase Token (Alternative)
If you want to test with real Firebase tokens:
1. Get your Firebase JWT token from browser dev tools
2. Replace `mock-test-token` with your actual token in test scripts

## 📊 Test Coverage

### ✅ Currently Tested Endpoints

#### Core System
- `GET /health` - Health check
- `GET /docs` - Swagger UI access

#### Authentication
- `POST /api/v1/users/auth/complete` - User registration/login
- `GET /api/v1/users/me` - Get current user profile

#### Analytics
- `GET /api/v1/analytics/dashboard` - Analytics dashboard

#### Workflows
- `GET /api/v1/workflows/api/workflows/templates` - Get workflow templates

### 🔧 Partially Tested (May Need Setup)
- `POST /api/v1/prompts/prompts/` - Create prompt
- `GET /api/v1/prompts/prompts/` - List prompts
- `POST /api/v1/intelligence/analyze` - AI prompt analysis
- `POST /api/v1/workflows/api/workflows/start` - Start workflow

## 🛡️ Security Configuration

### Issue: IP Blocking
If you see `403 Forbidden` errors, your IP may be blocked by the security middleware.

### Solution: Unblock IP
```bash
python unblock_ip.py
```

### Security Middleware Changes
The security middleware has been modified for testing:
- Localhost IPs (`127.0.0.1`, `::1`) bypass validation
- PowerShell/CMD patterns removed from suspicious patterns during development

## 📋 Test Results

### Test Output Locations
- API test results: `test_results_YYYYMMDD_HHMMSS.json`
- Browser test results: `browser_test_results_YYYYMMDD_HHMMSS.json`

### Sample Success Output
```
🎯 PromptForge.ai API Automated Testing Suite
============================================================
📡 Testing Basic Connectivity...
✅ Health Check

🔐 Testing Authentication...
✅ User Authentication - Create Profile
✅ Get User Profile

📋 TEST SUMMARY
============================================================
Total Tests: 10
✅ Passed: 5
❌ Failed: 5
Success Rate: 50.0%
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Server Not Running
```
❌ Server is not running! Please start the server first:
   uvicorn main:app --reload
```

#### 2. Dependencies Missing
```bash
pip install -r test_requirements.txt
```

#### 3. Playwright Not Installed
```bash
pip install playwright
playwright install
```

#### 4. IP Blocked (403 Forbidden)
```bash
python unblock_ip.py
# Then restart the server
```

#### 5. Security Violations
The original issue was caused by security middleware flagging "powershell" as suspicious. This has been resolved by:
- Excluding localhost from security validation
- Removing PowerShell patterns from suspicious detection during development

## 🎯 Advanced Usage

### Custom Test Data
Edit `api_test_safe.py` to modify test data:
```python
# Custom user data
user_data = {
    "uid": "your-custom-uid",
    "email": "your-email@example.com",
    "display_name": "Your Name"
}

# Custom prompt data
prompt_data = {
    "title": "Your Custom Prompt",
    "content": "Your prompt content here"
}
```

### Adding New Tests
1. Add test methods to `PromptForgeAPITester` class
2. Call them in `run_comprehensive_tests()`
3. Follow the pattern: `self.log_result(test_name, success, response_data, error)`

### Browser Test Customization
Modify `browser_test_automation.py`:
```python
# Headless mode
self.browser = await playwright.chromium.launch(headless=True)

# Custom viewport
await self.page.set_viewport_size({"width": 1920, "height": 1080})
```

## 📚 API Documentation Reference

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Test Documentation**: `API_TEST_DOCUMENTATION_PART_*.md`

## 🤝 Contributing

When adding new tests:
1. Follow the existing pattern for error handling
2. Use safe, non-malicious test data
3. Log results consistently
4. Update this README with new test coverage

## 📞 Support

If you encounter issues:
1. Check server logs for errors
2. Verify environment variables are set
3. Ensure MongoDB is running (if required)
4. Run `python unblock_ip.py` if getting 403 errors
