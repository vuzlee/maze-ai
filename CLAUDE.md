# CLAUDE.md

Ghi chú cho người (hoặc agent) **sửa** kho này. Người chỉ muốn học thì đọc [README.md](README.md).

MazeAI là site tĩnh thuần: **không build step, không server, không dependency**. Mở
`index.html` bằng trình duyệt là chạy. Chỉ có đúng một script Python để sinh lại chỉ mục.

## Cây thư mục = đúng những gì nhìn thấy trên giao diện

Ba tầng: **kệ → nhóm → bài**, xếp theo syllabus ôn tập.

```
index.html                       ← trang thư viện
kit.html                         ← trang tra khuôn hình (tài liệu nội bộ)
404.html                         ← chỉ dùng khi đã deploy; đường dẫn assets là tuyệt đối /… nên mở bằng file:// sẽ trơ
site.webmanifest                 ← tên + màu + icon khi cài site lên màn hình chính
sitemap.xml* · robots.txt*       ← sinh từ SITE_URL trong tools/build.py
assets/style.css · app.js · catalog.js* · search-index.js*     (* sinh tự động)
assets/favicon.svg               ← nguồn hình của logo; .ico + .png bên dưới sinh từ nó
assets/favicon.ico · icon-192.png · icon-512.png · apple-touch-icon.png   (sinh tự động)
content/                         ← thứ tự dưới đây = đúng thứ tự hiện trên giao diện
  01-dsa/                        23 bài · 0 khung
    category.json                ← tên kệ, ghi chú, danh sách nhóm + thứ tự bài
    01-overview/{dsa-overview}
    02-foundations/{big-o-complexity}
    03-data-structures/{data-structures-overview, array-string, linked-list, hash-map, stack-monotonic-queue, heap-priority-queue, tree-bst-traversal, trie, union-find}
    04-algorithms/{algorithms-overview, sorting, two-pointers, sliding-window, prefix-sum, binary-search, greedy, intervals, backtracking, graph-bfs-dfs-topo, shortest-path, dynamic-programming}
  02-python/                        17 bài · 0 khung
    01-overview/{python-overview}
    02-language-core/{language-core-overview, memory-model-mutability, memory-management-gc, scope-legb, data-model-dunder, iterator-generator, decorator-context-manager, exception-handling}
    03-builtin-structures/{list-tuple-set, dict-hash-table}
    04-concurrency/{thread-process-gil, asyncio}
    05-toolkit/{leetcode-toolkit}
    06-oop/{oop-python}
    07-typing/{typing-dataclass}
    08-performance/{performance-profiling}
  03-cs-fundamentals/                        14 bài · 0 khung
    01-overview/{cs-overview}
    02-os/{os-overview, process-thread-scheduling, memory-virtual-paging, lock-deadlock-race}
    03-networking/{networking-overview, dns-tls, tcp-http, caching, rest-api-design, load-balancing}
    04-distributed/{cap-theorem-consistency, consensus-leader-election}
    05-messaging/{messaging-queue-pubsub}
  04-database/                        23 bài · 0 khung
    01-overview/{db-overview}
    02-relational-basics/{relational-overview, relational-model, constraints-integrity, db-normalization, er-modeling}
    03-sql-basics/{sql-basics-overview, sql-select-filter, sql-join, sql-group-aggregate, sql-subquery-cte}
    04-sql-advanced/{sql-advanced-overview, sql-window-functions, sql-index-query-plan, transaction-isolation, query-tuning}
    05-beyond-sql/{nosql-landscape, sharding-replication}
    06-data-systems/{oltp-vs-olap, data-warehouse-lake, etl-elt, batch-stream-processing, data-quality}
  05-machine-learning/                        38 bài · 0 khung
    01-overview/{ml-overview}
    02-math-foundations/{math-foundations-overview, probability-basics, expectation-variance, bayes-theorem, linear-algebra-ml, gradient-optimization, mle-map}
    03-statistics/{statistics, ab-testing}
    04-core-concepts/{core-concepts-overview, supervised-unsupervised, bias-variance-tradeoff, train-val-test-cv, overfitting-regularization, feature-engineering}
    05-classical-ml/{classical-models-overview, linear-regression, logistic-regression, ridge-lasso-elasticnet, svm, knn, naive-bayes}
    06-tree-models/{tree-family-overview, decision-tree, random-forest, gradient-boosting, xgboost, lightgbm}
    07-clustering/{clustering-overview, kmeans-clustering, dbscan, hdbscan}
    08-dimensionality/{pca-dimensionality}
    09-evaluation/{evaluation-overview, metrics-confusion-matrix, roc-auc-pr, calibration}
  06-deep-learning/                        4 bài · 14 khung
    01-overview/{dl-overview*}
    02-neural-network/{neural-network-overview*, perceptron-mlp*, activation-functions*, backpropagation, weight-initialization, normalization, optimizer-sgd-adam*, dropout-regularization*}
    03-cnn/{convolution-basics*, cnn-mobilenet}
    04-sequence/{rnn*, lstm-gru*}
    05-training/{training-recipe*, debug-training*}
    06-generative/{autoencoder*, vae*, gan*}
  07-transformer/                        2 bài · 14 khung
    01-overview/{architecture-overview*}
    02-transformer-core/{transformer-core-overview*, tokenization*, embedding*, positional-encoding*, self-attention, transformer-architecture}
    03-model-families/{families-overview*, bert*, gpt*, encoder-decoder*}
    04-beyond-transformer/{beyond-overview*, ssm*, mamba*, hybrid-hymba*}
    05-efficient/{efficient-attention*}
  08-llm/                        4 bài · 27 khung
    01-overview/{llm-overview*}
    02-training/{training-overview*, pretraining*, scaling-law*, sft-alignment, peft-lora-qlora}
    03-techniques/{techniques-overview*, moe*, long-context*, chain-of-thought*}
    04-inference/{inference-overview*, decoding-strategies*, quantization*, inference-optimization}
    05-rag/{rag-overview*, rag-end-to-end, chunking-strategy*, vector-database*, reranking*}
    06-agents/{agent-tool-use*}
    07-model-labs/{model-labs-overview*, llama*, qwen*, deepseek*, mixtral*, closed-models*}
    08-rag-evaluation/{rag-evaluation*}
    09-multimodal/{clip*, vlm*, diffusion-models*, audio-models*}
  09-ml-system-design/                        1 bài · 4 khung
    01-overview/{mlsd-overview*}
    02-frameworks/{ml-system-design}
    03-case-studies/{recommendation-system*, search-ranking*, llm-rag-system*}
  10-mlops/                        1 bài · 13 khung
    01-overview/{mlops-overview*}
    02-engineering/{git-workflow*, docker-container*, linux-shell*, fastapi-service*}
    03-lifecycle/{experiment-tracking*, ci-cd-ml*, mlops-serving}
    04-infra/{gpu-inference*}
    05-serving-engines/{serving-engines-comparison*}
    06-ai-reliability/{hallucination*, guardrails-reliability*}
    07-ai-security/{prompt-injection*, ai-security-threats*}
tools/build.py                   ← quét content/ sinh lại catalog.js + search-index.js, và ghi lại meta trong <head>
tools/make-icons.py              ← vẽ lại bộ icon từ dấu ◆ thương hiệu (chỉ chạy khi đổi logo)
archive/mazeai-single-file.html  ← bản gốc gộp 1 file, KHÔNG đụng vào, giữ để đối chiếu

* = khung bài: dàn ý đã chốt, nội dung chưa viết (data-skeleton="1")
```

