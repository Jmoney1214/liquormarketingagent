"""OpenAI integration for AI-powered campaign planning"""
from typing import Any, Dict, List, Optional
from .core.config import settings


def plan_with_openai(
    system_prompt: str,
    user_prompt: str,
    context_docs: List[Dict[str, str]],
    actions: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Generate a campaign plan using OpenAI GPT-4.
    
    This is the AI "brain" that creates optimized marketing campaigns.
    
    Args:
        system_prompt: System role/instructions for the AI
        user_prompt: User's specific request (e.g., "Build a 7-day plan...")
        context_docs: Marketing playbooks and guidelines
        actions: Prioritized customer actions from subagent
        
    Returns:
        AI-generated campaign plan or None if AI fails
    """
    # If no OpenAI key, fall back to heuristic (caller handles None)
    if not settings.OPENAI_API_KEY:
        print("No OpenAI API key configured, using heuristic planning")
        return None
    
    try:
        from openai import OpenAI
        import json
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Lightweight "RAG": concat house docs (good enough for MVP)
        corpus = "\n\n".join([
            f"# {d['name']}\n{d['content'][:8000]}"
            for d in context_docs
        ])
        
        default_system = (
            "You are a revenue-obsessed liquor retail strategist.\n"
            "Honor legal/responsible marketing. Use house playbooks.\n"
            "Synthesize 'actions' to produce a 7-day JSON plan with fields: "
            "period, rationale, cohorts, kpis, "
            "sends[{date,email,channel,send_window,offer,creative_hint,segment}].\n"
            f"Docs:\n{corpus[:15000]}"
        )
        
        sys_msg = system_prompt or default_system
        tool_blob = {"actions": actions}

        # Call OpenAI API
        resp = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or gpt-4, gpt-3.5-turbo
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": json.dumps(tool_blob)},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=2000,
        )
        
        # Parse response
        plan = json.loads(resp.choices[0].message.content)
        return plan
        
    except Exception as e:
        # Any exception -> let caller fall back to heuristic
        print(f"OpenAI planning failed: {e}")
        return None

