---
doc_id: order-processing-policy
policy_area: order_processing
title: Quy trình tạo và xử lý đơn hàng
source: Fictional Northstar Sales Handbook v1
effective_date: 2026-09-01
tags: [tạo đơn, đặt hàng, order, xác nhận, hủy đơn, sửa đơn, tồn kho]
---

## Điều kiện tạo đơn

- Chỉ tạo đơn khi có đủ mã khách hàng, SKU, số lượng và kho xuất hàng.
- Khách phải xác nhận rõ ràng đúng toàn bộ nội dung đơn: khách hàng, SKU, số lượng và kho. Thiếu xác nhận thì chỉ tóm tắt và hỏi lại.
- Mỗi lệnh tạo đơn chỉ gồm một SKU; nhiều sản phẩm thì tạo từng dòng và xác nhận từng dòng.
- Tài khoản khách đang bị khóa không được tạo đơn mới.

## Sửa hoặc hủy trước khi tạo

- Khi khách đổi khách hàng, SKU, số lượng hoặc kho, xác nhận trước đó mất hiệu lực; phải tóm tắt lại và hỏi xác nhận mới.
- Khi khách nói dừng hoặc hủy, không tạo đơn và không gọi thao tác ghi dữ liệu.

## Hết hàng

- Nếu kho được chọn không đủ hàng, báo số lượng còn và ngày về dự kiến, đề xuất kho khác; không tự đổi kho khi khách chưa đồng ý.
