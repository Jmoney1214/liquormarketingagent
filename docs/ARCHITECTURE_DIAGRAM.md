# Architecture Diagrams

This document contains visual architecture diagrams for the Liquor Marketing Agent application.

---

## System Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
        Mobile[Mobile App - Future]
    end
    
    subgraph "CDN & Load Balancer"
        CDN[CloudFront CDN<br/>Static Assets]
        ALB[Application Load Balancer]
    end
    
    subgraph "Application Layer"
        API[FastAPI Backend<br/>Port 8000]
        Worker[Celery Workers<br/>Background Jobs]
    end
    
    subgraph "Data Layer"
        Postgres[(PostgreSQL<br/>Primary Database)]
        TimescaleDB[(TimescaleDB<br/>Time-Series Analytics)]
        Redis[(Redis<br/>Cache & Queue)]
        S3[S3 Storage<br/>Files & Exports]
    end
    
    subgraph "External Services"
        OpenAI[OpenAI API<br/>GPT-4 Planning]
        Mailgun[Mailgun<br/>Email Delivery]
        Twilio[Twilio<br/>SMS Delivery]
    end
    
    Browser -->|HTTPS| CDN
    Browser -->|REST API| ALB
    Browser -->|WebSocket| ALB
    CDN -->|HTML/CSS/JS| Browser
    ALB --> API
    API --> Postgres
    API --> TimescaleDB
    API --> Redis
    API --> S3
    API -->|Queue Jobs| Redis
    Worker -->|Process Jobs| Redis
    Worker --> Postgres
    Worker --> Mailgun
    Worker --> Twilio
    API --> OpenAI
    
    style Browser fill:#4A90E2
    style API fill:#7ED321
    style Worker fill:#F5A623
    style Postgres fill:#BD10E0
    style Redis fill:#D0021B
```

---

## Backend Service Architecture

```mermaid
graph LR
    subgraph "API Layer - FastAPI"
        Auth[Auth Service]
        Customer[Customer Service]
        Campaign[Campaign Service]
        Analytics[Analytics Service]
        Messaging[Messaging Service]
    end
    
    subgraph "Business Logic"
        Orchestrator[AI Orchestrator<br/>Campaign Planning]
        Subagent[Customer Scorer<br/>Action Generator]
        Renderer[Message Renderer<br/>Templates]
    end
    
    subgraph "Data Access"
        ORM[SQLAlchemy ORM]
        Cache[Redis Cache]
    end
    
    Auth --> ORM
    Customer --> ORM
    Customer --> Cache
    Campaign --> Orchestrator
    Campaign --> Subagent
    Orchestrator --> OpenAI[OpenAI API]
    Subagent --> ORM
    Messaging --> Renderer
    Messaging --> Worker[Celery Workers]
    Analytics --> ORM
    ORM --> DB[(Database)]
    
    style Orchestrator fill:#FFD700
    style Subagent fill:#FF6347
    style Renderer fill:#32CD32
```

---

## Frontend Architecture

```mermaid
graph TB
    subgraph "React Application"
        App[App.tsx<br/>Root Component]
        Router[React Router<br/>Routing]
        
        subgraph "Feature Modules"
            Dashboard[Dashboard]
            Customers[Customers]
            Campaigns[Campaigns]
            Analytics[Analytics]
            Settings[Settings]
        end
        
        subgraph "Shared Components"
            UI[shadcn/ui<br/>Component Library]
            Charts[Recharts<br/>Data Viz]
            Forms[React Hook Form]
            Tables[TanStack Table]
        end
        
        subgraph "State Management"
            AuthStore[Auth Store<br/>Zustand]
            AppStore[App Store<br/>Zustand]
            ReactQuery[React Query<br/>Server State]
        end
        
        subgraph "Services"
            APIClient[API Client<br/>Axios]
            WebSocket[WebSocket Client<br/>Socket.io]
        end
    end
    
    App --> Router
    Router --> Dashboard
    Router --> Customers
    Router --> Campaigns
    Router --> Analytics
    Router --> Settings
    
    Dashboard --> UI
    Customers --> UI
    Customers --> Tables
    Campaigns --> Forms
    Analytics --> Charts
    
    Dashboard --> ReactQuery
    Customers --> ReactQuery
    Campaigns --> ReactQuery
    Analytics --> ReactQuery
    
    ReactQuery --> APIClient
    WebSocket --> AuthStore
    APIClient --> Backend[Backend API]
    WebSocket --> Backend
    
    AuthStore -.->|Auth Token| APIClient
    
    style App fill:#61DAFB
    style ReactQuery fill:#FF4154
    style APIClient fill:#4A90E2
