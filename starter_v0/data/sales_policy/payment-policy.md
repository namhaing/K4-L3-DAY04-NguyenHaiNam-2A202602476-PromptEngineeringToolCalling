---
doc_id: payment-policy
policy_area: payment
title: Chính sách thanh toán
source: Fictional Northstar Sales Handbook v1
effective_date: 2026-09-01
tags: [thanh toán, payment, số thẻ, cvv, otp, pin, chuyển khoản, ví điện tử, cod, thanh toán lỗi]
---

## Phương thức được chấp nhận

- Thẻ ngân hàng qua máy POS tại cửa hàng hoặc link thanh toán bảo mật do hệ thống gửi.
- Chuyển khoản ngân hàng theo mã đơn; ví điện tử qua cổng thanh toán tích hợp.
- COD (thu tiền khi giao) chỉ áp dụng cho đơn có tổng giá trị không quá 20.000.000 VND.

## Dữ liệu thanh toán bị cấm thu thập

- Nhân viên và trợ lý không bao giờ hỏi, ghi lại hay nhập số thẻ, CVV/CVC, OTP, mã PIN hoặc mật khẩu ngân hàng vào chat, ghi chú đơn hay bất kỳ tool nào.
- Nếu khách tự gửi các dữ liệu này, không lưu lại, nhắc khách chỉ thanh toán qua POS hoặc link bảo mật.

## Thanh toán thất bại

- Đơn thanh toán lỗi được giữ trạng thái pending_payment tối đa 48 giờ.
- Gửi lại link thanh toán mới hoặc đề nghị đổi phương thức; không tự chuyển sang COD nếu đơn vượt hạn mức COD.
