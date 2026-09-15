from __future__ import annotations

import json
import re
from typing import Any

from tools._shared import ROOT, err


STOCK_FILE = ROOT / "data" / "sales_data" / "stock.json"
PRODUCT_FILE = ROOT / "data" / "sales_data" / "products.json"
SKU_PATTERN = re.compile(r"^SKU-\d{4}$")
WAREHOUSES = {"hcm", "hanoi", "danang", "online"}


def check_stock(sku: str = "", warehouse: str = "") -> dict[str, Any]:
    try:
        wanted_sku = str(sku or "").strip().upper()
        wanted_warehouse = str(warehouse or "").strip().lower()
        if not wanted_sku:
            return {"tool": "check_stock", "error": "missing_sku"}
        if not SKU_PATTERN.fullmatch(wanted_sku):
            return {"tool": "check_stock", "sku": wanted_sku, "error": "invalid_sku_format", "expected_format": "SKU-1001"}
        if not wanted_warehouse:
            return {"tool": "check_stock", "sku": wanted_sku, "error": "missing_warehouse", "available_warehouses": sorted(WAREHOUSES)}
        if wanted_warehouse not in WAREHOUSES:
            return {"tool": "check_stock", "sku": wanted_sku, "warehouse": wanted_warehouse, "error": "invalid_warehouse", "available_warehouses": sorted(WAREHOUSES)}

        products = json.loads(PRODUCT_FILE.read_text(encoding="utf-8"))["products"]
        product = next((item for item in products if item["sku"] == wanted_sku), None)
        if product is None:
            return {"tool": "check_stock", "sku": wanted_sku, "error": "sku_not_found"}

        data = json.loads(STOCK_FILE.read_text(encoding="utf-8"))
        row = next((item for item in data["stock"] if item["sku"] == wanted_sku and item["warehouse"] == wanted_warehouse), None)
        if row is None:
            return {"tool": "check_stock", "sku": wanted_sku, "warehouse": wanted_warehouse, "error": "stock_record_not_found"}
        warehouse_name = next((item["name"] for item in data["warehouses"] if item["warehouse"] == wanted_warehouse), wanted_warehouse)
        return {
            "tool": "check_stock",
            "sku": wanted_sku,
            "name": f"{product['brand']} {product['model']}",
            "warehouse": wanted_warehouse,
            "warehouse_name": warehouse_name,
            "qty": row["qty"],
            "status": row["status"],
            "restock_date": row["restock_date"],
            "checked_at": data["snapshot_at"],
        }
    except Exception as exc:
        return err("check_stock", exc)
