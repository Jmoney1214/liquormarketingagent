# Liquor Marketing Agent - Frontend & Backend Architecture Plan

## 📋 Executive Summary

This document outlines the complete architecture for transforming the CLI-based liquor marketing agent into a full-stack web application with a modern UI and robust backend infrastructure.

---

## 🎯 Current System Analysis

### Existing Components
1. **Subagent** - Customer scoring & action generation (CLI)
2. **Orchestrator** - Weekly campaign planning (CLI)
3. **Sender** - Message dispatch orchestration (CLI)
4. **Pusher** - Email/SMS rendering & delivery (CLI)
5. **Data Sources** - Customer knowledge base, segment playbooks

### Current Workflow
```
Knowledge Base → Subagent → Actions → Orchestrator → Weekly Plan → Sender → Pusher → Channels
```

---

## 🏗️ BACKEND ARCHITECTURE

### 1. Core Services Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                    │
│                     Port 8000 (Main API)                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────────────────┼─────────────────────────┐
    ↓                         ↓                         ↓
┌─────────┐          ┌──────────────┐         ┌──────────────┐
│Customer │          │  Campaign    │         │  Messaging   │
│Service  │          │  Service     │         │  Service     │
└─────────┘          └──────────────┘         └──────────────┘
    ↓                         ↓                         ↓
┌─────────┐          ┌──────────────┐         ┌──────────────┐
│Postgres │          │  PostgreSQL  │         │  Redis Queue │
│Database │          │  + TimescaleDB│         │  + Worker   │
└─────────┘          └──────────────┘         └──────────────┘
```

### 2. Backend Technology Stack

**Core Framework:**
- **FastAPI** (Python 3.11+) - High-performance async API
- **Pydantic** - Data validation & serialization
- **SQLAlchemy 2.0** - ORM with async support
- **Alembic** - Database migrations

**Database Layer:**
- **PostgreSQL 15+** - Primary database
- **TimescaleDB** - Time-series data for analytics
- **Redis** - Caching & job queue
- **S3/MinIO** - File storage (customer lists, exports)

**Background Jobs:**
- **Celery** or **RQ (Redis Queue)** - Async task processing
- **Celery Beat** - Scheduled campaigns & recurring jobs

**External Integrations:**
- **OpenAI API** - LLM orchestration (existing)
- **Mailgun** - Email delivery (existing)
- **Twilio** - SMS delivery (existing)
- **SendGrid** - Alternative email provider
- **Postmark** - Transactional emails

### 3. API Design (RESTful + WebSocket)

#### REST Endpoints

**Authentication & Users**
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
GET    /api/v1/users/me
PATCH  /api/v1/users/me
```

**Customers**
```
GET    /api/v1/customers              # List with filters, pagination
POST   /api/v1/customers              # Create customer
GET    /api/v1/customers/{id}         # Get customer details
PATCH  /api/v1/customers/{id}         # Update customer
DELETE /api/v1/customers/{id}         # Soft delete
POST   /api/v1/customers/import       # Bulk CSV/JSON import
GET    /api/v1/customers/segments     # Get segment breakdown
GET    /api/v1/customers/{id}/history # Purchase & campaign history
```

**Segments & Playbooks**
```
GET    /api/v1/segments               # List all segments
POST   /api/v1/segments               # Create segment
GET    /api/v1/segments/{id}          # Get segment details
PATCH  /api/v1/segments/{id}          # Update segment rules
DELETE /api/v1/segments/{id}          # Delete segment
GET    /api/v1/segments/{id}/customers # Get customers in segment
POST   /api/v1/segments/{id}/refresh  # Re-compute segment membership
```

**Campaigns**
```
GET    /api/v1/campaigns              # List campaigns
POST   /api/v1/campaigns              # Create campaign
GET    /api/v1/campaigns/{id}         # Get campaign details
PATCH  /api/v1/campaigns/{id}         # Update campaign
DELETE /api/v1/campaigns/{id}         # Delete campaign
POST   /api/v1/campaigns/{id}/start   # Start campaign execution
POST   /api/v1/campaigns/{id}/pause   # Pause campaign
POST   /api/v1/campaigns/{id}/resume  # Resume campaign
GET    /api/v1/campaigns/{id}/analytics # Get campaign performance
POST   /api/v1/campaigns/generate     # AI-generate weekly plan
```

