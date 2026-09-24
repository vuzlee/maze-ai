---
name: chuan-bai-mau
description: "Bài mẫu chuẩn của cả kho — bản Random forest người dùng chốt 2026-09-24, giữ nguyên ở bai-mau/random-forest.html. Khung 9 mục, 57 chữ/hình, hình động bằng keyframe, câu ngắn, ít mục, không lab không note"
metadata:
  type: feedback
updated: 2026-09-24
---

**Bản gốc nằm ngay cạnh ghi chú này: [`bai-mau/random-forest.html`](../bai-mau/random-forest.html)**
— mở bằng trình duyệt là thấy. Ghi chú này chỉ nói *vì sao* bản đó đúng; thứ gì đọc ra được từ
chính file thì đừng chép lại vào đây.

Người dùng 2026-09-24: *"đây mới là bản tôi kì vọng, tối giản, có trực quan hoá animation dễ hiểu
thân thiện, không phải tưởng tượng. các mục tối giản, hầu như hình, ít chữ, màu sắc cam và bold
những thứ quan trọng. đơn giản, không vẽ hình khó hiểu."*

Bản này **thay** mọi thước cũ (bản random-forest trước đó và cặp svm/knn). Luật cũ nào mâu thuẫn
với nó thì đã xoá khỏi bộ nhớ, không giữ kèm đính chính.

## Số đo — đây là mốc mới của cả kho

| | Bài mẫu | Luật |
|---|---|---|
| mục | **9** | 8–10, không hơn |
| chữ mặt bài | **914** | dưới 1.000 |
| hình | 16 (7 `<svg>`) | mục nào cũng có ít nhất một |
| **chữ/hình** | **57** | trên 100 là còn phải cắt chữ |
| chữ trong hình | 586 / 295 `<text>` | ~2 chữ một nhãn |
| bullet dài nhất | 19 từ | |
| đoạn trong *Hỏi đáp* dài nhất | 20 từ | mỗi đoạn một câu |
| `.note` · `<pre>` · `.card.bad` · lab | **0 · 0 · 0 · 0** | không phải "ít", là **không có** |

## Khung 9 mục

```
hero      eyebrow (kệ · nhóm) · h1 có đúng một <em> · lede MỘT câu
          + ul.ledelist ba gạch, mỗi gạch dưới 8 từ — "Ba thứ cần nhớ:"
01  Mental model     p.key + figure.gist (hình động, cả bài trong một khung) + ul.why một gạch
02 ┐
03 ├ 2–3 mục cơ chế  mỗi mục: p.key → một figure.scrollx → ul.why 1–2 gạch
04 ┘                 TÊN MỤC = đúng chữ ghi trên hình §01 (Bootstrap · Random features · Aggregating)
05  Loss function    mục CỐ ĐỊNH. Model không có loss riêng thì nói thẳng câu đó,
                     rồi cho công thức thật sự chi phối nó. .eq → dl.defs → hình
06  ┐ 1–2 mục "được  cái gì dùng được ngay: OOB score, feature importance
07  ┘ gì khi dùng"
08  Ưu và nhược      bảng 3 cột Mặt | Được gì | Mất gì (7 hàng) + ul.why: Chọn A khi… / Chọn B khi…
09  Hỏi đáp          5 câu, mỗi câu 4–5 <p>, mỗi <p> một câu đơn
```

