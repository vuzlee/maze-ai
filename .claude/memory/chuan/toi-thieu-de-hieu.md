---
name: toi-thieu-de-hieu
description: "Ba luật người dùng chốt 2026-09-06: chữ meta không được vào bài; bài nào có cấu trúc dữ liệu phải vẽ đúng cấu trúc đó; chỉ giữ thứ tối thiểu để hiểu mental model"
metadata:
  type: feedback
updated: 2026-09-06
---

Ngày 2026-09-06, sau khi xem bản đồ ver bài ([[trang-thai-kho]]), người dùng bổ sung ba
luật — đều về **cái gì được phép nằm trong bài**. Đọc cùng [[chuan-bai-mau]] và [[trinh-bay-bai]].

## Luật A — chữ meta thuộc về memory, không thuộc về bài

Người dùng: *"những chữ thừa như PHÓNG TO — CHỖ HỞ CỦA BẢN GỐC, cái này là memory chứ không cho
vào nội dung bài, bài chỉ nên có nội dung thiết yếu để hiểu"*.

**Vì sao.** Những nhãn đó nói về **cách bài được dựng** (mục này phóng to ô nào của bản đồ, chỗ nào
là chỗ hở của bản gốc, bài có đúng bốn ý), không nói về **thứ đang học**. Người đọc cần biết
XGBoost làm gì, không cần biết tác giả đã sắp xếp bài theo bố cục nào. Nó là ghi chú của người
viết bị bỏ quên trong sản phẩm.

**Áp dụng thế nào.** Xoá khỏi hình và khỏi văn xuôi các nhãn dạng:

- `PHÓNG TO — …` (mọi biến thể), `BỐN Ý — HẾT`, `CẢ BÀI TRONG NĂM DÒNG`, `BẢN ĐỒ`;
- câu kiểu "mục này phóng to ô ③", "chỗ hở của bản gốc", "bài có đúng bốn ý".

Thay bằng **tên của chính thứ đang vẽ**: `PHÓNG TO — GAIN` → `GAIN`; `PHÓNG TO — CHỖ HỞ CỦA BẢN
GỐC` → xoá cả ô nếu ô đó chỉ tồn tại để nói về bố cục. Nếu bỏ nhãn đi mà hình vẫn đọc được thì
nhãn đó là thừa.

**Vẫn giữ**: nhãn là **thuật ngữ thật** dù viết hoa — `ORDER BY`, `PARTITION BY`, `PRIMARY KEY`,
`SERIALIZABLE`, `ITERATOR`, `SHARDING`. Test phân biệt: dịch ngược ra được **một khái niệm trong
bài** thì giữ; chỉ mô tả **quan hệ giữa các mục của bài** thì xoá.

**Cách quét (dùng lại được).** Bắt trong `<text>` của SVG: `PHÓNG TO`, `BỐN Ý — HẾT`,
`CẢ BÀI TRONG`, `BẢN ĐỒ` đứng một mình, `TỔNG KẾT MỘT HÌNH`. Bắt trong văn xuôi: `phóng to ô`,
`mục này (phóng to|vẽ lại|nói)`, `chỗ hở của bản gốc`, `bài này gồm N ý`.

**Đừng quét lỏng.** Bản đầu tôi bắt cả `TỔNG KẾT`, `HẾT`, `MỤC \d`, `ô ①` ở mọi chỗ → ra
**1.323 chỗ ở 128 bài**, tức gần như mọi bài — vô dụng vì nuốt cả `①②③` là ký hiệu vùng hợp lệ
trong hình và chữ "hết" trong câu bình thường. Lọc chặt lại còn **233 nhãn ở 16 bài**, đó mới là
số thật.

**Hiện trạng 2026-09-06 — 233 nhãn ở 16 bài** (toàn bộ):

