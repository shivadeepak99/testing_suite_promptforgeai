# 🚀 PromptForge.ai API Testing Documentation - PART 3

**Continuation from Part 2**  
**Base URL:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs

---

## 📋 TABLE OF CONTENTS - PART 3

1. [AI Intelligence Features](#ai-intelligence-features)
2. [Extension Intelligence](#extension-intelligence)
3. [Smart Workflows](#smart-workflows)
4. [Monitoring & Performance](#monitoring--performance)
5. [Credit Management & Billing](#credit-management--billing)

---

## 🧠 AI Intelligence Features

### Prompt Intelligence

#### 1. Analyze Prompt
**POST /api/v1/intelligence/analyze** - Analyze Prompt

**Request Body:**
```json
{
  "prompt_text": "Write a blog post about machine learning for beginners",
  "session_history": [
    "Previous prompt about AI basics",
    "User showed interest in technical content"
  ],
  "context": {
    "user_expertise": "beginner",
    "target_audience": "general_public",
    "content_type": "educational"
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "analysis_id": "analysis_456",
    "timestamp": "2025-09-02T14:00:00Z",
    "prompt_metrics": {
      "clarity_score": 8.5,
      "specificity_score": 6.2,
      "completeness_score": 7.8,
      "overall_quality": 7.5
    },
    "detected_patterns": [
      "educational_content",
      "beginner_friendly",
      "technical_explanation"
    ],
    "suggestions": [
      {
        "type": "specificity",
        "suggestion": "Consider specifying the blog post length (e.g., '800-word blog post')",
        "impact": "medium",
        "example": "Write an 800-word blog post about machine learning basics for complete beginners"
      },
      {
        "type": "structure",
        "suggestion": "Add structure requirements to improve readability",
        "impact": "high",
        "example": "Include: introduction, 3 main concepts, practical examples, and conclusion"
      }
    ],
    "optimization_tips": [
      "Add target outcome specification",
      "Include tone and style preferences",
      "Specify technical depth level"
    ],
    "quality_score": 7.5,
    "processing_time": "1.2s"
  },
  "credits_used": 2
}
```

---

#### 2. Get Quick Suggestions
**GET /api/v1/intelligence/suggestions/quick** - Get Quick Suggestions

**Query Parameters:**
- `prompt`: `Write a marketing email`
- `category`: `marketing`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "quick_suggestions": [
      "Specify target audience (e.g., 'for B2B software companies')",
      "Add email type (welcome, promotional, newsletter)",
      "Include call-to-action requirements",
      "Specify tone (professional, casual, urgent)",
      "Add length preference (short, medium, detailed)"
    ],
    "improved_prompt": "Write a professional promotional email for B2B software companies that includes a clear call-to-action and persuasive benefits, keeping it concise but compelling",
    "categories": ["marketing", "email", "business"],
    "processing_time": "0.3s"
  }
}
```

---

#### 3. Get Personalized Templates
**GET /api/v1/intelligence/templates/personalized** - Get Personalized Templates

**Query Parameters (Optional):**
- `category`: `content_creation`
- `limit`: `5`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "templates": [
      {
        "id": "template_123",
        "title": "Blog Post Structure Template",
        "template": "Write a {word_count}-word blog post about {topic} for {target_audience}. Structure it with:\n1. Engaging introduction with hook\n2. {main_points_count} main points with examples\n3. Actionable conclusion\n\nTone: {tone}\nStyle: {writing_style}",
        "variables": ["word_count", "topic", "target_audience", "main_points_count", "tone", "writing_style"],
        "use_count": 45,
        "match_score": 0.92,
        "category": "content_creation"
      },
      {
        "id": "template_124",
        "title": "Social Media Post Generator",
        "template": "Create a {platform} post about {topic} that:\n- Captures attention in the first line\n- Includes {hashtag_count} relevant hashtags\n- Has a clear call-to-action\n- Matches {brand_voice} tone\n\nTarget audience: {audience}\nPost goal: {objective}",
        "variables": ["platform", "topic", "hashtag_count", "brand_voice", "audience", "objective"],
        "use_count": 38,
        "match_score": 0.88,
        "category": "social_media"
      }
    ],
    "personalization_factors": [
      "Most used categories: content_creation, marketing",
      "Preferred complexity: medium to high",
      "Common variables: target_audience, tone, word_count"
    ]
  }
}
```

---

### Context Intelligence

#### 1. Analyze Context
**POST /api/v1/context/analyze** - Analyze Context

**Request Body:**
```json
{
  "prompt_text": "Help me with my presentation",
  "domain_hints": ["business", "technology"],
  "session_context": {
    "previous_requests": ["PowerPoint tips", "presentation design"],
    "user_role": "product_manager",
    "project_context": "quarterly_review"
  },
  "user_context": {
    "expertise_level": "intermediate",
    "time_constraint": "urgent",
    "audience_size": "15-20 people"
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "analysis_id": "context_789",
    "timestamp": "2025-09-02T14:15:00Z",
    "domain_analysis": {
      "primary_domain": "business_presentation",
      "confidence": 0.94,
      "sub_domains": ["product_management", "quarterly_reporting", "stakeholder_communication"]
    },
    "context_completeness": {
      "score": 6.5,
      "missing_critical": ["presentation_topic", "duration", "key_message"],
      "missing_helpful": ["slide_count", "visual_requirements", "audience_background"]
    },
    "contextual_suggestions": [
      {
        "category": "specification",
        "suggestion": "Specify the main topic and key message of your presentation",
        "priority": "high",
        "reason": "Essential for creating relevant content"
      },
      {
        "category": "structure",
        "suggestion": "Add presentation duration and target slide count",
        "priority": "medium",
        "reason": "Helps determine content depth and pacing"
      }
    ],
    "missing_information": [
      "What is the main topic/subject of your presentation?",
      "How long should the presentation be?",
      "What's the key message you want to convey?",
      "Who is your specific audience (role, background)?",
      "What type of presentation (informative, persuasive, update)?"
    ],
    "follow_up_questions": [
      "What specific aspect of your quarterly review are you presenting?",
      "Do you need help with content creation or slide design?",
      "What's your biggest challenge with this presentation?"
    ],
    "enhancement_suggestions": [
      "Consider adding storytelling elements for engagement",
      "Include data visualization recommendations",
      "Suggest presenter notes and timing guidelines"
    ],
    "processing_time": "2.1s"
  },
  "credits_used": 3
}
```

---

#### 2. Get Quick Context Suggestions
**POST /api/v1/context/quick-suggestions** - Get Quick Context Suggestions

**Request Body:**
```json
{
  "prompt_text": "Create a workout plan",
  "domain_hint": "fitness"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "quick_suggestions": [
      "Specify fitness goals (weight loss, muscle gain, endurance)",
      "Add current fitness level (beginner, intermediate, advanced)",
      "Include available time per workout",
      "Mention equipment access (gym, home, bodyweight only)",
      "Add any physical limitations or preferences"
    ],
    "enhanced_prompt": "Create a personalized workout plan for [fitness_goal] suitable for a [fitness_level] who has [time_available] per session and access to [equipment_type]. Consider [any_limitations] and focus on [primary_objective].",
    "context_score": 3.2,
    "improvement_potential": "high"
  }
}
```

---

## 🔌 Extension Intelligence

### 1. Analyze Extension Prompt
**POST /api/v1/extension/analyze-prompt** - Analyze Extension Prompt

**Request Body:**
```json
{
  "prompt_text": "Summarize this article",
  "page_context": {
    "url": "https://example.com/ai-trends-2025",
    "title": "Top AI Trends for 2025: What to Expect",
    "content_type": "article",
    "word_count": 1200,
    "main_topics": ["artificial_intelligence", "technology_trends", "future_predictions"]
  },
  "tab_info": {
    "domain": "example.com",
    "category": "technology_blog",
    "reading_time": "5 minutes"
  },
  "quick_mode": false
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "analysis_id": "ext_analysis_456",
    "enhanced_prompt": "Summarize this 1200-word article about 'Top AI Trends for 2025: What to Expect' from example.com. Focus on:\n\n1. Key AI trends mentioned for 2025\n2. Specific predictions and timelines\n3. Impact on different industries\n4. Most significant developments highlighted\n\nProvide a concise but comprehensive summary in 3-4 bullet points, capturing the main insights and actionable takeaways.",
    "context_integration": {
      "page_relevance": 0.95,
      "content_analysis": "Technology article with high information density",
      "optimization_applied": ["topic_focus", "structure_enhancement", "length_specification"]
    },
    "suggestions": [
      "Added specific focus areas based on article content",
      "Included output format for better structure",
      "Specified summary length for clarity"
    ],
    "processing_time": "0.8s"
  },
  "credits_used": 1
}
```

---

### 2. Get Contextual Suggestions
**POST /api/v1/extension/suggestions/contextual** - Get Contextual Suggestions

**Request Body:**
```json
{
  "prompt_text": "Explain this",
  "page_url": "https://github.com/user/repo/blob/main/README.md",
  "page_title": "Advanced ML Library - README",
  "selected_text": "This library implements state-of-the-art transformer architectures with custom attention mechanisms"
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "contextual_suggestions": [
      "Explain this transformer architecture implementation in simple terms",
      "Break down the custom attention mechanisms mentioned in this code",
      "Provide a technical explanation of this ML library's key features",
      "Compare this implementation with standard transformer architectures"
    ],
    "enhanced_prompts": [
      {
        "suggestion": "Explain this transformer architecture implementation, focusing on the custom attention mechanisms and how they differ from standard implementations. Use technical but accessible language.",
        "context_used": ["selected_text", "page_type", "technical_content"],
        "quality_score": 9.2
      }
    ],
    "page_analysis": {
      "content_type": "technical_documentation",
      "complexity_level": "advanced",
      "domain": "machine_learning",
      "key_concepts": ["transformers", "attention_mechanisms", "neural_networks"]
    }
  }
}
```

---

### 3. Enhance Selected Text
**POST /api/v1/extension/enhance/selected-text** - Enhance Selected Text

**Request Body:**
```json
{
  "selected_text": "The product launched successfully with positive feedback",
  "enhancement_type": "expand",
  "page_context": {
    "url": "https://company.com/product-updates",
    "content_type": "business_blog",
    "topic": "product_launch"
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "original_text": "The product launched successfully with positive feedback",
    "enhanced_text": "The product launched successfully, exceeding initial expectations with overwhelmingly positive feedback from early adopters, industry experts, and key stakeholders across multiple market segments. Initial user reviews highlighted the intuitive design, robust functionality, and seamless integration capabilities.",
    "enhancement_details": {
      "type": "expansion",
      "techniques_applied": ["detail_addition", "context_enrichment", "stakeholder_specification"],
      "word_count_change": "10 words → 35 words",
      "readability_improvement": "+15%"
    },
    "alternative_enhancements": [
      {
        "type": "professional_tone",
        "text": "The product deployment was executed successfully, garnering substantial positive reception from target demographics and stakeholder groups."
      },
      {
        "type": "casual_tone", 
        "text": "We totally nailed the product launch! Everyone's loving it and the feedback has been amazing across the board."
      }
    ]
  },
  "credits_used": 2
}
```

---

## 🔄 Smart Workflows

### 1. Get Workflow Templates
**GET /api/v1/workflows/api/workflows/templates** - Get Workflow Templates

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "templates": [
      {
        "id": "template_content_creation",
        "name": "Content Creation Workflow",
        "description": "End-to-end content creation from research to final draft",
        "category": "content",
        "steps": [
          {
            "id": "research",
            "name": "Topic Research",
            "description": "Research and gather information about the topic"
          },
          {
            "id": "outline",
            "name": "Create Outline",
            "description": "Structure the content with detailed outline"
          },
          {
            "id": "draft",
            "name": "Write Draft",
            "description": "Create the first draft based on outline"
          },
          {
            "id": "review",
            "name": "Review & Edit",
            "description": "Review and refine the content"
          }
        ],
        "estimated_time": "15-20 minutes",
        "credits_required": 8,
        "difficulty": "intermediate"
      },
      {
        "id": "template_code_review",
        "name": "Code Review Workflow",
        "description": "Comprehensive code analysis and improvement suggestions",
        "category": "development",
        "steps": [
          {
            "id": "analysis",
            "name": "Code Analysis",
            "description": "Analyze code structure and logic"
          },
          {
            "id": "security",
            "name": "Security Review",
            "description": "Check for security vulnerabilities"
          },
          {
            "id": "performance",
            "name": "Performance Review",
            "description": "Identify performance optimizations"
          },
          {
            "id": "suggestions",
            "name": "Improvement Suggestions",
            "description": "Provide detailed improvement recommendations"
          }
        ],
        "estimated_time": "10-15 minutes",
        "credits_required": 12,
        "difficulty": "advanced"
      }
    ],
    "categories": ["content", "development", "business", "marketing", "research"],
    "total_templates": 15
  }
}
```

---

### 2. Start Workflow
**POST /api/v1/workflows/api/workflows/start** - Start Workflow

**Request Body:**
```json
{
  "template_id": "template_content_creation",
  "inputs": {
    "topic": "Artificial Intelligence in Healthcare",
    "target_audience": "healthcare professionals",
    "content_type": "blog_post",
    "word_count": 1500,
    "tone": "professional_yet_accessible"
  },
  "configuration": {
    "auto_proceed": false,
    "save_intermediary_results": true,
    "notification_email": "user@example.com"
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "instance_id": "workflow_789",
    "template_id": "template_content_creation",
    "status": "running",
    "current_step": "research",
    "started_at": "2025-09-02T15:00:00Z",
    "estimated_completion": "2025-09-02T15:20:00Z",
    "progress": {
      "current_step": 1,
      "total_steps": 4,
      "percentage": 25
    },
    "configuration": {
      "auto_proceed": false,
      "save_intermediary_results": true,
      "notification_email": "user@example.com"
    }
  },
  "message": "Workflow started successfully"
}
```

---

### 3. Get Workflow Status
**GET /api/v1/workflows/api/workflows/status/{instance_id}** - Get Workflow Status

**Path Parameters:**
- `instance_id`: `workflow_789`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "instance_id": "workflow_789",
    "template_id": "template_content_creation",
    "status": "in_progress",
    "current_step": {
      "id": "outline",
      "name": "Create Outline",
      "status": "running",
      "started_at": "2025-09-02T15:05:00Z"
    },
    "completed_steps": [
      {
        "id": "research",
        "name": "Topic Research",
        "status": "completed",
        "completed_at": "2025-09-02T15:05:00Z",
        "duration": "5 minutes",
        "result_preview": "Gathered 15 key research points about AI in healthcare..."
      }
    ],
    "progress": {
      "current_step": 2,
      "total_steps": 4,
      "percentage": 50,
      "estimated_remaining": "10 minutes"
    },
    "resource_usage": {
      "credits_used": 4,
      "credits_remaining": 4,
      "execution_time": "5 minutes"
    }
  }
}
```

---

### 4. Get Workflow Results
**GET /api/v1/workflows/api/workflows/results/{instance_id}** - Get Workflow Results

**Path Parameters:**
- `instance_id`: `workflow_789`

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "instance_id": "workflow_789",
    "final_status": "completed",
    "completed_at": "2025-09-02T15:18:00Z",
    "total_duration": "18 minutes",
    "results": {
      "final_output": {
        "title": "Transforming Healthcare: The Revolutionary Impact of Artificial Intelligence",
        "content": "# Transforming Healthcare: The Revolutionary Impact of Artificial Intelligence\n\n## Introduction\n\nArtificial Intelligence (AI) is reshaping the healthcare landscape at an unprecedented pace...",
        "word_count": 1485,
        "readability_score": 8.2,
        "seo_score": 85
      },
      "intermediary_results": [
        {
          "step": "research",
          "output": {
            "key_points": [
              "AI diagnostics improving accuracy by 40%",
              "Predictive analytics reducing hospital readmissions",
              "Automated medical imaging analysis"
            ],
            "sources": 12,
            "credibility_score": 9.1
          }
        },
        {
          "step": "outline",
          "output": {
            "structure": [
              "Introduction - AI revolution in healthcare",
              "Current AI applications in diagnostics",
              "Predictive analytics and patient care",
              "Challenges and ethical considerations",
              "Future outlook and recommendations"
            ],
            "estimated_sections": 5,
            "logical_flow_score": 8.8
          }
        }
      ]
    },
    "quality_metrics": {
      "overall_quality": 8.7,
      "content_relevance": 9.2,
      "structure_coherence": 8.5,
      "audience_appropriateness": 8.9
    },
    "resource_summary": {
      "total_credits_used": 8,
      "api_calls_made": 15,
      "processing_time": "18 minutes",
      "efficiency_score": 8.4
    }
  }
}
```

---

## 📊 Monitoring & Performance

### 1. Health Check
**GET /api/v1/monitoring/health** - Health Check

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-02T15:30:00Z",
  "version": "7.0.0",
  "environment": "production",
  "services": {
    "database": {
      "status": "healthy",
      "response_time": "12ms",
      "connections": {
        "active": 25,
        "max": 100
      }
    },
    "cache": {
      "status": "healthy",
      "hit_rate": 0.94,
      "memory_usage": "65%"
    },
    "ai_services": {
      "status": "healthy",
      "models_loaded": 8,
      "queue_size": 3
    }
  },
  "uptime": "99.98%",
  "last_restart": "2025-09-01T10:00:00Z"
}
```

