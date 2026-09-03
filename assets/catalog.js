/* SINH TỰ ĐỘNG bởi tools/build.py — đừng sửa tay. */
window.CATALOG = [
 {
  "dir": "01-dsa",
  "name": "DSA — data structures & algorithms",
  "note": "Ưu tiên số 1. Đích không phải số bài đã giải: gặp pattern → nhận ra → giải trong 15–30 phút → nói được complexity.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "dsa-overview",
      "slug": "dsaov",
      "title": "DSA overview",
      "tag": "Overview",
      "blurb": "DSA là gì, kệ này gồm hai phần nào, và học theo thứ tự nào cho nhanh vào việc.",
      "n": 3,
      "path": "content/01-dsa/01-overview/dsa-overview/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-foundations",
    "name": "Foundations",
    "books": [
     {
      "dir": "big-o-complexity",
      "slug": "bigo",
      "title": "Big-O",
      "tag": "Foundations",
      "blurb": "Bảng tra n → thuật toán được phép, ba quy tắc đếm, chi phí ẩn của Python, và cách nói complexity trong phỏng vấn.",
      "n": 9,
      "path": "content/01-dsa/02-foundations/big-o-complexity/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-data-structures",
    "name": "Data structures",
    "books": [
     {
      "dir": "data-structures-overview",
      "slug": "dsov",
      "title": "Data structures overview",
      "tag": "Overview",
      "blurb": "Tám cách cất dữ liệu trên một bảng: chọn khi nào, và chi phí từng thao tác.",
      "n": 2,
      "path": "content/01-dsa/03-data-structures/data-structures-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "array-string",
      "slug": "arrstr",
      "title": "Array & string",
      "tag": "Data structure",
      "blurb": "Bộ nhớ liên tục, chi phí thật của chèn/xoá, chuỗi bất biến, và vì sao nối chuỗi trong vòng lặp là O(n²).",
      "n": 7,
      "path": "content/01-dsa/03-data-structures/array-string/index.html",
      "skeleton": false,
      "lc": 6
     },
     {
      "dir": "linked-list",
      "slug": "llist",
      "title": "Linked list",
      "tag": "Data structure",
      "blurb": "Khi nào con trỏ thắng mảng, khuôn đảo danh sách, con trỏ giả, và ba dạng đề hay ra.",
      "n": 6,
      "path": "content/01-dsa/03-data-structures/linked-list/index.html",
      "skeleton": false,
      "lc": 8
     },
     {
      "dir": "hash-map",
      "slug": "hmap",
      "title": "Hash map & set",
      "tag": "Data structure",
      "blurb": "Vì sao O(1) trung bình, va chạm xử lý thế nào, khi nào tụt về O(n), và ba pattern đổi thời gian lấy bộ nhớ.",
      "n": 6,
      "path": "content/01-dsa/03-data-structures/hash-map/index.html",
      "skeleton": false,
      "lc": 8
     },
     {
      "dir": "stack-monotonic-queue",
      "slug": "stack",
      "title": "Stack & monotonic stack",
      "tag": "Data structure",
      "blurb": "Một mẫu code biến O(n²) thành O(n), ba bẫy, và 5 pattern kèm 19 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/03-data-structures/stack-monotonic-queue/index.html",
      "skeleton": false,
      "lc": 17
     },
     {
      "dir": "heap-priority-queue",
      "slug": "heap",
      "title": "Heap & priority queue",
      "tag": "Data structure",
      "blurb": "Cây nằm trong mảng phẳng, một mẫu code, ba bẫy, và 5 pattern kèm 15 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/03-data-structures/heap-priority-queue/index.html",
      "skeleton": false,
      "lc": 14
     },
     {
      "dir": "tree-bst-traversal",
      "slug": "tree",
      "title": "Tree, BST & traversal",
      "tag": "Data structure",
      "blurb": "Khung đệ quy sáu dòng, ba kiểu duyệt, ba bẫy, và 5 pattern kèm 19 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/03-data-structures/tree-bst-traversal/index.html",
      "skeleton": false,
      "lc": 19
     },
     {
      "dir": "trie",
      "slug": "trie",
      "title": "Trie",
      "tag": "Data structure",
      "blurb": "Cây tiền tố: tra theo tiền tố trong O(độ dài), đánh đổi bộ nhớ, và khi nào nó thắng hash map.",
      "n": 6,
      "path": "content/01-dsa/03-data-structures/trie/index.html",
      "skeleton": false,
      "lc": 5
     },
     {
      "dir": "union-find",
      "slug": "dsu",
      "title": "Union-Find (DSU)",
      "tag": "Data structure",
      "blurb": "Hai tối ưu bắt buộc, một mẫu code 8 dòng, ba bẫy, và 5 pattern kèm 14 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/03-data-structures/union-find/index.html",
      "skeleton": false,
      "lc": 12
     }
    ]
   },
   {
    "dir": "04-algorithms",
    "name": "Algorithms & patterns",
    "books": [
     {
      "dir": "algorithms-overview",
      "slug": "alov",
      "title": "Algorithms overview",
      "tag": "Overview",
      "blurb": "Đọc đề thấy chữ gì thì nghĩ tới pattern nào, và dữ liệu lớn cỡ nào thì được dùng cách nào.",
      "n": 2,
      "path": "content/01-dsa/04-algorithms/algorithms-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "sorting",
      "slug": "sort",
      "title": "Sorting",
      "tag": "Technique",
      "blurb": "Sáu thuật toán sort kèm code Python và complexity, vì sao O(n log n) là chặn dưới, và stable sort.",
      "n": 9,
      "path": "content/01-dsa/04-algorithms/sorting/index.html",
      "skeleton": false,
      "lc": 6
     },
     {
      "dir": "two-pointers",
      "slug": "twoptr",
      "title": "Two pointers",
      "tag": "Technique",
      "blurb": "Hai mẫu code, ba bẫy, và 2 pattern kèm 9 bài LeetCode có link.",
      "n": 7,
      "path": "content/01-dsa/04-algorithms/two-pointers/index.html",
      "skeleton": false,
      "lc": 9
     },
     {
      "dir": "sliding-window",
      "slug": "window",
      "title": "Sliding window",
      "tag": "Technique",
      "blurb": "Một mẫu code co giãn phủ gần hết đề, ba bẫy, và 3 pattern kèm 12 bài LeetCode có link.",
      "n": 8,
      "path": "content/01-dsa/04-algorithms/sliding-window/index.html",
      "skeleton": false,
      "lc": 12
     },
     {
      "dir": "prefix-sum",
      "slug": "prefix",
      "title": "Prefix sum & difference array",
      "tag": "Technique",
      "blurb": "Tiền xử lý một lần để trả lời truy vấn đoạn trong O(1), mẹo hash cho tổng bằng k, và mảng hiệu cho cập nhật đoạn.",
      "n": 6,
      "path": "content/01-dsa/04-algorithms/prefix-sum/index.html",
      "skeleton": false,
      "lc": 8
     },
     {
      "dir": "binary-search",
      "slug": "binsearch",
      "title": "Binary search",
      "tag": "Technique",
      "blurb": "Một mẫu code phủ mọi đề, ba bẫy, và 5 pattern kèm 20 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/04-algorithms/binary-search/index.html",
      "skeleton": false,
      "lc": 19
     },
     {
      "dir": "greedy",
      "slug": "greedy",
      "title": "Greedy",
      "tag": "Technique",
      "blurb": "Cách chứng minh một lựa chọn tham lam là đúng, ba dạng đề kinh điển, và vì sao greedy sai lại khó phát hiện.",
      "n": 6,
      "path": "content/01-dsa/04-algorithms/greedy/index.html",
      "skeleton": false,
      "lc": 8
     },
     {
      "dir": "intervals",
      "slug": "itv",
      "title": "Interval",
      "tag": "Technique",
      "blurb": "Sắp xếp theo đầu hay theo cuối, gộp đoạn, đếm đoạn chồng nhau bằng đường quét, và lịch phòng họp.",
      "n": 6,
      "path": "content/01-dsa/04-algorithms/intervals/index.html",
      "skeleton": false,
      "lc": 7
     },
     {
      "dir": "backtracking",
      "slug": "backtrack",
      "title": "Backtracking",
      "tag": "Technique",
      "blurb": "Khung sáu dòng cho mọi bài liệt kê, ba bẫy, và 5 pattern kèm 18 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/04-algorithms/backtracking/index.html",
      "skeleton": false,
      "lc": 16
     },
     {
      "dir": "graph-bfs-dfs-topo",
      "slug": "graph",
      "title": "Graph — BFS, DFS, topo sort",
      "tag": "Technique",
      "blurb": "Hai mẫu code, ba bẫy, và 5 pattern kèm 22 bài LeetCode có link.",
      "n": 10,
      "path": "content/01-dsa/04-algorithms/graph-bfs-dfs-topo/index.html",
      "skeleton": false,
      "lc": 20
     },
     {
      "dir": "shortest-path",
      "slug": "sp",
      "title": "Shortest path",
      "tag": "Technique",
      "blurb": "Dijkstra là BFS đổi hàng đợi thành heap, khi nào cần Bellman-Ford, và Floyd-Warshall cho mọi cặp.",
      "n": 7,
      "path": "content/01-dsa/04-algorithms/shortest-path/index.html",
      "skeleton": false,
      "lc": 6
     },
     {
      "dir": "dynamic-programming",
      "slug": "dp",
      "title": "Dynamic programming",
      "tag": "Technique",
      "blurb": "Bốn câu hỏi để dựng lời giải, ba bẫy, và 5 pattern kèm 21 bài LeetCode có link.",
      "n": 11,
      "path": "content/01-dsa/04-algorithms/dynamic-programming/index.html",
      "skeleton": false,
      "lc": 21
     }
    ]
   }
  ]
 },
 {
  "dir": "02-python",
  "name": "Python",
  "note": "Ngôn ngữ bạn sẽ code trong phỏng vấn. Hiểu tới cơ chế bên dưới thì viết nhanh hơn và trả lời được câu hỏi đào sâu.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "python-overview",
      "slug": "pyov",
      "title": "Python overview",
      "tag": "Overview",
      "blurb": "Python được thiết kế quanh vài quy tắc nhất quán — nắm chúng thì phần còn lại tự suy ra được.",
      "n": 6,
      "path": "content/02-python/01-overview/python-overview/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-language-core",
    "name": "Language core",
    "books": [
     {
      "dir": "language-core-overview",
      "slug": "lcov",
      "title": "Language core overview",
      "tag": "Overview",
      "blurb": "Các quy tắc nhất quán của Python — mô hình object, tham chiếu, giao thức, và phạm vi biến.",
      "n": 5,
      "path": "content/02-python/02-language-core/language-core-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "memory-model-mutability",
      "slug": "memory",
      "title": "Memory model & mutability",
      "tag": "Python internals",
      "blurb": "Biến là cái tên, không phải ô nhớ. Gán, shallow copy, deep copy, truyền tham số, và bốn cái bẫy mọc ra từ đó.",
      "n": 11,
      "path": "content/02-python/02-language-core/memory-model-mutability/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "memory-management-gc",
      "slug": "memgc",
      "title": "Memory management & GC",
      "tag": "Python internals",
      "blurb": "Đếm tham chiếu, chu trình, bộ thu gom theo thế hệ, bộ nhớ thật của object và bốn nguồn rò rỉ.",
      "n": 6,
      "path": "content/02-python/02-language-core/memory-management-gc/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "scope-legb",
      "slug": "scope",
      "title": "Scope & LEGB",
      "tag": "Language core",
      "blurb": "Python tra một cái tên ở đâu: bốn tầng LEGB, global và nonlocal, và cách hàm nhận đối số qua *args, **kwargs.",
      "n": 7,
      "path": "content/02-python/02-language-core/scope-legb/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "data-model-dunder",
      "slug": "dunder",
      "title": "Data model & dunder",
      "tag": "Language core",
      "blurb": "Vì sao len(x) chứ không phải x.len(), giao thức phía sau toán tử, và cách một object tự nhập vai list hay dict.",
      "n": 6,
      "path": "content/02-python/02-language-core/data-model-dunder/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "iterator-generator",
      "slug": "iter",
      "title": "Iterator & generator",
      "tag": "Python",
      "blurb": "Iterable khác iterator ở đâu, vòng for thực chất làm gì, generator tiết kiệm bao nhiêu bộ nhớ, yield from và itertools.",
      "n": 11,
      "path": "content/02-python/02-language-core/iterator-generator/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "decorator-context-manager",
      "slug": "deco",
      "title": "Decorator & context manager",
      "tag": "Python",
      "blurb": "Closure là nền của decorator, ba tầng lồng nhau khi có tham số, vì sao cần functools.wraps, và try/finally trong context manager.",
      "n": 8,
      "path": "content/02-python/02-language-core/decorator-context-manager/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "exception-handling",
      "slug": "exc",
      "title": "Exception handling",
      "tag": "Language core",
      "blurb": "try/except/else/finally, cây Exception, exception tự viết, raise from — và vì sao except: trần là lỗi nặng nhất.",
      "n": 7,
      "path": "content/02-python/02-language-core/exception-handling/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-builtin-structures",
    "name": "Built-in types",
    "books": [
     {
      "dir": "list-tuple-set",
      "slug": "listset",
      "title": "List, tuple & set",
      "tag": "Built-in types",
      "blurb": "Chi phí thật của từng thao tác, vì sao tuple làm khoá được mà list thì không, và set là hash table không giá trị.",
      "n": 6,
      "path": "content/02-python/03-builtin-structures/list-tuple-set/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "dict-hash-table",
      "slug": "dict",
      "title": "Python dict & hash table",
      "tag": "Python internals",
      "blurb": "Hash function, hashable, collision, probe sequence, clustering, tombstone, resize, insertion order. Công thức lấy đúng theo mã nguồn CPython.",
      "n": 23,
      "path": "content/02-python/03-builtin-structures/dict-hash-table/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "04-concurrency",
    "name": "Concurrency",
    "books": [
     {
      "dir": "thread-process-gil",
      "slug": "gil",
      "title": "Thread, process & GIL",
      "tag": "Concurrency",
      "blurb": "Process và thread khác nhau ở bộ nhớ và chi phí chuyển ngữ cảnh — hiểu hai thứ đó rồi thì GIL chỉ còn là một câu.",
      "n": 11,
      "path": "content/02-python/04-concurrency/thread-process-gil/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "asyncio",
      "slug": "async",
      "title": "Async / asyncio",
      "tag": "Python",
      "blurb": "Vì sao 1000 kết nối thì async chứ không thread, ba lỗi async kinh điển, chi phí thật của từng mô hình, và bảng chọn.",
      "n": 9,
      "path": "content/02-python/04-concurrency/asyncio/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "05-toolkit",
    "name": "Toolkit",
    "books": [
     {
      "dir": "leetcode-toolkit",
      "slug": "kit",
      "title": "LeetCode toolkit",
      "tag": "Toolkit",
      "blurb": "bisect, Counter, defaultdict, deque, heapq và comprehension — sáu thứ rút ngắn lời giải nhiều nhất.",
      "n": 6,
      "path": "content/02-python/05-toolkit/leetcode-toolkit/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "06-oop",
    "name": "OOP",
    "books": [
     {
      "dir": "oop-python",
      "slug": "oop",
      "title": "OOP trong Python",
      "tag": "OOP",
      "blurb": "Bốn trụ OOP mà Python hỗ trợ trực tiếp qua cú pháp: encapsulation, abstraction, inheritance, polymorphism — và MRO khi đa kế thừa.",
      "n": 9,
      "path": "content/02-python/06-oop/oop-python/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "07-typing",
    "name": "Typing",
    "books": [
     {
      "dir": "typing-dataclass",
      "slug": "typing",
      "title": "Type hints & dataclass",
      "tag": "Typing",
      "blurb": "Type hints không đổi runtime nhưng đổi cách team đọc code — Generic, Protocol và dataclass dùng thế nào cho đúng.",
      "n": 8,
      "path": "content/02-python/07-typing/typing-dataclass/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "08-performance",
    "name": "Performance",
    "books": [
     {
      "dir": "performance-profiling",
      "slug": "perf",
      "title": "Profiling & performance",
      "tag": "Performance",
      "blurb": "Đo trước khi tối ưu — cProfile, memory profiler và vì sao vectorize bằng NumPy nhanh hơn vòng lặp Python.",
      "n": 6,
      "path": "content/02-python/08-performance/performance-profiling/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   }
  ]
 },
 {
  "dir": "03-cs-fundamentals",
  "name": "CS fundamentals",
  "note": "Phần chung của một khoá CS: hệ điều hành và mạng. Không phụ thuộc ngôn ngữ nào.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "cs-overview",
      "slug": "csov",
      "title": "CS fundamentals overview",
      "tag": "CS",
      "blurb": "Từ một lệnh gọi hàm tới một request đi qua nửa vòng trái đất — các tầng trừu tượng và tầng nào hỏng thì thấy gì.",
      "n": 3,
      "path": "content/03-cs-fundamentals/01-overview/cs-overview/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-os",
    "name": "Operating system",
    "books": [
     {
      "dir": "os-overview",
      "slug": "osov",
      "title": "Operating system overview",
      "tag": "CS",
      "blurb": "Hệ điều hành chia một máy cho nhiều việc thế nào: tiến trình, bộ nhớ, và đồng bộ.",
      "n": 2,
      "path": "content/03-cs-fundamentals/02-os/os-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "process-thread-scheduling",
      "slug": "osproc",
      "title": "Process, thread & scheduling",
      "tag": "CS",
      "blurb": "Ranh giới cô lập, chi phí context switch, và bộ lập lịch quyết định ai chạy tiếp.",
      "n": 7,
      "path": "content/03-cs-fundamentals/02-os/process-thread-scheduling/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "memory-virtual-paging",
      "slug": "osmem",
      "title": "Virtual memory & paging",
      "tag": "CS",
      "blurb": "Địa chỉ ảo tới địa chỉ vật lý, page fault, và vì sao chương trình tưởng mình có cả bộ nhớ máy.",
      "n": 6,
      "path": "content/03-cs-fundamentals/02-os/memory-virtual-paging/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "lock-deadlock-race",
      "slug": "oslock",
      "title": "Lock, deadlock & race condition",
      "tag": "CS",
      "blurb": "Bốn điều kiện gây deadlock, mutex khác semaphore, và vì sao một phép cộng cũng có thể hỏng.",
      "n": 6,
      "path": "content/03-cs-fundamentals/02-os/lock-deadlock-race/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-networking",
    "name": "Networking",
    "books": [
     {
      "dir": "networking-overview",
      "slug": "netov",
      "title": "Networking overview",
      "tag": "CS",
      "blurb": "Một request đi qua những bước nào, và năm bài của nhóm rút ngắn khúc nào.",
      "n": 2,
      "path": "content/03-cs-fundamentals/03-networking/networking-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "dns-tls",
      "slug": "dnstls",
      "title": "DNS & TLS",
      "tag": "Networking",
      "blurb": "Hai chặng đầu tiên trước khi byte dữ liệu đầu tiên chạy, và chúng tốn bao nhiêu vòng khứ hồi.",
      "n": 6,
      "path": "content/03-cs-fundamentals/03-networking/dns-tls/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "tcp-http",
      "slug": "http",
      "title": "TCP & HTTP",
      "tag": "Networking",
      "blurb": "Đếm vòng khứ hồi, TCP bắt tay, HTTP/1.1 tới HTTP/3, idempotency, backoff có jitter, timeout và circuit breaker.",
      "n": 12,
      "path": "content/03-cs-fundamentals/03-networking/tcp-http/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "caching",
      "slug": "cache",
      "title": "Caching",
      "tag": "Networking",
      "blurb": "Cache HTTP, năm tầng cache, ba chiến lược vô hiệu hoá, thundering herd, và khác biệt giữa no-cache với no-store.",
      "n": 8,
      "path": "content/03-cs-fundamentals/03-networking/caching/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "rest-api-design",
      "slug": "rest",
      "title": "REST API design",
      "tag": "CS",
      "blurb": "Tài nguyên và động từ, mã trạng thái, phân trang, phiên bản, và hợp đồng giữa hai bên.",
      "n": 7,
      "path": "content/03-cs-fundamentals/03-networking/rest-api-design/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "load-balancing",
      "slug": "lb",
      "title": "Load balancing & scaling",
      "tag": "CS",
      "blurb": "Bốn thuật toán phân phối, sticky session, health check, và tầng 4 khác tầng 7 ở đâu.",
      "n": 7,
      "path": "content/03-cs-fundamentals/03-networking/load-balancing/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "04-distributed",
    "name": "Distributed systems",
    "books": [
     {
      "dir": "cap-theorem-consistency",
      "slug": "cap",
      "title": "CAP & consistency",
      "tag": "Distributed",
      "blurb": "Chọn 2 trong 3 không phải luật cứng — CAP thật ra nói gì, và các mức consistency giữa strong và eventual.",
      "n": 8,
      "path": "content/03-cs-fundamentals/04-distributed/cap-theorem-consistency/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "consensus-leader-election",
      "slug": "consensus",
      "title": "Consensus & leader election",
      "tag": "Distributed",
      "blurb": "Nhiều node phải đồng thuận một giá trị dù có node chết — Raft và ZooKeeper giải bài này thế nào, ở mức nhận diện.",
      "n": 5,
      "path": "content/03-cs-fundamentals/04-distributed/consensus-leader-election/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "05-messaging",
    "name": "Messaging",
    "books": [
     {
      "dir": "messaging-queue-pubsub",
      "slug": "mq",
      "title": "Message queue & Pub/Sub",
      "tag": "Messaging",
      "blurb": "Queue và Pub/Sub giải hai bài toán khác nhau — cùng với idempotency và delivery semantics, thứ hay bị hỏi nhất khi có Kafka trong đề.",
      "n": 8,
      "path": "content/03-cs-fundamentals/05-messaging/messaging-queue-pubsub/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   }
  ]
 },
 {
  "dir": "04-database",
  "name": "Database & SQL",
  "note": "Đi từ mô hình quan hệ và ràng buộc, qua SQL nền, rồi mới tới index, transaction và mở rộng. Đừng nhảy cóc.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "db-overview",
      "slug": "dbov",
      "title": "Database overview",
      "tag": "Database",
      "blurb": "Database giải bài toán gì, có mấy loại, và học theo thứ tự nào.",
      "n": 3,
      "path": "content/04-database/01-overview/db-overview/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-relational-basics",
    "name": "Relational foundations",
    "books": [
     {
      "dir": "relational-overview",
      "slug": "relov",
      "title": "Relational foundations overview",
      "tag": "Database",
      "blurb": "Bảng nối nhau bằng khoá thế nào, và bốn bài của nhóm học theo thứ tự nào.",
      "n": 2,
      "path": "content/04-database/02-relational-basics/relational-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "relational-model",
      "slug": "relmodel",
      "title": "Relational model",
      "tag": "Database",
      "blurb": "Bảng, hàng, cột, miền giá trị, khoá chính và khoá ngoại — bộ từ vựng mọi câu hỏi SQL đứng trên.",
      "n": 8,
      "path": "content/04-database/02-relational-basics/relational-model/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "constraints-integrity",
      "slug": "constraint",
      "title": "Constraints & integrity",
      "tag": "Database",
      "blurb": "NOT NULL, UNIQUE, CHECK, DEFAULT, khoá ngoại và hành vi khi xoá — để database tự chặn dữ liệu sai.",
      "n": 7,
      "path": "content/04-database/02-relational-basics/constraints-integrity/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "db-normalization",
      "slug": "norm3",
      "title": "Normalization & denormalization",
      "tag": "Database",
      "blurb": "1NF tới 3NF bằng ví dụ, BCNF khi nào cần, và vì sao hệ thống thật lại cố tình phá chuẩn.",
      "n": 7,
      "path": "content/04-database/02-relational-basics/db-normalization/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "er-modeling",
      "slug": "ermod",
      "title": "Schema design",
      "tag": "Database",
      "blurb": "Từ một đoạn mô tả nghiệp vụ ra sơ đồ thực thể — quan hệ, rồi ra bảng: quan hệ 1-n, n-n, bảng nối.",
      "n": 7,
      "path": "content/04-database/02-relational-basics/er-modeling/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-sql-basics",
    "name": "SQL basics",
    "books": [
     {
      "dir": "sql-basics-overview",
      "slug": "sqlov",
      "title": "SQL basics overview",
      "tag": "Database",
      "blurb": "SQL chạy theo thứ tự nào chứ không theo thứ tự viết, và bốn bài của nhóm.",
      "n": 2,
      "path": "content/04-database/03-sql-basics/sql-basics-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "sql-select-filter",
      "slug": "sqlsel",
      "title": "SELECT, WHERE & ORDER BY",
      "tag": "PostgreSQL",
      "blurb": "Thứ tự thực thi logic của một câu truy vấn — thứ giải thích gần hết lỗi SQL của người mới.",
      "n": 7,
      "path": "content/04-database/03-sql-basics/sql-select-filter/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "sql-join",
      "slug": "sqljoin",
      "title": "JOIN",
      "tag": "PostgreSQL",
      "blurb": "Bốn loại join bằng hình, vì sao join sai làm số hàng phình lên, và self join.",
      "n": 7,
      "path": "content/04-database/03-sql-basics/sql-join/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "sql-group-aggregate",
      "slug": "sqlagg",
      "title": "GROUP BY & aggregate",
      "tag": "PostgreSQL",
      "blurb": "Gom nhóm, WHERE khác HAVING ở đâu, COUNT(*) khác COUNT(cột), và bẫy NULL trong hàm tổng hợp.",
      "n": 7,
      "path": "content/04-database/03-sql-basics/sql-group-aggregate/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "sql-subquery-cte",
      "slug": "sqlcte",
      "title": "Subquery & CTE",
      "tag": "PostgreSQL",
      "blurb": "Truy vấn con tương quan và không tương quan, WITH cho dễ đọc, và CTE đệ quy để duyệt cây.",
      "n": 8,
      "path": "content/04-database/03-sql-basics/sql-subquery-cte/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "04-sql-advanced",
    "name": "SQL advanced",
    "books": [
     {
      "dir": "sql-advanced-overview",
      "slug": "sqladv",
      "title": "SQL advanced overview",
      "tag": "Overview",
      "blurb": "Ba thứ mà cú pháp SQL đúng không cứu được, và bốn bài của nhóm chữa cái nào.",
      "n": 2,
      "path": "content/04-database/04-sql-advanced/sql-advanced-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "sql-window-functions",
      "slug": "sqlwindow",
      "title": "SQL — window functions",
      "tag": "PostgreSQL",
      "blurb": "Khác GROUP BY ở đâu, vì sao WHERE không lọc được, ba hàm xếp hạng, top-N mỗi nhóm, và bẫy frame mặc định.",
      "n": 16,
      "path": "content/04-database/04-sql-advanced/sql-window-functions/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "sql-index-query-plan",
      "slug": "sqlindex",
      "title": "SQL — index & query plan",
      "tag": "PostgreSQL",
      "blurb": "Đọc EXPLAIN, vì sao planner bỏ qua index, leftmost prefix, ba thuật toán join, và bài toán N+1.",
      "n": 15,
      "path": "content/04-database/04-sql-advanced/sql-index-query-plan/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "transaction-isolation",
      "slug": "sqltx",
      "title": "Transaction & isolation level",
      "tag": "PostgreSQL",
      "blurb": "Bốn hiện tượng dị thường, mức nào chặn gì, MVCC, ba cách chữa lost update, deadlock và retry.",
      "n": 16,
      "path": "content/04-database/04-sql-advanced/transaction-isolation/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "query-tuning",
      "slug": "tuning",
      "title": "Query tuning",
      "tag": "PostgreSQL",
      "blurb": "Quy trình khi một truy vấn chậm: đọc plan, tìm chỗ quét toàn bảng, sửa index hay sửa câu lệnh.",
      "n": 9,
      "path": "content/04-database/04-sql-advanced/query-tuning/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "05-beyond-sql",
    "name": "Beyond relational",
    "books": [
     {
      "dir": "nosql-landscape",
      "slug": "nosql",
      "title": "NoSQL — four families",
      "tag": "Database",
      "blurb": "Key-value, document, column-family, graph: mỗi họ bỏ ràng buộc gì của mô hình quan hệ để đổi lấy gì, và khi nào polyglot persistence là hợp lý.",
      "n": 7,
      "path": "content/04-database/05-beyond-sql/nosql-landscape/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "sharding-replication",
      "slug": "shard",
      "title": "Replication & sharding",
      "tag": "Database",
      "blurb": "Bản sao đọc, độ trễ sao chép, ba chiến lược chia mảnh, mảnh nóng, và vì sao join qua nhiều mảnh lại đắt.",
      "n": 8,
      "path": "content/04-database/05-beyond-sql/sharding-replication/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "06-data-systems",
    "name": "Data systems",
    "books": [
     {
      "dir": "oltp-vs-olap",
      "slug": "oltp",
      "title": "OLTP vs OLAP",
      "tag": "Data systems",
      "blurb": "Một hệ tối ưu cho giao dịch, một hệ tối ưu cho phân tích — vì sao không dùng chung một database cho cả hai.",
      "n": 7,
      "path": "content/04-database/06-data-systems/oltp-vs-olap/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "data-warehouse-lake",
      "slug": "dwlake",
      "title": "Data warehouse & data lake",
      "tag": "Data systems",
      "blurb": "Warehouse ép schema trước khi lưu, lake lưu trước hỏi sau — chọn sai thì trả giá ở đâu.",
      "n": 7,
      "path": "content/04-database/06-data-systems/data-warehouse-lake/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "etl-elt",
      "slug": "etl",
      "title": "ETL & ELT",
      "tag": "Data systems",
      "blurb": "Transform trước khi load, hay load trước rồi transform sau — thứ tự đổi vì kho đích đổi từ warehouse sang lake.",
      "n": 7,
      "path": "content/04-database/06-data-systems/etl-elt/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "batch-stream-processing",
      "slug": "batch",
      "title": "Batch vs stream processing",
      "tag": "Data systems",
      "blurb": "Xử lý theo lô định kỳ, hay xử lý từng sự kiện ngay khi tới — độ trễ chấp nhận được quyết định chọn cái nào.",
      "n": 7,
      "path": "content/04-database/06-data-systems/batch-stream-processing/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "data-quality",
      "slug": "dq",
      "title": "Data quality",
      "tag": "Data systems",
      "blurb": "Pipeline chạy không lỗi không có nghĩa dữ liệu đúng — các chiều đo chất lượng và chỗ hay vỡ âm thầm nhất.",
      "n": 7,
      "path": "content/04-database/06-data-systems/data-quality/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   }
  ]
 },
 {
  "dir": "05-machine-learning",
  "name": "Machine learning",
  "note": "Toán và thống kê trước, khái niệm lõi sau, rồi mới tới từng model. Bias–variance là sợi chỉ xuyên suốt cả kệ.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "ml-overview",
      "slug": "mlov",
      "title": "Machine learning overview",
      "tag": "Overview",
      "blurb": "Máy học luật từ ví dụ thay vì được viết luật: ba kiểu bài toán, các họ model, và học theo thứ tự nào.",
      "n": 5,
      "path": "content/05-machine-learning/01-overview/ml-overview/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-math-foundations",
    "name": "Math foundations",
    "books": [
     {
      "dir": "math-foundations-overview",
      "slug": "mathov",
      "title": "Math foundations overview",
      "tag": "Overview",
      "blurb": "Sáu mảnh toán thật sự dùng trong ML, mỗi mảnh trả lời câu hỏi nào và xuất hiện lại ở bài model nào.",
      "n": 3,
      "path": "content/05-machine-learning/02-math-foundations/math-foundations-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "probability-basics",
      "slug": "prob",
      "title": "Probability",
      "tag": "Math",
      "blurb": "Biến ngẫu nhiên, xác suất có điều kiện, độc lập, và các phân phối hay gặp trong ML.",
      "n": 6,
      "path": "content/05-machine-learning/02-math-foundations/probability-basics/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "expectation-variance",
      "slug": "expvar",
      "title": "Expectation & variance",
      "tag": "Math",
      "blurb": "Tuyến tính của kỳ vọng, phương sai của tổng, hiệp phương sai, và luật số lớn với CLT.",
      "n": 6,
      "path": "content/05-machine-learning/02-math-foundations/expectation-variance/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "bayes-theorem",
      "slug": "bayes",
      "title": "Bayes' theorem",
      "tag": "Math",
      "blurb": "Tiên nghiệm, khả năng, hậu nghiệm; nghịch lý xét nghiệm y tế; và Bayes trong Naive Bayes.",
      "n": 5,
      "path": "content/05-machine-learning/02-math-foundations/bayes-theorem/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "linear-algebra-ml",
      "slug": "linalg",
      "title": "Linear algebra for ML",
      "tag": "Math",
      "blurb": "Vector, ma trận, nhân ma trận đọc thế nào, hạng, eigenvalue và eigenvector — chỉ phần thật sự dùng.",
      "n": 6,
      "path": "content/05-machine-learning/02-math-foundations/linear-algebra-ml/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "gradient-optimization",
      "slug": "grad",
      "title": "Gradient & optimization",
      "tag": "Math",
      "blurb": "Đạo hàm riêng, gradient chỉ hướng nào, quy tắc chuỗi, hàm lồi, và gradient descent hội tụ ra sao.",
      "n": 6,
      "path": "content/05-machine-learning/02-math-foundations/gradient-optimization/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "mle-map",
      "slug": "mle",
      "title": "MLE & MAP",
      "tag": "Math",
      "blurb": "Vì sao chọn loss function chính là chọn giả định phân phối, và regularization chính là tiên nghiệm.",
      "n": 7,
      "path": "content/05-machine-learning/02-math-foundations/mle-map/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-statistics",
    "name": "Statistics & experimentation",
    "books": [
     {
      "dir": "statistics",
      "slug": "stats",
      "title": "Statistics",
      "tag": "Statistics",
      "blurb": "Định nghĩa chính xác của p-value, bốn đại lượng gắn nhau, sample size và power, confidence interval, so sánh nhiều lần, và tương quan với nhân quả.",
      "n": 11,
      "path": "content/05-machine-learning/03-statistics/statistics/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "ab-testing",
      "slug": "abtest",
      "title": "A/B testing",
      "tag": "Statistics",
      "blurb": "Thiết kế thí nghiệm, vấn đề nhìn sớm, năm cái bẫy thực tế, ý nghĩa thống kê so với ý nghĩa thực tiễn, và checklist trước khi triển khai.",
      "n": 9,
      "path": "content/05-machine-learning/03-statistics/ab-testing/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "04-core-concepts",
    "name": "Core concepts",
    "books": [
     {
      "dir": "core-concepts-overview",
      "slug": "ccov",
      "title": "Core concepts overview",
      "tag": "Overview",
      "blurb": "Năm khái niệm dùng lại ở mọi model: gọi tên bài toán, phân rã sai số, chia dữ liệu, chống quá khớp, chuẩn bị đặc trưng.",
      "n": 3,
      "path": "content/05-machine-learning/04-core-concepts/core-concepts-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "supervised-unsupervised",
      "slug": "para",
      "title": "Supervised, unsupervised & reinforcement",
      "tag": "ML",
      "blurb": "Gọi tên bài toán cho đúng: nhãn tới từ đâu, khi nào hồi quy khi nào phân loại, và bốn cách xoay xở khi nhãn quá đắt.",
      "n": 6,
      "path": "content/05-machine-learning/04-core-concepts/supervised-unsupervised/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "bias-variance-tradeoff",
      "slug": "bv",
      "title": "Bias–variance tradeoff",
      "tag": "Generalization",
      "blurb": "Phân rã sai số thành ba phần, đường cong đánh đổi, và kỹ thuật nào đánh vào phần nào.",
      "n": 8,
      "path": "content/05-machine-learning/04-core-concepts/bias-variance-tradeoff/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "train-val-test-cv",
      "slug": "cv",
      "title": "Train/val/test & cross-validation",
      "tag": "Generalization",
      "blurb": "Vì sao cần ba tập, k-fold, chia theo nhóm và theo thời gian, sáu nguồn rò rỉ dữ liệu, và nested CV.",
      "n": 9,
      "path": "content/05-machine-learning/04-core-concepts/train-val-test-cv/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "overfitting-regularization",
      "slug": "overfit",
      "title": "Overfitting & regularization",
      "tag": "Generalization",
      "blurb": "Chẩn đoán bằng số, đọc learning curve để biết có nên thêm dữ liệu, các cách regularize, và vì sao random search thắng grid.",
      "n": 8,
      "path": "content/05-machine-learning/04-core-concepts/overfitting-regularization/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "feature-engineering",
      "slug": "feat",
      "title": "Feature engineering",
      "tag": "ML",
      "blurb": "Mã hoá biến phân loại, xử lý giá trị thiếu, co giãn, biến tương tác — và khi nào để model tự lo.",
      "n": 7,
      "path": "content/05-machine-learning/04-core-concepts/feature-engineering/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "05-classical-ml",
    "name": "Classical models",
    "books": [
     {
      "dir": "classical-models-overview",
      "slug": "clsov",
      "title": "Classical models overview",
      "tag": "Overview",
      "blurb": "Sáu model kinh điển trên một bảng: mỗi cái giả định một hình dạng khác nhau cho dữ liệu, và giả định đó quyết định khi nào chọn cái nào.",
      "n": 3,
      "path": "content/05-machine-learning/05-classical-ml/classical-models-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "linear-regression",
      "slug": "linreg",
      "title": "Linear regression",
      "tag": "ML",
      "blurb": "MSE hay MAE, nghiệm đóng hay gradient descent, bốn giả định, đa cộng tuyến và Ridge/Lasso.",
      "n": 10,
      "path": "content/05-machine-learning/05-classical-ml/linear-regression/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "logistic-regression",
      "slug": "logreg",
      "title": "Logistic regression",
      "tag": "ML",
      "blurb": "Vì sao log loss chứ không phải MSE, cách đọc odds ratio, ngưỡng quyết định, và vì sao vẫn là baseline.",
      "n": 10,
      "path": "content/05-machine-learning/05-classical-ml/logistic-regression/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "ridge-lasso-elasticnet",
      "slug": "ridge",
      "title": "Ridge, Lasso & Elastic Net",
      "tag": "ML",
      "blurb": "Ba cách regularize model tuyến tính: L2 co hệ số về gần 0, L1 đưa về đúng 0, Elastic Net gộp cả hai — khác nhau ở hình dạng vùng phạt.",
      "n": 8,
      "path": "content/05-machine-learning/05-classical-ml/ridge-lasso-elasticnet/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "svm",
      "slug": "svm",
      "title": "SVM",
      "tag": "ML",
      "blurb": "Lề lớn nhất, support vector, tham số C và gamma, kernel trick — và vì sao nó từng thắng trước khi deep learning tới.",
      "n": 8,
      "path": "content/05-machine-learning/05-classical-ml/svm/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "knn",
      "slug": "knn",
      "title": "KNN",
      "tag": "ML",
      "blurb": "Không huấn luyện gì cả, chỉ nhớ dữ liệu: chọn k, đo khoảng cách, và vì sao mọi thứ sụp đổ khi số chiều tăng.",
      "n": 7,
      "path": "content/05-machine-learning/05-classical-ml/knn/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "naive-bayes",
      "slug": "nb",
      "title": "Naive Bayes",
      "tag": "ML",
      "blurb": "Từ định lý Bayes ra bộ phân loại: giả định độc lập sai rõ ràng nhưng vẫn chạy tốt, làm mượt Laplace, và ba biến thể.",
      "n": 7,
      "path": "content/05-machine-learning/05-classical-ml/naive-bayes/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "06-tree-models",
    "name": "Tree models",
    "books": [
     {
      "dir": "tree-family-overview",
      "slug": "treeintro",
      "title": "Tree models overview",
      "tag": "Overview",
      "blurb": "Bài đầu tiên của nhánh: người ta đang cố giải quyết vấn đề gì, lịch sử 40 năm của nhánh này, hai hướng bagging và boosting, và học theo thứ tự nào.",
      "n": 9,
      "path": "content/05-machine-learning/06-tree-models/tree-family-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "decision-tree",
      "slug": "dtree",
      "title": "Decision tree",
      "tag": "ML",
      "blurb": "Đọc một cây, máy chọn câu hỏi ra sao, Gini và information gain, vì sao cây học thuộc dữ liệu, và ba hyperparameter để hãm nó lại.",
      "n": 14,
      "path": "content/05-machine-learning/06-tree-models/decision-tree/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "random-forest",
      "slug": "rf",
      "title": "Random forest & bagging",
      "tag": "Ensemble",
      "blurb": "Hỏi một cây thì hay sai — random forest trồng hàng trăm cây rồi cho bỏ phiếu. Ba bước của thuật toán, vì sao nó chạy được, và cái bẫy của bảng feature importance.",
      "n": 13,
      "path": "content/05-machine-learning/06-tree-models/random-forest/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "gradient-boosting",
      "slug": "gb",
      "title": "Gradient boosting",
      "tag": "Ensemble",
      "blurb": "Cộng cây nông theo phần dư, vì sao gọi là gradient, learning_rate bù trừ với n_estimators, và vì sao dữ liệu bảng vẫn thuộc về boosting.",
      "n": 10,
      "path": "content/05-machine-learning/06-tree-models/gradient-boosting/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "xgboost",
      "slug": "xgb",
      "title": "XGBoost",
      "tag": "Ensemble",
      "blurb": "Xấp xỉ Taylor bậc hai cho công thức điểm lá tính thẳng, số hạng phạt nằm trong objective, và cách nó xử lý dữ liệu thưa.",
      "n": 8,
      "path": "content/05-machine-learning/06-tree-models/xgboost/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "lightgbm",
      "slug": "lgbm",
      "title": "LightGBM",
      "tag": "Ensemble",
      "blurb": "Mọc cây theo lá thay vì theo tầng, GOSS bỏ bớt mẫu gradient nhỏ, EFB gộp đặc trưng thưa — ba mẹo đổi lấy tốc độ.",
      "n": 7,
      "path": "content/05-machine-learning/06-tree-models/lightgbm/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "07-clustering",
    "name": "Clustering",
    "books": [
     {
      "dir": "clustering-overview",
      "slug": "clov",
      "title": "Clustering overview",
      "tag": "Overview",
      "blurb": "Bốn họ phân cụm — theo tâm, theo mật độ, theo tầng, theo phân phối — cụm hình gì thì họ nào bắt được, và chấm điểm bằng gì khi không có đáp án.",
      "n": 4,
      "path": "content/05-machine-learning/07-clustering/clustering-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "kmeans-clustering",
      "slug": "kmeans",
      "title": "K-means & clustering",
      "tag": "ML",
      "blurb": "Lặp hai bước quanh k tâm, chọn k bằng elbow và silhouette, và bốn giả định ngầm khiến nó chia sai khi cụm không tròn.",
      "n": 7,
      "path": "content/05-machine-learning/07-clustering/kmeans-clustering/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "dbscan",
      "slug": "dbscan",
      "title": "DBSCAN",
      "tag": "ML",
      "blurb": "Cụm là vùng đông đúc nối nhau: không cần biết k trước, bắt được cụm hình bất kỳ, và tự đánh dấu điểm nhiễu.",
      "n": 9,
      "path": "content/05-machine-learning/07-clustering/dbscan/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "hdbscan",
      "slug": "hdb",
      "title": "HDBSCAN",
      "tag": "ML",
      "blurb": "Chạy DBSCAN ở mọi mức eps cùng lúc, dựng cây phân cấp rồi giữ lại cụm nào bền nhất — bỏ được tham số khó chọn nhất.",
      "n": 8,
      "path": "content/05-machine-learning/07-clustering/hdbscan/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "08-dimensionality",
    "name": "Dimensionality reduction",
    "books": [
     {
      "dir": "pca-dimensionality",
      "slug": "pca",
      "title": "PCA & dimensionality reduction",
      "tag": "ML",
      "blurb": "Xoay trục về hướng dữ liệu trải rộng nhất rồi bỏ bớt hướng: chọn số thành phần, vì sao phải chuẩn hoá, và vì sao nó không phải chọn đặc trưng.",
      "n": 7,
      "path": "content/05-machine-learning/08-dimensionality/pca-dimensionality/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "09-evaluation",
    "name": "Model evaluation",
    "books": [
     {
      "dir": "evaluation-overview",
      "slug": "evov",
      "title": "Model evaluation overview",
      "tag": "Overview",
      "blurb": "Ba câu hỏi độc lập về một model — xếp hạng, quyết định, xác suất — và bảng tra chọn metric theo bài toán và theo tỉ lệ lớp.",
      "n": 3,
      "path": "content/05-machine-learning/09-evaluation/evaluation-overview/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "metrics-confusion-matrix",
      "slug": "metrics",
      "title": "Metric & confusion matrix",
      "tag": "Evaluation",
      "blurb": "Bốn ô sinh ra mọi chỉ số: precision với recall chọn theo chi phí lỗi, vì sao accuracy nói dối khi dữ liệu lệch, và chốt ngưỡng bằng tiền thay vì bằng F1.",
      "n": 13,
      "path": "content/05-machine-learning/09-evaluation/metrics-confusion-matrix/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "roc-auc-pr",
      "slug": "roc",
      "title": "ROC-AUC & PR curve",
      "tag": "Evaluation",
      "blurb": "Hai đường cong khi ngưỡng chưa cố định: ý nghĩa xác suất của AUC, vì sao lớp dương hiếm thì ROC nói dối, và mức cơ sở của PR-AUC không phải 0.5.",
      "n": 7,
      "path": "content/05-machine-learning/09-evaluation/roc-auc-pr/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "calibration",
      "slug": "calib",
      "title": "Probability calibration",
      "tag": "Evaluation",
      "blurb": "Model xếp hạng đúng vẫn có thể nói 0.9 khi thực tế là 0.6: biểu đồ tin cậy, model nào lệch sẵn, Platt scaling và isotonic regression.",
      "n": 8,
      "path": "content/05-machine-learning/09-evaluation/calibration/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   }
  ]
 },
 {
  "dir": "06-deep-learning",
  "name": "Deep learning",
  "note": "Từ perceptron tới mạng sâu. Mỗi kỹ thuật ở đây sinh ra để chữa một chỗ hỏng cụ thể khi mạng sâu dần.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "dl-overview",
      "slug": "dlov",
      "title": "Deep learning overview",
      "tag": "DL",
      "blurb": "Perceptron 1958 → mùa đông AI → backpropagation → 2012 AlexNet → Transformer: mỗi mốc gỡ đúng một nút thắt.",
      "n": 8,
      "path": "content/06-deep-learning/01-overview/dl-overview/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-neural-network",
    "name": "Neural network",
    "books": [
     {
      "dir": "neural-network-overview",
      "slug": "nnov",
      "title": "Neural network overview",
      "tag": "DL",
      "blurb": "Sáu thứ phải có để một mạng sâu học được, và mỗi thứ chữa đúng một chỗ hỏng khi mạng sâu dần.",
      "n": 8,
      "path": "content/06-deep-learning/02-neural-network/neural-network-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "perceptron-mlp",
      "slug": "mlp",
      "title": "Perceptron & MLP",
      "tag": "DL",
      "blurb": "Một nơ-ron làm gì, vì sao XOR giết chết perceptron, và thêm một lớp ẩn thì thay đổi cái gì.",
      "n": 5,
      "path": "content/06-deep-learning/02-neural-network/perceptron-mlp/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "activation-functions",
      "slug": "act",
      "title": "Activation functions",
      "tag": "DL",
      "blurb": "Sigmoid, tanh, ReLU và họ hàng: vì sao ReLU thắng, vấn đề nơ-ron chết, và GELU trong Transformer.",
      "n": 5,
      "path": "content/06-deep-learning/02-neural-network/activation-functions/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "backpropagation",
      "slug": "backprop",
      "title": "Backpropagation",
      "tag": "Gradient",
      "blurb": "Mạng 2-2-1 với số thật, vì sao softmax + CE cho gradient p − y, gradient teo và nổ, và checklist debug.",
      "n": 15,
      "path": "content/06-deep-learning/02-neural-network/backpropagation/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "weight-initialization",
      "slug": "init",
      "title": "Weight initialization",
      "tag": "Foundations",
      "blurb": "Vì sao công thức có căn 1/n, Xavier so với He, và vì sao khởi tạo bằng 0 thì mạng không học được gì.",
      "n": 7,
      "path": "content/06-deep-learning/02-neural-network/weight-initialization/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "normalization",
      "slug": "norm",
      "title": "Normalization — BatchNorm & LayerNorm",
      "tag": "Foundations",
      "blurb": "BatchNorm phụ thuộc batch size ra sao, vì sao Transformer dùng LayerNorm, Pre-LN so với Post-LN, và cách chẩn đoán bằng thống kê activation.",
      "n": 11,
      "path": "content/06-deep-learning/02-neural-network/normalization/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "optimizer-sgd-adam",
      "slug": "optim",
      "title": "Optimizer — SGD tới Adam",
      "tag": "DL",
      "blurb": "Momentum, learning rate thích ứng, Adam ghép hai thứ đó, và vì sao AdamW mới là mặc định.",
      "n": 6,
      "path": "content/06-deep-learning/02-neural-network/optimizer-sgd-adam/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "dropout-regularization",
      "slug": "drop",
      "title": "Dropout & regularization",
      "tag": "DL",
      "blurb": "Dropout làm gì lúc huấn luyện và lúc suy luận, early stopping, data augmentation, và weight decay.",
      "n": 5,
      "path": "content/06-deep-learning/02-neural-network/dropout-regularization/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-cnn",
    "name": "Computer vision",
    "books": [
     {
      "dir": "convolution-basics",
      "slug": "conv",
      "title": "Convolution",
      "tag": "DL",
      "blurb": "Kernel, stride, padding, receptive field, và vì sao chia sẻ trọng số làm giảm tham số hàng nghìn lần.",
      "n": 5,
      "path": "content/06-deep-learning/03-cnn/convolution-basics/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "cnn-mobilenet",
      "slug": "cnn",
      "title": "CNN & MobileNet",
      "tag": "Computer vision",
      "blurb": "Công thức shape và chi phí, vì sao depthwise separable rẻ 8–9 lần, inverted residual, linear bottleneck, lượng tử hoá.",
      "n": 15,
      "path": "content/06-deep-learning/03-cnn/cnn-mobilenet/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "04-sequence",
    "name": "Sequence models",
    "books": [
     {
      "dir": "rnn",
      "slug": "rnn",
      "title": "RNN",
      "tag": "DL",
      "blurb": "Trạng thái ẩn, chia sẻ trọng số qua thời gian, và vì sao gradient tắt dần trên chuỗi dài.",
      "n": 8,
      "path": "content/06-deep-learning/04-sequence/rnn/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "lstm-gru",
      "slug": "lstm",
      "title": "LSTM & GRU",
      "tag": "DL",
      "blurb": "Cổng và đường trạng thái chữa gradient tắt dần thế nào; GRU gọn hơn mà gần bằng.",
      "n": 8,
      "path": "content/06-deep-learning/04-sequence/lstm-gru/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "05-training",
    "name": "Training",
    "books": [
     {
      "dir": "training-recipe",
      "slug": "recipe",
      "title": "Training recipe",
      "tag": "DL",
      "blurb": "Learning rate schedule, warmup, batch size, gradient clipping, mixed precision — bộ núm cần biết.",
      "n": 5,
      "path": "content/06-deep-learning/05-training/training-recipe/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "debug-training",
      "slug": "dbg",
      "title": "Debugging training",
      "tag": "DL",
      "blurb": "Quy trình theo thứ tự khi loss không giảm, thành NaN, hay chỉ tốt trên tập huấn luyện.",
      "n": 5,
      "path": "content/06-deep-learning/05-training/debug-training/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "06-generative",
    "name": "Generative models",
    "books": [
     {
      "dir": "autoencoder",
      "slug": "ae",
      "title": "Autoencoder",
      "tag": "DL",
      "blurb": "Nén rồi khôi phục để học representation — bước đệm dẫn tới VAE, không phải mô hình sinh thật sự.",
      "n": 5,
      "path": "content/06-deep-learning/06-generative/autoencoder/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "vae",
      "slug": "vae",
      "title": "VAE — Variational autoencoder",
      "tag": "DL",
      "blurb": "Ép latent space có phân phối biết trước để sinh được mẫu mới — và vì sao ảnh VAE sinh ra thường mờ hơn diffusion.",
      "n": 6,
      "path": "content/06-deep-learning/06-generative/vae/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "gan",
      "slug": "gan",
      "title": "GAN",
      "tag": "DL",
      "blurb": "Hai mạng đấu nhau tới khi generator giả không phân biệt được — nhận diện ý tưởng, không đào sâu vì diffusion đã thay thế ở hầu hết ứng dụng.",
      "n": 4,
      "path": "content/06-deep-learning/06-generative/gan/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   }
  ]
 },
 {
  "dir": "07-transformer",
  "name": "Transformer & architectures",
  "note": "Nhánh tiếp nối Deep learning — vẫn là mạng học bằng gradient, chỉ đổi cách các lớp nói chuyện với nhau.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "architecture-overview",
      "slug": "arcov",
      "title": "Architecture overview",
      "tag": "Transformer",
      "blurb": "Từ RNN tới attention tới SSM: mỗi kiến trúc gỡ được nút thắt nào của kiến trúc trước.",
      "n": 8,
      "path": "content/07-transformer/01-overview/architecture-overview/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-transformer-core",
    "name": "Transformer core",
    "books": [
     {
      "dir": "transformer-core-overview",
      "slug": "tcov",
      "title": "Transformer core overview",
      "tag": "Transformer",
      "blurb": "Năm mảnh ghép của một Transformer và thứ tự dữ liệu đi qua chúng.",
      "n": 8,
      "path": "content/07-transformer/02-transformer-core/transformer-core-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "tokenization",
      "slug": "tok",
      "title": "Tokenization",
      "tag": "LLM",
      "blurb": "BPE hoạt động thế nào, vì sao tiếng Việt tốn nhiều token hơn, và token quyết định chi phí ra sao.",
      "n": 5,
      "path": "content/07-transformer/02-transformer-core/tokenization/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "embedding",
      "slug": "emb",
      "title": "Embedding",
      "tag": "LLM",
      "blurb": "Từ id token tới vector, vì sao khoảng cách trong không gian đó mang nghĩa, và embedding cho tra cứu.",
      "n": 5,
      "path": "content/07-transformer/02-transformer-core/embedding/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "positional-encoding",
      "slug": "pos",
      "title": "Positional encoding",
      "tag": "LLM",
      "blurb": "Vì sao attention mù thứ tự, sin/cos, học được, và RoPE — thứ mọi model hiện nay dùng.",
      "n": 5,
      "path": "content/07-transformer/02-transformer-core/positional-encoding/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "self-attention",
      "slug": "attn",
      "title": "Self-attention",
      "tag": "Transformer",
      "blurb": "Q/K/V là gì, vì sao chia căn d_k, hai loại mask đừng nhầm, multi-head, complexity bậc hai, và KV cache quyết định chi phí phục vụ.",
      "n": 13,
      "path": "content/07-transformer/02-transformer-core/self-attention/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "transformer-architecture",
      "slug": "tfm",
      "title": "Transformer architecture",
      "tag": "Transformer",
      "blurb": "Tokenization, embedding, positional encoding, residual và LayerNorm, FFN chứa phần lớn tham số, một block hoàn chỉnh, và encoder hay decoder.",
      "n": 12,
      "path": "content/07-transformer/02-transformer-core/transformer-architecture/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-model-families",
    "name": "Model families",
    "books": [
     {
      "dir": "families-overview",
      "slug": "famov",
      "title": "Encoder, decoder & both",
      "tag": "Transformer",
      "blurb": "Cùng một khối Transformer, ba cách xếp — và mỗi cách hợp với loại tác vụ nào.",
      "n": 8,
      "path": "content/07-transformer/03-model-families/families-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "bert",
      "slug": "bert",
      "title": "BERT — encoder-only",
      "tag": "Transformer",
      "blurb": "Masked language modelling, attention hai chiều, và vì sao BERT không sinh chữ được.",
      "n": 8,
      "path": "content/07-transformer/03-model-families/bert/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "gpt",
      "slug": "gpt",
      "title": "GPT — decoder-only",
      "tag": "Transformer",
      "blurb": "Causal mask, dự đoán token kế tiếp, và vì sao kiến trúc đơn giản nhất lại thắng khi scale.",
      "n": 8,
      "path": "content/07-transformer/03-model-families/gpt/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "encoder-decoder",
      "slug": "encdec",
      "title": "T5 — encoder-decoder",
      "tag": "Transformer",
      "blurb": "Cross-attention nối hai nửa, và vì sao dạng này vẫn thắng ở dịch máy và tóm tắt.",
      "n": 8,
      "path": "content/07-transformer/03-model-families/encoder-decoder/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "04-beyond-transformer",
    "name": "Beyond Transformer",
    "books": [
     {
      "dir": "beyond-overview",
      "slug": "btov",
      "title": "Beyond Transformer overview",
      "tag": "Transformer",
      "blurb": "Attention tốn bậc hai theo độ dài — ba hướng thoát và hướng nào đang thắng.",
      "n": 8,
      "path": "content/07-transformer/04-beyond-transformer/beyond-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "ssm",
      "slug": "ssm",
      "title": "State space models",
      "tag": "Transformer",
      "blurb": "Từ phương trình trạng thái tới S4: tuyến tính theo độ dài chuỗi, và huấn luyện song song được.",
      "n": 8,
      "path": "content/07-transformer/04-beyond-transformer/ssm/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "mamba",
      "slug": "mamba",
      "title": "Mamba",
      "tag": "Transformer",
      "blurb": "Selective SSM: cho tham số phụ thuộc đầu vào, cộng một thuật toán quét nhận biết phần cứng.",
      "n": 8,
      "path": "content/07-transformer/04-beyond-transformer/mamba/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "hybrid-hymba",
      "slug": "hymba",
      "title": "Hybrid — Hymba",
      "tag": "Transformer",
      "blurb": "Ghép head attention và head SSM song song trong cùng một lớp, cộng meta token.",
      "n": 8,
      "path": "content/07-transformer/04-beyond-transformer/hybrid-hymba/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "05-efficient",
    "name": "Efficient architectures",
    "books": [
     {
      "dir": "efficient-attention",
      "slug": "effattn",
      "title": "Efficient attention",
      "tag": "Transformer",
      "blurb": "Attention chuẩn tốn O(n²) bộ nhớ — FlashAttention không đổi kết quả, chỉ đổi cách tính; sparse/linear attention đổi cả công thức.",
      "n": 6,
      "path": "content/07-transformer/05-efficient/efficient-attention/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   }
  ]
 },
 {
  "dir": "08-llm",
  "name": "LLM & GenAI",
  "note": "Kỹ thuật trước, model sau. Học hết phần kỹ thuật rồi tới bài model là ráp lại chứ không phải học mới.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "llm-overview",
      "slug": "llmov",
      "title": "LLM overview",
      "tag": "LLM",
      "blurb": "Từ word2vec tới GPT tới model có suy luận: mỗi bước mở khoá được gì, và vòng đời một model từ pretrain tới phục vụ.",
      "n": 8,
      "path": "content/08-llm/01-overview/llm-overview/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-training",
    "name": "Training",
    "books": [
     {
      "dir": "training-overview",
      "slug": "trov",
      "title": "LLM training overview",
      "tag": "LLM",
      "blurb": "Bốn giai đoạn từ dữ liệu thô tới model biết nghe lời, và mỗi giai đoạn tốn bao nhiêu.",
      "n": 8,
      "path": "content/08-llm/02-training/training-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "pretraining",
      "slug": "pre",
      "title": "Pretraining",
      "tag": "LLM",
      "blurb": "Mục tiêu dự đoán token kế, dữ liệu và cách lọc, scaling law, và vì sao pretrain đắt tới vậy.",
      "n": 5,
      "path": "content/08-llm/02-training/pretraining/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "scaling-law",
      "slug": "scale",
      "title": "Scaling law",
      "tag": "LLM",
      "blurb": "Quan hệ giữa tham số, dữ liệu và tính toán; Chinchilla đổi cách chia ngân sách thế nào.",
      "n": 8,
      "path": "content/08-llm/02-training/scaling-law/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "sft-alignment",
      "slug": "sft",
      "title": "SFT & alignment",
      "tag": "LLM",
      "blurb": "Khi nào fine-tune thay vì RAG, che mất mát trên prompt, RLHF ba bước, DPO bỏ hẳn reward model, và cách đánh giá sau fine-tune.",
      "n": 11,
      "path": "content/08-llm/02-training/sft-alignment/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "peft-lora-qlora",
      "slug": "lora",
      "title": "PEFT — LoRA & QLoRA",
      "tag": "LLM",
      "blurb": "Vì sao ma trận hạng thấp đủ dùng, chọn r và alpha thế nào, QLoRA nén 4-bit ra sao, và LoRA giảm quên kiến thức cũ tới đâu.",
      "n": 7,
      "path": "content/08-llm/02-training/peft-lora-qlora/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-techniques",
    "name": "Techniques",
    "books": [
     {
      "dir": "techniques-overview",
      "slug": "tqov",
      "title": "LLM techniques overview",
      "tag": "LLM",
      "blurb": "Ba nhóm kỹ thuật làm model rẻ hơn, nhớ xa hơn, và suy luận tốt hơn — kỹ thuật nào ở model nào.",
      "n": 8,
      "path": "content/08-llm/03-techniques/techniques-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "moe",
      "slug": "moe",
      "title": "Mixture of Experts",
      "tag": "LLM",
      "blurb": "Router chọn vài expert cho mỗi token: nhiều tham số mà chi phí mỗi token gần như không đổi.",
      "n": 8,
      "path": "content/08-llm/03-techniques/moe/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "long-context",
      "slug": "lctx",
      "title": "Long context",
      "tag": "LLM",
      "blurb": "Vì sao context dài đắt, và bốn hướng chữa: nội suy vị trí, attention thưa, FlashAttention, nén KV.",
      "n": 8,
      "path": "content/08-llm/03-techniques/long-context/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "chain-of-thought",
      "slug": "cot",
      "title": "Chain-of-Thought",
      "tag": "LLM",
      "blurb": "Bắt model viết ra các bước trung gian, self-consistency, và ranh giới giữa prompting và huấn luyện suy luận.",
      "n": 8,
      "path": "content/08-llm/03-techniques/chain-of-thought/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "04-inference",
    "name": "Inference & serving",
    "books": [
     {
      "dir": "inference-overview",
      "slug": "infov",
      "title": "Inference overview",
      "tag": "LLM",
      "blurb": "Chi phí phục vụ nằm ở đâu, và ba nhóm đòn bẩy: giảm bit, giảm bước, giảm bộ nhớ.",
      "n": 8,
      "path": "content/08-llm/04-inference/inference-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "decoding-strategies",
      "slug": "dec",
      "title": "Decoding strategies",
      "tag": "LLM",
      "blurb": "Greedy, beam search, temperature, top-k và top-p — mỗi núm đổi cái gì lấy cái gì.",
      "n": 6,
      "path": "content/08-llm/04-inference/decoding-strategies/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "quantization",
      "slug": "quant",
      "title": "Quantization",
      "tag": "LLM",
      "blurb": "INT8, NF4, sau huấn luyện hay lúc huấn luyện, và mất chất lượng bao nhiêu để đổi lấy bao nhiêu VRAM.",
      "n": 5,
      "path": "content/08-llm/04-inference/quantization/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "inference-optimization",
      "slug": "inference",
      "title": "Inference & cost optimization",
      "tag": "Operations",
      "blurb": "Prefill so với decode, tính KV cache, GQA, continuous batching, speculative decoding, bảng giảm chi phí.",
      "n": 15,
      "path": "content/08-llm/04-inference/inference-optimization/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "05-rag",
    "name": "RAG",
    "books": [
     {
      "dir": "rag-overview",
      "slug": "ragov",
      "title": "RAG overview",
      "tag": "LLM",
      "blurb": "Bốn bước của một hệ RAG, chỗ nào hay hỏng nhất, và khi nào RAG thắng fine-tune.",
      "n": 8,
      "path": "content/08-llm/05-rag/rag-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "rag-end-to-end",
      "slug": "rag",
      "title": "RAG end-to-end",
      "tag": "Retrieval",
      "blurb": "Chunking, hybrid search, reranking, lost-in-the-middle, cây debug năm bước và cách đánh giá tách hai tầng.",
      "n": 15,
      "path": "content/08-llm/05-rag/rag-end-to-end/index.html",
      "skeleton": false,
      "lc": 0
     },
     {
      "dir": "chunking-strategy",
      "slug": "chunk",
      "title": "Chunking strategy",
      "tag": "LLM",
      "blurb": "Kích thước đoạn, chồng lấn, chia theo cấu trúc, và vì sao chia sai thì mọi bước sau vô nghĩa.",
      "n": 5,
      "path": "content/08-llm/05-rag/chunking-strategy/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "vector-database",
      "slug": "vdb",
      "title": "Vector database",
      "tag": "LLM",
      "blurb": "Tìm láng giềng gần đúng, HNSW và IVF, lọc kết hợp metadata, và khi nào chưa cần vector DB.",
      "n": 6,
      "path": "content/08-llm/05-rag/vector-database/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "reranking",
      "slug": "rerank",
      "title": "Reranking & hybrid search",
      "tag": "LLM",
      "blurb": "Bi-encoder khác cross-encoder, BM25 ghép với vector, và vì sao thêm một bước xếp lại rẻ mà lãi.",
      "n": 5,
      "path": "content/08-llm/05-rag/reranking/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "06-agents",
    "name": "Agents",
    "books": [
     {
      "dir": "agent-tool-use",
      "slug": "agent",
      "title": "Agent & tool use",
      "tag": "LLM",
      "blurb": "Vòng lặp suy nghĩ–hành động–quan sát, mô tả công cụ, quản lý ngữ cảnh, và vì sao agent hay chạy vòng vô tận.",
      "n": 5,
      "path": "content/08-llm/06-agents/agent-tool-use/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "07-model-labs",
    "name": "Model labs",
    "books": [
     {
      "dir": "model-labs-overview",
      "slug": "labov",
      "title": "Model labs overview",
      "tag": "LLM",
      "blurb": "Bảng tra ngược: model nào của lab nào dùng kỹ thuật nào, và lab nào công bố đủ để học được kiến trúc.",
      "n": 8,
      "path": "content/08-llm/07-model-labs/model-labs-overview/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "llama",
      "slug": "llama",
      "title": "LLaMA",
      "tag": "LLM",
      "blurb": "Model mở đặt chuẩn cho cả ngành: RMSNorm, SwiGLU, RoPE, GQA — và bài học Chinchilla.",
      "n": 7,
      "path": "content/08-llm/07-model-labs/llama/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "qwen",
      "slug": "qwen",
      "title": "Qwen",
      "tag": "LLM",
      "blurb": "Dòng model mở của Alibaba: đa ngôn ngữ, bản MoE, và hệ sinh thái model theo kích thước.",
      "n": 7,
      "path": "content/08-llm/07-model-labs/qwen/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "deepseek",
      "slug": "dsk",
      "title": "DeepSeek",
      "tag": "LLM",
      "blurb": "MLA nén KV cache, MoE tỉ lệ kích hoạt rất thấp, và GRPO huấn luyện suy luận bằng RL.",
      "n": 7,
      "path": "content/08-llm/07-model-labs/deepseek/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "mixtral",
      "slug": "mixtral",
      "title": "Mistral & Mixtral",
      "tag": "LLM",
      "blurb": "Sliding window attention và bản MoE thưa đầu tiên được mở trọng số ở quy mô lớn.",
      "n": 7,
      "path": "content/08-llm/07-model-labs/mixtral/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "closed-models",
      "slug": "closed",
      "title": "GPT, Claude & Gemini",
      "tag": "LLM",
      "blurb": "Ba dòng model đóng: học được gì từ system card, và chỗ nào bắt buộc phải dừng ở suy đoán.",
      "n": 6,
      "path": "content/08-llm/07-model-labs/closed-models/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "08-rag-evaluation",
    "name": "RAG evaluation",
    "books": [
     {
      "dir": "rag-evaluation",
      "slug": "rageval",
      "title": "Đo một hệ RAG",
      "tag": "Retrieval",
      "blurb": "Retrieval đúng không có nghĩa câu trả lời đúng — Recall@K đo retrieval, faithfulness đo answer, hai lớp đo khác nhau hoàn toàn.",
      "n": 6,
      "path": "content/08-llm/08-rag-evaluation/rag-evaluation/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "09-multimodal",
    "name": "Multimodal",
    "books": [
     {
      "dir": "clip",
      "slug": "clip",
      "title": "CLIP",
      "tag": "Multimodal",
      "blurb": "Học chung một không gian embedding cho ảnh và chữ bằng contrastive loss — nền cho hầu hết mô hình multimodal sau này.",
      "n": 5,
      "path": "content/08-llm/09-multimodal/clip/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "vlm",
      "slug": "vlm",
      "title": "Vision-language model",
      "tag": "Multimodal",
      "blurb": "Ghép vision encoder vào LLM để mô hình đọc được ảnh — điểm ghép ở đâu quyết định model mạnh hay yếu.",
      "n": 5,
      "path": "content/08-llm/09-multimodal/vlm/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "diffusion-models",
      "slug": "diffusion",
      "title": "Diffusion models",
      "tag": "Multimodal",
      "blurb": "Học cách khử nhiễu từng bước nhỏ thay vì sinh trực tiếp — vì sao cách này ổn định và sinh ảnh nét hơn GAN, VAE.",
      "n": 6,
      "path": "content/08-llm/09-multimodal/diffusion-models/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "audio-models",
      "slug": "audio",
      "title": "Audio models",
      "tag": "Multimodal",
      "blurb": "Speech-to-text, text-to-speech và audio embedding — cùng chung một câu hỏi: âm thanh liên tục biến thành token rời rạc thế nào.",
      "n": 5,
      "path": "content/08-llm/09-multimodal/audio-models/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   }
  ]
 },
 {
  "dir": "09-ml-system-design",
  "name": "ML system design",
  "note": "Vòng phỏng vấn không có đáp án đúng duy nhất. Điểm nằm ở khung trả lời và ở chỗ bạn nêu ra đánh đổi.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "mlsd-overview",
      "slug": "sdov",
      "title": "ML system design overview",
      "tag": "System design",
      "blurb": "Vòng này chấm cái gì, khung sáu bước, và những câu hỏi làm rõ phải hỏi trước khi vẽ bất cứ thứ gì.",
      "n": 8,
      "path": "content/09-ml-system-design/01-overview/mlsd-overview/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-frameworks",
    "name": "Framework",
    "books": [
     {
      "dir": "ml-system-design",
      "slug": "mlsys",
      "title": "ML system design",
      "tag": "Design",
      "blurb": "Khung bảy bước, vì sao luôn hai tầng, ngân sách độ trễ và số máy, vòng phản hồi, ví dụ phát hiện gian lận.",
      "n": 15,
      "path": "content/09-ml-system-design/02-frameworks/ml-system-design/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-case-studies",
    "name": "Case studies",
    "books": [
     {
      "dir": "recommendation-system",
      "slug": "recsys",
      "title": "Recommendation system",
      "tag": "System design",
      "blurb": "Truy hồi rồi xếp hạng, lọc cộng tác so với dựa trên nội dung, khởi đầu lạnh, và đo bằng gì.",
      "n": 6,
      "path": "content/09-ml-system-design/03-case-studies/recommendation-system/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "search-ranking",
      "slug": "srch",
      "title": "Search & ranking",
      "tag": "System design",
      "blurb": "Từ truy vấn tới danh sách kết quả: hiểu truy vấn, truy hồi, đặc trưng xếp hạng, và learning to rank.",
      "n": 6,
      "path": "content/09-ml-system-design/03-case-studies/search-ranking/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "llm-rag-system",
      "slug": "ragsys",
      "title": "LLM/RAG system",
      "tag": "System design",
      "blurb": "Thiết kế một trợ lý hỏi đáp trên tài liệu nội bộ: nạp dữ liệu, truy hồi, sinh, đánh giá, chi phí và bảo vệ.",
      "n": 6,
      "path": "content/09-ml-system-design/03-case-studies/llm-rag-system/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   }
  ]
 },
 {
  "dir": "10-mlops",
  "name": "MLOps & engineering",
  "note": "Phần kỹ thuật phần mềm mà vị trí ML vẫn bị hỏi: đưa model ra khỏi notebook và giữ nó sống.",
  "groups": [
   {
    "dir": "01-overview",
    "name": "Overview",
    "books": [
     {
      "dir": "mlops-overview",
      "slug": "opsov",
      "title": "MLOps overview",
      "tag": "MLOps",
      "blurb": "Vì sao hệ thống ML khó vận hành hơn phần mềm thường, và vòng đời từ thí nghiệm tới giám sát.",
      "n": 8,
      "path": "content/10-mlops/01-overview/mlops-overview/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "02-engineering",
    "name": "Engineering tools",
    "books": [
     {
      "dir": "git-workflow",
      "slug": "git",
      "title": "Git",
      "tag": "MLOps",
      "blurb": "Mô hình dữ liệu của Git, nhánh và merge, rebase khác merge, và cách gỡ khi rối.",
      "n": 5,
      "path": "content/10-mlops/02-engineering/git-workflow/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "docker-container",
      "slug": "docker",
      "title": "Docker",
      "tag": "MLOps",
      "blurb": "Image khác container, tầng và cache, dựng nhiều tầng, và vì sao image ML hay nặng vài GB.",
      "n": 5,
      "path": "content/10-mlops/02-engineering/docker-container/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "linux-shell",
      "slug": "linux",
      "title": "Linux & shell",
      "tag": "MLOps",
      "blurb": "Bộ lệnh thật sự hay dùng, đường ống, quyền, tiến trình, và điều tra khi máy chậm.",
      "n": 5,
      "path": "content/10-mlops/02-engineering/linux-shell/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "fastapi-service",
      "slug": "api",
      "title": "Model serving API",
      "tag": "MLOps",
      "blurb": "FastAPI, kiểm tra đầu vào, gộp lô, đồng bộ hay bất đồng bộ, và health check cho service ML.",
      "n": 5,
      "path": "content/10-mlops/02-engineering/fastapi-service/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "03-lifecycle",
    "name": "Model lifecycle",
    "books": [
     {
      "dir": "experiment-tracking",
      "slug": "exp",
      "title": "Experiment tracking & versioning",
      "tag": "MLOps",
      "blurb": "Ghi lại cái gì để tái lập được, đánh phiên bản dữ liệu và model, và model registry.",
      "n": 4,
      "path": "content/10-mlops/03-lifecycle/experiment-tracking/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "ci-cd-ml",
      "slug": "cicd",
      "title": "CI/CD cho ML",
      "tag": "MLOps",
      "blurb": "Kiểm thử cái gì trong hệ ML, kiểm thử dữ liệu, huấn luyện lại tự động, và các chiến lược phát hành.",
      "n": 5,
      "path": "content/10-mlops/03-lifecycle/ci-cd-ml/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "mlops-serving",
      "slug": "mlops",
      "title": "MLOps & model serving",
      "tag": "Operations",
      "blurb": "Ba thứ thay đổi, bốn chiến lược triển khai kèm bán kính rủi ro, phát hiện drift bằng PSI, point-in-time correctness.",
      "n": 15,
      "path": "content/10-mlops/03-lifecycle/mlops-serving/index.html",
      "skeleton": false,
      "lc": 0
     }
    ]
   },
   {
    "dir": "04-infra",
    "name": "Infrastructure",
    "books": [
     {
      "dir": "gpu-inference",
      "slug": "gpu",
      "title": "GPU & inference",
      "tag": "MLOps",
      "blurb": "Bộ nhớ GPU đi đâu, giới hạn băng thông hay tính toán, gộp lô, và chọn phần cứng.",
      "n": 5,
      "path": "content/10-mlops/04-infra/gpu-inference/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "05-serving-engines",
    "name": "Serving engines",
    "books": [
     {
      "dir": "serving-engines-comparison",
      "slug": "serving",
      "title": "vLLM, SGLang & TensorRT-LLM",
      "tag": "MLOps",
      "blurb": "Ba serving engine cùng giải bài toán serve LLM nhanh — khác nhau ở đâu, và tên nào hay bị hỏi thẳng trong phỏng vấn hạ tầng.",
      "n": 6,
      "path": "content/10-mlops/05-serving-engines/serving-engines-comparison/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "06-ai-reliability",
    "name": "AI reliability",
    "books": [
     {
      "dir": "hallucination",
      "slug": "halluc",
      "title": "Hallucination",
      "tag": "AI reliability",
      "blurb": "Model không biết nó không biết — vì sao hallucination là hệ quả tự nhiên của next-token prediction, không phải lỗi cần vá.",
      "n": 5,
      "path": "content/10-mlops/06-ai-reliability/hallucination/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "guardrails-reliability",
      "slug": "guardrails",
      "title": "Guardrails & production reliability",
      "tag": "AI reliability",
      "blurb": "Guardrail chặn input/output xấu, fallback chặn khi model down, human-in-the-loop chặn khi guardrail không chắc — ba lớp phòng thủ khác nhau.",
      "n": 6,
      "path": "content/10-mlops/06-ai-reliability/guardrails-reliability/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   },
   {
    "dir": "07-ai-security",
    "name": "AI security",
    "books": [
     {
      "dir": "prompt-injection",
      "slug": "injection",
      "title": "Prompt injection & jailbreak",
      "tag": "AI security",
      "blurb": "Injection nhắm vào dữ liệu model đọc, jailbreak nhắm vào chính chỉ dẫn hệ thống — hai cách khác nhau để lái model đi khỏi ý định gốc.",
      "n": 5,
      "path": "content/10-mlops/07-ai-security/prompt-injection/index.html",
      "skeleton": true,
      "lc": 0
     },
     {
      "dir": "ai-security-threats",
      "slug": "aisec",
      "title": "Data poisoning, model extraction & access control",
      "tag": "AI security",
      "blurb": "Ba mối đe doạ nhắm vào ba giai đoạn khác nhau của vòng đời model — dữ liệu train, model đã deploy, và quyền truy cập.",
      "n": 4,
      "path": "content/10-mlops/07-ai-security/ai-security-threats/index.html",
      "skeleton": true,
      "lc": 0
     }
    ]
   }
  ]
 }
];