| Bài | Nhãn trong hình |
|---|---|
| `transaction-isolation` | 26 |
| `decision-tree` · `sql-window-functions` | 21 |
| `sql-index-query-plan` | 20 |
| `sharding-replication` · `random-forest` | 18 |
| `thread-process-gil` · `xgboost` | 17 |
| `gradient-boosting` | 15 |
| `asyncio` · `oop-python` | 14 |
| `dict-hash-table` | 10 |
| `iterator-generator` · `memory-management-gc` · `memory-model-mutability` | 8 |
| `adaboost` | 5 |

**16 bài này đều nằm trong danh sách bài "đã lên ver mới"** (nhóm A + B của
[[trang-thai-kho]]). Nhãn meta là **sản phẩm phụ của chính đợt áp luật 1** — càng sửa
theo chuẩn mới càng dính. Nên: **bài nào sắp áp luật 1 thì dọn nhãn ngay trong lượt đó**, đừng để
thành đợt riêng, và **đừng đẻ thêm** khi viết bài mới.

## Luật B — có cấu trúc dữ liệu thì phải vẽ đúng cấu trúc đó

Người dùng: *"những bài có đề cập tới cấu trúc dữ liệu bất kỳ như XGBoost hay các bài cây hoặc cấu
trúc dữ liệu khác thì phải có hình chi tiết về đúng cấu trúc đó để dễ nhớ, ví dụ xgboost phải có
mấy cái cây nối đuôi nhau"*, kèm hình tham khảo: **N cột nối tiếp**, mỗi cột là
`(X, r_{n-1})` → `Tree n` → `Predict` → `r_n = r_{n-1} − r̂_{n-1}`, mũi tên xanh vòng residual sang
cột sau, cột cuối `Tree N` với dấu `………` ở giữa.

**Vì sao.** Hình vẽ **quan hệ trừu tượng** (ô chữ nhật, mũi tên, band màu) thì nhớ được luồng
nhưng không nhớ được **vật**. Học cây mà chưa từng nhìn thấy cái cây thì mental model rỗng ở
chính chỗ tên bài nói tới.

**Áp dụng thế nào.** Bài nào có một cấu trúc dữ liệu đứng tên — cây, list liên kết, heap, trie,
hash table, đồ thị, matrix, chuỗi cột — thì trong bài **phải có ít nhất một hình vẽ đúng hình
dạng vật lý của nó**, không thay bằng ô chữ nhật:

- cây → node tròn + cạnh nối, thấy được tầng và nhánh trái/phải;
- chuỗi model nối tiếp (boosting) → N khối nối đuôi nhau, có mũi tên feedback mang residual;
- hash table → dãy bucket + chain/probe thật;
- đồ thị → đỉnh và cạnh, không phải bảng kề.

**Cách đo có đang vi phạm không.** Đếm `<circle>` + `<path>` cộng lại trong mọi SVG của bài, so
với `<rect>`. Tên bài là một cấu trúc dữ liệu mà tổng `circle+path` ≤ 3 → **đang vẽ bằng ô chữ
nhật**, tức vẽ quan hệ chứ chưa vẽ vật.

**Quét toàn kho 2026-09-06 — 11 bài vi phạm** (tên bài có cấu trúc dữ liệu, `circle+path` = 2):

| Kệ | Bài | rect | circle+path |
|---|---|---|---|
| 01-dsa | `linked-list` | 7 | 2 |
| 01-dsa | `hash-map` | 10 | 2 |
| 01-dsa | `stack-monotonic-queue` | 12 | 2 |
| 01-dsa | `array-string` | 22 | 2 |
| 01-dsa | `heap-priority-queue` | 55 | 2 |
| 01-dsa | `prefix-sum` | 32 | 2 |
| 02-python | `list-tuple-set` | 11 | 2 |
| 03-cs | `networking-overview` | 8 | 2 |
| 03-cs | `messaging-queue-pubsub` | 25 | 2 |
| 05-ml | `metrics-confusion-matrix` | 23 | 2 |
| 07-tf | `self-attention` | 32 | 2 |

