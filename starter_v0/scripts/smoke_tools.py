"""Smoke tests for the sales assistant tools.

Run from starter_v0/:  python scripts/smoke_tools.py

1. Contract: every tool declared in artifacts/tools.yaml is registered in
   TOOL_FUNCTIONS and its function accepts every declared parameter with a
   default value (agent.py calls func(**args), so a missing default crashes).
2. Behaviour: deterministic input/expected-output checks per tool.
3. Cases: eval case files have the right counts, allowed failure types,
   declared tools/params/enums, no array-of-object expectations and IDs that
   exist in data/sales_data.

Exit code: 0 all PASS, 1 any FAIL, 2 no FAIL but some PENDING.
"""
from __future__ import annotations

import argparse
import importlib
import inspect
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import TOOL_FUNCTIONS, load_tool_declarations  # noqa: E402


SALES_TOOLS = [
    "clarify", "search_products", "check_stock", "get_order", "lookup_customer",
    "sales_policy", "format_quote", "create_order", "search_product_web",
]

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

    # ---- lookup_customer ----
    ("lookup_customer", "CUS-3005 is gold with ORD-2006",
     {"customer_id": "CUS-3005"},
     lambda r: r["customer"]["tier"] == "gold" and r["customer"]["order_ids"] == ["ORD-2006"]),
    ("lookup_customer", "CUS-3009 locked, phone masked",
     {"customer_id": "cus-3009"},
     lambda r: r["customer"]["account_status"] == "locked" and "xxx" in r["customer"]["phone_masked"]),
    ("lookup_customer", "unknown customer -> customer_not_found",
     {"customer_id": "CUS-3999"},
     lambda r: r.get("error") == "customer_not_found"),
    ("lookup_customer", "bad format -> invalid_customer_id_format",
     {"customer_id": "3001"},
     lambda r: r.get("error") == "invalid_customer_id_format"),

    # ---- sales_policy ----
    ("sales_policy", "shipping delay rules found",
     {"query": "giao trễ", "policy_area": "shipping"},
     lambda r: r["results"] and r["results"][0]["doc_id"] == "shipping-policy" and "trễ" in r["results"][0]["facts"]),
    ("sales_policy", "pricing injection moved to untrusted_text",
     {"query": "chiết khấu tối đa", "policy_area": "pricing_discount", "top_k": 5},
     lambda r: any(x["untrusted_text"] for x in r["results"]) and all("50%" not in x["facts"] for x in r["results"])),
    ("sales_policy", "area all routes card-data rule to payment",
     {"query": "số thẻ CVV OTP", "policy_area": "all"},
     lambda r: r["results"][0]["policy_area"] == "payment"),
    ("sales_policy", "invalid area -> invalid_policy_area",
     {"query": "đổi trả", "policy_area": "returns"},
     lambda r: r.get("error") == "invalid_policy_area"),

    # ---- format_quote ----
    ("format_quote", "detailed quote totals lines",
     {"lines": [{"sku": "SKU-1001", "name": "ThinkPad T14 Gen 4", "quantity": 2, "unit_price": 32990000},
                {"sku": "SKU-1008", "name": "Anker Nano II 65W", "quantity": 2, "unit_price": 890000}],
      "template": "detailed", "title": "Báo giá văn phòng"},
     lambda r: r["total"] == 67760000 and r["line_count"] == 2 and "| SKU-1001 |" in r["markdown"]),
    ("format_quote", "brief accepts '7.990.000' string price",
     {"lines": [{"name": "Sony WH-1000XM5", "quantity": 1, "unit_price": "7.990.000"}], "template": "brief"},
     lambda r: r["total"] == 7990000 and r["markdown"].startswith("**Báo giá**")),
    ("format_quote", "invoice_draft is marked as draft",
     {"lines": [{"sku": "SKU-1006", "name": "Redmi Note 13 Pro", "quantity": 1, "unit_price": 7490000}], "template": "invoice_draft", "title": "Đơn nháp"},
     lambda r: "không phải hóa đơn" in r["markdown"]),
    ("format_quote", "empty lines -> missing_lines",
     {"lines": [], "template": "brief"},
     lambda r: r.get("error") == "missing_lines"),
    ("format_quote", "negative price -> invalid_lines",
     {"lines": [{"name": "X", "quantity": 1, "unit_price": -5}], "template": "brief"},
     lambda r: r.get("error") == "invalid_lines"),

    # ---- search_product_web (offline checks only; no network call) ----
    ("search_product_web", "SKU/ORD/CUS in model -> restricted_internal_identifier",
     {"brand": "Samsung", "model": "Galaxy S24 ORD-2003 CUS-3001", "query_type": "reviews"},
     lambda r: r.get("error") == "restricted_internal_identifier"),
    ("search_product_web", "phone number in model -> restricted_internal_identifier",
     {"brand": "Sony", "model": "WH-1000XM5 0901234567", "query_type": "specs"},
     lambda r: r.get("error") == "restricted_internal_identifier"),
    ("search_product_web", "invalid query_type",
     {"brand": "Sony", "model": "WH-1000XM5", "query_type": "drivers"},
     lambda r: r.get("error") == "invalid_query_type"),
    ("search_product_web", "missing model -> missing_public_product_identity",
     {"brand": "Apple", "model": "", "query_type": "specs"},
     lambda r: r.get("error") == "missing_public_product_identity"),
]