Số thứ tự ở tên thư mục quyết định thứ tự hiển thị. Thứ tự bài trong một nhóm nằm ở `books`
trong `category.json`. Kệ chỉ có đúng một nhóm thì trang chủ không hiện tiêu đề nhóm.

## Bộ nhớ giữa các phiên

[`.claude/memory/`](.claude/memory/) giữ những thứ **không suy ra được từ code**: phản hồi về cách
viết bài, tiến độ, kết quả soát từng kệ. **Đọc [`.claude/memory/MEMORY.md`](.claude/memory/MEMORY.md)
trước khi bắt tay vào việc** — nó là chỉ mục một dòng một ghi chú; chỉ mở file con khi việc đang
làm chạm tới nó. Quy ước ghi nằm ngay trong file đó.

Ranh giới: `CLAUDE.md` mô tả kho **đang như thế nào** (cấu trúc, quy ước, cách build), thư mục
memory ghi việc **đang làm tới đâu và vì sao chọn cách đó**. Cùng một điều đừng viết ở cả hai chỗ.

## Sau mỗi lần sửa nội dung

```bash
python3 tools/build.py
```

Sinh lại `assets/catalog.js` và `assets/search-index.js`, đồng thời báo các chỗ lệch: thư mục bài
chưa được liệt kê, khai báo trỏ tới thư mục không tồn tại, thiếu `index.html`, `data-base` sai số
cấp `../`. **Không chạy lại thì bài mới không hiện ở trang chủ và không tìm được.** Hai file
`assets/*.js` có gắn dấu sinh tự động — đừng sửa tay, lần build sau sẽ ghi đè.

