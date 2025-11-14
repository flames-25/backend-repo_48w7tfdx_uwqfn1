"""
Database Schemas for Tour Service

Each Pydantic model represents a MongoDB collection. The collection name
is the lowercase of the class name (e.g., Tour -> "tour").
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Core schemas for the Tour website

class Tour(BaseModel):
    title: str = Field(..., description="Tour package title")
    description: str = Field(..., description="Short description of the tour")
    price: float = Field(..., ge=0, description="Price per person in USD")
    duration_days: int = Field(..., ge=1, description="Tour duration in days")
    location: str = Field(..., description="Primary location / destination")
    image_url: Optional[str] = Field(None, description="Cover image URL")
    highlights: Optional[List[str]] = Field(default_factory=list, description="Key highlights of the tour")
    rating: Optional[float] = Field(4.8, ge=0, le=5, description="Average rating")

class Booking(BaseModel):
    tour_id: str = Field(..., description="ID of the tour being booked")
    full_name: str = Field(..., description="Customer full name")
    email: str = Field(..., description="Customer email")
    phone: Optional[str] = Field(None, description="Customer phone number")
    travel_date: str = Field(..., description="Planned travel date (ISO string)")
    guests: int = Field(..., ge=1, le=20, description="Number of guests")
    notes: Optional[str] = Field(None, description="Additional notes or requests")

class Inquiry(BaseModel):
    full_name: str = Field(..., description="Sender full name")
    email: str = Field(..., description="Sender email")
    message: str = Field(..., min_length=10, description="Message content")

# Example schemas retained for reference
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