```

---

## Data Flow - Campaign Creation

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant AI as AI Orchestrator
    participant DB as Database
    participant Queue as Redis Queue
    participant Worker as Celery Worker
    participant Mail as Mailgun/Twilio
    
    User->>Frontend: Create Campaign
    Frontend->>API: POST /campaigns
    API->>DB: Save Campaign (draft)
    DB-->>API: Campaign ID
    API-->>Frontend: Campaign Created
    
    User->>Frontend: Generate AI Plan
    Frontend->>API: POST /campaigns/{id}/generate
    API->>DB: Get Target Customers
    DB-->>API: Customer List
    API->>AI: Generate 7-day Plan
    AI-->>API: Optimized Plan
    API->>DB: Save Actions
    DB-->>API: Success
    API-->>Frontend: Plan Generated
    
    User->>Frontend: Start Campaign
    Frontend->>API: POST /campaigns/{id}/start
    API->>Queue: Enqueue Send Jobs
    API->>DB: Update Status (active)
    API-->>Frontend: Campaign Started
    
    loop For Each Send
        Worker->>Queue: Dequeue Job
        Worker->>DB: Get Customer & Template
        Worker->>Mail: Send Email/SMS
        Mail-->>Worker: Delivery Status
        Worker->>DB: Update Send Status
        Worker-->>Frontend: Status Update (WebSocket)
    end
    
    Frontend->>User: Show Real-time Progress
```

---

## Database Schema (Entity Relationship)

```mermaid
erDiagram
    USERS ||--o{ CAMPAIGNS : creates
    CUSTOMERS ||--o{ ACTIONS : targeted_by
    CUSTOMERS }o--|| SEGMENTS : belongs_to
    CAMPAIGNS ||--o{ ACTIONS : contains
    ACTIONS ||--|| SENDS : generates
    SENDS ||--o{ ANALYTICS_EVENTS : tracks
    CAMPAIGNS ||--o{ ANALYTICS_EVENTS : generates
    
    USERS {
        uuid id PK
        string email UK
        string password_hash
        string full_name
        string role
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }
    
    CUSTOMERS {
        uuid id PK
        string email UK
        string phone
        string name
        string rfm_segment FK
        string churn_risk
        decimal clv_score
        boolean is_night_buyer
        decimal total_spent
        decimal avg_order_value
        string primary_category
        jsonb raw_data
        timestamp created_at
        timestamp updated_at
    }
    
    SEGMENTS {
        uuid id PK
        string name
        text description
        jsonb rules
        jsonb recommended_offers
        int customer_count
        timestamp last_computed_at
    }
    
    CAMPAIGNS {
        uuid id PK
        string name
        string type
        string status
        date start_date
        date end_date
        array target_segments
        int total_sends
        int completed_sends
        decimal revenue_generated
        jsonb weekly_plan
        uuid created_by FK
        timestamp created_at
    }
    
    ACTIONS {
        uuid id PK
        uuid campaign_id FK
        uuid customer_id FK
        decimal priority_score
        text offer
        date scheduled_date
        jsonb send_window
        array channels
        string status
    }
    
    SENDS {
        uuid id PK
        uuid action_id FK
        uuid customer_id FK
        string channel
        string recipient
        text subject
        text body_html
        string status
        timestamp sent_at
        timestamp delivered_at
        timestamp opened_at
        timestamp clicked_at
    }
    
    ANALYTICS_EVENTS {
        uuid id PK
        string event_type
        uuid customer_id FK
        uuid campaign_id FK
        jsonb properties
        timestamp occurred_at
    }
```

---

## Deployment Architecture (AWS)

