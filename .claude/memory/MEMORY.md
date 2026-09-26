# Bộ nhớ của kho MazeAI

Chín ghi chú, hai thư mục, và **hai mươi bốn bài mẫu để mở ra xem** — 15/17 bài kệ Python:

- **`bai-mau/random-forest.html`** — bản người dùng chốt 2026-09-24 là *"bản tôi kì vọng"*, khung A (9 mục, model là vài cơ chế rời).
- **`bai-mau/xgboost.html`** · **`bai-mau/gradient-boosting.html`** · **`bai-mau/adaboost.html`** — ba bản chốt 2026-09-25, khung B (7–8 mục cắt theo thứ tự tính, model là một công thức chạy nhiều bước), hoạt hoạ **chạy một lần khi cuộn tới** thay vì lặp vô hạn. Tên mục gần trùng nhau, chỉ mục áp chót là riêng. Khung B giờ chỉ còn nhánh boosting — Naive Bayes đã chuyển sang khung C. **Không bản nào còn hình `infinite`.**
  **Mở bằng trình duyệt trước khi sửa bất kỳ bài nào.** Đọc luật không thay được việc nhìn nó.
- **`bai-mau/knn.html`** · **`bai-mau/logistic-regression.html`** · **`bai-mau/ridge-lasso-elasticnet.html`** · **`bai-mau/svm.html`** · **`bai-mau/naive-bayes.html`** — năm bản chốt 2026-09-25, **7–9 mục**, tất cả đều mở bằng `01 Mental model` và đóng bằng `Ưu và nhược` → `Hỏi đáp`, 4–6 hình mỗi bài, **không note, không `<pre>`, không `card.bad`, không `figcaption`, không lab**. Đây là bản cho thấy khuôn áp được cho cả model **không có bước huấn luyện** (KNN), **một họ ba biến thể** (Ridge/Lasso/Elastic Net) và model **xác suất** (Naive Bayes). Nội dung trong `content/` đúng bằng năm bản này. `linear-regression` cũng theo khung C và cũng đã chốt, nhưng **không có bản lưu ở đây** — đọc thẳng file trong `content/`.
- **`bai-mau/memory-model-mutability.html`** — bản chốt 2026-09-25, **bài mẫu đầu tiên ngoài kệ ML**
  và là thước của **hình động**: 8 mục, **13 hình, hình nào cũng động**, 0 note, 0 `<pre>`, 0 lab.
  Nguyên tắc gốc rút từ nó — *che hết chữ đi vẫn phải hiểu được* — cùng chín luật dựng hình,
  bảng bẫy kỹ thuật, kiểm bốn tầng và quy trình bảy bước nằm ở [[hinh-dong]].
- **`bai-mau/memory-management-gc.html`** — bản chốt 2026-09-25, cùng kệ Python và cùng thước
  hình động: **7 mục, 6 hình / 7 `<svg>`, hình nào cũng động**, 0 note, 0 `<pre>`, 0 lab.
  Nó là bản cho thấy luật *một hình một ý*: mục gộp `Reference cycle và cyclic GC` của bản trước
  đã **tách làm hai mục**, đúng cái mà [[hinh-dong]] dặn khi tiêu đề phải dùng chữ "và".
- **Năm bản chốt 2026-09-26, trọn nhóm `02-language-core`**: `scope-legb` · `data-model-dunder` ·
  `iterator-generator` · `decorator-context-manager` · `exception-handling` — **5–7 mục, hình nào
  cũng động**, 0 note, 0 `<pre>`, 0 lab. Cả nhóm bảy bài giờ cùng một thước; đây là **kệ đầu tiên
  ngoài ML có một nhóm trọn vẹn theo bản chốt**. Chúng mở ra một khác biệt so với bài mẫu ML:
  **`--clay` được dùng trong hình** làm màu ô trung tính — xem [[hinh-dong]] mục *Clay trong hình*.
- **Bốn bản chốt 2026-09-26, lượt hai**: `thread-process-gil` · `asyncio` · `dict-hash-table` ·
  `list-tuple-set` — **5–8 mục, hình nào cũng động** (26 `<svg>`), 0 note, 0 `<pre>`, 0 lab.
  `thread-process-gil` là bản **gộp**: nó ôm luôn `Context switch` + `Scheduling` của bài OS
  `process-thread-scheduling`, nên bài OS đó đã xoá — lý do chọn kệ Python làm chủ nằm ở
  [[trang-thai-kho]]. `asyncio` là bản có nhiều hình nhất của kệ Python (8 hình / 7 mục).
- **Bốn bản chốt 2026-09-26, lượt ba — đóng nốt 15/17 bài kệ Python**: `leetcode-toolkit` ·
  `oop-python` · `typing-dataclass` · `performance-profiling`. Kệ Python giờ **0 `lab.js`**.
  `performance-profiling` là bản **ít hình nhất** của khung D (2 hình / 5 mục) và vẫn được chốt —
  thêm bằng chứng cho luật *tỉ lệ chữ/hình không phải thước*. Một bẫy kỹ thuật lộ ra ở
  `typing-dataclass`: dấu `<` trần trong `<text>` của `<svg>` — xem [[trang-thai-kho]].
  Bản `leetcode-toolkit` giờ nằm ở **kệ DSA**, không phải kệ Python — lý do ở [[trang-thai-kho]].

