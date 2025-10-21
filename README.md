# Liquor Marketing Agent (Two-Agent Stack)

## Quickstart
```bash
pip install -e .[openai,dev]
cp sample_data/* data/
liquor-subagent --kb data/agent_knowledge_base.json --segments data/segment_playbooks.json --out outputs/subagent_actions.json
liquor-plan --actions outputs/subagent_actions.json --out outputs/weekly_plan.json
```

## Push to GitHub (two supported flows)
### A) GitHub CLI
```bash
brew install gh
gh auth login
./scripts/push_with_gh.sh <owner> <repo> --private
```
### B) Personal Access Token
```bash
export GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
./scripts/push_with_pat.sh <owner> <repo> true
```
