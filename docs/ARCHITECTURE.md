# Architecture Documentation

## System Overview

The AWS Service Automation & Control Platform is a multi-tenant SaaS application that provides daily automated checks and task execution across all AWS services.

## Architecture Components

### Backend (FastAPI)

**Technology Stack:**
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Task Queue**: Celery with Redis
- **Authentication**: JWT tokens
- **AWS Integration**: boto3 SDK

**Key Modules:**

1. **API Layer** (`app/api/v1/`)
   - RESTful API endpoints
   - Authentication and authorization
   - Request/response validation

2. **Service Layer** (`app/services/aws/`)
   - AWS service checkers organized by category
   - Base checker class with error handling
   - Support for all major AWS services

3. **Task Execution** (`app/tasks/`)
   - Task executor engine
   - Celery integration for scheduling
   - Daily/weekly/monthly task execution

4. **Data Models** (`app/models/`)
   - User management
   - Task definitions
   - AWS credentials (encrypted)
   - Subscriptions
   - Execution results

5. **Security** (`app/core/security.py`)
   - Password hashing (bcrypt)
   - JWT token generation/validation
   - AWS credentials encryption (Fernet)

### Frontend (Next.js)

**Technology Stack:**
- **Framework**: Next.js 14+ with TypeScript
- **State Management**: Zustand + React Query
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

**Key Features:**
- User authentication
- Task management dashboard
- AWS credentials management
- Execution results visualization
- Subscription management

### Infrastructure

**Components:**
- PostgreSQL database
- Redis for Celery broker/backend
- Docker containers for all services
- Optional: AWS ECS/Fargate for production

## Data Flow

### Task Execution Flow

1. **Task Creation**: User creates a task via API/Frontend
2. **Scheduling**: Celery Beat schedules tasks based on frequency
3. **Execution**: Celery Worker picks up task
4. **AWS API Call**: Task executor uses appropriate AWS service checker
5. **Result Storage**: Results stored in database
6. **Error Handling**: Errors are recorded (no fallbacks)

### Authentication Flow

1. User logs in with email/password
2. Backend validates credentials
3. JWT token generated and returned
4. Frontend stores token
5. Subsequent requests include token in Authorization header
6. Backend validates token on each request

### AWS Credentials Flow

1. User provides AWS credentials
2. Credentials encrypted using Fernet (symmetric encryption)
3. Encrypted credentials stored in database
4. On task execution, credentials decrypted
5. Credentials used to create boto3 session
6. AWS API calls made with session

## Database Schema

### Users Table
- User accounts with authentication
- Links to subscriptions and tasks

### Tasks Table
- Task definitions
- AWS service and operation
- Frequency and configuration
- Active status

### Task Executions Table
- Execution records
- Status (pending, running, success, failed)
- Timestamps
- Error messages

### Task Results Table
- Execution result data (JSON)
- Links to executions

### AWS Credentials Table
- Encrypted AWS credentials
- IAM role ARN support
- Default credential flag

### Subscriptions Table
- Subscription tiers
- Stripe integration
- Billing periods

## Security Architecture

### Credential Storage
- AWS credentials encrypted at rest using Fernet
- Encryption key stored in environment variable
- No plaintext credentials in database

### Authentication
- JWT tokens with expiration
- Password hashing with bcrypt
- Token validation on every request

### API Security
- CORS configuration
- Rate limiting (can be added)
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers (can run multiple instances)
- Celery workers can scale horizontally
- Database connection pooling
- Redis for distributed task queue

### Performance Optimization
- Database indexing on frequently queried fields
- Connection pooling for database
- Async/await for I/O operations
- Caching strategies (can be added)

### Multi-Tenancy
- User-based data isolation
- Per-user AWS credentials
- Subscription-based feature access

## Error Handling Philosophy

**No Fallbacks Rule:**
- Errors interrupt execution
- Errors are logged and stored
- Users see actual error messages
- No silent failures or default values
- Real AWS errors surface to users

## AWS Service Coverage

The platform supports automated checks for:

- **Compute**: EC2, Lambda, Lightsail, Batch, Elastic Beanstalk
- **Storage**: S3, EFS, FSx, Glacier, Backup
- **Database**: RDS, Aurora, DynamoDB, ElastiCache, Neptune
- **Networking**: VPC, CloudFront, API Gateway, Route 53
- **Security**: IAM, Cognito, Secrets Manager, GuardDuty
- **Management**: CloudWatch, CloudFormation, Systems Manager

And can be extended to support any AWS service via boto3.

## Deployment Architecture

### Development
- Docker Compose for local development
- Hot reload for backend and frontend
- Local PostgreSQL and Redis

### Production (Recommended)
- AWS ECS/Fargate for containers
- RDS for PostgreSQL
- ElastiCache for Redis
- Application Load Balancer
- CloudFront for frontend CDN
- Route 53 for DNS
- CloudWatch for monitoring

## Monitoring & Logging

### Logging
- Structured logging with structlog
- Log levels: INFO, WARNING, ERROR
- Task execution logs
- API request logs

### Monitoring (Can be added)
- CloudWatch metrics
- Error tracking (Sentry)
- Performance monitoring
- Task execution metrics

## Future Enhancements

- Real-time notifications (WebSockets)
- Email/SMS alerts for task failures
- Advanced task scheduling (cron expressions)
- Task templates and presets
- Multi-region support
- Cost tracking and optimization
- Compliance reporting
- API rate limiting
- Webhook integrations
