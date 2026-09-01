# TAXONOMY — bài nào nên tồn tại, và bài viết ra phải sạch tới đâu

Tài liệu nội bộ, không phải nội dung học. Hai phần:

- **Phần A — Sạch nghĩa là gì.** Mở bài ra sửa thì đọc phần này. Có lệnh chạy để tự kiểm.
- **Phần B — Bài nào nên tồn tại.** Định thêm/bớt/tách bài thì đọc phần này.

Số liệu dưới đây cập nhật **2026-09-02**. Đừng tin số trong tài liệu — chạy lệnh ở §A1 để lấy số thật.

---

# PHẦN A — SẠCH NGHĨA LÀ GÌ

## A1. Hai lệnh phải chạy trước khi coi là xong

```bash
python3 tools/build.py     # sinh lại chỉ mục — không được có cảnh báo
python3 tools/soat.py      # soát các lỗi build.py không bắt được
```

`build.py` bắt lỗi **cấu trúc**: bài chưa khai trong `category.json`, khai trỏ vào thư mục không có,
thiếu `index.html`, `data-base` sai số cấp `../`. Nó cũng in ra số bài / số nhóm / số mục tìm kiếm —
đây là nguồn số đáng tin duy nhất.

`soat.py` bắt lỗi **nội dung**, 5 nhóm, đúng 5 luật viết ở §A3–A7. Nó in ra từng chỗ sai kèm đường
dẫn, và thoát với mã lỗi khác 0 nếu còn chỗ phải sửa. Không có chỗ nào sai thì mọi mục đều `tổng: 0`.

Chạy xong hai lệnh, mở trình duyệt soát mắt: trang chủ, một bài có SVG (`dict-hash-table`), một bài
có lab (`binary-search`), `kit.html`, và màn hình hẹp ~490px.

## A2. Tình trạng hiện tại

94/196 bài đã viết. Ba kệ xong trọn: DSA (23), Python (14), CS fundamentals (14). Database còn 2 khung.
102 khung chờ viết, dồn ở 6 kệ sau: ML (28), LLM (27), Deep learning (14), Transformer (14), MLOps (13),
ML system design (4).

`soat.py` hiện báo **49 chỗ cần sửa** — không có chỗ nào làm vỡ trang, nhưng đều là nợ thật:

| Luật | Chỗ sai | Nặng nhẹ |
|---|---:|---|
| A3 · Không link vào khung | 6 | người đọc bấm vào ra trang rỗng |
| A4 · Chỉ dùng màu trong bảng token | 2 | lệch bảng màu, mắt thường khó thấy |
| A5 · Clay không vào hình | 0 | ✅ sạch |
| A6 · Đầu mục không đếm số | 36 | cần đọc từng chỗ, không sửa máy móc được |
| A7 · Code không tràn ngang | 5 | vỡ trên điện thoại |

## A3. Không link vào bài còn là khung

Bài đã viết mà đặt link sang một bài còn `data-skeleton="1"` thì người đọc bấm vào rơi vào trang chỉ
có dàn ý. Muốn nhắc tới khái niệm đó mà bài chủ chưa viết thì **nói tên nó trong văn xuôi, đừng đặt
link** — chờ viết xong bài chủ rồi mới nối.

Hiện sai 6 chỗ, tự hết khi viết xong 3 khung: `er-modeling` (3 bài trỏ tới), `data-quality` (2),
`vector-database` (1).

## A4. Chỉ dùng màu có trong `assets/style.css`

Mọi màu trong bài phải là một trong các mã đã khai ở `:root`. Tốt nhất là viết `var(--…)`; SVG
buộc phải ghi mã hex thì phải chép đúng mã trong bảng, không tự pha mã gần giống.

Bốn màu ngữ nghĩa, nghĩa cố định trong mọi hình:

| Mã | Biến | Nghĩa |
|---|---|---|
| `#8CA9F2` | `--filled` | dữ liệu, thứ đang xét |
| `#EDB44A` | `--probe` | con trỏ, điểm nhấn, đáp án |
| `#F2718A` | `--tomb` | sai, bị loại, chưa thoả |
| `#5BCFA0` | `--ok` | đúng, kết quả, đã thoả |

Hiện sai 2 chỗ, cùng một bài: `02-python/…/thread-process-gil` dùng `#E06C7A` — lệch khỏi `--tomb`
`#F2718A`. Sửa thành `#F2718A`.

## A5. Màu thương hiệu không được vào hình

Cam đất `--clay` `#E0855C` (và hai biến thể `#EE9E7A`, `#C96A44`) là **màu thương hiệu**: logo, nút,
link, viền mục đang đọc. Nó **không mang nghĩa nội dung**, nên tuyệt đối không dùng làm màu của một
ô, một mũi tên, một cột trong hình — người đọc sẽ tưởng nó có nghĩa như bốn màu ở §A4.

