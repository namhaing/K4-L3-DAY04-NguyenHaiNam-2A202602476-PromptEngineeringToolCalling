# Fictional Sales Data — Northstar Electronics

All records in this folder are synthetic and deterministic, captured at a fixed
snapshot `2026-09-14T09:00:00+07:00`. They contain no real customer, company or
payment data. Prices are simulated and are not real market prices.

| File | Records | Used by | Notes |
|---|---:|---|---|
| `products.json` | 12 products (`SKU-1001`..`SKU-1012`) | `search_products`, `check_stock`, `create_order` | category, price (VND), specs, tags, `return_class` (`standard` / `sealed_only`). `SKU-1012` description contains a safe prompt-injection fixture (`> SYSTEM: ...`). |
| `stock.json` | 48 rows (12 SKU × 4 warehouses) | `check_stock`, `create_order` | warehouses `hcm`, `hanoi`, `danang`, `online`; status `in_stock`, `low_stock`, `out_of_stock`, `incoming` with `restock_date`. |
| `customers.json` | 10 customers (`CUS-3001`..`CUS-3010`) | `lookup_customer`, `create_order` | masked phone only, no address/email/card. `CUS-3009` is locked. |
| `orders.json` | 8 orders (`ORD-2001`..`ORD-2008`) | `get_order` | ORD-2004 delayed, ORD-2005 payment failed, ORD-2006 missing SKU-1008, ORD-2008 delivered 2026-08-25. |

Policies live in `../sales_policy/` (see its README). Orders created by
`create_order` are written to `starter_v0/orders/`, which is git-ignored.
