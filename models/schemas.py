"""
Data models for Inventory Intelligence System
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CustomerData(BaseModel):
    """Customer information from Tally"""
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    total_purchases: float = 0.0
    purchase_count: int = 0
    last_purchase_date: Optional[datetime] = None
    customer_segment: Optional[str] = None


class ProductData(BaseModel):
    """Product/Inventory information from Tally"""
    product_id: str
    name: str
    category: str
    sku: str
    current_stock: int
    unit_price: float
    cost_price: Optional[float] = None
    reorder_level: Optional[int] = None
    supplier: Optional[str] = None
    last_restock_date: Optional[datetime] = None


class Transaction(BaseModel):
    """Sales transaction data"""
    transaction_id: str
    date: datetime
    customer_id: str
    product_id: str
    quantity: int
    unit_price: float
    total_amount: float
    payment_method: Optional[str] = None


class Insight(BaseModel):
    """Generated insight"""
    insight_type: str  # 'alert', 'recommendation', 'forecast', 'pattern'
    title: str
    description: str
    priority: str = Field(default="medium")  # 'low', 'medium', 'high', 'critical'
    action_required: bool = False
    related_products: List[str] = Field(default_factory=list)
    related_customers: List[str] = Field(default_factory=list)
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)


class ForecastResult(BaseModel):
    """Demand forecast result"""
    product_id: str
    product_name: str
    current_stock: int
    forecast_period: str  # '7d', '30d', '90d'
    predicted_demand: float
    recommended_order_quantity: int
    confidence_interval: tuple[float, float]
    risk_level: str  # 'low', 'medium', 'high'
