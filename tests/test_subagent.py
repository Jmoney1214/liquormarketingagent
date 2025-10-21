from liquor_agent.subagent import build_actions

def test_smoke():
    acts = build_actions([{'profile':{'email':'a@x.com'},'segmentation':{'rfm_segment':'Low_Value_Frequent','churn_risk':'High'},'behavioral_traits':{'night_buyer':'Yes'},'financial_metrics':{'success_rate_pct':40},'product_preferences':{'primary_category':'Rum'}}], limit=5)
    assert acts and 'offer' in acts[0]
