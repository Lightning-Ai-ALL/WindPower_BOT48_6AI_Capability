# Public Repository Policy

**Version**: 1.0  
**Date**: 2026-08-20  
**Status**: Active  

---

## Copyright Notice

This document and all original content contributed by project maintainers are protected by copyright law.  
Any unauthorized reproduction, distribution, modification, or commercial use is prohibited except as explicitly permitted by this policy.  

---

## 1. Purpose

This repository is a **concept showcase and public memory layer**, intended solely for describing system architecture, research direction, and verifiable performance data.  
**It is prohibited** to place any sensitive, executable, or core-implementation-revealing material into this repository.

---

## 2. Allowed Content

The following content **may** appear in this repository:

- `README.md`: Project overview, architecture diagrams, API concept descriptions.
- `docs/`: Architecture documents, data flow diagrams, module capability tables (using neutral naming).
- `benchmark/`: Simulation test results, latency data, accuracy metrics (must be marked `SIMULATION` or `PROTOTYPE`).
- `examples/`: Input/output samples of public interfaces (without real keys or complete business logic).
- `tests/`: Public test cases (testing only public interfaces, no private dependencies).
- `LICENSE`: Open-source license (if applicable).
- `SECURITY.md`: Security policy and reporting process.

**All Markdown files must not contain internal Bot/AI specific names, private IPs, domain names, keys, weight paths, or complete algorithm descriptions.**

---

## 3. Prohibited Content

The following content is **strictly prohibited** from appearing in this repository:

- Archive files: `.zip`, `.7z`, `.rar`, `.tar`, `.gz`, `.bz2`, `.xz`
- Source code files: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.sh`, `.ps1`, `.bat`, `.cmd`
- Configuration files: `.yml`, `.yaml`, `.json`, `.env`, `.ini`, `.toml`
- Executable / binary files: `.exe`, `.dll`, `.so`, `.dylib`, `.bin`, `.iso`
- Keys and certificates: `.pem`, `.key`, `.crt`, `.pfx`
- Version control metadata: `.git/`, `.github/`, `.gitlab/`, `.gitignore` (only a minimal `.gitignore` to exclude junk files is allowed)
- CI/CD workflows: `.github/workflows/`, `.gitlab-ci.yml`
- Any document containing internal naming (such as specific Bot codenames or module codenames)
- Any test data not marked as `SIMULATION`
- Any information that may expose private repository structure, internal IPs, domain names, or credentials

**Violating files will be automatically blocked by the public-layer firewall or immediately removed by administrators.**

---

## 4. Code Visibility Policy

This repository adopts a **public shell + private core** architecture:

- **Public repository**: Contains only documentation, interface definitions, examples, and tests.
- **Private repository**: Contains core implementation, model weights, Router, Memory, Agent, Prompt, and keys.
- When referencing core modules in public code, abstract interfaces or placeholders must be used; private dependencies must not be directly exposed.
- Private repository access is granted only to:
  - Core development team
  - AI assistants cooperating with the user (via fine-grained personal access token with read-only permission)
- The public repository's CI checker (placed in the private management repository) will validate file types and sensitive patterns before pushing.

---

## 5. Enforcement

- Scan file types and paths using `public_channel_guard.py`.
- Check before merging via GitHub Actions (existing only in the private repository).
- Manually review all Markdown files to ensure no internal naming leakage.

Submissions violating this policy will be rejected and recorded in the audit log.

---

## 6. Important Notice

This repository is a **conceptual reference** and does not constitute an executable product, patent, or commercial promise.  
Any actual deployment requires independent engineering and safety certification.

---

**End of Policy**
