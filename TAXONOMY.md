# TAXONOMY — luật viết bài & bản đồ bài

Tài liệu nội bộ. **Phần A** — sửa bài thì đọc. **Phần B** — thêm/bớt/tách bài thì đọc.
Số liệu ghi 2026-09-02, đừng tin — chạy lệnh §A1 lấy số thật.

---

# PHẦN A — SẠCH NGHĨA LÀ GÌ

## A1. Hai lệnh phải chạy

| Lệnh | Bắt gì | Sạch là |
|---|---|---|
| `python3 tools/build.py` | **cấu trúc** — bài chưa khai trong `category.json`, khai trỏ vào thư mục không có, thiếu `index.html`, `data-base` sai số cấp `../` | không cảnh báo |
| `python3 tools/soat.py` | **nội dung** — 5 luật §A2 | mọi mục `tổng: 0` |

`build.py` in số bài / nhóm / mục tìm kiếm — **nguồn số đáng tin duy nhất**.
`soat.py` in đường dẫn từng chỗ sai, thoát mã ≠0 nếu còn nợ.

Rồi soát mắt 5 chỗ: trang chủ · `dict-hash-table` (SVG) · `binary-search` (lab) · `kit.html` · màn hình ~490px.

## A2. Năm luật máy kiểm được — đang nợ 49 chỗ

| # | Luật | Vì sao | Sai | Ở đâu |
|---|---|---|---:|---|
| A3 | Không link vào bài còn là khung | bấm vào ra trang rỗng | **6** | tự hết khi viết `er-modeling` (3), `data-quality` (2), `vector-database` (1) |
| A4 | Chỉ dùng màu có trong `style.css` | lệch bảng màu | **2** | `thread-process-gil` dùng `#E06C7A` → sửa `#F2718A` |
| A5 | Clay `#E0855C` không vào hình | nó là màu thương hiệu, không mang nghĩa nội dung | **0** | ✅ sạch |
| A6 | Đầu mục không đếm số | thêm bớt một thẻ là số sai, không ai nhớ sửa | **36** | phải đọc từng chỗ — xem ngoại lệ dưới |
| A7 | Dòng `<pre>` dưới ~92 ký tự | dài hơn thì điện thoại bị đẩy ngang | **5** | dài nhất `db-normalization` (101) |

**A3 chi tiết** — muốn nhắc khái niệm mà bài chủ chưa viết: **nói tên trong văn xuôi, đừng đặt link**.

**A4 chi tiết** — tốt nhất viết `var(--…)`; SVG buộc ghi hex thì chép đúng mã, đừng pha mã gần giống.
Bốn màu ngữ nghĩa, nghĩa cố định trong mọi hình:

| Mã | Biến | Nghĩa |
|---|---|---|
| `#8CA9F2` | `--filled` | dữ liệu, thứ đang xét |
| `#EDB44A` | `--probe` | con trỏ, điểm nhấn, đáp án |
| `#F2718A` | `--tomb` | sai, bị loại, chưa thoả |
| `#5BCFA0` | `--ok` | đúng, kết quả, đã thoả |

**A6 chi tiết** — số thuộc bản chất chủ đề thì **giữ**, số đếm thẻ mình vừa viết thì **bỏ**:

| | Ví dụ |
|---|---|
| ✅ **Giữ** | `Bốn ô — mọi metric đều từ đây` · `Bốn loại join` · `Bốn mức cô lập` |
| ❌ **Bỏ** | `Sáu cách regularize` → `Cách regularize` · `Ba mẫu code cần thuộc` → `Mẫu code cần thuộc` · `Bốn bài của nhóm` → `Học theo thứ tự nào` |

Vì thế `soat.py` chỉ **liệt kê** chứ không kết luận sai. Phần lớn 36 chỗ thuộc loại ❌, dồn ở
[04-database](content/04-database/) (9) và [05-machine-learning](content/05-machine-learning/) (8).

## A3. Ba luật máy không kiểm được — tự đọc

**① Một khái niệm, một bài chủ.** Kệ khác nhắc tới thì viết **một mục 3–4 câu**, đúng bốn nhịp:

| Nhịp | Nội dung |
|---|---|
| 1 | **Vấn đề** — vì sao khái niệm tồn tại |
| 2 | **Định nghĩa + gọi thẳng tên** các nhánh chính — bắt buộc, vì `search-index.js` tìm theo chữ trong mục |
| 3 | **Một câu đánh đổi** — cái giá, không phải ưu điểm |
| 4 | **Link** tới bài chủ |