Nó còn **ghi lại khối meta trong `<head>` của mọi trang** (số trang tăng theo số bài, đừng chép số
cứng ở đây — xem log của `python3 tools/build.py`) — phần nằm giữa `</title>` và dòng
`preconnect`: mô tả trang, `color-scheme`, `theme-color`, thẻ Open Graph, và các link favicon.
Mô tả lấy thẳng từ `data-blurb`, tiêu đề chia sẻ lấy từ `data-title`, nên **sửa bài là meta tự khớp
theo** — đừng viết tay mấy dòng đó. `<title>` thì vẫn viết tay, build không đụng vào.

Đổi logo thì sửa `assets/favicon.svg` **và** `tools/make-icons.py` cho khớp, rồi chạy
`python3 tools/make-icons.py` (cần `Pillow`) để vẽ lại `.ico` và các `.png`.

## Deploy

Site chạy ở **<https://maze-ai-lemon.vercel.app/>** (Vercel, phục vụ thẳng cây thư mục, không cấu hình gì).

Địa chỉ đó khai đúng **một chỗ**: hằng số `SITE_URL` đầu `tools/build.py`. Từ đó build sinh ra
`canonical`, `og:url`, `og:image` tuyệt đối, `sitemap.xml` và `robots.txt`. **Đổi domain thì sửa
đúng dòng đó rồi chạy lại build**, đừng sửa tay mấy file kia.

Canonical cần vì Vercel trả 200 cho cả ba dạng `/x`, `/x/` và `/x/index.html` — dạng chuẩn đã chọn
là thư mục có `/` ở cuối. `kit.html` là tài liệu nội bộ nên không nằm trong sitemap.

Để `SITE_URL = ""` thì build bỏ qua toàn bộ phần trên và xoá `sitemap.xml`/`robots.txt` — kho quay
về thuần file://, vẫn chạy bình thường.

## Thêm một bài mới

1. Chép một thư mục bài có sẵn sang đúng nhóm, đổi tên thư mục.
2. Sửa `index.html` của nó:
   - `<article class="doc" id="art-SLUG" data-title="…" data-tag="…" data-blurb="…">`
     — `id` phải duy nhất trong cả kho; `data-*` chính là nội dung hàng bài ngoài trang chủ;
   - mỗi mục là một `<section id="SLUG-sN">` mở đầu bằng
     `<div class="sh"><b>01</b><h2>Tên mục</h2></div>` — mục lục bên trái và breadcrumb tự dựng
     từ đây, không phải khai báo ở đâu khác;
   - `data-base` ở `<html>` và mọi đường dẫn `assets/` phải đúng số cấp `../`.
3. Thêm tên thư mục vào `books` của đúng nhóm trong `category.json`.
4. Chạy `python3 tools/build.py`.

