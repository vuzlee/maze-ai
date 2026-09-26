---
name: hinh-dong
description: "Luật vẽ HÌNH ĐỘNG — nguyên tắc gốc che chữ vẫn hiểu, chín luật dựng hình, bảng bẫy kỹ thuật đã vấp, kiểm bốn tầng, quy trình bảy bước. Bài mẫu: memory-model-mutability"
metadata:
  type: feedback
updated: 2026-09-26
---

Tách khỏi [[chuan-bai-mau]] ngày 2026-09-25: hoạt hoạ đã thành thứ lớn nhất phân biệt bản mới với
bản cũ, giữ chung một file với luật khung bài thì cả hai đều khó đọc. File kia nói **bài gồm mấy
mục và mục nào**; file này nói **hình trong mục đó chạy thế nào**.

**Bài mẫu: [`bai-mau/memory-model-mutability.html`](../bai-mau/memory-model-mutability.html)**
(chốt 2026-09-25) — 13 hình, hình nào cũng động, và là bản đầu tiên **ngoài kệ ML**. Mở bằng
trình duyệt trước khi áp luật nào ở đây; đọc luật không thay được việc nhìn nó chạy.

## Nguyên tắc gốc: che hết chữ đi vẫn phải hiểu được

Lấy tay che mọi `<text>` trong hình. Còn lại là hộp, mũi tên, màu và chuyển động — **chừng đó phải
đủ để hiểu chuyện gì đang xảy ra**. Không đủ tức là hình đang minh hoạ cho chữ chứ chưa thay được
chữ, và mọi luật bên dưới chỉ là hệ quả của phép thử này.

## Chín luật dựng hình

**1 · Một hình một ý — tiêu đề phải dùng chữ "và" thì tách đôi.** "Append và concat" là hai hình.
Bài mẫu §04 có đúng hai hình cạnh nhau (list thêm được tại chỗ · chuỗi phải chép sang vùng mới)
thay vì một hình hai nửa.

**2 · Animation chạy theo thứ tự thực thi, có ô "đang chạy".** Dòng code đang chạy nằm trong một
badge ở mép trên hình, đổi theo bước — bài mẫu dùng ở §01 (`a = [1, 2]` → `b = a` →
`b.append(3)`) và ở §03 (`f1(x): lst.append(4)` → `f2(y): lst = [9, 9]`). Người đọc luôn biết
mình đang ở dòng nào, không phải đoán.

**3 · Phép toán map vào data: đường nối + khung khoanh đúng phạm vi.** Badge `b[0] = 9` phải có
một đường đứt nối xuống **đúng ô** nó sửa, và ô đó được khoanh. Vẽ badge trôi nổi phía trên rồi
để người đọc tự tìm là hỏng — đó chính là chỗ "che chữ đi" sụp đầu tiên.

**4 · Giá trị đổi từ từ, viết dòng thời gian trước khi code.** Ô `1` không nhảy thành `9`; nó
được khoanh, rồi mới đổi. Và **viết ra dòng thời gian bằng chữ trước khi viết một dòng Python
nào** — bước nào hiện lúc nào, giữ bao lâu. Code hoá một dòng thời gian đã chốt thì rẻ; sửa mốc
thời gian bên trong code đã viết thì đắt.

**5 · Màu nói lên quan hệ: cùng nhau thì cùng màu.** Hai tên trỏ cùng một object thì mọi thứ
thuộc về object đó dùng một màu; nhánh sai dùng `--tomb`, nhánh đúng dùng `--ok`. Màu ở đây là
**quan hệ**, không phải trang trí — bốn màu ngữ nghĩa trong `CLAUDE.md` giữ nguyên nghĩa.

**Clay trong hình — bảy bài Python nới luật này, và đó là nới có chủ ý.** Luật cũ của kệ ML là
`--clay` **tuyệt đối không vào hình**; bảy bản chốt của `02-language-core` dùng nó 300+ lượt
(`rgba(var(--clay-a),.14–.16)` + `stroke="var(--clay)"` cho ô, `fill:var(--clay)` cho nhãn). Vì sao
vẫn đúng: hình ở đó **không có "dữ liệu đang xét"** để tô xanh — chúng vẽ ô nhớ, khung scope, ngăn
stack, tức là **vật chứa trung tính**. Clay ở đây là *"ô bình thường, chưa có gì xảy ra"*, rồi bốn
màu ngữ nghĩa mới đánh dấu thứ đang đổi. Ranh giới:

> Clay được dùng cho **bề mặt trung tính** của hình. Nó **không được** mang nghĩa —
> đúng/sai/con trỏ/kết quả vẫn phải là `--ok`/`--tomb`/`--probe`/`--filled`.

`soat.py` phép 3 chỉ bắt mã hex (`#E0855C`) nên không thấy dạng `var(--clay)`; đừng coi phép đó
là bằng chứng hình sạch clay.

**6 · Bớt đường nối — để hành vi nói thay mũi tên.** Hai ô cùng sáng lên một lúc đã đủ nói chúng
liên quan; thêm mũi tên chỉ làm rối. Bài mẫu §05 chứng minh shallow copy bằng cách **cho hai ô ở
hai ma trận đổi cùng lúc**, không vẽ một mũi tên nào giữa chúng.

**7 · Vẽ đúng cấu trúc thật, chỉ đóng khung thứ quan trọng.** Stack là khung, heap là khung, ô
tên nằm trong stack, object nằm trong heap — đúng như máy. Nhưng chỉ khoanh viền đậm thứ mục đó
đang nói tới; khoanh hết thì không còn gì nổi lên.

**8 · Số liệu sinh từ code, và nói thẳng khi yêu cầu sai sự thật.** Mọi con số trên hình phải
chạy ra được, không ước lượng. Bài mẫu §04 đo tỉ lệ chậm đi khi *n* gấp đôi (1,93 lần · 5,37 lần)
và nói rõ đó là chi tiết cài đặt CPython. Yêu cầu vẽ một thứ không đúng với hành vi thật thì
**nói ra**, đừng vẽ cho xong.

**9 · Một hình một chu kỳ, chạy một lượt khi cuộn tới.** `linear 1 forwards` + khối
`IntersectionObserver` cuối bài, ngưỡng 0,4, bấm vào hình chạy lại. Giữ ở mốc 100%, không
`infinite`, không mốc tắt. Toàn bộ khối `animation:` nằm trong
`@media (prefers-reduced-motion:no-preference)`, chỉ hoạt hoạ `opacity` và `transform`.
Chu kỳ theo số lượt: bài mẫu 5,4s cho 6 lượt tới 16s cho 24 lượt.

## Bảng bẫy kỹ thuật đã vấp

| # | Bẫy | Dấu hiệu | Chữa |
|---|---|---|---|
| 1 | **`fly` chỉ vẽ trong keyframe, quên bản tĩnh** | tắt hoạt hoạ thì phần tử biến mất | phần tử bay phải có sẵn ở vị trí cuối trong `<g transform="translate(...)">`, keyframe chỉ *đưa nó tới đó* |
| 2 | **`loop=True` đi cùng `window`** | hình lặp nhưng khung nhìn đã cắt, lượt sau hiện nửa vời | bỏ `loop`; một lượt rồi đứng yên là mặc định |
| 3 | **`window` cắt sớm** | bước cuối rơi ra ngoài `viewBox` | tính chiều cao từ phần tử thấp nhất **sau khi** cộng mọi `translate`, không từ toạ độ tĩnh |
| 4 | **`str.replace` làm hỏng file** | sửa được chỗ này, lệch chỗ kia, hoặc thay nhầm chuỗi trùng | dựng lại cả khối `<svg>` từ generator, đừng vá chuỗi trong HTML đã sinh |
| 5 | **`check.py` báo nhầm "chữ đè chữ"** | hai nhãn cùng toạ độ nhưng **không cùng lúc** — cái sau thay chỗ cái trước | không phải lỗi. `check.py` đo trạng thái cuối nên không thấy trục thời gian; đối chiếu bằng cửa sổ hiện của từng `<g>` trước khi sửa toạ độ |
| 6 | **dấu `<` trần trong `<text>` của `<svg>`** | HTML vẫn hiện, nhưng mọi công cụ parse SVG vỡ ("not well-formed") | escape thành `&lt;`. Gặp ở bài mẫu `typing-dataclass` (`<__main__.Plain object …>`); `soat.py`/`audit.py` không bắt được, chỉ tầng 2 bắt được |

**Bảng này chưa đủ 8 dòng.** Sáu dòng trên là sáu bẫy đã gọi được tên; hai dòng còn lại chưa ghi
kịp. Gặp lại bẫy nào thì thêm vào đây, đừng để nó lặp lần ba — luật ở [[cong-cu-va-cach-kiem]]:
bẫy lặp được thì vá thẳng vào `tools/svgkit/check.py`.

