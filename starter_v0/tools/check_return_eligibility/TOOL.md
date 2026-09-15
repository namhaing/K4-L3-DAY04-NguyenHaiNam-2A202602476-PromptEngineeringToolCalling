---
name: check_return_eligibility
track: bonus
kind: local_status
provider: local_order_store
requires_env: []
inputs: [order_id, sku, reason, opened]
outputs: [eligible, failed_conditions, days_since_delivery, window_days, return_class, fee_percent, next_step, policy_ref]
side_effect: false
---
# check_return_eligibility

Bonus tool (ngoài luồng bán hàng cơ bản). Kiểm tra **chỉ đọc** xem một sản phẩm
trong một đơn đã giao có đủ điều kiện đổi trả không, theo
`data/returns_policy/returns-policy.md`, dùng `data/sales_data/orders.json`
(ngày giao, số lượng đã giao) và `products.json` (`return_class`).

- `reason`: `defective` (30 ngày), `wrong_item` (30 ngày), `changed_mind` (7 ngày).
- `opened` + `changed_mind`: hàng `sealed_only` không nhận; hàng `standard` nhận với phí 10%.
- Số ngày tính từ `delivered_at` tới `snapshot_at` cố định của dữ liệu (kết quả ổn định).

Lỗi rõ ràng: `missing_fields`, `invalid_order_id_format`, `invalid_sku_format`,
`invalid_reason`, `invalid_opened_type`, `order_not_found`, `sku_not_in_order`.
Đơn/sản phẩm chưa giao trả `eligible: false` với `order_not_delivered` /
`item_not_delivered`.

Không trả tên, số điện thoại hay mã khách; không tạo phiếu đổi trả và không ghi file.