**Actions & Sends**
```
GET    /api/v1/actions                # List generated actions
POST   /api/v1/actions/generate       # Generate actions (subagent)
GET    /api/v1/actions/{id}           # Get action details

GET    /api/v1/sends                  # List all sends
GET    /api/v1/sends/{id}             # Get send details
GET    /api/v1/sends/{id}/events      # Delivery events (open, click, etc)
POST   /api/v1/sends/{id}/resend      # Retry failed send
```

**Analytics & Reporting**
```
GET    /api/v1/analytics/dashboard    # KPI overview
GET    /api/v1/analytics/revenue      # Revenue metrics
GET    /api/v1/analytics/cohorts      # Cohort analysis
GET    /api/v1/analytics/churn        # Churn predictions
GET    /api/v1/reports/campaigns      # Campaign performance report
GET    /api/v1/reports/segments       # Segment performance report
POST   /api/v1/reports/export         # Export to CSV/PDF
```

**Settings & Configuration**
```
GET    /api/v1/settings/channels      # Email/SMS configuration
PATCH  /api/v1/settings/channels      # Update channel settings
GET    /api/v1/settings/templates     # Message templates
POST   /api/v1/settings/templates     # Create template
PATCH  /api/v1/settings/templates/{id}# Update template
GET    /api/v1/settings/compliance    # Legal disclaimers, opt-out
```

#### WebSocket Endpoints
```
WS     /ws/campaign/{id}/status       # Real-time campaign status
WS     /ws/notifications              # User notifications
WS     /ws/analytics                  # Live analytics updates
```

### 4. Database Schema

#### Core Tables

**users**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user', -- admin, manager, user
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**customers**
```sql
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    name VARCHAR(255),
    
    -- Segmentation
    rfm_segment VARCHAR(100),
    churn_risk VARCHAR(50),
    clv_score DECIMAL(10,2),
    
    -- Behavioral
    is_night_buyer BOOLEAN DEFAULT false,
    avg_purchase_hour INTEGER,
    purchase_frequency INTEGER DEFAULT 0,
    
    -- Financial
    total_spent DECIMAL(10,2) DEFAULT 0,
    avg_order_value DECIMAL(10,2) DEFAULT 0,
    success_rate_pct DECIMAL(5,2),
    
    -- Product Preferences
    primary_category VARCHAR(100),
    secondary_category VARCHAR(100),
    favorite_brands JSONB,
    
    -- Metadata
    raw_data JSONB, -- Store full customer record
    last_purchase_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_customers_segment ON customers(rfm_segment);
CREATE INDEX idx_customers_churn ON customers(churn_risk);
CREATE INDEX idx_customers_category ON customers(primary_category);
```

**segments**
```sql
CREATE TABLE segments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    rules JSONB NOT NULL, -- Query rules for dynamic segments
    
    -- Playbook
    recommended_offers JSONB,
    messaging_strategy TEXT,
    optimal_channels VARCHAR[] DEFAULT ARRAY['email'],
    optimal_send_window JSONB, -- {start: "18:00", end: "22:00"}
    
    is_active BOOLEAN DEFAULT true,
    customer_count INTEGER DEFAULT 0,
    last_computed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**campaigns**
```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50), -- weekly_plan, one_time, triggered
    status VARCHAR(50) DEFAULT 'draft', -- draft, scheduled, active, paused, completed, cancelled
    
    -- Planning
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    target_segments VARCHAR[] NOT NULL,
    target_kpis JSONB, -- ["win_back_rate", "aov", "conversion_rate"]
    
    -- Execution
    total_sends INTEGER DEFAULT 0,
    completed_sends INTEGER DEFAULT 0,
    failed_sends INTEGER DEFAULT 0,
    
    -- Performance
    opens INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue_generated DECIMAL(12,2) DEFAULT 0,
    
    -- Configuration
    engine VARCHAR(50) DEFAULT 'llm', -- llm, heuristic, manual
    llm_prompt TEXT,
    weekly_plan JSONB, -- Store full generated plan
    
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**actions**
```sql
CREATE TABLE actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    
    -- Priority & Scoring
    priority_score DECIMAL(5,2),
    reason TEXT,
    
    -- Offer Details
    offer TEXT NOT NULL,
    message TEXT,
    creative_hint TEXT,
    
    -- Timing
    scheduled_date DATE NOT NULL,
    send_window JSONB, -- ["18:00", "22:00"]
    
    -- Channel
    channels VARCHAR[] DEFAULT ARRAY['email'],
    
    status VARCHAR(50) DEFAULT 'pending', -- pending, queued, sent, failed, skipped
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_actions_campaign ON actions(campaign_id);
CREATE INDEX idx_actions_customer ON actions(customer_id);
CREATE INDEX idx_actions_status ON actions(status);
CREATE INDEX idx_actions_scheduled ON actions(scheduled_date, status);
```

