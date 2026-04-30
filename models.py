"""
models.py
---------
Data models / schema definitions for the Briefs Shop.

These dataclasses mirror the tables you will create in Supabase.
They are used throughout the app for type clarity and easy serialisation.

Supabase SQL to create the tables:
------------------------------------

CREATE TABLE products (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    brand       TEXT NOT NULL,
    description TEXT,
    image_file  TEXT,
    original_price    NUMERIC(10,2) NOT NULL,
    secondhand_price  NUMERIC(10,2) NOT NULL,
    stock_original    INT DEFAULT 0,
    stock_secondhand  INT DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE orders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id      UUID REFERENCES products(id),
    product_name    TEXT NOT NULL,
    quantity        INT NOT NULL,
    condition       TEXT CHECK (condition IN ('original','second_hand')) NOT NULL,
    payment_method  TEXT CHECK (payment_method IN ('cash','gcash','credit_card','bank_transfer')) NOT NULL,
    unit_price      NUMERIC(10,2) NOT NULL,
    total_price     NUMERIC(10,2) NOT NULL,
    customer_name   TEXT,
    customer_email  TEXT,
    status          TEXT DEFAULT 'pending',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE inventory (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id      UUID REFERENCES products(id) UNIQUE,
    stock_original    INT DEFAULT 0,
    stock_secondhand  INT DEFAULT 0,
    last_updated    TIMESTAMPTZ DEFAULT NOW()
);
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Product:
    id: Optional[str] = None
    name: str = ""
    brand: str = ""
    description: str = ""
    image_file: str = ""
    original_price: float = 0.0
    secondhand_price: float = 0.0
    stock_original: int = 0
    stock_secondhand: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "description": self.description,
            "image_file": self.image_file,
            "original_price": self.original_price,
            "secondhand_price": self.secondhand_price,
            "stock_original": self.stock_original,
            "stock_secondhand": self.stock_secondhand,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            brand=data.get("brand", ""),
            description=data.get("description", ""),
            image_file=data.get("image_file", ""),
            original_price=float(data.get("original_price", 0)),
            secondhand_price=float(data.get("secondhand_price", 0)),
            stock_original=int(data.get("stock_original", 0)),
            stock_secondhand=int(data.get("stock_secondhand", 0)),
        )


@dataclass
class Order:
    id: Optional[str] = None
    product_id: Optional[str] = None
    product_name: str = ""
    quantity: int = 1
    condition: str = "original"          # "original" | "second_hand"
    payment_method: str = "cash"         # "cash" | "gcash" | "credit_card" | "bank_transfer"
    unit_price: float = 0.0
    total_price: float = 0.0
    customer_name: str = ""
    customer_email: str = ""
    status: str = "pending"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "condition": self.condition,
            "payment_method": self.payment_method,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "status": self.status,
        }


@dataclass
class Inventory:
    id: Optional[str] = None
    product_id: Optional[str] = None
    stock_original: int = 0
    stock_secondhand: int = 0

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "stock_original": self.stock_original,
            "stock_secondhand": self.stock_secondhand,
        }