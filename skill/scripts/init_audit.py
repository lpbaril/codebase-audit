#!/usr/bin/env python3
"""
Audit Initialization Script

Creates the .audit/ folder structure in the target project and initializes
the audit-context.md file for session persistence.

Usage:
    python init_audit.py /path/to/target

Output:
    Path to the created audit-context.md file
"""

import os
import sys
from datetime import datetime
from pathlib import Path


AUDIT_CONTEXT_TEMPLATE = '''# Audit Context

Session memory file for security audit. AI agents should read this at the start of each session to understand the current audit state.

---

## Audit Metadata

| Field | Value |
|-------|-------|
| **Project Name** | {project_name} |
| **Audit Started** | {start_date} |
| **Last Updated** | {start_date} |
| **Current Phase** | Phase 0 - Reconnaissance |
| **AI Agent** | Claude Code |
| **Audit Status** | In Progress |

---

## Technology Stack

*To be filled after Phase 0 reconnaissance*

| Component | Technology |
|-----------|------------|
| Frontend | |
| Backend | |
| Database | |
| Cloud | |
| Infrastructure | |

---

## Phase Status

| Phase | Name | Status | Findings | Date Completed |
|-------|------|--------|----------|----------------|
| 0 | Reconnaissance | Not Started | 0 | |
| 1 | Authentication | Not Started | 0 | |
| 2 | Authorization | Not Started | 0 | |
| 3 | API Security | Not Started | 0 | |
| 4 | Business Logic | Not Started | 0 | |
| 5 | Data Layer | Not Started | 0 | |
| 6 | Frontend | Not Started | 0 | |
| 7 | Infrastructure | Not Started | 0 | |
| 8 | Secrets Management | Not Started | 0 | |
| 9 | Logging & Monitoring | Not Started | 0 | |
| 10 | Error Handling | Not Started | 0 | |
| 11 | Cross-Cutting | Not Started | 0 | |
| 12 | Synthesis | Not Started | 0 | |

---

## Specialized Audits

| Audit | Status | Findings | Notes |
|-------|--------|----------|-------|
| Mobile Security | Not Applicable | 0 | |
| AWS Security | Not Applicable | 0 | |
| Kubernetes | Not Applicable | 0 | |
| GraphQL | Not Applicable | 0 | |
| Performance | Not Applicable | 0 | |

---

## Findings Summary

| ID | Title | Severity | Phase | Status |
|----|-------|----------|-------|--------|
| | | | | |

*Findings will be added as the audit progresses*

---

## Carry-Forward Summaries

### Phase 0: Reconnaissance
*Not yet completed*

### Phase 1: Authentication
*Not yet completed*

### Phase 2: Authorization
*Not yet completed*

### Phase 3: API Security
*Not yet completed*

### Phase 4: Business Logic
*Not yet completed*

### Phase 5: Data Layer
*Not yet completed*

### Phase 6: Frontend
*Not yet completed*

### Phase 7: Infrastructure
*Not yet completed*

### Phase 8: Secrets Management
*Not yet completed*

### Phase 9: Logging & Monitoring
*Not yet completed*

### Phase 10: Error Handling
*Not yet completed*

### Phase 11: Cross-Cutting
*Not yet completed*

---

## Session Notes

### Observations
*Add observations during the audit*

### Blockers
*Document any blockers or issues*

### Questions for Stakeholders
*Questions that need clarification*

---

## Resumption Instructions

When resuming this audit:

1. Check the **Current Phase** in the metadata table
2. Review the **Phase Status** table to see what's completed
3. Read the **Carry-Forward Summaries** for context
4. Check **Session Notes** for any blockers or observations
5. Continue from where the last session ended

---

## Audit Configuration

- **Output Location**: `.audit/`
- **Finding Prefix**: Based on phase (e.g., AUTH-001, API-002)
- **Report Format**: Markdown
- **Compliance Mapping**: Enabled
'''


def create_audit_structure(target: Path) -> Path:
    """Create the .audit/ folder structure."""
    audit_dir = target / ".audit"

    # Create directories
    directories = [
        audit_dir,
        audit_dir / "findings",
        audit_dir / "reports",
        audit_dir / "carry-forward",
    ]

    for d in directories:
        d.mkdir(parents=True, exist_ok=True)

    return audit_dir


def create_audit_context(audit_dir: Path, project_name: str) -> Path:
    """Create the audit-context.md file."""
    context_file = audit_dir / "audit-context.md"

    # Don't overwrite existing context
    if context_file.exists():
        print(f"Audit context already exists: {context_file}", file=sys.stderr)
        return context_file

    # Generate content
    content = AUDIT_CONTEXT_TEMPLATE.format(
        project_name=project_name,
        start_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    context_file.write_text(content, encoding='utf-8')
    return context_file


def create_gitkeep_files(audit_dir: Path):
    """Create .gitkeep files in empty directories."""
    for subdir in ["findings", "reports", "carry-forward"]:
        gitkeep = audit_dir / subdir / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()


def main():
    if len(sys.argv) < 2:
        print("Usage: python init_audit.py /path/to/target", file=sys.stderr)
        sys.exit(1)

    target = Path(sys.argv[1]).resolve()

    if not target.exists():
        print(f"Error: Path does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    if not target.is_dir():
        print(f"Error: Path is not a directory: {target}", file=sys.stderr)
        sys.exit(1)

    # Get project name from directory
    project_name = target.name

    # Create structure
    audit_dir = create_audit_structure(target)
    print(f"Created audit directory: {audit_dir}", file=sys.stderr)

    # Create context file
    context_file = create_audit_context(audit_dir, project_name)
    print(f"Created audit context: {context_file}", file=sys.stderr)

    # Create .gitkeep files
    create_gitkeep_files(audit_dir)

    # Output the context file path
    print(str(context_file))


if __name__ == "__main__":
    main()
