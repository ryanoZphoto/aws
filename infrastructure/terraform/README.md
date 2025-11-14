# Infrastructure as Code - Terraform

This directory contains Terraform configurations for deploying the AWS Automation Platform.

## Prerequisites

- Terraform >= 1.5.0
- AWS CLI configured with appropriate credentials
- S3 bucket for Terraform state (configure in `main.tf`)

## Setup

1. Copy `terraform.tfvars.example` to `terraform.tfvars`:
```bash
cp terraform.tfvars.example terraform.tfvars
```

2. Edit `terraform.tfvars` with your values.

3. Initialize Terraform:
```bash
terraform init
```

4. Review the plan:
```bash
terraform plan
```

5. Apply the configuration:
```bash
terraform apply
```

## Resources Created

- VPC with public and private subnets
- RDS PostgreSQL instance
- ElastiCache Redis cluster
- ECS cluster (ready for service deployment)
- Security groups and networking
- IAM roles for ECS tasks

## Notes

- The ECS service definition is commented out as it requires a container image
- Configure Terraform backend S3 bucket in `main.tf`
- RDS password is generated randomly and stored in Terraform state
- For production, enable deletion protection and final snapshots