```mermaid
graph TB
    subgraph "CloudFront CDN"
        CF[CloudFront Distribution]
    end
    
    subgraph "VPC - us-east-1"
        subgraph "Public Subnets"
            ALB[Application Load Balancer]
            NAT[NAT Gateway]
        end
        
        subgraph "Private Subnets - App Tier"
            ECS1[ECS Fargate Task<br/>API Service]
            ECS2[ECS Fargate Task<br/>API Service]
            Worker1[ECS Fargate Task<br/>Celery Worker]
            Worker2[ECS Fargate Task<br/>Celery Worker]
        end
        
        subgraph "Private Subnets - Data Tier"
            RDS[(RDS PostgreSQL<br/>Multi-AZ)]
            ElastiCache[(ElastiCache Redis<br/>Cluster Mode)]
        end
    end
    
    subgraph "S3"
        StaticAssets[S3 Bucket<br/>Frontend Assets]
        DataBucket[S3 Bucket<br/>Customer Data]
    end
    
    subgraph "External Services"
        ECR[ECR<br/>Docker Images]
        Secrets[Secrets Manager<br/>API Keys]
        CW[CloudWatch<br/>Logs & Metrics]
        OpenAI[OpenAI API]
        Mailgun[Mailgun API]
        Twilio[Twilio API]
    end
    
    Users[Users] -->|HTTPS| CF
    CF --> StaticAssets
    Users -->|HTTPS API| ALB
    ALB --> ECS1
    ALB --> ECS2
    ECS1 --> RDS
    ECS2 --> RDS
    ECS1 --> ElastiCache
    ECS2 --> ElastiCache
    Worker1 --> ElastiCache
    Worker2 --> ElastiCache
    Worker1 --> RDS
    Worker2 --> RDS
    
    ECS1 --> NAT
    Worker1 --> NAT
    NAT --> OpenAI
    NAT --> Mailgun
    NAT --> Twilio
    
    ECS1 -.->|Pull Images| ECR
    ECS1 -.->|Get Secrets| Secrets
    ECS1 -.->|Logs| CW
    Worker1 -.->|Logs| CW
    
    DataBucket -.->|Backup| RDS
    
    style CF fill:#FF9900
    style ALB fill:#FF9900
    style RDS fill:#527FFF
    style ElastiCache fill:#D0021B
    style ECS1 fill:#FF9900
    style Worker1 fill:#FF6600
```

---

## Message Sending Flow

```mermaid
flowchart TD
    Start([Campaign Started]) --> Queue[Queue Actions<br/>to Redis]
    Queue --> Worker{Celery Worker<br/>Picks Up Job}
    Worker --> GetData[Get Customer<br/>& Template Data]
    GetData --> Render[Render Message<br/>Subject + Body]
    Render --> Channel{Channel Type?}
    
    Channel -->|Email| RenderEmail[Render HTML Email]
    Channel -->|SMS| RenderSMS[Render SMS Text]
    
    RenderEmail --> SendMailgun[Send via Mailgun]
    RenderSMS --> SendTwilio[Send via Twilio]
    
    SendMailgun --> CheckEmail{Success?}
    SendTwilio --> CheckSMS{Success?}
    
    CheckEmail -->|Yes| UpdateSent[Update Status: Sent]
    CheckEmail -->|No| Retry{Retry Count < 3?}
    
    CheckSMS -->|Yes| UpdateSent
    CheckSMS -->|No| Retry
    
    Retry -->|Yes| Delay[Wait 5 minutes]
    Retry -->|No| UpdateFailed[Update Status: Failed]
    
    Delay --> Worker
    UpdateSent --> WebhookListen[Listen for Webhooks]
    UpdateFailed --> Notify[Notify Admin]
    
    WebhookListen --> Delivered[Delivery Event]
    WebhookListen --> Opened[Open Event]
    WebhookListen --> Clicked[Click Event]
    
    Delivered --> UpdateDB[(Update Database)]
    Opened --> UpdateDB
    Clicked --> UpdateDB
    
    UpdateDB --> RealTime[Push to Frontend<br/>via WebSocket]
    RealTime --> End([User Sees Update])
    
    style Start fill:#00C853
    style End fill:#00C853
    style UpdateFailed fill:#D50000
    style UpdateSent fill:#00C853
    style RealTime fill:#2196F3
```

---

## AI Campaign Planning Flow

```mermaid
flowchart LR
    subgraph Input
        KB[Customer Knowledge Base]
        Segments[Segment Playbooks]
        Goal[Campaign Goal]
    end
    
    subgraph "Subagent - Scoring"
        Score[Score Customers]
        Rank[Rank by Priority]
        TopN[Select Top 300]
    end
    
    subgraph "Orchestrator - Planning"
        Context[Build Context]
        Prompt[Generate Prompt]
        GPT[OpenAI GPT-4]
        Parse[Parse Response]
    end
    
    subgraph Output
        Plan[7-Day Plan]
        Actions[Individual Actions]
        Schedule[Send Schedule]
    end
    
    KB --> Score
    Score --> Rank
    Rank --> TopN
    
    TopN --> Context
    Segments --> Context
    Goal --> Prompt
    Context --> Prompt
    
    Prompt --> GPT
    GPT --> Parse
    
    Parse --> Plan
    Plan --> Actions
    Actions --> Schedule
    
    style Score fill:#FFD700
    style GPT fill:#10A37F
    style Plan fill:#4CAF50
```

---

## Security Architecture

