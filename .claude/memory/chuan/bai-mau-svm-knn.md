---
name: bai-mau-svm-knn
description: "Hai bài mẫu của kệ ML — svm và knn: khung xương 8 mục, số đo, mười chi tiết đọc kĩ mới thấy, và ba chỗ knn còn thua svm"
metadata:
  type: feedback
updated: 2026-09-08
---

Đổi tên từ `bai-ml-chuan-svm` ngày 2026-09-08: người dùng chốt **cả hai** bài
`05-classical-ml/svm` và `05-classical-ml/knn` là bài mẫu, đọc kĩ cả hai mới ra đủ luật.

Nó bổ sung chứ không thay [[chuan-bai-mau]] (random-forest): random-forest là thước cho **cả kho**
(mật độ hình, độ dài bullet, độ sâu), svm/knn là thước riêng cho **kệ ML** — nơi bài nào cũng có
công thức và cũng là một model có ưu nhược.

## Số đo — hai bài gần trùng nhau, đó chính là bằng chứng có chuẩn

| | svm | knn | ghi chú |
|---|---|---|---|
| chữ | 1.724 | 1.717 | trung vị kệ ML 1.789 — **không phải ngắn nhất, là không lặp** |
| mục | 8 | 8 | cả hai đúng 8 |
| hình (kể `.eq`, `.axis`) | 16 | 11 | |
| chữ/hình | **108** | 156 | mốc cả kho 123 (random-forest) |
| `<svg>` | 6 | 4 | |
| `.eq` | 4 | 2 | |
| `.note` | **0** | **0** | ← không phải "ít", là **không có** |
| `<pre>` | **0** | **0** | |
| `.card.bad` ở *Lỗi hay gặp* | 6 | 6 | |
| `details.qa` | 5 | 4 | |
| đoạn >33 từ ở mặt bài | 0 | 0 | |

## Khung xương 8 mục — dùng lại được cho mọi bài model

```
01  Mental model          p.key + figure.gist nhiều ô + ul.why
02  ┐
03  ├ 2–4 mục cơ chế      mỗi mục: p.key → hình → (dl.defs) → .eq → ul.why
04  ┘                      tên mục là danh từ thuật ngữ, không phải câu
05  Loss function         ← mục CỐ ĐỊNH, kể cả khi model không có loss thật
06  Ưu và nhược           bảng 3 cột Mặt|Ưu|Nhược + ul.why đúng ba gạch
07  Lỗi hay gặp           6 thẻ .card.bad, mỗi thẻ 1–2 câu
08  Hỏi đáp               4–5 câu
```

**Mục *Loss function* vẫn phải có kể cả khi model không tối ưu gì.** knn §05 là chỗ hay nhất của
bài: nó không né câu hỏi, nó **trả lời rằng loss ở đây chỉ là cách viết lại quy tắc gộp k
neighbor lúc dự đoán**, rồi cho đúng một công thức `argmin` với chỗ trống `L` — thay `L` bằng
`[c ≠ y]` ra `mode`, bằng `(c − y)²` ra `mean`, bằng `|c − y|` ra `median`. Ba dòng, ba cách gộp,
một khung. Trả lời "model này không có loss" rồi bỏ trống mục là bỏ mất chỗ đắt nhất.

## Mười chi tiết chỉ thấy khi đọc kĩ — và vì sao người dùng bắt từng cái

**1 · Mỗi mục có đúng một `p.key`, và trong đó có đúng một `<em>`.** `<em>` là câu sẽ sống sót
nếu xoá hết phần còn lại của mục. Đó là lý do `p.key` ngắn: svm dài nhất 23 từ, knn 26.
*Câu chốt không phải tóm tắt mục — nó là mục, thu về một câu.*

**2 · `p.key` được dùng LẠI giữa mục.** svm §05 có **hai** `p.key`: một mở mục (nâng chiều), một
ở giữa mục (kernel trick bỏ bước tính toạ độ). Mục có hai bước ý thì hai câu chốt, không phải một
câu chốt gánh cả hai.

**3 · Bảng ký hiệu `dl.defs` đặt SAU khối `.eq`.** Đọc công thức trước, tra ký hiệu sau — người
đọc nhìn công thức là biết mình đang thiếu chữ nào, rồi mới tra. Đặt trước thì thành bắt học
thuộc ký hiệu trước khi biết dùng làm gì. `dd` viết như câu trả lời thường: `ξ` → *"một điểm lấn
vào sâu bao nhiêu"*, `C` → *"lấn 1 đơn vị thì bị phạt nặng bao nhiêu"*. Không có chữ "tham số
điều chỉnh mức độ…" nào cả.

**4 · Mấy trường hợp thì mấy panel, trong CÙNG một `<svg>`, trên CÙNG bộ ví dụ.**
svm §03: hard margin | soft margin, một tập điểm. knn §03: bốn ô cho bốn thước đo, **cùng đúng
hai điểm a và b** — đường thẳng (Euclidean), đường bậc thang (Manhattan), hai tia kèm cung θ
(cosine), hai hàng bit tô đỏ chỗ khác (Hamming). So bốn ô cạnh nhau mới thấy điều cần thấy:
*cùng hai điểm, bốn con số khác nhau*. Vẽ bốn hình rời thì mất hẳn ý đó.

**5 · Tiêu đề mỗi ô nằm TRONG hình.** `text.sv-hv` / `sv-t`, không phải câu dẫn bên dưới. Bên
dưới chỉ còn `figcaption`, và figcaption nói **cái cần nhận ra**, không mô tả cái đang vẽ:
knn §04 *"Ô trên: thêm một chiều thì số điểm cần để phủ kín nhân lên mười lần. Ô dưới: hệ quả đo
được"*. Không phải "hình vẽ ba trường hợp một, hai, ba chiều".