Hiện sạch, giữ nguyên vậy.

## A6. Đầu mục không đếm số

Đầu mục là **danh từ nói thẳng nội dung**, không mở đầu bằng con số: `Ba bẫy` → `Lỗi hay gặp`.
Lý do rất thực dụng: thêm hay bớt một thẻ là con số trong tiêu đề sai, và không ai nhớ sửa.

**Ngoại lệ — con số thuộc về bản chất chủ đề thì giữ.** Ranh giới:

- Con số là **sự thật của chủ đề**, không đổi dù mình viết thế nào → **giữ**.
  `Bốn ô — mọi metric đều từ đây` (confusion matrix đúng là 4 ô), `Bốn loại join`,
  `Bốn mức cô lập` (chuẩn SQL định nghĩa đúng 4 mức).
- Con số chỉ là **đếm số thẻ mình vừa viết**, thêm bớt lúc nào cũng được → **bỏ**.
  `Sáu cách regularize` → `Cách regularize`; `Năm cái bẫy thực tế` → `Bẫy thực tế`;
  `Ba mẫu code cần thuộc` → `Mẫu code cần thuộc`; `Bốn bài của nhóm` → `Học theo thứ tự nào`.

Vì thế `soat.py` chỉ **liệt kê** 36 chỗ chứ không kết luận sai — phải đọc từng chỗ mà quyết. Đọc lướt
thì phần lớn 36 chỗ đó thuộc loại thứ hai, tập trung ở [04-database](content/04-database/) (9 chỗ) và
[05-machine-learning](content/05-machine-learning/) (8 chỗ).

## A7. Code không được tràn ngang

Dòng trong `<pre>` giữ dưới ~92 ký tự. Dài hơn thì trên điện thoại trang bị đẩy ngang — một trong ba
lỗi giao diện dễ vỡ nhất của kho (hai lỗi kia: `[hidden]` thua `display:grid/flex` khi bật kết quả
tìm kiếm, và màu hardcode lệch bảng).

Hiện 5 bài vượt, dài nhất là `db-normalization` (101 ký tự).

## A8. Ba luật `soat.py` không kiểm được — phải tự đọc

Máy không đọc hiểu được, nên viết xong phải tự soát tay:

**Một khái niệm, một bài chủ.** Mỗi khái niệm chỉ có đúng một bài sở hữu. Kệ khác cần nhắc thì viết
**một mục ngắn 3–4 câu** theo đúng bốn nhịp, luôn theo thứ tự này: (1) vấn đề — vì sao khái niệm này
tồn tại; (2) định nghĩa + **gọi thẳng tên** các nhánh chính; (3) một câu đánh đổi — cái giá phải trả,
không phải liệt kê ưu điểm; (4) link tới bài chủ. Nhịp 2 bắt buộc gọi tên vì `search-index.js` tìm
theo chữ trong mục — thiếu tên thì người gõ đúng từ đó không thấy gì.

Ví dụ làm đúng: mục *Sharding & partitioning* trong `cap-theorem-consistency` — gọi tên range / hash /
consistent hashing, nói cái giá khi rebalance, rồi link sang bài chủ `04-database/sharding-replication`
mà không giảng lại cách chọn shard key.

Ba chỗ đang có nguy cơ chồng chéo, viết tới thì rà trước: **Sharding/Partitioning** (chủ duy nhất:
`04-database/sharding-replication`) · **GPU & training systems** (chủ duy nhất: `10-mlops/gpu-inference`,
không lặp ở Deep learning) · **Distributed systems** tổng quát (chồng được cả ba nơi: CS fundamentals,
Database, ML system design).

**Mỗi mục một hình.** Cần hai hình trong một mục thường là dấu hiệu mục đó nên tách đôi. Hình phải
**thay được** đoạn văn chứ không minh hoạ thêm cho nó. Chữ trong hình càng ít càng tốt. Hiện có đúng
một chỗ vượt: `decision-tree#dtree-s2` có 3 hình.

**Overview phải giữ tầng overview.** Overview cấp nhóm cũng vậy, không vì hẹp phạm vi hơn mà được đi
sâu. Nếu một mục overview đang vẽ lại cơ chế mà bài con nó trỏ tới đã vẽ rồi → cắt xuống 1–2 câu + link.
Và chọn đúng khuôn: nhóm là **các biến thể cạnh tranh nhau** (bagging vs boosting) thì dùng khuôn kể
chuyện nhân quả của [tree-family-overview](content/05-machine-learning/05-tree-models/tree-family-overview/index.html);
nhóm là **các công cụ song song** (array, hash map, heap — không cái nào sinh ra để chữa cái kia) thì
khuôn đó thành hình thức rỗng, dùng khuôn ngắn 2–3 mục như
[data-structures-overview](content/01-dsa/03-data-structures/data-structures-overview/index.html).

