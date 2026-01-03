# Changelog

All notable changes to the Codebase Security Audit Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-03

### Added
- **Phase 13: Remediation Verification** - New phase for verifying fixes are complete and effective, including bypass testing and regression analysis
- **Threat Modeling (STRIDE)** - Added comprehensive threat modeling section to Phase 0 with STRIDE analysis, trust boundaries, and high-value target identification
- **Rules of Engagement Template** - Professional pre-engagement questionnaire covering scope, authorization, restrictions, and sign-off
- **JSON/CSV Report Export** - `generate_report.py` now supports `--format json`, `--format csv`, and `--format all` for enterprise integration
- **Unit Test Suite** - 122 pytest tests covering `detect_stack.py`, `validate_finding.py`, and `generate_report.py`
- **CI/CD Workflows** - GitHub Actions for automated testing, security scanning, and PR feedback
- **Condensed Phase 13** for Claude Code skill integration (`skill/phases/phase-13.md`)

### Changed
- Phase 0 renamed to "Codebase Reconnaissance, Threat Modeling & Attack Surface Mapping"
- Phase 0 now includes 9 tasks (previously 8) with threat modeling as task #2
- Phase 0 duration updated from 30-60 minutes to 60-90 minutes
- `generate_report.py` now uses argparse for CLI arguments (backward compatible)

### Fixed
- N/A

## [1.0.0] - 2024-12-XX

### Added
- Initial release of 12-phase security audit methodology
- Core phases 0-12 covering reconnaissance through synthesis
- Specialized audits: Mobile, AWS, Kubernetes, GraphQL, API penetration testing, Frontend performance, Vibe coding
- Claude Code skill integration with automated orchestration
- Python utility scripts: `detect_stack.py`, `generate_report.py`, `init_audit.py`, `validate_finding.py`
- Templates: Finding template, Audit context template, Progress tracker
- Master checklist and compliance mapping (OWASP, SOC2, HIPAA, PCI-DSS, GDPR, ISO-27001)
- Air-gap focused methodology for sensitive environments
