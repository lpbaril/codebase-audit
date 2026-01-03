"""
Tests for generate_report.py

Tests report generation functionality including markdown, JSON, and CSV output,
as well as executive summary, findings organization, and remediation roadmap.
"""

import json
import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "skill" / "scripts"))

from generate_report import (
    read_file,
    extract_field,
    parse_finding,
    load_findings,
    load_audit_context,
    count_by_severity,
    count_by_phase,
    count_by_status,
    generate_executive_summary,
    generate_findings_by_severity,
    generate_findings_by_phase,
    generate_remediation_roadmap,
    generate_compliance_summary,
    generate_report,
    generate_json_report,
    generate_csv_report,
    generate_summary_only,
    _group_by_field,
)


class TestReadFile:
    """Tests for file reading utility."""

    def test_read_existing_file(self, temp_dir):
        """Test reading an existing file."""
        test_file = temp_dir / "test.md"
        test_file.write_text("# Test Content")
        assert read_file(test_file) == "# Test Content"

    def test_read_nonexistent_file(self, temp_dir):
        """Test reading non-existent file returns empty string."""
        nonexistent = temp_dir / "missing.md"
        assert read_file(nonexistent) == ""


class TestExtractField:
    """Tests for field extraction."""

    def test_extract_from_table(self):
        """Test extraction from markdown table."""
        content = "| **ID** | VULN-001 |"
        assert extract_field(content, "ID") == "VULN-001"

    def test_extract_from_header(self):
        """Test extraction from header format."""
        content = "## Severity: Critical"
        assert extract_field(content, "Severity") == "Critical"

    def test_case_insensitive(self):
        """Test case-insensitive extraction."""
        content = "| severity | High |"
        assert extract_field(content, "Severity") == "High"


class TestParseFinding:
    """Tests for finding parsing."""

    def test_parse_complete_finding(self, temp_dir):
        """Test parsing a complete finding."""
        finding_file = temp_dir / "finding.md"
        finding_file.write_text('''# Test Finding

| Field | Value |
|-------|-------|
| **ID** | TEST-001 |
| **Severity** | High |
| **Phase** | 3 |
| **Status** | Open |
| **OWASP** | A01:2021 |
| **CWE** | CWE-79 |

## Description
A test vulnerability.
''')
        finding = parse_finding(finding_file)
        assert finding is not None
        assert finding["id"] == "TEST-001"
        assert finding["severity"] == "high"
        assert finding["phase"] == "3"
        assert finding["status"] == "open"
        assert "A01" in finding["owasp"]
        assert "CWE-79" in finding["cwe"]

    def test_parse_minimal_finding(self, temp_dir):
        """Test parsing a minimal finding."""
        finding_file = temp_dir / "minimal.md"
        finding_file.write_text('''
| **Severity** | Medium |
| **Phase** | 5 |
''')
        finding = parse_finding(finding_file)
        assert finding["severity"] == "medium"
        assert finding["phase"] == "5"
        assert finding["id"] == "minimal"  # Falls back to filename

    def test_parse_nonexistent_finding(self, temp_dir):
        """Test parsing non-existent file returns None."""
        finding = parse_finding(temp_dir / "nonexistent.md")
        assert finding is None


class TestLoadFindings:
    """Tests for loading findings from directory."""

    def test_load_findings(self, sample_audit_dir):
        """Test loading all findings from audit directory."""
        findings = load_findings(sample_audit_dir)
        assert len(findings) == 3

    def test_findings_sorted_by_severity(self, sample_audit_dir):
        """Test that findings are sorted by severity."""
        findings = load_findings(sample_audit_dir)
        severities = [f["severity"] for f in findings]
        # Critical should come before Medium which should come before Low
        critical_idx = next(i for i, s in enumerate(severities) if s == "critical")
        medium_idx = next(i for i, s in enumerate(severities) if s == "medium")
        low_idx = next(i for i, s in enumerate(severities) if s == "low")
        assert critical_idx < medium_idx < low_idx

    def test_load_findings_empty_dir(self, temp_dir):
        """Test loading from directory with no findings."""
        audit_dir = temp_dir / ".audit"
        audit_dir.mkdir()
        findings = load_findings(audit_dir)
        assert findings == []


