# Specialized: AWS Security Audit

## Overview

**Use Case:** Security audit for applications deployed on Amazon Web Services
**Use With:** Phase 7 (Infrastructure), Phase 8 (Secrets Management)
**Estimated Time:** 3-4 hours
**Services Covered:** IAM, S3, EC2, Lambda, RDS, VPC, KMS, CloudTrail, ECS/EKS, API Gateway

---

## Files to Provide

```
[ ] Terraform files (*.tf)
[ ] CloudFormation templates (*.yaml, *.json)
[ ] AWS CDK code
[ ] SAM templates (template.yaml)
[ ] Serverless Framework config (serverless.yml)
[ ] IAM policies and roles
[ ] Security group configurations
[ ] Lambda function code
[ ] ECS task definitions
[ ] API Gateway configurations
```

---

## Audit Prompt

```markdown
# AWS Security Audit

## Context
You are conducting a specialized security audit of an AWS-deployed application. This audit focuses on AWS-specific security configurations, IAM permissions, network security, and service-specific best practices.

[PASTE: Phase 7 and Phase 8 Carry-Forward Summaries if available]

## AWS Services in Use
[List all AWS services used by the application]

## Provided Materials
[PASTE: Terraform, CloudFormation, CDK, or other infrastructure code]

---

## Audit Checklist

### AWS-1: IAM Security

**Critical:** IAM misconfigurations are the #1 cause of AWS security breaches.

| Check | Status | Notes |
|-------|--------|-------|
| No root account usage for daily operations | | |
| MFA enabled for all IAM users | | |
| MFA enabled for root account | | |
| Least privilege principle followed | | |
| No wildcard (*) actions in policies | | |
| No wildcard (*) resources in policies | | |
| Service roles scoped appropriately | | |
| Access keys rotated (< 90 days old) | | |
| No hardcoded credentials in code | | |
| No inline policies (use managed policies) | | |
| IAM Access Analyzer enabled | | |
| Permission boundaries used | | |

**Terraform IAM Patterns to Check:**
```hcl
# BAD - Overly permissive
resource "aws_iam_policy" "bad_policy" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "*"           # SECURITY ISSUE
      Resource = "*"           # SECURITY ISSUE
    }]
  })
}

# BAD - Admin access to Lambda
resource "aws_iam_role_policy_attachment" "lambda_admin" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"  # SECURITY ISSUE
}

# GOOD - Least privilege
resource "aws_iam_policy" "good_policy" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "arn:aws:s3:::my-bucket/*"
    }]
  })
}
```

**AWS CLI Verification:**
```bash
# Check for root account usage
aws iam get-account-summary | jq '.SummaryMap.AccountAccessKeysPresent'

# List users without MFA
aws iam list-users --query 'Users[*].UserName' | while read user; do
  aws iam list-mfa-devices --user-name $user
done

# Find overly permissive policies
aws iam list-policies --scope Local --query 'Policies[*].Arn' | while read arn; do
  aws iam get-policy-version --policy-arn $arn --version-id v1 | grep -E '"Action":\s*"\*"'
done

# Check access key age
aws iam list-access-keys --user-name USERNAME --query 'AccessKeyMetadata[*].CreateDate'
```

---

### AWS-2: S3 Bucket Security

| Check | Status | Notes |
|-------|--------|-------|
| No public buckets (unless intended) | | |
| Block Public Access enabled (account level) | | |
| Block Public Access enabled (bucket level) | | |
| Bucket policies are restrictive | | |
| Server-side encryption enabled (SSE-S3 or SSE-KMS) | | |
| Versioning enabled for critical buckets | | |
| Access logging enabled | | |
| Object Lock for compliance (if required) | | |
| No sensitive data exposure in bucket names | | |
| Cross-account access controlled | | |

**Terraform S3 Patterns:**
```hcl
# BAD - Public bucket
resource "aws_s3_bucket_public_access_block" "bad" {
  bucket                  = aws_s3_bucket.main.id
  block_public_acls       = false  # SECURITY ISSUE
  block_public_policy     = false  # SECURITY ISSUE
}

