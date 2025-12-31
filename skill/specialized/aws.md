# AWS Security Audit

**Services:** IAM, S3, VPC, Lambda, RDS, EC2, CloudTrail
**Use With:** Phase 7 (Infrastructure), Phase 8 (Secrets)

## Quick Checks

### IAM Security
- [ ] No root account usage
- [ ] MFA enabled for all users
- [ ] Least privilege policies
- [ ] No wildcard (*) permissions
- [ ] No hardcoded credentials

### S3 Security
- [ ] No public buckets (unless intended)
- [ ] Bucket policies restrictive
- [ ] Encryption enabled (SSE-S3/SSE-KMS)
- [ ] Versioning enabled
- [ ] Block Public Access enabled

### VPC & Network
- [ ] Security groups least privilege
- [ ] No 0.0.0.0/0 ingress
- [ ] VPC Flow Logs enabled
- [ ] Private subnets for databases

### Lambda Security
- [ ] Minimal IAM role
- [ ] No secrets in env vars (use SSM)
- [ ] Timeout configured
- [ ] VPC attached if needed

### RDS Security
- [ ] Not publicly accessible
- [ ] Encryption at rest
- [ ] SSL/TLS enabled
- [ ] Automated backups

### Logging
- [ ] CloudTrail enabled (all regions)
- [ ] GuardDuty enabled
- [ ] Config Rules enabled

## Terraform Patterns

```hcl
# BAD - Public S3
resource "aws_s3_bucket" "bad" {
  acl = "public-read"  # DANGEROUS
}

# GOOD
resource "aws_s3_bucket_public_access_block" "good" {
  bucket                  = aws_s3_bucket.main.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

```hcl
# BAD - Open security group
ingress {
  from_port   = 0
  to_port     = 65535
  cidr_blocks = ["0.0.0.0/0"]  # DANGEROUS
}

# GOOD
ingress {
  from_port       = 443
  to_port         = 443
  security_groups = [aws_security_group.alb.id]
}
```

## CLI Verification

```bash
# Check for public S3 buckets
aws s3api list-buckets --query 'Buckets[].Name' | xargs -I {} \
  aws s3api get-bucket-acl --bucket {}

# Check security groups
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]]'

# Check IAM users without MFA
aws iam generate-credential-report
aws iam get-credential-report --output text --query Content | base64 -d
```

## Finding Format
```markdown
### [AWS-###] Title
**Severity:** Critical/High/Medium/Low
**Service:** IAM/S3/VPC/Lambda/RDS/EC2
**Resource:** [ARN or identifier]
**Location:** file:line (for IaC)
```

---

*Full guide: `../specialized/aws-security-audit.md`*
