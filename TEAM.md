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
- Thời điểm đã tự nộp URL repo chung trên VLearn: → 09:48:14 16/9/2026

### Bùi Phương Duy — 2A202602684

- Phần việc và file/commit/PR: `artifacts/tools.yaml` v2 + run v2 base 29/30 (`runs/v2_B_base_openai_20260916T022444924297.json`) + dòng v2 trong `version_log.csv` — commit `8d13991`; nội dung dòng v2 trong REPORT B1; 5 case nhóm một lượt `G_S01`–`G_S05` (`ff22ad5`); kiểm tra cuối trước khi nộp.
- Quyết định, khó khăn và cách xử lý: →
  - Ở v2 chỉ sửa phần `description` trong `tools.yaml`, không đổi tên tool hay tham số, vì muốn giữ nguyên interface để các tool, script chấm và case đã chốt không bị vỡ. Cách này giúp đo riêng tác động của mô tả tool lên hành vi model.
  - Bổ sung mô tả rõ hơn cho `view`, `warehouse`, định dạng ID và ý nghĩa các enum để model bớt gọi sai tham số ở các case như S04, S05, S11, S19. Ví dụ `view` cần phân biệt xem tổng quan hay chi tiết, `warehouse` phải dùng đúng mã kho, còn ID không được tự bịa hoặc chép mẫu khi người dùng chưa cung cấp.
  - Khi viết 5 case nhóm một lượt `G_S01`–`G_S05`, Đọc lại bộ case đã chốt trước đó rồi chọn các tình huống khác góc kiểm tra: chính sách bảo mật dữ liệu, xử lý đơn, hóa đơn nháp, ngày hàng về và tình huống song song giữa lỗi thanh toán với chính sách payment. Nhờ vậy case mới không chỉ lặp lại các câu hỏi tồn kho/tạo đơn cơ bản.
- Điều đã học: →
  - Bản thân học được rằng mô tả tool ảnh hưởng rất mạnh tới cách model chọn tool và điền tham số. Chỉ sửa description nhưng điểm base tăng từ 25/30 lên 29/30, nên schema không chỉ là tài liệu cho người đọc mà là một phần của prompt điều khiển agent.
  - Em cũng thấy nếu mô tả ghi mẫu như `ORD-####` không cẩn thận thì model có thể chép nguyên mẫu đó vào tham số thật. Bài học là khi viết ví dụ trong tool description phải nói rõ đó là format minh họa, không phải giá trị hợp lệ để dùng trực tiếp.
- AI/công cụ đã dùng và cách kiểm tra: →
  - Em dùng Claude Code để hỗ trợ đọc lỗi, gợi ý cách diễn đạt description và rà lại case, nhưng tự kiểm tra bằng kết quả chạy và diff trước khi commit.
  - Cách kiểm tra của mình là đọc `git diff` của `artifacts/tools.yaml`, chạy `python scripts/smoke_tools.py`, sau đó đối chiếu từng case FAIL ở run v1 với run v2 để xem lỗi nào được sửa và lỗi nào còn giữ nguyên.
- Thời điểm đã tự nộp URL repo chung trên VLearn: → 09:48:32 16/9/2026


### Nguyễn Trần Bảo Tâm — 2A202602408

