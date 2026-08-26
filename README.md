# MazeAI

Kho deep dive chuẩn bị phỏng vấn Big Tech. Site tĩnh thuần, **không cần build, không cần server** —
mở thẳng `index.html` bằng trình duyệt là chạy.

## Cây thư mục = đúng những gì nhìn thấy trên giao diện

Ba tầng: **kệ → nhóm → bài**, xếp theo syllabus ôn tập.

```
index.html                       ← trang thư viện
assets/style.css · app.js · catalog.js* · search-index.js*     (* sinh tự động)
content/
  01-dsa/
    category.json                ← tên kệ, ghi chú, danh sách nhóm + thứ tự bài
    01-foundations/big-o-complexity/{index.html, lab.js}
    02-data-structures/{stack-monotonic-queue, heap-priority-queue, tree-bst-traversal, union-find}
    03-algorithms/{two-pointers-sliding-window, binary-search, graph-bfs-dfs-topo, backtracking, dynamic-programming}
  02-cs-fundamentals/
    01-python-internals/{memory-model-mutability, iterator-generator-decorator, dict-hash-table, gil-thread-process-async}
    02-sql/{sql-index-query-plan, sql-window-functions, transaction-isolation}
    03-os-networking/{http-tcp-caching}
  03-machine-learning/
    01-classical-ml/{linear-logistic-regression, tree-ensemble-boosting}
    02-statistics/{statistics-ab-testing}
    03-model-evaluation/{metrics-confusion-matrix}
    04-ml-theory/{overfitting-regularization}
  04-deep-learning/
    01-neural-network/{backpropagation, normalization-initialization}
    02-cnn/{cnn-mobilenet}
  05-llm/
    01-transformer/{self-attention-transformer}
    02-llm/{fine-tuning-sft-rlhf-dpo-lora}
    03-rag/{rag-end-to-end}
    04-llm-system/{inference-optimization}
  06-ml-system-design/01-frameworks/{ml-system-design}
  07-mlops/01-serving/{mlops-serving}
tools/build.py                   ← quét content/ sinh lại catalog.js + search-index.js
archive/mazeai-single-file.html  ← bản gốc gộp 1 file, giữ để đối chiếu
```

Số thứ tự ở tên thư mục quyết định thứ tự hiển thị. Thứ tự bài trong một nhóm nằm ở `books`
trong `category.json`. Kệ chỉ có đúng một nhóm thì trang chủ không hiện tiêu đề nhóm.

## Thêm một bài mới

1. Chép một thư mục bài có sẵn sang đúng nhóm, đổi tên thư mục.
2. Sửa `index.html` của nó:
   - `<article class="doc" id="art-SLUG" data-title="…" data-tag="…" data-blurb="…">`
     — `id` phải duy nhất trong cả kho; `data-*` chính là nội dung thẻ card ngoài trang chủ;
   - mỗi mục là một `<section id="SLUG-sN">` mở đầu bằng
     `<div class="sh"><b>01</b><h2>Tên mục</h2></div>` — mục lục bên trái và breadcrumb tự dựng
     từ đây, không phải khai báo ở đâu khác.
3. Thêm tên thư mục vào `books` của đúng nhóm trong `category.json`.
4. Chạy `python3 tools/build.py`.

Thêm nhóm mới: tạo thư mục `NN-ten-nhom/` rồi thêm `{"dir", "name", "books"}` vào `groups`.
Thêm kệ mới: tạo `content/NN-ten-ke/category.json` với `{"name", "note", "groups": []}`.

## Sau mỗi lần sửa nội dung

```bash
python3 tools/build.py
```

Sinh lại `assets/catalog.js` và `assets/search-index.js`, đồng thời báo các chỗ lệch: thư mục bài
chưa được liệt kê, khai báo trỏ tới thư mục không tồn tại, thiếu `index.html`. Không chạy lại thì
bài mới không hiện ở trang chủ và không tìm được.

## Đọc & học

Trang bài được bố trí để học chứ không chỉ để đọc:

- **dòng ngắn ~72 ký tự** cho phần chữ, còn code / bảng / sơ đồ / lab vẫn để rộng;
- **mỗi mục là một khối** có số thứ tự dạng huy hiệu và đường kẻ ngăn, lướt là thấy ranh giới;
- **thanh tiến độ đọc** ở đỉnh trang, mục lục đếm `06 / 15` và tô xanh những mục đã đi qua;
- **đánh dấu đã học** ở cuối mỗi bài — lưu trong `localStorage`, trang chủ hiện tổng tiến độ
  và có nút lọc *chỉ bài chưa học*;
- **mở/đóng toàn bộ phần hỏi đáp** bằng một nút trên tiêu đề mục, để tự kiểm tra trước khi xem đáp án.

Phím tắt: `j` mục sau · `k` mục trước · `m` đánh dấu đã học · `/` tìm toàn kho · `Esc` thoát tìm.

