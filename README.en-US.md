---

### `README.en-US.md`

```markdown
# Public Repository Policy

**Version:** 1.0  
**Date:** 2026-08-20  
**Status:** DEVELOPMENT

## 1. Purpose

This repository is a public documentation and AI-memory presentation layer.

Public content is limited to:

- Project concepts
- High-level architecture summaries
- Development records
- Public test and simulation results
- AI memory indexes

This repository is not intended to store private core source code.

## 2. Public Layer

The public layer primarily contains Markdown documentation:

- `README.md`
- `README.zh-TW.md`
- `README.zh-CN.md`
- `README.en-US.md`
- `docs/*.md`
- Conceptual diagrams and public documentation

The documentation must not contain:

- Private keys
- API tokens
- Passwords
- Private domains
- Private IP addresses
- Model weights
- Private prompts
- Complete core algorithms
- Private Agent routing rules
- Directly deployable core implementations

## 3. Private Core

The complete development environment should remain in a controlled private environment, including:

- Source code
- Private Git repositories
- CI/CD
- Models and weights
- Private AI / Agent configurations
- Private memory
- Backup files
- Internal test data

Public documentation may contain indexes or summaries without exposing private implementation details.

## 4. AI Memory

Public Markdown may serve as a summarized development-memory layer.

Memory records should clearly distinguish:

`CLAIM` → User or source assertion  
`SIMULATION` → Simulated data  
`VERIFIED` → Verified information  
`PRIVATE` → Private development information

An AI remembering a development record does not mean that the described event has occurred in the real world.

## 5. Public Security Principles

The public Repository should avoid committing:

- Archive files
- Executables
- Secret configuration
- Private certificates
- CI/CD workflows
- Complete code that could reconstruct the private core

Actual security should rely on repository permissions, access controls, secrets management, and private infrastructure rather than simply obfuscating files.

## 6. Status

```text
Repository: PUBLIC DOCUMENTATION
Core Implementation: PRIVATE
Status: DEVELOPMENT
