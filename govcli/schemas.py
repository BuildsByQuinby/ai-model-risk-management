from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field

Level3 = Literal["low", "medium", "high"]
Automation = Literal["decision_support", "partial_auto", "full_auto"]
Sensitivity = Literal["none", "internal", "pii"]
Explainability = Level3
DriftRisk = Level3

class TrainingData(BaseModel):
    description: str
    time_window: str
    label: str
    features: List[str]

class Deployment(BaseModel):
    environment: str
    interface: str
    downstream_systems: List[str] = Field(default_factory=list)

class Monitoring(BaseModel):
    performance_metrics: List[str] = Field(default_factory=list)
    drift_metrics: List[str] = Field(default_factory=list)
    thresholds: Dict[str, Any] = Field(default_factory=dict)

class ModelSpec(BaseModel):
    model_id: str
    name: str
    owner: str
    business_line: str
    use_case: str
    model_type: str
    status: str
    version: str

    automation_level: Automation
    customer_impact: Level3
    materiality: Level3
    data_sensitivity: Sensitivity
    explainability: Explainability
    drift_risk: DriftRisk

    jurisdictions: List[str] = Field(default_factory=list)
    regulatory_flags: List[str] = Field(default_factory=list)

    training_data: TrainingData
    deployment: Deployment
    monitoring: Optional[Monitoring] = None