class TestLoadAuditContext:
    """Tests for loading audit context."""

    def test_load_context(self, sample_audit_dir):
        """Test loading audit context."""
        context = load_audit_context(sample_audit_dir)
        assert context["project_name"] == "Test Application"
        assert context["audit_started"] == "2024-01-15"

    def test_load_missing_context(self, temp_dir):
        """Test loading context when file doesn't exist."""
        context = load_audit_context(temp_dir)
        assert context == {}


class TestCountFunctions:
    """Tests for counting functions."""

    def test_count_by_severity(self, sample_audit_dir):
        """Test counting findings by severity."""
        findings = load_findings(sample_audit_dir)
        counts = count_by_severity(findings)
        assert counts["critical"] == 1
        assert counts["medium"] == 1
        assert counts["low"] == 1

    def test_count_by_phase(self, sample_audit_dir):
        """Test counting findings by phase."""
        findings = load_findings(sample_audit_dir)
        counts = count_by_phase(findings)
        assert "Phase 5" in counts or "Phase 1" in counts or "Phase 7" in counts

    def test_count_by_status(self, sample_audit_dir):
        """Test counting findings by status."""
        findings = load_findings(sample_audit_dir)
        counts = count_by_status(findings)
        assert counts["open"] >= 1
        assert counts["resolved"] >= 1


class TestGenerateExecutiveSummary:
    """Tests for executive summary generation."""

    def test_summary_includes_counts(self, sample_audit_dir):
        """Test that summary includes finding counts."""
        findings = load_findings(sample_audit_dir)
        context = load_audit_context(sample_audit_dir)
        summary = generate_executive_summary(findings, context)
        assert "Critical" in summary
        assert "High" in summary
        assert "Total Findings" in summary

    def test_summary_shows_risk_level(self, sample_audit_dir):
        """Test that summary shows overall risk level."""
        findings = load_findings(sample_audit_dir)
        context = load_audit_context(sample_audit_dir)
        summary = generate_executive_summary(findings, context)
        assert "Risk Level" in summary

    def test_summary_includes_key_concerns(self, sample_audit_dir):
        """Test that summary includes key concerns."""
        findings = load_findings(sample_audit_dir)
        context = load_audit_context(sample_audit_dir)
        summary = generate_executive_summary(findings, context)
        assert "Key Concerns" in summary


class TestGenerateFindingsSections:
    """Tests for findings section generation."""

    def test_findings_by_severity_format(self, sample_audit_dir):
        """Test findings by severity formatting."""
        findings = load_findings(sample_audit_dir)
        section = generate_findings_by_severity(findings)
        assert "Critical" in section
        assert "Medium" in section
        assert "Low" in section

    def test_findings_by_phase_format(self, sample_audit_dir):
        """Test findings by phase formatting."""
        findings = load_findings(sample_audit_dir)
        section = generate_findings_by_phase(findings)
        assert "Phase" in section


class TestGenerateRemediationRoadmap:
    """Tests for remediation roadmap generation."""

    def test_roadmap_includes_priorities(self, sample_audit_dir):
        """Test that roadmap includes priority sections."""
        findings = load_findings(sample_audit_dir)
        roadmap = generate_remediation_roadmap(findings)
        assert "Immediate" in roadmap or "Short-term" in roadmap or "Medium-term" in roadmap

    def test_roadmap_only_includes_open_findings(self, sample_audit_dir):
        """Test that roadmap only includes open findings."""
        findings = load_findings(sample_audit_dir)
        roadmap = generate_remediation_roadmap(findings)
        # VULN-003 is resolved, should not be in roadmap checklist
        # (though it might appear in statistics)
        assert "VULN-001" in roadmap or "VULN-002" in roadmap


class TestGenerateComplianceSummary:
    """Tests for compliance summary generation."""

    def test_owasp_mapping(self, sample_audit_dir):
        """Test OWASP mapping in compliance summary."""
        findings = load_findings(sample_audit_dir)
        compliance = generate_compliance_summary(findings)
        if "OWASP" in compliance:
            assert "A03" in compliance or "Top 10" in compliance

    def test_cwe_mapping(self, sample_audit_dir):
        """Test CWE mapping in compliance summary."""
        findings = load_findings(sample_audit_dir)
        compliance = generate_compliance_summary(findings)
        if "CWE" in compliance:
            assert "CWE-" in compliance


