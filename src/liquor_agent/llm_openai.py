from typing import Any, Dict, List, Optional
from .config import settings

def plan_with_openai(system_prompt: str,
                     user_prompt: str,
                     context_docs: List[Dict[str, str]],
                     actions: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    # If no key, fall back to heuristic (caller handles None)
    if not settings.openai_api_key:
        return None
    try:
        from openai import OpenAI
        import json
        client = OpenAI()

        # lightweight “RAG”: concat house docs (good enough for MVP)
        corpus = "\n\n".join([f"# {d['name']}\n{d['content'][:8000]}" for d in context_docs])
        default_system = (
            "You are a revenue-obsessed liquor retail strategist.\n"
            "Honor legal/responsible marketing. Use house playbooks.\n"
            "Synthesize 'actions' to produce a 7-day JSON plan with fields: "
            "period, rationale, cohorts, kpis, sends[{date,email,channel,send_window,offer,creative_hint,segment}].\n"
            f"Docs:\n{corpus[:15000]}"
        )
        sys_msg = system_prompt or default_system
        tool_blob = {"actions": actions}

        resp = client.responses.create(
            model=settings.model,   # uses MODEL from .env (e.g., gpt-4.1)
            input=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_prompt},
                {"role": "tool", "content": "json:" + json.dumps(tool_blob)},
            ],
            response_format={"type": "json_object"},
        )
        return __import__("json").loads(resp.output_text)
    except Exception:
        # Any exception -> let caller fall back to heuristic
        return None