**sends** (TimescaleDB hypertable)
```sql
CREATE TABLE sends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action_id UUID REFERENCES actions(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
    campaign_id UUID REFERENCES campaigns(id) ON DELETE SET NULL,
    
    -- Message Details
    channel VARCHAR(50) NOT NULL, -- email, sms
    recipient VARCHAR(255) NOT NULL, -- email or phone
    subject TEXT,
    body_html TEXT,
    body_text TEXT,
    
    -- Delivery
    status VARCHAR(50) DEFAULT 'pending', -- pending, sent, delivered, failed, bounced
    provider VARCHAR(50), -- mailgun, twilio, sendgrid
    provider_message_id VARCHAR(255),
    
    -- Events (for analytics)
    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    opened_at TIMESTAMPTZ,
    clicked_at TIMESTAMPTZ,
    converted_at TIMESTAMPTZ,
    conversion_value DECIMAL(10,2),
    
    -- Error handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- TimescaleDB conversion
SELECT create_hypertable('sends', 'created_at');

CREATE INDEX idx_sends_action ON sends(action_id);
CREATE INDEX idx_sends_customer ON sends(customer_id);
CREATE INDEX idx_sends_campaign ON sends(campaign_id);
CREATE INDEX idx_sends_status ON sends(status);
```

**message_templates**
```sql
CREATE TABLE message_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    channel VARCHAR(50) NOT NULL, -- email, sms
    category VARCHAR(100), -- win_back, bundle_offer, discovery
    
    -- Template Content
    subject_template TEXT, -- For email
    body_html_template TEXT, -- For email
    body_text_template TEXT, -- For SMS
    
    -- Variables
    variables JSONB, -- Available template variables
    
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**analytics_events** (TimescaleDB hypertable)
```sql
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL, -- page_view, purchase, email_open, etc
    customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
    campaign_id UUID REFERENCES campaigns(id) ON DELETE SET NULL,
    send_id UUID REFERENCES sends(id) ON DELETE SET NULL,
    
    properties JSONB, -- Event-specific data
    
    occurred_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('analytics_events', 'occurred_at');

