import click, json, datetime as dt
from typing import Any, Dict, List
from .dataio import read_json, write_json

def score(record: Dict[str, Any]) -> float:
    seg = record.get("segmentation", {}) or {}
    beh = record.get("behavioral_traits", {}) or {}
    fin = record.get("financial_metrics", {}) or {}
    churn = (seg.get("churn_risk") or "").lower()
    rfm = (seg.get("rfm_segment") or "")
    s = 0
    s += 50 if churn == "high" else 10 if churn == "medium" else 0
    sr = fin.get("success_rate_pct")
    if isinstance(sr,(int,float)) and sr < 50: s += 15
    if (beh.get("night_buyer","")).lower() == "yes": s += 5
    if "Very_Frequent" in rfm or "High_Value" in rfm: s += 8
    return float(s)

def nudge(record: Dict[str, Any]) -> Dict[str, Any]:
    prefs = record.get("product_preferences", {}) or {}
    cat = (prefs.get("primary_category") or "Mixed").lower()
    seg = record.get("segmentation", {}) or {}
    churn = (seg.get("churn_risk") or "").lower()
    rfm = (seg.get("rfm_segment") or "Unknown")
    offer = "Discovery pack 3-for-2"
    msg = "Convenience + scarcity framing"
    if churn == "high":
        offer = "20% win-back discount"
    elif any(k in cat for k in ["tequila","whiskey"]):
        offer = "Premium bundle 15% off"
    elif any(k in cat for k in ["rum","vodka","beer","wine"]):
        offer = "Value bundle $50+ free delivery"
    if "Low_Value_Frequent" in rfm:
        offer = "Bundle uplift: buy 2 get 10% off"
    send_window = ["18:00","22:00"]
    return {"offer": offer, "message": msg, "send_window": send_window}

def build_actions(customers: List[Dict[str, Any]], limit: int = 300) -> List[Dict[str, Any]]:
    ranked = sorted(customers, key=score, reverse=True)[:limit]
    actions = []
    for r in ranked:
        nz = nudge(r)
        actions.append({
            "email": r.get("profile",{}).get("email","unknown@example.com"),
            "name": r.get("profile",{}).get("name","Customer"),
            "segment": r.get("segmentation",{}).get("rfm_segment","Unknown"),
            "primary_category": r.get("product_preferences",{}).get("primary_category","Mixed"),
            "offer": nz["offer"],
            "send_window": nz["send_window"],
            "channel": ["Email","SMS"],
            "creative_hint": f"{r.get('product_preferences',{}).get('primary_category','Mixed')} focus | {nz['message']}",
            "reason": "priority=churn/success_rate/behavior"
        })
    return actions

@click.command()
@click.option("--kb", "kb_path", required=True, type=click.Path(exists=True))
@click.option("--segments", "seg_path", required=True, type=click.Path(exists=True))
@click.option("--out", "out_path", required=True, type=click.Path())
@click.option("--limit", default=300, show_default=True)
def main(kb_path, seg_path, out_path, limit):
    customers = read_json(kb_path)
    _seg_rules = read_json(seg_path)
    actions = build_actions(customers, limit=limit)
    write_json(out_path, {"generated_at": dt.datetime.utcnow().isoformat() + "Z", "actions": actions})
    print(f"Wrote {out_path} with {len(actions)} actions.")

if __name__ == "__main__":
    main()
