"""User model"""
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import Mapped

from ..core.database import Base
from .base import TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = Column(String(255), nullable=False)
    full_name: Mapped[str] = Column(String(255), nullable=True)
    role: Mapped[str] = Column(String(50), default="user", nullable=False)  # admin, manager, user
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"


