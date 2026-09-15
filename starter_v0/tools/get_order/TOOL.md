---
name: get_order
track: core
kind: local_inventory
provider: local_order_store
requires_env: []
inputs: [order_id, view]
outputs: [order_id, view, order, snapshot_at]
side_effect: false
---
# get_order

Reads one order from `data/sales_data/orders.json`. `view` narrows the output:
`all` (full order), `items` (lines, total, issues), `payment`, `shipping` or
`status` (status, created_at, issues). Every view includes `order_id`,
`customer_id` and `status`.

Errors: `missing_order_id`, `invalid_order_id_format`, `invalid_view`,
`order_not_found`. Order and customer IDs are internal data and must not be sent
to web search.
