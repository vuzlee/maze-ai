---
name: dot-overview-ke-01-05
description: "Đợt sửa bài *-overview kệ 01→05 — hình phải nói thứ chữ bên cạnh chưa nói; ba luật mới về hình trong overview; danh sách overview còn nợ theo chữ/hình"
metadata:
  type: project
updated: 2026-09-05
---

Người dùng: *"mấy cái bài overview cũng sửa lại để người đọc hiểu kệ (xem trong rule có gì dùng
được thì dùng không cần quá cứng nhắc) → mục tiêu cốt lõi là hiểu nhanh, dễ dàng, thuận mắt, hiểu
mental model"*. Overview được [[chuan-bai-mau]] **miễn** phần "mỗi mục vẽ lại bản đồ", nhưng
**không miễn một hình ở mục đầu** — đó là chỗ đợt này làm.

## Ba luật mới, rút ra từ năm bản đồ

**1. Hình không được vẽ lại thứ đang nằm ngay cạnh nó.** Bản `dsa-map` đầu tiên vẽ cột phải là
sáu chặng học — đúng cái `div.stack` ngay dưới, mà `.stack` còn **có link** còn hình thì không.
Hình thành ra thừa và kém hơn thứ nó nhân đôi. Cùng lý do, `alg-map` cố ý **không** vẽ lại bảng
ràng buộc n ở §02. Trước khi vẽ: liệt kê mọi `.stack`/`table`/`.cmp` trong bán kính một màn hình.

**2. Chỗ nào định vẽ trùng thì chuyển thành *chứng minh một câu `ul.why` chưa được chứng minh*.**
`ul.why` toàn câu khẳng định trần ("bài nào cũng cần cả hai", "một đề thật thường ghép hai nhóm").
Một ví dụ chạy được nói thay hẳn:
- `dsa-map` → two-sum: cách cất (hash map) · các bước (duyệt một lượt) · 1.000 số thì 1.000.000
  phép so còn 1.000;
- `alg-map` → meeting rooms ghép Greedy + Heap → `O(n log n)` vừa khít `n ≤ 10⁵` đề cho;
- `cs-map` → một request "Đặt hàng" đi xuyên cả bốn lớp.
Đây là kiểu ô duy nhất trong overview mà bài con **không** vẽ lại được, vì nó cắt ngang nhiều bài.

**3. Trong MỘT hình, một màu chỉ được mang MỘT nghĩa.** Bản `cs-map` đầu lấy `--tomb` đỏ làm màu
nhấn cho lớp Messaging — nhưng đỏ trong kho là *sai / phải trả giá*. Sửa: cả bốn lớp xanh
`--filled` (đều là "lớp"), đỏ chỉ dành cho **kiểu hỏng mới mà mỗi lớp mua thêm**. Bản v2 vẫn sai
nhẹ vì bốn hàng request lại tô bốn màu khác — cũng phải về xanh hết. Quy ước bốn màu là **toàn
kho**, nhưng phép "một màu một nghĩa" là **trong từng hình**, chặt hơn.

## Đã xong — năm bản đồ

