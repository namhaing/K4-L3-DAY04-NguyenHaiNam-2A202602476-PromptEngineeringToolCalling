from __future__ import annotations

from typing import Any


TEMPLATES = {"brief", "detailed", "invoice_draft"}
VAT_NOTE = "Giá đã gồm VAT."


def _vnd(amount: float) -> str:
    return f"{int(round(amount)):,}".replace(",", ".") + " VND"


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.strip().replace(".", "").replace(",", "").replace("VND", "").replace("đ", "").strip()
        if cleaned.isdigit():
            return float(cleaned)
    return None


def format_quote(
    lines: list[dict[str, Any]] | None = None,
    template: str = "brief",
    title: str = "Báo giá",
) -> dict[str, Any]:
    wanted_template = str(template or "brief").strip().lower()
    if wanted_template not in TEMPLATES:
        return {"tool": "format_quote", "error": "invalid_template", "available_templates": sorted(TEMPLATES)}
    if not isinstance(lines, list) or not lines:
        return {"tool": "format_quote", "error": "missing_lines", "message": "Pass the quote lines already collected; this tool does not look up prices or stock."}

    rows: list[dict[str, Any]] = []
    problems: list[str] = []
    for index, item in enumerate(lines, start=1):
        if not isinstance(item, dict):
            problems.append(f"line {index}: not an object")
            continue
        quantity = _number(item.get("quantity", 1))
        unit_price = _number(item.get("unit_price"))
        if quantity is None or quantity <= 0:
            problems.append(f"line {index}: invalid quantity")
            continue
        if unit_price is None or unit_price < 0:
            problems.append(f"line {index}: invalid unit_price")
            continue
        rows.append({
            "sku": str(item.get("sku") or "").strip().upper() or None,
            "name": str(item.get("name") or item.get("sku") or f"Dòng {index}").strip(),
            "quantity": int(quantity),
            "unit_price": unit_price,
            "line_total": unit_price * int(quantity),
        })
    if problems:
        return {"tool": "format_quote", "error": "invalid_lines", "problems": problems}

    total = sum(row["line_total"] for row in rows)
    heading = str(title or "Báo giá").strip()
    if wanted_template == "brief":
        body = [f"**{heading}**", *[f"- {row['name']} × {row['quantity']}: {_vnd(row['line_total'])}" for row in rows], f"**Tổng: {_vnd(total)}**"]
    else:
        table = [
            "| SKU | Sản phẩm | SL | Đơn giá | Thành tiền |",
            "|---|---|---:|---:|---:|",
            *[f"| {row['sku'] or '-'} | {row['name']} | {row['quantity']} | {_vnd(row['unit_price'])} | {_vnd(row['line_total'])} |" for row in rows],
        ]
        if wanted_template == "detailed":
            body = [f"# {heading}", "", *table, "", f"**Tổng cộng: {_vnd(total)}**", "", f"- {VAT_NOTE}", "- Giá tham khảo theo catalog tại thời điểm báo giá; tồn kho cần kiểm tra lại khi tạo đơn."]
        else:
            body = [f"# HÓA ĐƠN NHÁP — {heading}", "", "_Bản nháp để khách xem trước, không phải hóa đơn hay xác nhận đơn hàng._", "", *table, "", f"**Tổng thanh toán: {_vnd(total)}**", f"- {VAT_NOTE}"]
    return {
        "tool": "format_quote",
        "template": wanted_template,
        "title": heading,
        "markdown": "\n".join(body),
        "line_count": len(rows),
        "total": total,
        "currency": "VND",
    }
