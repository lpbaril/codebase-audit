#!/usr/bin/env python3
"""
Report Generation Script

Compiles all audit findings into a final report with executive summary,
prioritized remediation roadmap, and compliance mapping.

Usage:
    python generate_report.py /path/to/.audit

Output:
    Writes final-report.md to the .audit directory
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 4,
    "informational": 4,
}

SEVERITY_EMOJI = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🔵",
    "info": "⚪",
    "informational": "⚪",
}


def read_file(path: Path) -> str:
    """Read file content."""
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        return ""


def extract_field(content: str, field: str) -> str:
    """Extract a field value from markdown content."""
    patterns = [
        rf'\|\s*\*?\*?{field}\*?\*?\s*\|\s*([^|]+)\s*\|',
        rf'(?:##\s*{field}|^\*\*{field}\*?\*?:?)\s*[:\-]?\s*(.+?)(?:\n|$)',
        rf'{field}\s*:\s*(.+?)(?:\n|$)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()

    return ""


def parse_finding(path: Path) -> dict:
    """Parse a finding file into a structured dict."""
    content = read_file(path)
    if not content:
        return None

    finding = {
        "file": path.name,
        "id": extract_field(content, "id") or path.stem,
        "title": extract_field(content, "title") or "Untitled Finding",
        "severity": extract_field(content, "severity").lower() or "medium",
        "phase": extract_field(content, "phase") or "Unknown",
        "status": extract_field(content, "status").lower() or "open",
        "owasp": extract_field(content, "owasp") or "",
        "cwe": extract_field(content, "cwe") or "",
        "description": "",
        "impact": extract_field(content, "impact") or "",
        "recommendation": extract_field(content, "recommendation") or "",
    }

    # Try to extract description section
    desc_match = re.search(r'##\s*Description\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if desc_match:
        finding["description"] = desc_match.group(1).strip()[:500]  # Limit length

    return finding


def load_findings(audit_dir: Path) -> list:
    """Load all findings from the findings directory."""
    findings_dir = audit_dir / "findings"
    if not findings_dir.exists():
        return []

    findings = []
    for f in findings_dir.glob("*.md"):
        if f.name.startswith("."):
            continue
        finding = parse_finding(f)
        if finding:
            findings.append(finding)

    # Sort by severity
    findings.sort(key=lambda x: SEVERITY_ORDER.get(x["severity"], 5))

    return findings


def load_audit_context(audit_dir: Path) -> dict:
    """Load audit context metadata."""
    context_file = audit_dir / "audit-context.md"
    if not context_file.exists():
        return {}

    content = read_file(context_file)

    return {
        "project_name": extract_field(content, "Project Name") or "Unknown Project",
        "audit_started": extract_field(content, "Audit Started") or "",
        "last_updated": extract_field(content, "Last Updated") or "",
        "audit_status": extract_field(content, "Audit Status") or "Unknown",
    }


def count_by_severity(findings: list) -> dict:
    """Count findings by severity."""
    counts = defaultdict(int)
    for f in findings:
        counts[f["severity"]] += 1
    return dict(counts)


def count_by_phase(findings: list) -> dict:
    """Count findings by phase."""
    counts = defaultdict(int)
    for f in findings:
        # Extract phase number
        phase_match = re.search(r'(\d+)', f["phase"])
        if phase_match:
            counts[f"Phase {phase_match.group(1)}"] += 1
        else:
            counts[f["phase"]] += 1
    return dict(counts)


def count_by_status(findings: list) -> dict:
    """Count findings by status."""
    counts = defaultdict(int)
    for f in findings:
        counts[f["status"]] += 1
    return dict(counts)


def generate_executive_summary(findings: list, context: dict) -> str:
    """Generate executive summary section."""
    by_severity = count_by_severity(findings)

    critical_count = by_severity.get("critical", 0)
    high_count = by_severity.get("high", 0)

    risk_level = "Low"
    if critical_count > 0:
        risk_level = "Critical"
    elif high_count > 2:
        risk_level = "High"
    elif high_count > 0:
        risk_level = "Medium"

    summary = f"""## Executive Summary