`heap-priority-queue` là ca nặng nhất: **55 ô chữ nhật, 1 hình tròn** cho một bài mà tên nó là một
cây. `self-attention` cũng vậy — 32 rect, không hình nào vẽ matrix Q·Kᵀ thật.

**Bài đã làm đúng, dùng làm mẫu:** `trie` (8 circle, 8 line, 0 rect), `tree-bst-traversal` (8/6),
`graph-bfs-dfs-topo` (6/6), `decision-tree` (20 circle), `tree-family-overview` (38 circle),
`clustering-overview` (1.046 circle — vẽ đám mây điểm thật).

Nhánh tree-based chỉ là chỗ người dùng phát hiện ra đầu tiên. **Luật áp cho mọi kệ**: DSA (7 bài),
Python, CS, ML, Transformer đều đang dính.

Hình nối tiếp của một họ phải **dùng chung khung** (luật đã có trong [[trang-thai-kho]]):
gradient-boosting · xgboost · lightgbm · adaboost cùng một bố cục cột, đặt cạnh nhau là so được.

## Luật C — chỉ giữ thứ tối thiểu để hiểu

Người dùng: *"XGBoost thì 'Xấp xỉ loss bằng một parabol' khó hiểu mà lại không cần… cần những thứ
tối thiểu để hiểu mental model, ý tưởng cốt lõi như là boosting nối tiếp nhau học residual theo
kiểu gì đó, kiến trúc, loss func (hiểu được từng khối của loss func), đủ hình về kiến trúc, cấu
trúc dữ liệu, mối quan hệ giữa các khối… từng bài nội dung chỉ cần hiểu nhanh là được, không cần
quá chi tiết"*.

**Vì sao.** Kho này để **ôn tập**, không phải để tra cứu đầy đủ. Một mục dẫn giải toán (khai triển
Taylor bậc hai) tốn công đọc nhất nhưng không đổi được cách người học hình dung model — bỏ đi thì
mental model vẫn nguyên vẹn.

**Áp dụng thế nào.** Bộ tối thiểu mà một bài kỹ thuật/model phải có, và **chỉ** cần có:

1. **Ý tưởng cốt lõi** — một câu, kiểu "boosting: cây sau học phần cây trước còn sai";
2. **Kiến trúc / cấu trúc dữ liệu** — hình theo luật B;
3. **Loss function** — hiểu được **từng khối** làm gì, không phải cách suy ra nó;
4. **Quan hệ giữa các khối** — cái nào chảy vào cái nào;
5. Đánh đổi · lỗi hay gặp · hỏi đáp.

**Cắt** mục nào chỉ trả lời "công thức này suy ra thế nào". Test: *bỏ mục này đi, người đọc có còn
hình dung đúng model không?* Còn → cắt, hoặc hạ xuống một dòng trong Hỏi đáp.

**Trần đề nghị: ~8–10 mục.** Trung vị toàn kho là **7 mục · 1.475 chữ**, nên bài nào vượt 12 mục
là đang kể chi tiết vượt mức ôn tập. Danh sách vượt trần, 2026-09-06:

| Bài | Mục | Chữ |
|---|---|---|
| `transaction-isolation` | 16 | 2.295 |
| `ml-system-design` | 15 | 3.962 |
| `rag-end-to-end` | 15 | 3.855 |
| `cnn-mobilenet` | 15 | 3.830 |
| `mlops-serving` | 15 | 3.779 |
| `inference-optimization` | 15 | 3.528 |
| `backpropagation` | 15 | 3.291 |
| `sql-window-functions` | 15 | 2.347 |
| `decision-tree` | 14 | 2.108 |
| `sql-index-query-plan` | 14 | 1.604 |
| `self-attention` | 13 | 3.071 |
| `metrics-confusion-matrix` | 13 | 2.732 |
| `random-forest` | 13 | 1.728 |
| `dict-hash-table` | 12 | 3.672 |
| `tcp-http` | 12 | 2.860 |
| `xgboost` | 12 | 2.196 |
| `transformer-architecture` | 12 | 2.017 |

