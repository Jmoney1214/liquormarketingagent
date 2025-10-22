"""Campaign management and AI planning endpoints"""
from datetime import date, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ...models.user import User
from ...api.deps import get_current_active_user
from ...services.campaign_planning import CampaignPlanningService
from ...services.customer_scoring import CustomerScoringService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...core.database import get_db
from ...models.customer import Customer

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


class GenerateCampaignRequest(BaseModel):
    """Request to generate AI campaign plan"""
    target_segments: List[str] = Field(..., min_items=1)
    start_date: Optional[str] = None  # ISO date format
    duration_days: int = Field(default=7, ge=1, le=30)
    objective: Optional[str] = "Build a 7-day plan to lift AOV and win back high-churn customers"
    use_ai: bool = True
    max_actions: int = Field(default=300, ge=1, le=1000)


class CampaignPlanResponse(BaseModel):
    """AI-generated campaign plan"""
    period: str
    rationale: str
    cohorts: List[str]
    kpis: List[str]
    sends: List[dict]
    engine: str  # "llm" or "heuristic"


@router.post("/generate", response_model=CampaignPlanResponse)
async def generate_campaign_plan(
    request: GenerateCampaignRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Generate an AI-powered campaign plan.
    
    This is the **AI ORCHESTRATOR BRAIN** that:
    1. Gets customers from selected segments
    2. Scores them using subagent logic
    3. Uses GPT-4 to create optimized 7-day plan
    4. Returns ready-to-execute campaign
    
    The magic happens here! 🧠✨
    """
    # Parse start date
    if request.start_date:
        start_dt = date.fromisoformat(request.start_date)
    else:
        start_dt = date.today()
    
    # Get customers from selected segments
    query = select(Customer).where(
        Customer.deleted_at.is_(None),
        Customer.rfm_segment.in_(request.target_segments)
    )
    
    result = await db.execute(query)
    customers_db = result.scalars().all()
    
    # Convert to dictionaries
    customers = [
        {
            "email": c.email,
            "name": c.name,
            "phone": c.phone,
            "rfm_segment": c.rfm_segment,
            "churn_risk": c.churn_risk,
            "success_rate_pct": float(c.success_rate_pct) if c.success_rate_pct else None,
            "is_night_buyer": c.is_night_buyer,
            "primary_category": c.primary_category,
            "total_spent": float(c.total_spent),
            "avg_order_value": float(c.avg_order_value),
        }
        for c in customers_db
    ]
    
    # Step 1: Generate actions using subagent (AI scoring)
    actions = CustomerScoringService.rank_and_generate_actions(
        customers=customers,
        limit=request.max_actions
    )
    
    # Step 2: Generate campaign plan
    if request.use_ai:
        # Use AI orchestrator (GPT-4)
        plan = await CampaignPlanningService.generate_ai_plan(
            actions=actions,
            start_date=start_dt,
            duration_days=request.duration_days,
            objective=request.objective
        )
    else:
        # Use heuristic planning
        plan = CampaignPlanningService.generate_heuristic_plan(
            actions=actions,
            start_date=start_dt,
            duration_days=request.duration_days
        )
    
    return CampaignPlanResponse(**plan)


@router.get("", response_model=List[dict])
async def list_campaigns(
    current_user: User = Depends(get_current_active_user),
):
    """List all campaigns (placeholder - will be implemented in Sprint 3)"""
    # Mock data for now
    return [
        {
            "id": "1",
            "name": "High Churn Win-back Campaign",
            "status": "active",
            "created_at": "2025-10-20T00:00:00Z"
        }
    ]

