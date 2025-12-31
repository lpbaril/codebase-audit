# Audit Selector

This guide helps the AI agent automatically determine which audits to run based on the target codebase. The AI should use **automatic detection first**, then ask clarifying questions only when needed.

---

## Autonomous Audit Workflow

When a user asks to audit a codebase, the AI should follow this autonomous workflow:

### Step 1: Automatic Technology Detection

**Scan the target codebase for these files/patterns:**

| Detection Target | Technology | Recommended Audit |
|------------------|------------|-------------------|
| `package.json` with `react`, `next`, `vue`, `nuxt` | Frontend Framework | Core Phases + Frontend Performance |
| `Podfile`, `*.xcodeproj`, `*.xcworkspace` | iOS | Mobile Security Audit |
| `build.gradle`, `AndroidManifest.xml` | Android | Mobile Security Audit |
| `pubspec.yaml` with `flutter` | Flutter | Mobile Security Audit |
| `package.json` with `react-native` | React Native | Mobile Security Audit |
| `*.tf`, `terraform/` | Terraform | Infrastructure + Cloud Audit |
| `serverless.yml`, `serverless.ts` | Serverless Framework | AWS Security Audit |
| `template.yaml`, `template.yml` (SAM) | AWS SAM | AWS Security Audit |
| `*.yaml` with `apiVersion: apps/v1` | Kubernetes | Kubernetes Audit |
| `docker-compose.yml`, `Dockerfile` | Docker | Infrastructure Audit |
| `schema.graphql`, `*.graphql`, `type Query` | GraphQL | GraphQL Audit |
| `requirements.txt`, `pyproject.toml` | Python | Check for Django/FastAPI |
| `Gemfile` with `rails` | Ruby on Rails | Core Phases |
| `composer.json` with `laravel` | Laravel | Core Phases |
| `pom.xml`, `build.gradle` with Spring | Spring Boot | Core Phases |
| `.github/workflows/` | GitHub Actions | CI/CD Security |
| `cloudbuild.yaml` | Google Cloud Build | GCP Audit |
| `azure-pipelines.yml` | Azure DevOps | Azure Audit |

### Step 2: Detect Cloud Provider

**Look for cloud-specific configurations:**

| File/Pattern | Cloud Provider | Audit |
|--------------|----------------|-------|
| `*.tf` with `provider "aws"` | AWS | AWS Security Audit |
| `*.tf` with `provider "google"` | GCP | GCP Security Audit |
| `*.tf` with `provider "azurerm"` | Azure | Azure Security Audit |
| `serverless.yml` with `provider: aws` | AWS | AWS Security Audit |
| `app.yaml` (App Engine) | GCP | GCP Security Audit |
| `.aws/`, `~/.aws/credentials` references | AWS | AWS Security Audit |

### Step 3: Detect Compliance Requirements

**Scan for compliance indicators:**

| Indicator | Compliance Framework |
|-----------|---------------------|
| `HIPAA`, `PHI`, `health` in docs/comments | HIPAA |
| `PCI`, `payment`, `credit card`, `cardholder` | PCI-DSS |
| `GDPR`, `data subject`, `consent`, EU references | GDPR |
| `SOC2`, `SOC 2`, `trust services` | SOC2 |
| `.gov`, `FedRAMP`, `federal` | FedRAMP |

### Step 4: Generate Audit Plan

Based on detection, automatically generate an audit plan:

```markdown
## Detected Technology Stack

Based on my scan of your codebase, I detected:

**Application Type:** [Web/Mobile/API/etc.]
**Frameworks:** [List detected frameworks]
**Cloud Provider:** [AWS/GCP/Azure/Self-hosted]
**Infrastructure:** [K8s/Docker/Serverless/etc.]
**API Type:** [REST/GraphQL/gRPC]
**Compliance Indicators:** [Any detected]

## Recommended Audit Path

I recommend running the following audits:

### Core Security Audit (Required)
- Phase 0: Reconnaissance
- Phase 1: Authentication
- Phase 2: Authorization
- Phase 3: API Security
- Phase 4: Business Logic
- Phase 5: Data Layer
- Phase 6: Frontend
- Phase 7: Infrastructure
- Phase 8: Secrets Management
- Phase 9: Logging & Monitoring
- Phase 10: Error Handling
- Phase 11: Cross-Cutting
- Phase 12: Synthesis

### Specialized Audits (Recommended)
- [List based on detection]

### Compliance Mapping
- [If compliance indicators found]

Shall I proceed with this audit plan?
```

---

## Fallback: Quick Questionnaire

If auto-detection is inconclusive, ask these questions:

### Q1: Application Type
What type of application is this?
- Web Application (SPA, SSR, traditional)
- Mobile Application (iOS, Android, cross-platform)
- API/Backend only
- Desktop Application
- CLI Tool / Library

### Q2: Mobile Platforms (if applicable)
Which mobile platforms?
- iOS (Swift/Objective-C)
- Android (Kotlin/Java)
- React Native
- Flutter
- None

### Q3: Cloud Infrastructure
Where is this deployed?
- AWS
- Google Cloud Platform
- Microsoft Azure
- Self-hosted / On-premise
- Multiple clouds

### Q4: Container/Orchestration
Using containers or orchestration?
- Kubernetes
- Docker (without K8s)
- Serverless (Lambda, Functions)
- Traditional VMs
- None

