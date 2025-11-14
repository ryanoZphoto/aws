# Setup Guide

## Prerequisites

Before setting up the AWS Service Automation & Control Platform, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **PostgreSQL 14+** installed and running
- **Redis** installed and running (for Celery)
- **Docker & Docker Compose** (optional, for containerized setup)
- **AWS Account** with appropriate IAM permissions
- **Stripe Account** (for subscription billing)

## Installation Steps

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env file with your configuration
# Important: Set SECRET_KEY, ENCRYPTION_KEY, DATABASE_URL, etc.
```

### 2. Database Setup

```bash
# Using Docker Compose (recommended)
cd infrastructure
docker-compose up -d postgres redis

# Or use local PostgreSQL
# Create database
createdb aws_automation

# Run migrations
cd ../backend
alembic upgrade head
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env file
# Set NEXT_PUBLIC_API_URL to your backend URL
```

### 4. Running the Application

#### Option A: Docker Compose (Recommended)

```bash
cd infrastructure
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis
- Backend API server
- Celery worker
- Celery beat scheduler

#### Option B: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Celery Worker:**
```bash
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info
```

**Terminal 3 - Celery Beat:**
```bash
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app beat --loglevel=info
```

**Terminal 4 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs

## Configuration

### Environment Variables

#### Backend (.env)

- `SECRET_KEY`: Secret key for JWT tokens (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- `ENCRYPTION_KEY`: Encryption key for AWS credentials (generate with: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `STRIPE_SECRET_KEY`: Stripe secret key for billing
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook secret

#### Frontend (.env)

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Creating Your First User

You can create a user via the API:

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }'
```

Or use the API documentation at http://localhost:8000/api/v1/docs

## Adding AWS Credentials

1. Login to get an access token
2. Add AWS credentials via the API:

```bash
curl -X POST "http://localhost:8000/api/v1/aws-credentials/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production AWS",
    "aws_access_key_id": "YOUR_ACCESS_KEY",
    "aws_secret_access_key": "YOUR_SECRET_KEY",
    "aws_region": "us-east-1",
    "is_default": true
  }'
```

## Creating Your First Task

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

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running: `pg_isready`
- Check DATABASE_URL format: `postgresql://user:password@host:port/database`
- Verify database exists: `psql -l`

### Redis Connection Issues

- Ensure Redis is running: `redis-cli ping`
- Check REDIS_URL format: `redis://host:port/db`

### Celery Not Running Tasks

- Check Celery worker logs
- Verify Redis connection
- Ensure tasks are active in database

### AWS API Errors

- Verify AWS credentials are correct
- Check IAM permissions for the AWS account
- Ensure the AWS service and operation are valid

## Production Deployment

For production deployment:

1. Set strong SECRET_KEY and ENCRYPTION_KEY
2. Use environment-specific database and Redis
3. Configure proper CORS origins
4. Set up SSL/TLS certificates
5. Use a production-grade WSGI server (e.g., Gunicorn)
6. Configure proper logging and monitoring
7. Set up backup strategies for database
8. Use AWS ECS/Fargate or Kubernetes for container orchestration

## Security Best Practices

- Never commit .env files
- Use strong, unique SECRET_KEY and ENCRYPTION_KEY
- Rotate AWS credentials regularly
- Use IAM roles instead of access keys when possible
- Enable MFA for AWS accounts
- Regularly audit task executions and results
- Monitor for suspicious activity
