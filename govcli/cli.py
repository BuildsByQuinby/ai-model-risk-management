from pathlib import Path
import yaml
import typer
from rich import print
from rich.table import Table

from .schemas import ModelSpec
from .risk import assess
from .artifacts import generate as generate_artifacts
from .audit import append_event
from .gate import check_artifacts, check_approval

app = typer.Typer(add_completion=False)

def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]

def load_model_spec(root: Path, model_id: str) -> ModelSpec:
    path = root / "models" / model_id / "model.yaml"
    if not path.exists():
        raise typer.BadParameter(f"Model spec not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ModelSpec.model_validate(data)

@app.command()
def assess_model(model_id: str = typer.Argument(..., help="Model ID in models/<model_id>/model.yaml")):
    """Assess model risk and output tier + drivers."""
    root = repo_root()
    spec = load_model_spec(root, model_id)
    res = assess(spec)

    table = Table(title=f"Risk Assessment — {model_id}")
    table.add_column("Driver")
    table.add_column("Value", justify="right")
    for k, v in res.drivers.items():
        table.add_row(k, str(v))
    print(table)
    print(f"[bold]Score:[/bold] {res.score}  |  [bold]Tier:[/bold] {res.tier.upper()}")

@app.command()
def generate(model_id: str = typer.Argument(..., help="Model ID to generate governance artifacts for.")):
    """Generate governance artifacts into artifacts/<model_id>/."""
    root = repo_root()
    spec = load_model_spec(root, model_id)
    res = assess(spec)
    out_dir = generate_artifacts(root, spec, res)
    print(f"[green]Generated artifacts:[/green] {out_dir}")

@app.command()
def approve(
    model_id: str,
    approver: str = typer.Option(..., "--approver", help="Approver name"),
    decision: str = typer.Option("approved", "--decision", help="approved|rejected|conditional"),
    reason: str = typer.Option(..., "--reason", help="Short justification"),
):
    """Append an approval event to the audit log."""
    root = repo_root()
    # minimal validation
    if decision not in {"approved", "rejected", "conditional"}:
        raise typer.BadParameter("decision must be approved|rejected|conditional")

    append_event(
        root,
        {
            "event": "approval",
            "actor": approver,
            "model_id": model_id,
            "decision": decision,
            "details": {"reason": reason},
        },
    )
    print(f"[green]Audit logged:[/green] approval={decision} for {model_id} by {approver}")

@app.command()
def gate(model_id: str):
    """Fail if required governance evidence is missing for the model's risk tier."""
    root = repo_root()
    spec = load_model_spec(root, model_id)
    res = assess(spec)

    missing = check_artifacts(root, model_id, res.tier)
    ok_approval, approval_msg = check_approval(root, model_id, res.tier)

    if missing:
        print("[red]Missing required artifacts:[/red]")
        for m in missing:
            print(f" - {m}")

    if not ok_approval:
        print(f"[red]Approval check failed:[/red] {approval_msg}")
    else:
        print(f"[green]Approval check:[/green] {approval_msg}")

    if missing or not ok_approval:
        raise typer.Exit(code=1)

    print(f"[green]Governance gate PASS[/green] — tier={res.tier.upper()} model={model_id}")

# nicer command name: `gov assess <id>`
app.command("assess")(assess_model)