**6 · Khái niệm con nào có công thức thì có một dòng `.eq` riêng.** knn §03 trước đây là bốn dòng
`.stack` toàn chữ, không công thức nào — nay bốn dòng `.eq`: `d_L2 · d_L1 · d_cos · d_H`, mỗi
dòng một `<em>` nói **dùng khi nào**. Đừng gộp bốn thước đo vào một đoạn văn rồi nhét công thức
vào `<code>`.

**7 · `<em>` trong `.eq` giải nghĩa từng NỬA công thức, không giải nghĩa cả dòng.**
svm §04: `‖w‖²/2` mang `<em>margin rộng — chính là L2</em>`, `C·Σ max(0, 1−y·F(x))` mang
`<em>hinge loss — phạt điểm chưa qua margin</em>`. Người đọc chỉ vào được nửa mình chưa hiểu.

**8 · Bảng chỉ dùng cho thứ thật sự là bảng tra.** svm có 3 bảng: tham số C/gamma, ba kernel,
Ưu và nhược. Không bảng nào là văn xuôi bị kẻ ô. Test: cột thứ hai có đọc dọc được không.

**9 · Điểm đánh dấu trong hình cùng HÌNH DẠNG với điểm dữ liệu, khác nhau bằng VÂN.**
knn §05 dùng `<pattern>` sọc chéo cho *điểm cần dự đoán* — vẫn là hình tròn như mọi điểm khác.
Đổi sang hình vuông thì người đọc hiểu nhầm là loại dữ liệu khác.

**10 · `figcaption` của `figure.gist` ở §01 nói bài này gồm mấy phần, bằng chữ của chính bài.**
svm: *"Bốn ô là toàn bộ bài"* — và bốn ô ghi ① Margin lớn nhất ② Support vector ③ Hard margin và
soft margin ④ Kernel trick, đúng tên bốn mục sau. knn: *"ba lựa chọn ②③④ chính là model — và cả
ba đều hỏng âm thầm: sai thì kết quả vẫn ra, chỉ là sai"*. Câu thứ hai là **cảnh báo**, không phải
mục lục — đó là chỗ knn hay hơn svm.

## Ba chỗ knn còn thua svm — sửa knn thì lấy svm làm đích

1. **`lede` 45 từ** (svm 33). Quá mốc 33 của luật câu đơn, và nó là câu đầu tiên người đọc gặp.
2. **Không có `dl.defs`** dù §05 có `argmin`, `N_k`, `y_j`, `c`. Chú thích đang nằm ở hai gạch
   `ul.why` bên dưới — đúng nội dung, sai khuôn, tra chậm hơn.
3. **156 chữ/hình so với 108.** Chênh nằm ở §02 *Chọn k* — mục duy nhất của cả hai bài **không có
   `<svg>` nào**, chỉ có `.axis`.

## Chỗ svm hơn CẢ KHO, không riêng knn: mục Hỏi đáp

svm là bài **duy nhất trong 128 bài đã viết** áp luật câu đơn vào tận *Hỏi đáp*:
**5 câu hỏi · 21 đoạn · đoạn dài nhất 32 từ.** Mọi bài khác trả lời bằng **một khối liền** —
knn 4 câu / 4 đoạn / dài nhất 118 từ; cả kệ ML còn 30 bài như vậy; ab-testing 108, statistics 122,
train-val-test-cv 126.

**Vì sao đây là chuẩn chứ không phải chuyện thẩm mỹ.** `tools/build.py` bóc thẳng `details.qa`
thành thẻ ôn ở `assets/quiz-index.js` (505 thẻ từ 109 mục). Một câu trả lời 118 từ liền khối là
một mặt sau thẻ không đọc nổi. Cắt thành 4–5 đoạn ngắn thì cùng nội dung đó ôn được.

## Bẫy kỹ thuật đã dính, đừng dính lại

- Sửa `.eq .t>span:first-child` sang `display:inline-flex` thì flex **cắt sạch dấu cách hai đầu
  mỗi text node** — "từ <var>a</var> tới" hiện thành "từatới". Giữ `display:inline`; phân số vẫn
  gióng giữa nhờ `vertical-align` của `.frac`.
- Regex bọc `<var>` phải chạy **quanh thẻ**, không xuyên qua: chạy lần hai trên file đã chuyển ra
  `<var><var>x</var></var>`.
- Chèn khối mới bằng `s.index('  </div>\n', …)` **rơi vào khối `.eq` của mục khác** — luôn neo
  bằng một chuỗi dài duy nhất của đúng mục đang sửa.
- Dấu căn cần vinculum: `.eq .ov{border-top:1px solid currentColor}`. Lớp màu chỉ có `.t.b` `.t.p`
  `.t.g` `.t.r` — **không có `.t.a`**, viết nhầm thì mất màu.
- Cắt hình ra khỏi một mục có thể **làm vỡ phép 8 của `soat.py`** (đếm theo mục thiếu hình).
  Chữa bằng cách thay khối bị cắt bằng một `.bars` gọn, không phải trả lại đoạn văn cũ.
- Muốn nhìn nhiều khối `.eq` cùng lúc thì sinh trang gộp ở `/tmp` **nhúng `assets/style.css` đọc
  lại từ đĩa** — trang gộp cũ giữ CSS cũ, sửa CSS xong mà không sinh lại thì ảnh chụp nói dối.

Luật trình bày bao trùm ở [[trinh-bay-bai]]; luật thuật ngữ ở [[thuat-ngu]]; số liệu ở
[[trang-thai-kho]].
