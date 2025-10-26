# Project Structure Blueprint

## Complete Directory Structure

```
liquor-marketing-agent/
├── README.md
├── LICENSE
├── Makefile
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── backend/                                    # NEW: Backend API
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   │
│   ├── alembic/                                # Database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 001_initial_schema.py
│   │       ├── 002_add_campaigns.py
│   │       └── ...
│   │
│   ├── src/
│   │   └── liquor_agent/
│   │       ├── __init__.py
│   │       │
│   │       ├── api/                            # FastAPI routes
│   │       │   ├── __init__.py
│   │       │   ├── main.py                     # FastAPI app entry
│   │       │   ├── deps.py                     # Dependencies (auth, db)
│   │       │   └── v1/
│   │       │       ├── __init__.py
│   │       │       ├── auth.py                 # Auth endpoints
│   │       │       ├── customers.py            # Customer endpoints
│   │       │       ├── campaigns.py            # Campaign endpoints
│   │       │       ├── actions.py              # Action endpoints
│   │       │       ├── segments.py             # Segment endpoints
│   │       │       ├── analytics.py            # Analytics endpoints
│   │       │       ├── sends.py                # Send endpoints
│   │       │       └── settings.py             # Settings endpoints
│   │       │
│   │       ├── models/                         # SQLAlchemy models
│   │       │   ├── __init__.py
│   │       │   ├── base.py                     # Base model
│   │       │   ├── user.py
│   │       │   ├── customer.py
│   │       │   ├── segment.py
│   │       │   ├── campaign.py
│   │       │   ├── action.py
│   │       │   ├── send.py
│   │       │   ├── template.py
│   │       │   └── analytics_event.py
│   │       │
│   │       ├── schemas/                        # Pydantic schemas
│   │       │   ├── __init__.py
│   │       │   ├── user.py
│   │       │   ├── customer.py
│   │       │   ├── segment.py
│   │       │   ├── campaign.py
│   │       │   ├── action.py
│   │       │   ├── send.py
│   │       │   └── common.py                   # Shared schemas
│   │       │
│   │       ├── services/                       # Business logic
│   │       │   ├── __init__.py
│   │       │   ├── customer_service.py
│   │       │   ├── campaign_service.py
│   │       │   ├── segment_service.py
│   │       │   ├── messaging_service.py
│   │       │   ├── analytics_service.py
│   │       │   └── ai_orchestrator.py          # AI planning
│   │       │
│   │       ├── core/                           # Core utilities
│   │       │   ├── __init__.py
│   │       │   ├── config.py                   # Settings
│   │       │   ├── database.py                 # DB connection
│   │       │   ├── security.py                 # Auth & JWT
│   │       │   ├── cache.py                    # Redis cache
│   │       │   └── logging.py                  # Logging config
│   │       │
│   │       ├── workers/                        # Background jobs
│   │       │   ├── __init__.py
│   │       │   ├── celery_app.py               # Celery config
│   │       │   ├── tasks.py                    # Celery tasks
│   │       │   ├── email_worker.py
│   │       │   ├── sms_worker.py
│   │       │   └── segment_worker.py
│   │       │
│   │       ├── integrations/                   # External APIs
│   │       │   ├── __init__.py
│   │       │   ├── mailgun.py
│   │       │   ├── twilio.py
│   │       │   ├── sendgrid.py
│   │       │   └── openai_client.py
│   │       │
│   │       └── utils/                          # Helpers
│   │           ├── __init__.py
│   │           ├── scoring.py                  # Customer scoring
│   │           ├── validators.py
│   │           └── formatters.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py                         # Pytest fixtures
│       ├── test_api/
│       │   ├── test_auth.py
│       │   ├── test_customers.py
│       │   ├── test_campaigns.py
│       │   └── ...
│       ├── test_services/
│       │   ├── test_customer_service.py
│       │   └── ...
│       └── test_workers/
│           └── test_tasks.py
│
├── frontend/                                   # NEW: React frontend
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   ├── Dockerfile
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── logo.png
│   │
│   ├── src/
│   │   ├── main.tsx                            # App entry
│   │   ├── App.tsx
│   │   ├── router.tsx                          # React Router config
│   │   ├── vite-env.d.ts
│   │   │
│   │   ├── assets/                             # Static assets
│   │   │   ├── images/
│   │   │   └── fonts/
│   │   │
│   │   ├── components/                         # Reusable components
│   │   │   ├── ui/                             # shadcn/ui components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   └── ...
│   │   │   │
│   │   │   ├── layout/                         # Layout components
│   │   │   │   ├── AppLayout.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Footer.tsx
│   │   │   │
│   │   │   ├── customers/                      # Customer components
│   │   │   │   ├── CustomerTable.tsx
│   │   │   │   ├── CustomerCard.tsx
│   │   │   │   ├── CustomerForm.tsx
│   │   │   │   └── CustomerImportModal.tsx
│   │   │   │
│   │   │   ├── campaigns/                      # Campaign components
│   │   │   │   ├── CampaignCard.tsx
│   │   │   │   ├── CampaignBuilder.tsx
│   │   │   │   ├── CampaignTimeline.tsx
│   │   │   │   └── CampaignMetrics.tsx
│   │   │   │
│   │   │   ├── segments/                       # Segment components
│   │   │   │   ├── SegmentCard.tsx
│   │   │   │   ├── SegmentRuleBuilder.tsx
│   │   │   │   └── SegmentPerformance.tsx
│   │   │   │
│   │   │   ├── analytics/                      # Analytics components
│   │   │   │   ├── KPICard.tsx
│   │   │   │   ├── RevenueChart.tsx
│   │   │   │   ├── CohortTable.tsx
│   │   │   │   └── FunnelChart.tsx
│   │   │   │
│   │   │   └── forms/                          # Form components
│   │   │       ├── CustomerForm.tsx
│   │   │       ├── CampaignForm.tsx
│   │   │       └── SegmentForm.tsx
│   │   │
│   │   ├── features/                           # Feature modules
│   │   │   ├── auth/
│   │   │   │   ├── components/
│   │   │   │   │   ├── LoginForm.tsx
│   │   │   │   │   └── RegisterForm.tsx
│   │   │   │   ├── hooks/
│   │   │   │   │   └── useAuth.ts
│   │   │   │   └── pages/
│   │   │   │       ├── LoginPage.tsx
│   │   │   │       └── RegisterPage.tsx
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── components/
│   │   │   │   │   ├── DashboardKPIs.tsx
│   │   │   │   │   ├── RecentActivity.tsx
│   │   │   │   │   └── ActiveCampaigns.tsx
│   │   │   │   └── pages/
│   │   │   │       └── DashboardPage.tsx
│   │   │   │
│   │   │   ├── customers/
│   │   │   │   ├── components/
│   │   │   │   │   └── ...
│   │   │   │   ├── hooks/
│   │   │   │   │   ├── useCustomers.ts
│   │   │   │   │   └── useCustomerDetail.ts
│   │   │   │   └── pages/
│   │   │   │       ├── CustomersListPage.tsx
│   │   │   │       └── CustomerDetailPage.tsx
│   │   │   │
│   │   │   ├── campaigns/
│   │   │   │   ├── components/
│   │   │   │   ├── hooks/
│   │   │   │   │   └── useCampaigns.ts
│   │   │   │   └── pages/
│   │   │   │       ├── CampaignsListPage.tsx
│   │   │   │       ├── CampaignDetailPage.tsx
│   │   │   │       └── CampaignBuilderPage.tsx
│   │   │   │
│   │   │   ├── segments/
│   │   │   │   └── ...
│   │   │   │
│   │   │   ├── analytics/
│   │   │   │   └── pages/
│   │   │   │       └── AnalyticsPage.tsx
│   │   │   │
│   │   │   └── settings/
│   │   │       └── pages/
│   │   │           └── SettingsPage.tsx
│   │   │
│   │   ├── hooks/                              # Shared hooks
│   │   │   ├── useDebounce.ts
│   │   │   ├── useLocalStorage.ts
│   │   │   ├── useWebSocket.ts
│   │   │   └── useInfiniteScroll.ts
│   │   │
│   │   ├── lib/                                # Utilities
│   │   │   ├── utils.ts                        # General helpers
│   │   │   ├── api-client.ts                   # Axios setup
│   │   │   ├── formatting.ts
│   │   │   └── validation.ts
│   │   │
│   │   ├── services/                           # API services
│   │   │   ├── api.ts                          # Base API config
│   │   │   ├── auth.service.ts
│   │   │   ├── customers.service.ts
│   │   │   ├── campaigns.service.ts
│   │   │   ├── segments.service.ts
│   │   │   └── analytics.service.ts
│   │   │
│   │   ├── stores/                             # State management
│   │   │   ├── auth.store.ts                   # Auth state
│   │   │   ├── app.store.ts                    # Global app state
│   │   │   └── filters.store.ts                # Filter state
│   │   │
│   │   ├── types/                              # TypeScript types
│   │   │   ├── api.types.ts
│   │   │   ├── customer.types.ts
│   │   │   ├── campaign.types.ts
│   │   │   └── common.types.ts
│   │   │
│   │   └── styles/                             # Global styles
│   │       ├── globals.css
│   │       └── themes.css
│   │
│   └── tests/
│       ├── setup.ts
│       ├── unit/
│       └── e2e/
│
├── data/                                       # EXISTING: Data files
│   ├── agent_knowledge_base.json
│   └── segment_playbooks.json
│
├── docs/                                       # EXISTING: Documentation
│   ├── ARCHITECTURE.md
│   ├── FRONTEND_BACKEND_PLAN.md               # NEW
│   ├── API_SPECIFICATION.md                   # NEW
│   ├── PROJECT_STRUCTURE.md                   # NEW (this file)
│   └── DEPLOY_GITHUB.md
│
├── outputs/                                    # EXISTING: CLI outputs
│   ├── weekly_plan.json
│   └── subagent_actions.json
│
├── scripts/                                    # EXISTING: Helper scripts
│   ├── push_with_gh.sh
│   └── push_with_pat.sh
│
└── src/liquor_agent/                          # EXISTING: CLI tools
    ├── __init__.py
    ├── config.py
    ├── dataio.py
    ├── llm_openai.py
    ├── orchestrator.py                        # Keep for backward compat
    ├── subagent.py                            # Keep for backward compat
    ├── pusher.py
    └── sender.py
```

