---
name: chuan-bai-mau
description: "Mười luật viết một bài đạt chất lượng — rút ra từ Random forest, luật 1 rút ra từ Memory management & GC; dùng để viết mới và sửa bài cũ"
metadata:
  type: feedback
updated: 2026-09-14
---

Ngày 2026-09-03, sau khoảng mười lượt review liên tiếp riêng bài
[Random forest & bagging](../../../content/05-machine-learning/06-tree-models/random-forest/index.html),
người dùng chốt: *"hãy coi đây là 1 bài chất lượng"* và yêu cầu sửa các bài đã viết theo nó.

**Vì sao.** Trước đó mỗi lượt sửa chỉ chữa một triệu chứng (chữ nhiều quá, hình rối, bullet dài,
công thức khó). Bài random-forest là chỗ đầu tiên mọi thứ cùng đúng một lúc, nên nó thành
**thước đo cụ thể** thay cho các nhận xét rời rạc — có số để đo, không phải cảm tính.

**Số đo của bài mẫu:** 2.577 chữ · 21 hình · **123 chữ/hình** · 43 bullet, trung bình **14,7 từ**,
dài nhất 24 · 13 mục · **0 khối `<pre>`**.

**Nhưng `random-forest` không phải mẫu của luật 1** — nó vẫn để hình lơ lửng dưới lede và có mục
*Tổng kết một hình* ở cuối, tức bản trước khi luật 1 ra đời. Nó là thước đo cho **mật độ hình,
độ dài bullet, độ sâu**; mẫu cho luật 1 là
[Memory management & GC](../../../content/02-python/02-language-core/memory-management-gc/index.html).

## Mười luật

### 1. Mục 01 = bài này là gì + mental model, trong đúng một mục

**Mental model và "hình tổng kết" là một thứ**, không phải hai. Mental model là cách người học
hiểu trong đầu; hình là cách vẽ cách hiểu đó ra. Nên cả bài chỉ có **một** hình đó, đặt ở
**mục 01** — không có mục tổng kết ở cuối bài nữa.

*(2026-09-05, người dùng chốt: "về bản chất nó là 1". Trước đó memory ghi hai mục riêng và coi
mental-model-lên-đầu là ngoại lệ cho bài cheatsheet — luật đó đã bỏ, giờ áp cho mọi bài.)*

**Mục 01 không bị hình chiếm chỗ — nó làm cả hai việc.** `CLAUDE.md` chốt khuôn *Bài kỹ thuật* mở
bằng *Vấn đề nó giải*, và bài `memory-management-gc` đã dính lỗi ngược lại: mở thẳng vào cơ chế
nên *"đọc mãi không hiểu GC là gì"*. Thứ tự bắt buộc trong mục 01:

1. **câu định nghĩa** — thứ này là gì, sinh ra để giải vấn đề gì (viết đủ chữ nếu tên bài viết tắt);
2. **hình mental model** ngay dưới;
3. `figcaption` chỉ nói **cách đọc hình**, không kết luận hộ.

Tên mục **chốt là `Mental model`** (2026-09-06, người dùng chốt sau khi thấy §01 đang có năm cách
đặt tên khác nhau trên 115 bài: *Ý tưởng* 23, *Vấn đề* 17, *X là gì* 12, *Mental model* 4, còn lại
mỗi bài một kiểu). Năm cái tên cho cùng một vai trò thì người đọc không nhận ra §01 luôn là cùng
một thứ. Ràng buộc cũ vẫn giữ nguyên: hình phải nằm **trong** mục đó. Đổi tên **khi chạm từng
bài**, đừng mở một đợt sửa 115 file chỉ để đổi chữ.

**Hình nằm *trong* mục 01, không lơ lửng dưới lede.** Sáu bài `06-tree-models` đang đặt
`figure.gist` ở ngoài mọi mục — mục lục không trỏ tới được, và nó tách khỏi câu định nghĩa. Đó là
di sản, không phải mẫu.

**Hình phải có cả cấu trúc lẫn flow.** Vẽ mỗi flow thì người đọc biết đường chạy mà không biết
hệ thống gồm những gì; vẽ mỗi cấu trúc thì biết có những bộ phận nào mà không biết chúng nối
nhau ra sao. Một hình phải trả lời **cùng lúc** hai câu:

- **gồm những bộ phận nào** — các nhánh, các tầng, thứ nào chứa thứ nào;
- **chạy theo đường nào** — điều kiện nào dẫn sang nhánh nào, kết thúc ở đâu.

Khung tối thiểu (ví dụ người dùng đưa cho bài GC): gốc là hệ thống → rẽ nhánh thành các bộ phận
→ mỗi nhánh ghi **điều kiện kích hoạt** → mũi tên xuống **kết quả** của nhánh đó.

```
        Python Memory Management          ← gốc: hệ thống đang nói tới
                   │
          ┌────────┴────────┐             ← cấu trúc: có mấy bộ phận
          ▼                 ▼
   Reference Counting   Cyclic GC
          │                 │
     refcount = 0     circular cycle      ← flow: điều kiện kích hoạt
          │                 │
          ▼                 ▼
      deallocate         collect          ← flow: kết quả
```

**Bản đồ 3–5 ô — ô là nhánh của khái niệm, không phải mục của bài.** Bốn bài đã làm đều dùng bản
đồ **4 ô** phục vụ **8–10 mục**: nhiều mục cùng soi một ô, đó là bình thường. Đừng đọc ngược thành
"bài 12 mục thì bản đồ 12 ô". Quá 6 ô là dấu hiệu **bài nên tách đôi**, không phải hình nên to ra.

**Mỗi mục sau bóc ra đúng một ô.** Hình được vẽ lại **nguyên xi ở mọi mục**; ô đang học đủ màu,
phần còn lại xám, và một đường gạch nối sang panel phóng to bên phải. Người đọc học cách đọc hình
**đúng một lần**, và luôn biết mình đang đứng ở đâu.

