"""Campaign planning service using AI orchestrator"""
from typing import Dict, Any, List
from datetime import date, timedelta


class CampaignPlanningService:
    """Service for AI-powered campaign planning using orchestrator logic"""
    
    @staticmethod
    def generate_heuristic_plan(
        actions: List[Dict[str, Any]],
        start_date: date,
        duration_days: int = 7
    ) -> Dict[str, Any]:
        """
        Generate a campaign plan using heuristic logic.
        
        Uses logic from src/liquor_agent/orchestrator.py
        
        Args:
            actions: List of action dictionaries from subagent
            start_date: Campaign start date
            duration_days: Number of days for the campaign
            
        Returns:
            Campaign plan dictionary
        """
        # Generate date range
        days = [start_date + timedelta(days=i) for i in range(duration_days)]
        
        plan = {
            "period": f"{days[0]} to {days[-1]}",
            "rationale": "Focus high-churn win-backs and bundle AOV uplift. Timing aligned to buyer behavior.",
            "cohorts": ["High churn", "Low_Value_Frequent", "Category primaries"],
            "kpis": ["win_back_rate", "aov", "conversion_rate"],
            "sends": [],
            "engine": "heuristic"
        }
        
        # Distribute actions across days (max 200 actions)
        for idx, action in enumerate(actions[:200]):
            day_str = str(days[idx % duration_days])
            
            send = {
                "date": day_str,
                "email": action.get("email"),
                "channel": action.get("channel", ["Email"]),
                "send_window": action.get("send_window", ["18:00", "22:00"]),
                "offer": action.get("offer", ""),
                "creative_hint": action.get("creative_hint", ""),
                "segment": action.get("segment", ""),
            }
            
            # Add phone if available
            if action.get("phone"):
                send["phone"] = action["phone"]
            
            plan["sends"].append(send)
        
        return plan
    
    @staticmethod
    async def generate_ai_plan(
        actions: List[Dict[str, Any]],
        start_date: date,
        duration_days: int = 7,
        objective: str = "Build a 7-day plan to lift AOV and win back high-churn customers.",
        context_docs: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a campaign plan using AI (OpenAI).
        
        Uses AI orchestration logic from src/liquor_agent/orchestrator.py
        
        Args:
            actions: List of action dictionaries
            start_date: Campaign start date
            duration_days: Campaign duration
            objective: Campaign objective/prompt
            context_docs: Optional context documents for AI
            
        Returns:
            AI-generated campaign plan or fallback to heuristic
        """
        try:
            from ..llm_openai import plan_with_openai
            
            # Prepare context
            system_prompt = "You are a revenue-obsessed liquor retail strategist."
            
            # Try AI planning
            ai_plan = plan_with_openai(
                system_prompt=system_prompt,
                user_prompt=objective,
                context_docs=context_docs or [],
                actions=actions
            )
            
            if ai_plan:
                ai_plan["engine"] = "llm"
                return ai_plan
            
        except ImportError:
            pass  # OpenAI not configured
        except Exception as e:
            print(f"AI planning failed: {e}")
        
        # Fallback to heuristic
        return CampaignPlanningService.generate_heuristic_plan(
            actions, start_date, duration_days
        )
    
    @staticmethod
    def analyze_plan_performance(plan: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the performance of an executed campaign plan.
        
        Args:
            plan: The original campaign plan
            results: Actual results from campaign execution
            
        Returns:
            Performance analysis dictionary
        """
        total_sends = len(plan.get("sends", []))
        
        # Extract results
        opens = results.get("opens", 0)
        clicks = results.get("clicks", 0)
        conversions = results.get("conversions", 0)
        revenue = results.get("revenue", 0)
        
        # Calculate metrics
        open_rate = (opens / total_sends * 100) if total_sends > 0 else 0
        click_rate = (clicks / opens * 100) if opens > 0 else 0
        conversion_rate = (conversions / total_sends * 100) if total_sends > 0 else 0
        aov = revenue / conversions if conversions > 0 else 0
        
        analysis = {
            "plan_id": plan.get("id"),
            "total_sends": total_sends,
            "metrics": {
                "opens": opens,
                "clicks": clicks,
                "conversions": conversions,
                "revenue": revenue,
            },
            "rates": {
                "open_rate": round(open_rate, 2),
                "click_rate": round(click_rate, 2),
                "conversion_rate": round(conversion_rate, 2),
            },
            "financial": {
                "total_revenue": revenue,
                "aov": round(aov, 2),
                "revenue_per_send": round(revenue / total_sends, 2) if total_sends > 0 else 0,
            },
            "kpis": plan.get("kpis", []),
            "performance_vs_target": {
                "win_back_rate": "TBD",  # Would need baseline
                "aov": f"${round(aov, 2)}",
                "conversion_rate": f"{round(conversion_rate, 2)}%",
            }
        }
        
        return analysis