CREATE INDEX idx_events_type ON analytics_events(event_type);
CREATE INDEX idx_events_customer ON analytics_events(customer_id);
```

### 5. Backend Services Detail

#### Customer Service
```python
# src/liquor_agent/services/customer_service.py
"""
- CRUD operations for customers
- Customer import (CSV, JSON bulk uploads)
- Segment membership calculation
- Customer scoring (existing logic from subagent)
- Churn prediction & CLV calculation
- Purchase history analysis
"""
```

#### Campaign Service
```python
# src/liquor_agent/services/campaign_service.py
"""
- Campaign lifecycle management (create, schedule, execute, monitor)
- Integration with orchestrator (AI planning)
- Action generation (subagent integration)
- Campaign scheduling & execution
- Performance tracking
"""
```

#### Messaging Service
```python
# src/liquor_agent/services/messaging_service.py
"""
- Message queue management
- Template rendering (existing pusher logic)
- Multi-channel delivery (email, SMS)
- Retry logic for failed sends
- Delivery status tracking
- Webhook handling (Mailgun, Twilio events)
"""
```

#### Analytics Service
```python
# src/liquor_agent/services/analytics_service.py
"""
- Real-time KPI calculation
- Cohort analysis
- Attribution modeling
- Revenue tracking
- Churn analysis
- A/B test results
"""
```

---

## 🎨 FRONTEND ARCHITECTURE

### 1. Frontend Technology Stack

**Core Framework:**
- **React 18+** with **TypeScript**
- **Vite** - Fast build tool
- **React Router v6** - Client-side routing

**State Management:**
- **Zustand** or **Jotai** - Lightweight state management
- **TanStack Query (React Query)** - Server state & caching
- **Zod** - Runtime type validation

**UI Framework:**
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Headless component library
- **Radix UI** - Accessible primitives
- **Recharts** - Data visualization
- **React Table (TanStack Table)** - Advanced tables

**Forms & Validation:**
- **React Hook Form** - Form management
- **Zod** - Schema validation

**Real-time:**
- **Socket.io Client** - WebSocket connections

**Build & Tooling:**
- **ESLint** + **Prettier** - Code quality
- **Vitest** - Unit testing
- **Playwright** - E2E testing

### 2. Application Structure

```
frontend/
├── public/
├── src/
│   ├── assets/              # Images, fonts
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   ├── customers/       # Customer-specific components
│   │   ├── campaigns/       # Campaign components
│   │   ├── analytics/       # Charts & dashboards
│   │   ├── forms/           # Form components
│   │   └── layouts/         # Layout components
│   ├── features/
│   │   ├── auth/            # Authentication
│   │   ├── customers/       # Customer management
│   │   ├── campaigns/       # Campaign management
│   │   ├── segments/        # Segment management
│   │   ├── analytics/       # Analytics & reports
│   │   └── settings/        # Settings & config
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utilities & helpers
│   ├── services/            # API client services
│   ├── stores/              # State management
│   ├── types/               # TypeScript types
│   ├── App.tsx
│   ├── main.tsx
│   └── router.tsx
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

### 3. Key User Interfaces

#### A. Dashboard (Home)
```
┌────────────────────────────────────────────────────────────┐
│  LIQUOR MARKETING AGENT                    [User Menu]     │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 KPI Overview                        Period: Last 7 Days │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ $142.5K  │ │  2,847   │ │  18.4%   │ │  $50.08  │     │
│  │ Revenue  │ │ Sends    │ │ Conv Rate│ │   AOV    │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
│                                                             │
│  📈 Revenue Trend                                          │
│  [Line chart: Last 30 days revenue by day]                │
│                                                             │
│  🎯 Active Campaigns                          [View All]   │
│  • High Churn Win-back Campaign      [85% complete]       │
│  • Weekend Bundle Promotion          [Active]             │
│  • Low-Value Uplift Series           [Scheduled]          │
│                                                             │
│  📬 Recent Sends                                           │
│  [Table: Latest 10 sends with status]                     │
└────────────────────────────────────────────────────────────┘
```

#### B. Customers Page
```
┌────────────────────────────────────────────────────────────┐
│  👥 Customers                                               │
├────────────────────────────────────────────────────────────┤
│  [Search] [Filter by Segment ▼] [Filter by Churn ▼]       │
│  [+ Import CSV] [+ Add Customer]                           │
│                                                             │
│  📊 Segment Breakdown                                      │
│  [Pie chart: Customer distribution by segment]            │
│                                                             │
│  📋 Customer List                    Showing 1-50 of 1,247 │
│  ┌──────────┬──────────┬─────────┬──────────┬──────┐     │
│  │ Name     │ Email    │ Segment │ Churn    │ CLV  │     │
│  ├──────────┼──────────┼─────────┼──────────┼──────┤     │
│  │ John Doe │ john@... │ High_V..│ Medium   │ $450 │ [•••]│
│  │ Jane Sm..│ jane@... │ Low_Val │ High     │ $120 │ [•••]│
│  └──────────┴──────────┴─────────┴──────────┴──────┘     │
│  [Previous] [1] [2] [3] ... [25] [Next]                   │
└────────────────────────────────────────────────────────────┘
```

