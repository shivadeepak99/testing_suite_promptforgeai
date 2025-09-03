# 🚀 PromptForge.ai API Testing Documentation - PART 2

**Continuation from Part 1**  
**Base URL:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs

---

## 📋 TABLE OF CONTENTS - PART 2

1. [Users & Authentication](#users--authentication)
2. [Packaging Management](#packaging-management)
3. [Partnerships](#partnerships)
4. [Analytics](#analytics)
5. [Projects & Notifications](#projects--notifications)

---

## 👥 Users & Authentication

### 1. Get Current User Profile
**GET /api/v1/users/me** - Get Me

**Request:**
```
Headers: Authorization: Bearer {token}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "id": "user_123",
    "username": "testuser",
    "email": "test@example.com",
    "profile": {
      "first_name": "John",
      "last_name": "Doe",
      "bio": "AI enthusiast and prompt engineer",
      "avatar_url": "https://...",
      "location": "San Francisco, CA"
    },
    "subscription": {
      "tier": "pro",
      "expires_at": "2025-12-01T00:00:00Z",
      "auto_renew": true
    },
    "credits": {
      "current_balance": 150,
      "monthly_allowance": 500,
      "usage_this_month": 350
    },
    "created_at": "2025-01-15T10:00:00Z",
    "verified": true
  }
}
```

---

### 2. Update User Profile
**PUT /api/v1/users/me/profile** - Update Profile

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "bio": "Senior AI Prompt Engineer with 5+ years experience",
  "location": "New York, NY",
  "website": "https://johnsmith.dev",
  "linkedin": "https://linkedin.com/in/johnsmith"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "profile": {
      "first_name": "John",
      "last_name": "Smith",
      "bio": "Senior AI Prompt Engineer with 5+ years experience",
      "location": "New York, NY",
      "website": "https://johnsmith.dev",
      "linkedin": "https://linkedin.com/in/johnsmith",
      "updated_at": "2025-09-02T12:00:00Z"
    }
  },
  "message": "Profile updated successfully"
}
```

---

### 3. Get User Credits
**GET /api/v1/users/credits** - Get User Credits

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "current_balance": 150,
    "monthly_allowance": 500,
    "usage_this_month": 350,
    "usage_breakdown": {
      "prompt_analysis": 45,
      "context_analysis": 30,
      "ai_generation": 125,
      "marketplace_purchases": 50,
      "workflow_executions": 100
    },
    "next_renewal": "2025-10-01T00:00:00Z",
    "credit_history": [
      {
        "date": "2025-09-02",
        "action": "monthly_renewal",
        "amount": 500,
        "balance_after": 650
      },
      {
        "date": "2025-09-02",
        "action": "prompt_analysis",
        "amount": -2,
        "balance_after": 148
      }
    ]
  }
}
```

---

### 4. Get User Preferences
**GET /api/v1/users/preferences** - Get User Preferences

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "notifications": {
      "email_notifications": true,
      "push_notifications": false,
      "marketing_emails": true,
      "workflow_updates": true
    },
    "ui_preferences": {
      "theme": "dark",
      "language": "en",
      "timezone": "America/New_York",
      "dashboard_layout": "grid"
    },
    "ai_preferences": {
      "default_model": "gpt-4",
      "creativity_level": "balanced",
      "response_length": "medium",
      "include_explanations": true
    },
    "privacy": {
      "profile_visibility": "public",
      "show_activity": true,
      "allow_analytics": true
    }
  }
}
```

---

### 5. Update User Preferences
**PUT /api/v1/users/preferences** - Update User Preferences

**Request Body:**
```json
{
  "notifications": {
    "email_notifications": false,
    "workflow_updates": true
  },
  "ui_preferences": {
    "theme": "light",
    "language": "en"
  },
  "ai_preferences": {
    "default_model": "gpt-4-turbo",
    "creativity_level": "high"
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "updated_preferences": {
      "notifications": {
        "email_notifications": false,
        "workflow_updates": true
      },
      "ui_preferences": {
        "theme": "light",
        "language": "en"
      },
      "ai_preferences": {
        "default_model": "gpt-4-turbo",
        "creativity_level": "high"
      }
    }
  },
  "message": "Preferences updated successfully"
}
```

---

### 6. Get User Stats
**GET /api/v1/users/stats** - Get User Stats

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "overview": {
      "total_prompts_created": 45,
      "total_prompts_executed": 1250,
      "total_credits_used": 3500,
      "account_age_days": 231
    },
    "this_month": {
      "prompts_created": 8,
      "prompts_executed": 180,
      "credits_used": 350,
      "marketplace_purchases": 3
    },
    "achievements": [
      {
        "id": "first_prompt",
        "name": "First Prompt Creator",
        "description": "Created your first prompt",
        "earned_at": "2025-01-15T10:30:00Z"
      },
      {
        "id": "power_user",
        "name": "Power User",
        "description": "Executed 1000+ prompts",
        "earned_at": "2025-08-20T15:45:00Z"
      }
    ],
    "rankings": {
      "global_rank": 1250,
      "country_rank": 85,
      "percentile": 92
    }
  }
}
```

---

### 7. Export User Data
**GET /api/v1/users/export-data** - Export User Data

**Query Parameters (Optional):**
- `format`: `json` (or `csv`)
- `include_prompts`: `true`
- `include_analytics`: `true`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "export_id": "export_789",
    "download_url": "https://api.promptforge.ai/exports/export_789.zip",
    "expires_at": "2025-09-09T12:00:00Z",
    "file_size": "2.5MB",
    "includes": [
      "user_profile",
      "prompts",
      "usage_analytics",
      "marketplace_activity"
    ]
  },
  "message": "Data export prepared successfully"
}
```

---

## 📦 Packaging Management

### 1. Package Prompt for Marketplace
**POST /api/v1/packaging/{prompt_id}/package** - Package Prompt For Marketplace

**Path Parameters:**
- `prompt_id`: `prompt_456`

**Request Body:**
```json
{
  "marketplace_ready": true,
  "sales_copy": "Transform your email marketing with this comprehensive prompt collection",
  "tags": ["email", "marketing", "automation", "business"],
  "price_usd": 25.00,
  "sales_title": "Ultimate Email Marketing Prompt Pack"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "package_id": "package_789",
    "prompt_id": "prompt_456",
    "marketplace_listing": {
      "title": "Ultimate Email Marketing Prompt Pack",
      "description": "Transform your email marketing with this comprehensive prompt collection",
      "price_usd": 25.00,
      "price_credits": 125,
      "status": "pending_review"
    },
    "package_details": {
      "created_at": "2025-09-02T12:30:00Z",
      "estimated_review_time": "24-48 hours",
      "submission_id": "sub_456"
    }
  },
  "message": "Prompt packaged and submitted for marketplace review"
}
```

---

### 2. List User Packages
**GET /api/v1/packaging/** - List User Packages

**Query Parameters (Optional):**
- `status`: `approved` (pending, approved, rejected)
- `limit`: `10`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "packages": [
      {
        "package_id": "package_789",
        "title": "Ultimate Email Marketing Prompt Pack",
        "status": "approved",
        "price_usd": 25.00,
        "sales_count": 145,
        "revenue_total": 3625.00,
        "commission_rate": 0.70,
        "net_earnings": 2537.50,
        "created_at": "2025-09-01T10:00:00Z",
        "approved_at": "2025-09-01T18:30:00Z"
      }
    ],
    "summary": {
      "total_packages": 5,
      "approved_packages": 4,
      "pending_packages": 1,
      "total_revenue": 8750.00,
      "total_earnings": 6125.00
    }
  }
}
```

