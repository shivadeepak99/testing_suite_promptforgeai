# 🚀 PromptForge.ai API Testing Documentation - PART 1

**Version:** 7.0.0-production-ready  
**Base URL:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs  
**Date:** September 2, 2025

---

## 🔐 Authentication Setup

Before testing protected endpoints, you need to authenticate:

1. **Get Bearer Token** (implement your auth flow)
2. **In Swagger UI:** Click "Authorize" button
3. **Enter:** `Bearer YOUR_TOKEN_HERE`

---

## 📋 TABLE OF CONTENTS - PART 1

1. [Basic Health Endpoints](#basic-health-endpoints)
2. [Prompts Management](#prompts-management)
3. [AI Features](#ai-features)
4. [Marketplace](#marketplace)

---

## 🏥 Basic Health Endpoints

### 1. Root Endpoint
**GET /** - Root

**Request:**
```
No parameters required
```

**Expected Response:**
```json
{
  "message": "Welcome to the PromptForge API ! 🥰🥰"
}
```

**Test Steps:**
1. Click on `GET /` endpoint
2. Click "Try it out"
3. Click "Execute"
4. Verify 200 status code

---

### 2. Health Check
**GET /health** - Health

**Request:**
```
No parameters required
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-02T10:30:00Z",
  "services": {
    "database": "connected",
    "cache": "operational"
  }
}
```

---

## 📝 Prompts Management

### 1. Get User Arsenal
**GET /api/v1/prompts/prompts/arsenal** - Get User Arsenal

**Request:**
```
Headers: Authorization: Bearer {token}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "prompts": [
      {
        "id": "prompt_123",
        "title": "Email Marketing Template",
        "body": "Write a compelling email for...",
        "role": "marketing",
        "created_at": "2025-09-01T10:00:00Z",
        "tags": ["email", "marketing"],
        "usage_count": 15
      }
    ],
    "total_count": 25,
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_pages": 2
    }
  }
}
```

**Test Steps:**
1. Ensure you're authenticated
2. Click "Try it out"
3. Execute
4. Verify 200 status and prompts array

---

### 2. Create New Prompt
**POST /api/v1/prompts/prompts/** - Create New Prompt

**Request Body:**
```json
{
  "title": "Test Prompt Creation",
  "body": "You are a helpful assistant that helps with {task}. Please provide detailed guidance on {topic}.",
  "role": "assistant"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "id": "prompt_456",
    "title": "Test Prompt Creation",
    "body": "You are a helpful assistant that helps with {task}. Please provide detailed guidance on {topic}.",
    "role": "assistant",
    "created_at": "2025-09-02T10:30:00Z",
    "user_id": "user_123",
    "version": 1
  },
  "message": "Prompt created successfully"
}
```

**Test Steps:**
1. Click "Try it out"
2. Replace request body with above JSON
3. Execute
4. Verify 201 status and prompt data

---

### 3. Test Drive Prompt By ID
**POST /api/v1/prompts/prompts/test-drive-by-id** - Test Drive Prompt By Id

**Request Body:**
```json
{
  "prompt_id": "prompt_456",
  "inputs": {
    "task": "learning Python",
    "topic": "object-oriented programming"
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "rendered_prompt": "You are a helpful assistant that helps with learning Python. Please provide detailed guidance on object-oriented programming.",
    "test_id": "test_789",
    "execution_time": "0.45s",
    "credits_used": 1
  }
}
```

---

### 4. Get Prompt Details
**GET /api/v1/prompts/prompts/{prompt_id}** - Get Prompt Details

**Path Parameters:**
- `prompt_id`: `prompt_456`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "id": "prompt_456",
    "title": "Test Prompt Creation",
    "body": "You are a helpful assistant that helps with {task}. Please provide detailed guidance on {topic}.",
    "role": "assistant",
    "created_at": "2025-09-02T10:30:00Z",
    "updated_at": "2025-09-02T10:30:00Z",
    "user_id": "user_123",
    "version": 1,
    "tags": [],
    "usage_stats": {
      "total_runs": 0,
      "last_used": null
    }
  }
}
```

---

### 5. Update Prompt
**PUT /api/v1/prompts/prompts/{prompt_id}** - Update Prompt

**Path Parameters:**
- `prompt_id`: `prompt_456`

**Request Body:**
```json
{
  "title": "Updated Test Prompt",
  "body": "You are an expert assistant that helps with {task}. Please provide comprehensive guidance on {topic} with examples."
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "id": "prompt_456",
    "title": "Updated Test Prompt",
    "body": "You are an expert assistant that helps with {task}. Please provide comprehensive guidance on {topic} with examples.",
    "role": "assistant",
    "updated_at": "2025-09-02T11:00:00Z",
    "version": 2
  },
  "message": "Prompt updated successfully"
}
```

---

### 6. Delete Prompt
**DELETE /api/v1/prompts/prompts/{prompt_id}** - Delete Prompt

**Path Parameters:**
- `prompt_id`: `prompt_456`

**Expected Response:**
```json
{
  "status": "success",
  "message": "Prompt deleted successfully"
}
```

**⚠️ Warning:** This action is irreversible. Test with a non-important prompt.

---

### 7. Get Public Prompts
**GET /api/v1/prompts/prompts/public** - Get Public Prompts

**Query Parameters (Optional):**
- `limit`: `10`
- `offset`: `0`
- `category`: `marketing`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "prompts": [
      {
        "id": "public_prompt_123",
        "title": "Social Media Post Generator",
        "description": "Creates engaging social media posts",
        "author": "promptforge_team",
        "rating": 4.8,
        "downloads": 1250,
        "tags": ["social-media", "marketing"]
      }
    ],
    "pagination": {
      "total": 150,
      "page": 1,
      "per_page": 10
    }
  }
}
```

---

## 🤖 AI Features

### 1. Remix Prompt
**POST /api/v1/ai/remix-prompt** - Remix Prompt

**Request Body:**
```json
{
  "prompt_body": "Write a blog post about artificial intelligence"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "original_prompt": "Write a blog post about artificial intelligence",
    "remixed_prompts": [
      "Create an engaging blog post that explores the transformative power of artificial intelligence in modern society",
      "Craft a thought-provoking blog article about AI's impact on daily life and future possibilities",
      "Write a comprehensive blog post examining artificial intelligence from multiple perspectives"
    ],
    "creativity_level": "high",
    "processing_time": "2.3s"
  }
}
```

---

### 2. Architect Prompt
**POST /api/v1/ai/architect-prompt** - Architect Prompt

**Request Body:**
```json
{
  "description": "I need a prompt for generating product descriptions for e-commerce",
  "techStack": ["OpenAI", "GPT-4"],
  "architectureStyle": "structured"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "architected_prompt": "You are an expert e-commerce copywriter. Create compelling product descriptions that:\n\n1. Highlight key features and benefits\n2. Use persuasive language that drives conversions\n3. Include relevant keywords for SEO\n4. Maintain brand voice consistency\n\nProduct Details: {product_name}, {features}, {target_audience}\n\nOutput a description that is {word_count} words and focuses on {primary_benefit}.",
    "structure": {
      "role_definition": "expert e-commerce copywriter",
      "task_breakdown": ["features", "benefits", "SEO", "brand_voice"],
      "input_variables": ["product_name", "features", "target_audience", "word_count", "primary_benefit"],
      "output_format": "structured description"
    },
    "optimization_suggestions": [
      "Add emotional triggers",
      "Include social proof elements",
      "Consider A/B testing variations"
    ]
  }
}
```

---

### 3. Fuse Prompts
**POST /api/v1/ai/fuse-prompts** - Fuse Prompts

**Request Body:**
```json
{
  "prompt_a": "Write a professional email",
  "prompt_b": "Create marketing content"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "fused_prompt": "Write a professional marketing email that effectively communicates your message while maintaining business etiquette and driving desired actions",
    "fusion_strategy": "semantic_blend",
    "confidence_score": 0.92,
    "fusion_elements": {
      "from_prompt_a": ["professional", "email"],
      "from_prompt_b": ["marketing", "content"],
      "synthesized": ["effective communication", "business etiquette", "driving actions"]
    }
  }
}
```

---

## 🏪 Marketplace

### 1. Search Marketplace
**GET /api/v1/marketplace/search** - Search Marketplace

**Query Parameters:**
- `q`: `email marketing`
- `category`: `marketing`
- `limit`: `5`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "marketplace_456",
        "title": "Email Marketing Automation",
        "description": "Complete email marketing prompt collection",
        "price_credits": 25,
        "rating": 4.9,
        "downloads": 2500,
        "author": {
          "username": "marketing_pro",
          "verified": true
        },
        "tags": ["email", "marketing", "automation"],
        "preview_available": true
      }
    ],
    "total_results": 45,
    "search_time": "0.12s"
  }
}
```

**Test Steps:**
1. Enter search query: "email marketing"
2. Set category filter if desired
3. Execute search
4. Verify relevant results returned

---

### 2. Get Public Prompt Details
**GET /api/v1/marketplace/{id}** - Get Public Prompt Details

**Path Parameters:**
- `id`: `marketplace_456`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "id": "marketplace_456",
    "title": "Email Marketing Automation",
    "description": "Complete collection of email marketing prompts for different industries and use cases",
    "full_description": "This comprehensive prompt pack includes 15 specialized email templates for marketing campaigns...",
    "price_credits": 25,
    "author": {
      "username": "marketing_pro",
      "profile_image": "https://...",
      "verified": true,
      "total_sales": 1250
    },
    "stats": {
      "downloads": 2500,
      "rating": 4.9,
      "reviews_count": 234
    },
    "tags": ["email", "marketing", "automation"],
    "created_at": "2025-08-15T10:00:00Z",
    "last_updated": "2025-09-01T15:30:00Z",
    "preview_prompts": [
      "Subject line optimizer prompt",
      "Welcome email sequence prompt"
    ]
  }
}
```

---

**🔄 Continue to PART 2 for more endpoints...**

**Next Parts Will Cover:**
- Users & Authentication
- Packaging & Partnerships  
- Analytics & Monitoring
- AI Intelligence Features
- Smart Workflows
- And more...

---

**💡 Testing Tips:**
1. Always test authentication first
2. Use realistic test data
3. Check both success and error responses
4. Verify response schemas match documentation
5. Test edge cases (empty data, invalid IDs, etc.)
