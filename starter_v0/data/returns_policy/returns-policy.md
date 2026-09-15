---
doc_id: returns-policy
policy_area: returns
title: Chính sách đổi trả
source: Fictional Northstar Sales Handbook v1
effective_date: 2026-09-01
tags: [đổi trả, trả hàng, hoàn tiền, lỗi, đổi ý, giao nhầm, sealed_only]
---

## Phạm vi

- Áp dụng cho sản phẩm **đã giao thành công** trong một đơn hàng; tính số ngày từ `delivered_at` của đơn.
- Tài liệu này được tool `check_return_eligibility` dùng để kiểm tra điều kiện; tool chỉ đọc, không tạo phiếu đổi trả.

## Thời hạn theo lý do

- `defective` (lỗi kỹ thuật): trong **30 ngày**, chấp nhận cả hàng đã mở hộp.
- `wrong_item` (giao nhầm sản phẩm): trong **30 ngày**, chấp nhận cả hàng đã mở hộp.
- `changed_mind` (khách đổi ý): trong **7 ngày**.

## Loại hàng

- `standard`: đổi ý khi đã mở hộp vẫn được nhận lại nhưng thu phí kiểm định **10%** giá sản phẩm; chưa mở hộp thì không thu phí.
- `sealed_only` (tai nghe nhét tai/chụp tai vì lý do vệ sinh): đổi ý **chỉ nhận khi còn nguyên niêm phong**; lỗi kỹ thuật hoặc giao nhầm vẫn áp dụng như `standard`.

## Không đủ điều kiện

- Đơn chưa giao, hoặc sản phẩm trong đơn chưa được giao (giao thiếu) — xử lý theo chính sách vận chuyển, không phải đổi trả.
- Quá thời hạn theo lý do.
- Sản phẩm không thuộc đơn hàng được nêu.
