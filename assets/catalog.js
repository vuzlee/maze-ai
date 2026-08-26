/* SINH TỰ ĐỘNG bởi tools/build.py — đừng sửa tay. */
window.CATALOG = [
 {
  "dir": "01-dsa",
  "name": "DSA — cấu trúc dữ liệu & giải thuật",
  "note": "Ưu tiên số 1. Đích không phải số bài đã giải: gặp pattern → nhận ra → giải trong 15–30 phút → nói được complexity.",
  "groups": [
   {
    "dir": "01-foundations",
    "name": "Nền tảng & phân tích",
    "books": [
     {
      "dir": "big-o-complexity",
      "slug": "bigo",
      "title": "Big-O & phân tích độ phức tạp",
      "tag": "Nền tảng",
      "blurb": "Cách đếm ra O(n log n), amortized thật sự là gì, chi phí ẩn của Python, và ngưỡng n nào thì thuật toán gãy.",
      "n": 15,
      "path": "content/01-dsa/01-foundations/big-o-complexity/index.html"
     }
    ]
   },
   {
    "dir": "02-data-structures",
    "name": "Cấu trúc dữ liệu",
    "books": [
     {
      "dir": "stack-monotonic-queue",
      "slug": "stack",
      "title": "Stack, monotonic stack & queue",
      "tag": "Cấu trúc",
      "blurb": "Monotonic stack biến O(n²) thành O(n): phần tử lớn hơn kế tiếp, histogram, hứng nước mưa, và deque cho max cửa sổ.",
      "n": 15,
      "path": "content/01-dsa/02-data-structures/stack-monotonic-queue/index.html"
     },
     {
      "dir": "heap-priority-queue",
      "slug": "heap",
      "title": "Heap & priority queue",
      "tag": "Cấu trúc",
      "blurb": "Cây nằm trong mảng phẳng, cơ chế sift, vì sao heapify là O(n), bốn cách giải top-K, và thứ heap không làm được.",
      "n": 15,
      "path": "content/01-dsa/02-data-structures/heap-priority-queue/index.html"
     },
     {
      "dir": "tree-bst-traversal",
      "slug": "tree",
      "title": "Cây, BST & các kiểu duyệt",
      "tag": "Cấu trúc",
      "blurb": "Chọn kiểu duyệt theo nhu cầu chứ không theo thứ tự, khung đệ quy bottom-up, ba ca xoá BST, và bẫy validate BST.",
      "n": 15,
      "path": "content/01-dsa/02-data-structures/tree-bst-traversal/index.html"
     },
     {
      "dir": "union-find",
      "slug": "dsu",
      "title": "Union-Find (DSU)",
      "tag": "Cấu trúc",
      "blurb": "Vì sao cần cả hai tối ưu, khi nào thắng DFS, DSU trên 2n đỉnh cho quan hệ đối kháng, và Kruskal.",
      "n": 15,
      "path": "content/01-dsa/02-data-structures/union-find/index.html"
     }
    ]
   },
   {
    "dir": "03-algorithms",
    "name": "Giải thuật & pattern",
    "books": [
     {
      "dir": "two-pointers-sliding-window",
      "slug": "window",
      "title": "Two pointers & sliding window",
      "tag": "Kỹ thuật",
      "blurb": "Hai mẫu code, ba bẫy, và 5 pattern kèm 22 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/03-algorithms/two-pointers-sliding-window/index.html"
     },
     {
      "dir": "binary-search",
      "slug": "binsearch",
      "title": "Binary search",
      "tag": "Kỹ thuật",
      "blurb": "Một mẫu code phủ mọi đề, ba bẫy, và 5 pattern kèm 20 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/03-algorithms/binary-search/index.html"
     },
     {
      "dir": "graph-bfs-dfs-topo",
      "slug": "graph",
      "title": "Đồ thị — BFS, DFS, topo sort",
      "tag": "Kỹ thuật",
      "blurb": "Hai mẫu code, ba bẫy, và 5 pattern kèm 22 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/03-algorithms/graph-bfs-dfs-topo/index.html"
     },
     {
      "dir": "backtracking",
      "slug": "backtrack",
      "title": "Backtracking",
      "tag": "Kỹ thuật",
      "blurb": "Khung sáu dòng cho subsets, permutations, N-Queens. Vì sao phải hoàn tác, cách bỏ trùng, và cắt tỉa.",
      "n": 15,
      "path": "content/01-dsa/03-algorithms/backtracking/index.html"
     },
     {
      "dir": "dynamic-programming",
      "slug": "dp",
      "title": "Dynamic programming",
      "tag": "Kỹ thuật",
      "blurb": "Bốn câu hỏi để dựng lời giải, đường từ backtracking sang bảng, vì sao thứ tự vòng lặp knapsack khác nhau, và cách chọn trạng thái.",
      "n": 15,
      "path": "content/01-dsa/03-algorithms/dynamic-programming/index.html"
     }
    ]
   }
  ]
 },
 {
  "dir": "02-cs-fundamentals",
  "name": "CS fundamentals",
  "note": "Phần giúp không bị nhìn như “AI guy chỉ biết model”.",
  "groups": [
   {
    "dir": "01-python-internals",
    "name": "Python internals",
    "books": [
     {
      "dir": "memory-model-mutability",
      "slug": "memory",
      "title": "Mô hình bộ nhớ & mutability",
      "tag": "Python internals",
      "blurb": "Biến là cái tên, không phải ô nhớ. Gán, shallow, deep copy, bốn cái bẫy, đếm tham chiếu và rò rỉ bộ nhớ.",
      "n": 15,
      "path": "content/02-cs-fundamentals/01-python-internals/memory-model-mutability/index.html"
     },
     {
      "dir": "iterator-generator-decorator",
      "slug": "iterator",
      "title": "Iterator, generator, decorator",
      "tag": "Python internals",
      "blurb": "Iterable khác iterator, vòng for thực chất làm gì, bộ nhớ O(n) xuống O(1), ba tầng closure của decorator.",
      "n": 15,
      "path": "content/02-cs-fundamentals/01-python-internals/iterator-generator-decorator/index.html"
     },
     {
      "dir": "dict-hash-table",
      "slug": "dict",
      "title": "Python dict & hash table",
      "tag": "Python internals",
      "blurb": "Hash function, hashable, collision, probe sequence, clustering, tombstone, resize, insertion order. Công thức lấy đúng theo mã nguồn CPython.",
      "n": 22,
      "path": "content/02-cs-fundamentals/01-python-internals/dict-hash-table/index.html"
     },
     {
      "dir": "gil-thread-process-async",
      "slug": "gil",
      "title": "GIL, thread, process, async",
      "tag": "Đồng thời",
      "blurb": "GIL khoá cái gì, chờ hay tính, ba lỗi async làm treo server, và vì sao GIL không cứu bạn khỏi race condition.",
      "n": 15,
      "path": "content/02-cs-fundamentals/01-python-internals/gil-thread-process-async/index.html"
     }
    ]
   },
   {
    "dir": "02-sql",
    "name": "SQL & cơ sở dữ liệu",
    "books": [
     {
      "dir": "sql-index-query-plan",
      "slug": "sqlindex",
      "title": "SQL — index & query plan",
      "tag": "PostgreSQL",
      "blurb": "Đọc EXPLAIN, vì sao planner bỏ qua index, leftmost prefix, ba thuật toán join, và bài toán N+1.",
      "n": 15,
      "path": "content/02-cs-fundamentals/02-sql/sql-index-query-plan/index.html"
     },
     {
      "dir": "sql-window-functions",
      "slug": "sqlwindow",
      "title": "SQL — window functions",
      "tag": "PostgreSQL",
      "blurb": "Khác GROUP BY ở đâu, vì sao WHERE không lọc được, ba hàm xếp hạng, top-N mỗi nhóm, và bẫy frame mặc định.",
      "n": 15,
      "path": "content/02-cs-fundamentals/02-sql/sql-window-functions/index.html"
     },
     {
      "dir": "transaction-isolation",
      "slug": "sqltx",
      "title": "Transaction & isolation level",
      "tag": "PostgreSQL",
      "blurb": "Bốn hiện tượng dị thường, mức nào chặn gì, MVCC, ba cách chữa lost update, deadlock và retry.",
      "n": 15,
      "path": "content/02-cs-fundamentals/02-sql/transaction-isolation/index.html"
     }
    ]
   },
   {
    "dir": "03-os-networking",
    "name": "OS & networking",
    "books": [
     {
      "dir": "http-tcp-caching",
      "slug": "net",
      "title": "HTTP, TCP & caching",
      "tag": "Mạng",
      "blurb": "Đếm vòng khứ hồi, khi nào được thử lại, backoff có jitter, năm tầng cache, thundering herd, circuit breaker.",
      "n": 15,
      "path": "content/02-cs-fundamentals/03-os-networking/http-tcp-caching/index.html"
     }
    ]
   }
  ]
 },
 {
  "dir": "03-machine-learning",
  "name": "Machine learning fundamentals",
  "note": "Không hỏi model là gì — hỏi vì sao chọn nó.",
  "groups": [
   {
    "dir": "01-classical-ml",
    "name": "Classical ML",
    "books": [
     {
      "dir": "linear-logistic-regression",
      "slug": "linreg",
      "title": "Linear & logistic regression",
      "tag": "Nền tảng",
      "blurb": "Vì sao không dùng MSE cho phân loại, vì sao L1 tạo hệ số 0, bốn giả định, và cách đọc odds ratio.",
      "n": 15,
      "path": "content/03-machine-learning/01-classical-ml/linear-logistic-regression/index.html"
     }
    ]
   },
   {
    "dir": "02-tree-models",
    "name": "Cây & ensemble — học theo thứ tự",
    "books": [
     {
      "dir": "tree-family-overview",
      "slug": "treeintro",
      "title": "Bản đồ nhánh cây — bắt đầu từ đâu",
      "tag": "Nhập môn",
      "blurb": "Bài đầu tiên của nhánh: người ta đang cố giải quyết vấn đề gì, lịch sử 40 năm của nhánh này, hai hướng bagging và boosting, và học theo thứ tự nào.",
      "n": 8,
      "path": "content/03-machine-learning/02-tree-models/tree-family-overview/index.html"
     },
     {
      "dir": "decision-tree",
      "slug": "dtree",
      "title": "Decision Tree — một cây học thế nào",
      "tag": "Nhập môn",
      "blurb": "Đọc một cây, máy chọn câu hỏi ra sao, Gini và information gain, vì sao cây học thuộc dữ liệu, và ba núm để hãm nó lại.",
      "n": 12,
      "path": "content/03-machine-learning/02-tree-models/decision-tree/index.html"
     },
     {
      "dir": "tree-ensemble-boosting",
      "slug": "trees",
      "title": "Rừng & boosting — bản gộp",
      "tag": "Đang tách",
      "blurb": "Bản tổng hợp cũ: Random Forest, OOB, gradient boosting, XGBoost/LightGBM, feature importance. Sẽ tách thành từng bài riêng theo lộ trình ở bài tổng quan.",
      "n": 15,
      "path": "content/03-machine-learning/02-tree-models/tree-ensemble-boosting/index.html"
     }
    ]
   },
   {
    "dir": "03-statistics",
    "name": "Thống kê & A/B testing",
    "books": [
     {
      "dir": "statistics-ab-testing",
      "slug": "stats",
      "title": "Thống kê & A/B testing",
      "tag": "Thống kê",
      "blurb": "P-value nghĩa là gì, bốn đại lượng gắn nhau, vì sao nhìn kết quả sớm làm dương giả tăng vọt, năm cái bẫy thực tế.",
      "n": 15,
      "path": "content/03-machine-learning/03-statistics/statistics-ab-testing/index.html"
     }
    ]
   },
   {
    "dir": "04-model-evaluation",
    "name": "Đánh giá model",
    "books": [
     {
      "dir": "metrics-confusion-matrix",
      "slug": "metrics",
      "title": "Metric & confusion matrix",
      "tag": "Đánh giá",
      "blurb": "Bốn ô ra mọi chỉ số, vì sao ROC-AUC nói dối khi lớp dương hiếm, chọn ngưỡng theo chi phí, và calibration.",
      "n": 15,
      "path": "content/03-machine-learning/04-model-evaluation/metrics-confusion-matrix/index.html"
     }
    ]
   },
   {
    "dir": "05-ml-theory",
    "name": "Lý thuyết & tổng quát hoá",
    "books": [
     {
      "dir": "overfitting-regularization",
      "slug": "overfit",
      "title": "Overfitting & regularization",
      "tag": "Tổng quát hoá",
      "blurb": "Đọc learning curve, bias–variance, sáu nguồn rò rỉ dữ liệu, vì sao random search thắng grid, và chia dữ liệu đúng kiểu.",
      "n": 15,
      "path": "content/03-machine-learning/05-ml-theory/overfitting-regularization/index.html"
     }
    ]
   }
  ]
 },
 {
  "dir": "04-deep-learning",
  "name": "Deep learning",
  "note": "Từ dùng được framework sang hiểu được model.",
  "groups": [
   {
    "dir": "01-neural-network",
    "name": "Neural network",
    "books": [
     {
      "dir": "backpropagation",
      "slug": "backprop",
      "title": "Backpropagation từng bước",
      "tag": "Gradient",
      "blurb": "Mạng 2-2-1 với số thật, vì sao softmax + CE cho gradient p − y, gradient teo và nổ, và checklist debug.",
      "n": 15,
      "path": "content/04-deep-learning/01-neural-network/backpropagation/index.html"
     },
     {
      "dir": "normalization-initialization",
      "slug": "norminit",
      "title": "Chuẩn hoá & khởi tạo",
      "tag": "Huấn luyện",
      "blurb": "Dẫn công thức khởi tạo từ phương sai, BatchNorm thật sự làm gì, Pre-LN so với Post-LN, và chẩn đoán bằng thống kê.",
      "n": 15,
      "path": "content/04-deep-learning/01-neural-network/normalization-initialization/index.html"
     }
    ]
   },
   {
    "dir": "02-cnn",
    "name": "CNN & thị giác",
    "books": [
     {
      "dir": "cnn-mobilenet",
      "slug": "cnn",
      "title": "CNN & MobileNet",
      "tag": "Thị giác · edge",
      "blurb": "Công thức shape và chi phí, vì sao depthwise separable rẻ 8–9 lần, inverted residual, linear bottleneck, lượng tử hoá.",
      "n": 15,
      "path": "content/04-deep-learning/02-cnn/cnn-mobilenet/index.html"
     }
    ]
   }
  ]
 },
 {
  "dir": "05-llm",
  "name": "Transformer · LLM · GenAI",
  "note": "Nơi tạo khác biệt lớn nhất hiện nay.",
  "groups": [
   {
    "dir": "01-transformer",
    "name": "Transformer",
    "books": [
     {
      "dir": "self-attention-transformer",
      "slug": "attn",
      "title": "Self-attention & Transformer",
      "tag": "Transformer",
      "blurb": "Đường đi từ token tới logits: Q/K/V, scaled dot-product, masking, multi-head, residual, FFN, KV cache, GQA. Hai lab tương tác.",
      "n": 22,
      "path": "content/05-llm/01-transformer/self-attention-transformer/index.html"
     }
    ]
   },
   {
    "dir": "02-llm",
    "name": "LLM & fine-tuning",
    "books": [
     {
      "dir": "fine-tuning-sft-rlhf-dpo-lora",
      "slug": "finetune",
      "title": "Fine-tuning — SFT, RLHF, DPO, LoRA",
      "tag": "Huấn luyện tiếp",
      "blurb": "Có nên fine-tune không, che mất mát trên prompt, cơ chế LoRA và vì sao B khởi tạo bằng 0, DPO bỏ reward model thế nào.",
      "n": 15,
      "path": "content/05-llm/02-llm/fine-tuning-sft-rlhf-dpo-lora/index.html"
     }
    ]
   },
   {
    "dir": "03-rag",
    "name": "RAG",
    "books": [
     {
      "dir": "rag-end-to-end",
      "slug": "rag",
      "title": "RAG đầu–cuối",
      "tag": "Truy xuất",
      "blurb": "Chunking, hybrid search, reranking, lost-in-the-middle, cây debug năm bước và cách đánh giá tách hai tầng.",
      "n": 15,
      "path": "content/05-llm/03-rag/rag-end-to-end/index.html"
     }
    ]
   },
   {
    "dir": "04-llm-system",
    "name": "LLM system & inference",
    "books": [
     {
      "dir": "inference-optimization",
      "slug": "inference",
      "title": "Suy luận & tối ưu chi phí",
      "tag": "Vận hành",
      "blurb": "Prefill so với decode, tính KV cache, GQA, continuous batching, speculative decoding, bảng giảm chi phí.",
      "n": 15,
      "path": "content/05-llm/04-llm-system/inference-optimization/index.html"
     }
    ]
   }
  ]
 },
 {
  "dir": "06-ml-system-design",
  "name": "ML system design",
  "note": "Phần AI candidate hay thiếu nhất — và là vòng quyết định level.",
  "groups": [
   {
    "dir": "01-frameworks",
    "name": "Khung thiết kế",
    "books": [
     {
      "dir": "ml-system-design",
      "slug": "mlsys",
      "title": "ML system design",
      "tag": "Thiết kế",
      "blurb": "Khung bảy bước, vì sao luôn hai tầng, ngân sách độ trễ và số máy, vòng phản hồi, ví dụ phát hiện gian lận.",
      "n": 15,
      "path": "content/06-ml-system-design/01-frameworks/ml-system-design/index.html"
     }
    ]
   }
  ]
 },
 {
  "dir": "07-mlops",
  "name": "MLOps & engineering",
  "note": "Không cần thành DevOps, nhưng phải tự đưa được model ra production.",
  "groups": [
   {
    "dir": "01-serving",
    "name": "Phục vụ & vận hành model",
    "books": [
     {
      "dir": "mlops-serving",
      "slug": "mlops",
      "title": "MLOps & phục vụ model",
      "tag": "Vận hành",
      "blurb": "Ba thứ thay đổi, bốn chiến lược triển khai kèm bán kính rủi ro, phát hiện drift bằng PSI, point-in-time correctness.",
      "n": 15,
      "path": "content/07-mlops/01-serving/mlops-serving/index.html"
     }
    ]
   }
  ]
 }
];
