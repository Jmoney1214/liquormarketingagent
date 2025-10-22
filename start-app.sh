#!/bin/bash
echo "🚀 Starting Liquor Marketing Agent..."
echo ""

# Start Docker services
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Run migrations
docker-compose exec -T backend alembic upgrade head

echo ""
echo "✅ App is ready!"
echo ""
echo "📱 Access your app at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "👤 Create your first user:"
echo '   curl -X POST http://localhost:8000/api/v1/auth/register \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"email": "admin@example.com", "password": "YourPassword123!", "full_name": "Admin"}'"'"
echo ""