Cài bằng một hàm `frame(hl)` trả về danh sách phần tử — thêm mục mới chỉ là gọi với ô khác,
không vẽ lại bố cục. Mẫu:
[Memory management & GC](../../../content/02-python/02-language-core/memory-management-gc/index.html).

**Lab cũng là một ô phóng to**, không phải hòn đảo riêng. 43 bài có `lab.js`; lab nào không chỉ
được ra nó đang chạy ô nào của bản đồ thì hoặc lab lạc đề, hoặc bản đồ thiếu một nhánh.

**Đây là thứ tự học, không phải quy ước vẽ hình.** Người dùng nghiệm thu: *"1 hình mental, xong
bóc tách dần nó rất liên kết tuần tự và dễ hiểu, đúng như ý tưởng học dễ, tuyến tính mà tôi cố
gắng truyền tải"*. Trước khi học một khái niệm, người đọc đã nhìn thấy ô của nó và biết nó nằm
cạnh cái gì — không mục nào rơi từ trên trời.

**Hệ quả về cách soạn: vẽ hình trước, dàn ý là hệ quả.** Thứ tự các mục phải đọc ra được từ chính
hình đó. Bố cục không gợi ra được một đường đi tuyến tính thì **hình sai, không phải dàn ý sai**.

#### Hai loại bài không áp luật 1 — 39/127 bài

| Loại | Số bài | Vì sao |
|---|---|---|
| `*-overview` | 19 | bản thân bài **đã là** bản đồ của cả nhóm; 15 bài chỉ 2–4 mục, "mỗi mục một ô" vô nghĩa |
| kệ `01-dsa` | 20 | `CLAUDE.md` chốt khuôn riêng: mục 01 = 1 hình + 1 câu chốt, đa số mở bằng *Ý tưởng* |

*(3 bài `01-dsa` là `*-overview` nên đếm một lần — 39 chứ không phải 42.)*

**Đo "bài này đã theo luật 1 chưa" bằng markup, không bằng tên mục:** `<section id="…-s1">` phải
chứa `figure class="gist"` **và** số `<svg>` của bài ≥ số mục nội dung. Đếm bằng tên mục
*Mental model* sẽ trượt (`transaction-isolation` đặt tên mục 01 là *Transaction là gì*), còn đếm
mỗi `gist` thì lọt bài mới làm được nửa — có bản đồ ở §01 nhưng các mục sau chưa bóc ô nào.

Hai loại này vẫn giữ **một hình ở mục 01**, chỉ bỏ phần "vẽ lại bản đồ ở mọi mục".

#### Bốn điều kiểm chứng được ở bài 16 mục — [[bai-hoc-soan-noi-dung]]

Làm thí điểm `transaction-isolation` (16 mục, bài khó nhất kệ 01→05) rút ra, áp cho mọi bài sau:

- **Mỗi *mục* một hình, không phải mỗi *ô* một hình.** 6 ô phục vụ 14 hình; ô `iso` có ba mục
  soi vào, mỗi mục một panel phải khác nhau. Đếm hình theo mục, không theo ô.
- **Cách đọc bản đồ chỉ nói một lần**, ở `figcaption` mục 01. Caption các mục sau chỉ nói phần
  panel phải. Lặp câu hướng dẫn ở mọi hình là rác — bài này từng lặp 11 lần, ~275 chữ.
- **Hình thay được `<pre>` thì xoá `<pre>`.** Luật 2 áp cho cả khối code, không riêng văn xuôi.
- **Vẽ hình bắt được lỗi phân loại của dàn ý.** Mục *"Bốn hiện tượng dị thường"* gộp lost update
  chung với ba hiện tượng đọc; bản đồ tách hai nhánh ĐỌC/GHI nên lỗi lộ ra, đã tách thành hai
  mục. Đọc chữ không thấy lỗi này.

Bộ công cụ `frame.py` / `check.py` / `apply.py` chép lại được — mô tả ở
[[bai-hoc-soan-noi-dung]]. `check.py` (đo bề rộng chữ, bắt tràn khung) bắt được lỗi mà
ảnh chụp không lộ; chạy nó trước khi chụp.

#### Bài là một chuỗi biến đổi — kiểm chứng 2026-09-10 ở `logistic-regression`

Không phải bài nào cũng có "gốc chứa các nhánh". Bài mà nội dung là **một mẫu đi qua nhiều chặng,
mỗi chặng đổi nó thành thứ khác** (logistic regression, request lifecycle, RAG, forward pass) thì
bản đồ là **flow ngang một hàng**, không phải cây. Người dùng nghiệm thu: *"chuẩn này đây mới là
cái tôi luôn muốn ở 1 mental model"*.

Mất bốn lượt mới ra, và **ba lượt đầu đều sai theo cùng một kiểu: ô chỉ chứa chữ**. Lượt 1 vẽ năm
ô rời cạnh nhau — đúng nội dung, sai quan hệ. Lượt 2 nối thành flow nhưng ô chỉ ghi tên và một
câu chú. Lượt 3 thêm công thức vào ô, vẫn là chữ. Lượt 4 mới đúng: **mỗi ô là một đồ thị thật**.
Yêu cầu gốc của người dùng ngay từ đầu là *"ảnh flow nhìn là hiểu"* — chữ trong ô không phải hình.

Sáu thứ làm nên ô đúng, thiếu cái nào cũng hụt:

1. **Ba dòng cố định mỗi ô: công thức · số ra · miền giá trị.** `z = w·x + b` / `= 0,85` /
   `−∞ … +∞`. Công thức ở **dạng rút gọn nhất đúng cho ca đang vẽ** (`L = −log p`, không phải hai
   số hạng đầy đủ) — dạng đủ để ở mục chuyên trách.