Sáu bài nặng nhất về **chữ** đều nằm ở kệ 06→10 (`ml-system-design`, `rag-end-to-end`,
`cnn-mobilenet`, `mlops-serving`, `inference-optimization`, `backpropagation` — đều ~3.4–4k chữ,
gấp đôi trung vị). Chúng viết trước khi có chuẩn nào, nên là chỗ luật C ăn nhiều nhất.

Ứng viên cắt đã chỉ đích danh: `xgboost` §04 *Xấp xỉ loss bằng một parabol* (12 mục, §04–§07 đều là
chặng suy ra công thức). Quét tên mục toàn kho theo từ khoá dẫn giải (`xấp xỉ|khai triển|suy ra|
chứng minh|taylor|rút gọn công thức`) chỉ ra thêm đúng một chỗ: `greedy` §*Cách chứng minh*.
**Tên mục không phải cách phát hiện tốt** — phần lớn mục dẫn giải mang tên trung tính
(*Gộp theo lá*, *Giá trị lá*), nên phải đọc nội dung, không grep được.

**Chữ trong hình cũng phải tối thiểu** — *"ví dụ của hình chi tiết thì ngắn gọn dễ hiểu đừng cố
note nhiều thế gây rối"*. Trung vị hiện tại **171 chữ/hình** (427 hình của kệ 01→05); các hình
nặng nhất: `hdbscan` 435 chữ/73 `<text>`, `decision-tree` 369, `scope-legb` 363,
`gradient-boosting` 355, `supervised-unsupervised` 355, `pca-dimensionality` 351. Hình cần chú
thích dài tới vậy là hình đang gánh việc của đoạn văn.

## Quan hệ với các luật cũ

Luật C **không mâu thuẫn** với "mỗi mục một hình" — nó cắt **số mục**, không cắt hình. Sau khi cắt,
tỉ lệ chữ/hình còn tốt hơn. Nó cũng không hạ độ sâu của mục *Hỏi đáp*: chỗ để dành cho chi tiết
vượt mức tối thiểu chính là đó, một hai dòng.

## Quy trình review một bài bất kỳ — sáu phép, chạy được cho mọi kệ

Ba luật trên **không riêng cho nhánh tree-based** — người dùng chốt 2026-09-06:
*"các bài ngoài tree based cũng sẽ bị đó, nên nhớ lưu vào memory một cách tổng quát"*.
Số liệu ở trên đã quét toàn bộ 128 bài có nội dung của cả 10 kệ.

Khi review bất kỳ bài nào, chạy đúng sáu phép này:

1. **Nhãn meta** — grep `PHÓNG TO|BỐN Ý — HẾT|CẢ BÀI TRONG|BẢN ĐỒ|TỔNG KẾT MỘT HÌNH` trong
   `<text>`, và `phóng to ô|mục này (phóng to|vẽ lại)|chỗ hở của bản gốc` trong văn xuôi. Có → xoá,
   giữ lại tên của chính thứ đang vẽ.
2. **Hình đúng hình dạng** — tên bài có cấu trúc dữ liệu không? Có mà `circle+path ≤ 3` → phải vẽ
   lại bằng hình dạng thật.
3. **Số mục** — vượt 12 → tìm mục cắt được. Trung vị kho là 7.
4. **Mục dẫn giải** — mục nào chỉ trả lời "công thức này suy ra thế nào" → cắt hoặc hạ xuống
   một dòng ở *Hỏi đáp*. Phải đọc, không grep được.
5. **Chữ trong hình** — hình nào >250 chữ là đang gánh việc của đoạn văn. Trung vị 171.
6. **Bộ tối thiểu còn đủ không** — ý tưởng cốt lõi · kiến trúc/cấu trúc dữ liệu · loss function
   theo từng khối · quan hệ giữa các khối · đánh đổi + lỗi + hỏi đáp.

