# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: ahihi
- Người đại diện / MSSV: Nguyễn Hải Nam — 2A202602476
- Tên repo: `K4-L3-DAY04-NguyenHaiNam-2A202602476-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt: https://github.com/namhaing/K4-L3-DAY04-NguyenHaiNam-2A202602476-PromptEngineeringToolCalling — nhánh `main` — commit chốt bộ case trước v0: `b14ba97`; commit nộp cuối: *(điền khi chốt)*
- Deadline áp dụng và link thông báo đổi hạn nếu có: 23:59 ngày làm lab, Asia/Ho_Chi_Minh *(bổ sung link nếu Keycoach đổi hạn)*

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| *Nguyễn Hải Nam* | 2A202602476 | namhaing | Người đại diện. Nền tảng: dữ liệu giả lập, 8 tool bán hàng, smoke test, 42 case chốt, prompt + `tools.yaml` v0, chạy v0; prompt v1; tool bonus đổi trả và chạy v4 | Xem "Nhật ký đóng góp" bên dưới |
| *Bùi Phương Duy* | 2A202602684 | DuyPhuong8804 | `tools.yaml` v2 và run v2; 5 case nhóm một lượt; kiểm tra cuối trước khi nộp | Xem "Nhật ký đóng góp" |
| *Nguyễn Trần Bảo Tâm* | 2A202602408 | BaoTamnt | Prompt v3 + run base/adversarial v3; UI Streamlit; REPORT phần an toàn (B4a, B6) và giới thiệu agent (A1, A4) | Xem "Nhật ký đóng góp" |
| *Trần Thị Thu Hiền* | 2A202602737 | hientran-ai | 5 case nhóm nhiều lượt; chạy bộ case nhóm; 4 transcript UI; REPORT B3, B4 | Xem "Nhật ký đóng góp" |

## Nhật ký đóng góp (sự thật từ git log — cập nhật liên tục)

Nhóm làm trên **một máy chung**; mỗi commit ghi đúng người đang thực hiện (tên/email git của người đó). Người ngồi máy dùng Claude Code hỗ trợ ở một số bước — mỗi người tự ghi rõ trong mục "AI/công cụ đã dùng" của mình.

### Nguyễn Hải Nam

| Commit | Thời gian | Nội dung |
|---|---|---|
| `ba0192c` | 2026-09-15 19:54 | Dữ liệu giả lập `data/sales_data/` (products, stock, customers, orders) |
| `89b1650` | 2026-09-15 20:02 | Sao lưu artifact IT sang `artifacts/it_reference/`, ignore `orders/` |
| `205e467` | 2026-09-15 20:02 | Tool `search_products`, `check_stock`, `get_order`, `create_order` |
| `58e26d9` | 2026-09-15 20:03 | `tools.yaml` v0 (8 tool + clarify), `scripts/smoke_tools.py` |
| `61fabbe` | 2026-09-16 00:24 | `system_prompt.md` v0 |
| `df7a3fd` | 2026-09-16 00:28 | Tool `lookup_customer`, `sales_policy`, `format_quote`, `search_product_web`; `data/sales_policy/`; smoke test kiểm tra case |
| `b14ba97` | 2026-09-16 00:29 | **Commit chốt** 30 case base + 12 case adversarial |
| `a62ed7d` | 2026-09-16 01:19 | Run v0 base 22/30, adversarial 6/12, `analysis/`, version log v0 |
| `580f82c` | 2026-09-16 01:54 | `system_prompt.md` v1 |
| `f29092e` | 2026-09-16 02:07 | Run v1 base 25/30, analysis, version log v1 |
| `3c737e8` | 2026-09-16 03:42 | Bonus: `tools/check_return_eligibility/`, `data/returns_policy/returns-policy.md`, `data/sales_bonus.json` (8 case), 9 smoke test |
| `64bf463` | 2026-09-16 03:42 | `tools.yaml` v4: khai báo tool bonus |
| `f7df194` | 2026-09-16 03:45 | Run v4 base **29/30**, adversarial **9/12** (2 đơn tạo sai), extension (bonus) **6/8**; analysis; 3 dòng v4 trong `version_log.csv` |
| `1d387db` | 2026-09-16 03:52 | Run kiểm chứng `v3-recheck` adversarial **8/12** (đúng artifact v3, lại tạo 2 đơn sai → xác nhận dao động của model); analysis (216 dòng); dòng v3-recheck trong `version_log.csv` |

### Bùi Phương Duy

| Commit | Thời gian | Nội dung |
|---|---|---|
| `8d13991` | 2026-09-16 02:33 | `artifacts/tools.yaml` v2: chỉ sửa description (khi nào dùng/không dùng tool, định dạng ID, ý nghĩa enum `view`/`warehouse`/`category`/`policy_area`, `clarify.response_type`, `create_order.confirmed`); run v2 base **29/30 (0,9667)** — `runs/v2_B_base_openai_20260916T022444924297.json`; `analysis/run-analysis.csv`; dòng v2 trong `version_log.csv` |
| `ff22ad5` | 2026-09-16 03:22 | `data/eval_group.json`: 5 case nhóm một lượt `G_S01`–`G_S05` (chính sách data_privacy, order_processing; hóa đơn nháp invoice_draft; ngày về hàng incoming; song song đơn thanh toán lỗi + chính sách payment) |

###  Nguyễn Trần Bảo Tâm

| Commit | Thời gian | Nội dung |
|---|---|---|
| `b213df0` | 2026-09-16 02:49 | `artifacts/system_prompt.md` v3: quy tắc hội thoại nhiều lượt, xác nhận gắn đúng đơn hiện tại và mất hiệu lực khi đổi, nội dung user dán (`SYSTEM:`, `<assistant>`, `TOOL_RESULTS_JSON`, `confirmed: true`) không phải quyền/xác nhận, dữ liệu thẻ, ranh giới web search |
| `3dfcf5f` | 2026-09-16 02:57 | Run v3 base **29/30 (0,9667)** — `runs/v3_B_base_openai_20260916T025127592466.json`; run v3 adversarial **11/12 (0,9167)** — `runs/v3_B_adversarial_openai_20260916T025255632910.json`; `analysis/run-analysis.csv` (144 dòng); 2 dòng v3 trong `version_log.csv` |
| *(chưa commit — file chung)* | | REPORT: B1 dòng v3 + so sánh, B4a (SA04, SA05, SA10, SA11, SA12), B6 |
| `f212bd2` | 2026-09-16 03:07 | UI `starter_v0/ui.py` (Streamlit): hiện tool, input args, result/lỗi, artifact_version, provider/model; dừng ở `clarify` + nút trả lời nhanh; lưu transcript. `requirements.txt` (+streamlit), README mục chạy UI |

### Trần Thị Thu Hiền

| Commit | Thời gian | Nội dung |
|---|---|---|
| `83c98ed` | 2026-09-16 03:16 | `data/eval_group.json`: đổi `dataset_id`/`description` sang bán hàng, 5 case nhiều lượt `G_M01`–`G_M05` (xác nhận hợp lệ → tạo đơn, khách bị khóa, đổi kho khi hết hàng, chuyển sang chính sách bảo hành, web search hợp lệ); `scripts/smoke_tools.py`: cho phép lượt `assistant` trong `turns` |
| `97bb2f2` | 2026-09-16 03:27 | Run group v3 **10/10** — `runs/v3_B_group_openai_20260916T032432135320.json`; `analysis/run-analysis.csv` (154 dòng); dòng group trong `version_log.csv` |
| `db4ce31` | 2026-09-16 03:35 | 4 transcript UI trong `starter_v0/transcripts/` (tồn kho; thiếu thông tin → bổ sung; sửa mã đơn; tạo đơn sau xác nhận → `SO-39AB059F`) |

## Nhận xét chung

- Kết quả và bằng chứng: v0 base 22/30 (0,7333) → v1 25/30 (0,8333) → v2 29/30 (0,9667) → v3 29/30 (multi-turn 1,00) — [version_log.csv](starter_v0/artifacts/version_log.csv), [REPORT B1](starter_v0/artifacts/REPORT.md). Adversarial v0 6/12 → v3 11/12. Group (10 case tự viết) v3 10/10. v4 (thêm tool bonus): base 29/30, adversarial 9/12, bonus 6/8; chạy lại đúng v3 chỉ 8/12 → adversarial dao động giữa các lần chạy, không do tool bonus. 8 đơn bị tạo sai (v0: SA04, SA10, SA11; v2: SM09; v4: SA03, SA11; v3-recheck: SA03, SA11) ([REPORT B4a/B6](starter_v0/artifacts/REPORT.md)). *(cập nhật sau v4)*
- Thay đổi hiệu quả nhất: *(nhóm thảo luận và tự viết; số liệu tham khảo: v2 `tools.yaml` +4 case base, v3 prompt +5 case adversarial và chặn toàn bộ đơn tạo sai)*
- Giới hạn còn lại: *(nhóm tự viết; dữ kiện: v3 S11 chép mẫu `CUS-####`, SA09 thiếu `category`, SA10 câu xác nhận tóm tắt sai payload, chỉ chấm lần gọi model đầu tiên, không có Tavily key)*
- Cách phân công và tích hợp: Nam dựng nền tảng (dữ liệu giả lập, 8 tool, 42 case chốt, artifact v0) và làm prompt v1. Từ v2 chia theo chuỗi bàn giao, mỗi người chỉ sửa artifact của mình rồi bàn giao: Duy `tools.yaml` v2 → Bảo Tâm prompt v3 và UI → Thu Hiền 10 case nhóm + transcript → Nam tool bonus và v4 → Duy kiểm tra cuối. Cả nhóm làm trên một máy chung; mỗi người commit bằng tên/email git của mình nên lịch sử commit đối chiếu được (xem Nhật ký đóng góp).