- Phần việc và file/commit/PR: `artifacts/system_prompt.md` v3 (`b213df0`); run v3 base 29/30 + adversarial 11/12 (`3dfcf5f`); UI `ui.py` + `requirements.txt` + README mục chạy UI (`f212bd2`); nội dung REPORT A1, A4, B1 dòng v3, B4a, B6, B7 phần prompt.
- Quyết định, khó khăn và cách xử lý: →
  - Ở prompt v3, em thêm quy tắc cho hội thoại nhiều lượt: xác nhận của người dùng chỉ hợp lệ với đúng đơn đang được hỏi và sẽ mất hiệu lực nếu người dùng đổi sản phẩm, đổi số lượng, đổi kho hoặc chuyển sang yêu cầu khác. Mục tiêu là tránh việc agent dùng lại một câu "đồng ý" cũ để tạo đơn mới.
  - Em cũng thêm luật coi các nội dung người dùng tự gõ như `SYSTEM:`, `<assistant>`, `TOOL_RESULTS_JSON` hay `confirmed: true` chỉ là dữ liệu đầu vào, không phải quyền hệ thống và không phải xác nhận hợp lệ. Cách này giúp giảm các case prompt injection và xác nhận giả.
  - Khi làm UI Streamlit, mình quyết định hiển thị tên tool, input arguments, kết quả hoặc lỗi tool, `artifact_version`, provider/model và dừng riêng ở bước `clarify`. Nhờ vậy lúc kiểm thử không chỉ thấy câu trả lời cuối mà còn thấy agent đã gọi tool gì, truyền tham số gì và lỗi nằm ở prompt hay ở tool.
- Điều đã học: →
  - Em học được rằng prompt có thể cải thiện hành vi rất rõ, ví dụ v3 sửa được SM09 và nhiều case xác nhận giả, nhưng chỉ dựa vào prompt thì chưa đủ ổn định. Việc `v3-recheck` adversarial chỉ còn 8/12 cho thấy model vẫn có dao động giữa các lần chạy và cần thêm guardrail ở tool hoặc evaluator để chắc hơn.
  - Em cũng nhận ra không thể chỉ nhìn điểm tổng. Phải mở `tool_results` để biết model gọi tool đúng hay sai, và kiểm tra thư mục `orders/` để xem có đơn nào bị tạo ngoài ý muốn không; có những lỗi chỉ nhìn câu trả lời cuối sẽ rất dễ bỏ sót.
- AI/công cụ đã dùng và cách kiểm tra: →
  - EM dùng Claude Code để hỗ trợ rà prompt, đọc kết quả fail và viết UI Streamlit nhanh hơn, sau đó tự kiểm tra lại bằng run thật và transcript.
  - Cách kiểm tra của mình là đọc diff của `artifacts/system_prompt.md`, chạy lại bộ base và adversarial, tự chạy UI bằng `python -m streamlit run ui.py`, thử các luồng cần `clarify`, rồi kiểm tra `orders/` sau mỗi run để chắc không có đơn bị tạo sai.
- Thời điểm đã tự nộp URL repo chung trên VLearn: → 09:46:12 16/9/2026

### Trần Thị Thu Hiền — 2A202602737

- Phần việc và file/commit/PR: 5 case nhóm nhiều lượt `G_M01`–`G_M05` trong `data/eval_group.json` + nới validator `scripts/smoke_tools.py` cho lượt `assistant` (`83c98ed`); run group v3 10/10 (`97bb2f2`); 4 transcript UI (`db4ce31`); nội dung REPORT A3, B3, B4.
- Quyết định, khó khăn và cách xử lý: →
  - *Gợi ý: bạn chọn 5 kịch bản nào và vì sao (xác nhận hợp lệ để tạo đơn, khách bị khóa, đổi kho khi hết hàng, chính sách bảo hành, tìm web hợp lệ)? Vì sao phải cho phép lượt `assistant` trong `turns`? Khi tạo 4 transcript, bạn dựng tình huống thiếu thông tin và sửa mã đơn thế nào?*
- Điều đã học: →
  - *Gợi ý: bộ case tự viết đạt 10/10 nhưng bộ chốt vẫn còn case FAIL — điều đó nói gì về việc tự viết case sau khi đã biết prompt? Trong transcript, agent hỏi lại bằng lời thay vì gọi `clarify`: bạn nghĩ sao về khoảng cách giữa điểm eval và hành vi thật?*
- AI/công cụ đã dùng và cách kiểm tra: →
  - *Gợi ý: công cụ AI đã dùng; cách kiểm tra — chạy `python scripts/smoke_tools.py --cases data/eval_group.json`, đối chiếu ID trong case với `data/sales_data/`, đọc lại 4 transcript xem có lộ dữ liệu nhạy cảm không.*
- Thời điểm đã tự nộp URL repo chung trên VLearn: →