- **`chuan/`** — luật viết bài, còn đúng mãi. Đọc hết trước khi sửa nội dung.
- **`nhat-ky/`** — trạng thái và bài học của việc đang làm.

Ranh giới với `CLAUDE.md`: file đó mô tả kho **đang như thế nào** (cấu trúc, cách build);
memory ghi **vì sao chọn cách đó** và **đang làm tới đâu**. Cùng một điều đừng viết ở cả hai chỗ.

## chuan/ — luật viết bài

| Ghi chú | Nội dung |
|---|---|
| [Bài mẫu — ba khuôn A/B/C](chuan/chuan-bai-mau.md) | **đọc đầu tiên, kèm mở file HTML ra xem.** Thước của cả kho, chốt 2026-09-24 và 2026-09-25 (**11 bản**). **Khung A** (Random forest) **9 mục** (không *Lỗi hay gặp*, không lab, không *Chọn khi nào* riêng) · **57 chữ/hình** · 0 note, 0 `<pre>` · hero có `ul.ledelist` ba gạch · tên mục = đúng chữ trên hình §01 · **hình động bằng keyframe trong `<style>` của từng `<svg>`**: chỉ `opacity`+`transform`, luôn bọc `prefers-reduced-motion:no-preference`, hiện dần rồi giữ tới mốc 87%, hình so sánh để tĩnh · `aria-label` kể trọn chuỗi động · **được tô nền mờ + viền màu** · chữ trong hình dùng một lớp `sv-d` · in đậm `<b>`, link là chữ cam · một bộ ví dụ chạy xuyên bài. **Khung B** (nhánh boosting) **7–8 mục cắt theo thứ tự tính**, loss tan vào mục 02–03, mục 06 là chỗ riêng của từng bài, bỏ hẳn mục khi model không có dạng đó, 92–140 chữ/hình (Naive Bayes 291 vẫn được chốt — thứ phải đếm là **mỗi mục một hình**, không phải tỉ lệ) · hoạt hoạ đổi sang `linear 1 forwards` + `IntersectionObserver` chạy một lượt khi cuộn tới, giữ ở mốc 100%. Chọn khuôn theo câu hỏi: vài cơ chế ghép lại hay một công thức nhiều bước? **Khung C** (sáu bài classical ML) **7–9 mục**, bộ xương cố định `01 Mental model` → `02 Công thức tổng quát` → vài mục mỗi mặt một mục → `Ưu và nhược` → `Hỏi đáp`; **bỏ hẳn mục *Lỗi hay gặp* và *Chọn khi nào***, cả hai tan vào bảng hai cột; một `<figure>` một `<svg>`; **tỉ lệ chữ/hình bỏ hẳn** (201–362) vì mỗi hình có hoạt hoạ nhiều bước gánh trọn một mục. Dấu hiệu chọn khung C: đọc mục sau **không cần** nhớ mục trước. |
| [Hình động](chuan/hinh-dong.md) | **đọc cùng `bai-mau/memory-model-mutability.html`.** Nguyên tắc gốc: **che hết chữ đi vẫn phải hiểu được** · chín luật: một hình một ý (tiêu đề có chữ "và" thì tách đôi) · animation theo **thứ tự thực thi**, có badge "đang chạy" · phép toán **map vào data** bằng đường nối + khung khoanh · giá trị đổi từ từ, **viết dòng thời gian trước khi code** · màu nói lên quan hệ · **bớt đường nối**, để hành vi nói thay mũi tên · vẽ đúng cấu trúc thật, chỉ đóng khung thứ quan trọng · số liệu **sinh từ code**, nói thẳng khi yêu cầu sai sự thật · một lượt khi cuộn tới, không `infinite`. Kèm **bảng bẫy kỹ thuật** (`fly` quên bản tĩnh · `loop=True`+`window` · `window` cắt sớm · `str.replace` làm hỏng file), **kiểm bốn tầng** (số → hình học → bản tĩnh → bản động) và **quy trình bảy bước** |
| [Tối thiểu để hiểu](chuan/toi-thieu-de-hieu.md) | chín luật A→I về **nội dung**: không chữ meta trong bài · có cấu trúc dữ liệu thì vẽ đúng hình dạng nó (phép `circle+path` chỉ là sàng — ô chữ nhật **là ô bảng** thì vẫn đúng) · chỉ giữ mức tối thiểu · nội dung là chữ thì dùng khuôn HTML đừng vẽ SVG · **cả bài chạy trên đúng MỘT bộ ví dụ** · viết cho người MỚI · cắt thì cắt cả ở *Hỏi đáp*. Kèm quy trình review sáu phép |
| [Trình bày bài](chuan/trinh-bay-bai.md) | luật **trình bày**: ít chữ nhiều hình (mốc **57**, trên 100 là còn phải cắt) · **không dùng note** · câu đơn mỗi dòng một ý (áp **cả trong `details.qa`** vì nó sinh ra thẻ ôn) · **công thức dáng LaTeX** · ký hiệu dùng bảng tra `dl.defs` · **mỗi mục kể 2+ trường hợp thì mỗi trường hợp một ô hình** · **bài quá kĩ thì cắt CHỮ đừng cắt MỤC** · **không ví von** — bốn họ ẩn dụ bị cấm, soát **cả chữ trong `<svg>`** · in đậm bằng `<b>`, không `.hl`. Kèm khuôn `*-overview` và cách báo cáo cho người dùng — **thật ngắn, đừng kể tên class** |
| [Thuật ngữ](chuan/thuat-ngu.md) | phép **dịch ngược** để biết chữ nào giữ tiếng Anh · ba bẫy "nghe xuôi vẫn là dịch sai" · luật tách riêng theo từng kệ · **năm bề mặt** phải đồng bộ không thì hỏng tìm kiếm · thuật ngữ phải nằm trên hình và sống sót qua mọi lần rút gọn |
| [Khuôn .eq cho công thức](chuan/khuon-eq-cong-thuc.md) | vì sao chọn HTML thay KaTeX · dáng LaTeX phải phủ **cả ba chỗ**: `.eq` (display) · **`.mth`** (ký hiệu trong văn xuôi — đừng dùng `<code>`) · **`sv-m`** (công thức trong `<svg>`) · ranh giới `<code>` vs `.mth` · quy ước vẽ đường cong bằng SVG |
| [Công cụ và cách kiểm](chuan/cong-cu-va-cach-kiem.md) | `soat.py` 8 phép · `svgkit` dùng chung đừng chép sang `/tmp` · **kiểm lại chính cái thước** · `check.py` là sàng, `getBBox` là trọng tài · bảy chỗ máy KHÔNG bắt được · **hình động máy không kiểm được — phải tắt hoạt hoạ xem lại và xem trọn một chu kỳ** · bẫy khi sửa `.eq` · chạy bao nhiêu vòng cho mỗi loại sửa |

