---
name: trang-thai-kho
description: "Trạng thái toàn kho — mốc số liệu duy nhất, sáu trục nghiệm thu, chất lượng trình bày từng kệ, việc còn lại"
metadata:
  type: project
updated: 2026-09-09
---

**Đây là mốc duy nhất.** Mọi con số rời rạc trong các phiên trước đã lệch; đo lại từ file bằng
`python3 tools/build.py`, đếm cờ `skeleton` trong `assets/catalog.js`, và `python3 tools/soat.py`.

## Tiến độ nội dung (2026-09-08)

| Kệ | Đã viết / tổng |
|---|---|
| 01 DSA · 02 Python · 03 CS · 04 Database | 23 · 17 · 14 · 23 — **xong hết** |
| 05 Machine learning | **39/39 ✅** |
| 06 Deep learning | 4/18 |
| 07 Transformer | 2/16 |
| 08 LLM & GenAI | 4/31 |
| 09 ML system design | 1/5 |
| 10 MLOps | 1/14 |

**200 bài · 72 khung còn lại, toàn bộ ở kệ 06→10.** Ba kệ 06→08 nối nhau bằng một dòng thời gian
duy nhất nên **phải viết theo đúng thứ tự đó**. Chặng tiếp theo: kệ 06 Deep learning.

Số của build hôm nay: `10 kệ · 62 nhóm · 200 bài · 1.461 mục · 505 thẻ ôn từ 109 mục Hỏi đáp`,
không cảnh báo. `soat.py`: **0 ở cả 8 phép**.

## Sáu trục nghiệm thu — kệ 01→05 SẠCH cả sáu (chốt 2026-09-08)

```
build.py                : sạch · 200 bài · meta khớp
audit.py  (luật 1)      : 116/116
soat.py   (8 phép)      : 0 toàn kho
svgkit/check.py         : 0 lỗi / 39 bài kệ ML
bbox thật (getBBox)     : 0 tràn/đè
đoạn văn mặt bài >33 từ : 0            (trước là 65)
490px Chrome thật       : 0 · 116 bài + 3 trang site
```

## Chất lượng TRÌNH BÀY — trục thứ bảy, chưa từng đo, đo lần đầu 2026-09-08

Sáu trục trên là trục **luật**. Chuẩn trình bày của người dùng (ít chữ nhiều hình · rất ít note ·
câu đơn · công thức LaTeX — xem [[trinh-bay-bai]]) là **trục khác**, và nó chỉ mới thật sự áp ở
kệ 05. Đây là bức tranh đúng, đừng báo cáo "kho đã sạch" mà không kèm bảng này.

### Mật độ `.note` (luật: tối đa 1 bài)

| Kệ | note/bài | |
|---|---|---|
| 05 ML | **0,2** | đạt — 39 bài đã quét lại |
| 02 Python | 0,6 | đạt |
| 01 DSA | 1,0 | sát mốc |
| 04 Database | 1,7 | quá |
| 03 CS | 2,5 | quá |
| 06 DL · 07 Transformer · 08 LLM | **7,8 · 8,5 · 8,5** | chưa đụng tới |
| 09 MLSD · 10 MLOps | **10,0 · 12,0** | chưa đụng tới |

Nặng nhất: `mlops-serving` 12 · `rag-end-to-end` 12 · `backpropagation` 11 ·
`inference-optimization` 11. Mười một bài đã viết sẵn ở kệ 06→10 là **di sản trước khi có chuẩn**,
không phải bài mới hỏng.

### Chữ/hình trên mốc 250 — 18 bài

DSA 13 bài, nặng nhất `tree-bst-traversal` 566 · `union-find` 499 · `linked-list` 394 ·
`backtracking` 379 · `stack-monotonic-queue` 377 · `sliding-window` 359 · `two-pointers` 344 ·
`sorting` 298. Database 4: `data-quality` 355 · `er-modeling` 269 · `nosql-landscape` 264 ·
`query-tuning` 258. Python 1: `python-overview` 263. **Kệ ML: 0 bài.**

### Công thức dáng LaTeX — chỉ có ở kệ ML

404 lượt `<var>`, **100% nằm ở kệ 05**. Kệ 06→10 có 24 khối `.eq` nhưng **không một `<var>` nào**
— công thức ở đó vẫn là chữ trơn. Viết bài mới ở 06→10 thì đây là việc phải làm ngay từ đầu, đừng
để thành đợt sửa sau.

**Còn 6 bài dùng `<span class="op">/</span>` thay `.frac`** (2026-09-09): `bayes-theorem` ·
`random-forest` · `statistics` · `normalization` · `rag-end-to-end` · `inference-optimization`.
Chạm bài nào thì đổi bài đó.

### Hai khuôn mới còn là bản thử, chưa thành chuẩn kho

`dl.defs` (bảng tra ký hiệu) chỉ có ở `svm` — 3 chỗ. `.hl` (in đậm cam thay `<b>`) chỉ có ở `knn`
— 3 chỗ. Cả hai đã chốt là đúng, nhưng chưa bài nào khác dùng. Chạm bài nào thì đổi bài đó.

### Câu đơn trong `details.qa` — chỗ hổng lớn nhất còn lại