Thêm nhóm mới: tạo thư mục `NN-ten-nhom/` rồi thêm `{"dir", "name", "books"}` vào `groups`.
Thêm kệ mới: tạo `content/NN-ten-ke/category.json` với `{"name", "note", "groups": []}`.

## Đặt tên: thuật ngữ giữ nguyên tiếng Anh

Tên kệ, tên nhóm, tên bài và đầu mục **dùng thuật ngữ tiếng Anh**, không dịch:
`Overview` chứ không phải "Bản đồ"; `Built-in types` chứ không phải "Cấu trúc dựng sẵn";
`Activation functions`, `Backpropagation`, `Sliding window`, `Dynamic programming`,
`Loss function`, `Clustering`, `Convolution`, `Load balancing`…

Phần văn xuôi vẫn là tiếng Việt. Chỉ những **cụm danh từ chuyên ngành** mới giữ tiếng Anh —
từ tiếng Việt thông thường như *sắp xếp, ràng buộc, chuẩn hoá, khởi tạo, suy luận* thì để nguyên,
thay hết sẽ thành thứ tiếng lai đọc không xuôi.

## Kiến trúc một nhóm — ba loại bài

Mọi nhóm dựng theo cùng một khuôn, để càng học càng dễ nối:

**Bài overview** — nhóm nào có **≥3 bài là biến thể / đối thủ của nhau** thì có một bài overview
đứng đầu. Nó kể chuyện chứ không phải mục lục: `Vấn đề · Ý tưởng đầu tiên · Vì sao chưa đủ ·
Dòng thời gian · Các nhánh · **Bảng so sánh** · Học theo thứ tự nào · Từ điển bỏ túi`.
Mọi so sánh ngang hàng (bagging vs boosting, k-means vs DBSCAN, RNN vs Transformer) nằm ở đây,
**không** nằm trong bài kỹ thuật. Nhóm gồm các công cụ rời rạc (Git, Docker, Linux) thì không cần.

**Bài kỹ thuật** — `Vấn đề nó giải · Ý tưởng cốt lõi · Cơ chế · **Hàm mục tiêu** · Đánh đổi ·
**Dùng ở model nào** · Lỗi hay gặp · Hỏi đáp`.

**Bài model** — `Bối cảnh · **Kỹ thuật dùng lại** · Điểm mới của riêng nó · Dữ liệu & huấn luyện ·
Kết quả & giới hạn · Bài học · Hỏi đáp`.

Hai mục in đậm là thứ tạo liên kết: bài MoE nói nó chạy ở Mixtral và DeepSeek; bài DeepSeek nói
nó ghép MoE + MLA + GRPO, ba thứ đã học. Đọc tới bài model là **ráp lại**, không phải học mới.

## Ba kệ nối nhau: Deep learning → Transformer → LLM

Transformer *là* deep learning — tách kệ chỉ để **điều hướng và chia buổi ôn**, không phải tuyên bố
ba ngành khác nhau. Sự liên tục giữ bằng nội dung, không bằng ranh giới thư mục:

- **một dòng thời gian duy nhất** (perceptron → MLP → CNN → RNN/LSTM → attention → Transformer →
  scale → MoE → SSM/Mamba) vẽ lại trong overview của **cả ba kệ**, mỗi kệ tô sáng đoạn của mình,
  làm mờ phần trước và phần sau;
- đầu mỗi overview có một dòng nối ngược về kệ trước.

Ranh giới đặt ở **chỗ attention xuất hiện** — mốc lịch sử sạch nhất.

## Khung bài (`data-skeleton="1"`)

Một bài có thể tồn tại ở dạng **khung**: hero + các mục + mỗi mục một dòng ghi sẽ viết gì.
Đánh dấu bằng `data-skeleton="1"` trên `<article>`. `build.py` mang cờ đó ra `catalog.js`,
và giao diện tự xử lý:

- trang thư viện: hàng bài mờ đi, vạch trái gạch đứt, nhãn đổi thành `khung · N mục`;
- **không tính vào tiến độ** và không tính vào ô "bài" ở trang bìa — chỉ bài có nội dung mới tính;
- đầu mỗi kệ hiện thêm `+N khung`.

