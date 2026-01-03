"""
Pytest configuration and shared fixtures for the codebase-audit test suite.
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_node_project(temp_dir):
    """Create a sample Node.js project structure."""
    package_json = temp_dir / "package.json"
    package_json.write_text('''{
  "name": "test-app",
  "dependencies": {
    "react": "^18.0.0",
    "express": "^4.18.0"
  }
}''')
    return temp_dir


@pytest.fixture
def sample_python_project(temp_dir):
    """Create a sample Python project structure."""
    requirements = temp_dir / "requirements.txt"
    requirements.write_text('''django>=4.0
fastapi
pydantic
''')
    return temp_dir


@pytest.fixture
def sample_mobile_project(temp_dir):
    """Create a sample React Native mobile project."""
    package_json = temp_dir / "package.json"
    package_json.write_text('''{
  "name": "mobile-app",
  "dependencies": {
    "react-native": "^0.72.0",
    "expo": "^49.0.0"
  }
}''')
    return temp_dir


@pytest.fixture
def sample_audit_dir(temp_dir):
    """Create a sample .audit directory with findings."""
    audit_dir = temp_dir / ".audit"
    audit_dir.mkdir()

    findings_dir = audit_dir / "findings"
    findings_dir.mkdir()

    # Create sample findings
    finding1 = findings_dir / "VULN-001.md"
    finding1.write_text('''# SQL Injection in Login

| Field | Value |
|-------|-------|
| **ID** | VULN-001 |
| **Severity** | Critical |
| **Phase** | 5 |
| **Status** | Open |
| **OWASP** | A03:2021 |
| **CWE** | CWE-89 |

## Description
SQL injection vulnerability in the login form.

## Impact
Full database access possible.

## Recommendation
Use parameterized queries.
''')

    finding2 = findings_dir / "VULN-002.md"
    finding2.write_text('''# Weak Password Policy

| Field | Value |
|-------|-------|
| **ID** | VULN-002 |
| **Severity** | Medium |
| **Phase** | 1 |
| **Status** | Open |
| **CWE** | CWE-521 |

## Description
Password policy allows weak passwords.

## Recommendation
Implement stronger password requirements.
''')

    finding3 = findings_dir / "VULN-003.md"
    finding3.write_text('''# Missing HTTPS Redirect

| Field | Value |
|-------|-------|
| **ID** | VULN-003 |
| **Severity** | Low |
| **Phase** | 7 |
| **Status** | Resolved |

## Description
Application does not redirect HTTP to HTTPS.
''')

    # Create audit context
    context = audit_dir / "audit-context.md"
    context.write_text('''# Audit Context

| Field | Value |
|-------|-------|
| **Project Name** | Test Application |
| **Audit Started** | 2024-01-15 |
| **Audit Status** | In Progress |
''')

    return audit_dir


@pytest.fixture
def sample_finding_content():
    """Return valid finding content for testing."""
    return '''# Sample Finding

| Field | Value |
|-------|-------|
| **ID** | TEST-001 |
| **Severity** | High |
| **Phase** | 3 |
| **Status** | Open |
| **OWASP** | A01:2021 |
| **CWE** | CWE-79 |

## Description
Cross-site scripting vulnerability in user input.

## Impact
Attacker can execute arbitrary JavaScript.

## Evidence
```javascript
// PoC code here
```

## Recommendation
Implement proper output encoding.
'''


@pytest.fixture
def aws_project(temp_dir):
    """Create a sample AWS project."""
    tf_file = temp_dir / "main.tf"
    tf_file.write_text('''
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
}
''')
    return temp_dir


@pytest.fixture
def kubernetes_project(temp_dir):
    """Create a sample Kubernetes project."""
    k8s_dir = temp_dir / "k8s"
    k8s_dir.mkdir()

    deployment = k8s_dir / "deployment.yaml"
    deployment.write_text('''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:latest
''')
    return temp_dir
