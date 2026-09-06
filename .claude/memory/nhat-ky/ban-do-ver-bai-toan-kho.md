---
name: ban-do-ver-bai-toan-kho
description: "Bảng phân loại 200 bài toàn kho theo hai trục: luật 1 (A/B/B2/C/D/E1/E2/F) và ba luật tối-thiểu-để-hiểu — đo lại từ file ngày 2026-09-06, thay cho các con số rời rạc trong nhật ký cũ"
metadata:
  type: project
updated: 2026-09-06
---

Ngày 2026-09-06, người dùng: *"rà soát xem còn những bài nào ver cũ và những bài nào ver mới nhất
theo memory, check kĩ từ DSA đến kệ ML"*, rồi *"list hết cơ, đầy đủ tất cả các bài và nhóm lại"*.

Đây là **bản đo từ file**, không phải chép lại nhật ký cũ. Các số rời rạc trong
[[dot-sua-theo-chuan-bai-mau]], [[dot-luat-1-ke-02-python]], [[dot-luat-1-ke-04-database]],
[[dot-luat-1-ke-05-ml]] đã lệch — dùng bảng này làm mốc.

## ⚠ TIẾN ĐỘ THẬT — đọc trước tiên (cập nhật 2026-09-07)

Người dùng review ngày 07/09 và **bác một phần báo cáo của đợt 06/09**. Ghi lại nguyên văn để
đừng tự khen lần nữa:

> *"có mấy cái vẫn còn ver cũ thậm chí có cả mấy bài bạn bảo sửa xong rồi như dbscan, MLE & MAP,
> Supervised…"* · *"có vẻ do tôi bắt bạn làm quá nhiều việc nên đang bị dở dang"*

**Nguyên nhân gốc của hiểu lầm: hai trục bị lẫn.** Đợt 06/09 chỉ chạy **trục luật A→I**
(chữ meta, đầu mục, tràn hình). Nó **không đụng gì tới trục luật 1** (đưa mental model lên §01,
gỡ *Tổng kết một hình*). Nói "đã sửa 75 bài" mà không nói rõ sửa theo trục nào thì người đọc
hiểu là bài đã lên ver mới — sai. **Từ nay mọi báo cáo phải ghi rõ TRỤC NÀO.**

Số thật lúc này: `Tổng kết một hình` vẫn còn **51 bài** — y hệt trước đợt 06/09. Ba bài người dùng
nêu (`dbscan`, `mle-map`, `supervised-unsupervised`) đều nhóm D, đều 0 `figure.gist`, đúng như bảng
D bên dưới. Bảng A/B/B2/C/D/E/F **chưa đổi một dòng nào** kể từ 06/09.

### Sáu việc đang mở — trạng thái 2026-09-07

| # | Việc | Mức | Phạm vi |
|---|---|---|---|
| ~~1~~ | ~~Hình vỡ — gỡ bản đồ nửa vời~~ | ✅ **XONG 07/09** | 93 hình · 11 bài · đo lại 0 vỡ |
| ~~2~~ | ~~Công thức `<pre>` gióng cột~~ | ✅ **XONG 07/09** | 5 khối · 5 bài · siết metric cứu thêm 3 khối |
| **3** | 51 bài còn ver cũ (trục luật 1) | 🔨 **đang làm** | đo 07/09: `svg ≥ số mục` đúng **0/51**; 4 bài mới được nửa |
| ~~4~~ | ~~Thuật ngữ thao tác chưa để tiếng Anh~~ | ✅ **XONG 07/09** | luật ghi ở `chuan/dat-ten-tach-theo-ke.md`; sửa 11 chỗ / 8 bài |
| ~~5~~ | ~~`Random forest & bagging` — tên ghép~~ | ✅ **XONG 07/09** | đổi tên + 4 link chéo; bagging vốn đã có chủ ở overview |
| **6** | 7 hình chữ-đóng-hộp · 8 bài ≥12 mục | nợ cũ, chưa đụng | xem trục hai |

---

### Thứ tự thi công đã chốt (2026-09-07)

Nguyên tắc xếp: **việc nào đang làm hỏng thứ người đọc nhìn thấy thì trước; việc nào là *luật*
thì phải chốt trước việc *áp luật*, không thì phải làm lại lần hai.**

| Bước | Việc | Vì sao đứng chỗ này | Cách nghiệm thu |
|---|---|---|---|
| ~~1~~ | ~~#1 — hình vỡ~~ | ✅ **XONG 07/09** — 93 hình, 4 phép nghiệm thu đều sạch | |
| ~~2~~ ✅ | ~~#2 — công thức `<pre>` → `.eq`~~ | 2 bài, tự chứa, luật đã có sẵn trong CLAUDE.md | **XONG 07/09** — 5 khối/5 bài, 8 khối `<pre>` còn lại đúng là code |
| ~~3~~ ✅ | ~~#5 — tên `Random forest & bagging`~~ | hoá ra không cần chốt: tách hay gộp đều ra một kết quả | **XONG 07/09** — `data-title` hết dấu `&`, 4 link chéo còn sống |
| ~~4~~ ✅ | ~~#4 — luật đặt tên tách theo kệ~~ | là **luật**, phải chốt trước bước 5 | **XONG 07/09** — luật vào `chuan/`, quét lại 13→10 và cả 10 đều đúng |
| ~~5~~ ✅ | ~~nhóm P — 9 bài thiếu hình~~ | **XONG 07/09** — siết metric 2 lần nữa, hoá ra chỉ 1 mục thật | A=38 · P=0 |
| **6** 🔨 | #3 — 51 bài nhóm D lên ver mới | khối lớn nhất, mỗi bài ~một phiên | `gist` trong §01 · hết *Tổng kết* · **svg ≥ số mục** · 490px sạch |
| 6 | #6 — nợ cũ luật B/C/D | phần lớn tự tan khi bước 5 vẽ lại hình | đo lại trục A→I |

**Vì sao #4 đứng trước #3:** bước 5 viết lại đầu mục của 51 bài. Chốt luật đặt tên sau bước 5
thì phải sờ lại đúng 51 bài đó lần nữa.

**Luật của mọi bước, không có ngoại lệ:**

1. Đo trước → sửa → **đo lại bằng chính script đó** → mới được ghi "xong".
2. Không nghiệm thu bằng cách grep chữ đã xoá. Phải đo **trạng thái kết quả** — đây đúng là chỗ
   làm hỏng 81 hình ở đợt 06/09.
3. `python3 tools/build.py` sạch trước khi đóng bước.
4. Ghi kết quả vào chính file này **trước khi** sang bước sau, và **luôn ghi rõ chạy TRỤC NÀO**.

### ✅ 1 — 93 hình vỡ ở 11 bài — ĐÃ XONG 2026-09-07

> **Trục: hiển thị SVG.** Không phải trục luật 1, không phải trục A→I. Không bài nào lên ver mới nhờ bước này.

Người dùng: *"OOP trong Python hình chi tiết đang lỗi"*. Đúng, và **không chỉ OOP**.

Đợt 06/09 gỡ cột bản đồ mờ ở 16 bài. Phép biến hình có hai nhịp — (a) xoá phần tử của cột bản đồ,
(b) dời phần còn lại về x=0 rồi nhân giãn. **Chỉ 5 bài chạy đủ hai nhịp; 11 bài dừng ở nhịp (a)**,
để lại mảng trắng rộng ~372px bên trái mọi hình thân bài.

**Số đo lại khi bắt tay: 93 hình / 11 bài**, không phải 81/10 như ghi lần đầu — lần đếm đầu sót
`sql-window-functions` (12 hình) vì bộ lọc đòi "không có `<text>` nào ở x ≤ 345", mà bài này còn
sót đúng một nhãn mồ côi `cột mới` ở x=327 nên trượt khỏi lưới.

| Bài | Hình đã sửa | | Bài | Hình đã sửa |
|---|---|---|---|---|
| `transaction-isolation` | 13 | | `thread-process-gil` | 8 |
| `sql-window-functions` | 12 | | `gradient-boosting` | 7 |
| `sql-index-query-plan` | 11 | | `asyncio` · `oop-python` | 6 mỗi bài |
| `decision-tree` | 10 | | `adaboost` | 3 |
| `random-forest` | 9 | | **tổng** | **93** |

**Phép biến đổi — đo ngược từ 5 bài đã sửa đúng, khớp err = 0,00:**

```
dx = min(x) của mọi <text>/<rect>/<circle> còn lại sau khi xoá rác
k  = W / (W − dx)          với W = 860 (viewBox chuẩn của cả kho)
x' = (x − dx) · k          áp cho x · x1 · x2 · cx · width của <rect> · số trong path d
<polygon> (mũi tên): CHỈ tịnh tiến theo tâm, không nhân k — nhân vào thì đầu mũi tên méo
<polyline>: nhân k như mọi thứ khác
```

Rác bị xoá, đúng 258 phần tử và **chỉ những thứ này**: 93 đường kẻ đứt cụt, 73 chấm nối,
72 đường cong nối sang cột bản đồ đã mất, 8 kẻ đứt phụ, và 12 nhãn `cột mới` mồ côi của
`sql-window-functions`. Không mất một chữ nội dung nào (đối chiếu số `<text>`/`<rect>` với bản backup).

**Bẫy suýt dính, ghi lại kẻo lặp:** bản script đầu tự phán đoán hình nào vỡ **sau khi** đã loại rác.
Làm vậy thì hình bản đồ ở §01 — vốn còn nguyên vẹn, lành — cũng bị coi là vỡ và **bị xoá sạch nửa
trái**: 570 phần tử, gồm cả `Encapsulation`, `Abstraction`, `PLANNER`… May là đếm phần tử-sẽ-xoá
trước khi ghi nên bắt được. **Luật: quyết định vỡ/lành phải đo trên TOÀN BỘ phần tử, trước khi loại
bất cứ thứ gì.**

**Tiện tay sửa nốt 12 chữ tràn khỏi viewBox** ở `decision-tree` (7), `random-forest` (4),
`adaboost` (1). Đã kiểm bằng bản backup: **tràn này có sẵn từ trước, không phải do phép giãn** —
số x_end trước và sau y hệt. Sửa bằng cách rút câu, không đổi ý; những dòng ~133 ký tự đó là
văn xuôi nhét vào SVG, tức nợ luật D vẫn còn ở ba bài này.

