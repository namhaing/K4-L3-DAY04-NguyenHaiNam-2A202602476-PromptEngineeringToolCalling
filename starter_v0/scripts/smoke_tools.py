"""Smoke tests for the sales assistant tools.

Run from starter_v0/:  python scripts/smoke_tools.py

1. Contract: every tool declared in artifacts/tools.yaml is registered in
   TOOL_FUNCTIONS and its function accepts every declared parameter with a
   default value (agent.py calls func(**args), so a missing default crashes).
2. Behaviour: deterministic input/expected-output checks per tool.

Exit code: 0 all PASS, 1 any FAIL, 2 no FAIL but some PENDING.
"""
from __future__ import annotations

import argparse
import importlib
import inspect
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import TOOL_FUNCTIONS, load_tool_declarations  # noqa: E402


OWNERS = {
    "clarify": "starter",
    "search_products": "C",
    "check_stock": "C",
    "get_order": "C",
    "create_order": "C",
    "lookup_customer": "A",
    "sales_policy": "D",
    "format_quote": "D",
    "search_product_web": "D",
}

Check = Callable[[dict[str, Any]], bool]
TESTS: list[tuple[str, str, dict[str, Any], Check]] = [
    # ---- search_products (C) ----
    ("search_products", "tai nghe chong on -> audio SKU-1004/1010",
     {"query": "tai nghe chống ồn", "category": "audio"},
     lambda r: {x["sku"] for x in r["results"][:2]} == {"SKU-1004", "SKU-1010"}),
    ("search_products", "keyword across all categories finds ThinkPad",
     {"query": "ThinkPad T14", "category": "all"},
     lambda r: r["results"][0]["sku"] == "SKU-1001"),
    ("search_products", "category-only query lists that category",
     {"query": "sản phẩm tương tự", "category": "wearable", "top_k": 5},
     lambda r: r["results"] and all(x["category"] == "wearable" for x in r["results"])),
    ("search_products", "SKU-1012 injection line moved to untrusted_text",
     {"query": "loa bluetooth JBL", "category": "audio"},
     lambda r: any(x["sku"] == "SKU-1012" and x["untrusted_text"] and "SYSTEM" not in x["description"] for x in r["results"])),
    ("search_products", "invalid category -> invalid_category",
     {"query": "tv", "category": "television"},
     lambda r: r.get("error") == "invalid_category"),
    ("search_products", "top_k limits results",
     {"query": "laptop", "category": "laptop", "top_k": 1},
     lambda r: len(r["results"]) == 1),

    # ---- check_stock (C) ----
    ("check_stock", "SKU-1002 hcm in stock",
     {"sku": "SKU-1002", "warehouse": "hcm"},
     lambda r: r.get("qty") == 6 and r.get("status") == "in_stock"),
    ("check_stock", "SKU-1004 hanoi out of stock with restock date",
     {"sku": "SKU-1004", "warehouse": "hanoi"},
     lambda r: r.get("status") == "out_of_stock" and r.get("restock_date") == "2026-09-19"),
    ("check_stock", "lowercase / spaced input normalised",
     {"sku": " sku-1008 ", "warehouse": "ONLINE"},
     lambda r: r.get("sku") == "SKU-1008" and r.get("status") == "low_stock"),
    ("check_stock", "unknown warehouse -> invalid_warehouse",
     {"sku": "SKU-1002", "warehouse": "cantho"},
     lambda r: r.get("error") == "invalid_warehouse" and "online" in r.get("available_warehouses", [])),
    ("check_stock", "unknown SKU -> sku_not_found",
     {"sku": "SKU-1999", "warehouse": "hcm"},
     lambda r: r.get("error") == "sku_not_found"),
    ("check_stock", "bad SKU format -> invalid_sku_format",
     {"sku": "1002", "warehouse": "hcm"},
     lambda r: r.get("error") == "invalid_sku_format"),

    # ---- get_order (C) ----
    ("get_order", "ORD-2003 view all",
     {"order_id": "ORD-2003", "view": "all"},
     lambda r: r["order"]["customer_id"] == "CUS-3001" and "payment" in r["order"] and "shipping" in r["order"]),
    ("get_order", "ORD-2004 shipping view shows delay only",
     {"order_id": "ORD-2004", "view": "shipping"},
     lambda r: r["order"]["shipping"]["status"] == "delayed" and "payment" not in r["order"]),
    ("get_order", "ORD-2005 payment failed",
     {"order_id": "ORD-2005", "view": "payment"},
     lambda r: r["order"]["payment"]["status"] == "failed"),
    ("get_order", "ORD-2006 items show SKU-1008 undelivered",
     {"order_id": "ORD-2006", "view": "items"},
     lambda r: any(i["sku"] == "SKU-1008" and i["delivered_qty"] == 0 for i in r["order"]["items"])),
    ("get_order", "unknown order -> order_not_found",
     {"order_id": "ORD-2999"},
     lambda r: r.get("error") == "order_not_found"),
    ("get_order", "invalid view -> invalid_view",
     {"order_id": "ORD-2001", "view": "refund"},
     lambda r: r.get("error") == "invalid_view"),

    # ---- create_order (C) ----
    ("create_order", "valid payload without confirmation -> needs_confirmation, no file",
     {"customer_id": "CUS-3001", "sku": "SKU-1001", "quantity": 1, "warehouse": "hcm"},
     lambda r: r.get("status") == "needs_confirmation" and r["pending_order"]["total"] == 32990000 and not _order_files()),
    ("create_order", "confirmed='true' string is not confirmation",
     {"customer_id": "CUS-3001", "sku": "SKU-1001", "quantity": 1, "warehouse": "hcm", "confirmed": "true"},
     lambda r: r.get("status") == "needs_confirmation" and not _order_files()),
    ("create_order", "card number + CVV in note rejected even when confirmed",
     {"customer_id": "CUS-3002", "sku": "SKU-1003", "quantity": 1, "warehouse": "hcm",
      "note": "Thẻ 4111 1111 1111 1111 CVV 123", "confirmed": True},
     lambda r: r.get("error") == "restricted_sensitive_data" and not _order_files()),
    ("create_order", "OTP in note rejected",
     {"customer_id": "CUS-3002", "sku": "SKU-1003", "quantity": 1, "warehouse": "hcm",
      "note": "mã OTP: 482913", "confirmed": True},
     lambda r: r.get("error") == "restricted_sensitive_data"),
    ("create_order", "harmless note with phone-length number accepted",
     {"customer_id": "CUS-3002", "sku": "SKU-1003", "quantity": 1, "warehouse": "hcm",
      "note": "Giao giờ hành chính, pin 4000mAh đã kiểm tra"},
     lambda r: r.get("status") == "needs_confirmation"),
    ("create_order", "locked customer -> customer_not_active",
     {"customer_id": "CUS-3009", "sku": "SKU-1006", "quantity": 1, "warehouse": "hcm", "confirmed": True},
     lambda r: r.get("error") == "customer_not_active" and not _order_files()),
    ("create_order", "unknown customer -> customer_not_found",
     {"customer_id": "CUS-3999", "sku": "SKU-1006", "quantity": 1, "warehouse": "hcm", "confirmed": True},
     lambda r: r.get("error") == "customer_not_found"),
    ("create_order", "unknown SKU -> sku_not_found",
     {"customer_id": "CUS-3001", "sku": "SKU-1999", "quantity": 1, "warehouse": "hcm", "confirmed": True},
     lambda r: r.get("error") == "sku_not_found"),
    ("create_order", "not enough stock -> insufficient_stock",
     {"customer_id": "CUS-3001", "sku": "SKU-1001", "quantity": 5, "warehouse": "hanoi", "confirmed": True},
     lambda r: r.get("error") == "insufficient_stock" and r.get("available_qty") == 4),
    ("create_order", "missing warehouse -> missing_fields",
     {"customer_id": "CUS-3001", "sku": "SKU-1001", "quantity": 1},
     lambda r: r.get("error") == "missing_fields" and "warehouse" in r.get("missing_fields", [])),
    ("create_order", "confirmed=True writes exactly one order file",
     {"customer_id": "CUS-3002", "sku": "SKU-1003", "quantity": 2, "warehouse": "hcm", "confirmed": True},
     lambda r: r.get("status") == "created" and r["order_id"].startswith("SO-") and len(_order_files()) == 1),

    # ---- lookup_customer (A): add 2-3 tests when A sends inputs ----
    # ---- sales_policy, format_quote, search_product_web (D): add tests when D sends inputs ----
]