## A9. Hai luật cũ đã bỏ

Ghi lại để khỏi ai sửa bài theo luật đã chết:

**`details.deep` — bỏ.** CLAUDE.md từng bắt mọi bài giữ ba lớp `.key` → `.why` → `details.deep`.
Thực tế `details.deep` chỉ còn ở 2 bài (`random-forest`, `gradient-boosting`); vai trò của nó đã được
`details.qa` (mục *Hỏi đáp*, 79 bài) thay hẳn. **Không cần thêm `details.deep` vào bài mới.** Hai lớp
còn dùng thật là `.key` (75 bài) và `.why` (60 bài).

**`id="<slug>-sN"` — nới.** 11 bài viết gần đây dùng luôn tên thư mục (`oop-python-s1` thay vì
`oop-s1`). Không gây lỗi — `app.js` đọc thẳng các `<section>`, không dựa vào tiền tố. Miễn là **liên
tục từ s1** và khớp với số `<b>NN</b>` bên cạnh, đặt tên nào cũng được. (Đánh số hiện liên tục ở cả
94 bài.)

---

# PHẦN B — BÀI NÀO NÊN TỒN TẠI

## B1. Ba quyết định gốc

**1. Cấp 2 của cây taxonomy → tên nhóm** (`groups` trong `category.json`). Không tạo kệ mới, không
dựng taxonomy song song — cây `content/` là nguồn sự thật duy nhất.

**2. Bài hay mục — quyết theo mức được nhận diện và giá trị ôn lại, không theo tầng trong cây.**
Tầng chỉ mô tả quan hệ kiến thức, không quyết định ranh giới trang.

> **Câu hỏi để quyết:** cái tên này có được gọi rộng rãi (paper, phỏng vấn, codebase quốc tế đều gọi
> đúng tên này) và có đáng quay lại ôn riêng không?
> Có → **1 bài**, dù nằm ở tầng nào. Không, chỉ có nghĩa khi đọc trong ngữ cảnh khái niệm cha →
> **1 mục** trong bài của cha.

Hai lá cùng cấp vẫn có thể ra hai quyết định khác nhau: dưới cùng node *Retrieval*, `Top-k` và
`Similarity score` chỉ đáng làm mục, nhưng `Recall@K` và `MRR` đủ nổi để lên bài riêng.

**3. `01-dsa` giữ nguyên, không áp cây taxonomy CS vào.** Khuôn DSA xếp theo *dạng đề bài xuất hiện*
(55 mục pattern · 198 bài LeetCode riêng biệt / 222 lượt link), phục vụ phản xạ nhận đề. *Two pointers*
và *Sliding window* không thuộc "Searching" trong taxonomy CS, nhưng là hai pattern trung tâm khi luyện
đề — xếp theo taxonomy sẽ làm mất tác dụng đó. Muốn dùng cây taxonomy CS thì chỉ dùng để **kiểm chéo**
đã đủ pattern chưa.

## B2. Ba kệ đã xong — chốt lại đã quyết gì

Phần này trước đây là danh sách "cần làm". Nay đã làm xong, giữ lại vì nó ghi **vì sao** bài đó tồn tại.

**02. Python** — `oop-python` và `typing-dataclass` là hai lỗ thật, nay đã viết. `performance-profiling`
tách thành bài riêng thay vì gộp vào `leetcode-toolkit`. Gộp làm mục, không tách bài: Scope/Modules/
Exceptions (trong `language-core-overview`), `collections` (chia cho `list-tuple-set` và `dict-hash-table`),
Closure (trong `decorator-context-manager`), Lambda và higher-order function (không đủ sâu cho một bài).
Testing/Logging/Packaging **cố ý bỏ khỏi Python**, để bên `10-mlops`.

**03. CS fundamentals** — thêm ba bài: `cap-theorem-consistency`, `consensus-leader-election`,
`messaging-queue-pubsub`. Gộp làm mục: File systems và IPC (trong `os-overview`), HTTP/2 và HTTP/3,
WebSocket (trong `tcp-http`), RPC và gRPC (trong `rest-api-design`), Sharding (mục ngắn trong
`cap-theorem-consistency`, bài chủ ở Database). Concurrency giữ nguyên một bài `lock-deadlock-race`,
không tách nhóm riêng khỏi OS.

Ghi chú quan hệ, **không phải cấu trúc trang**: Messaging hiển thị ngang hàng với Distributed systems
cho dễ điều hướng, nhưng về mental model nó là *một phần của* Distributed systems. Không sửa giao diện
cho khớp — chỉ cần bài `messaging-queue-pubsub` mở đầu bằng bối cảnh phân tán và link ngược về
`cap-theorem-consistency`.

