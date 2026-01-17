from dataclasses import dataclass
from typing import Dict, Tuple
from .schemas import ModelSpec

SCORE_MAP = {"low": 1, "medium": 2, "high": 3}
AUTOMATION_MAP = {"decision_support": 1, "partial_auto": 2, "full_auto": 3}
SENSITIVITY_MAP = {"none": 0, "internal": 1, "pii": 2}

@dataclass(frozen=True)
class RiskResult:
    score: int
    tier: str
    drivers: Dict[str, int]

def _tier(score: int) -> str:
    # Finance-friendly: conservative thresholds
    if score >= 12:
        return "high"
    if score >= 8:
        return "medium"
    return "low"

def assess(spec: ModelSpec) -> RiskResult:
    drivers = {
        "materiality": SCORE_MAP[spec.materiality],
        "customer_impact": SCORE_MAP[spec.customer_impact],
        "automation_level": AUTOMATION_MAP[spec.automation_level],
        "data_sensitivity": SENSITIVITY_MAP[spec.data_sensitivity],
        "drift_risk": SCORE_MAP[spec.drift_risk],
        # Explainability: low explainability increases risk
        "explainability_risk": {"high": 0, "medium": 1, "low": 2}[spec.explainability],
    }
    score = sum(drivers.values())

    # Regulatory flags bump risk (fair lending / adverse action etc.)
    if spec.regulatory_flags:
        score += 1
        drivers["regulatory_flags_bump"] = 1

    return RiskResult(score=score, tier=_tier(score), drivers=drivers)