Mặt bài đã sạch (0 đoạn >33 từ). **Bên trong `details.qa` thì chưa**: cả kho chỉ `svm` (0 đoạn
dài) và `decision-tree` (1) là đạt. Riêng kệ ML còn **29 bài** trả lời bằng một khối liền —
`train-val-test-cv` 126 từ · `statistics` 122 · `ab-testing` 108 · `knn` 118.
(`naive-bayes` đã sửa 2026-09-09: 5 câu, 24 đoạn, dài nhất 16 từ — cùng lần dựng lại theo luật 1.)

Đây không phải chuyện đẹp xấu: `tools/build.py` bóc `details.qa` thành **505 thẻ ôn**, nên mỗi
khối 118 từ là một mặt sau thẻ không đọc nổi. Sửa chỗ này là sửa luôn bộ thẻ ôn.

### `<pre>` còn nhiều ở kệ ngoài ML

Database 59 · DSA 43 · Python 42 khối, so với ML 4. Ở DSA thì đúng (mẫu code cần thuộc là khuôn
bài của kệ đó); ở Database phần lớn là bảng số và dẫn giải, xét lại được.

## Hai chỗ lệch đã xác minh, chưa sửa

1. **`soat.py` phép 6 không `html.unescape()`** trước khi dò, khác phép 5 và phép 8. 27 bài có
   tiếng Việt viết bằng entity (`&#225;`…; `adaboost` 404 chỗ, `er-modeling` 290,
   `tree-bst-traversal` 130), nên phép 6 **bỏ sót 3 vi phạm thật**: `adaboost` «cây quyết định»,
   `adaboost` «hàm mất mát», `dbscan` «hàng xóm». Đúng kiểu lỗi thước đã ghi ở
   [[cong-cu-va-cach-kiem]] — thước sạch và bài sạch in ra cùng một dòng.
2. **Tên mục lệch giữa hai nửa kho:** `<h2>Loss function</h2>` 14 lần (toàn kệ 05) so với
   `<h2>Hàm mục tiêu</h2>` 13 lần (3 ở DL, 6 ở Transformer, 4 ở LLM). `CLAUDE.md` ghi dạng tiếng
   Việt, nhưng cả hai bài mẫu dùng dạng tiếng Anh. Chốt theo bài mẫu: **Loss function**.

## Một thứ chưa được ghi ở đâu cả

`quiz.html` + `assets/quiz-index.js` + 505 thẻ ôn **không xuất hiện trong `CLAUDE.md` lẫn bất kỳ
ghi chú nào**. Nó sinh tự động từ `qa_cards()` ở `tools/build.py`, và nó là lý do luật câu đơn
phải áp vào `details.qa`.

## ⚠ Bài học lớn nhất: hai TRỤC bị lẫn thì báo cáo thành sai

Ngày 07/09 người dùng bác một phần báo cáo: *"có mấy cái vẫn còn ver cũ thậm chí có cả mấy bài bạn
bảo sửa xong rồi như dbscan, MLE & MAP, Supervised…"* · *"có vẻ do tôi bắt bạn làm quá nhiều việc
nên đang bị dở dang"*.

Nguyên nhân: đợt đó chỉ chạy **trục luật A→I** (chữ meta, đầu mục, tràn hình), **không** đụng tới
**trục luật 1** (mental model lên §01, gỡ *Tổng kết một hình*). Nói "đã sửa 75 bài" mà không nói
sửa theo trục nào thì người đọc hiểu là bài đã lên ver mới — sai.

> **Từ nay mọi báo cáo phải ghi rõ SỬA THEO TRỤC NÀO.** Bảy trục: build · audit luật 1 · soat 8
> phép · check.py · bbox thật · 490px · **trình bày** (bảng ở trên).

Bài học thứ hai cùng đợt: các số trong bảng phân loại A/B/C/D **tự cũ đi** — hai việc mở (#3 "51
bài còn *Tổng kết một hình*", #6 "8 bài ≥12 mục") hoá ra đã về **0** từ trước, chỉ là bảng chưa
đo lại. Đo lại từ file trước khi lập kế hoạch, đừng lập kế hoạch từ bảng cũ.

## Cách chọn việc

1. **Dài nhất làm trước** — theo phép 8 của `soat.py`, sắp theo số từ giảm dần.
2. **Trước khi viết bất kỳ khung nào, đọc hết bài đã viết CÙNG NHÓM.** Bốn lần liên tiếp việc thật
   hoá ra là **tách bài**, không phải viết mới — xem [[bai-hoc-soan-noi-dung]].
3. Rút được bài học chung thì **vá thẳng vào `tools/`**, không giữ riêng cho bài đang làm.
4. Viết bài mới ở kệ 06→10 thì lấy [[bai-mau-svm-knn]] làm khuôn ngay từ nháp đầu — rẻ hơn nhiều
   so với viết xong rồi sửa theo chuẩn.

## Việc còn lại

- 72 khung bài ở kệ 06→10, bắt đầu từ 06 Deep learning.
- 10 bài nợ luật 1 ở kệ 06→10 (các bài đã viết sẵn ở đó).
- Bảng chất lượng trình bày ở trên: note ở kệ 06→10 · 18 bài chữ/hình >250 · `<var>` ngoài ML ·
  30 bài ML còn khối Hỏi đáp dài.
- Nhóm B/B2 của bảng phân loại cũ (gist đúng chỗ, chỉ sai tên đầu mục): **đổi khi chạm từng bài**.