_ORDER_DIR: Path | None = None


def _order_files() -> list[Path]:
    return sorted(_ORDER_DIR.glob("*.json")) if _ORDER_DIR and _ORDER_DIR.exists() else []


def check_contract(declarations: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    declared = {item["name"] for item in declarations}
    for name in OWNERS:
        if name not in declared:
            rows.append(("FAIL", name, "not declared in tools.yaml"))
    for item in declarations:
        name = item["name"]
        owner = OWNERS.get(name, "?")
        func = TOOL_FUNCTIONS.get(name)
        if func is None:
            rows.append(("PENDING", name, f"declared but not registered in TOOL_FUNCTIONS (owner {owner})"))
            continue
        params = inspect.signature(func).parameters
        props = item.get("parameters", {}).get("properties", {})
        problems = [f"missing param {key!r}" for key in props if key not in params]
        problems += [
            f"param {key!r} has no default"
            for key, param in params.items()
            if key in props and param.default is inspect.Parameter.empty
        ]
        problems += [f"required {key!r} not a property" for key in item.get("parameters", {}).get("required", []) if key not in props]
        rows.append(("FAIL", name, "; ".join(problems)) if problems else ("PASS", name, "yaml matches signature"))
    return rows


def run_tests(only: set[str] | None) -> list[tuple[str, str, str]]:
    global _ORDER_DIR
    # tools/__init__.py binds the name `create_order` to the function, so fetch the module explicitly.
    create_order_module = importlib.import_module("tools.create_order.tool")

    rows: list[tuple[str, str, str]] = []
    with tempfile.TemporaryDirectory() as tmp:
        _ORDER_DIR = Path(tmp) / "orders"
        create_order_module.ORDER_DIR = _ORDER_DIR  # never write smoke orders into the repo
        tested = set()
        for name, desc, kwargs, check in TESTS:
            if only and name not in only:
                continue
            tested.add(name)
            func = TOOL_FUNCTIONS.get(name)
            if func is None:
                rows.append(("PENDING", name, f"{desc} (tool not registered)"))
                continue
            try:
                result = func(**kwargs)
                ok = bool(check(result))
                detail = desc if ok else f"{desc} -> got {result!r}"[:400]
            except Exception as exc:  # a crashing check is a failure, not a pass
                ok, detail = False, f"{desc} -> {type(exc).__name__}: {exc}"
            rows.append(("PASS" if ok else "FAIL", name, detail))
        for name, owner in OWNERS.items():
            if name == "clarify" or (only and name not in only) or name in tested:
                continue
            rows.append(("PENDING", name, f"no behaviour tests yet (owner {owner} to send inputs)"))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test sales assistant tools.")
    parser.add_argument("--tools", type=Path, default=ROOT / "artifacts" / "tools.yaml")
    parser.add_argument("--only", nargs="*", help="Only run behaviour tests for these tool names.")
    args = parser.parse_args()

    rows = [("contract", *row) for row in check_contract(load_tool_declarations(args.tools))]
    rows += [("behaviour", *row) for row in run_tests(set(args.only) if args.only else None)]
    for section, status, name, detail in rows:
        print(f"{status:<8} {section:<10} {name:<20} {detail}")

    counts = {status: sum(1 for row in rows if row[1] == status) for status in ("PASS", "FAIL", "PENDING")}
    print(f"\nPASS {counts['PASS']}  FAIL {counts['FAIL']}  PENDING {counts['PENDING']}")
    if counts["FAIL"]:
        return 1
    return 2 if counts["PENDING"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
