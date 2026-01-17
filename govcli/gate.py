from pathlib import Path
from typing import List, Tuple
from .controls import load_controls, required_artifacts, requires_approval
from .audit import latest_approval

def check_artifacts(repo_root: Path, model_id: str, tier: str) -> List[str]:
    controls = load_controls(repo_root)
    req = required_artifacts(controls, tier)
    missing = []
    out_dir = repo_root / "artifacts" / model_id
    for fname in req:
        if not (out_dir / fname).exists():
            missing.append(str(out_dir / fname))
    return missing

def check_approval(repo_root: Path, model_id: str, tier: str) -> Tuple[bool, str]:
    controls = load_controls(repo_root)
    if not requires_approval(controls, tier):
        return True, "Approval not required for this tier."

    ev = latest_approval(repo_root, model_id)
    if not ev:
        return False, "Missing approval event in audit_log.jsonl."

    decision = ev.get("decision")
    if decision != "approved":
        return False, f"Latest approval decision is '{decision}', not 'approved'."
    return True, f"Found approval by {ev.get('actor')} with decision=approved."