## Migration Strategy

### Phase 1: Keep Existing CLI
The existing CLI tools remain functional in `src/liquor_agent/`:
- `liquor-subagent`
- `liquor-plan`
- `liquor-send`

### Phase 2: New Backend Alongside
Create `backend/` directory with FastAPI that reuses existing logic:
- Import existing `subagent.py` scoring logic
- Import existing `orchestrator.py` planning logic
- Import existing `pusher.py` rendering logic

### Phase 3: New Frontend
Build React frontend in `frontend/` that calls the new API.

### Phase 4: Gradual Migration
- Backend services gradually refactor existing code
- Add database persistence
- Add authentication
- Add new features

## Docker Compose Setup

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: liquor_agent
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: liquor_agent_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://liquor_agent:dev_password@postgres:5432/liquor_agent_dev
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    command: uvicorn liquor_agent.api.main:app --host 0.0.0.0 --port 8000 --reload

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://liquor_agent:dev_password@postgres:5432/liquor_agent_dev
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    command: celery -A liquor_agent.workers.celery_app worker --loglevel=info

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000/api/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host 0.0.0.0

volumes:
  postgres_data:
  redis_data:
```

## Environment Variables

### Backend `.env`
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/liquor_agent
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# OpenAI
OPENAI_API_KEY=sk-...

# Email (Mailgun)
MAILGUN_API_KEY=your-mailgun-key
MAILGUN_DOMAIN=mg.yourdomain.com

# SMS (Twilio)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_FROM_NUMBER=+1234567890

# Features
ENABLE_PROVIDERS=true
ENABLE_ANALYTICS=true

# Monitoring
SENTRY_DSN=https://...
LOG_LEVEL=INFO
```

