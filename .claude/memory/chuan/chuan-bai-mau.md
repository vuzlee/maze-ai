---
name: chuan-bai-mau
description: "Hai mươi bốn bản gốc — trọn kệ Python người dùng chốt, giữ ở bai-mau/: random-forest (khung A), ba bài boosting (khung B), năm bài classical ML (khung C) bảy bài language core + bốn bài concurrency/built-in (khung D, thước hình động). Kèm số đo mốc và luật rút ra"
metadata:
  type: feedback
updated: 2026-09-26
---

**Mười sáu bản gốc nằm ngay cạnh ghi chú này — mở bằng trình duyệt là thấy:**
[`bai-mau/random-forest.html`](../bai-mau/random-forest.html) (chốt 2026-09-24, khung A) và ba bản
khung B chốt 2026-09-25: [`bai-mau/xgboost.html`](../bai-mau/xgboost.html),
[`bai-mau/gradient-boosting.html`](../bai-mau/gradient-boosting.html),
[`bai-mau/adaboost.html`](../bai-mau/adaboost.html). Thêm năm bản **khung C** chốt 2026-09-25:
[`bai-mau/knn.html`](../bai-mau/knn.html), [`bai-mau/logistic-regression.html`](../bai-mau/logistic-regression.html),
[`bai-mau/ridge-lasso-elasticnet.html`](../bai-mau/ridge-lasso-elasticnet.html), [`bai-mau/svm.html`](../bai-mau/svm.html),
[`bai-mau/naive-bayes.html`](../bai-mau/naive-bayes.html) — `linear-regression` cùng khung C và cũng
đã chốt nhưng **không lưu bản ở đây**, đọc thẳng file trong `content/`. Bản thứ mười là
[`bai-mau/memory-model-mutability.html`](../bai-mau/memory-model-mutability.html) (2026-09-25), bài mẫu
đầu tiên **ngoài kệ ML** và là thước của hình động — luật của nó ở [[hinh-dong]].
Bản thứ mười một là [`bai-mau/memory-management-gc.html`](../bai-mau/memory-management-gc.html)
(2026-09-25), bài kế bên nó trong cùng nhóm, theo cùng thước ấy.
Năm bản còn lại chốt 2026-09-26 và đóng trọn nhóm `02-language-core`:
[`scope-legb`](../bai-mau/scope-legb.html) · [`data-model-dunder`](../bai-mau/data-model-dunder.html) ·
[`iterator-generator`](../bai-mau/iterator-generator.html) ·
[`decorator-context-manager`](../bai-mau/decorator-context-manager.html) ·
[`exception-handling`](../bai-mau/exception-handling.html).
Bốn bản cuối chốt cùng ngày, sang hai nhóm khác của kệ Python:
[`thread-process-gil`](../bai-mau/thread-process-gil.html) ·
[`asyncio`](../bai-mau/asyncio.html) ·
[`dict-hash-table`](../bai-mau/dict-hash-table.html) ·
[`list-tuple-set`](../bai-mau/list-tuple-set.html).
Bốn bản đóng kệ Python: [`leetcode-toolkit`](../bai-mau/leetcode-toolkit.html) ·
[`oop-python`](../bai-mau/oop-python.html) ·
[`typing-dataclass`](../bai-mau/typing-dataclass.html) ·
[`performance-profiling`](../bai-mau/performance-profiling.html).

