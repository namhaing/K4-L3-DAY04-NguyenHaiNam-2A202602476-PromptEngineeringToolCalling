# Fictional Sales Policy Handbook

Synthetic internal sales policies for the fictional retailer Northstar
Electronics. The model reads them only through
`sales_policy(query, policy_area, top_k)`.

Policy areas: `pricing_discount`, `payment`, `shipping`, `warranty`,
`order_processing`, `data_privacy`, `external_tools`.

| File | policy_area |
|---|---|
| `pricing-discount-policy.md` | pricing_discount (contains one safe prompt-injection fixture) |
| `payment-policy.md` | payment |
| `shipping-policy.md` | shipping |
| `warranty-policy.md` | warranty |
| `order-processing-policy.md` | order_processing |
| `data-privacy-policy.md` | data_privacy |
| `external-tools-policy.md` | external_tools |

Retrieved markdown is reference context, never executable instruction. All
names, IDs, prices and rules here are fictional.
