from pathlib import Path
from datetime import datetime, timezone
from .schemas import ModelSpec
from .risk import RiskResult

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def generate(repo_root: Path, spec: ModelSpec, risk: RiskResult) -> Path:
    out_dir = repo_root / "artifacts" / spec.model_id
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "model_card.md").write_text(_model_card(spec, risk), encoding="utf-8")
    (out_dir / "data_sheet.md").write_text(_data_sheet(spec), encoding="utf-8")
    (out_dir / "validation_report.md").write_text(_validation_report(spec, risk), encoding="utf-8")
    (out_dir / "monitoring_plan.md").write_text(_monitoring_plan(spec), encoding="utf-8")

    # Only created if user wants; gate may require it for High tier.
    # We create it anyway (empty-but-structured) to reduce friction.
    (out_dir / "change_log.md").write_text(_change_log(spec), encoding="utf-8")

    return out_dir

def _model_card(spec: ModelSpec, risk: RiskResult) -> str:
    return f"""# Model Card — {spec.name}

**Model ID:** {spec.model_id}  
**Version:** {spec.version}  
**Owner:** {spec.owner}  
**Business Line:** {spec.business_line}  
**Use Case:** {spec.use_case}  
**Status:** {spec.status}  
**Generated:** {_utc_now()}

## Risk Classification
- **Tier:** {risk.tier.upper()}
- **Score:** {risk.score}
- **Drivers:** {risk.drivers}

## Intended Use
- Primary: {spec.use_case}

## Limitations
- Add known limitations, boundary conditions, and failure modes.
- Document where human review is required.

## Explainability
- Stated explainability: **{spec.explainability}**
- For adverse action / fair lending, include reason codes approach and documentation.

## Dependencies
- Downstream systems: {", ".join(spec.deployment.downstream_systems)}
"""

def _data_sheet(spec: ModelSpec) -> str:
    feats = "\n".join([f"- {f}" for f in spec.training_data.features])
    return f"""# Data Sheet — {spec.model_id}

**Generated:** {_utc_now()}

## Training Data Summary
- Description: {spec.training_data.description}
- Time Window: {spec.training_data.time_window}
- Label: {spec.training_data.label}

## Features
{feats}

## Data Sensitivity
- Sensitivity: **{spec.data_sensitivity}**
- Jurisdictions: {", ".join(spec.jurisdictions) if spec.jurisdictions else "N/A"}

## Data Quality & Governance
- Document sources, access controls, retention, and quality checks.
- Ensure PII handling aligns with enterprise policy.
"""

def _validation_report(spec: ModelSpec, risk: RiskResult) -> str:
    return f"""# Validation Report — {spec.model_id}

**Generated:** {_utc_now()}  
**Risk Tier:** {risk.tier.upper()} (score {risk.score})

## Executive Summary
- Purpose: {spec.use_case}
- Key Risks: (fill in)
- Validation Outcome: (approved / conditional / rejected)

## Methodology Review
- Model Type: {spec.model_type}
- Training window: {spec.training_data.time_window}
- Feature list reviewed for leakage and prohibited variables.

## Performance Testing
- Metrics: (AUC/KS/etc.)
- Backtesting: (describe)
- Stability: (describe)

## Sensitivity / Stress Testing
- What happens when key features shift?
- Scenario-based checks.

## Fair Lending / Bias Checks (if applicable)
- Regulatory Flags: {", ".join(spec.regulatory_flags) if spec.regulatory_flags else "None"}
- Disparate impact / fairness metrics: (fill in)
- Adverse action explainability: (fill in)

## Model Limitations
- Document limitations and compensating controls.

## Ongoing Monitoring Requirements
- Reference Monitoring Plan.
"""

def _monitoring_plan(spec: ModelSpec) -> str:
    mon = spec.monitoring
    perf = ", ".join(mon.performance_metrics) if mon and mon.performance_metrics else "TBD"
    drift = ", ".join(mon.drift_metrics) if mon and mon.drift_metrics else "TBD"
    thresholds = mon.thresholds if mon and mon.thresholds else {}
    return f"""# Monitoring Plan — {spec.model_id}

**Generated:** {_utc_now()}

## What to Monitor
- Performance metrics: {perf}
- Drift metrics: {drift}

## Thresholds
{thresholds}

## Cadence
- Monitoring frequency: monthly (default)
- Reporting: quarterly MRM review (default)

## Alerting & Escalation
- Define who gets paged and what actions are required when thresholds are breached.

## Retraining / Revalidation Triggers
- Material drift
- Data source changes
- Policy changes
- Performance degradation
"""

def _change_log(spec: ModelSpec) -> str:
    return f"""# Change Log — {spec.model_id}

**Generated:** {_utc_now()}

## {spec.version}
- Initial governance pack generated.
- Add future entries for:
  - data changes
  - feature changes
  - model re-training
  - threshold changes
  - deployment changes
"""
