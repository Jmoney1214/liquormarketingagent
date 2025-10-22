# API Specification

## Base URL
```
Development: http://localhost:8000/api/v1
Production: https://api.liquormarketing.app/api/v1
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Get Access Token
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user"
  }
}
```

## Data Models

### Customer
```typescript
interface Customer {
  id: string;
  email: string;
  phone?: string;
  name: string;
  
  // Segmentation
  rfm_segment: string;
  churn_risk: 'low' | 'medium' | 'high';
  clv_score: number;
  
  // Behavioral
  is_night_buyer: boolean;
  avg_purchase_hour: number;
  purchase_frequency: number;
  
  // Financial
  total_spent: number;
  avg_order_value: number;
  success_rate_pct: number;
  
  // Product Preferences
  primary_category: string;
  secondary_category?: string;
  favorite_brands: string[];
  
  // Timestamps
  last_purchase_at?: string;
  created_at: string;
  updated_at: string;
}
```

### Campaign
```typescript
interface Campaign {
  id: string;
  name: string;
  description?: string;
  type: 'weekly_plan' | 'one_time' | 'triggered';
  status: 'draft' | 'scheduled' | 'active' | 'paused' | 'completed' | 'cancelled';
  
  // Planning
  start_date: string;
  end_date: string;
  target_segments: string[];
  target_kpis: string[];
  
  // Execution
  total_sends: number;
  completed_sends: number;
  failed_sends: number;
  
  // Performance
  opens: number;
  clicks: number;
  conversions: number;
  revenue_generated: number;
  
  // Configuration
  engine: 'llm' | 'heuristic' | 'manual';
  llm_prompt?: string;
  weekly_plan: WeeklyPlan;
  
  created_by: string;
  created_at: string;
  updated_at: string;
}
```

### Action
```typescript
interface Action {
  id: string;
  campaign_id: string;
  customer_id: string;
  
  // Priority
  priority_score: number;
  reason: string;
  
  // Offer
  offer: string;
  message: string;
  creative_hint: string;
  
  // Timing
  scheduled_date: string;
  send_window: [string, string]; // ["18:00", "22:00"]
  
  // Channel
  channels: ('email' | 'sms')[];
  
  status: 'pending' | 'queued' | 'sent' | 'failed' | 'skipped';
  created_at: string;
  updated_at: string;
}
```

## API Endpoints

### Customers

#### List Customers
```http
GET /customers?page=1&limit=50&segment=Low_Value_Frequent&churn_risk=high

Response 200:
{
  "items": [Customer],
  "total": 1247,
  "page": 1,
  "limit": 50,
  "pages": 25
}
```

#### Get Customer
```http
GET /customers/{id}

Response 200:
Customer
```

#### Create Customer
```http
POST /customers
Content-Type: application/json

{
  "email": "customer@example.com",
  "phone": "+19145551234",
  "name": "Jane Smith",
  "primary_category": "Whiskey",
  "rfm_segment": "High_Value_Infrequent",
  "churn_risk": "low"
}

Response 201:
Customer
```

#### Import Customers (Bulk)
```http
POST /customers/import
Content-Type: multipart/form-data

file: customers.csv
format: csv

Response 202:
{
  "job_id": "uuid",
  "status": "processing",
  "message": "Import job started. Check /jobs/{job_id} for status"
}
```

### Campaigns

#### List Campaigns
```http
GET /campaigns?status=active&page=1&limit=20

Response 200:
{
  "items": [Campaign],
  "total": 15,
  "page": 1,
  "limit": 20,
  "pages": 1
}
```

#### Create Campaign
```http
POST /campaigns
Content-Type: application/json

{
  "name": "Weekend Win-back Blast",
  "description": "Target high-churn customers with premium offers",
  "type": "weekly_plan",
  "start_date": "2025-10-22",
  "end_date": "2025-10-28",
  "target_segments": ["High_Churn", "Low_Value_Frequent"],
  "target_kpis": ["win_back_rate", "aov", "conversion_rate"],
  "engine": "llm",
  "llm_prompt": "Generate a 7-day plan to lift AOV and win back high-churn customers"
}

Response 201:
Campaign
```

