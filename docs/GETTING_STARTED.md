# Getting Started - Sprint 1 Complete! 🎉

Congratulations! The foundational architecture for the Liquor Marketing Agent v2.0 is now complete!

## ✅ What's Been Built

### Backend (FastAPI)
- ✅ **Project Structure** - Complete backend directory with modular organization
- ✅ **Database Setup** - PostgreSQL with SQLAlchemy 2.0 (async)
- ✅ **Alembic Migrations** - Database migration system configured
- ✅ **Models** - User and Customer models with relationships
- ✅ **Authentication** - JWT-based auth (login, register, token management)
- ✅ **Customer API** - Full CRUD with pagination, filtering, search
- ✅ **Security** - Password hashing, JWT tokens, CORS, protected routes
- ✅ **API Documentation** - Auto-generated at `/docs`

### Frontend (React + TypeScript)
- ✅ **Project Structure** - Vite + React 18 + TypeScript
- ✅ **UI Components** - Button, Input, Card (shadcn/ui style)
- ✅ **Authentication UI** - Login and Register pages with validation
- ✅ **App Layout** - Responsive sidebar navigation
- ✅ **Dashboard** - KPI cards and campaign overview
- ✅ **State Management** - Zustand for auth state
- ✅ **API Client** - Axios with interceptors for auth
- ✅ **Styling** - Tailwind CSS with custom design system

### DevOps
- ✅ **Docker Compose** - Full stack (Postgres, Redis, Backend, Worker)
- ✅ **Dockerfile** - Multi-stage builds for backend
- ✅ **GitHub Actions** - CI/CD pipeline with linting and testing

---

## 🚀 Quick Start

### Prerequisites
```bash
# Required
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

# Optional (for local development without Docker)
- PostgreSQL 15+
- Redis 7+
```

### Option 1: Docker (Recommended)

**Start everything with one command:**

```bash
# 1. Clone and navigate
cd /Users/justinetwaru/Desktop/liquor-marketing-agent

# 2. Start all services
docker-compose up

# 3. In a new terminal, run database migrations
docker-compose exec backend alembic upgrade head

# 4. Access the application
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

**That's it!** The app is running with:
- PostgreSQL database
- Redis cache
- FastAPI backend
- React frontend (when you add it to docker-compose)

### Option 2: Manual Setup

#### Backend Setup

```bash
# 1. Navigate to backend
cd backend/

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Start PostgreSQL and Redis
# (Use Docker or install locally)
docker-compose up postgres redis -d

# 5. Run migrations
alembic upgrade head

# 6. Start backend server
python -m liquor_agent.api.main
# or
uvicorn liquor_agent.api.main:app --reload

# Backend running at http://localhost:8000
```

#### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend/

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# Frontend running at http://localhost:3000
```

---

## 📝 First Steps

### 1. Create Your First User

**Option A: Via UI**
1. Go to http://localhost:3000/register
2. Fill in the registration form
3. Click "Create Account"
4. Login with your credentials

**Option B: Via API**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "SecurePassword123!",
    "full_name": "Admin User"
  }'
```

### 2. Login and Get Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "SecurePassword123!"
  }'
```

### 3. Create Your First Customer

```bash
curl -X POST http://localhost:8000/api/v1/customers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "email": "customer@example.com",
    "name": "John Doe",
    "phone": "+19145551234",
    "rfm_segment": "High_Value_Frequent",
    "churn_risk": "low",
    "total_spent": 1250.00,
    "avg_order_value": 85.50,
    "primary_category": "Whiskey"
  }'
```

### 4. List Customers

```bash
curl http://localhost:8000/api/v1/customers \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🏗️ Project Structure

```
liquor-marketing-agent/
├── backend/                      # FastAPI Backend
│   ├── src/liquor_agent/
│   │   ├── api/                  # API routes
│   │   │   ├── main.py          # FastAPI app
│   │   │   ├── deps.py          # Dependencies (auth)
│   │   │   └── v1/
│   │   │       ├── auth.py      # Auth endpoints
│   │   │       └── customers.py # Customer endpoints
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   └── customer.py
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── core/                 # Core utilities
│   │   │   ├── config.py        # Settings
│   │   │   ├── database.py      # DB connection
│   │   │   └── security.py      # Auth utils
│   │   └── services/             # Business logic
│   ├── alembic/                  # Database migrations
│   ├── tests/                    # Tests
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/              # UI components
│   │   │   └── layout/          # Layout components
│   │   ├── features/
│   │   │   ├── auth/            # Auth pages
│   │   │   └── dashboard/       # Dashboard pages
│   │   ├── lib/                 # Utilities
│   │   ├── services/            # API services
│   │   ├── stores/              # State management
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml            # Docker orchestration
├── .github/workflows/ci.yml     # CI/CD pipeline
└── docs/                         # Documentation
```

---

## 🔧 Development Workflow

### Backend Development

```bash
# Run backend with hot reload
cd backend/
uvicorn liquor_agent.api.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=liquor_agent --cov-report=html

