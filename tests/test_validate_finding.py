"""
Tests for validate_finding.py

Tests finding document validation including required fields, severity validation,
OWASP/CWE reference validation, and phase validation.
"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "skill" / "scripts"))

from validate_finding import (
    extract_field,
    validate_severity,
    validate_status,
    validate_owasp,
    validate_cwe,
    validate_phase,
    validate_finding,
    VALID_SEVERITIES,
    VALID_STATUSES,
)


class TestExtractField:
    """Tests for field extraction from markdown content."""

    def test_extract_table_format(self):
        """Test extraction from markdown table format."""
        content = """
| Field | Value |
|-------|-------|
| **Severity** | Critical |
"""
        assert extract_field(content, "severity") == "Critical"

    def test_extract_header_format(self):
        """Test extraction from header format."""
        content = "## Severity\nCritical"
        assert extract_field(content, "severity") == "Critical"

    def test_extract_bold_format(self):
        """Test extraction from bold key format."""
        content = "**Severity**: High"
        assert extract_field(content, "severity") == "High"

    def test_extract_inline_format(self):
        """Test extraction from inline format."""
        content = "Severity: Medium"
        assert extract_field(content, "severity") == "Medium"

    def test_extract_missing_field(self):
        """Test extraction of missing field returns empty string."""
        content = "No severity here"
        assert extract_field(content, "severity") == ""

    def test_case_insensitive(self):
        """Test field extraction is case insensitive."""
        content = "| SEVERITY | Critical |"
        assert extract_field(content, "severity") == "Critical"


class TestSeverityValidation:
    """Tests for severity validation."""

    def test_valid_severities(self):
        """Test all valid severity levels."""
        for severity in VALID_SEVERITIES:
            valid, error = validate_severity(severity)
            assert valid, f"'{severity}' should be valid"
            assert error is None

    def test_case_insensitive(self):
        """Test severity validation is case insensitive."""
        valid, error = validate_severity("CRITICAL")
        assert valid

        valid, error = validate_severity("High")
        assert valid

    def test_invalid_severity(self):
        """Test invalid severity is rejected."""
        valid, error = validate_severity("urgent")
        assert not valid
        assert "Invalid severity" in error

    def test_empty_severity(self):
        """Test empty severity is rejected."""
        valid, error = validate_severity("")
        assert not valid
        assert "missing" in error.lower()


class TestStatusValidation:
    """Tests for status validation."""

    def test_valid_statuses(self):
        """Test all valid status values."""
        for status in VALID_STATUSES:
            valid, error = validate_status(status)
            assert valid, f"'{status}' should be valid"

    def test_empty_status_allowed(self):
        """Test that empty status is allowed (optional field)."""
        valid, error = validate_status("")
        assert valid

    def test_invalid_status(self):
        """Test invalid status is rejected."""
        valid, error = validate_status("completed")
        assert not valid
        assert "Invalid status" in error


class TestOWASPValidation:
    """Tests for OWASP reference validation."""

    def test_valid_owasp_references(self):
        """Test valid OWASP references."""
        valid_refs = ["A01", "A01:2021", "A03", "A10:2021"]
        for ref in valid_refs:
            valid, error = validate_owasp(ref)
            assert valid, f"'{ref}' should be valid"

    def test_empty_owasp_allowed(self):
        """Test empty OWASP is allowed (optional field)."""
        valid, error = validate_owasp("")
        assert valid

    def test_invalid_owasp(self):
        """Test invalid OWASP reference."""
        valid, error = validate_owasp("A00")
        assert not valid

        valid, error = validate_owasp("A11")
        assert not valid


class TestCWEValidation:
    """Tests for CWE reference validation."""

    def test_valid_cwe_references(self):
        """Test valid CWE references."""
        valid_refs = ["CWE-79", "CWE-89", "CWE-1234"]
        for ref in valid_refs:
            valid, error = validate_cwe(ref)
            assert valid, f"'{ref}' should be valid"

    def test_empty_cwe_allowed(self):
        """Test empty CWE is allowed (optional field)."""
        valid, error = validate_cwe("")
        assert valid

    def test_invalid_cwe(self):
        """Test invalid CWE reference."""
        valid, error = validate_cwe("79")
        assert not valid

        valid, error = validate_cwe("CWE")
        assert not valid


class TestPhaseValidation:
    """Tests for phase validation."""

    def test_valid_phases(self):
        """Test valid phase numbers."""
        for i in range(13):
            valid, error = validate_phase(f"Phase {i}")
            assert valid, f"Phase {i} should be valid"

    def test_phase_in_text(self):
        """Test phase number extraction from text."""
        valid, error = validate_phase("Authentication (Phase 1)")
        assert valid

    def test_empty_phase_rejected(self):
        """Test empty phase is rejected."""
        valid, error = validate_phase("")
        assert not valid
        assert "missing" in error.lower()

    def test_invalid_phase_number(self):
        """Test invalid phase number."""
        valid, error = validate_phase("Phase 15")
        assert not valid
        assert "between 0 and 12" in error


class TestFindingValidation:
    """Tests for complete finding validation."""

    def test_valid_finding(self, sample_finding_content):
        """Test validation of a complete valid finding."""
        result = validate_finding(sample_finding_content)
        assert result["valid"]
        assert len(result["errors"]) == 0

    def test_missing_severity(self):
        """Test that missing severity causes validation failure."""
        content = """