#### C. Campaign Builder
```
┌────────────────────────────────────────────────────────────┐
│  ← Back to Campaigns                                        │
│  Create New Campaign                                        │
├────────────────────────────────────────────────────────────┤
│  Step 1: Campaign Details                                  │
│  ┌────────────────────────────────────────────────┐       │
│  │ Campaign Name: [Weekend Win-back Blast       ] │       │
│  │ Description:   [Target high-churn customers  ] │       │
│  │ Type:          [○ One-time  ● Weekly  ○ Triggered] │   │
│  │ Date Range:    [10/22/25] to [10/28/25]        │       │
│  └────────────────────────────────────────────────┘       │
│                                                             │
│  Step 2: Audience Selection                                │
│  ┌────────────────────────────────────────────────┐       │
│  │ Target Segments: [☑ High Churn                ] │       │
│  │                  [☑ Low_Value_Frequent         ] │       │
│  │                  [☐ Very_Frequent_Buyers       ] │       │
│  │                                                  │       │
│  │ Estimated Reach: ~847 customers                 │       │
│  └────────────────────────────────────────────────┘       │
│                                                             │
│  Step 3: Strategy                                          │
│  ┌────────────────────────────────────────────────┐       │
│  │ Planning Engine: [● AI (GPT-4) ○ Rule-based]   │       │
│  │ AI Prompt:       [Generate a 7-day plan to... ]│       │
│  │                                                  │       │
│  │ [🤖 Generate Plan with AI]                      │       │
│  └────────────────────────────────────────────────┘       │
│                                                             │
│  [Cancel] [Save Draft] [Schedule Campaign]                │
└────────────────────────────────────────────────────────────┘
```

#### D. Analytics Dashboard
```
┌────────────────────────────────────────────────────────────┐
│  📊 Analytics & Reports                                     │
├────────────────────────────────────────────────────────────┤
│  [Period: Last 30 Days ▼] [Compare: Previous Period ▼]    │
│  [Export PDF] [Export CSV]                                 │
│                                                             │
│  Revenue & Performance                                     │
│  ┌────────────────────────────────────────┐               │
│  │ [Area chart: Revenue by day]           │               │
│  │ [Line overlay: Conversion rate]        │               │
│  └────────────────────────────────────────┘               │
│                                                             │
│  Campaign Performance                                      │
│  ┌──────────────────────┬──────┬──────┬──────┬──────┐    │
│  │ Campaign             │ Sends│ Opens│ Conv │ Rev  │    │
│  ├──────────────────────┼──────┼──────┼──────┼──────┤    │
│  │ High Churn Win-back  │ 1,247│ 18.4%│ 4.2% │$42.5K│    │
│  │ Bundle Promotion     │ 847  │ 22.1%│ 6.8% │$38.2K│    │
│  └──────────────────────┴──────┴──────┴──────┴──────┘    │
│                                                             │
│  Segment Analysis                                          │
│  ┌────────────────────────────────────────┐               │
│  │ [Bar chart: Revenue by segment]        │               │
│  └────────────────────────────────────────┘               │
│                                                             │
│  Churn Prediction                                          │
│  ┌────────────────────────────────────────┐               │
│  │ High Risk: 234 customers (18.8%)       │               │
│  │ [List of top 10 at-risk customers]     │               │
│  └────────────────────────────────────────┘               │
└────────────────────────────────────────────────────────────┘
```

#### E. Segments Management
```
┌────────────────────────────────────────────────────────────┐
│  🎯 Segments & Playbooks                                    │
├────────────────────────────────────────────────────────────┤
│  [+ Create Segment]                                        │
│                                                             │
│  Active Segments                                           │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Low_Value_Frequent                          [Edit] │    │
│  │ 487 customers • Last computed: 2 hours ago        │    │
│  │                                                    │    │
│  │ Rules:                                             │    │
│  │ • RFM Segment = "Low_Value_Frequent"               │    │
│  │ • AOV < $50                                        │    │
│  │                                                    │    │
│  │ Recommended Actions:                               │    │
│  │ • Offer: "Buy 2 get 10% off"                       │    │
│  │ • Channels: Email, SMS                             │    │
│  │ • Send Window: 18:00 - 22:00                       │    │
│  │                                                    │    │
│  │ Performance: 4.2% conv rate | $38/customer value  │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│  [More segments...]                                        │
└────────────────────────────────────────────────────────────┘
```

