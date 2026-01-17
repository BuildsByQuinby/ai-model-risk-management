# AI Model Risk Management (MRM) Toolkit

This repository demonstrates a practical implementation of **Model Risk Management (MRM)** controls commonly used in regulated financial institutions. It is designed to be lightweight, auditable, and CI-enforced.

## What it does
- **Model Inventory** (`models/<id>/model.yaml`) with required governance fields
- **Risk Tiering** (Low/Medium/High) based on materiality, customer impact, automation, data sensitivity, drift risk, explainability
- **Artifact Generation** (Model Card, Data Sheet, Validation Report, Monitoring Plan)
- **Approvals + Audit Trail** (append-only JSONL audit log)
- **Governance Gate** (CLI + GitHub Actions) to block releases without required evidence

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .

gov assess credit_default_lr
gov generate credit_default_lr
gov approve credit_default_lr --approver "Jane Risk" --decision approved --reason "Validation pack complete"
gov gate credit_default_lr
