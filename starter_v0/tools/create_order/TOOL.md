---
name: create_order
track: core
kind: action
provider: local_order_store
requires_env: []
inputs: [customer_id, sku, quantity, warehouse, note, confirmed]
outputs: [status, order_id, order, pending_order, path]
side_effect: local_file_write
requires_confirmation: true
---
# create_order

Creates a local mock sales order for **one SKU** under `orders/`.

Checks, in order:

1. Types and formats (`CUS-xxxx`, `SKU-xxxx`, warehouse `hcm|hanoi|danang|online`,
   quantity 1–50, note ≤ 500 chars).
2. Rejects notes containing card numbers (13–19 digits), CVV/CVC, OTP, PIN or
   passwords with `restricted_sensitive_data`.
3. Customer exists and is `active`, SKU exists, warehouse has enough stock
   (`customer_not_found`, `customer_not_active`, `sku_not_found`,
   `insufficient_stock`).
4. If `confirmed` is not exactly `true`, returns `needs_confirmation` with the
   `pending_order` summary and **writes nothing**.
5. Otherwise writes `orders/SO-XXXXXXXX.json` and returns `created`.

Stock is not decremented; this is a lab mock. `orders/` is git-ignored.
