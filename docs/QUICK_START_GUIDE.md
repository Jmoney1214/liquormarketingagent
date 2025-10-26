# Quick Start Guide - Liquor Marketing Agent

## 🚀 Get Started in 5 Minutes

This guide will help you understand and start developing the Liquor Marketing Agent full-stack application.

---

## 📚 Documentation Index

| Document | Purpose | Read First? |
|----------|---------|-------------|
| **FRONTEND_BACKEND_PLAN.md** | Complete architecture overview | ✅ YES |
| **API_SPECIFICATION.md** | API contracts and data models | 📝 Reference |
| **PROJECT_STRUCTURE.md** | Directory structure & setup | 🛠️ When coding |
| **IMPLEMENTATION_ROADMAP.md** | Sprint-by-sprint plan | 📅 For planning |
| **QUICK_START_GUIDE.md** | This file - Quick reference | 🎯 Start here |

---

## 🎯 What Are We Building?

A **full-stack web application** that uses AI to automate liquor retail marketing campaigns.

### Current State (CLI)
```bash
# Generate actions from customer data
liquor-subagent --kb data/customers.json --out actions.json

# Plan weekly campaign
liquor-plan --actions actions.json --out weekly_plan.json

# Send messages
liquor-send --plan weekly_plan.json
```

### Target State (Web App)
```
┌──────────────────────────────────────────────┐
│  🌐 Web Dashboard                             │
│  ├─ 👥 Customer Management                    │
│  ├─ 🎯 Segment Builder (Visual)              │
│  ├─ 🤖 AI Campaign Planner                    │
│  ├─ 📧 Message Templates                      │
│  ├─ 📊 Real-time Analytics                    │
│  └─ ⚙️  Settings & Configuration              │
└──────────────────────────────────────────────┘
```

---

## 🏗️ Architecture at a Glance

```
┌─────────────┐
│   Browser   │ ← React, TypeScript, Tailwind
└──────┬──────┘
       │ REST API / WebSocket
┌──────▼──────────────┐
│   FastAPI Backend   │ ← Python, FastAPI, Celery
├─────────────────────┤
│  • Auth & Users     │
│  • Customers        │
│  • Campaigns        │
│  • AI Orchestrator  │
│  • Message Queue    │
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│   PostgreSQL DB     │ ← Customer data, campaigns
│   TimescaleDB       │ ← Time-series analytics
│   Redis             │ ← Cache & job queue
└─────────────────────┘
       │
┌──────▼──────────────┐
│  External Services  │
│  • OpenAI (GPT-4)   │ ← AI campaign planning
│  • Mailgun          │ ← Email delivery
│  • Twilio           │ ← SMS delivery
└─────────────────────┘
```

---

## 💻 Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API framework |
| **PostgreSQL** | Database |
| **SQLAlchemy 2.0** | ORM |
| **Alembic** | Migrations |
| **Celery** | Background jobs |
| **Redis** | Cache & queue |
| **Pydantic** | Validation |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI library |
| **TypeScript** | Type safety |
| **Vite** | Build tool |
| **Tailwind CSS** | Styling |
| **shadcn/ui** | Components |
| **TanStack Query** | Data fetching |
| **Recharts** | Charts |
| **Zustand** | State management |

---

## 🛠️ Development Setup

### Prerequisites
```bash
# Required
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)
- Redis (or use Docker)

# Optional
- GitHub CLI (gh)
```

### Quick Start (Docker)
```bash
# 1. Clone the repository
git clone https://github.com/yourorg/liquor-marketing-agent.git
cd liquor-marketing-agent

# 2. Copy environment files
cp .env.example .env
# Edit .env with your API keys

# 3. Start everything with Docker
docker-compose up

# 4. Run migrations
docker-compose exec backend alembic upgrade head

# 5. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup (No Docker)

#### Backend
```bash
# 1. Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -e ".[dev,openai]"

# 3. Setup database
# Start PostgreSQL and Redis locally
createdb liquor_agent_dev

# 4. Run migrations
alembic upgrade head

# 5. Start development server
uvicorn liquor_agent.api.main:app --reload --port 8000

# 6. Start Celery worker (separate terminal)
celery -A liquor_agent.workers.celery_app worker --loglevel=info
```

#### Frontend
```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
# Runs on http://localhost:5173
```

---

## 📋 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/customer-import
```

### 2. Backend Development
```bash
# Create a model
# File: backend/src/liquor_agent/models/customer.py

# Create a schema
# File: backend/src/liquor_agent/schemas/customer.py

# Create an endpoint
# File: backend/src/liquor_agent/api/v1/customers.py

# Write tests
# File: backend/tests/test_api/test_customers.py
pytest tests/test_api/test_customers.py

# Run all tests
pytest
```

### 3. Frontend Development
```bash
# Create a page
# File: frontend/src/features/customers/pages/CustomersListPage.tsx

# Create a component
# File: frontend/src/components/customers/CustomerTable.tsx

# Create an API service
# File: frontend/src/services/customers.service.ts

# Run the app
npm run dev

# Run tests
npm test
```

### 4. Database Migration
```bash
# Auto-generate migration
alembic revision --autogenerate -m "add_customer_table"

# Review the migration file
# Edit: backend/alembic/versions/xxx_add_customer_table.py

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### 5. Commit and Push
```bash
git add .
git commit -m "feat: add customer import functionality"
git push origin feature/customer-import

