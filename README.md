# MazeAI

Kiến thức nền cho kỹ sư data, machine learning và AI, viết bằng tiếng Việt.

**→ [maze-ai-lemon.vercel.app](https://maze-ai-lemon.vercel.app/)**

**44 bài đã viết · 127 khung bài đã chốt dàn ý · 10 kệ · 490 mục tra cứu · 151 bài LeetCode có link.**

Mười kệ xếp theo thứ tự học được, từ cấu trúc dữ liệu và SQL tới Transformer, LLM và MLOps.
Mỗi bài đi từ **vấn đề nó sinh ra để giải**, qua **cơ chế bên dưới**, tới chỗ nó gãy — kèm code
chạy được, sơ đồ, lab bấm được và phần hỏi đáp.

## Mở lên đọc

Bản online ở **[maze-ai-lemon.vercel.app](https://maze-ai-lemon.vercel.app/)** — không cần cài gì,
mở là đọc.

Muốn đọc offline hoặc muốn sửa thì clone về. Site là HTML tĩnh thuần, không build step, không
server, không dependency:

```bash
git clone git@github.com:vuzlee/maze-ai.git && cd maze-ai
xdg-open index.html      # macOS: open index.html
```

Mở thẳng file bằng trình duyệt là chạy — y hệt bản online, trừ mỗi phần chia sẻ link.

Tiến độ học lưu ngay trong trình duyệt của bạn (`localStorage`) — không có tài khoản, không có gì
gửi đi đâu cả.

> Xoá dữ liệu duyệt web của trang này thì mất hết đánh dấu *đã học*.
> Đổi máy, đổi trình duyệt, hay đổi giữa bản online và bản offline đều không mang theo được.

## Trong kho có gì

| # | Kệ | Đã viết | Khung | Nội dung |
|---|---|---|---|---|
| 01 | DSA — data structures & algorithms | 11 | 12 | Big-O · array/string, linked list, hash map, stack, heap, tree/BST, trie, union-find · sorting, two pointers, sliding window, binary search, greedy, interval, graph, shortest path, dynamic programming |
| 02 | Python | 6 | 5 | Language core & data model · built-in types · thread/GIL & asyncio · LeetCode toolkit |
| 03 | CS fundamentals | 2 | 9 | Operating system (process, virtual memory, lock) · networking (DNS/TLS, TCP/HTTP, caching, REST, load balancing) |
| 04 | Database & SQL | 3 | 15 | Relational model, constraints, normalization, schema design · SQL basics · index, transaction, query tuning · NoSQL, sharding |
| 05 | Machine learning | 10 | 28 | Math foundations · bias–variance, cross-validation · linear/logistic, Ridge–Lasso, SVM, KNN, Naive Bayes · decision tree → random forest → gradient boosting → XGBoost → LightGBM · k-means, DBSCAN, HDBSCAN · PCA · evaluation & calibration · statistics, A/B testing |
| 06 | Deep learning | 4 | 11 | Perceptron & MLP, activation, backpropagation, initialization, normalization, optimizer, dropout · convolution & CNN · RNN, LSTM & GRU · training recipe & debugging |
| 07 | Transformer & architectures | 2 | 13 | Tokenization, embedding, positional encoding, self-attention, Transformer block · BERT, GPT, T5 · SSM, Mamba, Hymba |
| 08 | LLM & GenAI | 4 | 22 | Pretraining & scaling law · SFT, alignment, PEFT · MoE, long context, chain-of-thought · decoding, quantization, serving · RAG · agents · model labs: LLaMA, Qwen, DeepSeek, Mixtral, model đóng |
| 09 | ML system design | 1 | 4 | Framework · recommendation system, search & ranking, LLM/RAG system |
| 10 | MLOps & engineering | 1 | 8 | Git, Docker, Linux, serving API · experiment tracking, CI/CD, model serving · GPU & inference |

Kho vẫn đang mở rộng — các mảng còn thiếu bài liệt kê ở cuối
[CLAUDE.md](CLAUDE.md#chỗ-trống-theo-syllabus).

## Học thế nào

**Trang thư viện** là mục lục: mỗi kệ một chương, mỗi bài một hàng có tóm tắt một dòng và số
mục bên phải. Thanh kệ dính ở trên cho nhảy thẳng tới chương cần, mỗi chương có tiến độ riêng.

**Trang bài** bố trí để học chứ không chỉ để đọc:

- **dòng ngắn ~70 ký tự** cho phần chữ, còn code / bảng / sơ đồ / lab vẫn để rộng;
- **mỗi mục là một khối** có số thứ tự và đường kẻ ngăn, lướt là thấy ranh giới;
- **thanh tiến độ đọc** ở đỉnh trang, mục lục đếm `06 / 15` và tô xanh những mục đã đi qua;
- **lab bấm được** — chỉnh tham số, chạy từng bước, xem code sáng đúng dòng đang chạy;
- **hỏi đáp gập lại** — có nút mở/đóng cả mục để tự kiểm tra trước khi xem đáp án;
- **đánh dấu đã học** ở cuối mỗi bài, trang chủ hiện tổng tiến độ và có nút lọc *chỉ bài chưa học*.

### Tìm

Gõ `/` ở bất kỳ đâu là nhảy vào ô tìm kiếm. Nó tìm trong **toàn bộ 464 mục của cả kho**, không
chỉ tên bài — gõ `tombstone`, `KV cache`, `probe sequence` là ra thẳng mục chứa nó, kèm đoạn
trích có tô vàng từ khoá. Mở sẵn một truy vấn cũng được: `index.html?q=softmax`.

### Phím tắt

| Phím | Việc |
|---|---|
| `j` / `k` | mục sau / mục trước |
| `m` | đánh dấu bài này đã học |
| `/` | tìm trong toàn kho |
| `Esc` | thoát tìm kiếm |

## Đọc một bài DSA cho đúng cách

Mười bài trong kệ `01-dsa` cố tình xếp theo kiểu **lõi ngắn, đuôi dài để tra** — đừng đọc tuần tự
từ đầu tới cuối:

- **Mục 01–04 là phần đọc**, hết khoảng 1,5 phút: ý tưởng, mẫu code cần thuộc, ba bẫy, một lab.
- **Từ mục 05 trở đi là phần tra.** Mỗi pattern một mục, mở đầu bằng *dấu hiệu nhận đề* — gặp đề
  lạ thì lướt các dấu hiệu này để biết nó thuộc pattern nào, rồi xem cần sửa gì trong mẫu code.
- Mỗi pattern kèm danh sách bài LeetCode có link, ghi rõ bài đó luyện cái gì. Cuối mỗi bài có
  **thứ tự luyện gợi ý 10 bài** phủ hết pattern của chủ đề đó — làm theo đúng thứ tự ấy.

Đích không phải số bài đã giải. Đích là: gặp pattern → nhận ra → giải trong 15–30 phút →
nói được complexity.

## Muốn sửa hoặc thêm bài?

Cấu trúc thư mục, cách thêm bài, bảng màu, bộ khuôn hình và quy tắc soạn nằm ở
**[CLAUDE.md](CLAUDE.md)**.
