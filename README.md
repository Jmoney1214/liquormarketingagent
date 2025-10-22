# Liquor Marketing Agent

> AI-powered liquor retail marketing automation platform

## 🎯 Overview

The Liquor Marketing Agent is an intelligent marketing automation system that uses AI to optimize customer engagement, increase revenue, and reduce churn for liquor retailers. The system combines customer behavior analysis, AI-powered campaign planning, and multi-channel message delivery.

### Current Status

**CLI Version (v1.0)** - ✅ Complete and functional
- Customer scoring and action generation
- AI-powered weekly campaign planning
- Email/SMS message sending

**Web Application (v2.0)** - 📋 Architecture complete, ready for implementation
- Full-stack web application with React frontend and FastAPI backend
- Real-time analytics dashboard
- Visual campaign builder
- Advanced customer segmentation

---

## 📚 Documentation

### 🚀 **[Quick Start Guide](docs/QUICK_START_GUIDE.md)**
**Start here!** Get up and running in 5 minutes. Perfect for developers new to the project.

### 🏗️ **[Frontend & Backend Architecture Plan](docs/FRONTEND_BACKEND_PLAN.md)**
Complete technical architecture including:
- System architecture overview
- Backend services (FastAPI, PostgreSQL, Celery)
- Frontend design (React, TypeScript, Tailwind)
- Database schema
- Security & deployment strategy
- Technology stack
- 14-week implementation plan

### 📡 **[API Specification](docs/API_SPECIFICATION.md)**
Detailed API documentation:
- REST endpoints with request/response examples
- Data models and schemas
- WebSocket events
- Authentication flow
- Error handling

### 🗂️ **[Project Structure](docs/PROJECT_STRUCTURE.md)**
Complete directory structure:
- Backend organization
- Frontend architecture
- File locations
- Docker setup
- Environment configuration

### 📅 **[Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)**
Sprint-by-sprint development plan:
- 7 sprints (14 weeks)
- User stories with acceptance criteria
- Technical tasks breakdown
- Risk management
- Success metrics

### 📊 **[Architecture Diagrams](docs/ARCHITECTURE_DIAGRAM.md)**
Visual system architecture:
- System overview
- Data flow diagrams
- Database schema (ERD)
- Deployment architecture
- Security architecture
- Monitoring setup

---

## 🚀 Quick Start (CLI Version)

### Prerequisites
- Python 3.11+
- OpenAI API key (optional, falls back to heuristics)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/liquor-marketing-agent.git
cd liquor-marketing-agent

# Install dependencies
pip install -e .[openai,dev]