#### Generate Campaign Plan (AI)
```http
POST /campaigns/generate
Content-Type: application/json

{
  "target_segments": ["High_Churn", "Low_Value_Frequent"],
  "start_date": "2025-10-22",
  "end_date": "2025-10-28",
  "prompt": "Build a 7-day plan to lift AOV and win back high-churn customers",
  "strategy": "Focus on night buyers with premium bundle offers"
}

Response 200:
{
  "period": "2025-10-22 to 2025-10-28",
  "rationale": "Focus high-churn win-backs and bundle AOV uplift. Timing aligned to buyer behavior.",
  "cohorts": ["High churn", "Low_Value_Frequent", "Category primaries"],
  "kpis": ["win_back_rate", "aov", "conversion_rate"],
  "sends": [
    {
      "date": "2025-10-22",
      "segment": "High_Churn",
      "offer": "20% win-back discount",
      "channel": ["Email", "SMS"],
      "send_window": ["18:00", "22:00"],
      "creative_hint": "Premium whiskey focus | Scarcity framing",
      "estimated_reach": 234
    }
  ],
  "engine": "llm"
}
```

#### Start Campaign
```http
POST /campaigns/{id}/start

Response 200:
{
  "id": "uuid",
  "status": "active",
  "message": "Campaign started successfully"
}
```

#### Get Campaign Analytics
```http
GET /campaigns/{id}/analytics

Response 200:
{
  "campaign_id": "uuid",
  "overview": {
    "total_sends": 847,
    "delivered": 842,
    "opened": 156,
    "clicked": 38,
    "converted": 12,
    "revenue": 4250.00
  },
  "rates": {
    "delivery_rate": 0.994,
    "open_rate": 0.184,
    "click_rate": 0.045,
    "conversion_rate": 0.014
  },
  "timeline": [
    {
      "date": "2025-10-22",
      "sends": 121,
      "opens": 22,
      "conversions": 3,
      "revenue": 450.00
    }
  ],
  "by_segment": [
    {
      "segment": "High_Churn",
      "sends": 234,
      "conversion_rate": 0.018,
      "revenue": 1840.00
    }
  ]
}
```

### Analytics

#### Dashboard KPIs
```http
GET /analytics/dashboard?period=last_7_days

Response 200:
{
  "period": "2025-10-16 to 2025-10-22",
  "kpis": {
    "total_revenue": 142500.00,
    "total_sends": 2847,
    "conversion_rate": 0.184,
    "avg_order_value": 50.08,
    "active_campaigns": 3,
    "churn_risk_high": 234
  },
  "revenue_trend": [
    { "date": "2025-10-16", "revenue": 18500.00 },
    { "date": "2025-10-17", "revenue": 21200.00 }
  ],
  "top_segments": [
    { "segment": "High_Value_Frequent", "revenue": 45000.00, "customers": 127 }
  ]
}
```

#### Revenue Analytics
```http
GET /analytics/revenue?start_date=2025-10-01&end_date=2025-10-22&group_by=day

Response 200:
{
  "total_revenue": 425000.00,
  "avg_daily_revenue": 19318.18,
  "growth_rate": 0.12,
  "by_period": [
    {
      "period": "2025-10-01",
      "revenue": 18500.00,
      "orders": 234,
      "aov": 79.06
    }
  ],
  "by_segment": [
    {
      "segment": "High_Value_Frequent",
      "revenue": 145000.00,
      "percentage": 0.341
    }
  ],
  "by_category": [
    {
      "category": "Whiskey",
      "revenue": 125000.00,
      "percentage": 0.294
    }
  ]
}
```

### Segments

#### List Segments
```http
GET /segments

Response 200:
{
  "items": [
    {
      "id": "uuid",
      "name": "Low_Value_Frequent",
      "description": "Customers with frequent purchases but low AOV",
      "rules": {
        "rfm_segment": ["Low_Value_Frequent"],
        "avg_order_value": { "lt": 50 }
      },
      "recommended_offers": ["Buy 2 get 10% off", "Bundle uplift offers"],
      "customer_count": 487,
      "last_computed_at": "2025-10-22T14:30:00Z"
    }
  ]
}
```

