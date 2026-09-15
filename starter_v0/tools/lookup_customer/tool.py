from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err


CUSTOMER_FILE = ROOT / "sales_data" / "customers.json"


def lookup_customer(customer_id: str = "") -> dict[str, Any]:
    try:
        data = json.loads(CUSTOMER_FILE.read_text(encoding="utf-8"))
        wanted_id = (customer_id or "").strip().upper()
        customer = next((item for item in data["customers"] if item["customer_id"] == wanted_id), None)
        if customer is None:
            return {"tool": "lookup_customer", "customer_id": wanted_id, "error": "customer_not_found"}
        return {"tool": "lookup_customer", "customer": customer, "snapshot_at": data["snapshot_at"]}
    except Exception as exc:
        return err("lookup_customer", exc)
