# AWS Service Automation & Control Platform

A subscription-based SaaS platform providing daily automated monitoring, checks, and task execution across all AWS services.

## Features

- **Comprehensive AWS Service Coverage**: Supports all major AWS service categories
- **Daily Automated Tasks**: Schedule and execute tasks automatically
- **Real-Time Monitoring**: Track task execution and AWS service health
- **Subscription Management**: Multi-tier subscription plans
- **Error-First Approach**: No fallbacks - errors interrupt execution for immediate attention
- **Real Data Only**: No mock or dummy data - all operations use real AWS APIs

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture documentation.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Task Queue**: Celery
- **AWS SDK**: boto3
- **Frontend**: React + TypeScript
- **Infrastructure**: AWS ECS, API Gateway, CloudWatch

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Node.js 18+ (for frontend)
- AWS Account with appropriate IAM permissions

### Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Set up database:
```bash
alembic upgrade head
```

5. Run development server:
```bash
uvicorn app.main:app --reload --port 8000
```

6. Start Celery worker:
```bash
celery -A app.core.celery_app worker --loglevel=info
```

7. Start Celery beat (scheduler):
```bash
celery -A app.core.celery_app beat --loglevel=info
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
.
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core configuration
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── aws/              # AWS service integrations
│   ├── tasks/            # Celery tasks
│   └── main.py           # FastAPI application
├── frontend/             # React frontend
├── infrastructure/       # Terraform/CloudFormation
├── tests/                # Test suite
└── alembic/              # Database migrations
```

## AWS Service Integration

The platform integrates with all major AWS service categories:

- Compute (EC2, Lambda, ECS, etc.)
- Storage (S3, EFS, etc.)
- Database (RDS, DynamoDB, etc.)
- Networking (VPC, CloudFront, etc.)
- Security (IAM, Cognito, etc.)
- And many more...

See `app/aws/` for service-specific integration modules.

## Error Handling

This platform follows a strict error-handling policy:
- **No Fallbacks**: Errors interrupt execution immediately
- **Detailed Logging**: All errors logged to CloudWatch
- **User Notifications**: Users are immediately notified of failures
- **Error Categorization**: Errors classified by type (auth, permissions, limits, etc.)

## Subscription Plans

The platform offers tiered subscription plans with different:
- Task execution limits
- AWS service coverage
- Support levels
- Custom task capabilities

## Development

### Running Tests

```bash
pytest tests/ -v --cov=app
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Deployment

See `infrastructure/` for Infrastructure as Code (Terraform/CloudFormation) templates.

## License

Proprietary - All rights reserved

## Support

For issues and questions, please contact support.
