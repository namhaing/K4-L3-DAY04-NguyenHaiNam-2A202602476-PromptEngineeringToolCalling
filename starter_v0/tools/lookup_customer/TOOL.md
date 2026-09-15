---
name: lookup_customer
track: core
kind: local_directory
provider: mock_customer_directory
requires_env: []
inputs: [customer_id]
outputs: [customer, snapshot_at, privacy_notice]
side_effect: false
---
# lookup_customer

Looks up one fictional customer by ID in `data/sales_data/customers.json` and
returns name, tier, city, masked phone, loyalty points, account status and
order IDs. It never returns full addresses, emails or payment data.

Errors: `missing_customer_id`, `invalid_customer_id_format`,
`customer_not_found`. Customer data is internal and must not be sent to web
search.