2. **Miền giá trị là dòng quan trọng nhất** và là thứ dễ quên nhất. `−∞…+∞` → `0…1` → `0 hoặc 1`
   nói ngay **vì sao phải có chặng sau**: số ra khỏi chặng này chưa dùng được vào việc kia. Bỏ
   dòng này thì flow thành chuỗi công thức nối nhau, không còn lý do tồn tại.
3. **Đồ thị thật trong ô**, không phải chữ trong khung: đường thẳng cắt trục 0, đường cong sigmoid
   giữa hai vạch 0/1, trục xác suất có vạch ngưỡng, cặp thanh tỉ lệ.
4. **Một chấm probe duy nhất, cùng một mẫu, xuất hiện ở mọi đồ thị.** Đây là thứ khiến mắt bám
   theo được: chấm nằm trên đường thẳng → rơi lên đường cong → đáp vào nửa phải trục ngưỡng.
   Các đồ thị rời nhau mà không có chấm chung thì vẫn là mấy hình cạnh nhau, không phải một luồng.
5. **Hình tự nói ra lập luận của bài.** Đường thẳng vẽ vượt khỏi khung, đường cong bẹt vào hai
   vạch 0/1 — người đọc thấy lý do phải bọc sigmoid *trước khi* đọc mục nói về nó. Đó là phép thử:
   xoá hết chữ trong hình mà vẫn còn lập luận thì hình đúng.
6. **Tách đường chính khỏi nhánh rẽ.** `log loss` và `odds` không phải chặng của luồng — chúng rẽ
   **xuống** từ `p`, có nhãn *lúc học* / *đọc hệ số*. Xếp ngang hàng là nói dối về cấu trúc: người
   đọc tưởng phải đi qua log loss mới ra được nhãn.

Đánh số các ô **theo thứ tự mục của bài**, không theo thứ tự nhìn — nhánh rẽ nằm dưới nhưng mang
số của mục nói về nó, nên dãy số trên hình có thể nhảy cóc so với đường mắt đi. Nhờ vậy `ul.why`
chỉ cần một dòng *"mỗi mục sau bóc một ô, theo đúng số trên hình"*.

**Hệ quả về chữ trong bài.** Hình đúng thì `p.key` của mục 01 rút còn một dòng
(`x → z → p, rồi mới tới nhãn`), và câu giải thích *vì sao đổi tên `ŷ` thành `z`* ở mục 02 rút
còn một câu. Người dùng chốt: *"tối thiểu chữ của bài mà vẫn hiểu luồng"* — hình gánh phần giải
thích, chữ chỉ còn phần hình không vẽ được.

**Bẫy đã dính khi làm:** `class="gist scrollx"` thì `soat.py` phép 8 không nhận (nó tìm đúng chuỗi
`class="gist"`). Flow ngang vừa khung thì bỏ `scrollx` — chỉ thêm khi `svgkit/check.py` báo tràn.

#### Flow ngang là mặc định — kể cả bài đệ quy · 2026-09-14 ở `decision-tree`

Bản đồ §01 đầu tiên của `decision-tree` vẽ đúng **cấu trúc**: khung "một node" ở giữa, hai nhánh
con trỏ ngược lên nó, một ô đỏ dưới cùng, và cột phải liệt kê bốn ý. Đúng logic, nhưng người dùng
bác: *"cái mental model hãy giống kiểu flow giống bài Logistic regression ý"*.

> **Mặc định của mọi bản đồ §01 là flow ngang bốn chặng, không phải sơ đồ cấu trúc.** Chỉ đổi khi
> bài thật sự không có luồng nào cả.

Cây là cấu trúc đệ quy, nên phản xạ là vẽ hộp lồng hộp. Nhưng **cái người đọc cần hiểu không phải
cây trông thế nào — mà dữ liệu đi qua cái gì để thành cây**. Bốn chặng đó có thật:
`bảng vào → chấm điểm mọi ngưỡng → chia đôi → leaf mang nhãn đa số`.

Hai điều chỉnh so với khuôn `logistic-regression`:

- **Đệ quy vẽ bằng một mũi tên đứt quay ngược từ chặng cuối về chặng ①**, nằm *dưới* hàng ô, có
  nhãn. Không lồng hộp. Flow vẫn đọc trái sang phải, vòng lặp chỉ là một nét thêm.
- **Cái phá luồng thì tách ra khỏi hàng**: "đệ quy không tự dừng" là dải đỏ **dưới** cả flow, vì
  nó không phải một chặng — nó là lý do hyperparameter tồn tại.

Bỏ luôn **cột "bốn ý — hết" bên phải**. Nó là bản tóm tắt bằng chữ đặt cạnh bản đồ: hai lần nói
cùng một điều, và làm hình rộng gấp đôi. Flow đúng thì không cần chú thích lại bằng câu.

#### Tên mục phải trùng chặng trong bản đồ §01 · 2026-09-14 ở `decision-tree`

Bản đồ §01 vẽ bốn chặng nhưng tên mục lại đặt kiểu khác (`Chia một node`, `Mọc cả cây`) — người
dùng bác: *"rất khó hiểu… title và nội dung phải thật ngắn gọn dễ hiểu, đừng bôi vẽ nhiều"*.

> **Mỗi ô trong bản đồ §01 mang nhãn `mục NN · <tên chặng>`, và tên mục là đúng cụm chữ đó.**
> Đọc bản đồ xong là biết mục nào bóc chặng nào, không phải dò lại.

`Dữ liệu vào` · `Chấm điểm` · `Chia đôi rồi lặp lại` · `Dừng — hyperparameter`. Tên mục là **danh
từ hoặc việc đang xảy ra**, không phải câu ví von.

#### Không đóng khung màu — vạch trái, chú thích trong hình · 2026-09-14

Ba lượt người dùng bác cùng một thứ: *"hơi khó nhìn"*, *"không đóng khung màu linh tinh"*. Nền mờ
+ viền màu quanh mỗi dòng chữ biến hình thành một đống ô lổn nhổn.