```mermaid
graph TB
    subgraph "Client"
        Browser[Web Browser]
    end
    
    subgraph "Security Layers"
        WAF[AWS WAF<br/>DDoS Protection]
        TLS[TLS 1.3<br/>Encryption in Transit]
    end
    
    subgraph "Authentication"
        JWT[JWT Tokens<br/>Access + Refresh]
        AuthMiddleware[Auth Middleware<br/>Verify Token]
        RBAC[Role-Based Access Control<br/>Admin/Manager/User]
    end
    
    subgraph "Application"
        API[FastAPI Backend]
        ValidationLayer[Input Validation<br/>Pydantic]
    end
    
    subgraph "Data Protection"
        Encryption[(Database Encryption<br/>at Rest)]
        Secrets[Secrets Manager<br/>API Keys]
        PII[PII Masking<br/>Sensitive Data]
    end
    
    subgraph "Monitoring"
        Logs[Audit Logs<br/>All Actions Tracked]
        Alerts[Security Alerts<br/>Anomaly Detection]
    end
    
    Browser --> WAF
    WAF --> TLS
    TLS --> AuthMiddleware
    AuthMiddleware --> JWT
    JWT --> RBAC
    RBAC --> ValidationLayer
    ValidationLayer --> API
    API --> Encryption
    API --> Secrets
    API --> PII
    API --> Logs
    Logs --> Alerts
    
    style WAF fill:#FF5722
    style JWT fill:#4CAF50
    style Encryption fill:#9C27B0
    style Logs fill:#FF9800
```

---

## Monitoring & Observability

```mermaid
graph TB
    subgraph "Application"
        API[FastAPI Backend]
        Worker[Celery Workers]
        Frontend[React Frontend]
    end
    
    subgraph "Metrics Collection"
        Prometheus[Prometheus]
        CloudWatch[CloudWatch Metrics]
    end
    
    subgraph "Logging"
        AppLogs[Application Logs<br/>Structured JSON]
        AccessLogs[Access Logs<br/>ALB]
        ErrorLogs[Error Logs<br/>Sentry]
    end
    
    subgraph "Tracing"
        OpenTelemetry[OpenTelemetry]
        Jaeger[Jaeger<br/>Distributed Tracing]
    end
    
    subgraph "Visualization"
        Grafana[Grafana Dashboards]
        Kibana[Kibana<br/>Log Analysis]
        Sentry[Sentry<br/>Error Tracking]
    end
    
    subgraph "Alerting"
        PagerDuty[PagerDuty]
        Slack[Slack Notifications]
    end
    
    API --> Prometheus
    API --> AppLogs
    API --> OpenTelemetry
    Worker --> AppLogs
    Frontend --> ErrorLogs
    
    Prometheus --> Grafana
    AppLogs --> Kibana
    OpenTelemetry --> Jaeger
    
    API --> CloudWatch
    CloudWatch --> Grafana
    
    ErrorLogs --> Sentry
    Sentry --> PagerDuty
    CloudWatch --> Slack
    
    style API fill:#7ED321
    style Grafana fill:#F46800
    style Sentry fill:#362D59
    style PagerDuty fill:#06AC38
```

---

## Development Workflow

```mermaid
flowchart LR
    Dev[Developer] -->|Write Code| Local[Local Development]
    Local -->|Commit| Git[Git Branch]
    Git -->|Push| GitHub[GitHub]
    
    GitHub -->|Trigger| CI[GitHub Actions<br/>CI Pipeline]
    
    CI --> Lint[Run Linters]
    CI --> Test[Run Tests]
    CI --> Build[Build Docker Images]
    
    Test -->|Pass| Build
    Lint -->|Pass| Build
    
    Build -->|Push| ECR[ECR Registry]
    
    Build -->|Success| PR[Pull Request Review]
    PR -->|Approved| Merge[Merge to Main]
    
    Merge -->|Auto Deploy| Staging[Staging Environment]
    
    Staging -->|QA Pass| Approval[Manual Approval]
    Approval -->|Deploy| Prod[Production Environment]
    
    Prod -->|Monitor| Monitoring[Monitoring & Alerts]
    
    style Dev fill:#4A90E2
    style CI fill:#00C853
    style PR fill:#FF9800
    style Prod fill:#D50000
```

---

**Legend:**
- 🟦 Blue: Client/Frontend
- 🟩 Green: Backend Services
- 🟧 Orange: Workers/Background Jobs
- 🟪 Purple: Databases
- 🟥 Red: External Services
- 🟨 Yellow: AI/ML Components

---

**Last Updated:** October 22, 2025