---

### 2. Get Detailed Health Check
**GET /api/v1/monitoring/health/detailed** - Detailed Health Check

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-02T15:30:00Z",
  "detailed_status": {
    "api_gateway": {
      "status": "healthy",
      "request_rate": "245 req/min",
      "error_rate": "0.02%",
      "avg_response_time": "156ms"
    },
    "authentication": {
      "status": "healthy",
      "token_validation_time": "8ms",
      "active_sessions": 1250
    },
    "prompt_engine": {
      "status": "healthy",
      "processing_queue": 15,
      "avg_processing_time": "2.1s",
      "success_rate": "99.7%"
    },
    "intelligence_services": {
      "status": "healthy",
      "analysis_accuracy": "94.2%",
      "suggestion_relevance": "91.8%"
    },
    "workflow_engine": {
      "status": "healthy",
      "active_workflows": 45,
      "completion_rate": "98.5%"
    }
  },
  "performance_metrics": {
    "cpu_usage": "45%",
    "memory_usage": "68%",
    "disk_usage": "34%",
    "network_throughput": "125 Mbps"
  },
  "alerts": []
}
```

---

### 3. Get Performance Dashboard
**GET /api/v1/performance/performance/dashboard** - Get Performance Dashboard

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "overview": {
      "avg_response_time": "245ms",
      "throughput": "1250 requests/hour",
      "error_rate": "0.015%",
      "uptime": "99.98%"
    },
    "response_time_breakdown": [
      {"endpoint": "/api/v1/prompt/upgrade", "avg_time": "180ms", "p95": "320ms"},
      {"endpoint": "/api/v1/intelligence/analyze", "avg_time": "290ms", "p95": "450ms"},
      {"endpoint": "/api/v1/workflows/start", "avg_time": "350ms", "p95": "580ms"}
    ],
    "resource_utilization": {
      "cpu_average": "45%",
      "memory_average": "68%", 
      "disk_io": "34%",
      "network_utilization": "23%"
    },
    "bottlenecks": [
      {
        "component": "ai_processing",
        "severity": "low",
        "description": "Slight increase in AI model inference time during peak hours"
      }
    ],
    "recommendations": [
      "Consider scaling AI processing nodes during peak hours",
      "Optimize database queries for analytics endpoints"
    ]
  }
}
```

