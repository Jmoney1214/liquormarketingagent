"""Common schemas used across the API"""
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int
    page: int
    limit: int
    pages: int
    
    class Config:
        from_attributes = True


