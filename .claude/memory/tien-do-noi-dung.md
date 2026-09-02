---
name: tien-do-noi-dung
description: Tiến độ viết bài theo từng kệ — năm kệ đầu xong hẳn, toàn bộ khung còn lại nằm ở kệ 06→10
metadata:
  type: project
updated: 2026-09-02
---

**127/199 bài đã viết (64%)** tính tới 2026-09-02. Số liệu lấy bằng cách đếm cờ `skeleton` trong
`assets/catalog.js` sau khi chạy `python3 tools/build.py` — đó là nguồn duy nhất đáng tin, đừng
chép lại con số ở đây khi đã sửa nội dung.

| Kệ | Đã viết / tổng |
|---|---|
| 01 DSA | 23/23 ✅ |
| 02 Python | 17/17 ✅ |
| 03 CS fundamentals | 14/14 ✅ |
| 04 Database & SQL | 23/23 ✅ |
| 05 Machine learning | 38/38 ✅ |
| 06 Deep learning | 4/18 |
| 07 Transformer | 2/16 |
| 08 LLM & GenAI | 4/31 |
| 09 ML system design | 1/5 |
| 10 MLOps | 1/14 |

Năm kệ đầu đã xong hẳn; **toàn bộ 72 khung còn lại nằm ở kệ 06→10**.

Bảng "Việc còn lại" ở cuối `CLAUDE.md` đã sửa cho khớp ngày 2026-09-02, và thêm câu dặn đừng tin
số trong đó — nó lệch ngay khi có người viết xong một bài.

Kệ 05 viết từ trên xuống và **đã xong trọn 9 nhóm**. Ngày 2026-09-02 nhóm *Statistics &
experimentation* được **dời từ cuối kệ lên vị trí 03**, ngay sau Math foundations — nó là chiều
ngược của xác suất (mẫu → tổng thể) nên thuộc cùng mạch toán, và đọc trước làm chặng Core concepts
dễ vào hơn. Dời nhóm = đổi tiền tố thư mục + sửa mọi link tương đối trong kệ + `dir` trong
`category.json` + đoạn *Học theo thứ tự nào* ở `ml-overview`; `git mv` giữ được lịch sử. **Chặng tiếp theo là kệ 06 Deep learning**
(14 khung), rồi 07 Transformer (14) — ba kệ 06→08 nối nhau bằng một dòng thời gian duy nhất nên
phải viết theo đúng thứ tự đó.

Ba overview của kệ 05 đều **bỏ khuôn 8 mục ép sẵn** (timeline / nhánh / từ điển) —
`math-foundations-overview` và `core-concepts-overview` dùng khuôn ngắn 3 mục vì các bài trong nhóm
là **chặng của một câu hỏi**, không phải biến thể cạnh tranh. `classical-models-overview` cũng chỉ
3 mục dù nhóm *là* sáu model song song: chúng không cái nào sinh ra để chữa cái kia nên timeline
nhân quả thành hình thức rỗng — khuôn đúng là **giả định → bảng tra → thứ tự học**.
Xem [[quy-uoc-viet-overview]].
Nhóm Tree models lặp lại đúng cái bẫy của Core concepts và Classical ML: bài cha `gradient-boosting` đã ôm sẵn
hình mọc-theo-lá và cả bảng so sánh XGBoost/LightGBM mà hai khung sinh ra để giải thích. Cách gỡ:
**chuyển** hình sang `lightgbm` rồi rút §03 của bài cha còn một bảng trỏ đường, không viết lại.
Cùng dịp đó `details.deep` — quy ước đã chết theo TAXONOMY §A4 — được dọn nốt 5 chỗ cuối cùng
(2 ở `gradient-boosting`, 3 ở `random-forest`): phần đáng giữ đưa thẳng ra ngoài, phần chỉ lặp lại
`ul.why` phía trên thì bỏ. **Cả kho giờ sạch `details.deep`.**
Và nhóm Core concepts không viết mới bốn bài mà **tách** `overfitting-regularization` (15 mục, đã ôm sẵn
bias–variance + CV + rò rỉ dữ liệu) thành ba bài theo quy trình trong CLAUDE.md — chi tiết
[[tach-bai-overfitting-core-concepts]].

Nhóm Model evaluation lặp lại bẫy đó thêm lần nữa, và nặng nhất: **không có gì để viết mới** —
`metrics-confusion-matrix` (15 mục) đã ôm sẵn cả ROC-AUC, PR-AUC lẫn calibration, tức toàn bộ lý do
tồn tại của hai khung. Gỡ bằng quy trình *Tách một bài làm hai*: bê §06–07 sang `roc-auc-pr`, §09
sang `calibration`, **giữ nguyên câu chữ**, chia các thẻ `.card.bad` và `details.qa` về đúng bên rồi
viết bù cho đủ, đánh số lại từ 01, và bỏ thẻ `<script src="lab.js">` ở hai bài mới vì lab ở lại với
bài cha. Bốn lần liên tiếp gặp bẫy này ⇒ **trước khi viết bất kỳ khung nào, đọc hết bài đã viết
cùng nhóm** — rất có thể việc thật là tách chứ không phải viết.

Riêng kệ 02 xem [[soat-ke-02-python]], kệ 04 xem [[soat-ke-04-database]].
