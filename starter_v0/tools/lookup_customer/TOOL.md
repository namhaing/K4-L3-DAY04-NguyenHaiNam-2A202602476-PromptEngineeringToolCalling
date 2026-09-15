---
name: lookup_customer
track: core
kind: local_directory
provider: mock_customer_directory
requires_env: []
inputs: [customer_id]
outputs: [customer]
side_effect: false
---
# lookup_customer

Looks up one fictional customer by customer ID and returns their tier, city,
masked phone number, order IDs and account status. It never returns a full
phone number, address or payment data — `customers.json` only ever stores the
already-masked phone number.