| bài | chỗ đặt | thay cho | chữ/hình sau |
|---|---|---|---|
| `dsa-overview` | §02 | `.cmp two` (**sai ý**: hình nói "A hoặc B", chữ ngay dưới nói "A chạy TRÊN B") | 157 |
| `algorithms-overview` | §01 | bốn `.card` dày (bài **0 hình** duy nhất của kho) | 283 |
| `cs-overview` | §02 | bốn `.card` + một `.stack` ba lớp (**rơi mất** Distributed) | 234 |
| `db-overview` | §01 | bảng `orders` phẳng | 291 |
| `python-overview` | §03 | *chưa có gì* — câu quan trọng nhất kệ mà không hình | 352 |
| `sql-advanced-overview` | §01 | ba `.card.bad` trừu tượng → ba cảnh chạy được (4 ms vs 19 giây) | 163 |
| `math-foundations-overview` | §01 | `.cmp two` + một cột của bảng §02 | 279 |
| `classical-models-overview` | §01 | `.cmp two` + bảng 5 cột rút còn 4 | 258 |
| `clustering-overview` | §01 + §03 | `.stack` bốn định nghĩa cụm; §03 thêm hình chấm silhouette | 219 |
| `language-core-overview` | §03 | nửa "Ý mới" của bảy `.s` — hình §02 đã nói rồi | 256 |
| `tcp-http` (bài kỹ thuật) | §01 + §10 | `.bars` bốn chặng; §10 bỏ hai băng trùng §01 | 299 |
| `metrics-confusion-matrix` | §01 + §04 | SVG viết tay có hex ngoài bảng màu; §04 bỏ `.bars` vì hình đã nói | 272 |
| `data-quality` | §01 §03 §04 §05 | *chưa có §01*; §05 là SVG viết tay 542px hex cứng | 531 |
| `linear-regression` | §01 §02 §05 §08 | `.cmp two` linear-vs-logistic; hai SVG viết tay 41 hex cứng | 282 |
| `query-tuning` | §01 §02 §04 §07 | *chưa có §01*; §07 là SVG viết tay 536px, 54 hex cứng | 776 |
| `statistics` | §01 §04 §06 §09 | §09 "tổng kết một hình" vẽ lại §02+§03+§04; hai SVG viết tay ~35 hex cứng | 570 |
| `graph-bfs-dfs-topo` | §01 | SVG viết tay 900×250 vẽ lại đúng câu `p.key` (BFS theo lớp / DFS theo chiều sâu) | 400 |
| `union-find` | §01 | SVG viết tay 900×200 "trước/sau nén đường" — minh hoạ, không chứng minh | 383 |
| `dynamic-programming` | §01 | `.bars` 1,6 tỉ vs 40 + `.stripnote` khẳng định số mà không cho thấy vì sao | 367 |
| `shortest-path` | §01 | SVG viết tay 900×180 minh hoạ "ít bước ≠ rẻ nhất", 5 hex cứng | 406 |
| `dict-hash-table` | §01 | panel "cả bài trong năm dòng" nói lại cột trái, `ul.why` nói lần thứ ba | 351 |
| `intervals` | §01 | SVG viết tay 13 hex; §04 bỏ thẻ "sắp sai khoá" vì hình đã nói | 350 |
| `stack-monotonic-queue` | §01 | `.strip` + `.stripnote` nói lại `p.key`; **bài 0 hình** | 343 |
| `linked-list` | §01 | SVG viết tay 900×130 vẽ bốn nút — đúng câu `p.key`, 4 hex cứng | 338 |
| `er-modeling` | §01 §03 §05 | §01 `.flow` bốn bước = `p.key`; §03 SVG viết tay 41 hex; §05 "tổng kết một hình" | 338 |
| `tree-bst-traversal` | §01 | SVG viết tay 900×190 vẽ cây BST đẹp **+ `.cmp two` ngay dưới** liệt kê ba dãy | 333 |
| `backtracking` | §01 | SVG viết tay 900×200 vẽ cây quyết định = đúng câu `p.key` | 322 |
| `sliding-window` | §01 | `.strip` + `.stripnote` vẽ đúng câu `p.key`; **bài 0 hình** | 316 |
| `two-pointers` | §01 | `.strip` + `.stripnote` vẽ đúng câu `p.key`; **bài 0 hình** | 314 |
| `heap-priority-queue` | §01 | SVG viết tay 900×200 vẽ cây heap **+ `.strip` ngay dưới** — cả hai nói lại `p.key` | 313 |
| `overfitting-regularization` | §02 §04 §06 | ba SVG viết tay **vẽ phác không có số**; §06 là "Tổng kết một hình" gói lại §01+§02+§03 | 300 |
| `memory-model-mutability` | §01 §02 §06 §09 | bài **đã theo luật 1 đủ** (8 hình, 0 hex lạ) nhưng panel phải toàn hình vẽ **không có số** | 314 |
| `memory-management-gc` | §01 §05 | §01 panel "BỐN Ý — HẾT" kể lại `ul.why`; §05 ba generation không có giá | 318 |
| `iterator-generator` | §01 §05 §06 §08 | §01 lại "BỐN Ý — HẾT"; §05 số **ước lượng** `≈ 400 MB`; §08 `tee` gọi là ngoại lệ mà không có giá | 326 |
| `core-concepts-overview` | §01 | overview **0 hình**; `p.key` là ca luật 7 sách giáo khoa | 277 |
| `evaluation-overview` | §01 | `div.stack` ba trục — khẳng định trần "ba trục độc lập" mà không chứng minh | 270 |
| `ml-overview` | §01 | `.flow` ba bước + `ul.why` trần; overview mở kệ mà **0 hình** | 251 |
| `sorting` | §01 §06 §07 | `.cmp two` "trước/sau khi sắp" + một `.bars` **không có một con số đo nào** | 325 |
| `prefix-sum` | §01 §03 §04 | hai `.strip` + `.stripnote` vẽ lại đúng câu `p.key`; **0 hình** | 393 |
| `array-string` | §01 §02 §03 | `.strip` + `.bars` **nói sai sự thật** ("gấp đôi") + `.cmp two`; `lab.js` dạy sai cùng chỗ | 318 |
| `list-tuple-set` | §01 §02 §03 §04 §05 | §02 **trùng bài khác** (cấp phát list) — viết lại thành list-vs-tuple | 289 |
| `hash-map` | §01 §02 §03 §04 §07 | `.strip` 8 ô vẽ lại đúng câu `p.key`, `.cmp two` không một con số; §02 trùng `dict-hash-table` — đổi câu hỏi thành "khi nào O(1) chết"; **bài 0 hình** | 287 |
| `big-o-complexity` | §01 §05 §06 §09 | **bài 0 hình**; `.bars` §01 và §06 chỉ là bậc thang không đo; cả bài dựng trên mốc 10⁸ phép tính/giây mà **Python thuần chỉ đạt 5 × 10⁷** | 168 |
| `gradient-boosting` | §04 | panel phải là **bảng số về ba độ sâu** ở bài mà thứ đáng nhìn là hình dạng cây — thay bằng ba cây vẽ thật (stump 2 lá · depth 2 · depth 12), số đo tụt xuống làm nhãn | — |
| `adaboost` | **bài mới** | thêm giữa `random-forest` và `gradient-boosting`; 5 hình, §02 vẽ cấu trúc stump + mặt phẳng biên tròn mà một lát cắt thẳng không cắt nổi, §04 vẽ bốn vòng nối tiếp (chiều mũi tên + bagging song song đối chiếu); bỏ mục "dùng ở thư viện nào" | — |

Lỗi hình học đáng nhớ nhất là của `dsa-overview`: `.cmp two` là **hai cột song song**, hình học
đó có nghĩa "chọn A hoặc B", trong khi đoạn văn ngay dưới nói giải thuật *chạy trên* cấu trúc.
**Hình sai ý thì tệ hơn không có hình** — soát overview nên đọc hình trước, đọc chữ sau, xem hai
thứ có nói cùng một câu không.

## Luật 4 — đo chữ/hình thì bỏ cả `<table>`, không chỉ `<svg>`

Ba đợt đầu tôi chỉ tước `<svg>` trước khi đếm chữ. Sai: **bảng tra cũng là một thiết bị**, không
phải văn xuôi — người đọc quét bảng bằng mắt y như quét hình. Đếm cả chữ trong bảng thì mọi bài
`*-overview` (vốn có một bảng tra to) đều bị chấm oan; `clustering-overview` từ 348 tụt còn 288
chỉ vì đổi cách đếm, chưa sửa một chữ nào. Công thức đúng:

```python
s = re.sub(r'<svg.*?</svg>', '', raw, flags=re.S)
s = re.sub(r'<table.*?</table>', '', s, flags=re.S)   # ← thêm dòng này
```

## Luật 5 — chỉ số chữ/hình PHẠT đúng việc gộp hình, đừng chạy theo nó

`data-quality` sau khi sửa: 2668 → 2125 chữ (bỏ 543 chữ trùng), nhưng chỉ số chữ/hình lại
**tăng** 376 → 531. Vì mẫu số tụt nhanh hơn tử số: bốn `.cmp`/`.stack` bị hình mới nuốt gọn,
`<figure>` thì vẫn chỉ đếm là một. Nghĩa là **mỗi lần gộp đúng, chỉ số lại xấu đi**.

Nên dùng nó đúng một việc: **xếp hàng chờ** — tìm bài nào đáng mở ra xem. Chốt "xong hay chưa"
thì đọc bằng mắt theo ba câu:
1. §01 có một hình chứng minh được câu chốt của bài không (luật 1);
2. cạnh mỗi hình còn thiết bị nào **nói lại đúng thứ hình vừa nói** không;
3. chữ còn lại có phải thứ hình *không* nói được không (số liệu, câu lệnh, đánh đổi).

Ba câu đó `data-quality` đều đạt, dù chỉ số 531. Đừng thêm hình chỉ để kéo con số xuống.

## Luật 6 — mục "Tổng kết một hình" gần như luôn sai; đổi thành "đọc một ca thật"

Ba bài dài (`statistics`, `query-tuning`, `data-quality`) đều có một mục áp chót tên kiểu *Tổng
kết một hình*, và cả ba đều là **cùng một lỗi**: hình đó vẽ lại đúng những mục đã đọc, chỉ nhỏ
hơn và không link được. `statistics` §09 chẳng hạn gói lại §02 (`.mtx` hai loại sai) + §03
(`.cmp two` hướng p-value) + §04 (`.bars` MDE) — ba thứ vừa đọc xong cách đó vài màn hình. Nó
vi phạm luật 1 ở mức nặng nhất vì **nó tồn tại để nói lại**.

Chỗ đó vẫn đáng có một mục, nhưng phải đổi câu hỏi: từ *"cả bài nói gì"* sang **"cầm một kết quả
thật thì làm gì theo thứ tự nào"**. `statistics` §09 thành *Đọc một bảng kết quả* — một ca
`p = 0,03` đi qua bốn cửa, hai cửa chặn lại, `p` không đổi một chữ số. Ô đó là thứ **không mục
nào trong bài làm được**, vì mỗi mục chỉ dạy một cửa; chỉ mục cuối mới ráp được thứ tự.

Dấu hiệu nhận ra một mục tổng kết cần đổi: mở nó ra và đếm xem có bao nhiêu ô là **tên của một
mục khác trong cùng bài**. Từ hai ô trở lên là phải viết lại.

## Luật 7 — hình §01 của bài kỹ thuật phải chứng minh câu người đọc SẼ KHÔNG TIN

Bốn bài `01-dsa` đợt này đều hỏng cùng một kiểu: §01 có `p.key` nói một câu, rồi ngay dưới là một
hình **vẽ lại đúng câu đó**. Hình kiểu ấy không sai, nó chỉ vô ích — người đọc vừa đọc xong câu
tiếng Việt, không cần thấy nó lần hai bằng hộp và mũi tên.

Chỗ hình đắt nhất là câu mà **đọc chữ thì gật đầu nhưng không thật sự tin**:

- `union-find` — "thiếu một tối ưu thì vẫn đúng, chỉ chậm". Bảng đo 3×4 cho thấy mỗi tối ưu đứng
  một mình đều có **một dạng đầu vào riêng** bắt nó thua, và hai dạng đó khác nhau.
- `shortest-path` — "Dijkstra chết với cạnh âm". Bốn đỉnh, một cạnh −2: trả về 3 trong khi đường
  thật tốn 2, **không exception, không vòng lặp vô tận**. Chính chỗ "không có gì để debug" là thứ
  chữ nói mãi không thấm.
- `dynamic-programming` — "DP không phát minh phép tính mới, nó bỏ phần tính trùng". Cây fib(6):
  25 lần gọi cho 7 giá trị, cột đếm số lần mỗi giá trị bị hỏi lại.
- `graph-bfs-dfs-topo` — "BFS/DFS/Dijkstra là cùng một vòng lặp". Một đồ thị, bốn cái hộp chờ,
  bốn câu trả lời khác nhau.

Cách tìm: đọc `ul.why`, chọn gạch đầu dòng nào là **lời khẳng định trần không có số**, rồi dựng
đầu vào nhỏ nhất làm nó hiện ra. Nhỏ nhất thật — bốn đỉnh đủ thì đừng vẽ tám.

Hai thứ `check.py` không bắt được, phải chụp màn hình mới thấy:
- **figcaption nói lại tiêu đề/chân của chính cái hình** — caption phải là thứ hình *không* nói
  được (vì sao con số này đáng nhớ, phải làm gì khi gặp), không phải bản chữ của hình.
- câu chữ trong hình bị cụt hoặc chú giải lệch màu với ô nó chú ("7 ô xanh" trong khi cột phải
  tô xanh lá — phải viết rõ "xanh lam").

## Luật 8 — hình VẼ PHÁC không có số là dạng nói lại khó thấy nhất