**Mười lăm bài Python này là một khuôn thứ tư, gọi là khung D** — bài *giải thích cơ chế ngôn ngữ*,
không phải bài model. Bộ xương: **5–7 mục**, mở bằng `Mental model` (hoặc thẳng vào cơ chế khi bài
đủ hẹp), mỗi mục một cơ chế, đóng bằng `Hỏi đáp`. Khác ba khung kia ở ba chỗ:
**không** có mục `Công thức tổng quát` (ngôn ngữ không có loss), **không** có `Ưu và nhược`
(cơ chế ngôn ngữ không phải thứ để chọn hay bỏ), và **mục nào cũng có đúng một hình động**
— tỉ lệ chữ/hình không còn là thước, giống khung C.
Bốn bản 2026-09-26 cho thấy khung D **không bị bó trong nhóm `02-language-core`**: nó áp được cho
bài *so sánh cấu trúc dựng sẵn* (`list-tuple-set`, 5 mục) và bài *mô hình chạy song song*
(`thread-process-gil`, 8 mục — dài nhất của khung D vì nó gộp thêm phần scheduling của kệ CS).
Mục đóng của khung D có thể là một **bảng chọn** (`Chọn mô hình nào`) trước `Hỏi đáp`, khi bài
thật sự có nhiều lựa chọn để cân — đó không phải `Ưu và nhược` của khung C quay lại, vì nó chọn
giữa **mấy công cụ**, không phải chấm điểm một công cụ.
Bốn bản đóng kệ (2026-09-26) mở thêm hai biên của khung D: `performance-profiling` chỉ **2 hình /
5 mục** mà vẫn được chốt (mục *Thứ tự nên thử* là một bảng, đúng luật "nội dung là chữ thì dùng
khuôn HTML"), và `leetcode-toolkit` (giờ ở kệ DSA) là bài **gồm công cụ rời** nên mỗi mục một công cụ, không có
`Mental model` mở đầu — mở thẳng vào `bisect`. Khung D **không bắt buộc mục 01 tên Mental model**;
`audit.py` báo 10 bài Python "§01 chưa tên Mental model" chính là chỗ này, và đó là phép kiểm viết
cho khung A/B/C chứ không phải lỗi bài.
Ghi chú này chỉ nói *vì sao* các bản đó đúng;
thứ gì đọc ra được từ chính file thì đừng chép lại vào đây.

Chúng **không mâu thuẫn nhau** — là ba khuôn cho ba loại nội dung, xem mục
*Chọn khuôn nào* cuối file.

Người dùng 2026-09-24: *"đây mới là bản tôi kì vọng, tối giản, có trực quan hoá animation dễ hiểu
thân thiện, không phải tưởng tượng. các mục tối giản, hầu như hình, ít chữ, màu sắc cam và bold
những thứ quan trọng. đơn giản, không vẽ hình khó hiểu."*

Bản này **thay** mọi thước cũ (bản random-forest trước đó và cặp svm/knn). Luật cũ nào mâu thuẫn
với nó thì đã xoá khỏi bộ nhớ, không giữ kèm đính chính.

## Số đo — đây là mốc mới của cả kho

| | RF (A) | XGB | GB | Ada | 6 bài C | Luật |
|---|---|---|---|---|---|---|
| mục | **9** | 8 | 8 | **7** | **7–9** | 7–10, không hơn |
| chữ mặt bài | **914** | 1.657 | 1.538 | 1.382 | **1.206–1.578** | dưới 1.000 lý tưởng; khung B nới, đừng quá 1.700 |
| hình | 16 | 18 | 11 | 12 | 4–6 | mục nào cũng có ít nhất một |
| `<svg>` | 7 | 7 | 5 | 5 | 4–6 | khung C: **một `<svg>` một `<figure>`** |
| **chữ/hình** | **57** | 92 | 140 | 115 | 201–362 | khung A giữ mốc 57; **khung B tới ~140**; khung C bỏ hẳn mốc này |
| khối `.eq` | 2 | 4 | 1 | 2 | **1–3** | theo số bước tính, không theo quota |
| `figcaption` | 1 | **0** | **0** | **0** | **0** | chỉ dùng khi có điều *phải* nói, không mô tả hình |
| `.note` · `<pre>` · `.card.bad` · lab | **0** | **0** | **0** | **0** | **0** | không phải "ít", là **không có** |

Mốc 100 chữ/hình của bản 2026-09-24 **đã nới**: ba bài khung B đo 92 · 115 · 140 và người dùng
chốt cả ba. Khung B tốn chữ vì mỗi bước tính phải chạy tay ra số; **đừng cắt bước tính để hạ tỉ
lệ**. Mốc 57 vẫn là mốc của khung A.

**Naive Bayes phá mốc chữ/hình mà vẫn được chốt (362)** — và đó là bằng chứng tỉ lệ này *không
phải* luật, chỉ là dấu hiệu. Bài đó đúng **4 hình cho 7 mục**, mỗi hình gánh trọn một bước,
thay vì rải 11–18 hình nhỏ như ba bài boosting. Thứ cần đếm là **mục nào cũng có đúng một hình
thay được đoạn văn**, không phải số hình trên đầu chữ. Tỉ lệ cao mà mỗi mục vẫn một hình thì
không cắt; tỉ lệ cao vì có mục *không* hình thì mới là nợ.

## Khung A — 9 mục, dùng cho model có vài cơ chế rời (Random forest)

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

## Khung B — chuỗi tính, cho model là MỘT công thức chạy nhiều bước

Ba bài mẫu dùng khung này (XGBoost, Gradient boosting, AdaBoost) và **tên mục gần
như trùng nhau** —
đó là chủ ý: đọc xong một bài thì hai bài kia không phải học lại cách điều hướng, chỉ việc so
xem chỗ nào khác.

```
hero      như khung A
01  Mental model            p.key + figure.gist — hình là BẢN ĐỒ BÀI: mỗi ô mang số mục
                            và một dòng tóm tắt, ô của mục sau làm mờ đi
02  Công thức tổng quát     đưa ra objective TRƯỚC, trước cả loss cụ thể. .eq → dl.defs → hình
03  Regression và           cùng công thức trên, thay phần phụ thuộc loss cho hai bài toán.
    classification          Một hình hai cột, cùng bộ dữ liệu, chỉ khác vài dòng
04  Từ bảng tới một cây     chạy tay MỘT cây/stump trên bộ ví dụ, ra số thật
05  Cộng dồn nhiều cây      ba cây nối tiếp, cột "còn sai" nhỏ dần, rồi một mẫu mới đi qua cả ba
06  <mục riêng của bài>     chỗ duy nhất mỗi bài tự do
07  Ưu và nhược             như khung A
08  Hỏi đáp                 như khung A
```

**Mục 06 là chỗ duy nhất ba bài khác nhau** — và đó đúng là điểm riêng của từng model:

| Bài | Mục 06 | Vì sao đây mới là điểm riêng |
|---|---|---|
| XGBoost | *Vì sao công thức có dạng đó* | parabola của Obj theo giá trị lá: đáy là Output value, độ sâu là Similarity Score |
| Gradient boosting | *η, số cây và điểm dừng* | đóng góp riêng của nó là learning rate + early stopping, không phải công thức |
| AdaBoost | *Vì sao công thức có dạng đó* | α và trọng số đều suy ra từ exponential loss |

AdaBoost gọn còn **7 mục** vì nó không có mục 03: exponential loss chỉ làm classification, nên
không có hai dạng để đối chiếu. **Thiếu một dạng thì bỏ hẳn mục, đừng viết mục rỗng cho đủ khuôn.**

**Naive Bayes từng xếp vào khung B** vì công thức của nó chảy qua bốn bước (đếm → cộng α → lấy
log rồi cộng → argmax). Bản chốt 2026-09-25 xếp lại vào **khung C**: tên mục của nó
(*Mental model · Công thức tổng quát · Từ 10 lá thư tới bảng đếm · Laplace và thang log · Giả định
sai mà vẫn dùng được · Ưu và nhược · Hỏi đáp*) đúng bằng bộ xương khung C. Hai điều
riêng đáng chép lại:

- **Hai cái chữa hai lỗi khác nhau thì gộp một mục được** (Laplace chữa ô bằng 0, log chữa tràn
  số) — miễn là câu `p.key` nói thẳng ra chúng chữa hai lỗi khác nhau.
- **Các biến thể của cùng một model thì làm BẢNG trong *Ưu và nhược*, không làm mục riêng và
  không làm hình.** Ba dòng Multinomial · Bernoulli · Gaussian nói đủ; một hình cho việc này là
  hình chỉ chứa chữ.

**Vì sao khác khung A.** Random forest là ba cơ chế rời nhau (bootstrap, random features,
aggregating) — tách mục nào ra đọc riêng cũng hiểu. Ba bài boosting là **một công thức chảy qua
nhiều bước**, nên cắt theo cơ chế thì mục nào cũng cụt. Cắt theo **thứ tự tính** thì mỗi mục là
một bước, và mục 06 trả lời được câu "vì sao lại là công thức đó" mà khung A không có chỗ chứa.

**Mục *Loss function* của khung A tan vào mục 02 và 03** — loss không còn là một mục riêng mà là
thứ mục 02 nhận vào và mục 03 điền số vào. Đây là lý do cả ba bài khung B **không** có mục tên
"Loss function": hàm loss xuất hiện sớm hơn, ở chỗ nó thật sự được dùng.

**Không bài mẫu nào của 2026-09-25 có `<figcaption>`**, và bài nào cũng giữ đúng một bộ ví dụ nhỏ
chạy suốt bài — Naive Bayes chỉ dùng 10 lá thư và 4 chữ cho cả 4 hình.

## Khung C — 7–9 mục, cho model classical ML có nhiều mặt độc lập

Sáu bài `knn` · `logistic-regression` · `ridge-lasso-elasticnet` · `svm` · `linear-regression` ·
`naive-bayes` chốt 2026-09-25. Đây là khuôn **gọn nhất** trong ba khuôn, và là khuôn nên mặc định
lấy khi soạn tiếp `05-classical-ml`. Naive Bayes từng xếp vào khung B; bản chốt mới kéo nó về
đúng bộ xương này, nên khung B giờ chỉ còn nhánh boosting.

Bộ xương cố định — hai đầu giống nhau ở cả sáu bài, chỉ ruột là riêng:

```
01  Mental model        bản đồ cả bài, một hình
02  Công thức tổng quát  (KNN đổi thành "Từ bảng tới dự đoán" vì không có công thức học)
03…  mỗi mặt một mục    2–5 mục, tên mục là tên mặt
--  Ưu và nhược         gộp cả "chọn khi nào" và "lỗi hay gặp" vào một bảng Ưu | Nhược
--  Hỏi đáp             mục cuối, luôn có
```

Ba điều khung C làm khác hai khung kia:

- **Không còn mục *Lỗi hay gặp* và *Chọn khi nào* riêng.** Cả hai tan vào bảng hai cột của
  *Ưu và nhược*, rồi vài gạch `ul.why` bên dưới nói chọn nó khi nào. Sáu thẻ `.card.bad` của bản
  cũ biến mất hoàn toàn — nội dung đúng đó nằm ở cột **Nhược**.
- **Một `<figure>` một `<svg>`, không hình phụ.** Sáu bài đo 4–6 hình cho 7–9 mục, tức có mục
  không hình — đúng chỗ mục đó thuần công thức hoặc thuần bảng.
- **Tỉ lệ chữ/hình bỏ hẳn** (đo 201–362). Hình khung C là hình **nhiều bước có hoạt hoạ**, một
  hình gánh cả mục, nên đếm tỉ lệ là đếm sai thứ. Thứ vẫn phải giữ: 0 note, 0 `<pre>`,
  0 `.card.bad`, 0 `figcaption`, 0 lab.

Hoạt hoạ giống khung B: keyframe trong `<style>` của từng `<svg>`, `linear 1 forwards`,
`IntersectionObserver` chạy một lượt khi cuộn tới, bấm để chạy lại. **Không hình nào `infinite`.**

## Chọn khuôn nào

> Model này là **vài cơ chế ghép lại**, **một công thức chạy nhiều bước**, hay **một ý tưởng nhìn
> được từ vài mặt**?

Vài cơ chế ghép lại (Random forest) → **khung A**, tên mục là tên cơ chế.
Một công thức chạy nhiều bước (ba bài boosting) → **khung B**, tên mục là tên
bước.
Một ý tưởng, vài mặt độc lập nhau (sáu bài classical ML) → **khung C**, tên mục là tên mặt. Dấu
hiệu: đọc mục 04 **không cần** nhớ mục 03 — KNN chọn k và KNN ở nhiều chiều là hai chuyện rời. Câu hỏi không phải "có cộng dồn model không" mà **"đọc xong mục này có phải nhớ nó để hiểu
mục sau không"** — phải nhớ thì là chuỗi tính.

**Cả nhánh boosting đi khung B**, kể cả AdaBoost — ban đầu tưởng nó là "vài cơ chế" (stump ·
trọng số · α) nhưng ba thứ đó cùng rơi ra từ một công thức, tách rời là cụt. LightGBM thì chưa
chốt; nó là XGBoost đổi cách xây cây, nên nhiều khả năng cũng khung B.

Dấu hiệu chọn sai: viết theo khung A mà mục nào cũng phải mở đầu bằng "nhắc lại mục trước" — đó là
chuỗi tính bị cắt rời, đổi sang khung B.

## Hình động — đã tách ra file riêng

Luật dựng hình động nằm ở **[[hinh-dong]]**: nguyên tắc gốc *che hết chữ đi vẫn phải hiểu được*,
chín luật dựng hình, bảng bẫy kỹ thuật, kiểm bốn tầng, quy trình bảy bước. Bài mẫu của nó là
[`bai-mau/memory-model-mutability.html`](../bai-mau/memory-model-mutability.html).

Chỗ duy nhất còn ở đây là hệ quả cho **khuôn bài**:

- Mục 01 phải có `figure.gist` động vẽ cả bài, và nó là **thứ duy nhất** vẽ toàn cảnh.
- **Hình so sánh song song thì để tĩnh** — mắt phải so được hai cột cùng lúc. Nới đúng một mức:
  so sánh *"cái này rồi tới cái kia, khác ở đây"* (§03 của XGBoost và Gradient boosting) thì hiện
  lần lượt được.
- **`aria-label` của mỗi `<svg>` là một câu kể trọn cả chuỗi động, kèm con số kết quả** — ví dụ
  *"Một bảng dữ liệu rút thành ba mẫu, mỗi mẫu mọc một cây, ba cây bỏ phiếu cho khách A và hai
  trên ba phiếu là không mua"*. Không phải chuyện trợ năng suông: `search-index.js` đọc chuỗi đó,
  nên nội dung chỉ nằm trong hình vẫn tìm được.

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

Ba bài khung B giữ luật này chặt hơn nữa: **một bộ khách chạy suốt mọi mục, không đổi lấy một
lần, và không bài nào có `<figcaption>`.** Cùng bộ đó vừa làm regression (y là mức chi
tiêu) vừa làm classification (nhãn mua / không mua) — nên mục 03 chứng minh được "cùng công thức,
chỉ thay g và h" bằng chính con số, không phải bằng lời hứa.

Khung C cho thấy **giới hạn của luật này**. Sáu khách A–F vẫn là mặc định (KNN chạy trọn bài trên
đúng bộ đó), nhưng hai bài phải đổi bộ vì bộ chung làm hình **mất nghĩa**:

- **SVM** dùng riêng 18 điểm hai chiều — sáu điểm thì gần như điểm nào cũng thành support vector,
  không còn gì để chỉ.
- **Ridge/Lasso** cần hai cột tương quan cộng hai cột nhiễu mới thấy L1 bỏ cột còn L2 giữ cả bốn.

Cả hai **nói thẳng trong văn xuôi là đang đổi bộ và vì sao** — không phải bằng `figcaption`. Đó là
cách đúng: đổi bộ thì khai, đừng lặng lẽ đổi, và cũng đừng bóp nội dung cho vừa bộ chung.

## Công thức

Hai khối `.eq` cho cả bài, đều theo khuôn: mỗi **nửa** công thức mang một `<em>` giải nghĩa riêng
nửa đó, `dl.defs` đặt **sau** (đọc công thức trước, tra ký hiệu sau), `dd` viết như câu trả lời
thường (`ρ` → *"các cây giống nhau tới mức nào"*, không phải "hệ số tương quan giữa các cây").
Phân số luôn là `.frac` hai `<i>`, không viết `a / b`. Chi tiết khuôn ở [[khuon-eq-cong-thuc]].

Khung B dùng 1–4 khối `.eq` (AdaBoost 2, Gradient boosting 1, XGBoost 4) — theo số bước tính thật sự có công thức, không theo quota — nhưng đặt chúng **rải đều theo thứ tự tính**, không dồn một chỗ: objective ở §02, Similarity ở §03, và §06
mới suy ra vì sao công thức có dạng đó. Suy công thức luôn là **mục cuối trước phần đánh giá**,
không phải mục đầu: người đọc phải dùng công thức đã rồi mới quan tâm nó ở đâu ra.

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