Phép 1, 2, 3, 5 đo được bằng máy (regex ghi ở từng luật trên); phép 4 và 6 phải đọc bài.

**Số nền để so, đo 2026-09-06:** trung vị **243 chữ/hình** trên cả kho (kệ 01→05 riêng là 171). Hình nặng chữ
nhất: `hdbscan` 435 chữ / 73 `<text>`, `decision-tree` 369, `scope-legb` 363,
`gradient-boosting` 355, `supervised-unsupervised` 355, `pca-dimensionality` 351,
`linear-algebra-ml` 347, `kmeans-clustering` 332, `xgboost` 326/63. Đây đúng là thứ người dùng
gọi *"đừng cố note nhiều thế gây rối"*.

## Luật D — nội dung là chữ thì dùng khuôn HTML, đừng vẽ SVG

Ngày 2026-09-06, người dùng chụp hình *"Cùng một việc, hai chỗ làm khác nhau"* của `xgboost`:
*"hình này đừng xuống dòng vô lý, thiếu viết hoa ở đầu, nội dung đọc khó hiểu, cách bao hình cũng
chưa hợp lý… trình bày hình bị khó nhìn khó hiểu"*.

Hình đó là **hai cột chữ được vẽ bằng `<rect>` + `<text>`**. Bốn lỗi nó mắc là lỗi *cố hữu* của
cách làm này, không sửa vặt được:

- **Xuống dòng vô lý.** SVG không tự wrap, phải chẻ tay thành nhiều `<text>` — nên rơi ra
  những dòng cụt kiểu "hướng nào", "mò", "tối ưu". Sửa chữ là phải chẻ lại toạ độ.
- **Khung không ôm chữ.** Chiều cao `<rect>` gõ tay (22 hay 37) nên câu ngắn thì khung rỗng huếch,
  câu dài thì chữ chạm mép.
- **Thiếu viết hoa đầu câu.** Vì chúng bị coi là "nhãn trong hình" chứ không phải câu văn.
- **Cặp hộp–chú thích rời rạc.** "điểm mới thật sự" trong khung, "là hàm mục tiêu…" ngoài khung —
  mắt phải tự ghép hai mảnh mới ra một câu.

**Luật:** hình chỉ để vẽ *quan hệ* — mũi tên, thứ tự, cấu trúc, tỉ lệ. Nội dung là **văn xuôi song
song hai cột** thì dùng `.cmp two` (`<div>` + `<h5>` + `<p>`); tuần tự thì `.steps`; pipeline dọc
thì `.stack`; công thức thì `.eq`. Khuôn HTML tự wrap, tự co giãn theo màn hình, tự đúng bảng màu.

**Dấu hiệu nhận biết bằng máy:** một `<svg>` có `rect ≥ 4` mà `circle + path + line ≤ 2` thì gần
như chắc chắn là hộp chữ trá hình. Đo `xgboost` ngày 06/09: **9/10 hình dính**, sau khi sửa còn 7.

**Kèm theo — câu chữ trong khuôn HTML phải viết như câu văn thật:** viết hoa đầu câu, có dấu chấm,
mỗi `<p>` mở đầu bằng một cụm in đậm gọi tên ý rồi mới giải thích. Đừng bê nguyên nhãn cụt của
SVG sang.

## Luật E — các hình trong một bài phải kể tiếp nhau, không phải mỗi hình một thế giới

Ngày 2026-09-06, người dùng chụp §06 `xgboost` (hình gain) và lab ngay dưới nó:
*"hình này node thì để hình node chứ cho dễ hiểu, hình tiếp nhìn cũng khó hiểu, kiểu không ăn nhập
với các hình trên làm mỗi lần đọc là một hình hay kiến thức mới, gây khó nhận diện"*.

Hai lỗi tách bạch, đều phải chữa:

