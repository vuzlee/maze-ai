# Taxonomy — kế hoạch mở rộng nội dung

Tài liệu nội bộ, không phải nội dung học. Ghi lại quyết định gấp cây taxonomy (bản người dùng
chốt ngày viết tài liệu này) vào cấu trúc kệ → nhóm → bài đang có, để lần sau rà nội dung thì
có sẵn baseline chứ không phải nhớ lại từ đầu.

> **Trạng thái:** mọi mục 🆕 trong tài liệu này **đã có khung** (`data-skeleton="1"`, 25 bài,
> 13 nhóm mới trong `category.json`) — dàn ý mục đã viết đúng theo quyết định ở đây, kể cả mục
> ngắn "một khái niệm, một chủ" (xem `cap-theorem-consistency` mục 05). Còn thiếu **nội dung thật**
> trong từng mục — 🆕 trong bảng dưới nay đọc là "khung đã tạo, chưa viết", không phải "chưa tồn
> tại". Ô "Mở, chưa quyết" (ví dụ `optimizer-sgd-adam`) vẫn còn mở, không tự chốt theo việc tạo
> khung này — đó là quyết định nội dung, không phải quyết định cấu trúc.

## Ba quyết định gốc

1. **Cấp 2 của cây taxonomy → tên nhóm** (`category.json` groups). Không tạo kệ mới, không tạo
   taxonomy song song với cây `content/` — cây `content/` vẫn là nguồn sự thật duy nhất.
2. **Bài hay mục — quyết theo recognition + ROI + giá trị mental model, không theo tầng trong cây.**
   Tầng của cây chỉ mô tả quan hệ kiến thức (cái nào là con của cái nào), **không** quyết định ranh
   giới trang. Một node ở cấp 2 có thể chỉ đáng 1 mục; một lá ở cấp 3-4 vẫn có thể đáng 1 bài riêng,
   nếu nó được nhận diện rộng (paper/interview/codebase quốc tế hay gọi đúng tên này) và đáng quay
   lại ôn riêng — bỏ hẳn quy tắc cũ "cấp 2 mặc định là bài, cấp dưới mặc định là mục".

   - **Test:** node này có được nhận diện rộng + đáng ôn riêng không? Có → 1 bài, dù nằm ở tầng nào.
     Không, chỉ có nghĩa trong ngữ cảnh node cha → 1 mục trong bài của node cha, không tách trang.
   - **Ví dụ tách theo lá:** `Optimization → SGD, Momentum, AdaGrad, RMSProp, Adam, AdamW` — dù cùng
     nằm ở lá dưới một node, mỗi cái xứng 1 bài riêng vì recognition cao (tên gọi cụ thể, hay bị hỏi
     riêng lẻ, không ai hỏi chung "Optimization là gì").
   - **Ví dụ giữ nguyên mục:** `Retrieval → Top-k, Similarity score` — chỉ có nghĩa khi đọc trong
     ngữ cảnh Retrieval, không đáng đứng riêng. Nhưng `Recall@K`, `MRR` dưới cùng node Retrieval lại
     đủ recognition để lên bài riêng (nhóm RAG Evaluation) — hai lá cùng cấp, hai quyết định khác
     nhau, đúng như rule nói: tầng không quyết định.
   - Cấp 2 vẫn dùng để đặt tên **nhóm** (`category.json`) như quyết định #1 — đó là chuyện nhóm chứa
     bài nào, tách biệt hoàn toàn với chuyện bài nào được viết ra ở quyết định #2 này.
3. **01-dsa giữ nguyên** — không áp taxonomy CS (loại cấu trúc dữ liệu) vào đây. Khuôn DSA hiện
   tại xếp theo *dạng đề bài xuất hiện* (46 pattern · 151 LeetCode có link), phục vụ phản xạ nhận
   diện đề, khác mục đích với taxonomy giáo trình. Ví dụ: "Two pointers" và "Sliding window" không
   thuộc về "Searching" trong taxonomy CS, nhưng lại là hai pattern trung tâm khi luyện đề — xếp
   theo taxonomy sẽ làm mất tác dụng luyện phản xạ. Metadata (`priority/depth/recognition/…`) —
   hoãn, chưa có hạ tầng hiển thị và sẽ tạo nợ nội dung nếu gắn nửa vời trên 490 mục.

## Chú giải bảng dưới

| Dấu | Nghĩa |
|---|---|
| 🟢 | bài đã có — giữ nguyên, gắn nhãn cho khớp nhóm mới nếu cần |
| 🆕 | bài mới nên tạo — chưa có gì tương ứng trong kho |
| ▪ | không tách trang — gộp làm 1 mục trong bài đã ghi kèm |
| ⚠️ | trùng khái niệm với chỗ khác trong kho — không tạo mới, chỉ link chéo |

