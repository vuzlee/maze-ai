---
name: trinh-bay-bai
description: "Luật TRÌNH BÀY cho mọi kệ — ít chữ nhiều hình, rất ít note, câu đơn (cả trong Hỏi đáp), công thức dáng LaTeX, bảng tra ký hiệu, mỗi trường hợp một ô hình; kèm khuôn overview và cách báo cáo"
metadata:
  type: feedback
updated: 2026-09-08
---

Gộp từ bốn ghi chú cũ (ít-chữ-nhiều-hình · câu-đơn-và-bảng-tra · quy-ước-overview · cách-trả-lời).
Đây là luật **trình bày**; luật **nội dung** ở [[toi-thieu-de-hieu]], thước bài ở [[chuan-bai-mau]].

## Câu người dùng gói cả chuẩn vào một dòng (2026-09-08)

> "ít chữ, nhiều hình, rất ít note, phân hình theo từng trường hợp dễ nhìn, chú thích trên hình,
> tách bạch rõ ràng cho dễ đọc, nội dung ngắn gọn câu đơn, xuống dòng thì bullet, câu chữ dễ hiểu
> đơn giản không ví von đánh đố, **công thức latex**,… (xem lại kĩ svm, knn)"

Nhắc lại nguyên văn ngày 2026-09-08, lần này có thêm hai vế cuối. Hai bài mẫu:
[[bai-mau-svm-knn]].

**Nhắc lần ba cùng ngày**, sau khi sửa `ridge-lasso-elasticnet`, kèm câu hỏi *"đã note đủ trong
chuẩn chưa?"*. Cả tám vế đều đã có luật; vế **không ví von** thì chỉ có nửa (mới cấm ẩn dụ kinh
tế) nên đã mở rộng thành luật F ba họ ẩn dụ ở dưới. Người dùng nhắc lại nguyên văn cả câu **mỗi
lần thấy một vế bị phạm** — nên đọc lại đủ tám vế trước khi giao bài, đừng chỉ chữa vế bị bắt.

| Luật | Kiểm thế nào |
|---|---|
| ít chữ, nhiều hình | chỉ số chữ/hình — công thức bên dưới |
| **rất ít note** | `grep -c '<div class="note'` — tối đa **một** cái một bài |
| phân hình theo từng trường hợp | một `<svg>`, mỗi trường hợp một panel, cùng bộ ví dụ |
| chú thích **trên hình** | chữ nằm trong `<svg>`/`<figcaption>`, không phải đoạn văn dưới hình |
| tách bạch rõ ràng | mỗi mục một việc, đừng trộn hai ý vào một khối |
| câu đơn, xuống dòng thì bullet | mục A dưới đây |
| không ví von đánh đố | luật F dưới đây (ba họ ẩn dụ, **soát cả chữ trong `<svg>`**) · [[toi-thieu-de-hieu]] luật H |
| **công thức latex** | mọi công thức đứng riêng là `.eq` mang `<var>`/`.fn`/`.frac`/`.ov` — [[khuon-eq-cong-thuc]] |

**`.note` phải hiếm.** Nó là khối tô nền, mắt nhảy vào trước — dùng nhiều thì hết tác dụng nhấn.
Cách chữa: hoà tan thành `ul.why` (điều kiện, cảnh báo, hệ quả) hoặc thành hình. Chỉ giữ khi nó
là *một câu chốt đáng dừng lại*.

## Chỉ số chữ/hình

Chỉ số cũ "tỉ lệ văn xuôi" **sai hướng, đừng dùng lại** — 2026-09-03 tôi tăng văn xuôi cho
`random-forest` và người dùng đọc xong nói *"chả hiểu gì"*. Người dùng học bằng **hình**.

```python
v = len(re.findall(r'<figure|<svg |class="(?:strip|flow|cmp|stack|mtx|axis|seq|bars|eq|cellrow|cells)\b', s))
t = re.sub(r'<svg.*?</svg>', '', s, flags=re.S); t = re.sub(r'<[^>]+>', ' ', t)
ratio = len(t.split()) / max(v, 1)
```

Mốc: `random-forest` **123 chữ/hình**; trên **250 đáng soát**, trên **300 phải sửa**.
Thứ tự chữa: bảng so sánh văn xuôi → khuôn hình · `<ol>`/`ul.why` dài → `.stack` · đoạn văn lẽ ra
nên là hình → vẽ mới · bảng Hỏi đáp → `details.qa`. **Bảng tra thật thì để yên** — đó là bảng
đúng chỗ. `.axiscap`/`.stripnote` là flex ba `<span>` (nhãn · `<em>` · nhãn), viết câu trơn vào
là hỏng bố cục.

