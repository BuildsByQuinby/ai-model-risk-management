from pathlib import Path
from typing import Dict, Any, List
import yaml

def load_controls(repo_root: Path) -> Dict[str, Any]:
    path = repo_root / "controls" / "mrm_controls.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data

def required_artifacts(controls: Dict[str, Any], tier: str) -> List[str]:
    tiers = controls.get("tiers", {})
    if tier not in tiers:
        raise ValueError(f"Unknown tier '{tier}' in controls config.")
    return list(tiers[tier].get("required_artifacts", []))

def requires_approval(controls: Dict[str, Any], tier: str) -> bool:
    return bool(controls.get("tiers", {}).get(tier, {}).get("requires_approval", False))
