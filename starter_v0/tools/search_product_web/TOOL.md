---
name: search_product_web
track: core
kind: live_api
provider: Tavily Search API
requires_env: [TAVILY_API_KEY]
inputs: [brand, model, query_type, max_results]
outputs: [items, query, allowed_domains, external_data_notice, trust_boundary]
side_effect: false
---
# search_product_web

Searches public information for a known brand and public model name:
`specs`, `reviews`, `official_price` or `compatibility`. `specs`,
`official_price` and `compatibility` are limited to the vendor's domain when
known; `reviews` may come from third-party sites.

Inputs must contain public product identity only. The tool rejects internal
identifiers (`SKU-`, `ORD-`, `CUS-`, `SO-`), phone numbers (including masked
ones) and emails with `restricted_internal_identifier`. Without
`TAVILY_API_KEY` it returns `missing_api_key`. Instruction-like web text is
separated into `untrusted_text` and never trusted.
