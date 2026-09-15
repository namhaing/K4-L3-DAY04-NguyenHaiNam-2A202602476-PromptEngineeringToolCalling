from __future__ import annotations

import json
import re
from typing import Any

from tools._shared import ROOT, err


ORDER_FILE = ROOT / "data" / "sales_data" / "orders.json"
ORDER_ID_PATTERN = re.compile(r"^ORD-\d{4}$")
VIEWS = {"all", "items", "payment", "shipping", "status"}


def get_order(order_id: str = "", view: str = "all") -> dict[str, Any]:
    try:
        wanted_id = str(order_id or "").strip().upper()
        wanted_view = str(view or "all").strip().lower()
        if not wanted_id:
            return {"tool": "get_order", "error": "missing_order_id"}
        if not ORDER_ID_PATTERN.fullmatch(wanted_id):
            return {"tool": "get_order", "order_id": wanted_id, "error": "invalid_order_id_format", "expected_format": "ORD-2001"}
        if wanted_view not in VIEWS:
            return {"tool": "get_order", "order_id": wanted_id, "view": wanted_view, "error": "invalid_view", "available_views": sorted(VIEWS)}

        data = json.loads(ORDER_FILE.read_text(encoding="utf-8"))
        order = next((item for item in data["orders"] if item["order_id"] == wanted_id), None)
        if order is None:
            return {"tool": "get_order", "order_id": wanted_id, "error": "order_not_found"}

        header = {"order_id": order["order_id"], "customer_id": order["customer_id"], "status": order["status"]}
        if wanted_view == "all":
            selected = order
        elif wanted_view == "items":
            selected = {**header, "items": order["items"], "total": order["total"], "issues": order["issues"]}
        elif wanted_view == "status":
            selected = {**header, "created_at": order["created_at"], "issues": order["issues"]}
        else:
            selected = {**header, wanted_view: order[wanted_view]}
        return {
            "tool": "get_order",
            "order_id": wanted_id,
            "view": wanted_view,
            "order": selected,
            "currency": data.get("currency", "VND"),
            "snapshot_at": data["snapshot_at"],
        }
    except Exception as exc:
        return err("get_order", exc)
