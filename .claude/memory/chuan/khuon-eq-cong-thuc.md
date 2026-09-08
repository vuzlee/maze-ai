---
name: khuon-eq-cong-thuc
description: "Vì sao MazeAI chọn khuôn .eq thay vì KaTeX; dáng LaTeX phải phủ cả ba chỗ (.eq display · .mth trong văn xuôi · sv-m trong SVG); ranh giới .eq vs <pre> và <code> vs .mth; quy ước vẽ đường cong bằng SVG"
metadata:
  type: feedback
updated: 2026-09-08
---

Ngày 2026-09-03 chốt: công thức display trong kho dùng khuôn HTML `.eq` (khuôn thứ 9 trong
`kit.html`), **không** dùng KaTeX/MathJax.

**Vì sao không KaTeX.** Khảo sát 58 khối `<pre>` mang ký hiệu toán trong 25 bài đã viết: chỉ
~12 khối là display equation thật, còn lại là *dẫn giải* — chú thích tiếng Việt, bảng số, suy
luận nhiều dòng — thứ mà KaTeX vào là hỏng. Nhúng KaTeX offline tốn ~1.3MB (JS + font) để phục
vụ 12 khối, mà 46 khối kia vẫn phải ở `<pre>` → hai hệ thống song song, mỗi lần viết phải chọn.

Kiểm tiếp 22 khung chưa viết ở DL/Transformer/LLM có mục *Hàm mục tiêu*: hai bài đã viết mục đó
(xgboost, ridge-lasso) cho thấy khuôn thật của kho là **một công thức + chú thích từng ký hiệu**,
không phải toán nhiều tầng. `.eq` phủ đủ; KaTeX không thêm được gì.

**Lý do quyết định (không chỉ là thẩm mỹ).** ASCII math gióng lề bằng mắt thì sai — đo bài
bias–variance thấy vạch `└──┘` lệch 1–2 cột ở cả ba số hạng, vì `f̂` là hai codepoint nhưng một ô
hiển thị. `.eq` để trình duyệt gióng, lỗi đó biến mất theo cấu trúc chứ không phải sửa từng lần.

**Ranh giới.** `.eq` chỉ cho công thức đứng riêng. Dẫn giải vẫn là `<pre><code>` — đừng ép vào.
Giới hạn đã biết: `.eq` không làm được integral, matrix, nested fraction. Chưa gặp nhu cầu đó;
nếu gặp thì đó mới là lúc xét lại KaTeX.

Chi tiết cách dùng nằm ở mục 09 của `kit.html` và bảng khuôn trong `CLAUDE.md` — đừng chép lại
sang đây.

**Đã áp dụng xong (2026-09-03).** 14 khối trong 11 bài đã đổi sang `.eq`: bayes-theorem,
gradient-optimization (2), mle-map (2), expectation-variance (2), linear-regression,
logistic-regression, ridge-lasso-elasticnet, svm, xgboost, self-attention, backpropagation.
Số khối `<pre>` toán còn lại đều là dẫn giải, cố ý giữ nguyên. Đã soát bằng ảnh chụp ở 1200px.

## Đường cong thì vẽ SVG, không vẽ bằng ký tự

Cùng đợt, hình chữ U ở bài bias–variance đổi từ ASCII sang SVG. Lý do giống hệt trên: ký tự
không dựng được đường cong, chỉ gợi ý được nó.

Quy ước để mọi biểu đồ đường trong kho nhìn như một bộ:

- `viewBox="0 0 900 NNN"`, vùng vẽ **x từ 96 tới 730**, chừa lề phải cho nhãn đặt ở **x=744**.
- **Toạ độ các đường tính bằng công thức rồi in ra**, không gõ tay. Bài bias–variance dùng
  `bias(t)=0.92·exp(-3.4t)`, `var(t)=0.055·exp(3.0t)`, nhiễu `0.11`, rồi chuẩn hoá về khung.
  Tính thì ba đường mới thật sự cắt nhau đúng chỗ và đáy chữ U mới nằm đúng vị trí.
- Mỗi nhãn **một y riêng, tự đặt cho giãn ra** — để trình duyệt tự xếp là chúng dính vào nhau.
  Đã sửa ba lượt mới hết chồng chữ.
- Màu theo đúng bốn màu ngữ nghĩa, không dùng `--clay`.

Kiểm bằng `google-chrome --headless --screenshot` ở 1200px **và** ~500px. Lưu ý: chụp headless
ở 430px thì trang nào cũng bị cắt, kể cả trang chưa sửa — đó là tật của công cụ, không phải lỗi
bố cục.

## Dáng LaTeX — dựng bằng CSS, vẫn không nạp thư viện (2026-09-07)