---

### 3. Get Package Analytics
**GET /api/v1/packaging/analytics** - Get Package Analytics

**Query Parameters (Optional):**
- `period`: `30d` (7d, 30d, 90d, 1y)
- `package_id`: `package_789`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "overview": {
      "total_sales": 145,
      "total_revenue": 3625.00,
      "average_rating": 4.8,
      "conversion_rate": 12.5
    },
    "time_series": [
      {
        "date": "2025-09-01",
        "sales": 8,
        "revenue": 200.00,
        "views": 120,
        "downloads": 8
      },
      {
        "date": "2025-09-02",
        "sales": 12,
        "revenue": 300.00,
        "views": 180,
        "downloads": 12
      }
    ],
    "geographic_distribution": [
      {"country": "US", "sales": 85, "percentage": 58.6},
      {"country": "UK", "sales": 25, "percentage": 17.2},
      {"country": "CA", "sales": 18, "percentage": 12.4}
    ],
    "top_search_terms": [
      {"term": "email marketing", "frequency": 45},
      {"term": "marketing automation", "frequency": 32}
    ]
  }
}
```

---

## 🤝 Partnerships

### 1. Request Partnership
**POST /api/v1/partnerships/request** - Request Partnership Enhanced

**Request Body:**
```json
{
  "business_type": "agency",
  "use_case": "We provide AI-powered marketing solutions to enterprise clients",
  "expected_monthly_volume": 10000,
  "company_name": "AI Marketing Solutions Inc.",
  "website_url": "https://aimarketing.com",
  "portfolio_urls": [
    "https://case1.com",
    "https://case2.com"
  ]
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "application_id": "partner_app_456",
    "submission_date": "2025-09-02T13:00:00Z",
    "status": "under_review",
    "estimated_response_time": "5-7 business days",
    "next_steps": [
      "Initial review by partnerships team",
      "Technical integration discussion",
      "Contract and terms negotiation",
      "Partnership activation"
    ],
    "contact_person": {
      "name": "Sarah Johnson",
      "email": "partnerships@promptforge.ai",
      "calendar_link": "https://calendly.com/promptforge-partnerships"
    }
  },
  "message": "Partnership application submitted successfully"
}
```

---

### 2. Get Partner Dashboard
**GET /api/v1/partnerships/dashboard** - Get Partner Dashboard

**Query Parameters (Optional):**
- `timeframe`: `30d`
- `include_analytics`: `true`
- `include_revenue`: `true`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "partner_info": {
      "partner_id": "partner_123",
      "company_name": "AI Marketing Solutions Inc.",
      "partnership_tier": "premium",
      "joined_date": "2025-06-01T00:00:00Z",
      "status": "active"
    },
    "performance_metrics": {
      "api_calls_this_month": 85000,
      "revenue_generated": 12500.00,
      "commission_earned": 8750.00,
      "clients_served": 45,
      "average_satisfaction": 4.9
    },
    "usage_analytics": {
      "top_endpoints": [
        {"endpoint": "/api/v1/prompt/upgrade", "calls": 35000},
        {"endpoint": "/api/v1/intelligence/analyze", "calls": 25000}
      ],
      "geographic_distribution": [
        {"region": "North America", "percentage": 65},
        {"region": "Europe", "percentage": 25},
        {"region": "Asia Pacific", "percentage": 10}
      ]
    },
    "account_health": {
      "api_quota_usage": 85,
      "rate_limit_status": "healthy",
      "error_rate": 0.02,
      "uptime": 99.98
    }
  }
}
```