**E1 — vẽ đúng vật đang nói.** §06 nói về *tách một nút của cây* mà lại vẽ ba `<rect>` xếp thụt lề
("nút chưa tách" / "nhánh trái" / "nhánh phải"). Nút cây thì phải là `<circle>` có cạnh nối —
đây chính là luật B, chỉ khác là vật ở đây là **một nút** chứ không phải cả cấu trúc.

**E2 — dùng lại đúng một bộ dữ liệu cho cả bài.** Nặng hơn E1. `xgboost` có ba chỗ liên tiếp cùng
nói một việc mà dùng ba bộ số khác nhau: §04 sáu mẫu A–F, §06 ba hộp `G −7 · H 12` không ai biết ở
đâu ra, lab tám mẫu đánh số 1–8. Người đọc phải **nhận diện lại từ đầu ở mỗi hình**, nên tưởng
đang học ba thứ mới thay vì thấy một thứ được nhìn ba lần.

**Luật:** một bài chọn **một bộ ví dụ duy nhất** (ở đây: sáu mẫu A–F với `(g, h)` cố định), rồi mọi
hình *và cả `lab.js`* đều chạy trên đúng bộ đó. Hình sau nhắc lại tên bộ ngay ở dòng đầu — "VẪN
SÁU MẪU A–F CỦA MỤC TRƯỚC" — để người đọc biết mình không phải học lại. Số trong hình phải **tính
ra từ đúng công thức của bài**, đừng bịa cho tròn: chạy Python một lượt rồi chép sang.

**Nối hình với lab:** ngưỡng/tham số mà lab mở sẵn phải trùng trạng thái hình đang vẽ, và
`figcaption` nói thẳng điều đó ("Ngưỡng 4,5 là ngưỡng lab bên dưới mở sẵn"). Có vậy lab mới đọc
như *bấm thử chính cái hình vừa xem*, không phải một ví dụ thứ hai.

**Cách kiểm:** liệt kê mọi con số dạng `G ±x · H y` (hoặc bộ nhãn mẫu) xuất hiện trong bài + lab —
nhiều hơn một bộ là dấu hiệu vi phạm. Đổi bộ dữ liệu ở `lab.js` thì **bắt buộc sửa cả hình**, ghi
chú ngay trong lab để lần sau không quên.

## Luật F — hình mở bài chỉ chứa những mục CÒN TỒN TẠI, và lab chỉ hỏi một câu

Ngày 2026-09-06, sau khi cắt hai mục edge-case của `xgboost`, người dùng:
*"mấy cái dưới có phải thuộc Mental model không, không thì bỏ… nhớ rule sáng lên phần đang học
không?"* và *"có quá nhiều nút, đừng sinh nhiều nút mà chỉ nên tối thiểu các nút để tối ưu UX/UI,
bỏ các phần gây nhiễu loạn thông tin đi sao cho đọc phần nào hiểu phần đó mà không bị nhồi tin"*.

**F1 — hình `.gist` là mục lục của bài, phải sửa theo bài.** Cắt một mục thì ô của nó trong hình
mở bài **thành rác**: hình `xgboost` vẫn còn ô "Ba mẹo kỹ thuật" sau khi mục đó bị xoá, trỏ vào
chỗ không tồn tại. Quy trình: cắt mục xong → mở lại `figure.gist` → xoá ô tương ứng → nếu hình còn
ít ô quá thì **thu gọn cả hình** chứ đừng để khoảng trống. Hình cũ 354px cao, hai cột lặp nhau
(cột trái tóm tắt, cột phải giảng lại chính ba ô đó) — gộp còn một dải 232px.

**F2 — "sáng lên phần đang học" không có nghĩa là chép cả bản đồ vào mỗi mục.** Luật cũ (mỗi mục
tô sáng một ô của bản đồ) đẻ ra 7 hình đều mở đầu bằng cả bản đồ mờ — xem [[trang-thai-kho]].
Cách đúng: bản đồ **chỉ vẽ một lần ở §01**, `figcaption` của nó nói mục nào ứng với ô nào
("① Loss function · ② giá trị lá · ③ gain"); mục thân bài chỉ vẽ nội dung của riêng nó và mở đầu
bằng một dòng chữ nhắc lại mình đang ở ô nào. Chữ rẻ hơn hình vẽ lại.

