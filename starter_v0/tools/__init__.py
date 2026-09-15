from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .clarify.tool import ask_user
from .check_service_status.tool import check_service_status
from .create_ticket.tool import create_ticket
from .format_incident_report.tool import format_incident_report
from .inspect_device.tool import inspect_device
from .lookup_user.tool import lookup_user
from .policy.tool import search_company_policy
from .search_kb.tool import search_kb
from .search_device_info.tool import search_device_info

# Sales assistant tools (Northstar Electronics). Import a tool only after its
# folder exists; a missing module breaks every entry point.
from .check_return_eligibility.tool import check_return_eligibility
from .check_stock.tool import check_stock
from .create_order.tool import create_order
from .format_quote.tool import format_quote
from .get_order.tool import get_order
from .lookup_customer.tool import lookup_customer
from .sales_policy.tool import search_sales_policy
from .search_product_web.tool import search_product_web
from .search_products.tool import search_products


# These names are part of the fixed evaluation contract. Keep built-in names
# unchanged in tools.yaml, this registry and the supplied datasets. Improve
# descriptions and compatible schemas. Register any team-built bonus tool in
# this registry and tools.yaml, then test it with team-authored cases.
TOOL_FUNCTIONS = {
    "clarify": ask_user,
    "search_kb": search_kb,
    "search_device_info": search_device_info,
    "check_service_status": check_service_status,
    "inspect_device": inspect_device,
    "lookup_user": lookup_user,
    "format_incident_report": format_incident_report,
    "policy": search_company_policy,
    "create_ticket": create_ticket,
    # Sales assistant tools.
    "search_products": search_products,
    "check_stock": check_stock,
    "get_order": get_order,
    "lookup_customer": lookup_customer,
    "sales_policy": search_sales_policy,
    "format_quote": format_quote,
    "create_order": create_order,
    "search_product_web": search_product_web,
    # Bonus (outside the locked core flow): read-only return eligibility check.
    "check_return_eligibility": check_return_eligibility,
}


def load_tool_declarations(path: Path) -> list[dict[str, Any]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["tools"]


def to_openai_tools(declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "type": "function",
        "function": {
            "name": item["name"],
            "description": item.get("description", ""),
            "parameters": item.get("parameters", {"type": "object", "properties": {}}),
        },
    } for item in declarations]