Người dùng hỏi "công thức có theo kiểu toán học latex được không". Xét lại lần nữa và giữ
nguyên quyết định trên: cái đang thiếu là **dáng chữ**, không phải khả năng bố trí — `.eq`
bố trí được rồi. Nạp KaTeX (~330 KB + JS mỗi trang) chỉ để in `‖w‖²/2` một dòng là dao mổ
trâu, và nó phá đúng tính chất "mở bằng `file://` là chạy". MathML thì markup dài gấp 5.

Nên chỉ đổi dáng, theo đúng luật sắp chữ của TeX:

| Thứ | Cách viết | Luật |
|---|---|---|
| font | `--math` = Newsreader → Georgia → Times | Newsreader thiếu glyph `‖ √ Σ ∇`, hai font sau đỡ |
| biến | `<var>x</var>` | **biến nghiêng** |
| tên hàm | `<b class="fn">min</b>` | **hàm đứng**: min, max, log, exp, softmax |
| phân số | `<span class="frac"><i>tử</i><i>mẫu</i></span>` | vạch ngang thật, không phải dấu `/` |
| chú thích số hạng | `<em>` trong `.t` | giữ nguyên — thứ LaTeX không có |

Chữ số để nguyên, KHÔNG bọc `<var>` — TeX cũng in số đứng.

`.frac` canh `vertical-align:middle`, `.eq .line` canh `align-items:center`. Canh theo
baseline thì `max` treo lên trên còn phân số tụt xuống — đã dính đúng lỗi này một lượt.

Trong SVG không có `.frac`, phải vẽ tay: tử ở `y-7`, `<line>` ở `y`, mẫu ở `y+11`.

Bài mẫu: `05-classical-ml/svm` — xem [[bai-mau-svm-knn]].

## Dáng LaTeX phải phủ CẢ BA CHỖ, không chỉ `.eq` (2026-09-08)

Sau khi áp `.eq` cho cả kệ ML, người dùng vẫn báo *"công thức thiếu latex"* ở
`ridge-lasso-elasticnet`. Soát ra: `.eq` đúng dáng rồi, nhưng **hai chỗ còn lại thì không** —
và hai chỗ đó chiếm phần lớn số công thức người đọc gặp.

| Chỗ | Sai ở đâu | Đúng là |
|---|---|---|
| công thức display | — | `.eq` (đã có từ 2026-09-07) |
| ký hiệu **trong dòng văn xuôi** | `<code>λ</code>` — mono, nói *"đây là thứ gõ vào máy"* | `.mth` = `<span class="mth"><var>λ</var></span>` |
| công thức **trong `<svg>`** | `class="sv-h"` — mono CHỮ HOA giãn `letter-spacing` | `class="sv-m"`, biến bọc `<tspan class="v">` |

Ba chỗ giờ dùng chung `var(--math)` và chung luật TeX (**biến nghiêng, số và tên hàm đứng**),
nên cùng một công thức in ở ba chỗ trông như nhau.

**Ranh giới `<code>` vs `.mth`** — hỏi: *chuỗi này gõ vào máy được không?*
`reg_lambda`, `RidgeCV`, `C` (tên tham số sklearn) → `<code>`.
`λ`, `‖w‖²`, `Σ|w|`, `|w|` → `.mth`. Bài ridge trước đây có `<code>λ</code>` 17 lượt toàn kho.

**Bẫy**: `<tspan>` chỉ hợp lệ **trong SVG**. Sinh `.mth` bằng cùng một hàm với `sv-m` thì ra
`<span class="mth"><tspan class="v">λ</tspan></span>` giữa HTML — trình duyệt không nghiêng, và
`check.py` không bắt vì nó chỉ đọc `.svg`. Trong HTML là `<var>`, trong SVG là `<tspan class="v">`.

Phải đăng ký `sv-m` vào bảng `W` của `check.py` **và** `CW` của `base.py`, không thì `check.py`
dừng ngay với *"class chưa đăng ký bề rộng"*.

## Chú thích phải nằm chung một dòng — dựng bằng grid (2026-09-08)

`.eq .line` từng là flex. Flex canh giữa **từng số hạng một**, nên số hạng nào cao hơn
(có `.frac`) thì đẩy chú thích của nó xuống — mỗi chú thích một cao độ, nhìn như răng
cưa. Đổi sang **grid hai hàng cố định**: hàng 1 công thức, hàng 2 chú thích, `.eq .t`
là `display:contents` để hai con của nó rơi thẳng vào hai hàng đó.

Kèm theo: `.eq{overflow-x:auto}` cho công thức dài trên màn hẹp.

**Đừng đặt `display:inline-flex` cho `.eq .t>span:first-child`.** Flex biến mỗi text
node thành một item rồi **cắt sạch dấu cách hai đầu**: "từ <var>a</var> tới" hiện ra
"từatới". Để `display:inline`; `.frac` tự gióng giữa bằng `vertical-align:middle`.

Đã áp cho cả kệ ML: 106 công thức / 19 bài (2026-09-08).
