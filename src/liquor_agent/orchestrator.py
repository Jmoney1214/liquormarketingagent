import click, datetime as dt, pathlib as p
from typing import Any, Dict, List
from .dataio import read_json, write_json
from .llm_openai import plan_with_openai

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
    plan = {
        "period": f"{days[0]} to {days[-1]}",
        "rationale": "Focus high-churn win-backs and bundle AOV uplift. Timing aligned to buyer behavior.",
        "cohorts": ["High churn", "Low_Value_Frequent", "Category primaries"],
        "kpis": ["win_back_rate", "aov", "conversion_rate"],
        "sends": []
    }
    for idx, act in enumerate(actions[:200]):
        day = str(days[idx % 7])
        plan["sends"].append({
            "date": day,
            "email": act.get("email"),
            "channel": act.get("channel", ["Email"]),
            "send_window": act.get("send_window", ["18:00","22:00"]),
            "offer": act.get("offer",""),
            "creative_hint": act.get("creative_hint",""),
            "segment": act.get("segment","")
        })
    return plan

@click.command()
@click.option("--actions", "actions_path", required=True, type=click.Path(exists=True), help="subagent_actions.json path")
@click.option("--out", "out_path", required=True, type=click.Path(), help="Output weekly plan JSON")
def main(actions_path, out_path):
    actions_blob = read_json(actions_path)
    actions = actions_blob.get("actions", [])
    docs = load_docs()
    llm_plan = plan_with_openai(
        system_prompt="You are a revenue-obsessed liquor retail strategist.",
        user_prompt="Build a 7-day plan to lift AOV and win back high-churn customers.",
        context_docs=docs,
        actions=actions
    )
    plan = llm_plan if llm_plan else heuristic_plan(actions)
    plan["engine"] = "llm" if llm_plan else "heuristic"
    write_json(out_path, plan)
    click.echo(f"Wrote {out_path} with {len(plan.get('sends', []))} sends.")

if __name__ == "__main__":
    main()