> Mẫu đúng: mục *Sharding & partitioning* trong `cap-theorem-consistency` — gọi tên range / hash /
> consistent hashing, nói cái giá khi rebalance, link sang `04-database/sharding-replication`,
> không giảng lại cách chọn shard key.

Ba chỗ dễ chồng chéo, viết tới thì rà trước:

| Khái niệm | Chủ duy nhất |
|---|---|
| Sharding / partitioning | `04-database/sharding-replication` |
| GPU & training systems | `10-mlops/gpu-inference` — không lặp ở Deep learning |
| Distributed systems | chồng được cả CS fundamentals · Database · MLSD |

**② Mỗi mục một hình.** Cần hai hình = dấu hiệu mục nên tách đôi. Hình phải **thay được** đoạn văn,
không minh hoạ thêm. Chữ trong hình càng ít càng tốt. Đang vượt đúng một chỗ: `decision-tree#dtree-s2` (3 hình).

**③ Overview giữ tầng overview** — cấp nhóm cũng vậy. Mục overview đang vẽ lại cơ chế mà bài con đã
vẽ → cắt còn 1–2 câu + link. Chọn khuôn theo bản chất nhóm:

| Nhóm là… | Khuôn |
|---|---|
| các biến thể cạnh tranh nhau (bagging vs boosting) | kể chuyện nhân quả — [tree-family-overview](content/05-machine-learning/06-tree-models/tree-family-overview/index.html) |
| các công cụ song song (array, hash map, heap) | ngắn 2–3 mục — [data-structures-overview](content/01-dsa/03-data-structures/data-structures-overview/index.html) |

## A4. Hai luật cũ đã chết

| Luật | Trạng thái |
|---|---|
| `details.deep` | **bỏ, đã dọn sạch cả kho.** `details.qa` (*Hỏi đáp*, 79 bài) thay hẳn. **Không thêm vào bài mới.** Hai lớp còn dùng thật: `.key` (75 bài), `.why` (60 bài) |
| `id="<slug>-sN"` | **nới.** `app.js` đọc thẳng `<section>`, không dựa vào tiền tố. Miễn liên tục từ `s1` và khớp số `<b>NN</b>` |

---

# PHẦN B — BÀI NÀO NÊN TỒN TẠI

## B1. Ba quyết định gốc

**① Cấp 2 của cây taxonomy → tên nhóm** (`groups` trong `category.json`). Không tạo kệ mới, không
dựng taxonomy song song — cây `content/` là nguồn sự thật duy nhất.

**② Bài hay mục — quyết theo mức được nhận diện, không theo tầng trong cây.**

> Cái tên này có được gọi rộng rãi (paper, phỏng vấn, codebase đều gọi đúng tên này) và có đáng
> quay lại ôn riêng không?
> **Có → 1 bài**, dù nằm tầng nào. **Không → 1 mục** trong bài cha.

Hai lá cùng cấp vẫn ra hai kết quả khác nhau: dưới *Retrieval*, `Top-k` và `Similarity score` chỉ
đáng làm mục, còn `Recall@K` và `MRR` đủ nổi để lên bài riêng.

**③ `01-dsa` giữ nguyên, không áp cây taxonomy CS vào.** Khuôn DSA xếp theo *dạng đề bài xuất hiện*
(55 pattern · 198 bài LeetCode / 222 lượt link), phục vụ phản xạ nhận đề. *Two pointers* và
*Sliding window* không thuộc "Searching" trong taxonomy CS nhưng là hai pattern trung tâm khi luyện
đề. Cây taxonomy CS chỉ dùng để **kiểm chéo** đã đủ pattern chưa.

## B2. Tiến độ — 94/196 bài

