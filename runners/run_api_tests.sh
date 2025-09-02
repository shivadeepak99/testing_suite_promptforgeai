#!/bin/bash
# 🚀 PromptForge.ai API Test Runner
# Automated test execution script

echo "🧪 PromptForge.ai API Test Suite"
echo "================================"

# Check if server is running
echo "🔍 Checking if server is running..."
SERVER_URL="http://localhost:8000"

if curl -s "$SERVER_URL/health" > /dev/null 2>&1; then
    echo "✅ Server is running at $SERVER_URL"
else
    echo "❌ Server is not running!"
    echo "   Please start the server first:"
    echo "   uvicorn main:app --reload"
    exit 1
fi

# Install required packages if not present
echo "📦 Checking dependencies..."
python -c "import requests, pytest" 2>/dev/null || {
    echo "Installing required packages..."
    pip install requests pytest
}

echo ""
echo "🚀 Starting API Tests..."
echo "========================"

# Run the comprehensive test script
echo "1️⃣ Running Comprehensive Test Suite..."
python api_test_automation.py

echo ""
echo "2️⃣ Running Pytest Suite..."
echo "=========================="

# Run pytest with different options
pytest test_api_pytest.py -v --tb=short

echo ""
echo "3️⃣ Running Specific Test Categories..."
echo "====================================="

# Run only authentication tests
echo "🔐 Authentication Tests:"
pytest test_api_pytest.py -k "TestAuthentication" -v

# Run only health tests
echo "🏥 Health Check Tests:"
pytest test_api_pytest.py -k "TestHealthAndStatus" -v

# Run only prompt management tests
echo "📝 Prompt Management Tests:"
pytest test_api_pytest.py -k "TestPromptManagement" -v

echo ""
echo "🎉 All tests completed!"
echo "Check the output above for results."