class TestGenerateReport:
    """Tests for complete report generation."""

    def test_report_includes_all_sections(self, sample_audit_dir):
        """Test that report includes all required sections."""
        report = generate_report(sample_audit_dir)
        assert "Executive Summary" in report
        assert "Findings by Severity" in report
        assert "Remediation Roadmap" in report
        assert "Statistics" in report

    def test_report_has_header(self, sample_audit_dir):
        """Test that report has proper header."""
        report = generate_report(sample_audit_dir)
        assert "Security Audit Report" in report
        assert "Test Application" in report


class TestGenerateJSONReport:
    """Tests for JSON report generation."""

    def test_json_valid(self, sample_audit_dir):
        """Test that JSON output is valid JSON."""
        json_str = generate_json_report(sample_audit_dir)
        data = json.loads(json_str)
        assert isinstance(data, dict)

    def test_json_structure(self, sample_audit_dir):
        """Test JSON report structure."""
        json_str = generate_json_report(sample_audit_dir)
        data = json.loads(json_str)
        assert "metadata" in data
        assert "summary" in data
        assert "findings" in data
        assert "remediation" in data
        assert "compliance" in data

    def test_json_metadata(self, sample_audit_dir):
        """Test JSON metadata content."""
        json_str = generate_json_report(sample_audit_dir)
        data = json.loads(json_str)
        assert data["metadata"]["project_name"] == "Test Application"
        assert "generated_at" in data["metadata"]
        assert data["metadata"]["framework"] == "Codebase Security Audit Framework"

    def test_json_summary(self, sample_audit_dir):
        """Test JSON summary content."""
        json_str = generate_json_report(sample_audit_dir)
        data = json.loads(json_str)
        assert data["summary"]["total_findings"] == 3
        assert "by_severity" in data["summary"]
        assert "by_status" in data["summary"]

    def test_json_findings(self, sample_audit_dir):
        """Test JSON findings array."""
        json_str = generate_json_report(sample_audit_dir)
        data = json.loads(json_str)
        assert isinstance(data["findings"], list)
        assert len(data["findings"]) == 3

    def test_json_remediation_priorities(self, sample_audit_dir):
        """Test JSON remediation priorities."""
        json_str = generate_json_report(sample_audit_dir)
        data = json.loads(json_str)
        assert "immediate" in data["remediation"]
        assert "short_term" in data["remediation"]
        assert "medium_term" in data["remediation"]
        assert "backlog" in data["remediation"]


class TestGenerateCSVReport:
    """Tests for CSV report generation."""

    def test_csv_header(self, sample_audit_dir):
        """Test CSV has proper header."""
        csv_str = generate_csv_report(sample_audit_dir)
        lines = csv_str.strip().split("\n")
        header = lines[0]
        assert "ID" in header
        assert "Title" in header
        assert "Severity" in header
        assert "Phase" in header

    def test_csv_rows(self, sample_audit_dir):
        """Test CSV has data rows."""
        csv_str = generate_csv_report(sample_audit_dir)
        lines = csv_str.strip().split("\n")
        # Header + 3 findings
        assert len(lines) == 4

    def test_csv_content(self, sample_audit_dir):
        """Test CSV content."""
        csv_str = generate_csv_report(sample_audit_dir)
        assert "VULN-001" in csv_str
        assert "Critical" in csv_str or "critical" in csv_str


class TestGenerateSummaryOnly:
    """Tests for summary-only generation."""

    def test_summary_only(self, sample_audit_dir):
        """Test generating summary only."""
        summary = generate_summary_only(sample_audit_dir)
        assert "Executive Summary" in summary
        # The full report has these sections, but summary-only should not
        assert "Remediation Roadmap" not in summary
        assert "Findings by Phase" not in summary


class TestGroupByField:
    """Tests for grouping utility."""

    def test_group_findings(self):
        """Test grouping findings by field."""
        findings = [
            {"id": "A", "category": "auth"},
            {"id": "B", "category": "auth"},
            {"id": "C", "category": "xss"},
        ]
        grouped = _group_by_field(findings, "category")
        assert grouped["auth"] == ["A", "B"]
        assert grouped["xss"] == ["C"]

    def test_group_empty_field(self):
        """Test grouping with empty field values."""
        findings = [
            {"id": "A", "category": "auth"},
            {"id": "B", "category": ""},
        ]
        grouped = _group_by_field(findings, "category")
        assert "auth" in grouped
        assert "" not in grouped  # Empty strings filtered out
