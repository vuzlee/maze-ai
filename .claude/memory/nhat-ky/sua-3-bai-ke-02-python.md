---
name: sua-3-bai-ke-02-python
description: "2026-09-05 viết lại dict-hash-table (rồi rút gọn về mức phỏng vấn), iterator-generator, memory-model-mutability theo khuôn một bản đồ của memory-management-gc; kèm cách đo để chọn bài nào cần sửa"
metadata:
  type: project
updated: 2026-09-05
---

Người dùng nghiệm thu bài [[sua-bai-memory-management-gc]] rồi giao tiếp: *"đọc memory và tham
khảo Memory management & GC để update lại các bài khó hiểu chưa đạt chất lượng nhé. cấu trúc là
mental model trước."* Chọn phạm vi: ba bài còn lại của kệ 02-python.

## Cách chọn bài nào cần sửa — đo, đừng đoán

Quét cả kho bằng một script đếm bốn số trên mỗi bài: **chữ/hình · số `<pre>` ngoài `details.deep`
· số mục · bullet trung bình**. Bài tệ lộ ra ngay: `dict-hash-table` có **23 mục, 16 khối code,
4 hình** — tức là một tài liệu tham khảo chứ không phải bài học. Chỉ số đắt nhất là **`<pre>` ngoài
`details.deep`**: nó gần như luôn đồng nghĩa với "mục này đang giảng bằng code thay vì bằng hình".

Sau khi sửa, ba bài về đúng vùng của bài mẫu:

| Bài | trước | sau |
|---|---|---|
| dict-hash-table | 23 mục · 4 hình · 16 pre | 12 mục · 10 hình · 2 pre (đều trong `deep`) |
| iterator-generator | — | 10 mục · 8 hình · 0 pre |
| memory-model-mutability | — | 10 mục · 8 hình · 0 pre |

## Khuôn đã dùng lại nguyên vẹn

Mỗi bài có **bản đồ riêng của nó**, vẽ lại nguyên xi ở mọi hình, mỗi mục sáng đúng một ô. Bản đồ
của `dict-hash-table`: *phép tính ra chỗ* ở trên, ba thứ chống đỡ ở dưới (trùng ô · vết xoá ·
nhân đôi). Dàn ý 12 mục là hệ quả trực tiếp — không nghĩ dàn ý trước.

Quy trình ba chặng dùng lại được y nguyên cho cả ba bài, đáng giữ:

1. `frame.py` (bản đồ) + `gen.py` → `figs.json`
2. `check.py` — soát hình học: đè nhau, tràn `viewBox`
3. `shot.py` (hình 2×) + `page.py` (cả trang, 1180px và 490px) → soi mắt

Chặng 3 vẫn liên tục bắt lỗi mà chặng 2 không thấy được, vì đó là lỗi **nghĩa** chứ không phải
toạ độ: nhãn `x in c` viết tắt tới mức khó hiểu, `figcaption` nói "năm ô dưới bản đồ" trong khi
đó là năm dòng ở panel phải. Xem [[sua-bai-memory-management-gc]].

## Luật mới rút ra

**JetBrains Mono làm hỏng dấu tiếng Việt.** `số` hiện thành `sô´`, `vùng` thành `vùng` lệch dấu.
Nghĩa là hai class `sv-l` và `sv-h` **chỉ được dùng cho chữ không dấu** — tên biến, số, nhãn hoa
tiếng Anh. Nhãn nào có dấu phải chuyển sang `sv-d` hoặc `sv-t` (Be Vietnam Pro). Đây là lỗi im
lặng: markup đúng hoàn toàn, chỉ hình mới lộ.

**`<h2>` không được chứa `<code>`.** `app.js` dựng mục lục bằng `textContent` của `.sh h2`, nên
thẻ markup rơi thẳng vào sidebar. Tiêu đề mục 09 phải viết `__hash__ &amp; __eq__` dạng chữ trơn.

**Script sinh nội dung: đừng dùng `str.format`.** Bài nào cũng có dấu ngoặc nhọn thật trong văn
(`d = {}`, `{k: [] for k in keys}`, `@dataclass(frozen=True)`) nên `.format()` nổ. Thay bằng
`re.sub(r'\{(f\d\d)\}', ...)` chỉ thay đúng placeholder hình.

## Chỗ trùng đã dọn luôn

Phần immutable/mutable trong `dict-hash-table` trùng với bài chủ
[memory-model-mutability](../../../content/02-python/02-language-core/memory-model-mutability/index.html).
Gập thành một `details.deep` ba câu + link, theo đúng luật *một khái niệm, một chủ* trong
`CLAUDE.md`. Link chéo đặt ở `<footer>`.

## Lượt hai: người dùng bắt lỗi tương phản

*"MUTABLE quyết định việc thứ hai / immutable thì chỉ còn cách tạo object mới — cái thì đậm cái
thì mờ, nhưng vai trò ngang nhau, hãy lưu ý cả UX/UI nữa nhé, nhìn cho rõ, ngắn gọn xúc tích."*

Đúng, và nó lộ ra **hai** lỗi khác nhau:

