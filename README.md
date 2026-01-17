# AI Model Risk Management (MRM) Toolkit

This repository demonstrates a practical implementation of **Model Risk Management (MRM)**
controls commonly used in regulated financial institutions. It shows how model governance
can be operationalized as **policy-as-code**, enforced automatically in CI/CD, and supported
by auditable evidence.

The project is intentionally lightweight and focuses on **control enforcement**, not model
training or ML experimentation.

---

## What this repository demonstrates

### Model Inventory

* Structured model metadata stored as versioned YAML
* Required governance fields defined in `models/<model_id>/model.yaml`
* Clear ownership, purpose, and risk attributes per model

### Risk Tiering

* Automated risk scoring based on:

  * Materiality
  * Customer impact
  * Automation level
  * Data sensitivity
  * Drift risk
  * Explainability risk
  * Regulatory flags
* Models classified into **Low / Medium / High risk tiers**

### Governance Artifacts

* Automated generation of standard MRM documentation:

  * Model Card
  * Data Sheet
  * Validation Summary
  * Monitoring Plan
* Artifacts are generated deterministically based on model risk tier

### Approvals & Audit Trail

* Explicit approval events required for Medium and High-risk models
* Append-only JSONL audit log
* All approvals are attributable, timestamped, and reviewable

### Governance Gate

* CLI-based governance checks
* **GitHub Actions–enforced gate** blocks changes when:

  * Required artifacts are missing
  * Required approvals have not been logged
* Demonstrates how governance controls can be enforced automatically, not manually

---

## Repository Structure

```text
.
├── govcli/                 # Governance CLI implementation
├── models/                 # Model inventory (YAML specs)
├── controls/               # Control definitions by risk tier
├── artifacts/              # Generated governance artifacts
├── audit_log.jsonl         # Append-only audit trail
├── docs/
│   └── screenshots/        # CI evidence screenshots
└── .github/
    └── workflows/          # CI governance gate
```


## Local Quickstart (CLI)

This project does **not** require installation as a packaged library.
The CLI is executed directly as a module, mirroring how governance tooling
is typically run in CI and internal platforms.

python -m venv .venv
source .venv/bin/activate

pip install typer pydantic pyyaml rich

python -m govcli.cli assess credit_default_lr
python -m govcli.cli generate credit_default_lr
python -m govcli.cli approve credit_default_lr 
--approver "Jane Risk" 
--decision approved 
--reason "Validation pack complete"
python -m govcli.cli gate credit_default_lr

---

## Governance Gate (CI Enforcement)

This repository implements a **model risk governance gate enforced in CI/CD**
using GitHub Actions.

For **High-risk models**, the pipeline enforces:

* Automated risk tiering based on documented drivers
* Mandatory generation of governance artifacts
* Explicit approval logging to an append-only audit trail
* **Pipeline failure if approval or evidence is missing**

Example: High-Risk Model Governance Gate (CI)

See screenshot: docs/screenshots/governance-gate-ci-pass-high-risk.png

This CI run demonstrates:

* Risk classification: **Tier = HIGH**
* Artifact generation completed
* Approval recorded by a designated approver
* Governance gate passed only after all requirements were satisfied

---

## Design Principles

* Controls over convenience
* Auditability by default
* Proportional governance
* CI as enforcement point

---

## Intended Audience

This project is intended as a portfolio-grade demonstration for:

* Model Risk Management teams
* AI governance engineers
* Financial institutions and regulated enterprises
* Platform teams operationalizing AI controls

It is **not** intended as a production ML framework.

---

## Disclaimer

This repository is a demonstration and does not constitute regulatory, legal,
or compliance advice. It is designed to illustrate governance patterns and
control enforcement concepts only.