**Không có mục *Lỗi hay gặp*, không có lab, không có *Chọn khi nào* riêng.** Lỗi hay gặp hoà vào
cột *Mất gì* của bảng §08 và vào *Hỏi đáp* (câu cuối của bài mẫu chính là một cái bẫy: *"bảng
importance nói cột ID quan trọng nhất, bạn nghĩ sao?"*). *Chọn khi nào* rút thành 3 gạch `ul.why`
ngay dưới bảng.

**Vì sao.** Mỗi mục thêm là một lần người ôn phải nhận diện lại bối cảnh. Chín mục là vừa một
lượt ôn; 13 mục như bản cũ thì phải đọc thành nhiều buổi, và ba mục cuối luôn là mục bị bỏ qua.

## Hình động — thứ mới nhất, và là lý do bản này hơn bản cũ

Mỗi `<svg>` mang một khối `<style>` của riêng nó, ngay bên trong. Không đụng `assets/style.css`,
không JavaScript, mở bằng `file://` vẫn chạy.

**Chỉ hoạt hoạ `opacity` và `transform`.** Không đổi màu, không đổi kích thước hộp, không
`stroke-dashoffset`. Hai thuộc tính đó trình duyệt chạy trên GPU nên không giật, và chúng đủ để kể
mọi thứ cần kể.

**Khuôn keyframe: hiện dần theo lượt, giữ nguyên rất lâu, rồi tắt và lặp lại.**

```css
@keyframes mm2{
  0%     {animation-timing-function:ease-in-out; opacity:0}
  18.000%{animation-timing-function:ease-in-out; opacity:0}   /* tới lượt mình */
  21.500%{animation-timing-function:ease-in-out; opacity:1}   /* hiện trong 3,5% chu kỳ */
  87.000%{animation-timing-function:ease-in-out; opacity:1}   /* đứng yên cho người đọc */
  94.000%{animation-timing-function:ease-in-out; opacity:0}
  100%   {animation-timing-function:ease-in-out; opacity:0}
}
@media (prefers-reduced-motion:no-preference){
  .mm2{animation:mm2 10s linear infinite}
}
```

Năm luật đi kèm, cái nào bỏ cũng hỏng:

1. **Toàn bộ khối `animation:` nằm trong `@media (prefers-reduced-motion:no-preference)`.** Ai tắt
   hiệu ứng thì thấy **hình tĩnh đầy đủ** — nên trạng thái mặc định của SVG phải là hình đã vẽ
   xong, hoạt hoạ chỉ *tiết lộ dần* thứ vốn đã ở đó. Đừng bao giờ để một chi tiết chỉ tồn tại
   trong keyframe.
2. **Một hình một chu kỳ, dùng chung cho mọi phần tử của hình đó.** Bài mẫu dùng 10s cho hình đơn
   giản (3 lượt), 11s cho hình vừa (8–35 lượt), 13,5s cho hình đông lượt nhất (42). Chọn theo số
   lượt, không theo cảm hứng — các lượt phải xong trước mốc 87%.
3. **Giữ ở mốc 87% rồi mới tắt.** Gần chín phần mười thời gian là hình đứng yên. Người đọc cần
   nhìn *kết quả*, không nhìn chuyển động; chuyển động chỉ để chỉ **thứ tự đọc**.
4. **Bước ra sau thì mốc hiện muộn hơn, cách nhau đều.** Bài mẫu: 3% · 18% · 36% cho ba bước của
   hình mở bài. Lượt nào cũng ramp đúng 3,5%.
5. **Hình so sánh thì để tĩnh.** Mục *Feature importance* của bài mẫu không có lấy một keyframe —
   nó là bảng đối chiếu hai cách chấm điểm, mắt phải so được hai cột cùng lúc. Hoạt hoạ một bảng
   so sánh là làm người đọc phải chờ.

Phần tử cần mọc lên hoặc phóng to thì bọc `class="sy"`, có sẵn hai dòng:

```css
.sy{transform-box:fill-box;transform-origin:50% 100%}
.sy *{vector-effect:non-scaling-stroke}
```

`transform-box:fill-box` để gốc toạ độ là chính phần tử, không phải gốc của cả `viewBox`;
`vector-effect:non-scaling-stroke` để nét không dày lên khi phóng.

**`aria-label` của mỗi `<svg>` là một câu kể trọn cả chuỗi động, kèm con số kết quả** — ví dụ
*"Một bảng dữ liệu rút thành ba mẫu, mỗi mẫu mọc một cây, ba cây bỏ phiếu cho khách A và hai trên
ba phiếu là không mua"*. Đây không phải chuyện trợ năng suông: `search-index.js` đọc chuỗi đó, nên
nội dung chỉ nằm trong hình vẫn tìm được.

## Vẽ cái gì, bằng gì

**Vẽ đúng vật, kích thước thật nhỏ.** Bài mẫu là một bảng dữ liệu nên nó vẽ **ô của bảng**:
170 `<rect>` cỡ 18×14 tới 34×28, mỗi ô một khách. Cây thì `<circle>` + `<line>`. Không có hộp
chữ nhật nào chỉ để chứa chữ.

**Bảng màu — được tô nền mờ, và đây là chỗ khác luật cũ.** Nền mờ + viền đậm là cách phân biệt
đúng, dùng thoải mái:

```html
<rect ... fill="rgba(var(--blue-a),.42)" stroke="var(--filled)" stroke-width="1.3"/>   <!-- dữ liệu -->
<rect ... fill="none" stroke="var(--probe)" stroke-width="1.8"/>                        <!-- vòng nhấn -->
```

Độ mờ dùng theo thang: `.42` đặc (thuộc về), `.30/.22/.20` vừa, `.18/.16/.14/.12` nền nhạt.
Bốn màu ngữ nghĩa giữ nguyên nghĩa cũ (xanh = dữ liệu, vàng = con trỏ/đáp án, đỏ = sai/không giảm
được, lục = đúng/kết quả). **`--clay` vẫn tuyệt đối không vào hình.**

**Chữ trong hình dùng đúng một lớp: `sv-d`.** Bài mẫu 294/295 nhãn là `sv-d`, đúng một nhãn
`sv-hv` làm tiêu đề. Thang ba cỡ chữ cũ (`sv-t`/`sv-s`/`sv-d`) làm hình rối mà không thêm nghĩa —
bỏ. Mỗi `<text>` ghi cả `fill="var(--…)"` **và** `style="fill:var(--…)"` để bản xuất một file
vẫn đúng màu.

## Câu chữ

- **`p.key` mỗi mục đúng một cái, 1–3 câu ngắn, đúng một `<em>`** — `<em>` là câu sống sót nếu
  xoá hết phần còn lại. Dài nhất của bài mẫu 24 từ, ngắn nhất 9.
- **`ul.why` chỉ 1–2 gạch**, là thứ hình *không* nói được: một con số (`37%`), một tên tham số
  (`max_features`: √p và p/3), một đường dẫn sang bài khác. Không phải tóm tắt lại hình.
- **In đậm `<b>` cho thuật ngữ và con số đáng nhớ** ngay trong văn xuôi: **out-of-bag**, **37%**,
  **√p**, **Bagging**, **Chọn random forest**. Bài mẫu dùng 18 lượt, không dùng `.hl`.
- **`<code>` chỉ cho chuỗi gõ vào máy** (`max_features`); ký hiệu toán trong dòng dùng `.mth`.
- **Link sang bài khác là chữ cam**, đứng cuối `ul.why` hoặc cuối bảng: *"So sánh đầy đủ: Tree
  models overview."* Không giảng lại bài kia lấy một câu.
- **Hỏi đáp mỗi ý một `<p>` một câu.** `tools/build.py` bóc mục này thành thẻ ôn, nên một khối
  dài là một mặt thẻ không đọc nổi.

## Một bộ ví dụ cho cả bài

Sáu khách **A–F** chạy suốt §01→§06: rút mẫu ở §02, chia cột ở §03, bỏ phiếu ở §04, chấm OOB ở
§06 — cùng sáu người đó. Người đọc không phải nhận diện lại dữ liệu ở mỗi mục, nên phần chú ý còn
rảnh để theo dõi **thứ đang đổi**.

§07 buộc phải đổi (600 khách mới đủ dữ liệu cho feature importance) và nó **nói thẳng ra** —
đó là `<figcaption>` duy nhất của cả bài: *"Đổi sang bộ 600 khách để có đủ dữ liệu."*
**`figcaption` chỉ dùng khi có thứ như thế cần nói**, không dùng để mô tả hình.

## Công thức

Hai khối `.eq` cho cả bài, đều theo khuôn: mỗi **nửa** công thức mang một `<em>` giải nghĩa riêng
nửa đó, `dl.defs` đặt **sau** (đọc công thức trước, tra ký hiệu sau), `dd` viết như câu trả lời
thường (`ρ` → *"các cây giống nhau tới mức nào"*, không phải "hệ số tương quan giữa các cây").
Phân số luôn là `.frac` hai `<i>`, không viết `a / b`. Chi tiết khuôn ở [[khuon-eq-cong-thuc]].

## Áp dụng thế nào

Sửa một bài ML theo chuẩn này, theo đúng thứ tự:

1. **Đếm mục.** Trên 10 → gộp hoặc bỏ. *Lỗi hay gặp* hoà vào bảng §08 + *Hỏi đáp*; *Chọn khi nào*
   rút thành `ul.why`; mục dẫn giải công thức bỏ thẳng.
2. **Đặt tên mục theo đúng chữ trên hình §01**, và chữ đó là thuật ngữ tiếng Anh.
3. **Cắt chữ tới khi dưới 100 chữ/hình.** Cắt `p.key` xuống 1–3 câu, `ul.why` xuống 1–2 gạch, mỗi
   đoạn *Hỏi đáp* xuống một câu. Đừng cắt mục để hạ tỉ lệ.
4. **Bỏ hết `.note`, `<pre>`, `.card.bad`.**
5. **Chọn một bộ ví dụ nhỏ nhất** rồi vẽ lại mọi hình trên bộ đó.
6. **Thêm hoạt hoạ** cho hình có thứ tự đọc (quy trình, luồng, từng bước); để tĩnh hình so sánh.
7. `python3 tools/build.py` — [[cong-cu-va-cach-kiem]].

## Một chữ cũ vẫn dùng: "luật 1"

`tools/audit.py` và phép 8 của `soat.py` gọi **"luật 1"** là việc §01 phải có `figure.gist` vẽ cả
bài. Chuẩn mới giữ nguyên điều đó (mục 01 Mental model ở khung trên), nên hai công cụ đó vẫn đúng
— chỉ khác là hình `.gist` giờ phải động và phải là **thứ duy nhất** vẽ toàn cảnh, mục sau không
vẽ lại bản đồ nữa.

Luật trình bày bao trùm ở [[trinh-bay-bai]]; luật nội dung ở [[toi-thieu-de-hieu]]; thuật ngữ ở
[[thuat-ngu]]; số liệu toàn kho ở [[trang-thai-kho]].
