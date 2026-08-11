/* SINH TỰ ĐỘNG bởi tools/build.py — đừng sửa tay. */
window.CATALOG = [
 {
  "dir": "01-algorithms",
  "name": "Giải thuật & cấu trúc dữ liệu",
  "note": "Thứ quyết định vòng phỏng vấn đầu tiên.",
  "books": [
   {
    "dir": "big-o-complexity",
    "slug": "bigo",
    "title": "Big-O & phân tích độ phức tạp",
    "tag": "Nền tảng",
    "blurb": "Cách đếm ra O(n log n), amortized thật sự là gì, chi phí ẩn của Python, và ngưỡng n nào thì thuật toán gãy.",
    "n": 15,
    "path": "content/01-algorithms/big-o-complexity/index.html"
   },
   {
    "dir": "two-pointers-sliding-window",
    "slug": "window",
    "title": "Two pointers & sliding window",
    "tag": "Kỹ thuật",
    "blurb": "Điều kiện để hai kỹ thuật này đúng, hai mẫu code phủ hầu hết đề, kỹ thuật at-most-K, và lằn ranh phải đổi sang prefix sum.",
    "n": 14,
    "path": "content/01-algorithms/two-pointers-sliding-window/index.html"
   },
   {
    "dir": "binary-search",
    "slug": "binsearch",
    "title": "Binary search — mọi biến thể",
    "tag": "Kỹ thuật",
    "blurb": "Hai mẫu code phủ mọi đề, tìm nhị phân trên đáp án, mảng xoay, và vì sao lo < hi phải đi cùng hi = mid.",
    "n": 15,
    "path": "content/01-algorithms/binary-search/index.html"
   },
   {
    "dir": "stack-monotonic-queue",
    "slug": "stack",
    "title": "Stack, monotonic stack & queue",
    "tag": "Cấu trúc",
    "blurb": "Monotonic stack biến O(n²) thành O(n): phần tử lớn hơn kế tiếp, histogram, hứng nước mưa, và deque cho max cửa sổ.",
    "n": 15,
    "path": "content/01-algorithms/stack-monotonic-queue/index.html"
   },
   {
    "dir": "heap-priority-queue",
    "slug": "heap",
    "title": "Heap & priority queue",
    "tag": "Cấu trúc",
    "blurb": "Cây nằm trong mảng phẳng, cơ chế sift, vì sao heapify là O(n), bốn cách giải top-K, và thứ heap không làm được.",
    "n": 15,
    "path": "content/01-algorithms/heap-priority-queue/index.html"
   },
   {
    "dir": "tree-bst-traversal",
    "slug": "tree",
    "title": "Cây, BST & các kiểu duyệt",
    "tag": "Cấu trúc",
    "blurb": "Chọn kiểu duyệt theo nhu cầu chứ không theo thứ tự, khung đệ quy bottom-up, ba ca xoá BST, và bẫy validate BST.",
    "n": 15,
    "path": "content/01-algorithms/tree-bst-traversal/index.html"
   },
   {
    "dir": "graph-bfs-dfs-topo",
    "slug": "graph",
    "title": "Đồ thị — BFS, DFS, topo sort",
    "tag": "Kỹ thuật",
    "blurb": "Khi nào đánh dấu đã thăm, ba cách phát hiện chu trình, hai cách sắp topo, và BFS trên không gian trạng thái.",
    "n": 15,
    "path": "content/01-algorithms/graph-bfs-dfs-topo/index.html"
   },
   {
    "dir": "backtracking",
    "slug": "backtrack",
    "title": "Backtracking",
    "tag": "Kỹ thuật",
    "blurb": "Khung sáu dòng cho subsets, permutations, N-Queens. Vì sao phải hoàn tác, cách bỏ trùng, và cắt tỉa.",
    "n": 15,
    "path": "content/01-algorithms/backtracking/index.html"
   },
   {
    "dir": "dynamic-programming",
    "slug": "dp",
    "title": "Dynamic programming",
    "tag": "Kỹ thuật",
    "blurb": "Bốn câu hỏi để dựng lời giải, đường từ backtracking sang bảng, vì sao thứ tự vòng lặp knapsack khác nhau, và cách chọn trạng thái.",
    "n": 15,
    "path": "content/01-algorithms/dynamic-programming/index.html"
   },
   {
    "dir": "union-find",
    "slug": "dsu",
    "title": "Union-Find (DSU)",
    "tag": "Cấu trúc",
    "blurb": "Vì sao cần cả hai tối ưu, khi nào thắng DFS, DSU trên 2n đỉnh cho quan hệ đối kháng, và Kruskal.",
    "n": 15,
    "path": "content/01-algorithms/union-find/index.html"
   }
  ]
 },
 {
  "dir": "02-python",
  "name": "Python & nền tảng CS",
  "note": "Thứ phân biệt kỹ sư với người chạy notebook.",
  "books": [
   {
    "dir": "gil-thread-process-async",
    "slug": "gil",
    "title": "GIL, thread, process, async",
    "tag": "Đồng thời",
    "blurb": "GIL khoá cái gì, chờ hay tính, ba lỗi async làm treo server, và vì sao GIL không cứu bạn khỏi race condition.",
    "n": 15,
    "path": "content/02-python/gil-thread-process-async/index.html"
   },
   {
    "dir": "iterator-generator-decorator",
    "slug": "iterator",
    "title": "Iterator, generator, decorator",
    "tag": "Python internals",
    "blurb": "Iterable khác iterator, vòng for thực chất làm gì, bộ nhớ O(n) xuống O(1), ba tầng closure của decorator.",
    "n": 15,
    "path": "content/02-python/iterator-generator-decorator/index.html"
   },
   {
    "dir": "memory-model-mutability",
    "slug": "memory",
    "title": "Mô hình bộ nhớ & mutability",
    "tag": "Python internals",
    "blurb": "Biến là cái tên, không phải ô nhớ. Gán, shallow, deep copy, bốn cái bẫy, đếm tham chiếu và rò rỉ bộ nhớ.",
    "n": 15,
    "path": "content/02-python/memory-model-mutability/index.html"
   },
   {
    "dir": "dict-hash-table",
    "slug": "dict",
    "title": "Python dict & hash table",
    "tag": "Python internals",
    "blurb": "Hash function, hashable, collision, probe sequence, clustering, tombstone, resize, insertion order. Công thức lấy đúng theo mã nguồn CPython.",
    "n": 22,
    "path": "content/02-python/dict-hash-table/index.html"
   }
  ]
 },
 {
  "dir": "03-databases",
  "name": "SQL & cơ sở dữ liệu",
  "note": "Bị hỏi ở gần như mọi vòng có chữ data.",
  "books": [
   {
    "dir": "sql-index-query-plan",
    "slug": "sqlindex",
    "title": "SQL — index & query plan",
    "tag": "PostgreSQL",
    "blurb": "Đọc EXPLAIN, vì sao planner bỏ qua index, leftmost prefix, ba thuật toán join, và bài toán N+1.",
    "n": 15,
    "path": "content/03-databases/sql-index-query-plan/index.html"
   },
   {
    "dir": "sql-window-functions",
    "slug": "sqlwindow",
    "title": "SQL — window functions",
    "tag": "PostgreSQL",
    "blurb": "Khác GROUP BY ở đâu, vì sao WHERE không lọc được, ba hàm xếp hạng, top-N mỗi nhóm, và bẫy frame mặc định.",
    "n": 15,
    "path": "content/03-databases/sql-window-functions/index.html"
   },
   {
    "dir": "transaction-isolation",
    "slug": "sqltx",
    "title": "Transaction & isolation level",
    "tag": "PostgreSQL",
    "blurb": "Bốn hiện tượng dị thường, mức nào chặn gì, MVCC, ba cách chữa lost update, deadlock và retry.",
    "n": 15,
    "path": "content/03-databases/transaction-isolation/index.html"
   }
  ]
 },
 {
  "dir": "04-networking",
  "name": "Mạng & giao thức",
  "note": "Tầng dưới của mọi hệ thống phân tán.",
  "books": [
   {
    "dir": "http-tcp-caching",
    "slug": "net",
    "title": "HTTP, TCP & caching",
    "tag": "Mạng",
    "blurb": "Đếm vòng khứ hồi, khi nào được thử lại, backoff có jitter, năm tầng cache, thundering herd, circuit breaker.",
    "n": 15,
    "path": "content/04-networking/http-tcp-caching/index.html"
   }
  ]
 },
 {
  "dir": "05-machine-learning",
  "name": "Machine learning",
  "note": "Không hỏi model là gì — hỏi vì sao chọn nó.",
  "books": [
   {
    "dir": "linear-logistic-regression",
    "slug": "linreg",
    "title": "Linear & logistic regression",
    "tag": "Nền tảng",
    "blurb": "Vì sao không dùng MSE cho phân loại, vì sao L1 tạo hệ số 0, bốn giả định, và cách đọc odds ratio.",
    "n": 15,
    "path": "content/05-machine-learning/linear-logistic-regression/index.html"
   },
   {
    "dir": "tree-ensemble-boosting",
    "slug": "trees",
    "title": "Cây, rừng & boosting",
    "tag": "Dữ liệu bảng",
    "blurb": "Cách chọn điểm chia, bagging giảm variance boosting giảm bias, bẫy feature importance, và vì sao thắng deep learning.",
    "n": 15,
    "path": "content/05-machine-learning/tree-ensemble-boosting/index.html"
   },
   {
    "dir": "metrics-confusion-matrix",
    "slug": "metrics",
    "title": "Metric & confusion matrix",
    "tag": "Đánh giá",
    "blurb": "Bốn ô ra mọi chỉ số, vì sao ROC-AUC nói dối khi lớp dương hiếm, chọn ngưỡng theo chi phí, và calibration.",
    "n": 15,
    "path": "content/05-machine-learning/metrics-confusion-matrix/index.html"
   },
   {
    "dir": "overfitting-regularization",
    "slug": "overfit",
    "title": "Overfitting & regularization",
    "tag": "Tổng quát hoá",
    "blurb": "Đọc learning curve, bias–variance, sáu nguồn rò rỉ dữ liệu, vì sao random search thắng grid, và chia dữ liệu đúng kiểu.",
    "n": 15,
    "path": "content/05-machine-learning/overfitting-regularization/index.html"
   },
   {
    "dir": "statistics-ab-testing",
    "slug": "stats",
    "title": "Thống kê & A/B testing",
    "tag": "Thống kê",
    "blurb": "P-value nghĩa là gì, bốn đại lượng gắn nhau, vì sao nhìn kết quả sớm làm dương giả tăng vọt, năm cái bẫy thực tế.",
    "n": 15,
    "path": "content/05-machine-learning/statistics-ab-testing/index.html"
   }
  ]
 },
 {
  "dir": "06-deep-learning",
  "name": "Deep learning",
  "note": "Từ dùng được framework sang hiểu được model.",
  "books": [
   {
    "dir": "backpropagation",
    "slug": "backprop",
    "title": "Backpropagation từng bước",
    "tag": "Gradient",
    "blurb": "Mạng 2-2-1 với số thật, vì sao softmax + CE cho gradient p − y, gradient teo và nổ, và checklist debug.",
    "n": 15,
    "path": "content/06-deep-learning/backpropagation/index.html"
   },
   {
    "dir": "cnn-mobilenet",
    "slug": "cnn",
    "title": "CNN & MobileNet",
    "tag": "Thị giác · edge",
    "blurb": "Công thức shape và chi phí, vì sao depthwise separable rẻ 8–9 lần, inverted residual, linear bottleneck, lượng tử hoá.",
    "n": 15,
    "path": "content/06-deep-learning/cnn-mobilenet/index.html"
   },
   {
    "dir": "normalization-initialization",
    "slug": "norminit",
    "title": "Chuẩn hoá & khởi tạo",
    "tag": "Huấn luyện",
    "blurb": "Dẫn công thức khởi tạo từ phương sai, BatchNorm thật sự làm gì, Pre-LN so với Post-LN, và chẩn đoán bằng thống kê.",
    "n": 15,
    "path": "content/06-deep-learning/normalization-initialization/index.html"
   }
  ]
 },
 {
  "dir": "07-llm",
  "name": "LLM & GenAI",
  "note": "Nơi tạo khác biệt lớn nhất hiện nay.",
  "books": [
   {
    "dir": "self-attention-transformer",
    "slug": "attn",
    "title": "Self-attention & Transformer",
    "tag": "Transformer",
    "blurb": "Đường đi từ token tới logits: Q/K/V, scaled dot-product, masking, multi-head, residual, FFN, KV cache, GQA. Hai lab tương tác.",
    "n": 22,
    "path": "content/07-llm/self-attention-transformer/index.html"
   },
   {
    "dir": "fine-tuning-sft-rlhf-dpo-lora",
    "slug": "finetune",
    "title": "Fine-tuning — SFT, RLHF, DPO, LoRA",
    "tag": "Huấn luyện tiếp",
    "blurb": "Có nên fine-tune không, che mất mát trên prompt, cơ chế LoRA và vì sao B khởi tạo bằng 0, DPO bỏ reward model thế nào.",
    "n": 15,
    "path": "content/07-llm/fine-tuning-sft-rlhf-dpo-lora/index.html"
   },
   {
    "dir": "rag-end-to-end",
    "slug": "rag",
    "title": "RAG đầu–cuối",
    "tag": "Truy xuất",
    "blurb": "Chunking, hybrid search, reranking, lost-in-the-middle, cây debug năm bước và cách đánh giá tách hai tầng.",
    "n": 15,
    "path": "content/07-llm/rag-end-to-end/index.html"
   },
   {
    "dir": "inference-optimization",
    "slug": "inference",
    "title": "Suy luận & tối ưu chi phí",
    "tag": "Vận hành",
    "blurb": "Prefill so với decode, tính KV cache, GQA, continuous batching, speculative decoding, bảng giảm chi phí.",
    "n": 15,
    "path": "content/07-llm/inference-optimization/index.html"
   }
  ]
 },
 {
  "dir": "08-system-design",
  "name": "Thiết kế hệ thống & MLOps",
  "note": "Vòng quyết định level và lương.",
  "books": [
   {
    "dir": "ml-system-design",
    "slug": "mlsys",
    "title": "ML system design",
    "tag": "Thiết kế",
    "blurb": "Khung bảy bước, vì sao luôn hai tầng, ngân sách độ trễ và số máy, vòng phản hồi, ví dụ phát hiện gian lận.",
    "n": 15,
    "path": "content/08-system-design/ml-system-design/index.html"
   },
   {
    "dir": "mlops-serving",
    "slug": "mlops",
    "title": "MLOps & phục vụ model",
    "tag": "Vận hành",
    "blurb": "Ba thứ thay đổi, bốn chiến lược triển khai kèm bán kính rủi ro, phát hiện drift bằng PSI, point-in-time correctness.",
    "n": 15,
    "path": "content/08-system-design/mlops-serving/index.html"
   }
  ]
 }
];