### 4. Key Frontend Features

#### Real-time Updates
- WebSocket connection for live campaign status
- Toast notifications for important events
- Live analytics updates

#### Data Visualization
- Revenue trends (line/area charts)
- Segment distribution (pie/donut charts)
- Campaign performance (bar charts)
- Cohort retention heatmaps
- Funnel analysis

#### Advanced Tables
- Server-side pagination
- Multi-column sorting
- Advanced filtering
- Column visibility toggle
- CSV/Excel export

#### Form Features
- Multi-step forms (campaign creation)
- Auto-save drafts
- Validation with helpful error messages
- Conditional fields
- File uploads (customer import)

---

## 🔐 SECURITY & COMPLIANCE

### Authentication & Authorization
- **JWT tokens** with refresh mechanism
- **Role-based access control (RBAC)**: Admin, Manager, User
- **API key authentication** for programmatic access
- **2FA support** (TOTP)

### Data Protection
- **Encryption at rest**: Database encryption
- **Encryption in transit**: TLS 1.3
- **PII handling**: Customer data anonymization options
- **GDPR compliance**: Data export, deletion, opt-out
- **CAN-SPAM compliance**: Automatic unsubscribe links

### Monitoring & Logging
- **Application logs**: Structured JSON logging
- **Audit trail**: Track all data modifications
- **Error tracking**: Sentry integration
- **Performance monitoring**: New Relic / DataDog
- **Uptime monitoring**: Better Uptime / Pingdom

---

## 🚀 DEPLOYMENT ARCHITECTURE

### Infrastructure (AWS Example)

```
┌─────────────────────────────────────────────────────────┐
│                    CloudFront CDN                       │
│                  (Frontend Static Assets)               │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              Application Load Balancer                  │
└─────────────────────────────────────────────────────────┘
                            ↓
          ┌─────────────────┴─────────────────┐
          ↓                                   ↓
┌──────────────────┐              ┌──────────────────┐
│   ECS Fargate    │              │   ECS Fargate    │
│  (API Service)   │              │ (Worker Service) │
│   Auto-scaling   │              │  Celery Workers  │
└──────────────────┘              └──────────────────┘
          ↓                                   ↓
┌─────────────────────────────────────────────────────────┐
│                    RDS PostgreSQL                       │
│                   (Multi-AZ, Read Replicas)             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│          ElastiCache Redis (Clustered)                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│          S3 Buckets (Files, Backups, Exports)           │
└─────────────────────────────────────────────────────────┘
```

### Container Strategy
- **Docker** containers for all services
- **Docker Compose** for local development
- **ECS/Kubernetes** for production orchestration
- **Multi-stage builds** for optimized images

### CI/CD Pipeline
```
GitHub Push → GitHub Actions
              ↓
         [Run Tests]
              ↓
         [Build Docker Image]
              ↓
         [Push to ECR/Docker Hub]
              ↓
         [Deploy to Staging]
              ↓
         [Run E2E Tests]
              ↓
         [Manual Approval]
              ↓
         [Deploy to Production]
```

---

## 📈 IMPLEMENTATION PHASES

### Phase 1: Foundation (Weeks 1-3)
**Backend:**
- [ ] Setup FastAPI project structure
- [ ] Database schema & migrations
- [ ] Authentication & user management
- [ ] Customer CRUD API
- [ ] Segment API

**Frontend:**
- [ ] Setup React + Vite project
- [ ] UI component library (shadcn/ui)
- [ ] Authentication flow (login, register)
- [ ] Dashboard layout
- [ ] Customer list page

**DevOps:**
- [ ] Docker setup
- [ ] CI/CD pipeline
- [ ] Staging environment

### Phase 2: Core Features (Weeks 4-6)
**Backend:**
- [ ] Campaign API
- [ ] Action generation service (integrate subagent)
- [ ] Orchestrator service (integrate existing logic)
- [ ] Message queue setup
- [ ] Template rendering