| Thay vì | Dùng |
|---|---|
| `<rect>` nền mờ + viền màu quanh một dòng | **vạch trái** `<rect width="3" height="20" rx="1.5">` màu ngữ nghĩa |
| chú thích thành dòng chữ **dưới** hình | **khoanh vùng nét đứt ngay trong hình**, nhãn ở góc |
| dải màu to nguyên chiều rộng làm cảnh báo | vạch trái + hai cột chữ (thuật ngữ x=14, giải thích x=238) |

Cây ba tầng ở `decision-tree` cũ phải chú thích `root · internal · leaf` bằng một dòng riêng. Sửa
thành **ba vùng nét đứt bao đúng các tầng**, nhãn `ROOT · cả bộ dữ liệu` nằm ở góc phải vùng, lề
trái ghi `DEPTH 0…3` — chú thích biến mất vì hình đã tự nói.

**Tầng INTERNAL phải có ≥2 tầng**, không thì người đọc tưởng cây chỉ sâu được một mức. Và mỗi tầng
hỏi một cột khác nhau, để thấy *mỗi nhánh tự chọn câu hỏi riêng*.

#### Phân vùng bằng dải nền, không bằng khung nét đứt · 2026-09-14

Lượt đầu khoanh vùng root/internal/leaves bằng `<rect stroke-dasharray>` bao quanh các node, nhãn
đặt ở **góc phải**. Người dùng vẫn bác: *"hình phân vùng không rõ ràng, hơi khó nhìn"*. Ba lý do:
khung nét đứt cùng màu `--rule-hi` với đường branch nên chìm; nhãn ở góc phải xa các node nó mô
tả; lại còn một cột `DEPTH 0…3` riêng ở lề trái → hai hệ nhãn cho cùng một thứ.

> **Vùng = một dải nền `--sunk` chạy hết chiều rộng + vạch màu 3px ở mép trái + nhãn nằm TRONG dải
> ở lề trái.** Không khung nét đứt, không nhãn ở góc xa.

Và **gộp hai hệ nhãn làm một**: `ROOT · depth 0` / `INTERNAL · depth 1–2` / `LEAVES · depth 3` —
bỏ hẳn cột depth riêng. Chừa lề trái ~150px cho nhãn, cây vẽ trong phần còn lại; toạ độ node tính
bằng `cx(i,n) = G + W*(i+0.5)/n` để mọi tầng tự căn giữa.

#### Gọi thẳng keyword chuẩn của lĩnh vực · 2026-09-14 ở `decision-tree`

Người dùng đọc bài xong hỏi: *"Logits · Leaves · Training algorithm · stop criteria · Inference ·
Pruning — có các cái này chưa?"*. Bài đang mô tả đúng **cơ chế** nhưng đặt tên bằng tiếng Việt tự
chế (`Chia đôi rồi lặp lại`, `Dừng — hyperparameter`) nên người học không nối được với tài liệu
tiếng Anh, và **pruning thì thiếu hẳn**.

> **Trước khi coi một bài là xong, liệt kê keyword chuẩn của chủ đề rồi soát xem bài có gọi đúng
> tên chưa** — cơ chế đúng mà tên tự chế thì vẫn là thiếu.

Sửa: `04 Training algorithm` · `05 Stop criteria và pruning`; hình §02 đặt nhãn `LEAVES`,
`INFERENCE`; thêm hẳn pre-pruning vs post-pruning (`ccp_alpha`); nói rõ leaf trả về **tỉ lệ lớp,
không phải logits**. Nêu cả khái niệm bài **không** có, để người đọc khỏi tự suy sai.

#### Hyperparameter là danh sách tra, không phải hình · 2026-09-14

Hình §05 từng có thang `max_depth = 1 / 3–10 / 20 / không giới hạn` — bốn dòng chữ đóng khung,
người dùng bác: *"không cần mấy cái thừa như hyperparam của code đâu, cứ đủ các khái niệm,
keyword core là được"* và *"tối thiểu hoá vùng cần nhìn"*.

Hình chỉ vẽ **phân loại khái niệm** (pre vs post-pruning, hai cột), còn giá trị nên đặt bao nhiêu
thì để ở `ul.why` hoặc bảng. Bỏ thang đó: viewBox 398 → 262.

#### Câu chữ trong hình: không ví von, gọi đúng tên · 2026-09-14

*"một đường = một luật"* bị bác là *"nghe cực khó hiểu"*. Đường từ root xuống leaf là một chuỗi
**điều kiện tách nhánh** — gọi đúng thế. Câu mở đầu hình kiểu *"Ba tầng, ba tên gọi — và một
đường đọc thành luật"* thì bỏ hẳn: nó chỉ là bản tóm tắt bằng chữ của thứ hình đang vẽ. Cũng đừng
lặp lại nguyên câu `.key` ngay bên trên vào trong hình.

**Còn lại loại thứ ba, chưa kiểm chứng:** bài không phân cấp mà cũng không phải chuỗi biến đổi —
`sql-join`, `feature-engineering`, `statistics`. Đề xuất cũ: gốc là **câu hỏi bài trả lời**, các ô
là **các lựa chọn / chiều đánh đổi**. Vẽ thử một bài rồi mới ghi thành luật.

### 2. Chỉ 1–2 hình dạng, lặp lại suốt bài

*"cứ đưa về hình thù dạng data bảng / cây cho thân thiện chứ không mỗi bài lại 1 hình thì rất mệt
để hiểu"*. Người đọc học cách đọc hình một lần, không phải học lại ở mỗi mục. Hình dạng chọn theo
chủ đề: DSA thì mảng + con trỏ, database thì bảng + sơ đồ quan hệ, networking thì `.seq` + `.stack`.

