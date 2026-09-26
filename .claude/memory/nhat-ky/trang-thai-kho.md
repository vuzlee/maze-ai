---
name: trang-thai-kho
description: "Trạng thái toàn kho — mốc số liệu duy nhất, sáu trục nghiệm thu, chất lượng trình bày từng kệ, việc còn lại"
metadata:
  type: project
updated: 2026-09-26
---

**Đây là mốc duy nhất.** Mọi con số rời rạc trong các phiên trước đã lệch; đo lại từ file bằng
`python3 tools/build.py`, đếm cờ `skeleton` trong `assets/catalog.js`, và `python3 tools/soat.py`.

## Tiến độ nội dung (2026-09-08)

| Kệ | Đã viết / tổng |
|---|---|
| 01 DSA · 02 Python · 03 CS · 04 Database | **24 · 16 · 13** · 23 — **xong hết** (2026-09-26: bài scheduling gộp vào kệ Python, `leetcode-toolkit` chuyển sang kệ DSA) |
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

### Hình động — mới, đã lan ra cả nhóm tree models

Keyframe trong `<style>` của từng `<svg>` ([[chuan-bai-mau]]) hiện có ở **bảy bài**: cả nhóm
`06-tree-models` (`decision-tree` · `random-forest` · `adaboost` · `gradient-boosting` ·
`xgboost` · `lightgbm`) và `naive-bayes` bên `05-classical-ml` — bài đầu tiên ra khỏi nhóm tree
models. Bốn bài `xgboost` · `gradient-boosting` · `adaboost` · `naive-bayes` (2026-09-25, đều là
bài mẫu) dùng cách chạy mới — một lượt khi cuộn tới, không lặp vô hạn — và đó là cách nên theo từ
nay. Bản chốt mới của `naive-bayes` **không còn hình `infinite`** nào; cả kho giờ sạch `infinite`.
**2026-09-25 thêm sáu bài nữa**: `knn` · `logistic-regression` · `ridge-lasso-elasticnet` · `svm` ·
`linear-regression` · `naive-bayes` (khung C, đều là bài mẫu). Cả `05-classical-ml` giờ còn đúng
`classical-models-overview` là chưa có hình động.
**2026-09-25, bài mẫu đầu tiên ra khỏi kệ ML**: `memory-model-mutability` (kệ 02 Python) — 8 mục,
**13 hình động**, và là bản người dùng chốt làm thước cho *cách vẽ hình động* nói chung, không chỉ
cho một khung bài. Luật rút từ nó ở [[hinh-dong]] (tách khỏi [[chuan-bai-mau]] cùng ngày).
Nó cũng là bài đầu tiên **bỏ lab** ở kệ Python.
Cùng ngày, bài kế bên `memory-management-gc` cũng lên bản chốt (7 mục · 6 hình động) — nhóm
`02-language-core` giờ có hai bài theo thước hình động.
**2026-09-26 đóng trọn nhóm**: thêm `scope-legb` · `data-model-dunder` · `iterator-generator` ·
`decorator-context-manager` · `exception-handling`. Cả bảy bài của `02-language-core` giờ là
bài mẫu, **29 `<svg>` đều động**, và nhóm này là **nhóm đầu tiên ngoài kệ ML sạch trọn vẹn**.
`iterator-generator` là bài thứ hai của kệ Python bỏ lab; kệ Python giờ còn `leetcode-toolkit`
là chỗ duy nhất còn `lab.js` trong nhóm đã chạm.

**2026-09-26, lượt hai — gộp bài GIL và bài scheduling làm một.** Thêm bốn bài mẫu
`thread-process-gil` · `asyncio` · `dict-hash-table` · `list-tuple-set`; kệ Python giờ **sạch trọn
ba nhóm** `02-language-core` + `03-builtin-structures` + `04-concurrency`.

Bản chốt của `thread-process-gil` **ôm luôn hai mục `Context switch` và `Scheduling`** của bài
`03-cs-fundamentals/02-os/process-thread-scheduling`, nên bài OS đó đã **xoá**. Vì sao giữ bản
Python chứ không giữ bản OS: một khái niệm một chủ, và chủ phải là kệ nó đạt độ sâu tự nhiên nhất —
bản Python đi từ *core → scheduler → process/thread → GIL* rồi trả lời được câu *"chờ hay tính"*
bằng bảng bốn mô hình, tức là context switch ở đó **có chỗ dùng**; ở kệ OS nó chỉ là một mục rời.
Kệ CS không mất gì: `os-overview` vẫn giữ bản đồ bốn ô và trỏ sang bài Python cho ô ① + ③,
`memory-virtual-paging` và `lock-deadlock-race` đổi link theo. **Thứ mất thật** là mục
`Trạng thái tiến trình` (New → Ready → Running → Terminated) — bản gộp không có; nếu sau này thấy
thiếu thì viết lại **trong** bài Python, đừng dựng lại bài OS.

**2026-09-26, lượt ba — đóng nốt mọi bài kỹ thuật của kệ Python.** Bốn bản cuối
`leetcode-toolkit` · `oop-python` · `typing-dataclass` · `performance-profiling`.
**15/17 bài** có `data-reviewed="1"` và **0 `lab.js` trong cả kệ**; hai bài chưa chốt là
`python-overview` và `language-core-overview` — đều là bài `*-overview`, theo khuôn riêng
(xem [[trinh-bay-bai]]) nên không nằm trong khung D.

