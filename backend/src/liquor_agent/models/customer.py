"""Customer model"""
from typing import Optional
from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped

from ..core.database import Base
from .base import TimestampMixin, UUIDMixin


class Customer(Base, UUIDMixin, TimestampMixin):
    """Customer model with segmentation and behavioral data"""
    __tablename__ = "customers"
    
    # Basic info
    email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[Optional[str]] = Column(String(20), nullable=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    
    # Segmentation
    rfm_segment: Mapped[Optional[str]] = Column(String(100), nullable=True, index=True)
    churn_risk: Mapped[Optional[str]] = Column(String(50), nullable=True, index=True)  # low, medium, high
    clv_score: Mapped[Optional[float]] = Column(Numeric(10, 2), nullable=True)
    
    # Behavioral traits
    is_night_buyer: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    avg_purchase_hour: Mapped[Optional[int]] = Column(Integer, nullable=True)
    purchase_frequency: Mapped[int] = Column(Integer, default=0, nullable=False)
    
    # Financial metrics
    total_spent: Mapped[float] = Column(Numeric(10, 2), default=0, nullable=False)
    avg_order_value: Mapped[float] = Column(Numeric(10, 2), default=0, nullable=False)
    success_rate_pct: Mapped[Optional[float]] = Column(Numeric(5, 2), nullable=True)
    
    # Product preferences
    primary_category: Mapped[Optional[str]] = Column(String(100), nullable=True, index=True)
    secondary_category: Mapped[Optional[str]] = Column(String(100), nullable=True)
    favorite_brands: Mapped[Optional[list]] = Column(JSONB, nullable=True)
    
    # Metadata
    raw_data: Mapped[Optional[dict]] = Column(JSONB, nullable=True)
    last_purchase_at: Mapped[Optional[DateTime]] = Column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[DateTime]] = Column(DateTime, nullable=True)  # Soft delete
    
    def __repr__(self) -> str:
        return f"<Customer {self.email}>"