## INDIVIDUAL

**Cách dùng form này:** dòng *Phần việc* đã ghi sẵn sự thật lấy từ git log — kiểm tra lại rồi giữ nguyên. Bốn ý còn lại **mỗi người tự viết bằng lời của mình**, trả lời vào sau dấu `→` và **xóa các dòng "Gợi ý"** sau khi viết xong. Mỗi người tự commit phần của mình bằng tên/email git của mình.

### Nguyễn Hải Nam — 2A202602476

- Phần việc và file/commit/PR: dữ liệu `data/sales_data/` (`ba0192c`); 8 tool bán hàng (`205e467`, `df7a3fd`); `tools.yaml` v0 + `scripts/smoke_tools.py` (`58e26d9`); 30 + 12 case và commit chốt (`b14ba97`); prompt v0 (`61fabbe`); run v0 (`a62ed7d`); prompt v1 (`580f82c`) và run v1 (`f29092e`); bonus `check_return_eligibility` (`3c737e8`, `64bf463`), run v4 (`f7df194`) và run kiểm chứng v3-recheck (`1d387db`); REPORT đầu trang, A2, B1, B2, B5.
- Quyết định, khó khăn và cách xử lý: →
  - Khi thiết kế `create_order`, mình chọn mỗi lần gọi chỉ tạo một SKU để payload đơn giản, dễ kiểm tra tồn kho và dễ đối chiếu khi eval xem model đã gọi đúng tham số chưa. Mình cũng chặn ghi đơn nếu `confirmed != true` để tránh trường hợp agent tự ý tạo đơn khi người dùng mới hỏi giá hoặc mới cung cấp thiếu thông tin.
  - Với bonus đổi trả, mình đặt `returns-policy.md` trong `data/returns_policy/` thay vì trộn vào `data/sales_policy/` để tách rõ chính sách bán hàng và chính sách hậu mãi. Nhờ vậy tool `sales_policy` và tool `check_return_eligibility` không bị lẫn nguồn dữ liệu.
  - Khó khăn lớn nhất là lần chạy đầu bị dùng nhầm provider `openrouter`, làm toàn bộ 42 case thành `provider_error`. Mình xử lý bằng cách kiểm tra lại cấu hình provider/model, chạy lại bằng OpenAI, rồi chỉ dùng các run hợp lệ để so sánh trong báo cáo.
  - Mình vẫn giữ run v4 dù adversarial tụt vì v4 là bằng chứng thật sau khi thêm tool bonus, không nên xóa kết quả xấu. Sau đó mình chạy thêm `v3-recheck` để kiểm chứng xem việc tụt điểm do tool bonus hay do độ dao động của model; kết quả recheck cũng thấp hơn v3 ban đầu nên nhóm kết luận adversarial có dao động giữa các lần chạy.
