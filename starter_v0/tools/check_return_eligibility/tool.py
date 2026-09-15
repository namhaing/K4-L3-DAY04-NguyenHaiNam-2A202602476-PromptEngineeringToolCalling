from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any

from tools._shared import ROOT, err


DATA_DIR = ROOT / "data" / "sales_data"
POLICY_FILE = ROOT / "data" / "returns_policy" / "returns-policy.md"
ORDER_ID_PATTERN = re.compile(r"^ORD-\d{4}$")
SKU_PATTERN = re.compile(r"^SKU-\d{4}$")
# Mirrors data/returns_policy/returns-policy.md.
WINDOW_DAYS = {"defective": 30, "wrong_item": 30, "changed_mind": 7}
OPENED_CHANGED_MIND_FEE_PERCENT = 10


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip().lower() in {"true", "false"}:
        return value.strip().lower() == "true"
    return None


def check_return_eligibility(
    order_id: str = "",
    sku: str = "",
    reason: str = "",
    opened: bool = False,
) -> dict[str, Any]:
    wanted_order = str(order_id or "").strip().upper()
    wanted_sku = str(sku or "").strip().upper()
    wanted_reason = str(reason or "").strip().lower()
    opened_flag = _as_bool(opened)

    missing = [name for name, value in (("order_id", wanted_order), ("sku", wanted_sku), ("reason", wanted_reason)) if not value]
    if missing:
        return {"tool": "check_return_eligibility", "error": "missing_fields", "missing_fields": missing}
    if not ORDER_ID_PATTERN.fullmatch(wanted_order):
        return {"tool": "check_return_eligibility", "error": "invalid_order_id_format", "expected_format": "ORD- kèm 4 chữ số"}
    if not SKU_PATTERN.fullmatch(wanted_sku):
        return {"tool": "check_return_eligibility", "error": "invalid_sku_format", "expected_format": "SKU- kèm 4 chữ số"}
    if wanted_reason not in WINDOW_DAYS:
        return {"tool": "check_return_eligibility", "error": "invalid_reason", "available_reasons": sorted(WINDOW_DAYS)}
    if opened_flag is None:
        return {"tool": "check_return_eligibility", "error": "invalid_opened_type"}

    try:
        orders_data = json.loads((DATA_DIR / "orders.json").read_text(encoding="utf-8"))
        products = {item["sku"]: item for item in json.loads((DATA_DIR / "products.json").read_text(encoding="utf-8"))["products"]}
        order = next((item for item in orders_data["orders"] if item["order_id"] == wanted_order), None)
        if order is None:
            return {"tool": "check_return_eligibility", "order_id": wanted_order, "error": "order_not_found"}
        line = next((item for item in order["items"] if item["sku"] == wanted_sku), None)
        if line is None:
            return {
                "tool": "check_return_eligibility",
                "order_id": wanted_order,
                "sku": wanted_sku,
                "error": "sku_not_in_order",
                "order_skus": [item["sku"] for item in order["items"]],
            }

        base = {
            "tool": "check_return_eligibility",
            "order_id": wanted_order,
            "sku": wanted_sku,
            "product": line["name"],
            "reason": wanted_reason,
            "opened": opened_flag,
            "policy_ref": f"{POLICY_FILE.relative_to(ROOT).as_posix()}",
            "checked_at": orders_data["snapshot_at"],
        }
        delivered_at = order["shipping"].get("delivered_at")
        if not delivered_at or line.get("delivered_qty", 0) < 1:
            return {
                **base,
                "eligible": False,
                "failed_conditions": ["order_not_delivered" if not delivered_at else "item_not_delivered"],
                "next_step": "Sản phẩm chưa được giao nên chưa áp dụng đổi trả; kiểm tra giao hàng theo chính sách vận chuyển.",
            }

        snapshot = datetime.fromisoformat(orders_data["snapshot_at"])
        days_since_delivery = (snapshot - datetime.fromisoformat(delivered_at)).days
        return_class = products.get(wanted_sku, {}).get("return_class", "standard")
        window = WINDOW_DAYS[wanted_reason]
        failed: list[str] = []
        fee_percent = 0
        if days_since_delivery > window:
            failed.append("return_window_expired")
        if wanted_reason == "changed_mind" and opened_flag:
            if return_class == "sealed_only":
                failed.append("sealed_only_opened")
            else:
                fee_percent = OPENED_CHANGED_MIND_FEE_PERCENT
        eligible = not failed
        return {
            **base,
            "return_class": return_class,
            "delivered_at": delivered_at,
            "days_since_delivery": days_since_delivery,
            "window_days": window,
            "eligible": eligible,
            "failed_conditions": failed,
            "fee_percent": fee_percent if eligible else 0,
            "next_step": (
                "Đủ điều kiện: hướng dẫn khách mang sản phẩm và phụ kiện tới cửa hàng; công cụ này không tạo phiếu đổi trả."
                if eligible else
                "Không đủ điều kiện đổi trả theo chính sách; có thể hướng dẫn bảo hành nếu là lỗi kỹ thuật."
            ),
        }
    except Exception as exc:
        return err("check_return_eligibility", exc)
