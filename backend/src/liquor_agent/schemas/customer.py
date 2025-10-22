"""Customer schemas"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal


class CustomerBase(BaseModel):
    """Base customer schema"""
    email: EmailStr
    phone: Optional[str] = None
    name: str
    
    # Segmentation
    rfm_segment: Optional[str] = None
    churn_risk: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    clv_score: Optional[Decimal] = None
    
    # Behavioral
    is_night_buyer: bool = False
    avg_purchase_hour: Optional[int] = Field(None, ge=0, le=23)
    purchase_frequency: int = 0
    
    # Financial
    total_spent: Decimal = Decimal("0.00")
    avg_order_value: Decimal = Decimal("0.00")
    success_rate_pct: Optional[Decimal] = None
    
    # Product preferences
    primary_category: Optional[str] = None
    secondary_category: Optional[str] = None
    favorite_brands: Optional[List[str]] = None


class CustomerCreate(CustomerBase):
    """Schema for customer creation"""
    raw_data: Optional[Dict[str, Any]] = None


class CustomerUpdate(BaseModel):
    """Schema for customer update (all fields optional)"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    rfm_segment: Optional[str] = None
    churn_risk: Optional[str] = None
    clv_score: Optional[Decimal] = None
    is_night_buyer: Optional[bool] = None
    avg_purchase_hour: Optional[int] = None
    purchase_frequency: Optional[int] = None
    total_spent: Optional[Decimal] = None
    avg_order_value: Optional[Decimal] = None
    success_rate_pct: Optional[Decimal] = None
    primary_category: Optional[str] = None
    secondary_category: Optional[str] = None
    favorite_brands: Optional[List[str]] = None
    raw_data: Optional[Dict[str, Any]] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response"""
    id: UUID
    last_purchase_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerList(BaseModel):
    """Schema for customer list item (minimal fields)"""
    id: UUID
    email: EmailStr
    name: str
    rfm_segment: Optional[str] = None
    churn_risk: Optional[str] = None
    total_spent: Decimal
    clv_score: Optional[Decimal] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