**Các bài cùng cơ chế dùng chung một khung hình**, cùng dữ liệu, cùng các mốc — đặt cạnh nhau là
so được từng con số. Bài chỉ khác một chi tiết thì giữ nguyên khung, **làm mờ phần giống, tô sáng
đúng ô khác** rồi phóng to ô đó. Ngược lại, cơ chế khác thật thì bố cục phải khác thật.

### 3. Bullet ngắn nhất có thể

*"nội dung các bullet cả bài cần ngắn gọn nhất, tối giản nhất"*.
Mốc: **trung bình ≤ 15 từ, không câu nào quá 25**.

### 4. Việc nối tiếp dùng `ul.steps`, ý song song dùng `ul.why`

*"mấy cái bullet này cứ bị có gạch ngang làm mất sự liên kết của mắt"*. `.steps` là số thứ tự
trong vòng tròn nối bằng một vạch dọc liền, mục cuối gắn `class="end"` thành dấu ✓. `.why` không
có gạch đầu dòng.

### 5. Không để code trong mục khái niệm

*"đừng để code ở đây"*. `<pre><code>` chỉ còn đúng chỗ của nó: bài DSA mục *Mẫu code cần thuộc*,
bài Python/SQL dạy cú pháp. Câu "gọi hàm nào của thư viện" viết thành một dòng chữ, không phải
một khối code.

### 6. Công thức dùng `.eq` + `<dl>` giải nghĩa từng ký hiệu tại chỗ

Xem [[khuon-eq-cong-thuc]]. Không ký hiệu nào được xuất hiện trước khi có nhãn của nó. Kết bằng
`<p class="read">` nói công thức **đọc ra nghĩa gì**.

### 7. Hình và lab: to, rõ, ít — đừng vẽ cho đủ bộ

Áp cho **mọi** thứ trực quan, không riêng bảng: *"hình đủ to rõ ràng, ngắn gọn, không cần cố tạo
bảng quá nhiều cột hàng, hay không cần tạo cây quá nhiều level"*.

- **To và rõ hơn là đầy đủ.** Ô lớn, viền rõ từng ô, chữ căn giữa, đọc được ở cỡ thật.
- **Chỉ giữ đúng số phần tử đủ để thấy cơ chế.** Cây minh hoạ 3 tầng là đủ nếu 3 tầng đã cho thấy
  cách chia; bảng 4 hàng là đủ nếu 4 hàng đã cho thấy phép gộp. Thêm nữa chỉ làm chữ nhỏ đi.
- **Chọn hình dạng theo dữ liệu**, không mặc định lấy bảng: dãy thì `.strip`, quan hệ cha–con thì
  cây, thứ có thứ tự thì `.axis`, luồng thì `.flow`.
- **Lab tự chạy tiếp khi đủ điều kiện** — *"cái trồng cây tự động đi khi rút đủ"*.
- **Một lab, một ý.** Lab có ba phần thì hai phần sau thường là bài nghiên cứu, không phải chỗ để
  học. Mấy dòng dưới lab nói người học **nên tự thử gì**, đừng kết luận hộ họ.

### 8. Mặt bài là cheatsheet — không đoạn văn nào quá 33 từ

*"tôi muốn phong cách như cheatsheet nhưng chi tiết hơn để học kĩ hơn"*. Mặt bài chỉ có
`p.key` + hình + bullet ngắn. Mốc: **không đoạn văn nào quá 33 từ** (toàn kho hiện là 0).

> ⚠ **`details.deep` là quy ước ĐÃ CHẾT** (TAXONOMY §A4) — cả kho đã dọn sạch, đừng dựng lại.
> Đoạn văn dài giờ xử lý bằng cách **cắt** theo [[toi-thieu-de-hieu]] hoặc **đổi thành hình**,
> không phải gập vào `<details>`.

### 9. Trình bày theo vai trò, không theo cảm tính

Độ đậm, cỡ chữ và độ sáng là **thông tin**, người đọc luôn đọc chúng thành thứ bậc. Nên chỉ được
dùng khi có thứ bậc thật; hai thứ ngang vai thì trình bày y hệt nhau.

- **Ngang vai thì cùng độ đậm.** Trong một danh sách các ý cùng cấp, mọi dòng dùng chung một cặp
  màu — dòng này `--dim` dòng kia `--faint` là vô tình dìm một ý xuống hàng phụ.
- **Chữ nhỏ và mờ không được mang kết luận.** Nhãn to mà câu bài học lại nằm ở dòng nhỏ nhất, mờ
  nhất là nói ngược với ý định.
- **Ba bậc chữ trong hình:** `sv-t` = nhãn · `sv-s` = dòng mang kết luận · `sv-d` = chú thích thật
  sự phụ (nguồn, đơn vị, ghi chú bên lề).
- **Chữ phụ dùng `--muted`, không dùng `--faint`.** Trên nền `--panel`, `--faint` chỉ đạt 3,6:1,
  dưới mốc AA 4,5:1. `--faint` để dành cho chữ **cố tình phải mờ** — ô đã bị xám hoá.
- Tìm lỗi này **bằng máy**, đừng soi từng bài: dò cặp *nhãn `sv-t` + dòng ngay dưới nó* (cùng `x`
  ±3, cách 8–26px, dài > 26 ký tự) rồi nâng dòng dưới lên `sv-s`.

### 10. `Ưu và nhược` rồi `Chọn khi nào` — cặp mục đóng phần thân bài

Chốt 2026-09-08 khi sửa `ridge-lasso-elasticnet`. Người dùng đối chiếu với `svm`: *"so với svm thì
chưa có mục ưu nhược, tôi cần bảng ưu nhược để so sánh"*, và *"Chọn khi nào thay vì Chọn cái nào
cho các bài vì có những bài 1 cái nên không nên để Chọn cái nào, và sẽ ở dưới ưu nhược"*.

**Hai mục, đúng thứ tự này, ngay sau phần cơ chế:**

