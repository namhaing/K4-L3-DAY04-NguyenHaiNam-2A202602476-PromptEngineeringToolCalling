---
name: check_stock
track: core
kind: local_status
provider: local_stock_snapshot
requires_env: []
inputs: [sku, warehouse]
outputs: [sku, name, warehouse, qty, status, restock_date, checked_at]
side_effect: false
---
# check_stock

Returns stock for one SKU in one warehouse from `data/sales_data/stock.json`
(`hcm|hanoi|danang|online`). `status` is `in_stock`, `low_stock`,
`out_of_stock` or `incoming`; `restock_date` is set when a shipment is expected.

Errors: `missing_sku`, `invalid_sku_format`, `sku_not_found`,
`missing_warehouse`, `invalid_warehouse` (with `available_warehouses`). One call
checks one SKU in one warehouse; compare warehouses with separate calls.