## Khuôn bài DSA

Mười bài trong `01-dsa` dùng chung một khuôn: **lõi đọc 1,5 phút, phần còn lại để tra**.

```
01  Ý tưởng               1 hình + 1 câu chốt + 2 gạch đầu dòng
02  Mẫu code cần thuộc    1-2 khối 6-8 dòng
03  Ba bẫy                3 thẻ ngắn
04  Lab                   chạy từng bước
─────────────────────────  hết phần đọc
05+ Mỗi pattern một mục   dấu hiệu nhận đề (.sig) → sửa gì trong mẫu →
                          danh sách bài LeetCode có link (.probs)
cuối Hỏi đáp              4 câu, mỗi câu trả lời 1-2 dòng
```

160 bài LeetCode chia theo 48 pattern, mỗi bài ghi rõ luyện cái gì, cuối mỗi bài có
thứ tự luyện gợi ý 10 bài phủ hết pattern của chủ đề đó.

## Trực quan — bộ khuôn hình

Hình là thứ giúp học nhanh nhất, nên vẽ hình phải rẻ. **[kit.html](kit.html)** là trang tra khuôn:
mở ra, chép đoạn HTML dưới mỗi hình, thay chữ. Không phải tính toạ độ, tự co giãn theo màn hình,
tự đúng bảng màu.

| Khuôn | Dùng cho |
|---|---|
| `.strip` | mảng, miền đáp án, ô nhớ, dãy FALSE→TRUE |
| `.flow` | quy trình 2–4 bước, ba nhánh của một quyết định |
| `.cmp` | đối chiếu hai cột: hai quy ước, hai cách làm |
| `.stack` | pipeline dọc: RAG, vòng đời request, lượt forward |
| `.mtx` | ma trận 2×2: confusion matrix, bias–variance |
| `.axis` | thứ có thứ tự: mức cô lập, mức nén, độ trễ |
| `.seq` | trình tự qua lại: bắt tay TCP, giao thức hai bên |
| `.bars` | so sánh đại lượng chênh nhau nhiều lần |

Quy ước màu dùng chung cho **mọi** hình trong kho — đừng đổi nghĩa giữa các bài:
xanh dương = dữ liệu / thứ đang xét · vàng = con trỏ, điểm nhấn, đáp án ·
đỏ = sai, bị loại, chưa thoả · xanh lá = đúng, kết quả, đã thoả.

Ba quy tắc khi soạn: mỗi mục **một** hình (cần hai hình thường là dấu hiệu mục đó nên tách đôi);
hình phải **thay được** đoạn văn chứ không minh hoạ thêm cho nó; chữ trong hình càng ít càng tốt.

Chỉ dùng SVG khi hình có đường cong, đường chéo hoặc trục toạ độ thật — mẫu ở
[mục mảng xoay](content/01-dsa/03-algorithms/binary-search/index.html#binsearch-s9):
`viewBox="0 0 560 200"`, cột rộng 60, cách nhau 12, đáy y=158. Giữ nguyên khung này thì mọi
biểu đồ cột trong kho nhìn như một bộ.

## Chỗ trống theo syllabus

Khung thư mục đã dựng sẵn cho các mảng còn thiếu bài:

| Kệ / nhóm | Chưa có bài |
|---|---|
| `01-dsa/03-algorithms` | prefix sum · greedy · intervals · shortest path (Dijkstra) |
| `01-dsa/02-data-structures` | linked list · trie |
| `01-dsa` | bộ công cụ Python cho LeetCode: `bisect`, `Counter`, `defaultdict`, `deque`, comprehension |
| `02-cs-fundamentals/02-sql` | SQL nền: JOIN · GROUP BY / HAVING · subquery · CTE · normalization |
| `02-cs-fundamentals/03-os-networking` | process vs thread ở tầng OS · CPU scheduling · REST API · load balancing · connection pool |
| `03-machine-learning/01-classical-ml` | SVM · KNN · Naive Bayes · K-means · PCA |
| `03-machine-learning` | nền toán: probability · expectation/variance · Bayes · gradient · matrix · eigenvector · MLE/MAP |
| `04-deep-learning/01-neural-network` | activation function · dropout (đang nằm rải trong bài chuẩn hoá & overfitting) |
| `05-llm/01-transformer` | tokenization · embedding · positional encoding (bài hiện tại chỉ chạm qua) |
| `05-llm/02-llm` | pretraining · decoding: temperature / top-k / top-p · quantization (QLoRA) |
| `05-llm/03-rag` | vector database · chiến lược chunking · reranking chuyên sâu |
| `06-ml-system-design` | recommendation system · LLM/RAG system (hai ví dụ thiết kế đầu–cuối) |
| `07-mlops` | Git · Docker · Linux · FastAPI · CI/CD · experiment tracking · GPU inference |
