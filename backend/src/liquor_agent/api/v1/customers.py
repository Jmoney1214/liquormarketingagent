"""Customer management endpoints"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from math import ceil

from ...core.database import get_db
from ...models.user import User
from ...models.customer import Customer
from ...schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerList
from ...schemas.common import PaginatedResponse
from ...api.deps import get_current_active_user

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=PaginatedResponse[CustomerList])
async def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    segment: Optional[str] = None,
    churn_risk: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List customers with pagination and filtering
    
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 50, max: 100)
    - **segment**: Filter by RFM segment
    - **churn_risk**: Filter by churn risk (low, medium, high)
    - **search**: Search by name or email
    """
    # Build query
    query = select(Customer).where(Customer.deleted_at.is_(None))
    
    # Apply filters
    if segment:
        query = query.where(Customer.rfm_segment == segment)
    if churn_risk:
        query = query.where(Customer.churn_risk == churn_risk)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Customer.name.ilike(search_pattern),
                Customer.email.ilike(search_pattern)
            )
        )
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    customers = result.scalars().all()
    
    return PaginatedResponse(
        items=[CustomerList.model_validate(c) for c in customers],
        total=total,
        page=page,
        limit=limit,
        pages=ceil(total / limit) if total > 0 else 0,
    )


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new customer"""
    # Check if customer with email already exists
    result = await db.execute(select(Customer).where(Customer.email == customer_data.email))
    existing = result.scalar_one_or_none()
    
    if existing and existing.deleted_at is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this email already exists",
        )
    
    # Create customer
    customer = Customer(**customer_data.model_dump())
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    
    return customer


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get customer by ID"""
    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.deleted_at.is_(None)
        )
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    
    return customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: UUID,
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update customer"""
    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.deleted_at.is_(None)
        )
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    
    # Update fields
    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)
    
    await db.commit()
    await db.refresh(customer)
    
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Soft delete customer"""
    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id,
            Customer.deleted_at.is_(None)
        )
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    
    # Soft delete
    from datetime import datetime
    customer.deleted_at = datetime.utcnow()
    await db.commit()
    
    return None