1. **Trong một dòng**, tiêu đề ý và câu giải thích của nó là một cặp — nhưng tôi vẽ tiêu đề bằng
   màu ngữ nghĩa còn câu dưới bằng `--faint`, thành ra dòng nào cũng trông "nửa đậm nửa mờ".
   Chữa: câu dưới dùng `--dim`.
2. **Cả kho**, mặc định của `.sv-d`/`.sv-h` là `--faint` — không đạt tương phản AA ở cỡ 10,5px và
   9,5px. Đổi mặc định sang `--muted` trong `style.css`, ăn sang **toàn bộ 979 nhãn** đang dùng
   mặc định ở mọi bài, không riêng ba bài này. `--faint` giữ lại đúng vai trò của nó: chữ **cố ý
   phải mờ**, tức ô đã bị xám hoá trong bản đồ.

Chữ trong ô đã xám cũng nâng từ `--faint` lên `--muted` ở cả ba `frame.py` — bản đồ lặp lại ở mọi
mục thì phần xám vẫn phải **đọc được**, nó chỉ cần *lùi lại*, không phải biến mất.

Luật đã ghi vào [[chuan-bai-mau]]: độ sáng chỉ dành cho **thứ bậc thật**; hai thứ ngang vai thì
cùng độ đậm.

## Lượt ba: rút `dict-hash-table` về mức phỏng vấn

*"hơi chi tiết quá, chỉ cần core mà phỏng vấn bigtech hay hỏi… vẫn phải có Collision & probe
sequence nhé đừng bỏ 2 cái core này."* Giữ nguyên 12 mục và cả dòng chảy — chỉ **hạ mức trừu
tượng xuống một bậc** ở chỗ nói về bit. Luật rút ra đã ghi vào [[chuan-bai-mau]].

Cụ thể đã đổi: `hash & mask` → `hash % size` ở mọi hình và mọi câu (nhắc `& (size-1)` đúng một
lần, như một mẹo cài đặt); mục 02 bỏ hẳn phần "chỉ bit thấp quyết định ô đầu" + demo `rail-mask`,
thay bằng "nén khoảng lớn xuống ít chỗ nên trùng là tất yếu"; hình mục 04 bỏ công thức perturb ở
vị trí trung tâm, thay bằng **hai điều kiện của một probe sequence** (xác định · đi hết bảng) —
công thức tụt xuống một dòng phụ và một `details.deep` viết ở mức "biết tên là đủ".

Lab từ ba phần còn một (bỏ demo ba hash cùng ô đầu và mô phỏng clustering linear-vs-Python,
`lab.js` 117 → 68 dòng). Chữ gần như không đổi (3823 → 3729 từ) — **rút độ sâu không phải rút độ
dài**; phần cắt được bù lại bằng lý do ở mức cao hơn.

Cũng lượt này: bỏ nốt khối tiếng Anh trong hình gist của [[sua-bai-memory-management-gc]] và sửa
`fig03` của bài đó tràn ngang 862>860 — đó là chỗ người dùng thấy "chữ overlap hình".

## Lượt bốn: sửa *ngữ pháp hình* của `dict-hash-table`

Người dùng review hình mục 02 rồi đưa bốn yêu cầu cùng lúc — cả bốn đã thành luật chung ở
[[chuan-bai-mau]], đây chỉ ghi việc đã làm ở bài này:

1. **Ô là kết quả, mũi tên là hành động.** Hình 02 dựng lại: ba ô `key` / `hash value` /
   `slot index` nối bằng hai mũi tên có nhãn `hash(key)` và `% size` (hàm `arr_r_lbl` mới trong
   `frame.py`). Ô rộng 124, khe 64 để nhãn mũi tên nằm gọn.
2. **Gọi đúng thuật ngữ.** "ô" → `slot` / `slot index` ở toàn bộ 10 hình, văn xuôi và `lab.js`.
   Chữ "ô" chỉ còn nghĩa **ô của bản đồ mental model** — đúng một nghĩa, không lẫn nữa.
3. **Dòng kết luận không được nhỏ và mờ.** Thêm class `.sv-s` vào `style.css`; mọi dòng thứ hai
   trong `frame.py` và trong hàm `rows()` của `gen.py` chuyển từ `sv-d` sang `sv-s`.
4. **CPython chỉ cần ý.** Công thức `i = (i*5 + perturb + 1) % size` biến mất khỏi hình 04, khỏi
   deep dive và khỏi Hỏi đáp; thay bằng "trộn phần cao của hash vào bước nhảy" + hai vai trò.
   Cũng bỏ nốt "một phép AND" và "lũy thừa 2" còn sót trong Hỏi đáp.

Tên nhãn: đổi hết dạng hô khẩu hiệu sang cặp *nguyên nhân → cách chữa* viết chữ thường. Bảy tiêu
đề panel cũng viết lại (`BA THỨ CHỐNG ĐỠ NÓ` → `CẢ BÀI TRONG NĂM DÒNG`, v.v.).

Vòng kiểm: đăng ký `sv-s` vào bảng `W` của script kiểm (thiếu là `KeyError`, không cảnh báo) →
28 lỗi hình học → sửa còn 0 → `body.py` → `build.py` sạch → chụp 1180px và 490px soát mắt.