#### Create Segment
```http
POST /segments
Content-Type: application/json

{
  "name": "Premium Night Buyers",
  "description": "High-value customers who purchase after 6pm",
  "rules": {
    "rfm_segment": ["High_Value_Frequent", "High_Value_Infrequent"],
    "is_night_buyer": true
  },
  "recommended_offers": ["Exclusive late-night drops", "Premium bundle 15% off"],
  "optimal_channels": ["email", "sms"],
  "optimal_send_window": {"start": "18:00", "end": "22:00"}
}

Response 201:
Segment
```

#### Refresh Segment Membership
```http
POST /segments/{id}/refresh

Response 202:
{
  "job_id": "uuid",
  "status": "processing",
  "message": "Segment refresh started"
}
```

### Actions

#### Generate Actions
```http
POST /actions/generate
Content-Type: application/json

{
  "segments": ["High_Churn", "Low_Value_Frequent"],
  "limit": 300,
  "priority_weights": {
    "churn_risk": 50,
    "success_rate": 15,
    "behavioral": 10
  }
}

Response 201:
{
  "job_id": "uuid",
  "generated_at": "2025-10-22T15:45:00Z",
  "actions_count": 300,
  "actions": [Action]
}
```

### Message Templates

#### List Templates
```http
GET /settings/templates?channel=email

Response 200:
{
  "items": [
    {
      "id": "uuid",
      "name": "Win-back Offer",
      "channel": "email",
      "category": "win_back",
      "subject_template": "{{primary_category}} • {{offer}}",
      "body_html_template": "<html>...</html>",
      "variables": ["primary_category", "offer", "name"],
      "is_active": true
    }
  ]
}
```

## WebSocket Events

### Campaign Status Updates
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/campaign/{campaign_id}/status');

// Events received:
{
  "event": "campaign_started",
  "campaign_id": "uuid",
  "timestamp": "2025-10-22T16:00:00Z"
}

{
  "event": "send_completed",
  "campaign_id": "uuid",
  "action_id": "uuid",
  "status": "sent",
  "progress": {
    "completed": 45,
    "total": 847,
    "percentage": 5.3
  }
}

{
  "event": "campaign_completed",
  "campaign_id": "uuid",
  "summary": {
    "total_sends": 847,
    "successful": 842,
    "failed": 5
  }
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Error Codes
- `VALIDATION_ERROR` (400) - Invalid input data
- `UNAUTHORIZED` (401) - Missing or invalid authentication
- `FORBIDDEN` (403) - Insufficient permissions
- `NOT_FOUND` (404) - Resource not found
- `CONFLICT` (409) - Resource already exists
- `RATE_LIMITED` (429) - Too many requests
- `INTERNAL_ERROR` (500) - Server error

## Rate Limiting

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1698087600
```

Limits:
- Authenticated: 1000 requests/hour
- Unauthenticated: 100 requests/hour
- Bulk operations: 10 requests/hour

## Pagination

All list endpoints support pagination:
```
?page=1&limit=50
```

Response includes:
```json
{
  "items": [...],
  "total": 1247,
  "page": 1,
  "limit": 50,
  "pages": 25
}
```

## Filtering & Sorting

```
?segment=High_Churn&churn_risk=high&sort=-created_at
```

- Prefix `-` for descending sort
- Multiple filters with `&`
- Arrays with comma: `?segments=High_Churn,Low_Value`

## Webhooks

Configure webhooks to receive events:

```http
POST /settings/webhooks
{
  "url": "https://yourapp.com/webhooks",
  "events": ["campaign.completed", "send.delivered", "send.opened"],
  "secret": "your_webhook_secret"
}
```

Webhook payload:
```json
{
  "event": "campaign.completed",
  "timestamp": "2025-10-22T16:30:00Z",
  "data": {
    "campaign_id": "uuid",
    "summary": {...}
  },
  "signature": "sha256=..."
}
```

