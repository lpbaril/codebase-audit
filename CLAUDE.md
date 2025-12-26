# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **security audit methodology framework** - a collection of structured markdown documents designed for conducting LLM-assisted security audits of full-stack applications. There is no build system, no automated tests, and no code to compile.

**Target use case:** Security professionals using Claude or similar LLMs to systematically audit codebases, with special focus on air-gapped environments, sensitive data handling, and enterprise security requirements.

## Repository Structure

- **`core-phases/`** - 13 sequential audit phases (00-12), each containing prompts to paste into an LLM conversation along with target code
- **`specialized/`** - Deep-dive audits for GraphQL, Kubernetes, and API penetration testing
- **`templates/`** - Finding documentation template and progress tracker
- **`checklists/`** - Master checklist consolidating all phases

## How the Framework Works

1. **Sequential execution**: Phases 0-12 run in order, each building on previous findings
2. **Carry-forward system**: Each phase produces a summary that provides context to the next phase
3. **Prompt-based**: Each phase markdown file contains a prompt section (in code blocks) to paste into an LLM conversation
4. **Manual verification**: LLM findings should be validated by the auditor

## Working with This Repository

When asked to help with this framework:
- Each phase is self-contained in its markdown file
- Prompts are in triple-backtick code blocks within each phase file
- "Air-Gap Specific" sections appear throughout for offline environment considerations
- Finding severity levels: Critical > High > Medium > Low > Info

## Key Files

| File | Purpose |
|------|---------|
| `templates/finding-template.md` | Standard format for documenting vulnerabilities |
| `templates/progress-tracker.md` | Tracking sheet for audit timeline |
| `checklists/master-checklist.md` | Quick reference across all phases |
