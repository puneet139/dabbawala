from enum import Enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class OrderStatus(str, Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    customer_address: str
    items: str
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(SQLModel):
    customer_name: str
    customer_address: str
    items: str

class OrderUpdate(SQLModel):
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    items: Optional[str] = None
    status: Optional[OrderStatus] = None


class OrderStatusLog(SQLModel):
    order_id: int
    previous_status: OrderStatus
    new_status: OrderStatus
    changed_at: datetime = Field(default_factory=datetime.utcnow)