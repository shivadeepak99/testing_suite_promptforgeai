# 🚀 PromptForge.ai API Test Runner (PowerShell)
# Automated test execution script for Windows

Write-Host "🧪 PromptForge.ai API Test Suite" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Configuration
$ServerUrl = "http://localhost:8000"
$MockToken = "mock-test-token"

# Check if server is running
Write-Host "🔍 Checking if server is running..." -ForegroundColor Yellow

try {
    $healthCheck = Invoke-WebRequest -Uri "$ServerUrl/health" -TimeoutSec 5 -ErrorAction Stop
    if ($healthCheck.StatusCode -eq 200) {
        Write-Host "✅ Server is running at $ServerUrl" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Server is not running!" -ForegroundColor Red
    Write-Host "   Please start the server first:" -ForegroundColor Yellow
    Write-Host "   uvicorn main:app --reload" -ForegroundColor White
    exit 1
}

# Check Python dependencies
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow

try {
    python -c "import requests, pytest" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing required packages..." -ForegroundColor Yellow
        pip install requests pytest
    }
} catch {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install requests pytest
}

Write-Host ""
Write-Host "🚀 Starting API Tests..." -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

# Test 1: Quick API Health Check
Write-Host "🏥 Quick Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$ServerUrl/" -Headers @{"Authorization" = "Bearer $MockToken"}
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Root endpoint: $($data.message)" -ForegroundColor Green
} catch {
    Write-Host "❌ Root endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Authentication Test
Write-Host "🔐 Authentication Test..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$ServerUrl/api/v1/users/auth/complete" -Method POST -Headers @{"Authorization" = "Bearer $MockToken"; "Content-Type" = "application/json"}
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Auth complete: User ID $($data.data.uid)" -ForegroundColor Green
    
    # Test get current user
    $userResponse = Invoke-WebRequest -Uri "$ServerUrl/api/v1/users/me" -Headers @{"Authorization" = "Bearer $MockToken"}
    $userData = $userResponse.Content | ConvertFrom-Json
    Write-Host "✅ Get user profile: $($userData.data.uid)" -ForegroundColor Green
} catch {
    Write-Host "❌ Authentication failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Create a test prompt
Write-Host "📝 Prompt Creation Test..." -ForegroundColor Yellow
try {
    $promptData = @{
        title = "PowerShell Test Prompt"
        body = "You are a helpful assistant. Help with {task} by providing {guidance_type} guidance."
        role = "assistant"
    } | ConvertTo-Json

    $response = Invoke-WebRequest -Uri "$ServerUrl/api/v1/prompts/prompts/" -Method POST -Body $promptData -Headers @{"Authorization" = "Bearer $MockToken"; "Content-Type" = "application/json"}
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Prompt created: $($data.data.title)" -ForegroundColor Green
} catch {
    Write-Host "❌ Prompt creation failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Get user credits
Write-Host "💳 Credits Test..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$ServerUrl/api/v1/users/credits" -Headers @{"Authorization" = "Bearer $MockToken"}
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Credits retrieved: $($data.data.credits) credits" -ForegroundColor Green
} catch {
    Write-Host "❌ Credits test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "1️⃣ Running Comprehensive Python Test Suite..." -ForegroundColor Cyan
python api_test_automation.py

Write-Host ""
Write-Host "2️⃣ Running Pytest Suite..." -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

# Check if pytest is available and run tests
try {
    pytest test_api_pytest.py -v --tb=short
} catch {
    Write-Host "❌ Pytest not available or failed. Running basic tests only." -ForegroundColor Red
}

Write-Host ""
Write-Host "3️⃣ Running Specific Test Categories..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Test specific endpoints with PowerShell
$testEndpoints = @(
    @{Name="Health Check"; Endpoint="/health"; Method="GET"},
    @{Name="Monitoring Health"; Endpoint="/api/v1/monitoring/health"; Method="GET"},
    @{Name="Performance Health"; Endpoint="/api/v1/performance/performance/health"; Method="GET"},
    @{Name="Workflow Health"; Endpoint="/api/v1/workflows/api/workflows/health"; Method="GET"},
    @{Name="Extension Health"; Endpoint="/api/v1/extension/extension/health"; Method="GET"},
    @{Name="Billing Tiers"; Endpoint="/api/v1/billing/tiers"; Method="GET"},
    @{Name="Debug Auth Headers"; Endpoint="/api/v1/debug/auth-headers"; Method="GET"},
    @{Name="Debug Test Auth"; Endpoint="/api/v1/debug/test-auth"; Method="POST"}
)

Write-Host "🔗 Testing Core Endpoints:" -ForegroundColor Yellow
foreach ($test in $testEndpoints) {
    try {
        $headers = @{"Authorization" = "Bearer $MockToken"}
        if ($test.Method -eq "GET") {
            $response = Invoke-WebRequest -Uri "$ServerUrl$($test.Endpoint)" -Headers $headers -TimeoutSec 10
        } else {
            $headers["Content-Type"] = "application/json"
            $response = Invoke-WebRequest -Uri "$ServerUrl$($test.Endpoint)" -Method $test.Method -Headers $headers -Body "{}" -TimeoutSec 10
        }
        
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✅ $($test.Name)" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  $($test.Name) - Status: $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ❌ $($test.Name) - Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test marketplace endpoints
Write-Host ""
Write-Host "🏪 Testing Marketplace Endpoints:" -ForegroundColor Yellow
$marketplaceTests = @(
    @{Name="Search Marketplace"; Endpoint="/api/v1/marketplace/search?q=test&limit=5"},
    @{Name="Marketplace Listings"; Endpoint="/api/v1/marketplace/listings"},
    @{Name="Public Prompts"; Endpoint="/api/v1/prompts/prompts/public?limit=5"}
)

foreach ($test in $marketplaceTests) {
    try {
        $response = Invoke-WebRequest -Uri "$ServerUrl$($test.Endpoint)" -Headers @{"Authorization" = "Bearer $MockToken"} -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✅ $($test.Name)" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  $($test.Name) - Status: $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ❌ $($test.Name) - Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 All tests completed!" -ForegroundColor Green
Write-Host "Check the output above for detailed results." -ForegroundColor Cyan

# Generate a simple test report
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportFile = "api_test_report_$timestamp.txt"

@"
PromptForge.ai API Test Report
Generated: $(Get-Date)
Server: $ServerUrl
Mock Token: $MockToken

Test Summary:
- Health checks completed
- Authentication tested  
- Prompt management tested
- Credits system tested
- Core endpoints verified
- Marketplace endpoints tested

For detailed results, see the console output above.
"@ | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host ""
Write-Host "📄 Test report saved to: $reportFile" -ForegroundColor Cyan