### Q5: API Type
What type of API?
- REST API
- GraphQL
- gRPC
- WebSockets / Real-time
- Multiple

### Q6: Compliance Requirements
Any compliance requirements?
- SOC2
- HIPAA
- GDPR
- PCI-DSS
- ISO 27001
- None specific

---

## Audit Path Recommendations

Based on detection/answers, use these audit paths:

### Standard Web Application
```
Core Phases 0-12
+ Frontend Performance Audit (optional)
```

### Web + Mobile Application
```
Core Phases 0-12
+ Mobile Security Audit
+ Frontend Performance Audit
```

### AWS-Deployed Application
```
Core Phases 0-12
+ AWS Security Audit
```

### Kubernetes Application
```
Core Phases 0-12
+ Kubernetes Audit
```

### GraphQL API
```
Core Phases 0-12
+ GraphQL Audit
+ API Penetration Testing
```

### Enterprise with Compliance
```
Core Phases 0-12
+ Relevant Cloud Audit
+ Compliance Mapping (for reporting)
+ All relevant specialized audits
```

### Full Stack Monorepo (Web + Mobile + API)
```
Core Phases 0-12
+ Mobile Security Audit
+ Cloud Security Audit (AWS/GCP/Azure)
+ Kubernetes Audit (if applicable)
+ Frontend Performance Audit
+ Compliance Mapping
```

---

## Autonomous Execution Guidelines

The AI should operate autonomously as much as possible:

### DO Automatically:
- Scan the codebase to detect technologies
- Create the `.audit/` folder structure
- Initialize `audit-context.md`
- Run phases sequentially without waiting for confirmation between phases
- Document findings as they're discovered
- Generate carry-forward summaries
- Proceed to specialized audits after core phases

### ASK the User About:
- Adding `.audit/` to `.gitignore` (required consent)
- Skipping phases that don't apply (e.g., "No Kubernetes found, skip K8s audit?")
- Prioritizing specific areas if time-constrained
- Clarifying business logic questions
- Access to external systems (databases, cloud consoles)

### ALWAYS Do at End:
- Generate final synthesis report
- Create prioritized remediation roadmap
- Update `audit-context.md` with completion status
- Offer to create GitHub issues for critical findings

---

## Detection Scripts

The AI can use these commands to detect technologies:

### Detect Package Managers & Frameworks
```bash
# Node.js ecosystem
ls package.json 2>/dev/null && cat package.json | grep -E '"(react|next|vue|nuxt|angular|express|fastify)"'

# Python
ls requirements.txt pyproject.toml setup.py 2>/dev/null

# Ruby
ls Gemfile 2>/dev/null && grep -E 'rails|sinatra' Gemfile

# PHP
ls composer.json 2>/dev/null && grep -E 'laravel|symfony' composer.json

# Java/Kotlin
ls pom.xml build.gradle 2>/dev/null
```

### Detect Mobile
```bash
# iOS
ls Podfile *.xcodeproj *.xcworkspace 2>/dev/null

# Android
ls app/build.gradle AndroidManifest.xml 2>/dev/null
find . -name "AndroidManifest.xml" 2>/dev/null

# React Native
grep -l "react-native" package.json 2>/dev/null

# Flutter
ls pubspec.yaml 2>/dev/null && grep flutter pubspec.yaml
```

### Detect Infrastructure
```bash
# Terraform
find . -name "*.tf" 2>/dev/null | head -5

# Kubernetes
find . -name "*.yaml" -exec grep -l "apiVersion.*apps/v1\|kind: Deployment" {} \; 2>/dev/null

# Docker
ls Dockerfile docker-compose.yml 2>/dev/null

# Serverless
ls serverless.yml serverless.ts template.yaml 2>/dev/null
```

### Detect Cloud Provider
```bash
# In Terraform files
grep -r 'provider "aws"' *.tf 2>/dev/null
grep -r 'provider "google"' *.tf 2>/dev/null
grep -r 'provider "azurerm"' *.tf 2>/dev/null

# In serverless
grep 'provider: aws' serverless.yml 2>/dev/null
```

### Detect GraphQL
```bash
find . -name "*.graphql" 2>/dev/null
find . -name "schema.graphql" 2>/dev/null
grep -r "type Query" --include="*.ts" --include="*.js" 2>/dev/null | head -3
```

---

## Example Autonomous Audit Start

When user says: "Audit the codebase at ../my-app/"

**AI Response:**
```
I'll scan your codebase to determine the optimal audit path.

## Technology Detection Results

Scanning ../my-app/...

**Detected:**
- Frontend: Next.js 14 (React)
- Backend: Node.js with Express
- Database: PostgreSQL (Prisma ORM)
- Mobile: React Native (iOS + Android)
- Infrastructure: AWS (Terraform)
- API: REST + GraphQL
- CI/CD: GitHub Actions
- Containerization: Docker

**Compliance Indicators:** None detected

## Recommended Audit Path

I recommend the following comprehensive audit:

**Core Security Audit** (Phases 0-12) - ~34 hours
**Specialized Audits:**
- Mobile Security Audit (React Native) - ~3 hours
- AWS Security Audit - ~3 hours
- GraphQL Audit - ~2 hours
- Frontend Performance Audit - ~2 hours

**Total Estimated Time:** ~44 hours

I'll now create the .audit/ folder and begin with Phase 0: Reconnaissance.

[Proceeds autonomously...]
```