# Copy sample data
cp sample_data/* data/
```

### Usage

#### 1. Generate Customer Actions
```bash
liquor-subagent \
  --kb data/agent_knowledge_base.json \
  --segments data/segment_playbooks.json \
  --out outputs/subagent_actions.json \
  --limit 300
```

#### 2. Create Weekly Campaign Plan
```bash
liquor-plan \
  --actions outputs/subagent_actions.json \
  --out outputs/weekly_plan.json
```

#### 3. Send Messages (Preview Mode)
```bash
liquor-send \
  --plan outputs/weekly_plan.json \
  --mode email \
  --limit 10
```

#### 4. Send Messages (Live with Providers)
```bash
# Set environment variables
export ENABLE_PROVIDERS=1
export MAILGUN_API_KEY=your_key
export MAILGUN_DOMAIN=mg.yourdomain.com
export TWILIO_ACCOUNT_SID=your_sid
export TWILIO_AUTH_TOKEN=your_token
export TWILIO_FROM_NUMBER=+1234567890

# Send for real
liquor-send --plan outputs/weekly_plan.json --mode both --limit 50
```

---

## 🌟 Features

### Current (CLI)
- ✅ **Customer Scoring** - Prioritize customers by churn risk, behavior, and value
- ✅ **AI Campaign Planning** - GPT-4 powered weekly campaign optimization
- ✅ **Multi-channel Messaging** - Email (Mailgun) and SMS (Twilio) delivery
- ✅ **Segment Playbooks** - Targeted offers based on customer segments
- ✅ **Heuristic Fallback** - Works without AI when needed

### Planned (Web Application)
- 📋 **Web Dashboard** - Real-time KPI monitoring and campaign tracking
- 📋 **Visual Campaign Builder** - Drag-and-drop campaign creation
- 📋 **Customer Management** - Import, segment, and analyze customers
- 📋 **Advanced Analytics** - Cohort analysis, funnel tracking, revenue attribution
- 📋 **Template Editor** - Create and customize message templates
- 📋 **A/B Testing** - Test offers and messages for optimization
- 📋 **Real-time Updates** - WebSocket-powered live status tracking
- 📋 **Role-based Access** - Admin, manager, and user permissions

---

## 🏗️ Architecture

### System Components

```
┌─────────────┐
│   Browser   │ ← React + TypeScript Frontend
└──────┬──────┘
       │ REST API / WebSocket
┌──────▼──────────────┐
│   FastAPI Backend   │ ← Python API + Background Jobs
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│  PostgreSQL + Redis │ ← Data + Cache
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│  OpenAI + Mailgun   │ ← External Services
│     + Twilio        │
└─────────────────────┘
```

### Tech Stack

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL + TimescaleDB
- Redis (cache & queue)
- Celery (background jobs)
- SQLAlchemy 2.0

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui
- TanStack Query (data fetching)
- Recharts (visualization)

**External Services:**
- OpenAI GPT-4 (AI planning)
- Mailgun (email)
- Twilio (SMS)

---

## 📊 How It Works

### 1. Customer Scoring
```python
# Existing logic in subagent.py
score = 0
if churn_risk == "high": score += 50
if success_rate < 50%: score += 15
if night_buyer: score += 5
# Returns prioritized list of customers
```

### 2. AI Campaign Planning
```python
# Existing logic in orchestrator.py
1. Take top 300 scored customers
2. Send to GPT-4 with segment playbooks
3. Generate optimized 7-day send schedule
4. Assign offers, timing, and channels
```

### 3. Message Delivery
```python
# Existing logic in pusher.py + sender.py
1. Render email/SMS from templates
2. Queue sends via Celery
3. Deliver via Mailgun/Twilio
4. Track delivery events via webhooks
```

---

## 🚀 Next Steps - Building the Web Application

### For Developers

1. **Read the Architecture**
   - [Frontend & Backend Plan](docs/FRONTEND_BACKEND_PLAN.md)
   - [API Specification](docs/API_SPECIFICATION.md)

2. **Setup Development Environment**
   - Follow [Quick Start Guide](docs/QUICK_START_GUIDE.md)
   - Review [Project Structure](docs/PROJECT_STRUCTURE.md)

3. **Start Development**
   - See [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)
   - Sprint 1: Backend foundation + Authentication
   - Sprint 2: Customer management
   - Sprint 3: Campaign management
   - And so on...

### For Project Managers

1. Review [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)
2. Create JIRA/Linear tickets from user stories
3. Assign tasks to team members
4. Track progress using sprint goals

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Read the [Quick Start Guide](docs/QUICK_START_GUIDE.md)
2. Pick a task from the [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)
3. Create a feature branch
4. Write tests
5. Submit a pull request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🆘 Support

- **Documentation:** Check the `/docs` folder
- **Issues:** [GitHub Issues](https://github.com/yourusername/liquor-marketing-agent/issues)
- **Questions:** Open a discussion on GitHub

---

## 🎉 Project Status

| Component | Status | Version |
|-----------|--------|---------|
| CLI Tools | ✅ Complete | v1.0 |
| Architecture Docs | ✅ Complete | v1.0 |
| Backend API | 📋 Planned | v2.0 |
| Frontend UI | 📋 Planned | v2.0 |
| Production Deploy | ⏳ Future | v2.0 |

**Ready to build?** Start with the [Quick Start Guide](docs/QUICK_START_GUIDE.md)! 🚀

---

## 📦 Repository Structure

```
liquor-marketing-agent/
├── docs/                   # 📚 Complete documentation
│   ├── QUICK_START_GUIDE.md
│   ├── FRONTEND_BACKEND_PLAN.md
│   ├── API_SPECIFICATION.md
│   ├── PROJECT_STRUCTURE.md
│   ├── IMPLEMENTATION_ROADMAP.md
│   └── ARCHITECTURE_DIAGRAM.md
│
├── src/liquor_agent/       # Current CLI tools (v1.0)
│   ├── subagent.py         # Customer scoring
│   ├── orchestrator.py     # AI planning
│   ├── sender.py           # Message sending
│   └── pusher.py           # Email/SMS delivery
│
├── data/                   # Customer & segment data
├── outputs/                # Generated plans
└── sample_data/            # Example data

# Future additions (v2.0):
# ├── backend/              # FastAPI application
# └── frontend/             # React application
```

---

**Last Updated:** October 22, 2025 | **Version:** 1.0
