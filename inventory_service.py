"""
inventory_service.py
---------------------
Handles all inventory-related database operations via Supabase.
"""

from supabase_client import get_supabase
from models import Inventory


def get_all_inventory() -> list[dict]:
    """Return inventory records for all products."""
    supabase = get_supabase()
    response = supabase.table("inventory").select("*").execute()
    return response.data or []


def get_inventory_by_product(product_id: str) -> dict | None:
    """Return inventory for a specific product."""
    supabase = get_supabase()
    response = (
        supabase.table("inventory")
        .select("*")
        .eq("product_id", product_id)
        .single()
        .execute()
    )
    return response.data


def update_stock(product_id: str, condition: str, quantity_sold: int) -> bool:
    """
    Decrease stock after a successful order.
    condition: 'original' or 'second_hand'
    Returns True if successful.
    """
    supabase = get_supabase()
    inv = get_inventory_by_product(product_id)
    if not inv:
        return False

    field_name = "stock_original" if condition == "original" else "stock_secondhand"
    new_stock = inv[field_name] - quantity_sold

    if new_stock < 0:
        return False  # Not enough stock

    supabase.table("inventory").update(
        {field_name: new_stock}
    ).eq("product_id", product_id).execute()

    # Also sync products table
    supabase.table("products").update(
        {field_name: new_stock}
    ).eq("id", product_id).execute()

    return True


def restock(product_id: str, condition: str, quantity: int) -> bool:
    """Add stock for a product."""
    supabase = get_supabase()
    inv = get_inventory_by_product(product_id)

    field_name = "stock_original" if condition == "original" else "stock_secondhand"

    if inv:
        new_stock = inv[field_name] + quantity
        supabase.table("inventory").update(
            {field_name: new_stock}
        ).eq("product_id", product_id).execute()
    else:
        data = {
            "product_id": product_id,
            field_name: quantity,
        }
        supabase.table("inventory").insert(data).execute()

    return True