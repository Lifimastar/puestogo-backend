from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime, timezone

class Merchant(SQLModel, table=True):
    __tablename__ = "merchants"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    rating: float = 0.0
    delivery_time_min: Optional[int] = None
    delivery_fee: float = 0.0
    is_open: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    merchant_id: uuid.UUID = Field(foreign_key="merchants.id")
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    merchant_id: uuid.UUID = Field(foreign_key="merchants.id")
    total: float
    status: str = "pending" # pending, confirmed, preparing, delivered
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(foreign_key="orders.id")
    product_id: uuid.UUID = Field(foreign_key="products.id")
    quantity: int
    price: float # Precio al momento de la compra