**Nghiệm thu — bốn phép, tất cả sạch:**

| Phép | Kết quả |
|---|---|
| đo lại toạ độ toàn kệ 01→05 | **0** hình vỡ (trước: 93) |
| lề trái 108 hình đã sửa | **đều = 0**; không có x âm; không tràn viewBox |
| `getBBox()` thật trong Chrome, 119 SVG | **0** khoảng trắng > 40px · **0** chữ tràn |
| 11 bài ở 490px **qua HTTP** | **0** tràn ngang · **0** hình lệch |

`python3 tools/build.py` sạch. XML hợp lệ cả 119 SVG.

**Bẫy đo mới — `<base href>` làm hỏng phép đo màn hình hẹp.** Đo lần đầu bằng cách chèn `<base>`
vào file rồi mở `file://` → báo 6 chỗ tràn ngang ở **cả 8 bài**. Nhưng `hash-map` (bài chưa hề
đụng tới) cũng ra đúng 6 chỗ ấy: `<base>` làm đường dẫn `../../../assets/style.css` hỏng, mất CSS
nên mục lục desktop không bị ẩn. **Muốn đo màn hình hẹp thì phải chạy qua HTTP thật**
(`python3 -m http.server`), đừng chèn `<base>`.

**Bài học lớn nhất của bước này — kiểm phải nhìn kết quả, không nhìn dấu vết.** Đợt 06/09 kiểm bằng
*"còn chữ `PHÓNG TO` / `BẢN ĐỒ` không"* → ra 0, tưởng xong. Chữ bị xoá **không** chứng minh hình
còn dùng được. `getBBox()` một mình cũng không đủ — khoảng trắng nằm trong viewBox nên không phải
tràn; phải đo **lề trái**.

### ✅ 2 — công thức `<pre>` → `.eq` — ĐÃ XONG 2026-09-07

> **Trục: chuẩn khuôn hình (CLAUDE.md).** Không phải trục luật 1.

Người dùng: *"Naive Bayes thì công thức khó nhìn (nên dùng kiểu như latex)"*.

CLAUDE.md đã có luật: *"Công thức đứng riêng dùng `.eq` chứ không phải `<pre>`"*. Khuôn `.eq` làm
sẵn việc gióng lề: `.eq .t` bọc một số hạng, `.eq .t em` là nhãn nằm dưới có gạch ngang — **không
phải đếm cột**, nên không lệch ở font tỉ lệ và màn hình hẹp.

**Đã chuyển 5 khối / 5 bài:**

| Bài | Khối | Chuyển thành |
|---|---|---|
| `naive-bayes` | định lý Bayes có mũi tên `↑` chỉ lên 4 số hạng | 1 `.line` · 4 `.t` · mỗi số hạng một nhãn màu ngữ nghĩa + `p.read` |
| `naive-bayes` | làm mượt α, hai trường hợp gióng cột bằng dấu cách | 2 `.line` (đỏ = không mượt · xanh = có mượt) + `dl` giải nghĩa α, V |
| `hdbscan` | `core_k` và `d_mreach` kèm `↑` | 2 `.line` + `p.read` |
| `gradient-optimization` | chain rule `y = f(g(x)) → dy/dx = …` | 1 `.line` · 2 `.t` |
| `kmeans-clustering` | `Inertia = Σ ‖ xᵢ − μ ‖²` kèm `←` | 1 `.line` + `p.read` gộp hai câu bước gán/dời |
| `pca-dimensionality` | `C · v = λ · v` + tỉ lệ phương sai giữ lại | 2 `.line` + `dl` giải nghĩa v, λ |

**Cách quét, và vì sao metric đầu tiên sai.** Bộ lọc đầu (`có ký tự ↑`) chỉ ra **2 bài** và sau khi
sửa thì về 0 — tưởng xong. Siết lại bằng bộ lọc rộng hơn (khối `<pre>` ≤ 6 dòng, có `= ≈ ∝`, và
**không** chứa dấu hiệu code `def/return/SELECT/#/--/…`) thì ra **11 khối**, trong đó 3 khối nữa là
công thức thật. Đúng bẫy *"metric thô phải siết hai lần"* — lần này siết đã cứu được 3 khối.

**8 khối `<pre>` còn lại là ĐÚNG chỗ, đừng đổi:** `exception-handling`, `scope-legb` ×3 (code
Python), `er-modeling` (câu tiếng Việt cần đọc), `sql-window-functions` · `transaction-isolation`
(SQL), `linear-regression` (ví dụ số kèm diễn giải hai dòng — CLAUDE.md dặn `<pre>` vẫn là chỗ của
dẫn giải).

**Nghiệm thu:** dựng lại 5 bài trong Chrome qua HTTP ở **1400px và 490px** — 9 khối `.eq`, đủ số
`.line`/`.t`, **0 chỗ tràn ngang**. Chỗ duy nhất rộng hơn khung là `.line` của naive-bayes ở 490px
(566 > 440) — **đúng thiết kế**, `.eq .line{overflow-x:auto}` cho cuộn trong lòng khối.
`python3 tools/build.py` sạch.

### 🔨 3 — 51 bài còn ver cũ — ĐANG LÀM, bắt đầu 2026-09-07

> **Trục: luật 1 của [[chuan-bai-mau]].** Đây là trục *nội dung*, khác hẳn ba bước vừa xong —
> ba bước kia là hiển thị và đặt tên, xong là xong; bước này phải **vẽ lại hình cho từng bài**.

Ba bài người dùng chỉ đích danh (`dbscan`, `mle-map`, `supervised-unsupervised`) đều nằm trong 51
bài này. Vì sao trước đây tôi báo "đã sửa" mà người dùng vẫn thấy ver cũ: các đợt trước chạy **trục
khác** (rút chữ, sửa hình vỡ, gộp mục), không phải trục luật 1.

**Đo lại đầy đủ 07/09 — 51 bài, chia theo mức nợ:**

| Kệ | Số bài | Đã có `figure.gist` ở §01 | Nợ nặng nhất |
|---|---|---|---|
| 02-python | 6 | 0 | cả 6 bài đều 2 svg / 6–8 mục |
| 03-cs-fundamentals | 11 | 1 (`tcp-http`) | 10 bài 2–3 svg / 5–8 mục |
| 04-database | 14 | 1 (`data-quality`) | 13 bài 2–4 svg / 7–9 mục |
| 05-machine-learning | 20 | 2 (`linear-regression`, `metrics-confusion-matrix`) | 18 bài 2–5 svg / 5–13 mục |

**⚠️ Metric đã siết lại 07/09 — con số cũ ngay dưới đây là SAI, giữ để đối chiếu.**

Luật *"metric thô phải siết ít nhất hai lần"* lại đúng lần nữa. Đếm `svg ≥ **mọi** <h2>` là sai vì
*Hỏi đáp*, *Lỗi hay gặp*, *Mẫu code*, *Lab*, *Từ điển bỏ túi* **không cần hình** — luật 1 không đòi.
Đếm lại chỉ các mục **cần hình** (`/tmp/tight.py`), trên 116 bài có nội dung của 5 kệ:

| Nhóm | Số bài | Nghĩa |
|---|---|---|
| **A — đạt luật 1** | **29** | xong thật, không phải sửa |
| **P — có `gist@§01`, hết *Tổng kết*, nhưng thiếu hình** | **9** | nợ nhẹ, vẽ thêm 1–4 hình là xong |
| **D — còn *Tổng kết một hình*** | **51** | nợ nặng, phải viết lại theo luật 1 |
| **E — không có `gist@§01`** | 27 | phần lớn là bài `01-dsa` + overview được miễn |

Khác biệt lớn nhất so với lần đo trước: **cả 7 bài `02-python` và 4 bài `04-database` nặng nhất
(`transaction-isolation`, `sql-window-functions`, `sql-index-query-plan`, `sharding-replication`)
cùng `decision-tree`, `random-forest`, `gradient-boosting`, `adaboost` thật ra ĐÃ ĐẠT** — trước bị
đánh trượt chỉ vì thiếu đúng một hình cho mục *Hỏi đáp*. Nhóm P chỉ còn 9 bài, không phải 20.

**⚠️ Siết lần BA và lần BỐN — nhóm P thật ra chỉ có 1 bài, không phải 9.**

Bắt tay vào `xgboost` (bài "thiếu 1 hình") thì lộ ngay lỗi: script chỉ đếm thẻ `<svg>`, trong khi
CLAUDE.md coi `.strip .flow .cmp .stack .mtx .axis .seq .bars .eq` **đều là khuôn hình**. `xgb-s3`
và `xgb-s7` có `.eq`/`.cmp` — chúng không thiếu gì cả.

Đếm lại theo "mục có **bất kỳ khối trực quan nào** không" (`/tmp/t3.py`) → P còn 13. Đọc tay 15 mục
bị báo thì **13 mục là `<table>` tra cứu** (bảng chính *là* khối trực quan của mục đó) và 2 mục là
`.probs` (danh sách LeetCode, khuôn DSA). Thêm `<table>` + `.probs` vào bộ lọc (`/tmp/t4.py`) →
**P còn đúng 1 bài**.

| Lần đo | Bộ lọc | A | P |
|---|---|---|---|
| 1 | `svg ≥ mọi <h2>` | — | 32 |
| 2 | `svg ≥ mục cần hình` | 29 | 9 |
| 3 | có khối trực quan bất kỳ | 25 | 13 |
| **4** | **+ `<table>` + `.probs`** | **38** | **0** |

Lần 3 ra A thấp hơn lần 2 vì bộ lọc chặt hơn theo chiều khác — đúng cảnh báo *"con số đầu tiên của
bất kỳ metric nào cũng nên coi là sai"*, lần này sai **bốn** lần liên tiếp.

### ✅ Bước 5 — nhóm P — ĐÃ XONG 2026-09-07

> **Trục: luật 1.** Đây là bước đầu tiên thật sự đẩy bài lên ver mới.