---

## 📊 Analytics

### 1. Get Analytics Dashboard
**GET /api/v1/analytics/dashboard** - Get Analytics Dashboard

**Query Parameters (Optional):**
- `period`: `30d`
- `metrics`: `usage,performance,revenue`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "overview": {
      "total_api_calls": 125000,
      "unique_users": 2500,
      "revenue": 15750.00,
      "error_rate": 0.015,
      "average_response_time": "245ms"
    },
    "usage_trends": [
      {
        "date": "2025-09-01",
        "api_calls": 4200,
        "unique_users": 85,
        "revenue": 525.00
      },
      {
        "date": "2025-09-02",
        "api_calls": 4800,
        "unique_users": 92,
        "revenue": 600.00
      }
    ],
    "top_endpoints": [
      {
        "endpoint": "/api/v1/prompt/upgrade",
        "calls": 35000,
        "success_rate": 99.2,
        "avg_response_time": "180ms"
      },
      {
        "endpoint": "/api/v1/intelligence/analyze",
        "calls": 28000,
        "success_rate": 98.8,
        "avg_response_time": "320ms"
      }
    ],
    "user_segments": [
      {"segment": "power_users", "count": 125, "api_calls": 45000},
      {"segment": "regular_users", "count": 1200, "api_calls": 55000},
      {"segment": "new_users", "count": 1175, "api_calls": 25000}
    ]
  }
}
```

---

### 2. Create Analytics Job
**POST /api/v1/analytics/jobs/analytics** - Create Analytics Job

**Request Body:**
```json
{
  "job_type": "custom_report",
  "parameters": {
    "date_range": "2025-08-01,2025-09-01",
    "metrics": ["usage", "performance", "revenue"],
    "breakdown_by": ["user_tier", "geographic_region"],
    "format": "detailed"
  },
  "job_name": "Monthly Performance Report - August 2025",
  "priority": "normal",
  "notification_email": "analytics@mycompany.com",
  "retention_days": 30
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "job_id": "analytics_job_789",
    "job_name": "Monthly Performance Report - August 2025",
    "status": "queued",
    "estimated_completion": "2025-09-02T14:30:00Z",
    "priority": "normal",
    "created_at": "2025-09-02T13:15:00Z",
    "parameters": {
      "date_range": "2025-08-01,2025-09-01",
      "metrics": ["usage", "performance", "revenue"],
      "breakdown_by": ["user_tier", "geographic_region"]
    }
  },
  "message": "Analytics job created and queued for processing"
}
```

---

### 3. Get Analytics Job Status
**GET /api/v1/analytics/jobs/analytics/{job_id}/status** - Get Analytics Job Status

**Path Parameters:**
- `job_id`: `analytics_job_789`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "job_id": "analytics_job_789",
    "job_name": "Monthly Performance Report - August 2025",
    "status": "completed",
    "progress": 100,
    "started_at": "2025-09-02T13:20:00Z",
    "completed_at": "2025-09-02T13:45:00Z",
    "processing_time": "25 minutes",
    "result": {
      "download_url": "https://api.promptforge.ai/downloads/analytics_job_789.pdf",
      "preview_url": "https://api.promptforge.ai/preview/analytics_job_789",
      "expires_at": "2025-10-02T13:45:00Z",
      "file_size": "4.2MB",
      "format": "PDF"
    },
    "summary": {
      "total_records_processed": 125000,
      "insights_generated": 45,
      "recommendations": 12
    }
  }
}
```

---

**🔄 Continue to PART 3 for remaining endpoints...**

**Next Part Will Cover:**
- AI Intelligence Features (Prompt Intelligence, Context Intelligence)
- Extension Intelligence
- Smart Workflows (detailed testing)
- Monitoring & Performance
- Billing & Payments

---

**💡 Additional Testing Notes:**
- Test with different user roles (free, pro, enterprise)
- Verify rate limiting behavior
- Test error scenarios (invalid data, unauthorized access)
- Check pagination on list endpoints
