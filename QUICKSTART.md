# Quick Start Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 14+ (or use Docker)
- Redis 6+ (or use Docker)

## 5-Minute Setup

### 1. Clone and Setup

```bash
# Run the setup script
./setup.sh
```

This will:
- Create a virtual environment
- Install Python dependencies
- Create `.env` file from template
- Start PostgreSQL and Redis via Docker
- Run database migrations

### 2. Configure Environment

Edit `.env` file with your settings:

```bash
# Minimum required settings
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/aws_automation
REDIS_URL=redis://localhost:6379/0
REDIS_CELERY_URL=redis://localhost:6379/1
SECRET_KEY=your-secret-key-here-min-32-chars
```

### 3. Start Backend Services

Terminal 1 - API Server:
```bash
source venv/bin/activate
make run-server
```

Terminal 2 - Celery Worker:
```bash
source venv/bin/activate
make run-worker
```

Terminal 3 - Celery Beat (Scheduler):
```bash
source venv/bin/activate
make run-beat
```

### 4. Start Frontend

Terminal 4:
```bash
cd frontend
npm install
npm run dev
```

### 5. Access the Application

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## First Steps

1. **Register a User**
   - Go to http://localhost:3000/login
   - Click "Register" (or use API: `POST /api/v1/auth/register`)

2. **Add AWS Credentials**
   - Navigate to AWS Credentials section
   - Add your AWS Access Key ID and Secret Access Key
   - Set as default if this is your primary account

3. **Create a Task**
   - Go to Tasks section
   - Create a new task:
     - Name: "EC2 Health Check"
     - Service Category: "compute"
     - Service: "ec2"
     - Task Type: "health_check"
     - Frequency: "daily"

4. **Execute Task**
   - Click "Execute" on your task
   - View execution results in the Executions tab

## Example API Calls

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "securepassword",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepassword"
```

### Create Task (with token)
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "S3 Bucket List",
    "aws_service_category": "storage",
    "aws_service": "s3",
    "task_type": "resource_list",
    "configuration": {},
    "frequency": "daily"
  }'
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running: `docker-compose ps`
- Check DATABASE_URL in `.env`
- Verify database exists: `psql -U user -d aws_automation`

### Redis Connection Error
- Ensure Redis is running: `docker-compose ps`
- Check REDIS_URL in `.env`
- Test connection: `redis-cli ping`

### Celery Tasks Not Executing
- Verify Celery worker is running
- Check Redis connection
- Review worker logs for errors

### AWS API Errors
- Verify AWS credentials are correct
- Check IAM permissions
- Ensure credentials have necessary permissions

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) for architecture details
- Read [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
- Read [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) for full feature overview