Thứ tự nhóm dưới đây tạm theo cây gốc, **không phải thứ tự hiển thị cuối cùng** — thứ tự hiển thị
vẫn quyết ở `books`/`groups` trong `category.json` khi thực làm, theo đúng nguyên tắc CLAUDE.md
(overview trước, cơ bản trước nâng cao).

---

## 01. DSA — data structures & algorithms

**Giữ nguyên cấu trúc hiện tại (pattern-first).** Không áp cây taxonomy CS. Nếu muốn dùng cây đó,
chỉ dùng để **kiểm chéo** đã đủ pattern hay chưa, không dùng để tổ chức lại trang.

---

## 02. Python

| Nhóm (cấp 2) | Lá trong cây | Quyết định |
|---|---|---|
| Core Language | Variables & Objects, Mutable/Immutable | 🟢 `memory-model-mutability` |
| | Scope, Functions cơ bản, Modules/Packages, Exceptions | ▪ mục trong `language-core-overview` |
| Built-in Data Structures | List, Tuple, Set | 🟢 `list-tuple-set` |
| | Dict | 🟢 `dict-hash-table` |
| | `collections` (Counter, deque, defaultdict, namedtuple) | ▪ mục thêm vào `list-tuple-set` (deque) và `dict-hash-table` (Counter/defaultdict) |
| Functions | Lambda, Higher-Order Functions | ▪ mục nhỏ — không đủ sâu 1 bài |
| | Closure | ▪ mục trong `decorator-context-manager` |
| | Decorator | 🟢 `decorator-context-manager` |
| Iteration | Iterable/Iterator, Generator, Generator expression | 🟢 `iterator-generator` |
| **OOP** | Class/Object, Inheritance, Composition, Polymorphism, MRO | 🆕 **`oop-python`** — lỗ thật, chưa có bài nào về OOP trong kho |
| **Typing** | Type Hints, Generic, Protocol, Dataclass | 🆕 **`typing-dataclass`** — lỗ thật, recognition cao (mọi codebase Python hiện đại đều dùng type hints) |
| Performance | Profiling, Memory Optimization, NumPy Vectorization | 🆕 bài ngắn, hoặc gộp mục vào `leetcode-toolkit` |
| Async & Concurrency | Threading, Multiprocessing, GIL | 🟢 `thread-process-gil` |
| | AsyncIO, Coroutine, Event Loop, await | 🟢 `asyncio` |
| Engineering | Testing, Logging, Packaging, Dependency Management | ⚠️ trùng `10-mlops` (Git, Testing, Code Quality) → **bỏ khỏi Python**, để nguyên bên MLOps |

**Ưu tiên làm trước:** `oop-python`, `typing-dataclass` — hai lỗ có recognition cao nhất trong kệ này.

---

## 03. CS fundamentals

| Nhóm (cấp 2) | Lá trong cây | Quyết định |
|---|---|---|
| Operating Systems | Process, Thread, Scheduling, Context Switching | 🟢 `process-thread-scheduling` |
| | Memory Management, Virtual Memory, Paging | 🟢 `memory-virtual-paging` |
| | File Systems, IPC | ▪ mục thêm vào `os-overview` (priority thấp, awareness-level) |
| Concurrency | Race Condition, Deadlock, Starvation, Mutex, Semaphore, Condition Variable | 🟢 `lock-deadlock-race` — giữ 1 bài, **không tách nhóm riêng** khỏi OS |
| Networking | TCP/IP, TCP, UDP, HTTP | 🟢 `tcp-http` |
| | HTTP/2, HTTP/3 (QUIC) | ▪ mục trong `tcp-http` (nâng thành bài riêng sau nếu cần đào sâu) |
| | DNS, TLS | 🟢 `dns-tls` |
| | WebSocket | ▪ mục trong `tcp-http` |
| APIs & Communication | REST, API Design | 🟢 `rest-api-design` |
| | RPC, gRPC | ▪ mục trong `rest-api-design` (nâng 🆕 sau nếu recognition đủ cao) |
| **Distributed Systems** | CAP, Consistency, Replication | 🆕 **`cap-theorem-consistency`** |
| | Sharding, Partitioning | ▪ **mục trong `cap-theorem-consistency`**, viết theo công thức 4 nhịp ở CLAUDE.md § *Một khái niệm, một chủ*: (1) vấn đề — 1 node không chịu được tải/dữ liệu vượt quy mô; (2) định nghĩa + gọi tên 3 chiến lược — range, hash, consistent hashing; (3) đánh đổi — thêm/bớt node thì rebalance tốn gì, hotspot lệch khi chọn sai key; (4) link sang bài chủ. Bài chủ vẫn là `04-database/sharding-replication` — mục này không giảng lại cách chọn shard key hay replication topology, những cái đó ở bên bài chủ. |
| | Consensus, Leader Election | 🆕 bài bridge — **giữ, không bỏ dù ưu tiên thấp hơn.** Đúng kiểu topic recognition cao (Raft/ZooKeeper hay bị gọi tên) nhưng không cần deep dive — viết brief là đủ, xếp làm sau trong danh sách ưu tiên |
| | Scalability, Availability, Reliability, Fault Tolerance | ▪ phần lớn là khái niệm nền, gộp làm mục trong bài CAP hoặc trong `09-ml-system-design` (đã có "Requirements" tương ứng) |
| Caching | Cache, Cache Invalidation, TTL, LRU, Distributed Cache | 🟢 `caching` — đã đủ |
| **Messaging** | Queue, Pub/Sub, Idempotency, Delivery Semantics, Event Streaming | 🆕 **`messaging-queue-pubsub`** — lỗ thật, recognition cao (Kafka, SQS thường gặp trong system design) |