`overfitting-regularization` có ba SVG viết tay và cả ba đều "đúng": learning curve hai đường
khép lại, learning curve hai đường dính nhau, grid 3×3 so với random 9 điểm. Nhưng cả ba chỉ vẽ
**hình dạng của câu vừa đọc** — không một con số nào. Kiểu hình này qua được luật 1 (nó không
trùng thiết bị nào bên cạnh) nhưng vẫn vi phạm tinh thần luật 7: người đọc gật đầu vì hình vẽ
đúng thứ họ vừa được kể, chứ không phải vì hình cho thấy thứ họ chưa tin.

Cách chữa rẻ: **chạy thật rồi vẽ số đo được**. Ba hình mới của bài đều dựng từ mô phỏng thuần
Python (hồi quy đa thức bậc 9 vs bậc 1 trên `sin(2,6x)+0,4x` cộng nhiễu 0,300):
- §02 — thêm 4.980 mẫu: bậc 9 lỗi val giảm **97%**, bậc 1 giảm **6%**. Cùng một tập, cùng một
  khoản chi. Hình cũ vẽ đúng hai hình dạng đó nhưng không nói được cái giá.
- §04 — grid 3×3 dừng ở 0,837; 400 lần lặp random 9 điểm cho trung vị 0,515 và **thắng grid
  387/400**. Quét dày 201 điểm cho biết tối ưu thật là 0,415 — tức λ tốt *không nằm trên lưới*.
- §06 — bốn cửa trên **một** ca: bậc 9 / n = 20 / val 9,26. Vặn λ được 0,64; hạ bậc 9 → bậc 5
  được **0,41** mà không thêm siêu tham số nào. Đó là chứng minh cho câu "giảm độ phức tạp thử
  trước" ở §03, thứ trước đó chỉ là lời khuyên trần.

Dấu hiệu nhận ra: mở hình ra, đếm **chữ số** trong đó. Không có chữ số nào và bài lại là bài
có thể đo được (ML, DB, hiệu năng) thì gần như chắc chắn phải dựng lại bằng số đo.

Một mẹo vẽ: khi một điểm vọt ra ngoài khung (val 9,25 với trục 0..1), đừng nới trục — cả đường
còn lại sẽ bẹp dí. Vẽ một mũi tên ở mép trên kèm nhãn *"val = 9,25, ngoài khung"*.