# GOOD - Secure bucket
resource "aws_s3_bucket" "secure" {
  bucket = "my-secure-bucket"
}

resource "aws_s3_bucket_public_access_block" "secure" {
  bucket                  = aws_s3_bucket.secure.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.secure.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
  }
}
```

**AWS CLI Verification:**
```bash
# List public buckets
aws s3api list-buckets --query 'Buckets[*].Name' | while read bucket; do
  aws s3api get-bucket-acl --bucket $bucket | grep -E 'AllUsers|AuthenticatedUsers'
done

# Check encryption status
aws s3api get-bucket-encryption --bucket BUCKET_NAME

# Check public access block
aws s3api get-public-access-block --bucket BUCKET_NAME
```

---

### AWS-3: VPC & Network Security

| Check | Status | Notes |
|-------|--------|-------|
| Security groups use least privilege | | |
| No 0.0.0.0/0 ingress (except ALB/NLB on 80/443) | | |
| No 0.0.0.0/0 egress (if restrictive) | | |
| VPC Flow Logs enabled | | |
| Private subnets for databases/internal services | | |
| NAT Gateway for private subnet egress | | |
| Network ACLs configured appropriately | | |
| VPC endpoints for AWS services (S3, DynamoDB, etc.) | | |
| No default VPC usage in production | | |
| Transit Gateway security (if multi-VPC) | | |

**Terraform Network Patterns:**
```hcl
# BAD - Open security group
resource "aws_security_group" "bad" {
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # SECURITY ISSUE - All traffic from anywhere
  }
}

# BAD - SSH from anywhere
resource "aws_security_group" "bad_ssh" {
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # SECURITY ISSUE
  }
}

# GOOD - Restrictive security group
resource "aws_security_group" "good" {
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]  # Only from ALB
  }
}
```

**AWS CLI Verification:**
```bash
# Find security groups with 0.0.0.0/0
aws ec2 describe-security-groups --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]'

# Check VPC Flow Logs
aws ec2 describe-flow-logs --query 'FlowLogs[*].[FlowLogId,ResourceId,LogDestination]'
```

---

### AWS-4: Lambda Security

| Check | Status | Notes |
|-------|--------|-------|
| Minimal IAM execution role permissions | | |
| VPC attached if accessing internal resources | | |
| Environment variables encrypted with KMS | | |
| No secrets in code or environment variables | | |
| Timeout configured appropriately | | |
| Memory limits set | | |
| Reserved concurrency set (DoS protection) | | |
| Dead letter queue configured | | |
| Function URL authentication (if used) | | |
| Layers from trusted sources only | | |

**Terraform Lambda Patterns:**
```hcl
# BAD - Lambda with admin permissions
resource "aws_iam_role_policy_attachment" "lambda_bad" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"  # SECURITY ISSUE
}

# BAD - Secrets in environment variables
resource "aws_lambda_function" "bad" {
  environment {
    variables = {
      DATABASE_PASSWORD = "plaintext-password"  # SECURITY ISSUE
    }
  }
}

# GOOD - Minimal permissions and secrets from SSM
resource "aws_lambda_function" "good" {
  function_name = "my-function"
  role          = aws_iam_role.lambda_minimal.arn
  timeout       = 30
  memory_size   = 256

  reserved_concurrent_executions = 100  # DoS protection

  dead_letter_config {
    target_arn = aws_sqs_queue.dlq.arn
  }

  environment {
    variables = {
      DATABASE_SECRET_ARN = aws_secretsmanager_secret.db.arn  # Reference only
    }
  }
}
```

**AWS CLI Verification:**
```bash
# Check Lambda execution role permissions
aws lambda get-function --function-name FUNCTION_NAME --query 'Configuration.Role'
aws iam list-attached-role-policies --role-name ROLE_NAME

