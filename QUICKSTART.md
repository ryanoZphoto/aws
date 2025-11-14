# Quick Start Guide

Get the AWS Service Automation & Control Platform running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (need 3.11+)
python --version

# Check Node.js version (need 18+)
node --version

# Check if Docker is installed
docker --version
docker-compose --version
```

## Quick Setup with Docker Compose

### 1. Generate Required Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 2. Configure Backend

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and set:
- `SECRET_KEY` (from step 1)
- `ENCRYPTION_KEY` (from step 1)
- Other values as needed

### 3. Configure Frontend

```bash
cd frontend
cp .env.example .env
```

Edit `frontend/.env` - usually defaults are fine for local development.

### 4. Start Everything

```bash
cd infrastructure
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Celery Worker
- Celery Beat Scheduler

### 5. Initialize Database

```bash
cd ../backend
# If using Docker, exec into container:
docker exec -it aws-automation-backend alembic upgrade head

# Or if running locally:
source venv/bin/activate
alembic upgrade head
```

### 6. Start Frontend (Optional - for UI)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:3000

## Create Your First User

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "SecurePassword123!",
    "full_name": "Admin User"
  }'
```

## Login and Get Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=SecurePassword123!"
```

Save the `access_token` from the response.

## Add AWS Credentials

```bash
curl -X POST "http://localhost:8000/api/v1/aws-credentials/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My AWS Account",
    "aws_access_key_id": "YOUR_AWS_ACCESS_KEY",
    "aws_secret_access_key": "YOUR_AWS_SECRET_KEY",
    "aws_region": "us-east-1",
    "is_default": true
  }'
```

## Create Your First Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Check EC2 Instances",
    "description": "Daily check of all EC2 instances",
    "aws_service": "ec2",
    "aws_operation": "describe_instances",
    "frequency": "daily",
    "is_active": true
  }'
```

## Execute Task Manually

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/TASK_ID/execute" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## View Task Executions

```bash
curl "http://localhost:8000/api/v1/tasks/TASK_ID/executions" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Access API Documentation

Open your browser to: http://localhost:8000/api/v1/docs

This provides an interactive Swagger UI to test all endpoints.

## Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery-worker
```

### Stop Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
```

### Check Service Status

```bash
docker-compose ps
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check DATABASE_URL in backend/.env

### Redis Connection Error
- Ensure Redis container is running
- Check REDIS_URL in backend/.env

### Celery Not Running Tasks
- Check celery-worker logs: `docker-compose logs celery-worker`
- Verify tasks are active in database

### Port Already in Use
- Change ports in docker-compose.yml
- Or stop conflicting services

## Next Steps

1. Explore the API documentation at http://localhost:8000/api/v1/docs
2. Set up more AWS credentials for different accounts
3. Create tasks for different AWS services
4. Monitor task executions
5. Set up Stripe for subscription billing (see SETUP.md)

## Production Deployment

For production, see `docs/SETUP.md` and `docs/ARCHITECTURE.md` for detailed deployment instructions.