# Create PR on GitHub
gh pr create --title "Customer Import" --body "Adds bulk customer import"
```

---

## 🔑 Key Concepts

### Customer Scoring
```python
# Logic from existing subagent.py
def score(customer):
    score = 0
    if customer.churn_risk == "high":
        score += 50
    if customer.success_rate < 50:
        score += 15
    if customer.is_night_buyer:
        score += 5
    return score
```

### AI Campaign Planning
```python
# Logic from existing orchestrator.py
def plan_campaign(customers, segments):
    # 1. Generate actions using subagent scoring
    actions = generate_actions(customers)
    
    # 2. Use OpenAI to create 7-day plan
    plan = ai_orchestrator.plan(
        actions=actions,
        segments=segments,
        objective="Lift AOV and win back churn"
    )
    
    # 3. Return optimized send schedule
    return plan
```

### Message Rendering
```python
# Logic from existing pusher.py
def render_email(customer, offer):
    subject = f"{customer.primary_category} • {offer}"
    html = template.render(
        name=customer.name,
        offer=offer,
        segment=customer.segment
    )
    return subject, html
```

---

## 📊 Data Flow

### Campaign Creation Flow
```
1. User creates campaign in UI
   ↓
2. Frontend calls POST /api/v1/campaigns
   ↓
3. Backend creates campaign record
   ↓
4. User clicks "Generate Plan with AI"
   ↓
5. Backend calls OpenAI API (orchestrator logic)
   ↓
6. AI returns optimized 7-day plan
   ↓
7. Backend creates Action records for each send
   ↓
8. User clicks "Start Campaign"
   ↓
9. Actions queued to Celery
   ↓
10. Workers send emails/SMS via Mailgun/Twilio
    ↓
11. Webhooks update delivery status
    ↓
12. Analytics dashboard updates in real-time
```

---

## 🧪 Testing Strategy

### Backend Tests
```bash
# Unit tests
pytest tests/test_services/

# Integration tests
pytest tests/test_api/

# Test with coverage
pytest --cov=liquor_agent --cov-report=html

# View coverage
open htmlcov/index.html
```

### Frontend Tests
```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e

# Run specific test
npm test -- CustomerTable.test.tsx
```

---

## 🚀 Deployment

### Staging Deployment
```bash
# Automatic on push to main branch
git push origin main
# GitHub Actions will:
# 1. Run tests
# 2. Build Docker images
# 3. Push to registry
# 4. Deploy to staging
```

### Production Deployment
```bash
# Manual approval required
# 1. Go to GitHub Actions
# 2. Find "Deploy to Production" workflow
# 3. Click "Approve"
```

---

## 📈 Monitoring

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/health/db

# Redis connection
curl http://localhost:8000/health/redis
```

### Logs
```bash
# Backend logs
docker-compose logs -f backend

# Worker logs
docker-compose logs -f worker

# Frontend logs
docker-compose logs -f frontend
```

### Metrics
```bash
# API metrics
curl http://localhost:8000/metrics

# Celery stats
celery -A liquor_agent.workers.celery_app inspect stats
```

---

## 🐛 Troubleshooting

### Common Issues

#### "Database connection failed"
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check connection string
echo $DATABASE_URL

# Try connecting manually
psql $DATABASE_URL
```

#### "Redis connection failed"
```bash
# Check if Redis is running
docker-compose ps redis

# Try connecting
redis-cli ping
```

#### "OpenAI API error"
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### "Frontend can't connect to API"
```bash
# Check CORS settings in backend
# File: backend/src/liquor_agent/api/main.py

# Check frontend API URL
cat frontend/.env | grep VITE_API_URL
```

---

## 📚 Learning Resources

### FastAPI
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)

### React
- [React Docs](https://react.dev/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Tools
- [shadcn/ui Components](https://ui.shadcn.com/)
- [Recharts Examples](https://recharts.org/en-US/examples)

---

## 🎯 Next Steps

### For Backend Developers
1. ✅ Read **FRONTEND_BACKEND_PLAN.md** (Backend section)
2. ✅ Review **API_SPECIFICATION.md**
3. 🛠️ Start with **Sprint 1: BK-001** in **IMPLEMENTATION_ROADMAP.md**
4. 💻 Setup local environment
5. 🏗️ Create first endpoint (Customer CRUD)

### For Frontend Developers
1. ✅ Read **FRONTEND_BACKEND_PLAN.md** (Frontend section)
2. ✅ Review **API_SPECIFICATION.md** (understand data models)
3. 🛠️ Start with **Sprint 1: FE-001** in **IMPLEMENTATION_ROADMAP.md**
4. 💻 Setup local environment
5. 🏗️ Create login page

### For Project Managers
1. ✅ Read **FRONTEND_BACKEND_PLAN.md** (Executive Summary)
2. ✅ Review **IMPLEMENTATION_ROADMAP.md** (all sprints)
3. 📅 Create JIRA/Linear tickets from user stories
4. 👥 Assign tasks to developers
5. 📊 Setup sprint board

---

## 🤝 Getting Help

### Documentation
- Check the `/docs` folder for detailed guides
- API docs at `http://localhost:8000/docs`

### Team
- Backend questions: #backend-dev
- Frontend questions: #frontend-dev
- DevOps questions: #devops

### External
- GitHub Issues: [Report bugs](https://github.com/yourorg/liquor-marketing-agent/issues)
- Stack Overflow: Tag with `liquor-marketing-agent`

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎉 Ready to Build!

You're all set! Start with **Sprint 1** in the **IMPLEMENTATION_ROADMAP.md** and build something amazing! 🚀

---

**Last Updated:** October 22, 2025
**Version:** 1.0