| Field | Value |
|-------|-------|
| **Phase** | 3 |
"""
        result = validate_finding(content)
        assert not result["valid"]
        assert any("severity" in e.lower() for e in result["errors"])

    def test_missing_phase(self):
        """Test that missing phase causes validation failure."""
        content = """
| Field | Value |
|-------|-------|
| **Severity** | High |
"""
        result = validate_finding(content)
        assert not result["valid"]
        assert any("phase" in e.lower() for e in result["errors"])

    def test_warnings_for_missing_recommended_fields(self):
        """Test that warnings are generated for missing recommended fields."""
        content = """
| Field | Value |
|-------|-------|
| **Severity** | High |
| **Phase** | 3 |
"""
        result = validate_finding(content)
        assert result["valid"]  # Still valid, just has warnings
        assert len(result["warnings"]) > 0
        assert any("id" in w.lower() for w in result["warnings"])

    def test_evidence_section_warning(self):
        """Test warning when no evidence section exists."""
        content = """
| Field | Value |
|-------|-------|
| **Severity** | High |
| **Phase** | 3 |

## Description
A vulnerability.
"""
        result = validate_finding(content)
        assert any("evidence" in w.lower() for w in result["warnings"])

    def test_remediation_section_warning(self):
        """Test warning when no remediation section exists."""
        content = """
| Field | Value |
|-------|-------|
| **Severity** | High |
| **Phase** | 3 |

## Evidence
PoC here
"""
        result = validate_finding(content)
        assert any("remediation" in w.lower() for w in result["warnings"])

    def test_fields_extracted(self, sample_finding_content):
        """Test that fields are correctly extracted."""
        result = validate_finding(sample_finding_content)
        assert result["fields"]["severity"] == "High"
        assert result["fields"]["phase"] == "3"
        assert result["fields"]["id"] == "TEST-001"
        assert "CWE-79" in result["fields"]["cwe"]

    def test_invalid_owasp_generates_warning(self):
        """Test that invalid OWASP reference generates warning."""
        content = """
| Field | Value |
|-------|-------|
| **Severity** | High |
| **Phase** | 3 |
| **OWASP** | A99 |
"""
        result = validate_finding(content)
        assert any("owasp" in w.lower() for w in result["warnings"])

    def test_invalid_cwe_generates_warning(self):
        """Test that invalid CWE reference generates warning."""
        content = """
| Field | Value |
|-------|-------|
| **Severity** | High |
| **Phase** | 3 |
| **CWE** | 79 |
"""
        result = validate_finding(content)
        assert any("cwe" in w.lower() for w in result["warnings"])