# Check for environment variables (potential secrets)
aws lambda get-function-configuration --function-name FUNCTION_NAME --query 'Environment.Variables'
```

---

### AWS-5: RDS/Database Security

| Check | Status | Notes |
|-------|--------|-------|
| Not publicly accessible | | |
| Encryption at rest enabled | | |
| Encryption in transit (SSL/TLS) enforced | | |
| Automated backups enabled | | |
| Multi-AZ for production | | |
| Security groups restrictive | | |
| IAM authentication enabled (if supported) | | |
| Enhanced monitoring enabled | | |
| Deletion protection enabled | | |
| No default master username (admin/root) | | |

**Terraform RDS Patterns:**
```hcl
# BAD - Public RDS
resource "aws_db_instance" "bad" {
  publicly_accessible = true  # SECURITY ISSUE
  storage_encrypted   = false  # SECURITY ISSUE

  # Using default subnet group (might be public)
}

# GOOD - Secure RDS
resource "aws_db_instance" "good" {
  publicly_accessible    = false
  storage_encrypted      = true
  kms_key_id             = aws_kms_key.rds.arn

  multi_az               = true
  deletion_protection    = true
  backup_retention_period = 30

  db_subnet_group_name   = aws_db_subnet_group.private.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  iam_database_authentication_enabled = true

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
}
```

---

### AWS-6: Secrets Management

| Check | Status | Notes |
|-------|--------|-------|
| AWS Secrets Manager or SSM Parameter Store used | | |
| Secrets rotated automatically | | |
| No secrets in environment variables directly | | |
| No secrets in code or config files | | |
| KMS encryption for secrets | | |
| Secrets access audited via CloudTrail | | |
| Least privilege access to secrets | | |
| No secrets in Lambda layers | | |

**Terraform Secrets Patterns:**
```hcl
# BAD - Hardcoded secrets
resource "aws_lambda_function" "bad" {
  environment {
    variables = {
      DB_PASSWORD = "MySecretPassword123!"  # SECURITY ISSUE
      API_KEY     = "sk-live-xxxxx"          # SECURITY ISSUE
    }
  }
}

# GOOD - Using Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "prod/db/password"
  kms_key_id = aws_kms_key.secrets.id
}

resource "aws_secretsmanager_secret_rotation" "db_password" {
  secret_id           = aws_secretsmanager_secret.db_password.id
  rotation_lambda_arn = aws_lambda_function.rotation.arn

  rotation_rules {
    automatically_after_days = 30
  }
}
```

---

### AWS-7: Logging & Monitoring

| Check | Status | Notes |
|-------|--------|-------|
| CloudTrail enabled (all regions) | | |
| CloudTrail log file validation enabled | | |
| CloudTrail logs encrypted with KMS | | |
| CloudTrail logs in separate account (recommended) | | |
| CloudWatch Logs for applications | | |
| CloudWatch Alarms for security events | | |
| GuardDuty enabled | | |
| AWS Config enabled | | |
| Security Hub enabled | | |
| VPC Flow Logs enabled | | |

**Terraform Logging Patterns:**
```hcl
# GOOD - Comprehensive CloudTrail
resource "aws_cloudtrail" "main" {
  name                          = "main-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  kms_key_id                    = aws_kms_key.cloudtrail.arn

  event_selector {
    read_write_type           = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::S3::Object"
      values = ["arn:aws:s3"]
    }
  }
}

# GuardDuty
resource "aws_guardduty_detector" "main" {
  enable = true

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
  }
}
```

**AWS CLI Verification:**
```bash
# Check CloudTrail status
aws cloudtrail describe-trails --query 'trailList[*].[Name,IsMultiRegionTrail,LogFileValidationEnabled]'

# Check GuardDuty
aws guardduty list-detectors