| Kệ | Đã viết | Khung | Đã quyết gì |
|---|---:|---:|---|
| 01 · DSA | 23 | — | ✅ xong trọn |
| 02 · Python | 14 | — | ✅ `oop-python` + `typing-dataclass` là hai lỗ thật, đã viết · `performance-profiling` tách riêng khỏi `leetcode-toolkit` · Testing/Logging/Packaging **cố ý bỏ**, để bên MLOps |
| 03 · CS fundamentals | 14 | — | ✅ thêm `cap-theorem-consistency`, `consensus-leader-election`, `messaging-queue-pubsub` · Concurrency giữ một bài `lock-deadlock-race` |
| 04 · Database | 21 | 2 | nhóm mới *Data systems* chặn ở đúng 6 khái niệm · còn `er-modeling`, `data-quality` |
| 05 · Machine learning | 10 | 28 | cây đã khớp sẵn · Data leakage + Distribution shift làm mục thêm, không tách bài |
| 06 · Deep learning | 4 | 14 | *Generative models* ba bài **cố ý ngắn** · GPU/FLOPs/distributed **không tạo mới** |
| 07 · Transformer | 2 | 14 | thêm `efficient-attention` — hay bị hỏi ở vòng sâu |
| 08 · LLM | 4 | 27 | thêm `rag-evaluation` · nhóm mới *Multimodal* |
| 09 · ML system design | 1 | 4 | đã khớp sẵn · "Production design" **không làm bài riêng** |
| 10 · MLOps | 1 | 13 | ba nhóm mới: *Serving engines* · *AI reliability* · *AI security* |

**Gộp làm mục, không tách bài** — ghi lại để khỏi ai tách ra lại:

| Kệ | Gộp vào bài |
|---|---|
| Python | Scope/Modules/Exceptions → `language-core-overview` · `collections` → `list-tuple-set` + `dict-hash-table` · Closure → `decorator-context-manager` · Lambda + higher-order function |
| CS | File systems + IPC → `os-overview` · HTTP/2 + HTTP/3 + WebSocket → `tcp-http` · RPC + gRPC → `rest-api-design` · Sharding → mục ngắn trong `cap-theorem-consistency` |

> **Ghi chú quan hệ, không phải cấu trúc trang:** Messaging hiển thị ngang hàng với Distributed
> systems cho dễ điều hướng, nhưng về mental model nó là *một phần của* Distributed systems.
> Không sửa giao diện — chỉ cần `messaging-queue-pubsub` mở đầu bằng bối cảnh phân tán và link
> ngược về `cap-theorem-consistency`.

## B3. Ba chỗ cố ý viết ngắn / cố ý không mở rộng

| Chỗ | Chặn ở đâu |
|---|---|
| **Data systems** (Database) | đúng 6 khái niệm: OLTP vs OLAP · Data warehouse · Data lake · ETL/ELT · Batch vs stream · Data quality. **Không phình thành chương trình Data engineering** |
| **Generative models** (DL) | `autoencoder` là cầu nối lịch sử dẫn tới VAE · `vae` ngắn nhưng đủ để bắc cầu sang Diffusion, cần rõ **vì sao Diffusion thắng thế** · `gan` rất ngắn, chỉ cần nhận ra tên, **không đào sâu training GAN** |
| **Multimodal** (LLM) | CLIP · VLM · Diffusion · Audio — **mỗi khái niệm một bài ngắn trước**, chưa chẻ Diffusion thành overview + DDPM + score-based + latent |

> **Còn mở, chưa quyết:** `optimizer-sgd-adam` đang gộp SGD/Momentum/AdaGrad/RMSProp/Adam/AdamW.
> Theo B1②, Adam và SGD chắc đáng bài riêng (hay bị hỏi "vì sao Adam mà không SGD"); AdaGrad/RMSProp
> có thể chỉ cần làm mục trong bài Adam. Quyết khi thật sự ngồi viết.

## B4. Làm gì trước

| | Việc | Được gì |
|---|---|---|
| 1 | `er-modeling` + `data-quality` | xong Database, tự hết 5/6 chỗ vi phạm A3 |
| 2 | Sửa `#E06C7A` ở `thread-process-gil` | một phút, hết A4 |
| 3 | Rà 36 đầu mục đếm số | hết A6 — phải đọc từng chỗ |
| 4 | MLOps: Serving engines · AI reliability · AI security | chỗ trống lớn nhất |
| 5 | LLM: nhóm Multimodal | |

## B5. Đã hoãn

**Metadata overlay** (`priority` / `depth` / `recognition` / `interview_frequency` / `learning_modes`)
— chưa có hạ tầng đọc và hiển thị trong `build.py` hay giao diện; gắn nửa vời trên gần 500 mục sẽ
thành nợ. Muốn thử: **đúng một field** (`recognition`) trên **một kệ**, xem có đáng giữ rồi mới mở rộng.
