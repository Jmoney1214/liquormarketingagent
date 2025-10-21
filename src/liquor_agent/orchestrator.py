import click, datetime as dt, pathlib as p
from typing import Any, Dict, List
from .dataio import read_json, write_json

PLAYBOOK_FILES = [
    "data/Marketing_Automation_Playbook.md",
    "data/AGENT_INTEGRATION_GUIDE.md",
    "data/AGENT_QUICK_REFERENCE.txt",
    "data/API_Integration_Guide.md",
]

def load_docs() -> List[Dict[str,str]]:
    blobs = []
    for fp in PLAYBOOK_FILES:
        path = p.Path(fp)
        if path.exists():
            blobs.append({"name": path.name, "content": path.read_text()})
    return blobs

def heuristic_plan(actions: List[Dict[str,Any]]) -> Dict[str,Any]:
    today = dt.date.today()
    days = [today + dt.timedelta(days=i) for i in range(7)]
    plan = {"period": f"{days[0]} to {days[-1]}","rationale": "High-churn win-backs + bundle AOV uplift","cohorts":["High churn","Low_Value_Frequent","Category primaries"],"kpis":["win_back_rate","aov","conversion_rate"],"sends":[]}
    for idx, act in enumerate(actions[:200]):
        day = str(days[idx % 7])
        plan["sends"].append({"date": day,"email": act["email"],"channel": act["channel"],"send_window": act["send_window"],"offer": act["offer"],"creative_hint": act["creative_hint"],"segment": act["segment"]})
    return plan

@click.command()
@click.option("--actions", "actions_path", required=True, type=click.Path(exists=True))
@click.option("--out", "out_path", required=True, type=click.Path())
def main(actions_path, out_path):
    actions_blob = read_json(actions_path)
    actions = actions_blob.get("actions", [])
    _docs = load_docs()  # reserved for LLM usage
    plan = heuristic_plan(actions)
    write_json(out_path, plan)
    print(f"Wrote {out_path} with {len(plan.get('sends', []))} sends.")

if __name__ == "__main__":
    main()
