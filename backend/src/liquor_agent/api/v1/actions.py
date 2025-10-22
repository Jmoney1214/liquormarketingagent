"""Action generation endpoints - AI Brain"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field

from ...core.database import get_db
from ...models.user import User
from ...models.customer import Customer
from ...api.deps import get_current_active_user
from ...services.customer_scoring import CustomerScoringService

router = APIRouter(prefix="/actions", tags=["actions"])


class GenerateActionsRequest(BaseModel):
    """Request to generate customer actions"""
    segments: Optional[List[str]] = None
    churn_risk: Optional[str] = None
    limit: int = Field(default=300, ge=1, le=1000)


class ActionResponse(BaseModel):
    """Individual action response"""
    email: str
    name: str
    segment: str
    primary_category: str
    offer: str
    send_window: List[str]
    channel: List[str]
    creative_hint: str
    reason: str
    priority_score: float


class GenerateActionsResponse(BaseModel):
    """Response from action generation"""
    generated_at: str
    actions_count: int
    actions: List[ActionResponse]


@router.post("/generate", response_model=GenerateActionsResponse)
async def generate_actions(
    request: GenerateActionsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Generate prioritized customer actions using AI scoring.
    
    This uses the **subagent brain** to:
    1. Score customers based on churn risk, behavior, value
    2. Rank by priority
    3. Generate personalized offers
    4. Return top N actions
    
    This is the first step in AI campaign creation!
    """
    # Build query for customers
    query = select(Customer).where(Customer.deleted_at.is_(None))
    
    # Apply filters
    if request.segments:
        query = query.where(Customer.rfm_segment.in_(request.segments))
    if request.churn_risk:
        query = query.where(Customer.churn_risk == request.churn_risk)
    
    # Get customers
    result = await db.execute(query)
    customers_db = result.scalars().all()
    
    # Convert to dictionaries for scoring service
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
    
    # Use AI scoring service to generate actions
    actions = CustomerScoringService.rank_and_generate_actions(
        customers=customers,
        limit=request.limit
    )
    
    return GenerateActionsResponse(
        generated_at=datetime.utcnow().isoformat() + "Z",
        actions_count=len(actions),
        actions=[ActionResponse(**action) for action in actions]
    )