---

## 💳 Credit Management & Billing

### 1. Get Credit Dashboard
**GET /api/v1/credits/dashboard** - Get Credit Dashboard

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "current_balance": 150,
    "monthly_allowance": 500,
    "usage_this_month": 350,
    "days_remaining": 28,
    "projected_usage": 425,
    "usage_trend": "normal",
    "breakdown": {
      "prompt_analysis": {
        "credits_used": 45,
        "percentage": 12.9,
        "avg_cost_per_use": 2.0
      },
      "ai_generation": {
        "credits_used": 125,
        "percentage": 35.7,
        "avg_cost_per_use": 3.5
      },
      "workflow_execution": {
        "credits_used": 100,
        "percentage": 28.6,
        "avg_cost_per_use": 8.0
      },
      "marketplace_features": {
        "credits_used": 80,
        "percentage": 22.8,
        "avg_cost_per_use": 5.0
      }
    },
    "efficiency_tips": [
      "Use quick analysis instead of full analysis when possible",
      "Batch similar requests for better credit efficiency",
      "Consider workflow templates for repetitive tasks"
    ]
  }
}
```

---

### 2. Get Billing Tiers
**GET /api/v1/billing/tiers** - Get Billing Tiers

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "tiers": [
      {
        "id": "free",
        "name": "Free",
        "price_monthly": 0,
        "credits_monthly": 100,
        "features": [
          "Basic prompt creation",
          "Limited AI analysis",
          "Community templates",
          "Basic support"
        ],
        "limits": {
          "prompts_per_month": 50,
          "api_calls_per_day": 100,
          "workflow_executions": 5
        }
      },
      {
        "id": "pro",
        "name": "Pro",
        "price_monthly": 29,
        "credits_monthly": 500,
        "features": [
          "Advanced AI analysis",
          "Premium templates",
          "Workflow automation",
          "Priority support",
          "Export capabilities"
        ],
        "limits": {
          "prompts_per_month": "unlimited",
          "api_calls_per_day": 1000,
          "workflow_executions": 50
        }
      },
      {
        "id": "enterprise",
        "name": "Enterprise",
        "price_monthly": 99,
        "credits_monthly": 2000,
        "features": [
          "All Pro features",
          "Custom integrations",
          "Advanced analytics",
          "Dedicated support",
          "Custom workflows",
          "Team collaboration"
        ],
        "limits": {
          "prompts_per_month": "unlimited",
          "api_calls_per_day": "unlimited",
          "workflow_executions": "unlimited"
        }
      }
    ],
    "current_tier": "pro",
    "upgrade_benefits": {
      "to_enterprise": [
        "4x more monthly credits",
        "Unlimited API calls",
        "Custom integrations",
        "Advanced analytics"
      ]
    }
  }
}
```

---

**🎉 TESTING COMPLETE!**

## 🎯 Final Testing Checklist

### ✅ Core Functionality Tests
- [ ] Authentication flow
- [ ] Prompt CRUD operations
- [ ] AI analysis features
- [ ] Workflow execution
- [ ] Credit usage tracking

### ✅ Error Scenario Tests
- [ ] Invalid authentication
- [ ] Malformed requests
- [ ] Rate limiting
- [ ] Insufficient credits
- [ ] Network timeouts

### ✅ Performance Tests
- [ ] Response time verification
- [ ] Concurrent request handling
- [ ] Large payload processing
- [ ] Rate limit behavior

### ✅ Security Tests
- [ ] Token validation
- [ ] Input sanitization
- [ ] Access control
- [ ] Data privacy compliance

---

**🚀 Your PromptForge.ai API is ready for comprehensive testing!**

**Happy Testing! 🧪**
