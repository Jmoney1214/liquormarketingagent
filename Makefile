PY=python3
install:
	pip install -e .[openai,dev]

actions:
	$(PY) -m liquor_agent.subagent --kb data/agent_knowledge_base.json --segments data/segment_playbooks.json --out outputs/subagent_actions.json

plan:
	$(PY) -m liquor_agent.orchestrator --actions outputs/subagent_actions.json --out outputs/weekly_plan.json

demo:
	mkdir -p outputs
	cp -n sample_data/* data/ 2>/dev/null || true
	$(MAKE) actions
	$(MAKE) plan