## Sáu luật trình bày (chốt 2026-09-07 khi sửa `svm`)

**A — câu đơn, mỗi dòng một ý.** Kho này để **ôn**, không để thưởng thức. Hai dấu phải soi:
gạch ngang `—` nối mệnh đề, chấm phẩy `;` đối lập → tách thành câu riêng. Đoạn nhiều ý thì tách
nhiều `<p>`, đừng ngại đoạn một câu. Đo được: `svm` đoạn dài nhất 96 → 39 từ, đoạn >33 từ 9 → 0.

Luật này áp **cả trong `details.qa`**, không dừng ở mặt bài. `svm` là bài duy nhất của cả kho đã
làm: 5 câu hỏi tách thành 21 đoạn, đoạn dài nhất 32 từ. Lý do không phải thẩm mỹ — `tools/build.py`
bóc thẳng `details.qa` thành thẻ ôn trong `assets/quiz-index.js`, nên một câu trả lời 118 từ liền
khối là một mặt thẻ không dùng được.

**B — chú thích ký hiệu là BẢNG TRA.** `dl.defs` ngay dưới câu chốt: `dt` là ký hiệu, `dd` là
nghĩa, mỗi dòng dưới 10 từ, **thay hẳn** đoạn văn giảng. `dd` viết như trả lời câu hỏi thường
(*"một điểm lấn vào sâu bao nhiêu"*). Bảng ký hiệu đặt **SAU** khối `.eq` — đọc công thức trước,
tra ký hiệu sau.

**C — mỗi trường hợp một ô hình.** Vẽ các ô cạnh nhau trong **cùng một** `<svg>`, cùng kích thước,
cùng bố cục, **chỉ một thứ đổi**. Chọn trường hợp phổ biến, **bỏ ca biên**.

Luật này **không dừng ở mục Mental model**. 2026-09-08 người dùng hỏi *"các trường hợp khác nhau
tách hình như svm chưa?"* — bài `ridge` lúc đó đã có hình bốn ô ở §01, nhưng mục *λ* vẫn còn là
`.axis` bốn chặng chữ, đúng thứ mà luật này ra đời để thay. Cách nhận ra một mục còn nợ hình:

> **mục này có kể ra 2+ trường hợp / mức / chế độ không?** Có → mỗi cái một ô hình.

`svm` là thước: **ba mục khác nhau, ba hình nhiều ô** (bốn ý ở §01 · đủ điểm vs chỉ support
vector ở §02 · hard vs soft ở §03 · ba mức ξ ở §03). Không phải một hình tổng ở đầu rồi hết.

`.axis`/`.strip`/`.flow` là khuôn **chữ xếp hàng**, không phải hình. Chúng hợp khi các chặng
thật sự chỉ là nhãn (mức cô lập, các bước một quy trình). Khi mỗi chặng có **hình thù khác nhau
vẽ ra được** thì phải vẽ.

**Bốn ô phải chung một hệ quy chiếu.** Hình λ của `ridge` lần đầu vẽ mỗi ô một bộ đồng mức tính
riêng — nhìn ra bốn hình rời, không so được. Sửa: tính sẵn ba đồng mức **giống hệt ở cả bốn ô**,
chỉ đổi đúng một thứ (bán kính vùng phạt). Lúc đó mắt mới đọc ra câu *vùng hẹp dần thì nghiệm
trượt ra đồng mức cao hơn*, tức là đọc ra chính nội dung của mục.

**D — hiểu ý trước, chi tiết sau.** *"HARD MARGIN SOFT MARGIN trước để hiểu, sau đó mới chi tiết"*.
Thứ tự trong một mục: câu chốt → hình toàn cảnh → bảng ký hiệu → hình chi tiết từng ca → công thức.