> **Ghi chú quan hệ, không phải cấu trúc trang:** Messaging hiển thị như một nhóm ngang hàng với
> Distributed Systems trong `category.json` (tốt cho điều hướng — người học không cần biết nó là
> "con" của cái gì mới bấm vào được), nhưng về mental model, Messaging **là một phần của**
> Distributed Systems (cùng nhóm Consistency, Replication, Partitioning, Fault Tolerance). Không
> cần sửa UI cho khớp quan hệ này — chỉ ghi lại đây để bài `messaging-queue-pubsub` biết nó nên mở
> đầu bằng việc thừa nhận bối cảnh phân tán, và link ngược về `cap-theorem-consistency` nếu có nhắc
> tới CAP/consistency khi giải thích delivery semantics.

**Ưu tiên làm trước:** `messaging-queue-pubsub`, `cap-theorem-consistency`.

---

## 04. Database & SQL

Đã khớp sẵn hầu hết (15 bài hiện có phủ SQL, Relational, Indexing, Transactions, NoSQL). Chỉ thêm:

| Nhóm (cấp 2) | Lá trong cây | Quyết định |
|---|---|---|
| **Data Systems** | OLTP vs OLAP, Data Warehouse, Data Lake, ETL/ELT, Batch vs Stream, Data Quality | 🆕 **nhóm mới, đúng 6 khái niệm này — chặn ở đây.** Đủ để AI Engineer đọc hiểu hệ thống dữ liệu mình dùng, không mở rộng thành chương trình Data Engineering (không thêm data pipeline orchestration, data governance chi tiết, v.v. trừ khi có lý do recognition cụ thể) |

---

## 05. Machine learning

Đã khớp sẵn hầu hết. Chỉ vá nhỏ:

| Nhóm (cấp 2) | Lá trong cây | Quyết định |
|---|---|---|
| Learning Theory | Data Leakage, Distribution Shift | ▪ mục thêm vào `overfitting-regularization` hoặc `train-val-test-cv` |

---

## 06. Deep learning

| Nhóm (cấp 2) | Lá trong cây | Quyết định |
|---|---|---|
| **Generative Models** | Autoencoder | 🆕 bài ngắn — cầu nối lịch sử (dẫn tới VAE), không phải trọng tâm AI Engineer hiện nay |
| | VAE | 🆕 bài ngắn nhưng đủ ý — bridge sang Diffusion ở `08-llm` Multimodal, cần rõ vì sao Diffusion thắng thế |
| | GAN | 🆕 bài rất ngắn — chỉ cần nhận diện tên và vì sao ít dùng hơn Diffusion hiện nay, **không đào sâu training GAN** (mode collapse, discriminator loss…) |
| Training Systems | GPU Basics, GPU Memory, FLOPs, Distributed Training Basics | ⚠️ trùng `10-mlops` (`gpu-inference`) → **không tạo mới**, chỉ link chéo |