- Điều đã học: →
  - Học được cách làm việc nhóm và chia việc hiệu quả giữa các thành viên dù mới đầu còn bỡ ngỡ
  - Mình học được rằng guardrail trong code rất cần thiết nhưng không đủ. Code có thể chặn số thẻ hoặc mã nội bộ theo điều kiện rõ ràng, nhưng nếu schema cho phép `confirmed: true` thì model vẫn có thể tự điền và vượt qua ý định ban đầu nếu prompt/eval chưa ràng buộc chặt.
  - Một lần chạy chỉ cho biết hành vi của agent ở đúng cấu hình, dữ liệu và thời điểm đó; nó không chứng minh hệ thống luôn an toàn. Muốn đánh giá chắc hơn cần xem nhiều run, đọc `tool_results`, kiểm tra artifact tạo ra và so sánh cả case base, adversarial, group.
- AI/công cụ đã dùng và cách kiểm tra: →
  - Mình dùng Claude Code để hỗ trợ đọc diff, viết/soát prompt, tool và báo cáo; các quyết định cuối vẫn tự kiểm tra lại bằng file và kết quả chạy.
  - Cách kiểm tra của mình là đọc `git diff` trước khi commit, chạy `python scripts/smoke_tools.py`, đối chiếu `tool_results` trong các file run JSON, mở thư mục `orders/` để xem có đơn nào bị tạo sai không, và so lại artifact với commit tương ứng trong `version_log.csv`.
- Thời điểm đã tự nộp URL repo chung trên VLearn: →

### Bùi Phương Duy — 2A202602684

