# Fictional Sales Data — Northstar Electronics

All records in this folder are synthetic and deterministic, captured at a fixed
snapshot (`2026-09-14T09:00:00+07:00`). They exist only for the lab and contain
no real customer, order or payment data.

- `products.json` (C): 12 mock products across laptop/phone/tablet/audio/wearable/accessory,
  including `SKU-1012` as a safe prompt-injection fixture in its description.
- `stock.json` (C): stock per SKU across 4 warehouses (`hcm`, `hanoi`, `danang`, `online`).
- `customers.json` (A): 10 mock customers with masked phone numbers only — no full
  address or card data. `CUS-3008` is `locked` to exercise account-status handling.
- `orders.json` (A): 8 mock orders covering normal flows plus contract fixtures:
  - `ORD-2004` — shipping delayed past its ETA.
  - `ORD-2005` — payment failed.
  - `ORD-2006` — partially shipped; `SKU-1008` line is backordered.
  - `ORD-2008` — delivered 20 days before the snapshot (used by the bonus
    return-eligibility check).
- `sales_policy/*.md` (D): sales policy articles, including one prompt-injection fixture.

Customer and order IDs follow `CUS-30xx` / `ORD-20xx` and are cross-referenced:
each customer's `order_ids` matches the `customer_id` on the corresponding order.
`get_order`, `lookup_customer` and any tool that reads this data must never send
customer IDs, order IDs, phone numbers or shipping city to `search_product_web`.

Students may extend this data when they build a new tool, but they must document
their contract and add eval cases for the behavior they introduce.