### Overview

| Metric | Value |
|--------|-------|
| **Project** | {context.get('project_name', 'Unknown')} |
| **Audit Date** | {context.get('audit_started', datetime.now().strftime('%Y-%m-%d'))} |
| **Total Findings** | {len(findings)} |
| **Overall Risk Level** | {risk_level} |

### Findings by Severity

| Severity | Count |
|----------|-------|
| 🔴 Critical | {by_severity.get('critical', 0)} |
| 🟠 High | {by_severity.get('high', 0)} |
| 🟡 Medium | {by_severity.get('medium', 0)} |
| 🔵 Low | {by_severity.get('low', 0)} |
| ⚪ Informational | {by_severity.get('info', 0) + by_severity.get('informational', 0)} |

### Key Concerns

"""

    # Add top 3 critical/high findings
    critical_high = [f for f in findings if f["severity"] in ["critical", "high"]][:3]
    if critical_high:
        for i, f in enumerate(critical_high, 1):
            emoji = SEVERITY_EMOJI.get(f["severity"], "⚪")
            summary += f"{i}. {emoji} **{f['id']}**: {f['title']}\n"
    else:
        summary += "No critical or high severity findings identified.\n"

    return summary


def generate_findings_by_severity(findings: list) -> str:
    """Generate findings organized by severity."""
    content = "## Findings by Severity\n\n"

    for severity in ["critical", "high", "medium", "low", "info"]:
        severity_findings = [f for f in findings if f["severity"] == severity]
        if not severity_findings:
            continue

        emoji = SEVERITY_EMOJI.get(severity, "⚪")
        content += f"### {emoji} {severity.title()} ({len(severity_findings)})\n\n"

        for f in severity_findings:
            content += f"#### {f['id']}: {f['title']}\n\n"
            content += f"- **Phase**: {f['phase']}\n"
            content += f"- **Status**: {f['status'].title()}\n"
            if f['owasp']:
                content += f"- **OWASP**: {f['owasp']}\n"
            if f['cwe']:
                content += f"- **CWE**: {f['cwe']}\n"
            if f['description']:
                content += f"\n{f['description'][:300]}...\n" if len(f['description']) > 300 else f"\n{f['description']}\n"
            content += "\n"

    return content


def generate_findings_by_phase(findings: list) -> str:
    """Generate findings organized by phase."""
    content = "## Findings by Phase\n\n"

    by_phase = count_by_phase(findings)

    for phase in sorted(by_phase.keys(), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 99):
        phase_findings = [f for f in findings if phase.split()[-1] in f["phase"]]
        if not phase_findings:
            continue

        content += f"### {phase} ({len(phase_findings)} findings)\n\n"

        content += "| ID | Title | Severity | Status |\n"
        content += "|----|----|----|----|----|\n"

        for f in phase_findings:
            emoji = SEVERITY_EMOJI.get(f["severity"], "⚪")
            content += f"| {f['id']} | {f['title']} | {emoji} {f['severity'].title()} | {f['status'].title()} |\n"

        content += "\n"

    return content


def generate_remediation_roadmap(findings: list) -> str:
    """Generate prioritized remediation roadmap."""
    content = "## Remediation Roadmap\n\n"

    # Immediate (Critical)
    critical = [f for f in findings if f["severity"] == "critical" and f["status"] == "open"]
    if critical:
        content += "### 🚨 Immediate (Fix Now)\n\n"
        for f in critical:
            content += f"- [ ] **{f['id']}**: {f['title']}\n"
            if f['recommendation']:
                content += f"  - {f['recommendation'][:200]}\n"
        content += "\n"

    # Short-term (High, 1-4 weeks)
    high = [f for f in findings if f["severity"] == "high" and f["status"] == "open"]
    if high:
        content += "### ⚠️ Short-term (1-4 weeks)\n\n"
        for f in high:
            content += f"- [ ] **{f['id']}**: {f['title']}\n"
        content += "\n"

    # Medium-term (Medium, 1-3 months)
    medium = [f for f in findings if f["severity"] == "medium" and f["status"] == "open"]
    if medium:
        content += "### 📋 Medium-term (1-3 months)\n\n"
        for f in medium:
            content += f"- [ ] **{f['id']}**: {f['title']}\n"
        content += "\n"

    # Backlog (Low/Info)
    low = [f for f in findings if f["severity"] in ["low", "info", "informational"] and f["status"] == "open"]
    if low:
        content += "### 📝 Backlog\n\n"
        for f in low:
            content += f"- [ ] **{f['id']}**: {f['title']}\n"
        content += "\n"

    return content


def generate_compliance_summary(findings: list) -> str:
    """Generate compliance framework mapping summary."""
    content = "## Compliance Mapping\n\n"

    # OWASP Top 10
    owasp_findings = [f for f in findings if f["owasp"]]
    if owasp_findings:
        content += "### OWASP Top 10\n\n"
        owasp_map = defaultdict(list)
        for f in owasp_findings:
            owasp_map[f["owasp"]].append(f["id"])

        content += "| OWASP Category | Findings |\n"
        content += "|----------------|----------|\n"
        for owasp, ids in sorted(owasp_map.items()):
            content += f"| {owasp} | {', '.join(ids)} |\n"
        content += "\n"

    # CWE
    cwe_findings = [f for f in findings if f["cwe"]]
    if cwe_findings:
        content += "### CWE References\n\n"
        cwe_map = defaultdict(list)
        for f in cwe_findings:
            cwe_map[f["cwe"]].append(f["id"])

        content += "| CWE | Findings |\n"
        content += "|-----|----------|\n"
        for cwe, ids in sorted(cwe_map.items()):
            content += f"| {cwe} | {', '.join(ids)} |\n"
        content += "\n"

    return content


def generate_report(audit_dir: Path) -> str:
    """Generate the complete final report."""
    context = load_audit_context(audit_dir)
    findings = load_findings(audit_dir)

    report = f"""# Security Audit Report