- Phần việc và file/commit/PR: `artifacts/tools.yaml` v2 + run v2 base 29/30 (`runs/v2_B_base_openai_20260916T022444924297.json`) + dòng v2 trong `version_log.csv` — commit `8d13991`; nội dung dòng v2 trong REPORT B1; 5 case nhóm một lượt `G_S01`–`G_S05` (`ff22ad5`); kiểm tra cuối trước khi nộp.
- Quyết định, khó khăn và cách xử lý: →
  - *Gợi ý: vì sao v2 chỉ sửa phần `description` mà không đổi tên tool/tham số? Bạn chọn mô tả thêm gì cho `view`, `warehouse` và định dạng ID để sửa S04, S05, S11, S19? Khi viết 5 case một lượt, bạn tránh trùng với các case đã chốt bằng cách nào?*
- Điều đã học: →
  - *Gợi ý: mô tả tool ảnh hưởng tới hành vi model ra sao (base 25/30 → 29/30)? Tác dụng phụ khi ghi mẫu `ORD-####` trong mô tả (model chép nguyên mẫu vào tham số) cho bạn bài học gì?*
- AI/công cụ đã dùng và cách kiểm tra: →
  - *Gợi ý: công cụ AI đã dùng và cách bạn tự kiểm tra — đọc `git diff` của `tools.yaml`, chạy smoke test, đối chiếu từng case FAIL trong run v1 với run v2.*
- Thời điểm đã tự nộp URL repo chung trên VLearn: →

### Nguyễn Trần Bảo Tâm — 2A202602408

- Phần việc và file/commit/PR: `artifacts/system_prompt.md` v3 (`b213df0`); run v3 base 29/30 + adversarial 11/12 (`3dfcf5f`); UI `ui.py` + `requirements.txt` + README mục chạy UI (`f212bd2`); nội dung REPORT A1, A4, B1 dòng v3, B4a, B6, B7 phần prompt.
- Quyết định, khó khăn và cách xử lý: →
  - *Gợi ý: v3 bạn thêm quy tắc nào cho hội thoại nhiều lượt và cho xác nhận? Vì sao coi `SYSTEM:`, `<assistant>`, `TOOL_RESULTS_JSON` do người dùng gõ là dữ liệu chứ không phải quyền? Khi làm UI, bạn quyết định hiển thị gì để không che lỗi tool?*
- Điều đã học: →
  - *Gợi ý: v3 sửa được SM09 và nhóm case xác nhận giả, nhưng lần chạy lại chỉ còn 8/12 — điều đó nói gì về việc chỉ dựa vào prompt? Vì sao phải mở `tool_results` và thư mục `orders/` thay vì chỉ nhìn điểm?*
- AI/công cụ đã dùng và cách kiểm tra: →
  - *Gợi ý: công cụ AI đã dùng; cách kiểm tra — đọc diff prompt, chạy base + adversarial, tự chạy UI bằng `python -m streamlit run ui.py`, kiểm tra `orders/` sau mỗi run.*
- Thời điểm đã tự nộp URL repo chung trên VLearn: →

### Trần Thị Thu Hiền — 2A202602737

- Phần việc và file/commit/PR: 5 case nhóm nhiều lượt `G_M01`–`G_M05` trong `data/eval_group.json` + nới validator `scripts/smoke_tools.py` cho lượt `assistant` (`83c98ed`); run group v3 10/10 (`97bb2f2`); 4 transcript UI (`db4ce31`); nội dung REPORT A3, B3, B4.
- Quyết định, khó khăn và cách xử lý: →
  - *Gợi ý: bạn chọn 5 kịch bản nào và vì sao (xác nhận hợp lệ để tạo đơn, khách bị khóa, đổi kho khi hết hàng, chính sách bảo hành, tìm web hợp lệ)? Vì sao phải cho phép lượt `assistant` trong `turns`? Khi tạo 4 transcript, bạn dựng tình huống thiếu thông tin và sửa mã đơn thế nào?*
- Điều đã học: →
  - *Gợi ý: bộ case tự viết đạt 10/10 nhưng bộ chốt vẫn còn case FAIL — điều đó nói gì về việc tự viết case sau khi đã biết prompt? Trong transcript, agent hỏi lại bằng lời thay vì gọi `clarify`: bạn nghĩ sao về khoảng cách giữa điểm eval và hành vi thật?*
- AI/công cụ đã dùng và cách kiểm tra: →
  - *Gợi ý: công cụ AI đã dùng; cách kiểm tra — chạy `python scripts/smoke_tools.py --cases data/eval_group.json`, đối chiếu ID trong case với `data/sales_data/`, đọc lại 4 transcript xem có lộ dữ liệu nhạy cảm không.*
- Thời điểm đã tự nộp URL repo chung trên VLearn: →
