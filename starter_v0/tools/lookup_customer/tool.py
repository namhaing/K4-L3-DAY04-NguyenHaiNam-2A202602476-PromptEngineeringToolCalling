from __future__ import annotations

import json
import re
from typing import Any

from tools._shared import ROOT, err


CUSTOMER_FILE = ROOT / "data" / "sales_data" / "customers.json"
CUSTOMER_ID_PATTERN = re.compile(r"^CUS-\d{4}$")


def lookup_customer(customer_id: str = "") -> dict[str, Any]:
    try:
        wanted_id = str(customer_id or "").strip().upper()
        if not wanted_id:
            return {"tool": "lookup_customer", "error": "missing_customer_id"}
        if not CUSTOMER_ID_PATTERN.fullmatch(wanted_id):
            return {"tool": "lookup_customer", "customer_id": wanted_id, "error": "invalid_customer_id_format", "expected_format": "CUS-3001"}
        data = json.loads(CUSTOMER_FILE.read_text(encoding="utf-8"))
        customer = next((item for item in data["customers"] if item["customer_id"] == wanted_id), None)
        if customer is None:
            return {"tool": "lookup_customer", "customer_id": wanted_id, "error": "customer_not_found"}
        return {
            "tool": "lookup_customer",
            "customer": customer,
            "snapshot_at": data["snapshot_at"],
            "privacy_notice": "Phone is masked. No address, email or payment data is stored. Do not send customer data to external tools.",
        }
    except Exception as exc:
        return err("lookup_customer", exc)