### Frontend `.env`
```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_APP_NAME=Liquor Marketing Agent
VITE_ENABLE_ANALYTICS=true
```

## Quick Start Commands

### Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn liquor_agent.api.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Full stack with Docker
docker-compose up
```

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests
cd frontend
npm run test:e2e
```

### Production Build
```bash
# Backend
docker build -t liquor-agent-api:latest ./backend

# Frontend
cd frontend
npm run build

# Full stack
docker-compose -f docker-compose.prod.yml up -d
```

## Implementation Checklist

### Week 1-2: Backend Foundation
- [ ] Create backend directory structure
- [ ] Setup FastAPI app skeleton
- [ ] Configure database (PostgreSQL + SQLAlchemy)
- [ ] Setup Alembic migrations
- [ ] Create base models (User, Customer)
- [ ] Implement authentication (JWT)
- [ ] Create basic CRUD endpoints
- [ ] Setup Redis for caching
- [ ] Write initial tests

### Week 3-4: Backend Core Features
- [ ] Campaign models & endpoints
- [ ] Action generation service (integrate existing subagent)
- [ ] Orchestrator service (integrate existing planning)
- [ ] Segment models & endpoints
- [ ] Background job setup (Celery)
- [ ] Message queue integration

### Week 5-6: Frontend Foundation
- [ ] Create React + Vite project
- [ ] Setup Tailwind + shadcn/ui
- [ ] Configure React Router
- [ ] Setup API client (Axios + React Query)
- [ ] Implement authentication flow
- [ ] Create layout components
- [ ] Build dashboard skeleton

### Week 7-8: Frontend Core Features
- [ ] Customer management UI
- [ ] Campaign builder UI
- [ ] Segment management UI
- [ ] Analytics dashboard
- [ ] Real-time updates (WebSocket)

### Week 9-10: Integration & Polish
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation
- [ ] Production deployment

---

**Last Updated:** October 22, 2025