| Mục | Nội dung | Khuôn |
|---|---|---|
| `Ưu và nhược` | mỗi mặt một hàng, mỗi phương án một cột | `<table>` |
| `Chọn khi nào` | mỗi tình huống một ô, nói **điều kiện dữ liệu** | `.stack` |

**Vì sao thứ tự này.** Đọc bảng xong mới biết cái giá của từng phương án; lúc đó câu *"khi nào
dùng"* mới có nghĩa. Ngược lại thì người đọc phải tin lời khuyên mà chưa thấy lý do.

**Tên là `Chọn khi nào`, không phải `Chọn cái nào`.** Bài chỉ nói về **một** thứ vẫn cần mục này
(khi nào nên dùng SVM), nhưng không có "cái nào" để chọn. Một tên dùng được cho cả hai loại bài.

**Thuật ngữ đắt phải nằm trong bảng.** *sparse* là ví dụ: nó là **nhược điểm** của Lasso, nên chỗ
đúng của nó là một hàng ở cột nhược, kèm một câu định nghĩa ngay dưới bảng — không phải một đoạn
văn rải giữa bài. Đừng né thuật ngữ bằng từ tiếng Việt tự chế (*"model thưa"*); gọi thẳng tên
tiếng Anh rồi giải nghĩa một câu.

**Nhược điểm phải nói được cái giá thật**, không phải liệt kê "chậm hơn". Ba câu đáng có sau bảng:
sparse tốt khi nào · sparse hại khi nào · và **hiểu sai hay gặp** (biến bị Lasso bỏ không phải
biến vô dụng, chỉ là biến trùng thông tin).

## Ngữ pháp của một hình: ô là kết quả, mũi tên là hành động

*"để tên các bước hành động ở mũi tên còn các ô là kết quả, ví dụ `key "user"` --`hash(key)`-->
`hash value` --`hash % size`--> `slot index`"*.

Khi ô chứa cả hành động lẫn kết quả, người đọc phải tự đoán ô nào là *cái đang có* và ô nào là
*việc đang làm*. Tách ra thì hình tự nói:

- **trong ô** — một danh từ: thứ đang cầm trên tay ở bước đó, dòng dưới là ví dụ cụ thể của nó;
- **trên mũi tên** — phép biến đổi, viết bằng `sv-l` (mono) cùng màu mũi tên.

Cài bằng `arr_r_lbl(y, x1, x2, màu, nhãn)`. Chừa khe **≥ 64px** giữa hai ô — nhãn mũi tên nằm giữa
khe, hẹp hơn thì nhãn thò sang đè khung bên cạnh.

**Luật này áp cho cả `.flow` trong HTML, không riêng SVG.** Khuôn (`style.css`, mẫu ở `kit.html`):

```html
<div class="n"><h5>Dữ liệu thô</h5><p>còn nằm ngoài kho đích</p></div>
<div class="a act"><i>Transform</i>→</div>
<div class="n ok"><h5>Dữ liệu đã sạch</h5><p>đã chuẩn hoá, tính lại</p></div>
```

- `h5` là **danh từ** — thứ đang cầm ở bước đó; `p` mô tả chính nó, không phải việc kế tiếp.
- `<i>` là **động từ**, mono, màu `--probe`, **≤ 30 ký tự**.
- Không phải hành động (`·`, `+`, `≠`, `↻`) thì để mũi tên trần, đừng gán `act`.
- **≤ 4–5 ô một flow.** 6 ô thì ô cuối rớt xuống dòng riêng, nhìn như lỗi. Gộp hai chặng vào một
  nhãn: `<i>GROUP BY rồi HAVING</i>`.
- Mobile: `.a` trần bị ẩn, nhưng `.a.act` **phải hiện** — mất nhãn là mất nửa nội dung.

**Hình phải vẽ cơ chế đang chạy, không phải ảnh chụp từng chặng.** Có mũi tên đặt tên và vòng hồi
tiếp nếu thuật toán có lặp. Bố cục tự nó nói lên cơ chế: tuần tự thì các cột nối nhau, song song
thì các cột rời nhau rồi mới gặp ở ô gộp. **Cột cuối luôn là lúc đã hội tụ** — vẽ ba bước đầu mà
chưa thấy kết quả thì hình vô nghĩa.

## Bố cục phải nói đúng quan hệ giữa các khái niệm

*"thế cái hình chưa có mô tả 1 process có nhiều thread"* — bản đồ bài `thread-process-gil` vẽ
Process và Thread thành **hai ô cạnh nhau bằng nhau**, trong khi câu định nghĩa ngay trên nó nói
*"thread là nhiều luồng chạy bên trong một process"*. Hình nói "hai thứ song song", chữ nói
"cái này nằm trong cái kia" — người đọc tin hình.

**Trước khi chọn bố cục, gọi tên quan hệ giữa các ô, rồi lấy đúng hình dạng của quan hệ đó:**

| Quan hệ | Bố cục bắt buộc | Sai nếu vẽ thành |
|---|---|---|
| A **chứa** B (process ⊃ thread, class ⊃ method) | hộp lồng hộp, B nằm trong khung A | hai ô cạnh nhau |
| A **rồi tới** B (pipeline, boosting) | các cột nối nhau bằng mũi tên có tên | các ô rời nhau |
| A **hay** B (hai lựa chọn thay thế nhau) | hai ô cạnh nhau, cùng cỡ | ô này trên ô kia |
| A **dựng trên** B (bốn trụ OOP trên cơ chế tra tên) | B một hàng trên, A xếp dưới, có mũi tên xuống | lưới phẳng không mũi tên |
| A **sinh ra** B (bộ nhớ chung → race condition) | mũi tên đi từ A xuống B | đặt B cạnh A không nối |

Kiểm nhanh, làm ngay sau khi vẽ xong bản đồ: **che hết chữ, chỉ nhìn khung và mũi tên — có đọc ra
được câu định nghĩa ở mục 01 không?** Không ra thì bố cục sai, không phải chữ sai. Đây là lỗi
`check.py` **không bắt được**: hình đo ra hoàn toàn hợp lệ, chỉ có nghĩa là sai.