# Check Config status
aws configservice describe-configuration-recorders
```

---

### AWS-8: EC2/Compute Security

| Check | Status | Notes |
|-------|--------|-------|
| IMDSv2 required (no IMDSv1) | | |
| Latest AMIs used (patched) | | |
| SSM Session Manager for access (not SSH keys) | | |
| Security groups minimal | | |
| EBS encryption enabled | | |
| No public IP unless required | | |
| Instance profiles with minimal permissions | | |
| No key pairs in user data | | |
| Nitro-based instances (if sensitive workloads) | | |

**Terraform EC2 Patterns:**
```hcl
# BAD - IMDSv1 allowed (SSRF risk)
resource "aws_instance" "bad" {
  # No metadata_options = IMDSv1 allowed by default

  user_data = <<-EOF
    #!/bin/bash
    export AWS_ACCESS_KEY=AKIA...  # SECURITY ISSUE - Credentials in user data
  EOF
}

# GOOD - IMDSv2 required
resource "aws_instance" "good" {
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"  # Enforce IMDSv2
    http_put_response_hop_limit = 1
  }

  root_block_device {
    encrypted = true
  }

  iam_instance_profile = aws_iam_instance_profile.minimal.name
}
```

---

### AWS-9: API Gateway Security (if applicable)

| Check | Status | Notes |
|-------|--------|-------|
| Authorization configured (IAM, Cognito, Lambda) | | |
| API keys used for rate limiting | | |
| Throttling/rate limiting enabled | | |
| Request validation enabled | | |
| WAF attached | | |
| Access logging enabled | | |
| HTTPS only (no HTTP) | | |
| CORS configured restrictively | | |

---

### AWS-10: ECS/EKS Security (if applicable)

| Check | Status | Notes |
|-------|--------|-------|
| Task roles with minimal permissions | | |
| Secrets from Secrets Manager/SSM | | |
| No secrets in task definitions | | |
| Private registry for images | | |
| Image scanning enabled | | |
| Read-only root filesystem | | |
| Non-root user in containers | | |
| Network policies (EKS) | | |
| Pod Security Standards (EKS) | | |

---

## AWS CLI Audit Commands

```bash
# === IAM ===
# Get credential report
aws iam generate-credential-report
aws iam get-credential-report --query 'Content' --output text | base64 -d

# === S3 ===
# List all buckets with public access
for bucket in $(aws s3api list-buckets --query 'Buckets[*].Name' --output text); do
  echo "Checking $bucket..."
  aws s3api get-public-access-block --bucket $bucket 2>/dev/null || echo "No block configured"
done

# === EC2 ===
# Find instances without IMDSv2
aws ec2 describe-instances --query 'Reservations[*].Instances[?MetadataOptions.HttpTokens!=`required`].[InstanceId,MetadataOptions]'

# === Lambda ===
# List all functions with their roles
aws lambda list-functions --query 'Functions[*].[FunctionName,Role]'

# === RDS ===
# Find publicly accessible databases
aws rds describe-db-instances --query 'DBInstances[?PubliclyAccessible==`true`].[DBInstanceIdentifier]'

# === CloudTrail ===
# Verify CloudTrail is enabled
aws cloudtrail get-trail-status --name TRAIL_NAME
```

---

## Carry-Forward Summary

Provide a summary including:
1. **AWS Services Audited:** [List of services reviewed]
2. **Critical IAM Issues:** [Any admin/wildcard policies]
3. **Public Resources:** [Any public S3/RDS/EC2]
4. **Network Security:** [Security group issues]
5. **Secrets Management:** [Hardcoded secrets found]
6. **Logging Status:** [CloudTrail/GuardDuty enabled]
7. **Encryption Status:** [At-rest and in-transit encryption]

---

## Output Format

```markdown
### [AWS-###] Finding Title

**Severity:** Critical/High/Medium/Low
**AWS Service:** IAM / S3 / EC2 / Lambda / RDS / VPC / etc.
**Category:** Access Control / Encryption / Network / Logging / Secrets

**Resource:**
- Resource ARN: `arn:aws:service:region:account:resource`
- Terraform file: `path/to/file.tf:line`

**Issue:**
[Description of the security issue]

**Evidence:**
```hcl
[Terraform/CloudFormation code showing the issue]
```

**Recommendation:**
[Specific remediation with code examples]

**AWS Documentation:**
- [Relevant AWS security documentation link]

**CIS AWS Benchmark:**
- [Relevant CIS benchmark reference if applicable]
```
