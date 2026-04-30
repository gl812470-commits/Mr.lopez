"""
payment_service.py
-------------------
Handles payment method validation and processing logic.
In a real app this would integrate with a payment gateway (e.g. PayMongo for PH).
"""


PAYMENT_METHODS = {
    "cash":           "Cash on Delivery",
    "gcash":          "GCash",
    "credit_card":    "Credit / Debit Card",
    "bank_transfer":  "Bank Transfer",
}


def get_payment_methods() -> dict:
    """Return available payment methods as a dict {key: label}."""
    return PAYMENT_METHODS


def validate_payment_method(method: str) -> bool:
    """Check if the submitted payment method is valid."""
    return method in PAYMENT_METHODS


def calculate_total(unit_price: float, quantity: int) -> float:
    """Return total price."""
    return round(unit_price * quantity, 2)


def process_payment(order_data: dict) -> dict:
    """
    Simulate payment processing.
    In production: integrate PayMongo or another PH payment gateway here.

    Returns a result dict with keys:
        success (bool), message (str), transaction_ref (str|None)
    """
    method = order_data.get("payment_method", "")
    if not validate_payment_method(method):
        return {"success": False, "message": "Invalid payment method.", "transaction_ref": None}

    # --- Placeholder logic ---
    # Replace this block with actual gateway API calls.
    if method == "cash":
        return {
            "success": True,
            "message": "Order placed! Pay upon delivery.",
            "transaction_ref": None,
        }

    # For digital methods pretend it always succeeds (demo only)
    import uuid
    ref = str(uuid.uuid4())[:8].upper()
    return {
        "success": True,
        "message": f"Payment received via {PAYMENT_METHODS[method]}. Ref: {ref}",
        "transaction_ref": ref,
    }