> **Mở, chưa quyết — ví dụ áp rule mới:** `optimizer-sgd-adam` hiện là 1 bài skeleton gộp cả
> Gradient Descent/SGD/Momentum/AdaGrad/RMSProp/Adam/AdamW. Theo rule #2, mỗi optimizer là một lá
> cùng tầng nhưng recognition khác nhau rõ — Adam/SGD chắc đáng bài riêng (tên gọi cụ thể, hay bị
> hỏi tách bạch "vì sao dùng Adam mà không SGD"), AdaGrad/RMSProp có thể chỉ cần mục trong bài Adam
> (đường dẫn lịch sử tới Adam, ít khi bị hỏi riêng). Không quyết ở đây — để mở, rà lại khi thật sự
> viết bài này.

---

## 07. Transformer & architectures

Đã khớp sẵn hầu hết. Thêm:

| Nhóm (cấp 2) | Lá trong cây | Quyết định |
|---|---|---|
| **Efficient Architectures** | FlashAttention, Sparse Attention, Linear Attention | 🆕 bài mới — recognition cao, hay bị hỏi ở vòng sâu |

---

## 08. LLM & Generative AI

Đã khớp sẵn hầu hết. Thêm:

| Nhóm (cấp 2) | Lá trong cây | Quyết định |
|---|---|---|
| **RAG Evaluation** | Recall@K, Precision@K, MRR, NDCG, Faithfulness, Context/Answer Relevance | 🆕 bài mới — tách khỏi kỹ thuật RAG, vì đây là câu hỏi riêng ("đo RAG bằng gì") |
| **Multimodal** | CLIP, VLM, Diffusion Models, Audio Models, Multimodal Agents | 🆕 nhóm mới, ROI cao theo xu hướng hiện tại — nhưng **mỗi khái niệm 1 bài ngắn trước**, chưa mở nhóm con đào sâu riêng từng nhánh (ví dụ chưa tách "Diffusion" thành overview + DDPM + score-based + latent diffusion). Phình sau, nếu recognition thực tế đòi hỏi. |

---

## 09. ML system design

Đã khớp sẵn (framework + 3 case study hiện có tương ứng đúng Recommendation/Search/LLM systems
trong cây). "Production Design" (Scalability, Fault Tolerance, Rate Limiting, Observability,
Security, Cost…) **không nên là bài riêng** — để làm checklist lặp trong mỗi case study, tránh
trùng với Distributed Systems ở CS fundamentals.

---

## 10. MLOps & AI engineering

Đã khớp sẵn phần lớn (Git, Docker, Linux, serving API, experiment tracking, CI/CD, GPU). Thêm:

| Nhóm (cấp 2) | Lá trong cây | Quyết định |
|---|---|---|
| **Serving Engines** | vLLM, SGLang, TensorRT-LLM, so sánh giữa chúng | 🆕 bài mới — recognition rất cao hiện nay, thường bị hỏi thẳng tên |
| **AI Reliability** | Hallucination, Guardrails, Fallback, Human-in-the-loop, Regression Testing | 🆕 **nhóm mới hoàn toàn** — thiếu hẳn |
| **AI Security** | Prompt Injection, Data Poisoning, Model Extraction, Jailbreaks, Access Control | 🆕 **nhóm mới hoàn toàn** — thiếu hẳn, ROI rất cao (hot topic, ít nơi dạy có hệ thống) |

---

## Tổng hợp: làm gì trước

**Lỗ có recognition + ROI cao nhất (nên làm trước):**
1. `oop-python`, `typing-dataclass` — 02-python
2. `messaging-queue-pubsub` — 03-cs-fundamentals
3. Serving Engines (vLLM/SGLang/TensorRT-LLM), AI Reliability, AI Security — 10-mlops
4. Multimodal — 08-llm

**Rủi ro trùng cần canh khi thực làm** (nguyên tắc: mỗi khái niệm một chủ, xem *CLAUDE.md § Một
khái niệm, một chủ*):
- Sharding/Partitioning: **chủ duy nhất là `04-database/sharding-replication`.** Mục trong
  `cap-theorem-consistency` chỉ nói khái quát 3–4 câu rồi link sang, không viết lại chi tiết.
- GPU/Training systems cơ bản: chủ duy nhất là `10-mlops/gpu-inference`, không lặp ở Deep learning.
- Distributed Systems tổng quát ⚠️ nguy cơ chồng cả ba nơi (CS fundamentals, Database, ML system
  design) — khi viết thật cần rà lại link chéo giữa ba kệ này trước, không viết riêng độc lập.

**Hoãn:** metadata overlay (`priority/depth/recognition/interview_frequency/learning_modes`) —
chưa có hạ tầng đọc/hiển thị trong `build.py` hay UI. Nếu sau này muốn thử, bắt đầu bằng đúng một
field (`recognition`) trên một kệ, xem có đáng giữ không rồi mới mở rộng.
