from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

from tools._shared import ROOT, err, fold_text


ORDER_DIR = ROOT / "orders"
DATA_DIR = ROOT / "data" / "sales_data"
CUSTOMER_ID_PATTERN = re.compile(r"^CUS-\d{4}$")
SKU_PATTERN = re.compile(r"^SKU-\d{4}$")
WAREHOUSES = {"hcm", "hanoi", "danang", "online"}
MAX_QUANTITY = 50
MAX_NOTE_LENGTH = 500
# 13-19 digits, optionally grouped by spaces or dashes (payment card numbers).
CARD_NUMBER_PATTERN = re.compile(r"(?<!\d)\d(?:[ -]?\d){12,18}(?!\d)")
# Matched against accent-folded lowercase text, so "mật khẩu" becomes "mat khau".
SECRET_VALUE_PATTERN = re.compile(
    r"\b(?:cvv|cvc|otp|ma bao mat|so the)\b\s*(?:[:=]|\bla\b|\bis\b)?\s*\d{3,}"
    r"|\b(?:pin|password|passwd|mat khau)\b\s*(?:[:=]|\bla\b|\bis\b)\s*\S+",
)


def _load(name: str, key: str) -> list[dict[str, Any]]:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))[key]


def create_order(
    customer_id: str = "",
    sku: str = "",
    quantity: int = 1,
    warehouse: str = "",
    note: str = "",
    confirmed: bool = False,
) -> dict[str, Any]:
    for field, value in (("customer_id", customer_id), ("sku", sku), ("warehouse", warehouse), ("note", note)):
        if not isinstance(value, str):
            return {"tool": "create_order", "error": f"invalid_{field}_type"}
    if isinstance(quantity, bool) or not isinstance(quantity, (int, str)):
        return {"tool": "create_order", "error": "invalid_quantity_type"}
    if isinstance(quantity, str):
        if not quantity.strip().isdigit():
            return {"tool": "create_order", "error": "invalid_quantity_type"}
        quantity = int(quantity.strip())

    wanted_customer = customer_id.strip().upper()
    wanted_sku = sku.strip().upper()
    wanted_warehouse = warehouse.strip().lower()
    normalized_note = note.strip()

    missing = [name for name, value in (("customer_id", wanted_customer), ("sku", wanted_sku), ("warehouse", wanted_warehouse)) if not value]
    if missing:
        return {"tool": "create_order", "error": "missing_fields", "missing_fields": missing}
    if not CUSTOMER_ID_PATTERN.fullmatch(wanted_customer):
        return {"tool": "create_order", "error": "invalid_customer_id_format", "expected_format": "CUS-3001"}
    if not SKU_PATTERN.fullmatch(wanted_sku):
        return {"tool": "create_order", "error": "invalid_sku_format", "expected_format": "SKU-1001"}
    if wanted_warehouse not in WAREHOUSES:
        return {"tool": "create_order", "error": "invalid_warehouse", "available_warehouses": sorted(WAREHOUSES)}
    if quantity < 1 or quantity > MAX_QUANTITY:
        return {"tool": "create_order", "error": "invalid_quantity", "min": 1, "max": MAX_QUANTITY}
    if len(normalized_note) > MAX_NOTE_LENGTH:
        return {"tool": "create_order", "error": "note_too_long", "max_length": MAX_NOTE_LENGTH}
    if CARD_NUMBER_PATTERN.search(normalized_note) or SECRET_VALUE_PATTERN.search(fold_text(normalized_note)):
        return {
            "tool": "create_order",
            "error": "restricted_sensitive_data",
            "message": "Remove card numbers, CVV, OTP, PIN and passwords from the order note. Payment data is never stored in orders.",
        }

    try:
        customer = next((item for item in _load("customers.json", "customers") if item["customer_id"] == wanted_customer), None)
        if customer is None:
            return {"tool": "create_order", "customer_id": wanted_customer, "error": "customer_not_found"}
        if customer.get("account_status") != "active":
            return {"tool": "create_order", "customer_id": wanted_customer, "error": "customer_not_active", "account_status": customer.get("account_status")}
        product = next((item for item in _load("products.json", "products") if item["sku"] == wanted_sku), None)
        if product is None:
            return {"tool": "create_order", "sku": wanted_sku, "error": "sku_not_found"}
        stock = next(
            (item for item in _load("stock.json", "stock") if item["sku"] == wanted_sku and item["warehouse"] == wanted_warehouse),
            None,
        )
        available = stock["qty"] if stock else 0
        if available < quantity:
            return {
                "tool": "create_order",
                "sku": wanted_sku,
                "warehouse": wanted_warehouse,
                "error": "insufficient_stock",
                "requested_qty": quantity,
                "available_qty": available,
                "restock_date": stock["restock_date"] if stock else None,
            }

        pending_order = {
            "customer_id": wanted_customer,
            "sku": wanted_sku,
            "name": f"{product['brand']} {product['model']}",
            "quantity": quantity,
            "warehouse": wanted_warehouse,
            "unit_price": product["price"],
            "total": product["price"] * quantity,
            "note": normalized_note or None,
        }
        if confirmed is not True:
            return {
                "tool": "create_order",
                "status": "needs_confirmation",
                "pending_order": pending_order,
                "message": "Create the order only after the customer explicitly confirms this exact customer, SKU, quantity and warehouse.",
            }

        now = datetime.now(timezone.utc)
        seed = f"{now.isoformat()}|{wanted_customer}|{wanted_sku}|{quantity}|{wanted_warehouse}"
        order_id = "SO-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8].upper()
        payload = {
            "order_id": order_id,
            **pending_order,
            "status": "created",
            "created_at": now.isoformat(),
            "source": "educational_local_mock",
        }
        ORDER_DIR.mkdir(parents=True, exist_ok=True)
        path = ORDER_DIR / f"{order_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"tool": "create_order", "status": "created", "order_id": order_id, "order": pending_order, "path": str(path)}
    except Exception as exc:
        return err("create_order", exc)