**Bài theo luật 1 đủ điểm vẫn dính luật 8.** `memory-model-mutability` là ca sạch nhất từng gặp
theo mọi thước cũ: 8 hình cho 10 mục, bản đồ 4 ô lặp lại đúng cách, 0 hex lạ, `check.py` không
một lỗi. Nhưng đếm chữ số trong tám panel phải thì gần như bằng không — panel nào cũng là hộp và
mũi tên vẽ lại đúng câu `p.key` bên trên. Đo bằng `timeit` mới ra thứ chưa ai tin:
`b = a` **2,1 ns bất kể n** (1.000.000 phần tử cũng vậy) trong khi `b = a[:]` là 6,74 ms —
**3,2 triệu lần**, và bộ nhớ 32 byte so với 8 MB. Đó chính là câu chốt của bài ("gán chép địa chỉ,
không chép dữ liệu") ở dạng **không thể gật đầu suông**.

Ba chỗ còn lại của bài cũng chữa cùng kiểu: `deepcopy` chậm **695 lần** shallow (0,01 · 1,7 ·
1.181 µs trên list 1.000 dòng), và bẫy `for x in a: a.remove(x)` **bỏ sót đúng một nửa** (định
xoá 1.000, còn lại 500) — cái nguy là *im lặng*, không phải exception. Mỗi lần một hình mới nói
thay được một `ul.why`, gạch đầu dòng đó phải **đổi thành sự thật khác**, không được xoá trống:
bullet "gán không tốn bộ nhớ theo kích thước" (bảng đã nói) thành `del a` chỉ gỡ nhãn — nối sang
bài GC ngay sau nó.

**Ba bài liền nhau hỏng cùng một khuôn panel.** Cả ba bài `02-language-core` dày nhất đều có
panel phải §01 tên kiểu *"BỐN Ý — HẾT"*: bốn băng, mỗi băng chép lại một gạch `ul.why` ngay dưới
nó. Đó là luật 1 vi phạm ở khoảng cách **20 pixel** — gần tới mức không ai để ý, vì hình và chữ
nằm trong cùng một màn hình. Dấu hiệu nhận ra nhanh nhất: **đếm số băng trong panel phải và số
`<li>` trong `ul.why` — bằng nhau là gần như chắc chắn nó đang kể lại**.

Cách chữa giống hệt nhau ở cả ba: thay panel bằng **một bảng đo cùng một việc theo n**, để cột
"lười / trỏ" phẳng lì còn cột kia phình theo n. `iterator-generator`: generator **200 byte · 0,13
µs bất kể n**, kể cả nguồn vô hạn, trong khi list n = 1.000.000 là 40,4 MB · 50 ms và hàng vô hạn
thì *không dựng được*. Cùng khuôn với bảng 2,1 ns / 6,74 ms của `memory-model-mutability` — đó là
lý do ba bài giờ đọc như một bộ.

**Số ước lượng trong hình là một dạng luật 8 khác.** `iterator-generator` §05 ghi `≈ 400 MB` và
`vài trăm byte`. Có chữ số nên qua được phép đếm, nhưng dấu `≈` là lời thú nhận rằng chưa ai chạy
thử. Đo thật ra **409 MB vs 544 byte — 752.000 lần**, và quan trọng hơn: bản lười còn **nhanh
hơn** (589 ms vs 656 ms), thứ mà con số ước lượng không thể nói.

**Thêm một chiều ngược lại thì hình mới hết là lời quảng cáo.** Bài nào cũng chỉ vẽ chiều mình
thắng. `iterator-generator` §05 bổ sung bảng n nhỏ: n = 1.000 thì generator **chậm hơn list 1,17
lần** và chẳng tiết kiệm gì. Hai bảng ngược chiều nhau trong một hình dạy được thứ một bảng không
dạy nổi — **ranh giới ở đâu**. Cùng kiểu: `tee` chỉ đắt khi hai nhánh **lệch nhịp** (4.116 byte
khi đi song song, 41,0 MB khi để một nhánh chạy cạn trước), nên câu "tee trả lại phần bộ nhớ vừa
tiết kiệm" là *đúng một nửa* — và nửa kia mới là thứ đáng nhớ.

## Luật 9 — hình đúng nhất của bài "kỹ thuật X nhanh hơn" là bảng CÓ CẢ CHỖ NÓ LỖ

Năm bài đợt này (`sorting`, `prefix-sum`, `ml-overview`, `evaluation-overview`,
`core-concepts-overview`) hỏng cùng một kiểu ở §01: bài dạy một kỹ thuật, hình vẽ **chiều kỹ
thuật đó thắng**, hết. Người đọc gật đầu và không học được thứ duy nhất khó: **khi nào đừng dùng**.

Khuôn đã chạy đúng năm lần: một bảng quét theo **một tham số** (n, số truy vấn, số mẫu), để
người đọc thấy **cột kết luận đổi dấu giữa chừng**, cộng một ô đỏ là chiều ngược lại hẳn.

- `prefix-sum` — q = 1 thì prefix **chậm 6,4×**, q = 10 hoà, q = 10.000 nhanh **481×**; ô đỏ:
  mảng bị sửa xen kẽ thì prefix **chậm 13,8×**. Câu chốt của bài đổi từ "O(1) mỗi truy vấn" thành
  **"trả tiền trước"** — cùng một sự thật nhưng câu sau nói được cả chỗ lỗ.
- `sorting` — chênh nở 25× → 3.804× theo n; ô ngược: chỉ cần 10 phần tử lớn nhất thì
  `nlargest` **rẻ hơn 11 lần** so với sắp cả mảng.
- `evaluation-overview` — viết lại điểm bằng một hàm tăng: ROC-AUC đứng im 0,969 ba lần trong khi
  F1 đổi **5,5 lần**; ô đỏ: model **không học gì** vẫn ăn accuracy 0,970.

Dấu hiệu bài cần khuôn này: `p.key` có dạng "X nhanh/tốt hơn Y" mà **không kèm điều kiện**.
Chỗ đắt nhất trong hình là **hàng đổi dấu** — ghi thẳng chữ *"điểm hoà vốn"* vào hàng đó.

## Luật 10 — chỗ hai bài chồng nhau thì hình mới phải đổi CÂU HỎI của mục, không chỉ đổi hình

`list-tuple-set` §02 tên là *"List cấp phát thế nào"* — đúng cái `array-string` §02 vừa được dựng
lại bằng số đo (1,125× · 86 lần nở · ≈ 8n phép chép). Vẽ một hình cấp phát nữa ở đây là **hai bài
sở hữu một khái niệm**, thứ `CLAUDE.md` cấm thẳng. Nhưng bỏ trống mục thì bài mất một nhịp.

Cách chữa: hỏi **bài này sở hữu câu hỏi nào mà bài kia không**. Bài đang đứng ở kệ Python, tên là
*List, tuple & set* — câu của nó là **chọn list hay tuple**, không phải list nở ra sao. Mục đổi
tên, hình đổi theo, và đoạn cấp phát rút còn một câu trỏ sang `array-string`.

Đo ra thì câu trả lời còn ngược với thứ ai cũng nói: **tuple không nhẹ hơn và không nhanh hơn**.
Từ n = 1.000 bộ nhớ chênh 0,2%, đọc chênh 3%, duyệt chênh 0%. Chỗ "nhanh 4,5×" duy nhất là khi cả
ba phần tử là hằng số viết thẳng (`(1,2,3)` nằm sẵn trong bytecode, 7,6 ns vs 34,0 ns) — thay một
hằng số bằng biến là tụt còn 1,9×, tức 19 ns, tức không ai đo được. Lý do thật để chọn tuple là
**làm khoá được**: tìm một điểm trong 20.000 điểm, list các list 157 µs, set các tuple 0,094 µs —
**1.672 lần**.

Ba dấu hiệu một mục đang lấn bài khác: tên mục **là tên một mục của bài kia**; `p.key` giảng một
cơ chế mà bài kia mới là chủ; `ul.why` toàn câu bài kia phải nói lại cho đủ nghĩa.

## Luật 11 — bẫy "kết quả sai mà không có lỗi" đắt gấp mấy lần bẫy "chậm"

Ba bài liền nhau (`prefix-sum`, `array-string`, `list-tuple-set`) đều có mục *Lỗi hay gặp*, và ở
cả ba, thẻ đáng nhớ nhất **không phải** thẻ nói "cái này O(n²)". Chậm thì đo là thấy. Thứ không
thấy được là bẫy **chạy xong, không exception, kết quả thiếu**:

- `list-tuple-set` — sửa một object đang làm khoá dict: `p in d` thành `False`, `d[p]` ném
  `KeyError`, nhưng `len(d)` vẫn là 1 và `list(d)` vẫn in ra phần tử đó. Dữ liệu còn nguyên, chỉ
  là không còn đường tra tới. Dựng lại đúng bản sao cũng không thấy.
- `list-tuple-set` — dựa vào thứ tự của set: `set([1,2,3,4,5])` lặp ra đúng thứ tự tăng dần nên
  **test nhỏ luôn qua**; `set([1,2,3,8])` ra `[8,1,2,3]`. Với chuỗi thì đổi **mỗi lần chạy**.
- `prefix-sum` — bản 2D quên `+ pre[r1][c1]`: mọi hình chữ nhật chạm mép trên trái đều ra đúng.

Khuôn viết: nêu **cái vẫn đúng** trước (`len` vẫn 1, test nhỏ vẫn qua, ô `[0,0]` vẫn đúng) rồi mới
nêu chỗ sai. Đúng thứ tự đó thì người đọc mới thấy vì sao mình sẽ không phát hiện ra.

## Luật 12 — mục nào mà HÌNH DẠNG của dữ liệu chính là bài học thì panel phải vẽ cấu trúc

(2026-09-06, người dùng chỉ ra khi đọc `gradient-boosting`.)

Bài đó có **9 hình mà không hình nào vẽ một cái cây**. §04 tên là *"Bước ② — Cây nông"*, panel phải
là **bảng số** ba mức độ sâu — nói bằng chữ rằng cây phải nông, không cho thấy cây nông trông ra
sao. Với `adaboost` thì lỗ hổng đó thành chí mạng: **stump là nội dung** — một nút, hai lá, một
ngưỡng, nhìn một cái là nhớ; tả bằng chữ thì mất hẳn.

Cách chữa **không phải thêm hình vào §01**. §01 sở hữu câu hỏi "vòng lặp này là gì", nhét cây vào
là hai câu hỏi một hình (luật 1 cấm), mà hình cây cũng chỉ có nghĩa **sau khi** người đọc biết
vòng lặp có bước "trồng cây". Giữ nguyên cơ chế đang chạy tốt — **ô trái sáng lên, panel phải hiện
chi tiết** — chỉ đổi panel phải từ bảng số sang **cấu trúc vẽ thật**, còn số đo tụt xuống thành
nhãn dưới mỗi hình. Hình mang cấu trúc, chữ mang con số.

Test để biết mục nào cần: **bỏ hình đi, người đọc có còn hình dung được hình dạng của thứ đang
bàn không?** Không → phải vẽ cấu trúc.

Các mục đã soi ra đang thiếu: `gradient-boosting` (stump vs cây nông vs cây sâu) ·
`decision-tree` (cây có ngưỡng thật trên nhánh) · `random-forest` (mấy cây khác nhau đặt cạnh) ·
`xgboost`/`lightgbm` (leaf-wise vs level-wise — **thuần cấu trúc**) · `trie` (cây ký tự) ·
`union-find` (cây cha–con trước/sau path compression).

## Bẫy svgkit — đừng đưa HTML entity vào `txt()`

`base.py:esc()` đổi `&` thành `&amp;`, nên `txt(..., 'A &#8212; B')` hiện **nguyên chữ**
`&#8212;` trên hình. Phải truyền ký tự Unicode thật: `—`, `√`, `→`, `⟺`, `µ`, `×`.
Entity chỉ đúng trong HTML viết tay **ngoài** svgkit. `check.py` **không bắt được** lỗi này —
chỉ ảnh chụp mới thấy, nên hình nào cũng phải qua `shot.py` một lần.

Hai bẫy nhỏ cùng họ, cũng chỉ ảnh chụp mới thấy:
- `stack()` / `band()` / `row()` mặc định `x=PANX` (cột phải). Vẽ ở cột trái **phải truyền `x=8`**,
  không thì ô nằm đè lên panel phải mà `check.py` chỉ báo "chữ đè chữ" ở nơi khác.
- Đổi `sv-d` sang `sv-s` để chữ *nhỏ lại* là sai: `sv-s` **rộng hơn** `sv-d` mỗi ký tự
  (bảng `CW`). Muốn hết tràn thì ngắt dòng hoặc viết ngắn lại, đừng đổi class.

## Overview còn nợ, dày trước (đo lại theo luật 4)

`math-foundations-overview` 286 · `classical-models-overview` 258 · `language-core-overview` 256 ·
`python-overview` 249 · `db-overview` 245 · `cs-overview` 235.

Ba overview của kệ ML (`ml-overview` · `core-concepts-overview` · `evaluation-overview`) **đã xong**
— cả ba trước đó là bài **0 hình**, và cả ba đều làm chỉ số **tăng** đúng như luật 5.

**Không sửa**: `clustering-overview` 219 · `data-structures-overview` 211 ·
`algorithms-overview` 209 · `tree-family-overview` 207 — trong khoảng, hình khớp nội dung.
`sql-basics-overview` chấm 282 nhưng **cả bài chỉ 282 chữ** — chỉ số vô nghĩa ở bài quá ngắn,
đừng sửa theo con số.


## Xếp hàng chờ theo chữ/**thiết bị** (không chỉ `<figure>`)

Mẫu số của luật 5 nên đếm **mọi thiết bị**, không riêng `<figure>` — nếu không thì bài đầy `.cmp`
và `.strip` bị chấm oan là "toàn chữ":

```python
DEV = ['<figure', 'class="strip"', 'class="flow"', 'class="cmp', 'class="stack"',
       'class="mtx"', 'class="axis"', 'class="seq"', 'class="bars"', 'class="eq"',
       'class="grid2"']
```

Hàng chờ 01→05 **kệ 02-python đã hết** — ba bài dày nhất (`memory-model-mutability`,
`memory-management-gc`, `iterator-generator`) đều đã qua luật 8, và cả ba đều làm chỉ số **tăng**
(300→314 · 300→318 · 298→326), đúng như luật 5 nói.

Bài trong 01→05 **không có `<figure>` nào** (đo lại sau `hash-map`, dày trước):
`greedy` 164. (`os-overview` 142 nằm ở kệ 03, ngoài phạm vi đợt này.)

Rà lại toàn bộ 115 bài 01→05 (2026-09-06) thì hàng chờ **rộng hơn nhiều** so với danh sách 0 hình:
19 bài nhóm A (thiếu hình ở §01, hoặc SVG vẽ tay không có số), 42 bài nhóm B (hình đúng, thiếu
số đo), 32 bài đạt. Đừng lấy danh sách 0 hình làm "phần còn lại" — nó bỏ sót gần hết kệ ML.

Nối sang [[bo-ve-hinh-svgkit]] (bẫy khi vẽ), [[quy-uoc-viet-overview]] (khuôn chữ),
[[it-chu-nhieu-hinh]] (cách đo).

## Đợt "model rõ hình + loss function" (2026-09-06)

Yêu cầu: hình rõ, **không overlap chữ/hình**, mỗi bài model có mục **Loss function** chú thích
từng khối công thức, hình cấu trúc dữ liệu rõ, **bỏ hẳn "Dùng ở thư viện nào"**.

Xong: `adaboost` · `svm` · `knn` · `naive-bayes` · `ridge-lasso-elasticnet` ·
**`lightgbm`** (3 hình sinh: `lg-s1` 352 · `lg-loss` 586 · `lg-tree` 634; mục thành
01 Mental model · 02 Loss function · 03 Mọc theo lá · 04 GOSS và EFB · 05 Đánh đổi · 06 Lỗi
hay gặp · 07 Hỏi đáp; hex còn đúng `#14110E`) ·
**`tree-family-overview`** (4 SVG vẽ tay → sinh: `tf-s1` 410 · `tf-tree` 290 · `tf-time` 450 ·
`tf-two` 578; 155 hex → 0; `.bars` bịa 100/73/88% → số đo thật).

**Số đo dùng chung cho cả nhóm tree** (`/tmp/tf/m1.py`, thuần Python, 400 train / 4.000 test,
nhãn hai lớp, DGP phi tuyến có tương tác `3*x1*x2`):

| | train | test |
|---|---|---|
| một cây sâu | 100% | **64,8%** |
| random forest | 100% | **70,5%** |
| boosting stump, 300 cây | 75,2% | **73,8%** |
| boosting depth 3, 150 cây | 89,5% | 72,8% |

Bất ổn của cây: bỏ 10% dòng rồi trồng lại **hai lần** → hai cây đoán khác nhau **30,1%** số dòng
test (trung bình 45 cặp); cùng phép đó lên rừng chỉ còn **17,0%**.

**Bẫy**: probe bất ổn đầu tiên đo *cột tách ở gốc* — ra `[(3,20)]`, giống hệt 20/20 lần, nên
**không chứng minh được gì**. Cây đổi ở **tầng dưới**, không ở gốc. Muốn cho thấy bất ổn thì đo
**% dự đoán lệch nhau giữa hai model**, đừng đo cấu trúc ở gốc.

`check.py` thiếu bề rộng cho lớp `sv-n` → mọi SVG vẽ tay dùng lớp đó làm nó chết. Đã vá bảng `W`.

### Nhóm tree-models: đủ 6/6 bài có mục Loss function (2026-09-06)

`xgboost` · `gradient-boosting` · `decision-tree` · `random-forest` thêm mục **Loss function**
(cùng `adaboost`, `lightgbm` đã có từ trước). Mỗi mục = 1 hình sinh + 3 gạch `.why`, và
**mỗi hình phải có một bảng đo thật** — chỉ có số đo mới cho thấy loss chọn khác nhau thì hỏng
kiểu gì. Đo thuần Python, không sklearn.

- **xgboost** (`/tmp/xg`, `xgb-loss` H=702, chèn thành §03, mọi mục dồn xuống 12): tách objective
  ra ba khối màu (xấp xỉ bậc hai · γ·T · ½λΣw²) rồi mới giải ra `w*` và `gain`. Bảng λ/γ (400 mẫu,
  80 cây, sâu 6, σ=1,2): λ=0/γ=0 → RMSE test **2,852**, λ=20 → **2,606** mà lá vẫn 24,8 (từ 25,6);
  γ=10 → **3,282** và lá tụt còn 5,6. **Chuyện của bài**: λ ghìm ĐỘ LỚN giá trị lá, γ đổi HÌNH cây.
  Chỉnh λ trước.
- **gradient-boosting** (`/tmp/gb`): không tách mục mới — đổi tên §06 "Vì sao gọi là gradient" →
  **Loss function** và nối bảng đo vào cuối chính SVG cũ (viewBox 358 → 560). Đo MSE/MAE/Huber trên
  cùng 500 mẫu: nhãn sạch thì ba loss ngang nhau (2,038 / 2,206 / 2,055) — **bắn hỏng 5% nhãn** thì
  MSE tụt về 2,417 còn Huber chỉ 2,089. Đổi loss chỉ đáng công khi dữ liệu bẩn.
  *Bẫy*: lần chạy đầu MAE/Huber TỆ HƠN MSE cả trên dữ liệu bẩn — vì giá trị lá vẫn lấy **trung
  bình** phần dư. Loss phi-MSE phải đặt lại giá trị lá (MAE → median, Huber → median + hiệu chỉnh),
  không thì đo ra kết luận ngược.
- **decision-tree** (`/tmp/dt`, `dt-loss` H=644, §06, tổng 14 mục; id là `dtree-sN` chứ không phải
  `dt-sN`): câu chốt là **cây không có loss toàn cục** (tìm cây tối ưu là NP-hard), nó tối ưu độ lẫn
  từng nút. Vẽ 3 đường cong impurity theo p, chú giải bằng **đoạn kẻ + nhãn xếp dọc trong góc**
  (nhãn đặt cạnh đường cong thì luôn đè lên đường khác). Đo: Gini sâu 6 → 25 lá / **74,3%**;
  entropy → 24 lá / 72,8% (không đáng kể); **sai số phân loại → tắc ở 6 lá / 70,5%, bỏ hãm cũng
  không mọc thêm** — bằng chứng vì sao không lấy thẳng thứ mình muốn tối đa làm tiêu chí chia.
- **random-forest** (`/tmp/rf`, `rf-loss` H=618, §06, tổng 13 mục): rừng **không có objective
  riêng**, nên mục này mổ sai số bình phương = bias² + variance. Đo bằng **20 lần huấn luyện lại
  trên 300 mẫu mới, chấm trên cùng 600 điểm sạch**: một cây 5,839/5,627 → rừng 100 cây
  **5,365/0,997** (bias đứng yên, variance còn 1/5,6). Dòng đối chứng **stump**: variance cũng
  xuống 1,490 nhưng bias² vọt lên 8,815 — rừng lấy nửa lợi mà không trả nửa giá.
  `max_features`=2 → variance 0,603 nhưng bias 5,830, tổng gần như không đổi.
  Tiện tay sửa nhãn `trồng nhiều cây, ép chúng KHÁC NHAU` (10 chỗ) → `ép các cây KHÁC NHAU`: nó
  tràn từ cột trái sang tiêu đề cột phải ở x=372 trong mọi hình bản đồ của bài.

**Luật rút ra cho các bài còn lại**: `check.py` không bắt được chữ cột trái tràn sang cột phải
(vẫn trong viewBox). Sau khi sửa hình bản đồ nhiều panel, quét thêm bằng tay:
`x < 372 and x + len(text)*w > 366`.

### Nhóm classical-ml + clustering + dimensionality: đủ mục Loss function (2026-09-06)

Tiếp sau tree-models. Kết quả: cả `05-classical-ml` (7 bài), `07-clustering` (4 bài) và
`08-dimensionality` (1 bài) đều có mục Loss function có bảng **đo thật** chống lưng.

**Đã làm mới:**

- `logistic-regression` — §02 đổi tên thành *Loss function — sigmoid và log loss*, và
  **hình `lr-loss.svg` đặt ở §03**, chỗ bài đang khẳng định "MSE giết tín hiệu học" mà chưa có
  số nào. Đo: gradient descent thuần, 800 train / 4.000 test. Từ `w = 0` thì log loss 0,2738 và
  MSE 0,2747 — **ngang nhau**, đó là lý do sai lầm này sống dai. Từ `w = ±8` (sigmoid bão hoà)
  thì log loss vẫn về 0,2738 còn MSE kẹt ở 1,0357. Cũng đã quét sạch 9 màu hex hardcode.
- `linear-regression`, `ridge-lasso-elasticnet`, `svm`, `knn`, `naive-bayes` — **đã có sẵn**
  mục loss function đạt yêu cầu, không đụng. `classical-models-overview` là bài bảng tra,
  không cần.
- `kmeans-clustering` — thêm §03 *Loss function* + `km-loss.svg`. inertia = Σ‖x−μ‖², hai bước
  lặp đều chỉ làm nó giảm. Đo trên 600 điểm / 4 cụm thật: inertia theo k cho khuỷu rõ ở k=4
  (3.220 → 982 rồi chững ở 884, 801, 713); và **k=4 chạy 50 lần**: tốt nhất 982,6, tệ nhất
  3.125,3 — kẹt 3/50 lần với khởi tạo ngẫu nhiên, 2/50 với k-means++.
- `dbscan` — thêm §04 *Loss function*, mà nội dung là **nó không có hàm mất mát, và không thể
  có**. Chốt bằng số: trên hình hai trăng khuyết, cách chia ĐÚNG có inertia 2.013,4 còn cách
  k-means chọn chỉ 1.818,3 — mục tiêu số đó *chấm điểm cao hơn cho câu trả lời sai*.
- `hdbscan` — thêm §03 *Loss function*: không có hàm mất mát nhưng **có điểm số để chọn**
  (độ bền = Σ(λ_rời − λ_sinh)), vì nó phải chọn cắt nhánh nào. Dựng bộ dữ liệu **hai cụm dày
  σ=0,10 sát nhau + một cụm thưa σ=1,8**: không eps nào của DBSCAN bắt được cả ba (eps 0,25 →
  cụm thưa 0%; eps 1,10 → hai cụm dày dính). HDBSCAN lấy hai cụm dày ở mức ~eps 0,58 và cụm
  thưa ở 2,68, cùng một lần chạy.
- `pca-dimensionality` — thêm §03 *Loss function*: sai số tái tạo **bằng đúng** tổng trị riêng
  bị bỏ (đo ra trùng ba chữ số: 0,302 vs 0,302), nên "giữ nhiều phương sai" và "tái tạo sai ít"
  là một bài toán. Cái giá: nhân cột **vô dụng nhất** với 100 thì PC1 nhảy 62,0% → 97,5% và
  trọng số 1,000 dồn hết vào cột đó.

**Bẫy mới ghi lại:**

- **Dựng dữ liệu để chứng minh một luận điểm thì phải chạy đi chạy lại tới khi số nói đúng
  điều mình định nói.** Bộ dữ liệu HDBSCAN phải sửa 5 lần (σ, khoảng cách hai cụm dày, dải eps)
  mới ra được bảng "không eps nào đúng". Đừng viết chú thích trước rồi ép số theo.
- **Hàm chấm điểm cũng phải chặt.** Bản đầu của `score()` cho phép hai cụm thật cùng khớp vào
  một cụm tìm được, nên báo "3/3 đúng" ở cả những eps đã gộp hai cụm — phải thêm `used` set.
- Số lớn trong bảng phải chấm nghìn kiểu Việt: `'{:,.1f}'.format(v).replace(',','#').replace('.',',').replace('#','.')`
  (11.547,2 chứ không phải 11547,2).
