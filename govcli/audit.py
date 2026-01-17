import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Iterable

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def append_event(repo_root: Path, event: Dict[str, Any]) -> None:
    path = repo_root / "audit_log.jsonl"
    event = dict(event)
    event.setdefault("ts", _utc_now())
    line = json.dumps(event, ensure_ascii=False)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def iter_events(repo_root: Path) -> Iterable[Dict[str, Any]]:
    path = repo_root / "audit_log.jsonl"
    if not path.exists():
        return []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        yield json.loads(line)

def latest_approval(repo_root: Path, model_id: str) -> Optional[Dict[str, Any]]:
    latest = None
    for ev in iter_events(repo_root):
        if ev.get("event") == "approval" and ev.get("model_id") == model_id:
            latest = ev
    return latest
