---
name: khuon-eq-cong-thuc
description: "Vì sao MazeAI chọn khuôn .eq thay vì KaTeX cho công thức toán, ranh giới .eq vs <pre>, và quy ước vẽ đường cong bằng SVG"
metadata:
  type: feedback
updated: 2026-09-03
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
Giới hạn đã biết: `.eq` không làm được tích phân, ma trận, phân số lồng. Chưa gặp nhu cầu đó;
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