Hệ quả cho ô con: ô nằm trong ô khác thì **kích cỡ phải nói lên vai trò** — hộp ngoài giữ nguyên
màu và bề rộng của nó, ba ô con bên trong nhỏ hơn, chỉ một dòng chữ. Đừng vẽ ô con to bằng ô cha.

## Đặt tên nhãn: đọc phát hiểu, không cần suy

Luật *"đầu mục là danh từ, đọc là hiểu"* của `CLAUDE.md` áp cho **nhãn trong hình** y như cho đầu
mục. Mỗi ô là một cặp **nguyên nhân → cách chữa**, viết như câu nói thường:

| Mơ hồ | Đọc phát hiểu |
|---|---|
| `HAI KEY CÙNG MỘT Ô` | `Hai key ra cùng một slot` · *thì dò sang slot khác — probe sequence* |
| `XOÁ ĐỂ LẠI VẾT` | `Xoá làm đứt đường dò` · *thì để lại vết xoá — tombstone* |
| `ĐẦY 2/3 THÌ NHÂN ĐÔI` | `Bảng chật thì đường dò dài ra` · *thì nhân đôi bảng — resize* |

Hoa toàn bộ chỉ dành cho **nhãn nhóm**; tên một ô viết chữ thường như câu nói — hoa toàn bộ vừa
khó đọc vừa ép rút ngắn tới mức mất nghĩa.

**Nhãn là *nhãn*, không phải câu văn** — câu văn để `figcaption`. Mốc thực dụng: nhãn phải ngắn
tới mức không cần đo; dài quá thì tách hai dòng, hoặc đẩy hẳn xuống `figcaption`.

Nhưng **chữ trong SVG không tự xuống dòng, nên phải dùng hết bề ngang có được**: panel rộng 500px,
`sv-t` 12,5px chứa ~72 ký tự một dòng — ngắt sớm ở 45–50 ký tự là bỏ trống một phần ba panel vô cớ.
Đo trước khi ngắt: `len(chuỗi) × cỡ chữ × hệ số` phải vừa trong bề rộng panel.

## Câu lede

- **Không được có ẩn dụ cần giải thích thêm.** Viết *"cả bài gói trong một bản đồ hai nhánh"* là
  bắt người đọc hỏi lại "hai nhánh là gì" ngay câu đầu.
- Khuôn dùng được: **(1) hai khái niệm gốc là gì · (2) hệ quả trực tiếp của chúng · (3) tên bài
  nằm ở đâu trong đó** — không nhắc chữ "bản đồ", không hứa hẹn về cấu trúc bài; hình ngay dưới
  đã nói giúp phần đó.
- **Ý nào liệt kê được thì cho thành bullet.** *"mọi thứ gãy gọn là tốt nhất"* — lede dạng *"chỉ
  làm một trong hai việc — A, hoặc B"* thì cắt ở dấu hai chấm rồi đẩy A, B xuống `ul.ledelist`.
  Luật này áp cho **mọi** chỗ: đếm được thì xuống dòng được.
- **Bài có chữ viết tắt trong tên phải viết đủ chữ đó ra ở lede**, và mục 01 phải trả lời *"thứ
  này là gì"* trước khi bất kỳ mục nào nói *"nó chạy thế nào"*. Hình đẹp không thay được câu
  định nghĩa.
- Panel của hình mở bài **chỉ chứa các ý, không chứa "câu trả lời thuộc lòng" bằng tiếng Anh** —
  nó trùng nghĩa với dòng ý ngay dưới, mà lại chiếm chỗ đẹp nhất và bắt người đọc đổi ngôn ngữ
  ngay giây đầu.

## Thuật ngữ: gọi đúng tên, đừng gọi bằng từ đời thường

*""ô" thì dùng từ cho đúng thuật ngữ"*. Người đọc đi phỏng vấn cần **đúng chữ mà người phỏng vấn
dùng** — gọi slot là "ô" thì lúc đọc hiểu được, gặp lại từ khoá ở chỗ khác là không nhận ra.

Danh từ chuyên ngành giữ tiếng Anh **xuyên suốt**: nhãn trong hình, chữ trong lab, văn xuôi, tiêu
đề mục. `CLAUDE.md` đã có luật này cho tên bài — nó áp cho cả bên trong bài. Chi tiết ở
[[thuat-ngu]].

Và khi hình mental model cũng có "ô" theo nghĩa hình học thì càng phải tách hai từ ra, không dùng
chung một chữ cho hai nghĩa.

## Độ sâu: dừng ở mức phỏng vấn hỏi

*"chỉ cần core mà phỏng vấn bigtech cho swe ai ml engineer hay hỏi, còn chi tiết từng phần nào
dùng bit nào thì giống thiết kế tối ưu phần cứng quá… vẫn đủ hiểu cả flow nhưng cái gì không core
thì không đi sâu."*

Ranh giới đi qua **mức trừu tượng**, không qua độ dài:

| Bỏ — mức cài đặt | Giữ — mức khái niệm |
|---|---|
| `hash & (size-1)`, "cắt bit thấp", size là lũy thừa của 2 | `hash % size` ra số slot; CPython viết thành phép AND cho nhanh |
| `perturb >>= 5`, PERTURB_SHIFT, vì sao là số 5 | probe phải **xác định** và **đi hết bảng** — gọi tên `perturb` là đủ |
| primary vs secondary clustering, LCG chu kỳ đầy đủ | Python không dùng `i+1` vì nó dồn key thành dải liền kề |