**E — chú thích trong hình càng ít càng tốt.** *"đừng note nhiều như hiện tại, nhìn không biết cái
nào quan trọng"*. Test: hình ngay dưới đã nói cùng chuyện → xoá; chú thích chỉ đếm (`4 support
vector`) hoặc nhắc lại công thức bên dưới → xoá.

**F — không ẩn dụ, dù là ẩn dụ nghe rất tự nhiên.** Bốn họ đã mắc:

| Họ ẩn dụ | Chữ đã dùng sai | Nói thẳng |
|---|---|---|
| kinh tế | *trả phí · giá phải trả · đắt/rẻ* | **bị phạt** · phạt nặng / phạt nhẹ · **nhược điểm** |
| vật lý | *lực đẩy về 0 · hãm model lại · kéo/tụt/nhảy* | **đạo hàm** bằng λ · cộng số hạng phạt · hệ số đổi nhiều |
| đồ vật | *núm vặn λ · vặn quá tay* | **λ — cường độ phạt** · λ quá lớn |
| y học | *chữa một bệnh · triệu chứng · liều lượng* | **chống overfitting** · gọi thẳng tên vấn đề |

Cái bẫy: ẩn dụ vật lý nghe *đúng* — L1 quả thật cư xử như một lực không đổi. Nhưng người đọc phải
tự dịch "lực" ngược về "đạo hàm" mới dùng được, mà bài đã có sẵn công thức `d|w|/dw = ±λ` ngay
cạnh. Test một câu: **chữ này có tên kỹ thuật thật ở ngay trong bài không?** Có → dùng tên thật.

Chỗ hay lọt nhất là **nhãn trong hình** — 2026-09-08 người dùng bắt được đúng một nhãn
`CÙNG CHUYỆN ĐÓ, NÓI BẰNG LỰC ĐẨY VỀ 0` trong `ridge-lasso-elasticnet`, trong khi mặt bài đã sạch.
Soát ẩn dụ phải soát cả `<text>` bên trong `<svg>`, không dừng ở văn xuôi.

## Sáu điều rút ra khi sửa `knn` §05 (2026-09-08)

1. **Bảng số bổ trợ thì bỏ, nếu hình đã nói xong.** Câu hỏi để quyết: *nhìn hình xong còn hụt gì*.
2. **Chi tiết thư viện là code, không phải nội dung** — «sklearn mặc định mean…» bị gạt thẳng.
3. **Không tự chế thuật ngữ** — «điểm hỏi» → **điểm cần dự đoán**. Chữ nào chỉ tồn tại trong bài
   của mình thì là chữ tự chế.
4. **In đậm trong văn xuôi → `.hl` màu cam** (`.lesson .hl{color:var(--clay);font-weight:600}`).
   `<b>` để dành cho trong hình và bảng.
5. **Đừng trỏ bằng vị trí** — «cả hai ô trên» không chỉ vào đâu. Gọi thẳng tên.
6. Điểm đánh dấu trong hình nên **cùng hình dạng với điểm dữ liệu, khác bằng vân** (`<pattern>`
   sọc chéo), không phải khác hình dạng.

Bẫy kỹ thuật: chèn khối mới bằng `s.index('  </div>\n', …)` **rơi vào khối `.eq` của mục khác** —
luôn neo bằng một chuỗi dài duy nhất của đúng mục đang sửa.

## Bài `*-overview` — chọn khuôn theo bản chất nhóm

Hỏi trước khi viết: chủ đề này có thật là **nhiều giải pháp cạnh tranh nhau qua lịch sử** không?

- **Có** → khuôn `tree-family-overview`: vấn đề → ý tưởng đầu tiên → vì sao chưa đủ → dòng thời
  gian → các nhánh → học theo thứ tự nào → từ điển.
- **Không** (một ngôn ngữ, một hệ thống, các công cụ song song) → khuôn ngắn: nó là gì → vì sao
  đáng quan tâm → học theo thứ tự nào. **Đừng dựng timeline và nhánh giả.**

Sáu lỗi đã mắc khi ép khuôn dài: đặt tên mục theo khuôn dù nội dung không khớp · nhồi timeline và
trivia · vẽ lại đúng cơ chế bài con đã vẽ · ba mục khác nhau mô tả cùng một danh sách bài · gán
nhiều sự kiện khác nguồn gốc vào chung một nguyên nhân (thành sai kiến thức) · tên mục tự bình
luận lý do tồn tại thay vì nói nội dung.

Ba thứ soát mỗi lần: mục này có vẽ lại cơ chế của bài con không (có → cắt còn 1–2 câu kèm link) ·
tiêu đề có gọi thẳng tên khái niệm không (đừng rút gọn tới mức mất từ khoá khỏi mục lục) ·
overview cấp nhóm giữ đúng tầng overview như cấp kệ.

## Báo cáo cho người dùng: thật ngắn, tiếng thường

*"thật ngắn gọn dễ hiểu vì tôi không hiểu gì về cái này"* — nói về CSS / khuôn hình / cách dựng
giao diện. Người dùng làm chủ phần **nội dung**, không làm phần kỹ thuật hiển thị.

Khi báo cáo việc ở phần giao diện: nói **thấy khác gì trên màn hình** và **tốt lên chỗ nào**, mỗi
ý một dòng. Tên class, tên file, số liệu kỹ thuật chỉ đưa khi được hỏi. Phần nội dung/sư phạm thì
bàn bình thường — chỗ đó họ rành.