**Frontend:**
- [ ] Campaign builder UI
- [ ] Campaign list & details
- [ ] Segment management UI
- [ ] Customer detail pages

### Phase 3: Messaging & Execution (Weeks 7-8)
**Backend:**
- [ ] Messaging service (email/SMS)
- [ ] Celery workers for async sending
- [ ] Webhook handlers (delivery events)
- [ ] Retry logic & error handling

**Frontend:**
- [ ] Send status monitoring
- [ ] Campaign execution controls
- [ ] Real-time status updates (WebSocket)
- [ ] Message template editor

### Phase 4: Analytics & Reporting (Weeks 9-10)
**Backend:**
- [ ] Analytics service
- [ ] TimescaleDB setup for time-series
- [ ] KPI calculation endpoints
- [ ] Report generation

**Frontend:**
- [ ] Analytics dashboard
- [ ] Charts & visualizations
- [ ] Report export (PDF/CSV)
- [ ] Cohort analysis UI

### Phase 5: Advanced Features (Weeks 11-12)
**Backend:**
- [ ] A/B testing framework
- [ ] Advanced segmentation (ML-based)
- [ ] Predictive churn model
- [ ] API rate limiting & quotas

**Frontend:**
- [ ] Advanced filters & search
- [ ] Bulk operations
- [ ] Settings & configuration pages
- [ ] User management (admin)

### Phase 6: Polish & Launch (Weeks 13-14)
- [ ] Performance optimization
- [ ] Security audit
- [ ] Load testing
- [ ] Documentation
- [ ] User onboarding flow
- [ ] Production deployment

---

## 🛠️ DEVELOPMENT SETUP

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev,openai]"

# Setup database
docker-compose up -d postgres redis
alembic upgrade head

# Run development server
uvicorn liquor_agent.api.main:app --reload --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev  # Runs on http://localhost:5173
```

### Docker Development
```bash
# Run full stack
docker-compose up

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 📦 TECHNOLOGY SUMMARY

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + TypeScript | UI Framework |
| | Vite | Build tool |
| | Tailwind CSS + shadcn/ui | Styling |
| | TanStack Query | Server state |
| | Zustand | Client state |
| | Recharts | Visualization |
| **Backend** | FastAPI | API framework |
| | PostgreSQL 15 | Primary database |
| | TimescaleDB | Time-series data |
| | Redis | Cache & queue |
| | Celery | Background jobs |
| | SQLAlchemy 2.0 | ORM |
| **External** | OpenAI API | LLM orchestration |
| | Mailgun | Email delivery |
| | Twilio | SMS delivery |
| **DevOps** | Docker | Containerization |
| | GitHub Actions | CI/CD |
| | AWS/GCP | Cloud hosting |
| | Sentry | Error tracking |

---

## 🎯 SUCCESS METRICS

### Technical Metrics
- API response time < 200ms (p95)
- Page load time < 2s
- 99.9% uptime
- Zero data loss

### Business Metrics
- Campaign creation time: < 5 minutes
- Customer import: 10K records/minute
- Message throughput: 1000+ sends/minute
- Real-time dashboard latency: < 1s

---

## 📚 NEXT STEPS

1. **Review & Approve** this architecture plan
2. **Setup Development Environment** (Phase 1 kickoff)
3. **Create Detailed User Stories** for each feature
4. **Design Database Migrations** strategy
5. **Establish Code Review Process**
6. **Schedule Regular Sprint Planning**

---

## 📝 NOTES

### Open Questions
1. **Multi-tenancy**: Should this support multiple brands/organizations?
2. **White-labeling**: Custom branding per tenant?
3. **API versioning strategy**: How to handle breaking changes?
4. **Data retention policy**: How long to keep analytics data?
5. **Internationalization**: Support for multiple languages?

### Future Enhancements
- Mobile app (React Native)
- Slack/Teams integration for notifications
- Shopify/WooCommerce plugin
- WhatsApp Business API integration
- Advanced AI features (GPT-4 creative generation)
- Loyalty program integration
- Recommendation engine

---

**Last Updated:** October 22, 2025
**Version:** 1.0
**Author:** Liquor Marketing Agent Team