**Project:** {context.get('project_name', 'Unknown Project')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Framework:** Codebase Security Audit Framework

---

"""

    report += generate_executive_summary(findings, context)
    report += "\n---\n\n"
    report += generate_findings_by_severity(findings)
    report += "\n---\n\n"
    report += generate_findings_by_phase(findings)
    report += "\n---\n\n"
    report += generate_remediation_roadmap(findings)
    report += "\n---\n\n"
    report += generate_compliance_summary(findings)
    report += "\n---\n\n"

    # Statistics
    by_status = count_by_status(findings)
    report += f"""## Statistics

| Metric | Count |
|--------|-------|
| Total Findings | {len(findings)} |
| Open | {by_status.get('open', 0)} |
| In Progress | {by_status.get('in progress', 0) + by_status.get('in-progress', 0)} |
| Resolved | {by_status.get('resolved', 0) + by_status.get('fixed', 0)} |
| Accepted Risk | {by_status.get('accepted risk', 0) + by_status.get('accepted-risk', 0)} |

---

*Report generated by Codebase Security Audit Framework*
"""

    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py /path/to/.audit", file=sys.stderr)
        sys.exit(1)

    audit_dir = Path(sys.argv[1]).resolve()

    if not audit_dir.exists():
        print(f"Error: Audit directory does not exist: {audit_dir}", file=sys.stderr)
        sys.exit(1)

    # Generate report
    report = generate_report(audit_dir)

    # Write to file
    report_path = audit_dir / "final-report.md"
    report_path.write_text(report, encoding='utf-8')

    print(f"Report generated: {report_path}")

    # Also output to stdout
    print("\n" + "="*60)
    print(report)


if __name__ == "__main__":
    main()