## Kiểm bốn tầng

Bốn tầng này đi theo thứ tự, tầng trước sạch mới sang tầng sau:

1. **Số** — mọi con số trên hình chạy ra từ generator, có `assert` đối chiếu với nguồn.
2. **Hình học** — `tools/svgkit/check.py` là sàng (tràn `viewBox`, chữ đè nhau), `getBBox` trong
   trình duyệt là trọng tài. Với hình động, phép "chữ đè chữ" **báo nhầm có hệ thống** (bẫy #5):
   chạy nó trên **bản tĩnh** (bỏ mọi `<g opacity="0">`) mới là con số đúng — bài mẫu 4 lỗi ở bản
   đầy đủ nhưng **0 lỗi ở bản tĩnh**, và 0 cặp chữ nào thật sự hiện cùng lúc ở cùng toạ độ.
3. **Bản tĩnh** — bật "giảm chuyển động" (hoặc bỏ khối `@media`) rồi đọc lại: hình phải đầy đủ,
   không thiếu chi tiết nào. Đây là tầng bắt bẫy #1, và máy không bắt hộ được.
4. **Bản động** — xem trọn một lượt từ đầu, kiểm thứ tự bước có khớp thứ tự thực thi, và badge
   "đang chạy" có đổi đúng chỗ không.

## Quy trình bảy bước

1. **Viết dòng thời gian bằng chữ** — bước nào, hiện lúc nào, giữ bao lâu. Chưa có cái này thì
   chưa viết code.
2. **Chốt bộ số** và viết `assert` cho nó.
3. **Dựng bản tĩnh trước** — hình đọc được đầy đủ khi chưa có một keyframe nào.
4. **Thêm keyframe** theo dòng thời gian ở bước 1, chỉ `opacity` và `transform`.
5. **Chạy `check.py`**, sửa hình học.
6. **Kiểm bốn tầng** ở trên.
7. `python3 tools/build.py` rồi mở bằng trình duyệt — [[cong-cu-va-cach-kiem]].

## Bài mẫu chạy gì ở mục nào

Mười ba hình, hình nào cũng động. Cột cuối là thứ hình đó phải cho thấy **khi đã che hết chữ**:

| Mục | Hình | Lượt / chu kỳ | Che chữ vẫn phải thấy |
|---|---|---|---|
| 01 Mental model | RAM · stack · heap (`.gist`) | 24 / 10,4s | ba dòng code chạy lần lượt, hai ô tên chụm về **một** object, object phình ra |
| 01 | C/Java so Python | 12 / 7,7s | bên trái giá trị nằm trong ô tên, bên phải ô tên rỗng và mũi tên đi xuống heap |
| 02 Tên và object | `b = a` | 6 / 5,4s | mũi tên thứ hai mọc ra, trỏ vào **đúng** object cũ |
| 03 Gán lại hay sửa | gán lại tên | 6 / 5,4s | mũi tên của `b` **chuyển hướng**, `a` đứng im |
| 03 | sửa ô qua `b` | 7 / 11s | badge nối xuống đúng ô, ô được khoanh rồi mới đổi |
| 03 | hai frame hàm | 21 / 12s | frame mới mọc ra rồi **biến mất**; nhánh trên đổi heap, nhánh dưới không |
| 04 Mutable hay không | `append` | 10 / 12s | ô trống mọc ở cuối, phần tử bay vào, khung object **không** đổi |
| 04 | chuỗi `+=` | 21 / 16s | ký tự bị chặn ở ô cuối, cả dãy phải chép sang chỗ khác |
| 04 | ba cách nối chuỗi | 12 / 7,5s | ba cột cao thấp khác hẳn nhau |
| 05 Copy | gán | 12 / 11s | một ô đổi, **hai** tên cùng thấy |
| 05 | shallow copy | 24 / 16s | vỏ đã là hai, nhưng hai ô ruột đổi **cùng lúc** |
| 05 | deep copy | 16 / 13s | đúng hình trên, nhưng bên kia đứng im |
| 07 Bốn bẫy | bốn bẫy + ma trận | 7 / 8,9s | bốn cặp sai/đúng, và một dòng được trỏ ba lần |

Mục 06 (`is` và `==`) **không có hình** — nội dung là hai bảng tra, đúng luật "nội dung là chữ
thì dùng khuôn HTML đừng vẽ SVG" ở [[toi-thieu-de-hieu]].