**04. Database** — nhóm mới *Data systems*, chặn ở đúng 6 khái niệm: OLTP vs OLAP, Data warehouse,
Data lake, ETL/ELT, Batch vs stream, Data quality. Đủ để đọc hiểu hệ thống dữ liệu mình đang dùng,
**không mở rộng thành chương trình Data engineering** (không thêm pipeline orchestration, data
governance chi tiết…) trừ khi có lý do cụ thể. Còn 2 khung: `er-modeling`, `data-quality` — viết xong
là hết luôn 5/6 chỗ vi phạm §A3.

## B3. Còn lại 102 khung — đã quyết gì cho từng nhóm

**05. Machine learning** (28 khung) — cây đã khớp sẵn, chỉ vá nhỏ: Data leakage và Distribution shift
làm mục thêm vào `overfitting-regularization` hoặc `train-val-test-cv`, không tách bài.

**06. Deep learning** (14 khung) — nhóm *Generative models* ba bài, cả ba đều **cố ý viết ngắn**:
`autoencoder` là cầu nối lịch sử dẫn tới VAE, không phải trọng tâm; `vae` ngắn nhưng đủ ý vì nó bắc
cầu sang Diffusion ở kệ LLM, cần rõ **vì sao Diffusion thắng thế**; `gan` rất ngắn — chỉ cần nhận ra
tên và biết vì sao nay ít dùng hơn Diffusion, **không đào sâu training GAN** (mode collapse,
discriminator loss…). GPU basics / FLOPs / distributed training **không tạo mới**, chủ duy nhất là
`10-mlops/gpu-inference`, chỉ link chéo.

> **Còn mở, chưa quyết:** `optimizer-sgd-adam` đang là một khung gộp cả SGD/Momentum/AdaGrad/RMSProp/
> Adam/AdamW. Theo B1#2, Adam và SGD chắc đáng bài riêng (hay bị hỏi tách bạch "vì sao Adam mà không
> SGD"), AdaGrad/RMSProp có thể chỉ cần làm mục trong bài Adam như đường dẫn lịch sử. Quyết khi thật
> sự ngồi viết, không chốt trước ở đây.

**07. Transformer** (14 khung) — thêm `efficient-attention` (FlashAttention, sparse, linear attention):
hay bị hỏi ở vòng phỏng vấn sâu.

**08. LLM** (27 khung) — thêm `rag-evaluation`, tách khỏi các bài kỹ thuật RAG vì "đo RAG bằng gì" là
câu hỏi riêng (Recall@K, Precision@K, MRR, NDCG, faithfulness, context/answer relevance). Nhóm mới
*Multimodal*: CLIP, VLM, Diffusion, Audio — **mỗi khái niệm một bài ngắn trước**, chưa tách nhóm con
đào sâu (chưa chẻ Diffusion thành overview + DDPM + score-based + latent). Phình sau nếu thực tế đòi.

**09. ML system design** (4 khung) — đã khớp sẵn. "Production design" (scalability, fault tolerance,
rate limiting, observability, security, cost) **không làm bài riêng** — để làm checklist lặp trong
mỗi case study, tránh trùng với Distributed systems bên CS fundamentals.

**10. MLOps** (13 khung) — ba nhóm mới: *Serving engines* (vLLM, SGLang, TensorRT-LLM và so sánh —
hay bị hỏi thẳng tên), *AI reliability* (hallucination, guardrails, fallback, human-in-the-loop),
*AI security* (prompt injection, data poisoning, model extraction, jailbreak, access control). Hai
nhóm sau trước đây thiếu hẳn.

## B4. Làm gì trước

Theo thứ tự nên làm:

1. **`er-modeling` + `data-quality`** — xong Database luôn, và tự hết 5/6 chỗ vi phạm §A3.
2. **Sửa `#E06C7A`** ở `thread-process-gil` — một chỗ, sửa trong một phút (§A4).
3. **Rà 36 đầu mục đếm số** (§A6) — cần đọc từng chỗ để phân biệt số bản chất với số đếm thẻ.
4. **MLOps**: Serving engines, AI reliability, AI security — ba nhóm mới, hiện là chỗ trống lớn nhất.
5. **LLM**: nhóm Multimodal.

## B5. Đã hoãn

**Metadata overlay** (`priority` / `depth` / `recognition` / `interview_frequency` / `learning_modes`):
chưa có hạ tầng đọc và hiển thị trong `build.py` hay giao diện, gắn nửa vời trên gần 500 mục sẽ thành
nợ. Nếu sau muốn thử: bắt đầu bằng **đúng một field** (`recognition`) trên **một kệ**, xem có đáng giữ
rồi mới mở rộng.
