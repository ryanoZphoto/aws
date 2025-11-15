# Deployment Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Docker and Docker Compose (for local development)
- AWS Account with appropriate permissions
- Terraform >= 1.5.0 (for infrastructure deployment)

## Local Development Setup

### 1. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development services (PostgreSQL, Redis)
make dev-up

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
make upgrade

# Start FastAPI server
make run-server

# In separate terminals, start Celery worker and beat
make run-worker
make run-beat
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000
The API will be available at http://localhost:8000

## Production Deployment

### 1. Infrastructure Deployment (Terraform)

```bash
cd infrastructure/terraform

# Configure variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars

# Initialize and apply
terraform init
terraform plan
terraform apply
```

### 2. Build and Push Container Image

```bash
# Build Docker image
docker build -t aws-automation-platform:latest .

# Tag for ECR
docker tag aws-automation-platform:latest <account-id>.dkr.ecr.<region>.amazonaws.com/aws-automation-platform:latest

# Push to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/aws-automation-platform:latest
```

### 3. Deploy ECS Service

Update the ECS service definition in `infrastructure/terraform/ecs.tf` with your container image and deploy.

### 4. Environment Variables

Set environment variables in ECS task definition:
- `DATABASE_URL`: From RDS endpoint
- `REDIS_URL`: From ElastiCache endpoint
- `SECRET_KEY`: Generate a secure random key
- Other variables from `.env.example`

## Database Migrations

Run migrations in production:

```bash
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql+asyncpg://user:pass@rds-endpoint:5432/aws_automation"

# Run migrations
alembic upgrade head
```

## Monitoring

- CloudWatch Logs: `/aws/automation-platform`
- CloudWatch Metrics: ECS task metrics
- Application logs: Structured JSON logs via structlog

## Security Considerations

1. **AWS Credentials**: Users' AWS credentials are encrypted at rest using SQLAlchemy-utils
2. **Database**: RDS in private subnets, encrypted at rest
3. **Redis**: ElastiCache with encryption at rest
4. **Network**: VPC with private subnets for application resources
5. **Secrets**: Use AWS Secrets Manager for sensitive configuration

## Scaling

- **ECS**: Adjust `desired_count` in ECS service
- **RDS**: Enable read replicas for read-heavy workloads
- **Redis**: Use ElastiCache cluster mode for scaling
- **Celery Workers**: Scale ECS tasks running worker containers

## Backup and Recovery

- **RDS**: Automated backups enabled (7-day retention)
- **Terraform State**: Stored in S3 with versioning
- **Application Data**: Regular database backups recommended

## Troubleshooting

### Database Connection Issues
- Check security group rules
- Verify RDS endpoint and credentials
- Check VPC/subnet configuration

### Celery Tasks Not Executing
- Verify Redis connection
- Check Celery worker logs
- Verify task registration

### AWS API Errors
- Check IAM permissions for user's AWS credentials
- Verify service availability in region
- Check rate limits and quotas