Viết nội dung xong thì **xoá `data-skeleton="1"`** và chạy lại `build.py` — không phải sửa gì khác.

Quy ước dàn ý một khung bài, theo đúng thứ tự: **overview → cơ bản → nâng cao**.

Bài `*-overview` có **hai khuôn, chọn theo bản chất nhóm** — đừng mặc định lấy khuôn dài:

**Nhóm là các biến thể cạnh tranh nhau** (bagging vs boosting, k-means vs DBSCAN) — hiểu cái sau
*cần* hiểu cái trước sinh ra để chữa gì. Chuỗi nhân quả đó chính là nội dung, nên dùng khuôn của
[Bản đồ nhánh cây](content/05-machine-learning/06-tree-models/tree-family-overview/index.html):
vấn đề → ý tưởng đầu tiên → vì sao chưa đủ → dòng thời gian → các nhánh → học theo thứ tự nào →
từ điển bỏ túi.

**Nhóm là các công cụ song song** (array, hash map, heap — không cái nào sinh ra để chữa cái kia)
thì khuôn trên **thành hình thức rỗng**: dòng thời gian chỉ còn là mốc năm, "vì sao chưa đủ" bị
kéo dài cho vừa khuôn. Dùng khuôn ngắn 2–3 mục: **cách đọc bảng → bảng tra → (nếu là bài mở kệ)
học theo thứ tự nào**. Xem [Data structures](content/01-dsa/03-data-structures/data-structures-overview/index.html)
và [Algorithms](content/01-dsa/04-algorithms/algorithms-overview/index.html).

Ba luật chung cho mọi overview:

