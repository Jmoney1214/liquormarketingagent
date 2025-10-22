# Deployment Guide

## 🏠 Local Deployment (Start Using Immediately)

### Quick Start with Docker

```bash
cd /Users/justinetwaru/Desktop/liquor-marketing-agent

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Create your first user via API
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "YourSecurePassword123!",
    "full_name": "Admin User"
  }'
```

**Access the app:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

You can now use the full application on your local machine!

---

## ☁️ Cloud Deployment Options

### **Option 1: Vercel (Frontend) + Railway (Backend) - RECOMMENDED**

**Best for:** Easy setup, free tier, automatic deployments

#### Deploy Backend to Railway

1. **Sign up:** https://railway.app
2. **Create new project** → "Deploy from GitHub repo"
3. **Add services:**
   - PostgreSQL database
   - Redis
   - Backend (from your repo)

4. **Configure backend environment variables:**
```env
DATABASE_URL=postgresql://user:pass@host:5432/db (Railway provides)
REDIS_URL=redis://host:6379 (Railway provides)
SECRET_KEY=generate-a-secure-key-here
JWT_ALGORITHM=HS256
CORS_ORIGINS=https://your-app.vercel.app
OPENAI_API_KEY=your-openai-key
MAILGUN_API_KEY=your-mailgun-key
MAILGUN_DOMAIN=mg.yourdomain.com
```

5. **Deploy:**
```bash
# Railway auto-deploys from GitHub
# Or use Railway CLI
railway login
railway init
railway up
```

Your backend will be at: `https://your-app.railway.app`

#### Deploy Frontend to Vercel

1. **Sign up:** https://vercel.com
2. **Import project** → Connect GitHub repo
3. **Configure:**
   - Root Directory: `frontend`
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Environment variables:**
```env
VITE_API_URL=https://your-backend.railway.app/api/v1
```

5. **Deploy:** Vercel auto-deploys on push to main!

Your frontend will be at: `https://your-app.vercel.app`

**Cost:** FREE for hobby projects!

---

### **Option 2: AWS (Full Control)**

**Best for:** Production workloads, full control, scalability

#### Architecture
```
CloudFront (CDN) → S3 (Frontend)
                → ALB → ECS (Backend)
                      → RDS (PostgreSQL)
                      → ElastiCache (Redis)
```

#### Step 1: Deploy Database

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier liquor-agent-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourSecurePassword \
  --allocated-storage 20
```

#### Step 2: Deploy Backend to ECS

1. **Build and push Docker image:**
```bash
cd backend/

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t liquor-agent-backend .

# Tag and push
docker tag liquor-agent-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/liquor-agent-backend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/liquor-agent-backend:latest
```

2. **Create ECS task definition:**
```json
{
  "family": "liquor-agent-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/liquor-agent-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://..."
        }
      ]
    }
  ]
}
```

3. **Create ECS service with ALB**

#### Step 3: Deploy Frontend to S3 + CloudFront

```bash
cd frontend/

# Build frontend
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name/

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name your-bucket-name.s3.amazonaws.com \
  --default-root-object index.html
```

**Cost:** ~$30-50/month for small workload

---

### **Option 3: DigitalOcean App Platform**

**Best for:** Simple deployment, reasonable pricing

1. **Sign up:** https://www.digitalocean.com
2. **Create App** → Import from GitHub
3. **Configure:**
   - Add PostgreSQL database ($7/month)
   - Add Redis ($7/month)
   - Add backend service (autodeploys)
   - Add frontend static site

4. **Environment variables:** Same as Railway above

5. **Deploy:** Auto-deploys from GitHub!

**Cost:** ~$25/month (database + Redis + app)

---

### **Option 4: Heroku (Easiest)**

**Best for:** Simplicity, quick deployment

#### Deploy Backend

```bash
cd backend/

# Login to Heroku
heroku login

# Create app
heroku create liquor-agent-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Add Redis
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set CORS_ORIGINS=https://your-frontend.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run alembic upgrade head
```

#### Deploy Frontend

```bash
cd frontend/

# Create app
heroku create liquor-agent-frontend

# Add Node.js buildpack
heroku buildpacks:add heroku/nodejs

# Set environment
heroku config:set VITE_API_URL=https://liquor-agent-backend.herokuapp.com/api/v1

# Deploy
git push heroku main
```

**Cost:** ~$16/month (Eco dynos + add-ons)

---

### **Option 5: Render.com**

**Best for:** Heroku alternative, modern platform

1. **Sign up:** https://render.com
2. **Create Blueprint** (render.yaml):

```yaml
services:
  - type: web
    name: liquor-agent-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn liquor_agent.api.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: liquor-agent-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
    
  - type: web
    name: liquor-agent-frontend
    env: static
    buildCommand: "cd frontend && npm install && npm run build"
    staticPublishPath: frontend/dist
    