Bản `typing-dataclass` có **một lỗi thật trong bài mẫu, không phải lỗi map**: hai chỗ viết
`<__main__.Plain object …>` bằng dấu `<` trần trong `<text>` của `<svg>` và trong `<li>` — HTML
vẫn hiện được nhưng XML parser (và mọi công cụ đọc SVG) vỡ ngay. Đã sửa thành `&lt;` ở cả
`content/` và bản lưu trong `bai-mau/`. **Bẫy để nhớ**: chữ trong hình có thể chứa ký tự cần
escape; `soat.py` và `audit.py` không bắt được — chỉ tầng 2 (parse SVG) bắt được, nên đừng bỏ tầng
đó khi map bài mẫu vào.

**2026-09-26, lượt bốn — `leetcode-toolkit` chuyển sang kệ DSA, và cả kệ DSA đánh `reviewed`.**
Bài đó là **bộ công cụ giải bài**, không phải bài giải thích cơ chế Python: nó dạy đọc `bisect`,
`Counter`, `deque`, `heapq` để viết lời giải ngắn hơn, tức là chủ phải là kệ **dùng** nó. Giờ nằm
ở `content/01-dsa/05-toolkit/`, link sang kệ Python đổi thành `../../../02-python/…`,
`dsa-overview` mục *Học theo thứ tự nào* nhắc nó là **thứ đi song song cả sáu chặng chứ không phải
chặng thứ bảy**, `python-overview` đổi mục 4 thành "Kỹ thuật" và trỏ ngược sang kệ DSA.

Cùng lượt này **23 bài DSA còn lại được đánh `data-reviewed="1"`** theo yêu cầu người dùng. Đây là
**kệ đầu tiên reviewed 24/24**. Lưu ý khi đọc số: `reviewed` ở kệ DSA nghĩa là *người dùng đã
nghiệm thu nội dung*, **không** nghĩa là bài đã theo khung D hay đã có hình động — khuôn của DSA
là khuôn riêng trong `CLAUDE.md` (lõi 1,5 phút + phần tra pattern). Đừng suy từ cờ này ra rằng
kệ DSA đã qua trục hình động.

Đây vẫn là việc lớn nhất còn lại của trục trình bày; làm dần, chạm bài nào thì thêm cho bài đó.
Từ nay bài nào thêm hình động thì theo [[hinh-dong]], không phải theo trí nhớ về bài mẫu ML.

`dl.defs` (bảng tra ký hiệu) đã thành chuẩn. `.hl` (in đậm cam) thì **bỏ** — 2026-09-24 chốt in
đậm bằng `<b>`, cam để dành cho link. Sáu bài khung C đã sạch theo bản chốt 2026-09-25;
chỗ còn lại nằm ngoài `05-classical-ml`, chạm bài nào thì đổi bài đó.

### Câu đơn trong `details.qa` — chỗ hổng lớn nhất còn lại

Mặt bài đã sạch (0 đoạn >33 từ). **Bên trong `details.qa` thì chưa**: mốc là bài mẫu
2026-09-24 — 5 câu, mỗi câu 4–5 `<p>`, đoạn dài nhất **20 từ**. Riêng kệ ML còn **29 bài** trả lời bằng một khối liền —
`train-val-test-cv` 126 từ · `statistics` 122 · `ab-testing` 108. Sáu bài khung C 2026-09-25 đã ra
khỏi danh sách này.
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
> phép · check.py · bbox thật · 490px · **trình bày** (bảng ở trên). Sửa hình động thì ghi rõ
> **tầng nào trong bốn tầng** ở [[hinh-dong]] đã chạy — "vẽ xong" mà chưa xem bản tĩnh là chưa xong.

Bài học thứ hai cùng đợt: các số trong bảng phân loại A/B/C/D **tự cũ đi** — hai việc mở (#3 "51
bài còn *Tổng kết một hình*", #6 "8 bài ≥12 mục") hoá ra đã về **0** từ trước, chỉ là bảng chưa
đo lại. Đo lại từ file trước khi lập kế hoạch, đừng lập kế hoạch từ bảng cũ.

## Cách chọn việc

1. **Dài nhất làm trước** — theo phép 8 của `soat.py`, sắp theo số từ giảm dần.
2. **Trước khi viết bất kỳ khung nào, đọc hết bài đã viết CÙNG NHÓM.** Bốn lần liên tiếp việc thật
   hoá ra là **tách bài**, không phải viết mới — xem [[bai-hoc-soan-noi-dung]].
3. Rút được bài học chung thì **vá thẳng vào `tools/`**, không giữ riêng cho bài đang làm.
4. Viết bài mới ở kệ 06→10 thì mở thẳng `bai-mau/random-forest.html` ra chép khung ngay từ nháp
   đầu ([[chuan-bai-mau]]) — rẻ hơn nhiều so với viết xong rồi sửa theo chuẩn.

## Việc còn lại

- 72 khung bài ở kệ 06→10, bắt đầu từ 06 Deep learning.
- 10 bài nợ luật 1 ở kệ 06→10 (các bài đã viết sẵn ở đó).
- Bảng chất lượng trình bày ở trên: note ở kệ 06→10 · 18 bài chữ/hình >250 · `<var>` ngoài ML ·
  30 bài ML còn khối Hỏi đáp dài.
- Nhóm B/B2 của bảng phân loại cũ (gist đúng chỗ, chỉ sai tên đầu mục): **đổi khi chạm từng bài**.