**F3 — một lab, một câu hỏi, số nút tối thiểu.** Lab gain của `xgboost` từng có **8 nút** (λ bốn
mức × γ bốn mức) nên người đọc phải cân hai thứ cùng lúc và không biết con số nào đổi vì cái gì.
Chốt λ = 1 (λ là chuyện của mục trước, đã dạy xong) và để lại **3 nút γ** chọn theo *kết quả khác
nhau*: 0,5 → 5/5 ngưỡng dương · 4 → 3/5 · 10 → 0/5, tức cây tự dừng. Câu dẫn nêu thẳng câu hỏi
duy nhất: *"tiền thuê lá đắt tới đâu thì cây thôi mọc?"*

**Luật chọn nút:** mỗi nút phải cho một **kết quả khác về chất**, không phải khác về số lẻ. Hai nút
cho cùng một kết luận thì bỏ một. Tham số đã dạy ở mục khác thì **chốt cứng và ghi rõ giá trị**
trong câu dẫn, đừng mở núm.

## Luật G — một bộ ví dụ chạy xuyên bài là thứ đáng giữ

Người dùng xác nhận 2026-09-06: *"tôi thấy hợp lý khi 'Gộp theo lá' và 'Giá trị lá và tác dụng của
λ' vẫn dùng ABCDEF vì cho thấy sự nhất quán tuyến tính dễ học"*.

Đây là **xác nhận trực tiếp cho luật E**, không phải luật mới về hình: giá trị nằm ở chỗ người đọc
**không phải nhận diện lại dữ liệu ở mỗi mục**, nên phần não còn rảnh để theo dõi *cái đang đổi*.
`xgboost` giờ chạy A–F xuyên §04 (gộp thành G, H) → §05 (hai lá đó co lại theo λ) → §06 (chính hai
lá đó có đáng tách không) → lab (bấm thử trên đúng sáu mẫu ấy). Bốn chặng, một bộ số.

**Áp cho bài mới:** chọn bộ ví dụ **trước khi viết mục đầu tiên**, cỡ nhỏ nhất mà vẫn cho thấy
được hiện tượng (6 mẫu là đủ, 8 đã thừa), rồi mọi mục và lab dùng lại. Nếu một mục cần bộ khác
thật thì phải nói rõ vì sao ngay trong hình.

## Luật H — chữ trong bài viết cho người MỚI, không viết cho người đã biết

Ngày 2026-09-06, người dùng chỉ vào hai dòng của hình `xgboost`: *"'hai tiêu chí, không phải một'
và 'VIẾT LẠI BA LẦN' nghe khó hiểu quá, tôi muốn bạn luôn dùng từ ngữ dễ hiểu nhất cho người mới
cũng có thể hiểu được"*.

Cả hai câu **đúng về nội dung** nhưng chỉ đọc ra nghĩa khi đã hiểu bài — tức chúng là *tóm tắt cho
người đã biết*, không phải lời giảng. Đây là lỗi hay gặp nhất khi viết lại cho gọn: gọn quá thành
mật mã.

**Bốn phép thay, theo thứ tự ưu tiên:**