databases:
  - name: liquor-agent-db
    databaseName: liquor_agent
    user: liquor_agent
```

3. **Push to GitHub** → Render auto-deploys!

**Cost:** ~$20/month (Starter plan)

---

## 🎯 Recommended Setup by Use Case

### Personal/Testing
**→ Local Docker** (Free)
```bash
docker-compose up
```

### Hobby Project
**→ Vercel + Railway** (Free tier)
- Vercel: Frontend hosting
- Railway: Backend + Database

### Small Business
**→ DigitalOcean App Platform** (~$25/month)
- Managed PostgreSQL
- Easy scaling
- Good support

### Production/Scale
**→ AWS** (~$50+/month)
- Full control
- Unlimited scaling
- Advanced features

---

## 🔧 Post-Deployment Setup

### 1. Set up custom domain

**Vercel:**
```bash
vercel domains add yourdomain.com
```

**Railway:**
Settings → Domains → Add custom domain

### 2. Enable HTTPS
All modern platforms (Vercel, Railway, etc.) provide free SSL automatically!

### 3. Configure environment variables

**Critical settings for production:**
```env
# Security
SECRET_KEY=<generate-with-openssl-rand-hex-32>
JWT_ALGORITHM=HS256
CORS_ORIGINS=https://yourdomain.com

# Database (provided by hosting platform)
DATABASE_URL=postgresql://...

# Features
ENABLE_PROVIDERS=true
OPENAI_API_KEY=sk-...
MAILGUN_API_KEY=...
MAILGUN_DOMAIN=mg.yourdomain.com
```

### 4. Run migrations

**Railway/Render:**
```bash
# In dashboard, run one-time job:
alembic upgrade head
```

**Heroku:**
```bash
heroku run alembic upgrade head
```

### 5. Create first admin user

**Via API:**
```bash
curl -X POST https://your-backend.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourdomain.com",
    "password": "SecurePassword123!",
    "full_name": "Admin User"
  }'
```

---

## 📊 Deployment Comparison

| Platform | Difficulty | Cost/Month | Free Tier | Auto-Deploy | Best For |
|----------|-----------|------------|-----------|-------------|----------|
| **Local Docker** | Easy | $0 | N/A | No | Development |
| **Vercel + Railway** | Easy | $0-20 | ✅ Yes | ✅ Yes | Hobby |
| **DigitalOcean** | Medium | $25+ | ❌ No | ✅ Yes | Small business |
| **Render** | Easy | $20+ | ⚠️ Limited | ✅ Yes | Startups |
| **Heroku** | Easy | $16+ | ❌ No | ✅ Yes | Quick deploy |
| **AWS** | Hard | $50+ | ⚠️ 12mo | ❌ No | Production |

---

## 🚀 Quick Deploy Script

For Railway deployment:

```bash
#!/bin/bash
# deploy-railway.sh

echo "🚀 Deploying to Railway..."

# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project (or create new)
railway link

# Add PostgreSQL
railway add --plugin postgresql

# Add Redis
railway add --plugin redis

# Deploy
railway up

echo "✅ Deployment complete!"
echo "📝 Don't forget to:"
echo "   1. Set environment variables in Railway dashboard"
echo "   2. Run migrations: railway run alembic upgrade head"
echo "   3. Create your first user"
```

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Generate secure `SECRET_KEY`
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set proper `CORS_ORIGINS`
- [ ] Use environment variables (never commit secrets)
- [ ] Enable database backups
- [ ] Set up monitoring (Sentry, LogRocket)
- [ ] Configure rate limiting
- [ ] Review security headers
- [ ] Set up firewall rules
- [ ] Enable 2FA for hosting accounts

---

## 📈 Monitoring & Logs

### Vercel
- Analytics built-in
- Logs in dashboard
- Automatic error tracking

### Railway
- Logs in dashboard
- Metrics provided
- Add Sentry for errors

### AWS
- CloudWatch for logs
- X-Ray for tracing
- Custom dashboards

---

## 🆘 Troubleshooting

### "Cannot connect to database"
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Ensure database is running
# Railway/Heroku: Check add-on status
# AWS: Check security groups
```

### "CORS errors"
```bash
# Update CORS_ORIGINS in backend
# Must match frontend URL exactly
CORS_ORIGINS=https://your-app.vercel.app
```

### "Migration failed"
```bash
# Reset and retry
alembic downgrade -1
alembic upgrade head
```

---

## 🎉 You're Ready to Deploy!

**Recommended for immediate use:**

1. **Start locally** (5 minutes):
   ```bash
   docker-compose up
   ```

2. **Deploy to cloud** when ready (30 minutes):
   - Frontend → Vercel (free)
   - Backend → Railway (free tier)

---

**Last Updated:** October 22, 2025