Chỉ phải sửa **1 mục / 1 bài**: `big-o-complexity` §06 *Amortized — vì sao append là O(1)* chỉ có
`p.key` + `ul.why`, không khối trực quan nào. Thêm một `.bars` ba cột (lần nở đắt nhất 981× ·
tổng phép chép 8,56n · trung bình O(1)) + `p.stripnote` — số lấy từ chính hình đo ở §05, không
bịa thêm.

**Nghiệm thu:** `/tmp/t4.py` đo lại → **A=38 · P=0** · D=51 · E=27. `build.py` sạch
(202 URL · 1474 mục · 506 thẻ). Dựng ở 490px qua HTTP: 0 tràn ngang · 0 hình lệch.

*(Bảng dưới là con số sai của lần đo 2, giữ để đối chiếu.)*

**Nhóm P — 9 bài, thiếu bao nhiêu hình:**

| Kệ | Bài | Cần | Có | Thiếu |
|---|---|---|---|---|
| 01-dsa | `big-o-complexity` | 7 | 3 | 4 |
| 01-dsa | `sorting` | 6 | 3 | 3 |
| 05-ml | `svm` | 6 | 3 | 3 |
| 05-ml | `ml-overview` | 4 | 2 | 2 |
| 05-ml | `knn` | 5 | 3 | 2 |
| 05-ml | `naive-bayes` | 5 | 3 | 2 |
| 05-ml | `ridge-lasso-elasticnet` | 5 | 3 | 2 |
| 05-ml | `xgboost` | 7 | 6 | 1 |
| 05-ml | `evaluation-overview` | 3 | 2 | 1 |

*(Con số cũ, sai, giữ để đối chiếu:)* **`svg ≥ số mục` — hiện đúng 0/51 bài.** Bốn bài có `gist` ở §01 rồi vẫn
chưa xong, vì luật 1 đòi **mỗi mục vẽ lại bản đồ với một ô sáng** (`tcp-http`: 3 svg / 12 mục;
`metrics-confusion-matrix`: 3 svg / 13 mục). Nên bốn bài đó là **đã làm được nửa**, không phải xong.

**Vì sao mỗi bài ~một phiên, không gộp lô được.** Luật 1 không phải phép biến đổi máy móc như bước
1 — nó đòi *nghĩ ra* bản đồ 3–5 ô cho từng khái niệm, rồi dàn ý phải đọc ra được từ chính hình đó
(*"vẽ hình trước, dàn ý là hệ quả"*). Không có script nào làm hộ.

**Thứ tự làm trong bước 5** — làm kệ nhỏ trước để mỗi kệ đóng lại được trọn vẹn, và làm bài người
dùng chỉ đích danh trước trong từng kệ:

1. **02-python** (6 bài) — kệ nhỏ nhất, đóng được sớm nhất.
2. **03-cs-fundamentals** (11) — `tcp-http` đã có nửa, làm nốt trước.
3. **04-database** (14) — `data-quality` đã có nửa.
4. **05-machine-learning** (20) — bắt đầu bằng ba bài người dùng chỉ tên:
   `dbscan` · `mle-map` · `supervised-unsupervised`; rồi `linear-regression`,
   `metrics-confusion-matrix` (đã có nửa); rồi 15 bài còn lại.

**Nghiệm thu mỗi bài, đo bằng markup chứ không bằng tên mục:**
`<section id="…-s1">` chứa `figure class="gist"` · **không** còn `<h2>` chứa "Tổng kết" ·
số `<svg>` ≥ số mục **cần hình** · `build.py` sạch · dựng ở 490px không tràn ngang.
Script đo: **`/tmp/tight.py`** (A/P/D/E, chỉ đếm mục *cần* hình). `/tmp/ver.py` và
`/tmp/vera.py` là hai bản cũ đếm mọi `<h2>` — **đừng dùng lại**, chúng thổi phồng nợ.

### ✅ 4 — luật đặt tên TÁCH THEO KỆ — ĐÃ XONG 2026-09-07

> **Trục: chuẩn đặt tên.** Không phải trục luật 1.

Người dùng: *"thuật ngữ chưa để tiếng anh, như tra/Tìm trong cấu trúc dữ liệu nên để thành search,
tương tự với add insert, delete, remove… **nên tách bạch rule của các kệ lớn ra để tránh lộn xộn**,
ví dụ DSA như bây giờ cũng không phải sửa gì thêm nhiều nhưng các kệ khác vẫn còn nhiều vấn đề"*.

**Luật đã ghi:** [`chuan/dat-ten-tach-theo-ke.md`](../chuan/dat-ten-tach-theo-ke.md), có trong
`MEMORY.md`. Cốt lõi hai điều:

1. **Chỉ áp vào chỗ mà bản thân chuỗi chữ đó *là tên thao tác*** — ô tiêu đề bảng, ô cột đầu bảng
   tra, nhãn SVG gọi tên một bước, `<h2>` khi cả mục nói về đúng thao tác đó. **Không áp vào văn
   xuôi** (`p.key`, `.why`, `figcaption`, nhãn SVG là một câu).
2. **Mỗi kệ một bộ từ riêng.** DSA = tên thao tác (`access` `search` `insert` `delete` `traverse`
   `merge` `union`). Python = **cú pháp thật** (`remove(v)`, `x in s`, `for x in it`) chứ không
   phải từ tiếng Anh trần. Database = từ khoá lĩnh vực (`primary key` `foreign key` `aggregate`).
   ML = tên model/metric/kỹ thuật, **nhưng không đổi động từ**.

**Vì sao phải tách — đo được bằng số.** Quét cả kho bằng một danh sách động từ ra **58 đầu mục
dính**; đọc tay thì gần hết là tiếng Việt thường (*"tìm ba dấu hiệu này trước"*, *"đánh giá đang
trả lời câu hỏi nào"*). Cùng chữ "tìm" là **thuật ngữ** ở DSA (`search`, có độ phức tạp riêng, bị
hỏi thẳng khi phỏng vấn) nhưng là **động từ thường** ở ML. Một luật chung không phân biệt nổi.

Thêm một luật chống tiếng lai: **đổi cả cụm hoặc không đổi gì** — `Metric cho regression` được,
~~`Metric hồi quy`~~ nửa nọ nửa kia thì thà giữ nguyên tiếng Việt.

**Đã sửa 11 chỗ, đúng những chỗ luật bắt:**

| Kệ | Chỗ | Từ | Thành |
|---|---|---|---|
| 01-dsa | `data-structures-overview` — tiêu đề 3 cột bảng tra | `Lấy theo vị trí · Tìm · Thêm / bỏ` | `Access · Search · Insert / delete` (+ 1 câu `p.key` dạy đọc bảng) |
| 02-python | `list-tuple-set` — ô bảng thao tác | `xoá theo giá trị` | `remove(v)` theo giá trị |
| 03-cs | `caching` — ô bảng + nhãn SVG ×2 | `Xoá khi ghi · Khoá có phiên bản` | `Invalidate on write · Versioned key` |
| 03-cs | `tcp-http` — ô bảng | `Bắt tay` | `Handshake` |
| 04-db | `relational-model` — 3 `<h2>` | `Khoá chính · Khoá ngoại · Khoá dự tuyển & khoá tổ hợp` | `Primary key · Foreign key · Candidate key & composite key` |
| 04-db | `sql-window-functions` §11 | `Hàm gộp làm window` | `Aggregate function làm window` |
| 05-ml | `supervised-unsupervised` §03 | `Hồi quy hay phân loại` | `Regression hay classification` |
| 05-ml | `metrics-confusion-matrix` §08 | `Metric hồi quy` | `Metric cho regression` |

**Cố ý KHÔNG đổi — và vì sao:** bảng dunder của `data-model-dunder` (cột đầu là *mô tả ý muốn*,
đã kèm sẵn cú pháp `for`/`[]`/`with`); `leetcode-toolkit` (cột đầu mô tả nhu cầu, cột hai là code
thật); `Thêm dữ liệu` ở `bias-variance-tradeoff`/`overfitting-regularization` (tên một **kỹ thuật
chữa**, tiếng Việt đúng hơn `add data`); `duyệt DFS là ra ngay` ở `trie` (câu văn xuôi trong ô);
mọi chỗ "khoá chính/khoá ngoại" nằm **trong văn xuôi** của `relational-model`, `er-modeling`,
`db-normalization`.

**Nghiệm thu:** quét lại bộ lọc ô-bảng — **13 → 10**, cả 10 đã đọc tay và đều đúng là tiếng Việt
thường. `build.py` sạch. Dựng 8 bài đã sửa ở **490px qua HTTP**: `caching` báo 5 tràn ngang và
`relational-model`/`supervised-unsupervised` báo 1 hình lệch — **kiểm bằng bản `git show HEAD` thì
cả ba lỗi đó có y hệt từ trước**, không do bước này gây ra. Chúng là nợ cũ, đưa sang việc #6:
`caching` §02 có `div.strip` với chip `stale-while-revalidate=60` dài hơn khung 490px.

### ✅ 5 — `Random forest & bagging` → `Random forest` — ĐÃ XONG 2026-09-07

> **Trục: chuẩn đặt tên (CLAUDE.md).** Không phải trục luật 1 — bài này vẫn ở nhóm ver cũ, sẽ
> gặp lại ở bước 5.

Người dùng: *"nên tách ra vì các model khác đâu có kiểu & bagging, có thể tách hay gộp vào overview"*.

**Đọc trước khi sửa, và kết quả đọc làm nhẹ hẳn việc.** Đếm chữ "bagging" trong cả nhóm: nó **đã
có chủ** ở `tree-family-overview` từ trước — mục `.cmp` *Bagging — khi từng cây quá phức tạp* đối
chiếu với boosting, một dòng trong *Từ điển bỏ túi*, và cả bảng so sánh hai hướng gộp cây. Trong
`random-forest` bagging chỉ còn **hai câu cơ chế**: một dòng `.why` giải nghĩa chữ viết tắt
(Bootstrap aggregating = bước 1 + bước 3) và một dòng nói bỏ bước 2 thì thành bagging thuần.