| Kiểu chữ khó | Cách chữa | Ví dụ đã sửa |
|---|---|---|
| Đếm trừu tượng ("hai tiêu chí, không phải một") | nói thẳng hai thứ đó là gì | "cây mọc theo một thước đo, boosting lại chấm điểm bằng thước đo khác" |
| Ẩn dụ tự chế ("viết lại ba lần", "nhìn từ ba phía") | nói việc nó làm | "MỘT CÔNG THỨC, DÙNG CHO BA VIỆC" |
| Thuật ngữ toán làm đầu mục ("Xấp xỉ bằng parabol", "Giải đỉnh parabol", "So hai đỉnh") | đầu mục là **việc**, thuật ngữ xuống dòng phụ | "① Chấm điểm một cây" · "② Tìm số mỗi lá trả về" · "③ Quyết có tách nút không" |
| Thuật ngữ chuyên ngành xuất hiện trước khi được giải thích | dùng lời thường trước, tên tiếng Anh trong ngoặc **sau** | "công thức chấm điểm cây (objective function)" |
| Ẩn dụ kinh tế ("trả phí", "giá phải trả", "đắt/rẻ") | nói thẳng cái xảy ra: **bị phạt**, phạt nặng/nhẹ | `svm`: "cho lấn và bắt trả phí" → "cho lấn nhưng bị phạt" |

**Vẫn giữ nguyên:** công thức mà bài đang dạy (`w* = − G/(H+λ)`) và tên tiếng Anh của bài. Diễn
giải chúng ra lời là mất chỗ neo — luật này áp cho **chữ giảng**, không áp cho ký hiệu.

**Cách tự kiểm:** đọc từng dòng chữ trong hình và mọi `p.key`, hỏi *"câu này có đọc ra nghĩa với
người chưa học mục sau không?"* Nếu phải biết trước mới hiểu thì đó là tóm tắt, không phải giảng.
Dấu hiệu máy dò được: đầu mục/nhãn hình chứa số đếm trừu tượng ("ba…", "hai…", "N cách") mà không
kèm tên cụ thể; hoặc chứa thuật ngữ toán (`parabol`, `đạo hàm`, `khai triển`, `xấp xỉ`, `đỉnh`,
`ma trận`, `chuẩn hoá`) ở vị trí tiêu đề.

## Luật I — cắt phần không phải core, kể cả trong Lỗi hay gặp và Hỏi đáp

Người dùng, cùng ngày: *"bản chất chỉ cần hiểu core, không cần lưu ý edge cases"*, rồi *"có thừa
phần nào không quá quan trọng thì bỏ nhé"*.

Cắt một mục thân bài thì dễ nhớ, nhưng **cùng nội dung đó thường còn sống ở ba chỗ khác**:

1. một thẻ trong *Lỗi hay gặp*,
2. một câu trong *Hỏi đáp* — mục này hay là mục dài nhất bài (Hỏi đáp của `xgboost` từng 581 chữ,
   gấp đôi mục dài thứ hai),
3. một `ul.why` lặp gần nguyên văn đoạn văn ngay trên nó (sinh ra khi thay hình bằng khuôn HTML).

**Bốn loại nội dung đáng cắt** — đo trên `xgboost` thì bốn loại này chiếm 1.367 ký tự:

- **thứ tự chỉnh hyperparameter, tên tham số vận hành** (`subsample`, `colsample_bytree`,
  grid vs random search): vận hành, không phải cơ chế bài dạy → một câu trỏ sang bài chủ;
- **lời khuyên công cụ** (SHAP, permutation importance): không phải lỗi về cơ chế;
- **câu Hỏi đáp giảng lại đúng edge case vừa cắt khỏi thân bài**;
- **`ul.why` lặp ý của đoạn văn liền trên**.

**Bắt buộc sau khi cắt** — hai lỗi đã dính:
- **tham chiếu chết trong văn xuôi**: thẻ "đừng điền `NaN`" còn viện dẫn *sparsity-aware split* vốn
  chỉ giải thích ở mục đã xoá. Sau khi cắt phải `grep` mọi thuật ngữ chỉ có trong mục vừa xoá.
- **ô chết trong `figure.gist`** — xem luật F1.

Đánh số lại `<b>NN</b>` và `id="slug-sN"` bằng token tạm, tránh đụng nhau:
`for old in (9,10,11): id="x-s{old}" → "x-sT{old-2}"` rồi mới bỏ chữ `T`.