Test nhanh: **câu này có xuất hiện trong một buổi phỏng vấn SWE/ML không?** Không → bỏ, hoặc gập
vào `details.deep` viết ở mức "biết tên là đủ". Chi tiết bỏ đi phải **thay bằng lý do**, đừng để
lại lỗ: "cắt bit thấp nên trùng slot" → "nén một khoảng rất lớn xuống 8 chỗ nên trùng là tất yếu".

Cách kiểm: `grep` các dấu vết mức-cài-đặt rồi hỏi từng chỗ câu hỏi trên. Áp cả vào **hình** — ô
giữa hình không in công thức, mà nói **công thức đó làm gì**.

## Lỗi hình dễ dính — cả sáu đều im lặng

Markup đúng hoàn toàn, chỉ ảnh chụp hoặc script kiểm mới lộ:

- **`viewBox` thấp hơn hình** → ô cuối bị cắt cụt. Hàm sinh khung phải **trả về `y` cuối cùng**,
  đừng chép số cứng.
- **Nhãn mũi tên đè khung bên cạnh** → chừa khe đủ rộng, hoặc rút nhãn.
- **Hình nói dối** → số nào hình khoe cũng phải `assert` trong script sinh, hoặc tính lại từ chính
  thuật toán của lab. Đã dính: hình LightGBM vẽ hai cây khác số lá trong khi bài nói "cùng ngân
  sách lá".
- **Dấu tiếng Việt rơi trong font mono** → `sv-l` và `sv-h` (JetBrains Mono) vẽ `số` thành `sô´`.
  Hai class đó **chỉ dùng cho chữ không dấu**. Nhãn hoa có dấu dùng `sv-hv`, nhãn thường có dấu
  dùng `sv-d`/`sv-t`. Cách chắc ăn: để `txt()` **tự đổi class** khi thấy ký tự có dấu.
- **Script ghi đè `fill` về `--faint`** → mặc định CSS đã là `--muted` nhưng script sinh lại ép
  xuống. Cho `txt()` tự nâng `--faint` → `--muted`.
- **`<h2>` chứa `<code>`** → `app.js` dựng mục lục bằng `textContent` nên thẻ rơi thẳng vào
  sidebar. Tiêu đề kiểu `__hash__ & __eq__` viết dạng chữ trơn.

**Soát overlap bằng máy, đừng soát bằng mắt.** Ước lượng bề rộng chữ từ class (`sv-t` ≈ 0,55 × cỡ
chữ mỗi ký tự, `sv-d` ≈ 0,52, `sv-l` ≈ 0,60, `sv-h` ≈ 0,72) rồi kiểm năm thứ: chữ đè chữ · chữ thò
khỏi `rect` bao nó · `rect` đè `rect` không lồng nhau · tràn khỏi `viewBox` · vạch cắt qua chữ.
Nhớ **đăng ký class mới vào bảng bề rộng** của script kiểm, thiếu là nó `KeyError` chứ không cảnh báo.

Chụp để soát: render **một hình một trang** (nhúng `assets/style.css` vào file tạm) rồi
`google-chrome --headless --force-device-scale-factor=2 --screenshot` — phóng to gấp đôi, không có
chữ xung quanh, lỗi 2–3px hiện ra ngay. Script sinh phải **idempotent** (xoá hình cũ trước khi
chèn) để chỉnh toạ độ rồi chạy lại thoải mái.

## Margin: chrome hẹp lại để hình rộng ra

*"margin hơi to, khiến nội dung như hình vẽ đôi khi bị hẹp chỗ"*. Hình SVG có `viewBox` cố định
nên cột nội dung hẹp đi bao nhiêu là hình thu nhỏ bấy nhiêu — margin ăn thẳng vào cỡ chữ trong hình.

| | cũ | nay |
|---|---|---|
| `.wrap` max-width · padding | 1240 · 28 | **1320 · 22** |
| `.cols` cột mục lục · gap | 186 · 32 | **172 · 26** |
| `nav.toc` margin-left (≥1280px) | −64 | **−52** |
| padding ngang mobile | 20 | **17** |

Đổi mấy số này thì soát lại hai mốc: **1400px** (mục lục không chồng lên bài) và **490px** (không
tràn ngang).

## Áp dụng thế nào

Trước khi sửa một bài, đo bằng script ở [[trinh-bay-bai]] và script dưới đây; sửa xong đo lại.
**Đo lại sau mỗi lô, đừng chỉ đo một lần ở cuối đợt** — bản vừa viết lại cũng hay vượt ngưỡng.

Thứ tự việc: (1) bullet dài → cắt; (2) `<pre>` khái niệm → bỏ hoặc đổi thành hình; (3) hình lạ →
đưa về hình dạng chính của bài; (4) công thức trần → `.eq`; (5) chưa có hình mental model ở mục 01
→ vẽ (bản đồ 3–5 ô trước, dàn ý sau). Không viết thêm chữ mới trừ khi đang bù kiến thức thiếu.

```python
lis = re.findall(r'<li[^>]*>((?:(?!</?li).)*?)</li>', s, flags=re.S)
ws = [len(re.sub(r'<[^>]+>', ' ', x).split()) for x in lis]   # tb ≤15, max ≤25

# đoạn văn *mặt bài*: bắt buộc bỏ <details> và <figure> trước,
# không thì <text> trong SVG bị đếm thành văn xuôi và ra số ảo
b = re.sub(r'<(details|figure).*?</\1>', '', art, flags=re.S)
# (?!re\b) là bắt buộc — thiếu nó thì <pre> khớp luôn vào <p...> và số bị thổi lên
ps = re.findall(r'<p(?!re\b)(?![^>]*class=)[^>]*>((?:(?!</?p[ >]).)*?)</p>', b, flags=re.S)  # max ≤33
# đo theo từng dòng <br>, không đo cả khối: nhãn lab ngắt dòng bằng <br> là hợp lệ
```

Số vòng kiểm tuỳ loại sửa — xem [[cong-cu-va-cach-kiem]]. Báo cáo kết quả theo
[[trinh-bay-bai]].