Nên **"tách" và "gộp vào overview" ra cùng một kết quả**: chỉ phải đổi tên, **không phải chuyển
nội dung đi đâu cả**. Đúng luật *một khái niệm một chủ* — bài chủ của bagging là overview, bài
random-forest nhắc lại bằng đúng cơ chế "một câu + link".

**Đã sửa 7 chỗ:**

| Chỗ | Từ | Thành |
|---|---|---|
| `random-forest` `<title>` · `og:title` · `data-title` | `Random forest & bagging` | `Random forest` |
| `random-forest` `<h1>` | `Random forest <em>& bagging</em>` | `Random <em>forest</em>` |
| `random-forest` dòng `.why` mục 02 | định nghĩa cụt | thêm link tới `tree-family-overview` |
| `decision-tree` `<footer>` · `tree-family-overview` nút sau · `gradient-boosting` `<footer>` | chữ link cũ | `Random forest` |

`<h1>` giữ đúng khuôn của kho: một chữ nằm trong `<em>` để lấy chữ nghiêng serif, giống
`<em>Probability</em>`, `<em>SVM</em>`, `Feature <em>engineering</em>`.

**Nghiệm thu:** `grep 'Random forest &amp; bagging'` toàn `content/` = **0**; `catalog.js` sau build
ghi `"title": "Random forest"`; `build.py` sạch (202 URL · 200 bài · 1474 mục · 506 thẻ); XML mọi
SVG trong nhóm hợp lệ; dựng cả 7 bài của nhóm ở **490px qua HTTP** — 0 tràn ngang, 0 hình lệch.

### 🔨 Bước 6 — nhóm D — ĐANG LÀM (bắt đầu 2026-09-07)

> **Trục: luật 1.** 51 bài còn mục *Tổng kết một hình*.

**Phát hiện làm nhẹ việc:** `/tmp/d.py` cho thấy **44/51 bài đã có hình ở mọi mục nội dung**.
Việc chính không phải vẽ mới mà là **tái cấu trúc**: SVG trong *Tổng kết* vốn đã gồm N khối
①②③… ứng 1-1 với N mục nội dung. Cách làm chuẩn (mẫu: `transaction-isolation`, `random-forest`):

1. Dựng một bản đồ chung từ chính SVG *Tổng kết* đó — `/tmp/mapgen2.py` sinh tự động
   (`build(boxes, hi, head, rows, label)`, `hi` = ô sáng, 0 = không ô nào).
2. §01 đổi tên thành *Mental model*, đặt bản đồ vào `figure.gist`, **không ô nào sáng**,
   kèm câu "Cả bài là N ý dưới đây. Mỗi mục sau vẽ lại bản đồ này và tô sáng ô đang học."
3. Mỗi mục nội dung nhận `figure.scrollx` cùng bản đồ, **ô của nó sáng**, thêm panel chi tiết bên phải.
4. Xoá mục *Tổng kết*; nội dung trong đó đã nằm rải ở các mục.
5. Ô nào chưa có mục riêng thì **tách mục mới** cho nó (đừng nhét hai ô vào một mục).

**Bẫy đã gặp:** dòng chú thích trong panel phải **≤ ~78 ký tự**, dài hơn là tràn khỏi
`viewBox 0 0 860` — probe 490px bắt được (`hinh_lech`), phải rút gọn câu chứ không nới viewBox.

| # | Bài | Kệ | Xong |
|---|---|---|---|
| 1 | `data-model-dunder` | 02-python | ✅ 07/09 — 6 mục, hết *Tổng kết*, 490px sạch |
| 2 | `scope-legb` | 02-python | ✅ 07/09 — tách ô ① thành mục riêng → 7 mục; rút 6 dòng quá dài |
| 3 | `decorator-context-manager` | 02-python | ✅ 07/09 — 7 mục |
| 4 | `exception-handling` | 02-python | ✅ 07/09 — tách ô ① → 7 mục |
| 5 | `typing-dataclass` | 02-python | ✅ 07/09 — tách ô ① → 8 mục; ô ③ chia đôi Generic / Protocol |
| 6 | `performance-profiling` | 02-python | ✅ 07/09 — tách ô ① và **viết mới mục *Thao tác O(n) bị giấu*** → 7 mục |

**✅ Kệ 02-python hết nhóm D.** Đo lại bằng `/tmp/t4.py`: **A=44 · P=0 · D=45 · E=27**
(trước bước 6: A=38 · D=51). `build.py` sạch, 490px sạch trên cả 6 bài.

**Bẫy thứ hai đã gặp:** chèn hình bằng mốc `<p class="key">` là sai — vài mục không có `p.key`,
nên hình rơi nhầm sang mục khác. Mốc đúng là `</div>` đóng của `<div class="sh">`.
**Bẫy thứ ba:** sau khi xoá mục *Tổng kết* phải **đổi id lẫn `<b>NN</b>` từ dưới lên**, không thì
trùng id (đã dính một lần ở `performance-profiling`).

**Bắt được một lỗi cũ nhân tiện:** `naive-bayes` có **hai `<section id="nb-s4">`** — sinh ra từ
bước sửa trước, không phải phiên này. Đã sửa mục *Các biến thể* thành `nb-s5`. Từ nay quét bằng
đoạn kiểm `id trùng + <b>NN</b> liên tục` sau mỗi bài.

### Kệ 03-cs-fundamentals — 4/11 bài xong

| Bài | Mục trước → sau | Ghi chú |
|---|---|---|
| `process-thread-scheduling` | 5 → 7 | tách *Process so với thread* khỏi §01 |
| `lock-deadlock-race` | 5 → 7 | tách *Race condition* khỏi §01; mục *Deadlock* đang có 2 hình nên cắt đôi thành *Deadlock — bốn điều kiện* (bản đồ) + *Phá vòng chờ* (SVG vòng chờ cũ) |
| `memory-virtual-paging` | 6 → 7 | tách *Ảo giác và cô lập* + *Hai process, hai page table* khỏi §01 |
| `caching` | 8 → 7 | 4 ô ①–④ khớp đúng s2–s5, không phải tách mục nào |

**Bẫy thứ tư:** mục nào **đã có `<figure>` riêng** thì chèn bản đồ vào là thành 2 hình, phạm luật
*mỗi mục một hình*. Cách xử đúng là **cắt mục làm hai** (bản đồ ở mục khái niệm, hình cũ ở mục
chi tiết), không phải xoá hình cũ — hình cũ thường là thứ dạy tốt nhất trong bài.
Kiểm bằng cột `svg` mà `/tmp/apply.py` in ra: phải là `[1,1,…,1,0]`, số 0 cuối là mục *Hỏi đáp*.

