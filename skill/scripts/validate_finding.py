#!/usr/bin/env python3
"""
Finding Validation Script

Validates security finding documents to ensure they have all required fields
and proper formatting.

Usage:
    python validate_finding.py /path/to/finding.md

Output:
    JSON object with validation result (pass/fail) and any errors
"""

import json
import re
import sys
from pathlib import Path


VALID_SEVERITIES = ["critical", "high", "medium", "low", "info", "informational"]
VALID_STATUSES = ["open", "in progress", "in-progress", "resolved", "fixed", "accepted risk", "accepted-risk", "wont fix", "wont-fix"]

REQUIRED_FIELDS = [
    "severity",
    "phase",
]

RECOMMENDED_FIELDS = [
    "id",
    "title",
    "cwe",
    "owasp",
    "description",
    "impact",
    "recommendation",
]

OWASP_PATTERN = r'A0[1-9]|A10'
CWE_PATTERN = r'CWE-\d+'


def read_file(path: Path) -> str:
    """Read file content."""
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return ""


def extract_field(content: str, field: str) -> str:
    """Extract a field value from markdown content."""
    # Try table format: | Field | Value |
    table_pattern = rf'\|\s*\*?\*?{field}\*?\*?\s*\|\s*([^|]+)\s*\|'
    match = re.search(table_pattern, content, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Try header format: ## Field or **Field:**
    header_pattern = rf'(?:##\s*{field}|^\*\*{field}\*?\*?:?)\s*[:\-]?\s*(.+?)(?:\n|$)'
    match = re.search(header_pattern, content, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Try inline format: Field: Value
    inline_pattern = rf'{field}\s*:\s*(.+?)(?:\n|$)'
    match = re.search(inline_pattern, content, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return ""


def validate_severity(severity: str) -> tuple:
    """Validate severity level."""
    if not severity:
        return False, "Severity is missing"

    severity_lower = severity.lower().strip()
    if severity_lower not in VALID_SEVERITIES:
        return False, f"Invalid severity '{severity}'. Must be one of: {', '.join(VALID_SEVERITIES)}"

    return True, None


def validate_status(status: str) -> tuple:
    """Validate finding status."""
    if not status:
        return True, None  # Status is optional

    status_lower = status.lower().strip()
    if status_lower not in VALID_STATUSES:
        return False, f"Invalid status '{status}'. Must be one of: {', '.join(VALID_STATUSES)}"

    return True, None


def validate_owasp(owasp: str) -> tuple:
    """Validate OWASP reference format."""
    if not owasp:
        return True, None  # OWASP is recommended but not required

    # Check for valid OWASP Top 10 reference
    if not re.search(OWASP_PATTERN, owasp):
        return False, f"Invalid OWASP reference '{owasp}'. Should reference A01-A10 (e.g., A01:2021)"

    return True, None


def validate_cwe(cwe: str) -> tuple:
    """Validate CWE reference format."""
    if not cwe:
        return True, None  # CWE is recommended but not required

    if not re.search(CWE_PATTERN, cwe):
        return False, f"Invalid CWE reference '{cwe}'. Should be format CWE-XXX (e.g., CWE-89)"

    return True, None


def validate_phase(phase: str) -> tuple:
    """Validate phase reference."""
    if not phase:
        return False, "Phase is missing"

    # Extract phase number
    phase_match = re.search(r'(\d+)', phase)
    if not phase_match:
        return False, f"Invalid phase '{phase}'. Should include phase number (0-12)"

    phase_num = int(phase_match.group(1))
    if phase_num < 0 or phase_num > 12:
        return False, f"Invalid phase number {phase_num}. Must be between 0 and 12"

    return True, None


def validate_finding(content: str) -> dict:
    """Validate a finding document."""
    errors = []
    warnings = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        value = extract_field(content, field)
        if not value:
            errors.append(f"Required field missing: {field}")

    # Check recommended fields
    for field in RECOMMENDED_FIELDS:
        value = extract_field(content, field)
        if not value:
            warnings.append(f"Recommended field missing: {field}")

    # Validate severity
    severity = extract_field(content, "severity")
    valid, error = validate_severity(severity)
    if not valid:
        errors.append(error)

    # Validate status
    status = extract_field(content, "status")
    valid, error = validate_status(status)
    if not valid:
        errors.append(error)

    # Validate OWASP reference
    owasp = extract_field(content, "owasp")
    valid, error = validate_owasp(owasp)
    if not valid:
        warnings.append(error)

    # Validate CWE reference
    cwe = extract_field(content, "cwe")
    valid, error = validate_cwe(cwe)
    if not valid:
        warnings.append(error)

    # Validate phase
    phase = extract_field(content, "phase")
    valid, error = validate_phase(phase)
    if not valid:
        errors.append(error)

    # Check for evidence/proof section
    if "evidence" not in content.lower() and "proof" not in content.lower() and "poc" not in content.lower():
        warnings.append("No evidence/proof section found")

    # Check for remediation section
    if "remediation" not in content.lower() and "recommendation" not in content.lower() and "fix" not in content.lower():
        warnings.append("No remediation/recommendation section found")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "fields": {
            "severity": extract_field(content, "severity"),
            "status": extract_field(content, "status"),
            "phase": extract_field(content, "phase"),
            "owasp": extract_field(content, "owasp"),
            "cwe": extract_field(content, "cwe"),
            "id": extract_field(content, "id"),
        }
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_finding.py /path/to/finding.md", file=sys.stderr)
        sys.exit(1)

    finding_path = Path(sys.argv[1]).resolve()

    if not finding_path.exists():
        result = {
            "valid": False,
            "errors": [f"File does not exist: {finding_path}"],
            "warnings": [],
            "fields": {}
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    content = read_file(finding_path)

    if not content:
        result = {
            "valid": False,
            "errors": ["File is empty or could not be read"],
            "warnings": [],
            "fields": {}
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    result = validate_finding(content)
    print(json.dumps(result, indent=2))

    # Exit with error code if invalid
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
