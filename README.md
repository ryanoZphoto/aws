# AWS Service Automation & Control Platform

A comprehensive SaaS platform that provides daily automated checks and task execution across all AWS services. Built for autonomy, control, and reliability.

## Architecture Overview

### Tech Stack
- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: Next.js 14+ with TypeScript
- **Database**: PostgreSQL
- **Task Scheduler**: AWS EventBridge + Lambda
- **AWS Integration**: boto3 (Python AWS SDK)
- **Authentication**: JWT tokens
- **Billing**: Stripe integration
- **Infrastructure**: Docker, AWS ECS/Fargate

### Key Features
- ✅ Daily automated checks across all AWS service categories
- ✅ Real-time task execution and monitoring
- ✅ Secure AWS credential management
- ✅ Multi-tenant SaaS architecture
- ✅ Subscription-based billing
- ✅ No fallbacks - errors surface directly to users
- ✅ Real AWS integration - no mock data

## Project Structure

```
/
├── backend/              # FastAPI backend application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core configuration, security
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   │   └── aws/     # AWS service checkers
│   │   └── tasks/       # Task execution engine
│   ├── alembic/         # Database migrations
│   └── requirements.txt
├── frontend/            # Next.js frontend application
│   ├── app/             # Next.js app directory
│   ├── components/      # React components
│   └── package.json
├── infrastructure/      # Infrastructure as code
│   ├── docker-compose.yml
│   └── terraform/       # Optional: Terraform configs
└── docs/                # Documentation

```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker & Docker Compose
- AWS Account with appropriate IAM permissions
- Stripe account (for billing)

### Installation

1. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Frontend Setup**
```bash
cd frontend
npm install
```

3. **Database Setup**
```bash
# Using Docker Compose
docker-compose up -d postgres

# Run migrations
cd backend
alembic upgrade head
```

4. **Environment Variables**
Create `.env` files in both `backend/` and `frontend/` directories (see `.env.example` files)

### Running Locally

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## AWS Service Coverage

The platform supports automated checks and tasks for:

- **Compute**: EC2, Lambda, Lightsail, Batch, Elastic Beanstalk, etc.
- **Containers**: ECS, EKS, ECR
- **Storage**: S3, EFS, FSx, Glacier, Backup
- **Database**: RDS, Aurora, DynamoDB, ElastiCache, Neptune, etc.
- **Networking**: VPC, CloudFront, API Gateway, Route 53
- **Security**: IAM, Cognito, Secrets Manager, GuardDuty, etc.
- **Management**: CloudWatch, CloudFormation, Systems Manager, Config
- **And 100+ more services...**

## Security

- AWS credentials stored encrypted in database
- IAM role assumption support
- JWT-based authentication
- Rate limiting and API security
- Audit logging for all actions

## License

Proprietary - All rights reserved