**Trả một món nợ cũ (#6) nhân tiện:** chip `stale-while-revalidate=60` trong `.strip` của
`caching` tràn ngang ở 490px. Sửa ở `assets/style.css` breakpoint hẹp — thêm
`.strip .c i,.strip .c u{overflow-wrap:anywhere}`. Sửa một chỗ, 29 bài dùng `.strip` cùng được.

**✅ Kệ 03-cs-fundamentals hết nhóm D — 11/11 bài.** `/tmp/t4.py`: **A=55 · P=0 · D=34 · E=27**
(đầu bước 6: A=38 · D=51). `build.py` sạch, 490px sạch trên cả 11 bài, quét id/số toàn kho 0 lệch.
`os-overview` không có `figure.gist` ở §01 — đúng, nó là bài overview, thuộc diện miễn trừ.

| Bài | Mục | Cách xử |
|---|---|---|
| `dns-tls` | 6 → 6 | tách *DNS phân giải thế nào* khỏi §01 |
| `load-balancing` | 7 → 7 | tách *Vì sao cần* khỏi §01 |
| `rest-api-design` | 7 → 7 | tách *Tài nguyên, không phải hành động* khỏi §01 |
| `tcp-http` | 12 → 12 | **ca riêng** — xem dưới |
| `cap-theorem-consistency` | 8 → 8 | 5 ô ①–⑤ khớp s2–s6, tách *Vấn đề* khỏi §01 |
| `consensus-leader-election` | 5 → 5 | tách *Vấn đề* khỏi §01 |
| `messaging-queue-pubsub` | 8 → 8 | tách *Vấn đề* khỏi §01 |

**Bẫy thứ năm — bài đã có gist sẵn ở §01 (`tcp-http`).** Hình *Tổng kết* của nó không phải bản đồ
cả bài mà là bản đồ **nửa sau** (thử lại · backoff · timeout). Xoá đi là mất một hình dạy tốt.
Cách xử đúng: **chuyển nó lên làm mục mở đầu của nửa đó** (mục 06 *Khi một vòng không về*),
`figure.gist` → `figure.scrollx`, sửa "Ô trái/giữa/phải" thành "Mục 07/08/10" cho khớp số mới.
Luật rút ra: hình *Tổng kết* nào **chỉ tóm một phần bài** thì đẩy lên đầu phần đó, không ép làm
bản đồ toàn bài.

Còn lại: 04-database (14) → 05-ml (20, ưu tiên `dbscan`, `mle-map`,
`supervised-unsupervised` như người dùng nêu).

### Chen ngang 07/09 — kệ tree-models phải VẼ RA CÂY (trục **chuẩn khuôn hình**)

Người dùng review bằng mắt và bác cả ba gist chính của `06-tree-models`:

> *"đảm bảo các bài tree đều có hình tree hay nhiều cây, thể hiện đúng bản chất bagging hoặc
> boosting nhé, như adaboost tôi chưa thấy đâu, với ① Dữ liệu có trọng số đâu cần có trọng số?"*

**Đúng cả hai.** Đo lại thì rõ: `rf-s1` có `rect=10 line=3`, `rf-s2` `rect=17 line=1` — toàn chữ
đóng hộp, **không một cái cây nào**. `gb-s1` y hệt. `ada-s1` có đúng một stump nhưng trọng số chỉ
mã hoá bằng **bán kính chấm** (r=2,6 vs r=6,0) — nhìn ảnh chụp thì không đọc ra được là trọng số.

**Lỗi gốc không phải ở từng bài mà ở chỗ không có primitive chung.** Mỗi bài tự vẽ nên bài nào
lười thì thành hộp chữ. Đã chữa tận gốc: thêm **`tree()` và `forest()` vào `tools/svgkit/base.py`**
— từ nay mọi bài tree vẽ cây bằng đúng hai hàm đó, đúng luật 5 *"1–2 hình thù lặp lại cả kho"*.

| Bài | Sửa | Nhìn ra cái gì |
|---|---|---|
| `adaboost` | ô ① đổi chấm-to-nhỏ → **bảng thanh trọng số có số** (0,06 / 0,30, điểm sai tô đỏ); thêm dải **5 stump nối tiếp** mũi tên ngang, mỗi cái một α | boosting = nối tiếp, phiếu không đều |
| `random-forest` | thêm dải **5 cây song song** cùng toả từ một tập huấn luyện, mỗi cây một phiếu, gộp bằng đa số | bagging = song song, phiếu ngang nhau |
| `gradient-boosting` | thêm dải **5 cây nối tiếp**, trên mỗi cây ghi `r = y − Fₖ`, dưới ghi `F + η·hₖ` | boosting cộng dồn phần dư |
| `lightgbm` | §01 vốn **0 hình** (phạm luật 1) — vẽ gist **hai cây cạnh nhau**: level-wise mở đều cả tầng vs leaf-wise dồn cả ba lần tách vào nhánh gain lớn nhất; bỏ `.cmp` cũ vì hình đã nói đủ | vì sao cây LightGBM lệch |

Cặp adaboost ↔ random-forest giờ **phân biệt được bằng mắt trong một giây**: mũi tên ngang nối
cây với cây (nối tiếp) so với các đường đứt toả xuống từ một hộp (song song). Trước đây phải đọc
chữ mới biết bài nào là bagging.

**Bẫy thứ sáu — số trong hình phải đếm lại bằng tay.** Bản đầu của hình `lightgbm` ghi tiêu đề
*"cùng 6 lần tách"* trong khi mỗi bên chỉ vẽ **ba** lần tách. `check.py` không bắt được loại lỗi
này (nó chỉ soát chồng chữ và tràn khung) — chỉ có đếm bằng mắt trên ảnh chụp mới ra.

**Bẫy thứ bảy — nhãn hình mô tả BIẾN TRONG như thể là YÊU CẦU ĐẦU VÀO.** Ô ① của `adaboost`
ban đầu tên *"Dữ liệu có trọng số"*. Người dùng đọc ra ngay: *"data bình thường cũng được mà?"* —
và đúng: trọng số là **biến trong** của AdaBoost, nó tự khởi tạo `wᵢ = 1/n` rồi tự cập nhật;
dữ liệu vào là dữ liệu thường, không cần cột `w` nào. Đã đổi thành *"AdaBoost tự gán trọng số"*,
thêm chú thích *"vào là dữ liệu thường, KHÔNG cần cột trọng số"*, và sửa cả câu `p.key` vốn mắc
đúng lỗi ấy (*"Mỗi điểm dữ liệu mang một trọng số"*). Quét cả kho: không còn chỗ nào khác.
Luật rút ra: **nhãn ô phải nói ai làm việc đó**, không được viết như một thuộc tính có sẵn của
dữ liệu — người đọc sẽ hiểu thành điều kiện để dùng được thuật toán.

**Một lỗi công cụ cần biết:** `shot.py` trước đây **không nạp webfont**, nên mọi ảnh chụp để soát
mắt từ trước 07/09 đều rơi dấu tiếng Việt ("BỐN VIỆC" hiện thành "BÓN VIỆC"). Đã vá (thêm link
Google Fonts vào HTML tạm). Hệ quả: **những lần soát mắt trước đó đều nhìn nhầm chữ**, cần soát lại.

Nghiệm thu: `build.py` sạch · `check.py` 0 lỗi trên cả 4 hình mới · `/tmp/http2.py` 490px
**tran=0 hinh_lech=0 trên cả 7 bài** của kệ.


### ⚠ 2026-09-07 chiều — SÁU tiêu chí, không phải ba. Có `tools/audit.py` rồi

Người dùng: *"random-forest là check chưa kĩ rồi đó"* — **đúng**. Tôi báo `random-forest` đạt
trong khi nó 13 mục, phạm luật C; và cả kho có **87 bài §01 chưa mang tên `Mental model`** mà
không metric nào trước đây đo.

Người dùng chốt lại tinh thần của luật 1, ghi nguyên văn kẻo lại quên:

> *"đổi `Tổng kết một hình` thành mental model mà, bài nào cũng cần mental model, thế mới dễ học,
> và các mục dưới là bóc tách mental model đó ra"*

Tức mục *Tổng kết* **không bị xoá** — nó được **chuyển lên đầu bài** thành `Mental model`, và các
mục dưới là các lần bóc tách chính bản đồ đó.

**Nguyên nhân gốc của việc đo sai nhiều lần: mỗi đợt tôi tự nghĩ ra một metric rời rạc**
(`/tmp/ver.py`, `/tmp/vera.py`, `/tmp/tight.py`, `/tmp/t3.py`, `/tmp/t4.py`, `/tmp/d.py` — sáu
script, sáu con số khác nhau) và mỗi cái bỏ sót một trục. Đã chữa tận gốc: **`tools/audit.py`**
đo cả sáu tiêu chí một lượt, nằm trong repo, không phải `/tmp`.

```bash
python3 tools/audit.py            # bảng tóm tắt + danh sách bài chưa đạt
```

**Sáu tiêu chí — bài phải đạt CẢ SÁU mới được ghi "xong":**

| Cờ | Nghĩa |
|---|---|
| `gist@s1` | §01 chứa `<figure class="gist">` — bản đồ cả bài |
| `ten` | §01 mang đúng tên `Mental model` |
| `gist=1` | cả bài dùng **một** `figure.gist` |
| `TK` | không còn mục *Tổng kết một hình* (nó đã thành §01) |
| `thieu` | mọi mục nội dung có ít nhất một khối trực quan |
| `C` | dưới 12 mục |

**Số thật lúc đo đầu (07/09 chiều): 116 bài có nội dung · chỉ 26 đạt cả sáu.**

| Lỗi | Số bài |
|---|---|
| §01 chưa tên `Mental model` | 87 |
| thiếu `gist@s1` | 57 |
| số gist ≠ 1 | 57 |
| còn *Tổng kết* | 34 |
| mục thiếu hình | 12 |
| ≥12 mục (luật C) | 8 |

**Đã làm trong đợt này — trục luật 1:**

| Việc | Kết quả |
|---|---|
| Đổi tên §01 → `Mental model` cho bài **đã có** gist ở §01 | 30 bài. *Cố ý không đổi 57 bài chưa có gist* — đổi tên khi chưa có hình là nói dối |
| `dbscan` · `mle-map` · `supervised-unsupervised` | ✅ ba bài người dùng chỉ đích danh, xong |
| Thêm `tools/apply_map.py` | biến một bài nhóm D sang khuôn mental model, tự đánh số lại, tự kiểm id trùng |
| Chuyển `/tmp/mapgen2.py` vào `tools/svgkit/mapgen.py` | hết cảnh công cụ sống trong `/tmp` rồi mất |

**Đạt cả sáu: 26 → 48.** `build.py` sạch · 490px `TONG 0` trên cả ba bài mới.

**`random-forest` — trạng thái thật:** đạt luật 1, đạt chuẩn khuôn hình, đạt chuẩn đặt tên,
**nhưng 13 mục nên phạm luật C**. Chưa xong. Bảy bài cùng cảnh: `transaction-isolation` 16 ·
`sql-window-functions` 15 · `sql-index-query-plan` 14 · `decision-tree` 14 ·
`metrics-confusion-matrix` 13 · `tcp-http` 12 · `dict-hash-table` 12.

**Luật của mọi báo cáo từ nay:** chạy `python3 tools/audit.py`, dán số của nó. Không được tự
nghĩ metric mới rồi báo — đó đúng là thứ đã làm hỏng ba đợt liên tiếp.

### 2026-09-07 tối — **trục luật 1** — kệ 05-machine-learning: XONG

`python3 tools/audit.py` — **72/116 đạt cả sáu tiêu chí**, và **kệ ML còn 0 bài chưa đạt**.

Đợt này làm:

| Việc | Bài |
|---|---|
| Dựng mục 01 `Mental model` + bản đồ, xoá *Tổng kết một hình* | `bias-variance-tradeoff` · `train-val-test-cv` · `feature-engineering` · `ab-testing` · `logistic-regression` · `statistics` · `overfitting-regularization` · `tree-family-overview` |
| Đã có `Mental model` sẵn nhưng còn *Tổng kết* → gộp bản đồ lên đầu | `linear-regression` (hình tán xạ tách thành mục 02) · `metrics-confusion-matrix` |
| Hai `figure.gist` trong một bài → hình phụ đổi sang `scrollx` | `lightgbm` · `clustering-overview` · `tree-family-overview` |
| Luật C (<12 mục) — gộp mục con thành `<h3>` | `statistics` 12→11 · `metrics-confusion-matrix` 13→11 · `decision-tree` 14→11 · `random-forest` 13→11 |
| Nợ cũ: adaboost hardcode "BỐN MƯƠI" | đổi sang `T`/`h_T`/`α_T·h_T(x)`; chỉ giữ 40 ở dòng **đo thật** |

Mỗi lần gộp/đánh số lại đều phải **soát chữ "mục NN" trong văn xuôi và trong SVG** — đã sửa ở
`statistics`, `overfitting-regularization`, `metrics-confusion-matrix`, `random-forest`.

Kiểm: `tools/build.py` sạch (200 bài · 1470 mục · 506 thẻ · meta khớp) · `tools/audit.py` 72/116 ·
490px `TONG 0`.

Còn lại theo kệ: **04-database 19** (đang tạm hoãn theo ý người dùng), **01-dsa 17** (tạm hoãn),
**02-python 5**, **03-cs-fundamentals 3**. Kệ tiếp theo nên làm: **02-python** rồi **03-cs-fundamentals**.


## Tiêu chí xếp loại — theo luật 1 của [[chuan-bai-mau]]

Ver mới = §01 tên `Mental model` + `figure.gist` **nằm trong** §01 + **không** còn mục
*Tổng kết một hình* ở cuối.

| Loại | Nghĩa | Số bài |
|---|---|---|
| **A** | ver mới đủ ba điều kiện | **10** |
| **B** | gist đúng ở §01, chỉ còn đổi tên đầu mục | **28** |
| **B2** | gist nằm trong `<section>` nhưng **không phải §01** — nợ nặng hơn B | **5** |
| **C** | gist lơ lửng ngoài mọi `<section>` | **2** |
| **D** | ver cũ — còn *Tổng kết một hình* ở cuối | **51** |
| **E1** | chưa có hình mental model — **nợ thật** | **17** |
| **E2** | kệ 01-DSA, ngoại lệ có chủ ý theo CLAUDE.md | **15** |
| **F** | khung chưa viết | **72** |
| | **tổng** | **200** |

**Nợ thật để lên ver mới: 70 bài** = D 51 + C 2 + E1 17. Nhóm B/B2 rẻ hơn (đã có hình đúng, chỉ
sai chỗ đặt hoặc tên mục) — theo [[chuan-bai-mau]] thì **đổi khi chạm từng bài**, đừng mở đợt sửa
33 file chỉ để đổi chữ.

## A — ver mới đủ (10)

| Kệ | Nhóm | Bài | chữ/hình |
|---|---|---|---|
| 01-dsa | 02-foundations | big-o-complexity | 253 |
| 02-python | 02-language-core | iterator-generator | 290 |
| 02-python | 02-language-core | memory-management-gc | 283 |
| 02-python | 02-language-core | memory-model-mutability | 279 |
| 02-python | 03-builtin-structures | dict-hash-table | 333 |
| 05-ml | 05-classical-ml | knn | 287 |
| 05-ml | 05-classical-ml | naive-bayes | 286 |
| 05-ml | 05-classical-ml | svm | 281 |
| 05-ml | 05-classical-ml | ridge-lasso-elasticnet | 274 |
| 05-ml | 06-tree-models | adaboost | 279 |

Nhánh `05-classical-ml` + `adaboost` lên ver mới **mà không nhật ký nào ghi** — phát hiện khi đo lại.

## B — gist đúng §01, chỉ cần đổi tên đầu mục thành `Mental model` (28)

| Kệ | Nhóm | Bài | §01 hiện tại | chữ/hình |
|---|---|---|---|---|
| 01-dsa | 03-data-structures | array-string | Ý tưởng | 314 |
| 01-dsa | 03-data-structures | hash-map | Ý tưởng | 280 |
| 01-dsa | 03-data-structures | data-structures-overview | Cấu trúc nào cũng đánh đổi | 180 |
| 01-dsa | 04-algorithms | prefix-sum | Ý tưởng | 345 |
| 01-dsa | 04-algorithms | sorting | Ý tưởng | 298 |
| 01-dsa | 04-algorithms | algorithms-overview | Dấu hiệu nhận đề | 148 |
| 02-python | 03-builtin-structures | list-tuple-set | Bảng chi phí | 295 |
| 02-python | 04-concurrency | asyncio | Event loop và await | 127 |
| 02-python | 04-concurrency | thread-process-gil | Process, thread và GIL | 122 |
| 02-python | 06-oop | oop-python | Class và object | 119 |
| 03-cs | 03-networking | networking-overview | Một request đi qua đâu | 177 |
| 04-db | 01-overview | db-overview | Database là gì | 198 |
| 04-db | 03-sql-basics | sql-basics-overview | Thứ tự thực thi thật | 200 |
| 04-db | 04-sql-advanced | sql-window-functions | Window function là gì | 156 |
| 04-db | 04-sql-advanced | transaction-isolation | Transaction là gì | 153 |
| 04-db | 04-sql-advanced | sql-index-query-plan | Từ câu SQL tới kết quả | 123 |
| 04-db | 04-sql-advanced | sql-advanced-overview | Câu SQL đúng vẫn có thể hỏng | 113 |
| 04-db | 05-beyond-sql | sharding-replication | Từ một máy tới nhiều máy | 172 |
| 05-ml | 01-overview | ml-overview | Machine learning là gì | 217 |
| 05-ml | 02-math-foundations | math-foundations-overview | Vì sao ML cần toán | 223 |
| 05-ml | 04-core-concepts | core-concepts-overview | Câu hỏi chung của cả nhóm | 241 |
| 05-ml | 05-classical-ml | classical-models-overview | Giả định là thứ phân biệt chúng | 228 |
| 05-ml | 06-tree-models | gradient-boosting | Gradient boosting là gì | 197 |
| 05-ml | 06-tree-models | xgboost | XGBoost là gì | 183 |
| 05-ml | 06-tree-models | decision-tree | Decision tree là gì | 140 |
| 05-ml | 06-tree-models | random-forest | Random forest là gì | 123 |
| 05-ml | 07-clustering | clustering-overview | Không có định nghĩa nào cho "cụm" | 214 |
| 05-ml | 09-evaluation | evaluation-overview | Đánh giá đang trả lời câu hỏi nào | 226 |

## B2 — gist trong `<section>` nhưng KHÔNG ở §01 (5) — toàn bài overview

| Kệ | Nhóm | Bài | gist đang ở | §01 hiện tại |
|---|---|---|---|---|
| 01-dsa | 01-overview | dsa-overview | §02/3 | DSA là gì |
| 02-python | 01-overview | python-overview | §03/6 | Python là ngôn ngữ gì |
| 02-python | 02-language-core | language-core-overview | §02/4 | Vấn đề |
| 03-cs | 01-overview | cs-overview | §02/3 | Kệ này học gì |
| 04-db | 02-relational-basics | relational-overview | §02/2 | Mô hình quan hệ là gì |

Cả năm đều là `*-overview`, và **§01 của cả năm đều 0 hình** — nên không phải "dời hình xuống
một mục" mà là dời hẳn gist lên §01, rồi xử lý chỗ trống nó để lại ở mục cũ.

## C — gist lơ lửng ngoài mọi `<section>` (2)

| Kệ | Nhóm | Bài | §01 | chữ/hình |
|---|---|---|---|---|
| 05-ml | 06-tree-models | lightgbm | Mental model | 261 |
| 05-ml | 06-tree-models | tree-family-overview | Vấn đề | 217 |

Di sản đợt tree-models — mục lục không trỏ tới được, sửa rẻ (chuyển vào §01).

## D — ver cũ, còn *Tổng kết một hình* (51)

| Kệ | Nhóm | Bài | §01 hiện tại | chữ/hình | TK |
|---|---|---|---|---|---|
| 02-python | 02-language-core | data-model-dunder | Ý tưởng | 248 | 4/6 |
| 02-python | 02-language-core | scope-legb | Ý tưởng | 232 | 5/7 |
| 02-python | 02-language-core | exception-handling | Ý tưởng | 220 | 5/7 |
| 02-python | 02-language-core | decorator-context-manager | Vì sao phải hiểu closure trước | 189 | 6/8 |
| 02-python | 07-typing | typing-dataclass | Vì sao có type hints | 191 | 6/8 |
| 02-python | 08-performance | performance-profiling | Đo trước, đoán sau | 175 | 4/6 |
| 03-cs | 02-os | process-thread-scheduling | Process so với thread | 267 | 5/7 |
| 03-cs | 02-os | lock-deadlock-race | Race condition | 254 | 4/6 |
| 03-cs | 02-os | memory-virtual-paging | Vì sao cần virtual memory | 244 | 5/6 |
| 03-cs | 03-networking | tcp-http ✚ | TCP và HTTP nằm ở đâu | 317 | 10/12 |
| 03-cs | 03-networking | load-balancing | Vì sao cần | 252 | 5/7 |
| 03-cs | 03-networking | caching | Vì sao cache là câu trả lời mặc định | 248 | 6/8 |
| 03-cs | 03-networking | dns-tls | DNS phân giải thế nào | 235 | 4/6 |
| 03-cs | 03-networking | rest-api-design | Tài nguyên, không phải hành động | 235 | 5/7 |
| 03-cs | 04-distributed | cap-theorem-consistency | Vấn đề | 157 | 7/8 |
| 03-cs | 04-distributed | consensus-leader-election | Vấn đề | 147 | 4/5 |
| 03-cs | 05-messaging | messaging-queue-pubsub | Vấn đề | 219 | 6/8 |
| 04-db | 02-relational-basics | relational-model | Quan hệ là gì | 243 | 6/8 |
| 04-db | 02-relational-basics | db-normalization | Vấn đề: dị thường cập nhật | 219 | 5/7 |
| 04-db | 02-relational-basics | constraints-integrity | Các loại ràng buộc | 212 | 5/7 |
| 04-db | 03-sql-basics | sql-select-filter | Thứ tự thực thi logic | 249 | 5/7 |
| 04-db | 03-sql-basics | sql-subquery-cte | Truy vấn con ở ba chỗ | 226 | 6/8 |
| 04-db | 03-sql-basics | sql-group-aggregate | Gom nhóm làm gì | 210 | 5/7 |
| 04-db | 03-sql-basics | sql-join | Các loại join | 160 | 5/7 |
| 04-db | 04-sql-advanced | query-tuning | Quy trình sáu bước | 329 | 7/9 |
| 04-db | 05-beyond-sql | nosql-landscape | "NoSQL" không phải một công nghệ | 266 | 5/7 |
| 04-db | 06-data-systems | data-quality ✚ | Vấn đề | 417 | 5/7 |
| 04-db | 06-data-systems | etl-elt | Vấn đề | 204 | 5/7 |
| 04-db | 06-data-systems | oltp-vs-olap | Vấn đề | 202 | 6/7 |
| 04-db | 06-data-systems | batch-stream-processing | Vấn đề | 196 | 5/7 |
| 04-db | 06-data-systems | data-warehouse-lake | Vấn đề | 163 | 5/7 |
| 05-ml | 02-math-foundations | probability-basics | Biến ngẫu nhiên & phân phối | 295 | 4/6 |
| 05-ml | 02-math-foundations | expectation-variance | Kỳ vọng | 242 | 5/6 |
| 05-ml | 02-math-foundations | mle-map | Vấn đề: loss function ở đâu ra | 196 | 6/7 |
| 05-ml | 02-math-foundations | gradient-optimization | Đạo hàm riêng & gradient | 181 | 5/6 |
| 05-ml | 02-math-foundations | linear-algebra-ml | Vector & tích vô hướng | 178 | 5/6 |
| 05-ml | 02-math-foundations | bayes-theorem | Vấn đề: đảo chiều điều kiện | 164 | 4/5 |
| 05-ml | 03-statistics | ab-testing | A/B test là thống kê cộng thêm hạ tầng | 259 | 7/9 |
| 05-ml | 04-core-concepts | bias-variance-tradeoff | Phân rã sai số | 268 | 7/8 |
| 05-ml | 04-core-concepts | train-val-test-cv | Vì sao ba tập chứ không hai | 251 | 7/9 |
| 05-ml | 04-core-concepts | supervised-unsupervised | Câu hỏi phân loại bài toán | 245 | 5/6 |
| 05-ml | 04-core-concepts | feature-engineering | Biến phân loại | 230 | 5/7 |
| 05-ml | 05-classical-ml | linear-regression ✚ | Linear regression là gì | 278 | 8/10 |
| 05-ml | 05-classical-ml | logistic-regression | Vì sao không dùng linear regression… | 214 | 8/10 |
| 05-ml | 07-clustering | hdbscan | Vấn đề nó giải | 279 | 7/9 |
| 05-ml | 07-clustering | kmeans-clustering | Vấn đề nó giải | 244 | 6/8 |
| 05-ml | 07-clustering | dbscan | Vấn đề nó giải | 205 | 8/10 |
| 05-ml | 08-dimensionality | pca-dimensionality | Vấn đề nó giải | 253 | 6/8 |
| 05-ml | 09-evaluation | metrics-confusion-matrix ✚ | Vì sao accuracy không đủ | 303 | 11/13 |
| 05-ml | 09-evaluation | calibration | Vấn đề nó giải | 287 | 6/8 |
| 05-ml | 09-evaluation | roc-auc-pr | Từ confusion matrix tới đường cong | 244 | 5/7 |

**Bốn bài D có dấu ✚ đã có `figure.gist` đúng ở §01** (`tcp-http`, `data-quality`,
`linear-regression`, `metrics-confusion-matrix`) — chúng chỉ còn phải **gỡ mục *Tổng kết một hình***
và đổi tên §01, tức nợ nhẹ hơn hẳn 47 bài kia (phải dựng hình từ đầu). Bốn bài này cũng chính là
bốn trong sáu bài "có nhiều hơn một gist" ở mục bẫy bên dưới — gist thứ hai nằm trong mục Tổng kết,
nên gỡ mục đó là hết trùng luôn.

## E1 — chưa có hình mental model, nợ thật (17)

| Kệ | Nhóm | Bài | §01 hiện tại | chữ/hình |
|---|---|---|---|---|
| 02-python | 05-toolkit | leetcode-toolkit | Sáu thứ này tiết kiệm cái gì | 302 |
| 03-cs | 02-os | os-overview | OS chia một máy thế nào | 157 |
| 04-db | 02-relational-basics | er-modeling | Thực thể và quan hệ | 341 |
| 05-ml | 03-statistics | statistics | Thống kê trả lời câu hỏi nào | 204 |
| 05-ml | 04-core-concepts | overfitting-regularization | Nhận biết bằng số, không bằng cảm giác | 424 |
| 06-dl | 02-neural-network | normalization | Vì sao cần normalization | 319 |
| 06-dl | 02-neural-network | backpropagation | Backpropagation là gì | 253 |
| 06-dl | 02-neural-network | weight-initialization | Khởi tạo trọng số là gì | 243 |
| 06-dl | 03-cnn | cnn-mobilenet | CNN là gì | 255 |
| 07-tf | 02-transformer-core | self-attention | Self-attention là gì | 341 |
| 07-tf | 02-transformer-core | transformer-architecture | Từ một phép attention tới một model | 252 |
| 08-llm | 02-training | peft-lora-qlora | Vì sao không fine-tune toàn bộ trọng số | 239 |
| 08-llm | 02-training | sft-alignment | Fine-tuning và alignment là gì | 204 |
| 08-llm | 04-inference | inference-optimization | Inference optimization là gì | 271 |
| 08-llm | 05-rag | rag-end-to-end | RAG là gì | 226 |
| 09-mlsd | 02-frameworks | ml-system-design | Khung bảy bước | 283 |
| 10-mlops | 03-lifecycle | mlops-serving | MLOps là gì | 209 |

**E1 không đồng đều — chia ba mức việc:**

| Mức | Bài | Việc phải làm |
|---|---|---|
| §01 đã có SVG rời (`<figure>`+`<svg>`) | `leetcode-toolkit`, `er-modeling`, `statistics`, `rag-end-to-end`, `mlops-serving` | gắn class `gist`, chỉnh hình cho nói đúng câu định nghĩa |
| §01 chỉ có khuôn `.cmp/.stack/.bars/.mtx` | `os-overview`, `overfitting-regularization`, `backpropagation`, `weight-initialization`, `cnn-mobilenet`, `self-attention`, `peft-lora-qlora`, `sft-alignment`, `inference-optimization`, `ml-system-design` | khuôn không phải hình mental model — phải **dựng hình mới** |
| §01 **không hình gì** | `normalization`, `transformer-architecture` | dựng từ đầu, nặng nhất |

**12 bài của kệ 06→10 chưa từng được đếm trong nhật ký nào** — chúng viết trước khi luật 1 ra đời.
Trước lần đo này, nhật ký ngầm coi 06→10 là "toàn khung". Không phải: 12 bài đã có nội dung.

## E2 — kệ 01-DSA, ngoại lệ có chủ ý (15)

`heap-priority-queue` 544 · `tree-bst-traversal` 542 · `union-find` 464 · `graph-bfs-dfs-topo` 413 ·
`dynamic-programming` 406 · `backtracking` 357 · `linked-list` 348 · `stack-monotonic-queue` 348 ·
`intervals` 336 · `sliding-window` 320 · `two-pointers` 309 · `shortest-path` 298 · `trie` 225 ·
`binary-search` 215 · `greedy` 166.

CLAUDE.md chốt khuôn DSA riêng, §01 đã là "1 hình + 1 câu chốt" — **không tính là nợ**. Nhưng
chữ/hình của nhóm này cao nhất kho (trung vị ~348 so với 123 của bài mẫu), nên nếu có đợt tăng mật
độ hình thì đây là chỗ đáng vào nhất.

## F — khung chưa viết (72)

06-dl 14 · 07-transformer 14 · 08-llm 27 · 09-mlsd 4 · 10-mlops 13. Danh sách tên nằm trong
`CLAUDE.md`; đừng chép lại ở đây, nó lệch ngay khi viết xong một bài.

## Trục thứ hai — chín luật [[toi-thieu-de-hieu]] (đo lại sau đợt sửa 2026-09-06 chiều)

Bảng A/…/F ở trên đo **luật 1**. Chín luật A→I của [[toi-thieu-de-hieu]] là **trục vuông góc**:
một bài loại A vẫn có thể vi phạm cả chín. Ngày 06/09 đã mở một đợt sửa **chỉ trong kệ 01→05**
(116 bài có nội dung), 81 file đổi. Số dưới đây là **đo lại sau khi sửa**, không phải mục tiêu.

| Luật | Trước đợt | Sau đợt | Ghi chú |
|---|---|---|---|
| **A** chữ meta trong hình | 16 bài · 220 chỗ | **6 bài · 6 chỗ** | 6 chỗ còn lại là tiêu đề `.gist` hợp lệ, không phải nợ — **nhưng 10/16 bài hình vỡ, xem việc #1** |
| **B** hình không đúng hình dạng cấu trúc | 11 bài | chưa đụng | vẫn nợ, xem danh sách cũ |
| **C** quá dài (≥12 mục) | 17 bài | **8 bài** | giảm nhờ luật I chứ không phải cắt riêng |
| **D** chữ nên nằm trong khuôn HTML | 15 hình | **18 hình** (metric siết lại) | 3 hình đã chuyển sang `div.grid2`; con số tăng vì **đổi cách đo**, không phải hỏng thêm |
| **H** chữ cho người mới | 10 đầu mục đếm số | **0** | |
| **I** cắt phần không core | — | làm ở `xgboost` | mẫu để chiếu |

> **Cảnh báo:** đợt này chỉ chạy **trục A→I**. Không bài nào lên ver mới nhờ nó — trục luật 1
> (bảng A/…/F ở trên) đứng yên. Đừng đọc bảng dưới thành "đã sửa xong 75 bài".

### Điều lớn nhất phát hiện trong đợt này — 137 nhãn `BẢN ĐỒ` là MỘT lỗi, không phải 137 lỗi

Mọi mục thân bài của 16 bài đều **vẽ lại nguyên bản đồ §01**, làm mờ, trong một cột trái rộng
~304px, rồi mới "phóng to" sang ô của mục — đúng thứ luật F2 cấm. Một phép biến hình chạy một lượt
gỡ hết: bỏ mọi phần tử có max-x ≤ 310, dời phần còn lại về x=0, rồi **nhân giãn** x và `width`
theo `k = W/(W−dx)`.

**Phép này chạy nửa vời ở 10/16 bài — xem việc #1 ở đầu file.** Nhịp xoá chạy, nhịp dời+giãn
không chạy, để lại khoảng trắng 366px. Ghi lại ở đây để ai đọc mục này đừng tưởng nó đã xong.

**Phải nhân giãn chứ không được chỉ thu `viewBox`** — cả kho dùng `viewBox` rộng 860, thu lại thì
cỡ chữ của bài đó to hơn mọi bài khác. Và `<polygon>` (đầu mũi tên) chỉ được **dời**, không giãn,
không thì mũi tên méo; `<polyline>` thì giãn như mọi thứ khác. Quên `polyline` trong regex là
`decision-tree`/`gradient-boosting` trượt ngưỡng phủ 92% và báo `PARSE-MISS`.

16 bài đã gỡ: `iterator-generator` · `memory-management-gc` · `memory-model-mutability` ·
`dict-hash-table` · `asyncio` · `thread-process-gil` · `oop-python` · `performance-profiling` ·
`sql-index-query-plan` · `sql-window-functions` · `transaction-isolation` · `sharding-replication` ·
`adaboost` · `decision-tree` · `gradient-boosting` · `random-forest`.

### Luật D — 18 hình còn là chữ đóng hộp, chia ba mức

Metric cũ (`rect≥4 && cong≤2`) ra 96 hình — **sai**, vì ô chữ nhật vẽ ô mảng là *đúng* theo luật B.
Metric đã siết: **0 nét nối (`line`/`polyline`/`path`/`polygon`) VÀ ≥3 rect rộng ≥60 cao ≥22**.

| Mức | Hình | Việc |
|---|---|---|
| **Sẽ tự biến mất** — nằm trong mục *Tổng kết một hình* | `rest-api-design` rest-s5 · `constraints-integrity` constraint-s5 · `nosql-landscape` nosql-s5 · `expectation-variance` expvar-s5 · `linear-algebra-ml` linalg-s5 · `supervised-unsupervised` para-s5 | **đừng sửa** — 6 bài này thuộc nhóm D, lên ver mới là gỡ cả mục |
| **Báo động giả — là BẢNG, vẽ đúng** | `data-structures-overview` dsov-s1 · `oltp-vs-olap` -s3 · `train-val-test-cv` cv-s2 + cv-s3 · `db-normalization` norm3-s1 | ô chữ nhật *là* ô bảng / *là* fold; câu dài chỉ 1–6 trên 19–31 nhãn. **Không phải nợ** |
| **Nợ thật — văn xuôi nhét vào ô** | `big-o-complexity` bigo-s5 · `linked-list` llist-s1 · `stack-monotonic-queue` stack-s1 · `sliding-window` window-s1 · `er-modeling` ermod-s3 + ermod-s5 · `statistics` stats-s9 | 11–21 nhãn ≥7 từ mỗi hình; chuyển sang `div.grid2`+`div.card` hoặc `<table>` |

**Cách phân biệt ba mức bằng số, dùng lại được:** đếm nhãn `<text>` có ≥7 từ. Bảng thật có ≤6;
văn xuôi đóng hộp có ≥11. Đừng chỉ đếm rect.

### Luật C — 8 bài còn ≥12 mục

`transaction-isolation` 16 · `sql-window-functions` 15 · `sql-index-query-plan` 14 ·
`decision-tree` 14 · `random-forest` 13 · `metrics-confusion-matrix` 13 · `tcp-http` 12 ·
`dict-hash-table` 12. Trung vị kho 01→05 là **7 mục · 1.800 chữ · 308 chữ/hình**.

### Luật H — 29 chỗ máy báo thì 29 đều là báo động giả

Regex bắt từ toán trong đầu mục (`gradient|chuẩn hoá|kỳ vọng|phương sai|đạo hàm|ma trận|entropy`)
ra 29 chỗ ở 17 bài, nhưng đọc ra thì **tất cả đều là tên khái niệm chính bài đó dạy** —
*Gradient descent* trong `linear-regression`, *Không chuẩn hoá thang đo* trong `dbscan`,
*Kỳ vọng* trong `expectation-variance`. Luật H nhắm từ toán **thay chỗ hành động**
("Giải đỉnh parabol" thay vì "Tìm số mỗi lá trả về"), không nhắm tên khái niệm.
**Regex này chỉ dùng để lọc ra danh sách đọc tay, đừng sửa theo nó.**

### 10 đầu mục đếm số đã đổi → 0

`leetcode-toolkit` · `cs-overview` · `tcp-http` · `transaction-isolation` · `ab-testing` ·
`ridge-lasso-elasticnet` · `adaboost` · `kmeans-clustering` · `metrics-confusion-matrix` ·
`train-val-test-cv`.

### `xgboost` — bài mẫu mới của luật H và luật I

Từ 42.257 → 40.890 byte, còn **9 mục · 2.721 chữ · 10 khối hình**. Cắt: danh sách 5 bước chỉnh
hyperparameter, thẻ *Tin thẳng feature importance* (SHAP), thẻ Hỏi đáp về giá trị thiếu, một
`ul.why` chép lại đoạn văn ngay trên nó. Và viết lại 12 chỗ chữ trong `.gist` cho người mới —
*"MỘT HÀM MỤC TIÊU — VIẾT LẠI BA LẦN"* → *"MỘT CÔNG THỨC, DÙNG CHO BA VIỆC"*,
*"① Xấp xỉ bằng parabol"* → *"① Chấm điểm một cây"*. Công thức `w* = − G/(H+λ)` **giữ nguyên** —
đó là thứ bài dạy, luật H không đụng tới.

## Hai công cụ kiểm mới — dùng lại được

**`getBBox()` KHÔNG bắt được khoảng trắng thừa.** Nó chỉ báo phần tử nằm *ngoài* `viewBox`.
Hình vỡ của việc #1 nằm gọn trong `viewBox`, chỉ lệch sang phải — nên 0 tràn mà vẫn hỏng. Muốn bắt
thì phải **đo toạ độ nhỏ nhất** của mọi phần tử, hoặc chụp ảnh trang.

**Đo tràn `viewBox` phải bằng `getBBox()` trong Chrome headless.** Ước theo số ký tự cho cả báo
động giả lẫn bỏ sót. Script chèn một đoạn JS vào bản sao tạm của trang, gọi `getBBox()` trên mọi
`text|rect|line|polygon|path|circle` trong `figure svg`, trả kết quả qua `document.title`.
Sau đợt sửa: **0 tràn trên cả 81 file**.

**Muốn biết lỗi có sẵn hay mình vừa gây ra thì dùng `git worktree`, đừng chép file sang `/tmp`.**
Chép rời làm đường dẫn `assets/` gãy, CSS không nạp, đo ra số vô nghĩa. `git worktree add -f /tmp/wt HEAD`
cho trang render đúng như thật — nhờ đó biết 4 trong 6 chỗ tràn là **có sẵn từ trước**, không phải
do đợt này.

**Cuộn ngang ở 490px KHÔNG phải lỗi.** Đo màn hình hẹp thấy `figure.scrollx` 720 > 456 và
`figure.gist` 668 > 454 — đó là `min-width` CSS cố ý đặt, cùng `.eq .line{overflow-x:auto}`.
Chỉ báo động khi phần tử **không** thuộc ba nhóm đó.

**Bẫy đã dính lần nữa:** rút ngắn nhãn cho vừa `viewBox` thì **cắt mất nội dung thật** —
`db-normalization` mất đoạn "phải có cơ chế giữ đồng bộ · ghi rõ cột nào là cache", đã trả lại
bằng một đoạn `<p>` dưới hình. Rút nhãn thì phần bị bỏ phải đi đâu đó, không được biến mất.

## Cách đo lại — năm bẫy đã dính trong chính lần đo này

1. **`figure.gist` ở `<section>` thứ hai, không phải §01.** Chỉ hỏi "có gist trong section không"
   thì năm bài overview lọt vào nhóm B (chỉ cần đổi tên) trong khi thật ra phải **dời hình**.
   Phải kiểm `gi[0] == 1` chứ không phải `gi[0] >= 1`.
2. **`<h2>` bị encode HTML entity** — 6 file (`tree-bst-traversal`, `big-o-complexity`,
   `dict-hash-table`, `er-modeling`, `gradient-boosting`, `adaboost`) có `Ý t&#432;&#7903;ng`.
   Không `html.unescape()` thì mọi phép so tên đầu mục đều trượt im lặng.
3. **Nhóm E vẫn có hình ở §01** — chỉ là không gắn class `gist`. "Không có gist" ≠ "không có hình";
   khi sửa thì thường là gắn class + chỉnh hình cho nói đúng câu định nghĩa, không phải vẽ từ đầu.
   Ngoại lệ: `normalization` và `transformer-architecture` §01 **thật sự 0 hình**.
4. **6 bài có nhiều hơn một `figure.gist`** (`array-string`, `list-tuple-set` 3 cái; `tcp-http`,
   `data-quality`, `linear-regression`, `clustering-overview` 2 cái) — ngược luật "cả bài chỉ có
   một hình mental model", đáng soát lại khi chạm vào.

5. **Metric thô luôn phải siết hai lần trước khi tin.** "Hình là chữ đóng hộp" đo thô ra 96,
   siết một lần còn 15, siết lần nữa (thêm phép đếm nhãn ≥7 từ) mới ra **7 hình nợ thật**. Ba lần
   đo cho ba con số khác hẳn nhau — con số đầu tiên của bất kỳ metric nào cũng nên coi là sai.

Tên mục *Tổng kết một hình* chỉ có **đúng một biến thể** trên cả kho (51 chỗ), nên grep chuỗi đó
là đủ, không sợ sót.

## Những phép đã kiểm và SẠCH — khỏi kiểm lại

- **200 bài** khớp ba nguồn độc lập: `glob content/*/*/*/index.html`, số `slug` trong `catalog.js`,
  và `find` (mọi index.html đều đúng độ sâu 3 cấp, không bài nào lạc chỗ). Không bài nào có trong
  `content/` mà thiếu ở `catalog.js`.
- **72 khung** khớp giữa `data-skeleton="1"` trong file và cờ `skeleton` trong `catalog.js`.
- **Cấu trúc parse sạch tuyệt đối**: mọi bài đều 1 `<section id>` = 1 `<h2>`; không `<section>` lồng
  nhau; không `<section>` thiếu `id`; không `<h2>` nào nằm ngoài mọi section. Nên phép cắt
  `re.split(r'(?=<section id=)')` và ghép `<h2>` theo thứ tự là **đáng tin**.
- **Nhóm A đủ ba nhịp** của luật 1 ở cả 10 bài: có câu định nghĩa trước hình (22–135 chữ) và có
  `figcaption`.
- **51 bài D đều đặt *Tổng kết một hình* đúng vị trí** — không bài nào còn mục nội dung nằm sau nó
  (lỗi 4 bài từng dính trong [[dot-sua-theo-chuan-bai-mau]] đã sửa xong thật).
