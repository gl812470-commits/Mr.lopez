"""
order_service.py
-----------------
Handles all order-related database operations via Supabase.
"""

from supabase_client import get_supabase
import inventory_service


def create_order(order_data: dict):
    supabase = get_supabase()

    # Try to update stock, but don't block the order if it fails
    try:
        inventory_service.update_stock(
            product_id=order_data["product_id"],
            condition=order_data["condition"],
            quantity_sold=order_data["quantity"],
        )
    except Exception as e:
        print(f"[INVENTORY WARNING] Stock update failed: {e}")

    # Always save the order
    response = supabase.table("orders").insert(order_data).execute()
    return response.data[0] if response.data else None


def get_all_orders() -> list:
    supabase = get_supabase()
    response = supabase.table("orders").select("*").order("created_at", desc=True).execute()
    return response.data or []


def get_order_by_id(order_id: str):
    supabase = get_supabase()
    response = supabase.table("orders").select("*").eq("id", order_id).single().execute()
    return response.data


def get_orders_by_email(email: str) -> list:
    supabase = get_supabase()
    response = supabase.table("orders").select("*").eq("customer_email", email).order("created_at", desc=True).execute()
    return response.data or []


def update_order_status(order_id: str, status: str) -> bool:
    supabase = get_supabase()
    supabase.table("orders").update({"status": status}).eq("id", order_id).execute()
    return True