## nhat-ky/ — đang làm tới đâu

| Ghi chú | Nội dung |
|---|---|
| [Trạng thái kho](nhat-ky/trang-thai-kho.md) | **mốc số liệu duy nhất.** 200 bài · 72 khung còn lại ở kệ 06→10 · kệ 01→05 sạch cả sáu trục **luật**. Kèm **trục thứ bảy — chất lượng trình bày**. Và luật **mọi báo cáo phải ghi rõ sửa theo TRỤC NÀO** |
| [Số cho 4 bài classical ML](nhat-ky/so-classical-ml.md) | bốn bài đã có **bản chốt trong `bai-mau/`** — số đọc thẳng từ đó, đừng chép ra ghi chú. Chỉ giữ lý do **ba bài phải đổi bộ ví dụ** thay vì dùng sáu khách A–F |
| [Bài học soạn nội dung](nhat-ky/bai-hoc-soan-noi-dung.md) | bẫy lặp bốn lần: việc thật là **tách bài** chứ không phải viết mới · bốn lỗi khiến người đọc không hiểu · hình dạng bản đồ phải tương phản với bài anh em |

## Cách dùng

**Đọc** — đầu phiên đọc file này; mở hết `chuan/` **và mở các file trong `bai-mau/`** khi sắp
sửa nội dung.

**Ghi** — đáng ghi là: phản hồi của người dùng về *cách làm việc* (kèm lý do), quyết định về nội
dung/lộ trình không suy ra được từ code, trạng thái công việc dài hơi. **Không ghi** thứ đã có
trong `CLAUDE.md`, `TAXONOMY.md`, cây thư mục hay lịch sử git — **và không ghi thứ đọc ra được từ
chính bài mẫu**. Bài mẫu là bản gốc; ghi chú chỉ nói *vì sao*.

**Giữ gọn.** Chín file là mức trần — bộ nhớ phình ra thì không ai đọc hết, và luật trùng nhau ở hai
file thì sẽ lệch nhau. Trước khi tạo file mới, tìm chỗ đã có: **thêm một dòng vào bảng có sẵn tốt
hơn viết một mục mới**. Số liệu chỉ khai ở [[trang-thai-kho]] và [[chuan-bai-mau]], đừng rải ra các
file luật. Ghi chú sai thì **xoá**, đừng để lại kèm đính chính — 2026-09-24 đã xoá cả ghi chú
`bai-mau-svm-knn` vì bài mẫu mới thay hẳn nó.

Frontmatter mỗi file: `name` · `description` · `metadata.type` (`feedback`/`project`/`reference`) ·
`updated: YYYY-MM-DD`. Loại `feedback` phải có **Vì sao** và **Áp dụng thế nào**. Ngày viết tuyệt
đối. Nối sang ghi chú khác bằng `[[tên-slug]]`.