# Create new migration
alembic revision --autogenerate -m "add_campaign_model"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Check code style
black src/
ruff check src/
```

### Frontend Development

```bash
# Run frontend with hot reload
cd frontend/
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Docker Development

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f worker

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build

# Run migrations in Docker
docker-compose exec backend alembic upgrade head

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U liquor_agent -d liquor_agent_dev
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend/

# Run all tests
pytest

# Run with coverage
pytest --cov=liquor_agent --cov-report=html

# Run specific test file
pytest tests/test_api/test_auth.py

# Run specific test
pytest tests/test_api/test_auth.py::test_register_user

# View coverage report
open htmlcov/index.html
```

---

## 📚 API Documentation

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

**Authentication:**
```
POST   /api/v1/auth/register    # Register new user
POST   /api/v1/auth/login       # Login and get token
```

**Customers:**
```
GET    /api/v1/customers        # List customers (paginated)
POST   /api/v1/customers        # Create customer
GET    /api/v1/customers/{id}   # Get customer by ID
PATCH  /api/v1/customers/{id}   # Update customer
DELETE /api/v1/customers/{id}   # Delete customer (soft)
```

---

## 🐛 Troubleshooting

### Backend Issues

**"Connection refused" when connecting to database:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

**"Module not found" errors:**
```bash
# Reinstall dependencies
cd backend/
pip install -r requirements-dev.txt
```

**"Table does not exist" errors:**
```bash
# Run migrations
cd backend/
alembic upgrade head
```

### Frontend Issues

**"Cannot find module" errors:**
```bash
# Reinstall node modules
cd frontend/
rm -rf node_modules package-lock.json
npm install
```

**"CORS" errors:**
```bash
# Check backend CORS settings in backend/src/liquor_agent/core/config.py
# Ensure frontend URL is in CORS_ORIGINS list
```

### Docker Issues

**"Port already in use":**
```bash
# Check what's using the port
lsof -i :8000
lsof -i :5432

# Stop conflicting services or change ports in docker-compose.yml
```

**"Permission denied" errors:**
```bash
# Fix volume permissions
docker-compose down -v
docker-compose up
```

---

## 🔒 Security Notes

### Development
- Default secret key is in `.env` - **DO NOT use in production**
- JWT tokens expire after 1 hour
- Passwords are hashed with bcrypt

### Production Checklist
- [ ] Generate secure SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure proper CORS origins
- [ ] Set up environment variables securely
- [ ] Enable rate limiting
- [ ] Set up monitoring and logging

---

## 📈 Next Steps (Sprint 2)

Now that Sprint 1 is complete, here's what's next:

### Backend
- [ ] Campaign model and API endpoints
- [ ] Segment model and API endpoints
- [ ] Customer import (CSV bulk upload)
- [ ] Customer search (full-text)
- [ ] Integrate existing subagent.py scoring logic

### Frontend
- [ ] Customer list page with table
- [ ] Customer detail page
- [ ] Customer import modal
- [ ] Segment management pages
- [ ] Filters and search UI

### DevOps
- [ ] Add frontend to Docker Compose
- [ ] Setup staging environment
- [ ] Configure environment secrets

See **[Implementation Roadmap](IMPLEMENTATION_ROADMAP.md)** for the complete plan!

---

## 🎉 Congratulations!

You now have a fully functional foundation for the Liquor Marketing Agent v2.0!

**What works:**
- ✅ User registration and login
- ✅ Protected API endpoints with JWT
- ✅ Customer CRUD operations
- ✅ Responsive UI with dark mode support
- ✅ Database migrations
- ✅ Docker development environment
- ✅ CI/CD pipeline

**Ready to continue building?** Check out the [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md) for Sprint 2 tasks!

---

**Questions?** Check the documentation in `/docs` or open an issue on GitHub.

**Last Updated:** October 22, 2025 | **Sprint:** 1 Complete