_ORDER_DIR: Path | None = None


def _order_files() -> list[Path]:
    return sorted(_ORDER_DIR.glob("*.json")) if _ORDER_DIR and _ORDER_DIR.exists() else []


def check_contract(declarations: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    declared = {item["name"] for item in declarations}
    for name in SALES_TOOLS:
        if name not in declared:
            rows.append(("FAIL", name, "not declared in tools.yaml"))
    for item in declarations:
        name = item["name"]
        func = TOOL_FUNCTIONS.get(name)
        if func is None:
            rows.append(("PENDING", name, "declared but not registered in TOOL_FUNCTIONS"))
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
        for name in SALES_TOOLS:
            if name == "clarify" or (only and name not in only) or name in tested:
                continue
            rows.append(("PENDING", name, "no behaviour tests yet"))
    return rows


ALLOWED_FAILURE_TYPES = {"wrong_tool", "wrong_arg_value", "wrong_boundary", "unnecessary_tool", "out_of_scope", "missing_info"}
# dataset_role -> (single-turn count, multi-turn count); None means only the total is fixed.
EXPECTED_COUNTS = {"base": (20, 10), "adversarial": None, "group": (5, 5)}
EXPECTED_TOTALS = {"base": 30, "adversarial": 12, "group": 10}
ID_PATTERN = re.compile(r"\b(?:SKU|ORD|CUS)-\d{4}\b")


def _known_ids() -> set[str]:
    data_dir = ROOT / "data" / "sales_data"
    ids: set[str] = set()
    for name, key, field in (("products.json", "products", "sku"), ("orders.json", "orders", "order_id"), ("customers.json", "customers", "customer_id")):
        ids |= {item[field] for item in json.loads((data_dir / name).read_text(encoding="utf-8"))[key]}
    return ids


def check_cases(paths: list[Path], declarations: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    """Catch case-file mistakes that would crash run_eval or make a run invalid."""
    rows: list[tuple[str, str, str]] = []
    schemas = {item["name"]: item.get("parameters", {}).get("properties", {}) for item in declarations}
    known_ids = _known_ids()
    for path in paths:
        label = path.name
        if not path.exists():
            rows.append(("PENDING", label, "file not written yet"))
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rows.append(("FAIL", label, f"invalid JSON: {exc}"))
            continue
        cases = data.get("cases", [])
        role = data.get("dataset_role", "")
        problems: list[str] = []
        ids = [case.get("id") for case in cases]
        if len(ids) != len(set(ids)):
            problems.append("duplicate case ids")
        single = sum(1 for case in cases if "query" in case)
        multi = sum(1 for case in cases if "turns" in case)
        if role in EXPECTED_TOTALS and len(cases) != EXPECTED_TOTALS[role]:
            problems.append(f"{len(cases)} cases, expected {EXPECTED_TOTALS[role]}")
        if EXPECTED_COUNTS.get(role) and (single, multi) != EXPECTED_COUNTS[role]:
            problems.append(f"{single} single + {multi} multi, expected {EXPECTED_COUNTS[role][0]} + {EXPECTED_COUNTS[role][1]}")
        for case in cases:
            cid = case.get("id", "<no id>")
            if case.get("phase") != "B":
                problems.append(f"{cid}: phase must be 'B'")
            if case.get("failure_type") not in ALLOWED_FAILURE_TYPES:
                problems.append(f"{cid}: invalid failure_type {case.get('failure_type')!r}")
            if ("query" in case) == ("turns" in case):
                problems.append(f"{cid}: needs exactly one of query/turns")
            # run_eval folds earlier turns (user or assistant) into context; only the last turn is answered.
            if "turns" in case and (
                len(case["turns"]) < 2
                or any(turn.get("role") not in {"user", "assistant"} for turn in case["turns"])
                or case["turns"][-1].get("role") != "user"
            ):
                problems.append(f"{cid}: turns must be >= 2 user/assistant turns ending with a user turn")
            if not case.get("metadata", {}).get("what_it_tests"):
                problems.append(f"{cid}: missing metadata.what_it_tests")
            expect = case.get("expect", {})
            calls = expect.get("tool_calls", [])
            if bool(expect.get("no_tool")) == bool(calls):
                problems.append(f"{cid}: expect needs exactly one of no_tool / tool_calls")
            for call in calls:
                name = call.get("name")
                if name not in schemas:
                    problems.append(f"{cid}: {name!r} not declared in tools.yaml")
                    continue
                if name not in TOOL_FUNCTIONS:
                    problems.append(f"{cid}: {name!r} not registered")
                for key, value in call.get("args", {}).items():
                    prop = schemas[name].get(key)
                    if prop is None:
                        problems.append(f"{cid}: {name}.{key} is not a declared parameter")
                        continue
                    if isinstance(value, list) and any(isinstance(item, dict) for item in value):
                        problems.append(f"{cid}: {name}.{key} is an array of objects (crashes run_eval scoring)")
                    if "enum" in prop and str(value).lower() not in {str(option).lower() for option in prop["enum"]}:
                        problems.append(f"{cid}: {name}.{key}={value!r} not in enum")
                    for found in ID_PATTERN.findall(json.dumps(value)):
                        if found not in known_ids:
                            problems.append(f"{cid}: {found} in expect does not exist in sales_data")
        detail = f"{len(cases)} cases ({single} single + {multi} multi)"
        rows.append(("FAIL", label, detail + "; " + "; ".join(problems[:8])) if problems else ("PASS", label, detail))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test sales assistant tools and eval case files.")
    parser.add_argument("--tools", type=Path, default=ROOT / "artifacts" / "tools.yaml")
    parser.add_argument("--only", nargs="*", help="Only run behaviour tests for these tool names.")
    parser.add_argument(
        "--cases", nargs="*", type=Path,
        default=[ROOT / "data" / "sales_base.json", ROOT / "data" / "sales_adversarial.json"],
        help="Case files to validate (default: sales_base + sales_adversarial).",
    )
    args = parser.parse_args()

    declarations = load_tool_declarations(args.tools)
    rows = [("contract", *row) for row in check_contract(declarations)]
    rows += [("behaviour", *row) for row in run_tests(set(args.only) if args.only else None)]
    rows += [("cases", *row) for row in check_cases(args.cases, declarations)]
    for section, status, name, detail in rows:
        print(f"{status:<8} {section:<10} {name:<24} {detail}")

    counts = {status: sum(1 for row in rows if row[1] == status) for status in ("PASS", "FAIL", "PENDING")}
    print(f"\nPASS {counts['PASS']}  FAIL {counts['FAIL']}  PENDING {counts['PENDING']}")
    if counts["FAIL"]:
        return 1
    return 2 if counts["PENDING"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