- **Đầu mục là danh từ, đọc là hiểu** — không đếm số ("Bốn thao tác"), không từ tự chế ("Nhận đề
  thuộc họ nào"), không tiếng lóng ("Ràng buộc n"). Hai bài tra công cụ đặt tên thành cặp:
  *Chọn cấu trúc nào* · *Chọn thuật toán nào*.
- **Câu định nghĩa không được chứa thuật ngữ chưa giải thích.** Ví dụ đời thường trước, tên tiếng
  Anh sau — "mở giữa rồi bỏ nửa" trước, "binary search" sau.
- **Mỗi mục phải là thứ không bài nào khác làm được.** Kệ-overview định hướng; nhóm-overview là
  bảng tra. Thứ tự học chỉ khai một chỗ, từ điển thì để ở bài chủ của từng từ.

## Tách một bài làm hai

Bài nào gồm **nhiều chủ đề độc lập** thì tách; bài có tên ghép nhưng chỉ là **một khái niệm**
thì để yên — `Heap & priority queue`, `Metric & confusion matrix`, `Python dict & hash table`
là một chủ đề, không phải hai.

Khi tách, giữ nguyên câu chữ gốc thay vì viết lại:

1. Chia các `<section>` cho hai bên; mỗi bên viết thêm **một mục mở đầu** nói nó nối tiếp bài kia,
   kèm link chéo hai chiều ở mục mở đầu và ở `<footer>`.
2. Mục *Lỗi hay gặp* và *Hỏi đáp*: **bốc từng thẻ `.card.bad` / `details.qa`** sang đúng bên,
   không viết lại. Bên nào bị mỏng dưới 3–4 mục thì viết bổ sung.
3. Đánh số lại `<b>NN</b>` và `id="slug-sN"` cho liên tục từ 01.
4. `lab.js`: lab nào thuộc về nửa nào thì theo nửa đó. Nửa không có lab **phải xoá thẻ
   `<script src="lab.js">`**, không thì trỏ vào file không tồn tại.
5. Sửa `books` trong `category.json`, xoá thư mục cũ, chạy `tools/build.py`.
6. **Quét lại link chéo toàn kho** — bài khác có thể đang trỏ vào bài vừa xoá.

## Một khái niệm, một chủ — không viết hai bài cho cùng một thứ

Khái niệm nào cũng chỉ có **đúng một bài sở hữu** — chọn kệ mà nó đạt độ sâu tự nhiên nhất (nhiều
ví dụ, nhiều đánh đổi thật, không phải kệ nào "nghe hợp" hơn). Đừng viết bản "khái quát" ở một kệ
và bản "áp dụng" ở kệ khác cho cùng một khái niệm — tưởng là hai góc nhìn nhưng thật ra là một bài
bị chia đôi, và sẽ phải sửa hai nơi mỗi lần cập nhật.

Ở **mọi kệ khác** cần nhắc tới nó, chỉ được nhắc bằng đúng cơ chế đã có sẵn — field in đậm kiểu
**"Dùng ở model nào"** / **"Kỹ thuật dùng lại"** trong khuôn *Bài kỹ thuật* / *Bài model*: một câu
trỏ tới bài chủ, không giảng lại. Test để biết có cần mục riêng hay chỉ cần một câu trong văn xuôi:

> Bỏ nó đi, người đọc có hụt một từ khoá **chắc sẽ gặp** ở kệ này không?
> Có → một mục ngắn 2–4 câu + link tới bài chủ. Không → một câu trong văn xuôi là đủ, không cần mục.

**Mục ngắn đó không phải định nghĩa từ điển** — viết theo đúng bốn nhịp sau, luôn theo thứ tự này:

1. **Vấn đề** (1 câu) — vì sao khái niệm này tồn tại, khớp style "vào từ vấn đề" của toàn kho.
2. **Định nghĩa + tên các nhánh/chiến lược chính** (1–2 câu) — gọi thẳng tên, không cần giảng từng
   cái. Bắt buộc phải gọi tên: `search-index.js` đọc chữ trong mục để tìm — thiếu tên thì ai gõ tìm
   đúng từ đó sẽ không thấy mục này, mất tác dụng "nhận ra" mà mục ngắn này tồn tại để làm.
3. **Một câu đánh đổi** — cái giá phải trả khi dùng, không phải liệt kê ưu điểm.
4. **Link tới bài chủ** để xem đầy đủ.

Vẫn chỉ 3–4 câu, không phình thành bài — nếu thấy cần thêm ví dụ hay đào sâu hơn nữa, đó là dấu
hiệu khái niệm này đáng một bài riêng thật (xem đoạn dưới), không phải mục ngắn nữa.

Nếu viết thử mà thấy phần "khái quát" ở kệ khác đã dài hơn một mục — đó là dấu hiệu khái niệm này
đáng một bài riêng thật, nhưng vẫn chỉ có **một** bài, và bài đang định viết ở kệ kia phải xoá,
chuyển link sang bài mới đó.

## Ngôn ngữ thiết kế

Chất riêng của kho: **nền mực ám nâu, nhấn cam đất, tiêu đề serif** — gần với một cuốn sách
chuyên khảo hơn là một dashboard. Toàn bộ nằm trong `assets/style.css`; sửa token ở `:root`
là đổi cả kho. Đừng viết màu thẳng vào bài, luôn dùng `var(--…)` hoặc `rgba(var(--blue-a),…)`.

**Bề mặt & chữ** — phân tầng bằng độ sáng, không bằng viền dày:

| Token | Giá trị | Dùng cho |
|---|---|---|
| `--bg` | `#14110E` | nền trang, mực ám nâu |
| `--panel` | `#1C1815` | thẻ, khối, bảng |
| `--raise` | `#241F1A` | ô nổi lên trên panel |
| `--sunk` | `#0E0C0A` | ô lõm: nền code, track tiến độ |
| `--rule` · `--rule-hi` | `#2E2822` · `#3D352C` | hai mức đường kẻ |
| `--text` → `--faint` | `#EDE7DE` → `#7A6F63` | bốn mức chữ |

**Cam đất `--clay` `#E0855C`** là màu thương hiệu: logo, chữ nghiêng trong tiêu đề, nút chính,
link trong bài, viền mục đang đọc, vạch hover ở đầu mỗi hàng. **Nó không mang nghĩa nội dung —
tuyệt đối không dùng trong hình.**

**Bốn màu ngữ nghĩa** — nghĩa cố định cho mọi hình, mỗi màu kèm một biến `rgb` để pha nền mờ:

| Token | Giá trị | Nghĩa |
|---|---|---|
| `--filled` / `--blue-a` | `#8CA9F2` | dữ liệu, thứ đang xét |
| `--probe` / `--amber-a` | `#EDB44A` | con trỏ, điểm nhấn, đáp án |
| `--tomb` / `--red-a` | `#F2718A` | sai, bị loại, chưa thoả |
| `--ok` / `--green-a` | `#5BCFA0` | đúng, kết quả, đã thoả |

**Chữ** — cả ba font đều có bộ dấu tiếng Việt đầy đủ, đã kiểm bằng subset `vietnamese` của
Google Fonts. **Trước khi đổi font phải kiểm lại subset này** — Instrument Serif chẳng hạn
*không* có `vietnamese`, dùng vào là dấu rơi về font hệ thống.

| Biến | Font | Dùng cho |
|---|---|---|
| `--display` | Newsreader | tiêu đề, tên bài, câu chốt (nghiêng), tên hàng |
| `--body` | Be Vietnam Pro | phần đọc, nút, nhãn |
| `--mono` | JetBrains Mono | code, số thứ tự, nhãn nhỏ chữ hoa |

**Bố cục trang thư viện** dựng như **mục lục một cuốn sách**: mỗi kệ là một chương có số treo
ở lề trái, mỗi bài là **một hàng** (số · tên serif · tóm tắt · nhãn · mũi tên) chứ không phải thẻ —
34 mục quét bằng mắt nhanh hơn hẳn. Trục dọc của số chương và số bài trùng nhau ở mốc `78px`;
đổi `grid-template-columns` của `.shelfhead` hoặc `.bk` thì phải chỉnh cả hai cho khớp lại.

`app.js` dựng cả hai trang: trang chủ đọc `CATALOG` sinh chương + hàng + thanh kệ dính;
trang bài dựng mục lục từ chính các `<section>`, scrollspy, breadcrumb, nút trước/sau,
và đẩy `<footer>` xuống dưới cùng cho đúng thứ tự đọc.

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
| `.eq` | công thức display: mỗi số hạng một nhãn nằm dưới |

Ba quy tắc khi soạn: mỗi mục **một** hình (cần hai hình thường là dấu hiệu mục đó nên tách đôi);
hình phải **thay được** đoạn văn chứ không minh hoạ thêm cho nó; chữ trong hình càng ít càng tốt.

Công thức đứng riêng dùng `.eq` chứ không phải `<pre>`: trình duyệt gióng lề thay mình, nên
không còn cảnh đếm cột rồi lệch (`f̂` là hai codepoint nhưng một ô). `<pre><code>` vẫn là chỗ của
**dẫn giải** — chú thích tiếng Việt, bảng số, suy luận nhiều dòng.

Chỉ dùng SVG khi hình có đường cong, đường chéo hoặc trục toạ độ thật — mẫu ở
[mục mảng xoay](content/01-dsa/04-algorithms/binary-search/index.html#binsearch-s9):
`viewBox="0 0 560 200"`, cột rộng 60, cách nhau 12, đáy y=158. Giữ nguyên khung này thì mọi
biểu đồ cột trong kho nhìn như một bộ.

## Khuôn bài DSA

Các bài kỹ thuật trong `01-dsa` dùng chung một khuôn: **lõi đọc 1,5 phút, phần còn lại để tra**.

Đầu mục **không đếm số** (~~Ba bẫy~~ → `Lỗi hay gặp`) và **thuật ngữ giữ nguyên tiếng Anh** như mọi
chỗ khác trong kho: `Collision`, `Sweep line`, `Stable sort` — không dịch thành "va chạm", "đường
quét", "tính ổn định".

```
01  Ý tưởng               1 hình + 1 câu chốt + 2 gạch đầu dòng
02  Mẫu code cần thuộc    1-2 khối 6-8 dòng
03  Lỗi hay gặp           3 thẻ ngắn
04  Lab                   chạy từng bước
─────────────────────────  hết phần đọc
05+ Mỗi pattern một mục   dấu hiệu nhận đề (.sig) → sửa gì trong mẫu →
                          danh sách bài LeetCode có link (.probs)
cuối Hỏi đáp              4 câu, mỗi câu trả lời 1-2 dòng
```

Hiện có **45 mục pattern** kèm **198 bài LeetCode riêng biệt** (222 lượt link, vài bài dùng lại
ở chủ đề khác). Ba bài `*-overview` của kệ không theo khuôn này — xem phần khuôn overview ở trên. Bài mới trong `01-dsa` phải theo đúng khuôn này. Các kệ khác tự do hơn nhưng vẫn giữ
ba lớp `.key` → `.why` → `details.deep` của bộ khuôn bài học.

## Kiểm trước khi coi là xong

Không có test suite. Cách kiểm tối thiểu sau khi sửa giao diện:

```bash
python3 tools/build.py                       # không được có cảnh báo
```

Rồi mở bằng trình duyệt và soát: trang chủ, một bài có SVG (`dict-hash-table`),
một bài có lab (`binary-search`), `kit.html`, và màn hình hẹp ~490px.
Ba chỗ dễ vỡ nhất: tràn ngang trên mobile, `[hidden]` bị thua `display:grid/flex`
khi bật kết quả tìm kiếm, và màu hardcode trong SVG/lab lệch khỏi bảng màu mới.

## Việc còn lại

Khung thư mục đã dựng đủ cho cả syllabus. Mở bài ra là thấy dàn ý đã chốt; viết xong thì xoá
`data-skeleton="1"` rồi chạy `tools/build.py`. **Đừng tin số trong bảng dưới** — nó lệch ngay khi
có người viết xong một bài; lấy số thật từ log của `python3 tools/build.py` hoặc đếm cờ `skeleton`
trong `assets/catalog.js`. `TAXONOMY.md` giải thích vì sao từng khung tồn tại và bài nào là chủ duy
nhất khi một khái niệm chạm nhiều kệ.

| Kệ | Khung bài chờ viết |
|---|---|
| DSA — data structures & algorithms | ✅ **xong** — 23 bài, không còn khung |
| Python | ✅ **xong** — 17 bài, không còn khung |
| CS fundamentals | ✅ **xong** — 14 bài, không còn khung |
| Database & SQL | ✅ **xong** — 23 bài, không còn khung |
| Machine learning | ✅ **xong** — 38 bài, không còn khung |
| Deep learning | Deep learning overview · Neural network overview · Perceptron & MLP · Activation functions · Optimizer — SGD tới Adam · Dropout & regularization · Convolution · RNN · LSTM & GRU · Training recipe · Debugging training · **Autoencoder · VAE · GAN** |
| Transformer & architectures | Architecture overview · Transformer core overview · Tokenization · Embedding · Positional encoding · Encoder, decoder & both · BERT — encoder-only · GPT — decoder-only · T5 — encoder-decoder · Beyond Transformer overview · State space models · Mamba · Hybrid — Hymba · **Efficient attention** |
| LLM & GenAI | LLM overview · LLM training overview · Pretraining · Scaling law · LLM techniques overview · Mixture of Experts · Long context · Chain-of-Thought · Inference overview · Decoding strategies · Quantization · RAG overview · Chunking strategy · Vector database · Reranking & hybrid search · Agent & tool use · Model labs overview · LLaMA · Qwen · DeepSeek · Mistral & Mixtral · GPT, Claude & Gemini · **RAG evaluation · CLIP · Vision-language model · Diffusion models · Audio models** |
| ML system design | ML system design overview · Recommendation system · Search & ranking · LLM/RAG system |
| MLOps & engineering | MLOps overview · Git · Docker · Linux & shell · Model serving API · Experiment tracking & versioning · CI/CD cho ML · GPU & inference · **vLLM/SGLang/TensorRT-LLM · Hallucination · Guardrails & reliability · Prompt injection & jailbreak · Data poisoning/model extraction/access control** |
