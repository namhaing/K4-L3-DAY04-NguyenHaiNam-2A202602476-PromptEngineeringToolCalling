---
name: format_quote
track: core
kind: local_formatter
requires_env: []
inputs: [lines, template, title]
outputs: [markdown, line_count, total, currency]
side_effect: false
---
# format_quote

Formats quote lines that were already collected (`sku`, `name`, `quantity`,
`unit_price`) into markdown using `brief`, `detailed` or `invoice_draft`.
It computes line totals and the grand total only; it does not look up prices,
stock or customers and does not create orders. `invoice_draft` is a preview,
not an invoice.

Errors: `invalid_template`, `missing_lines`, `invalid_lines` (with per-line
problems).
