# CLAUDE.md

Ghi chú cho người (hoặc agent) **sửa** kho này. Người chỉ muốn học thì đọc [README.md](README.md).

MazeAI là site tĩnh thuần: **không build step, không server, không dependency**. Mở
`index.html` bằng trình duyệt là chạy. Chỉ có đúng một script Python để sinh lại chỉ mục.

## Cây thư mục = đúng những gì nhìn thấy trên giao diện

Ba tầng: **kệ → nhóm → bài**, xếp theo syllabus ôn tập.

```
index.html                       ← trang thư viện
kit.html                         ← trang tra khuôn hình (tài liệu nội bộ)
assets/style.css · app.js · catalog.js* · search-index.js*     (* sinh tự động)
content/                         ← thứ tự dưới đây = đúng thứ tự hiện trên giao diện
  01-dsa/                        11 bài · 10 khung
    category.json                ← tên kệ, ghi chú, danh sách nhóm + thứ tự bài
    01-overview/{dsa-overview*}
    02-foundations/{big-o-complexity}
    03-data-structures/{array-string*, linked-list*, hash-map*, stack-monotonic-queue, heap-priority-queue, tree-bst-traversal, trie*, union-find}
    04-algorithms/{sorting*, two-pointers, sliding-window, prefix-sum*, binary-search, greedy*, intervals*, backtracking, graph-bfs-dfs-topo, shortest-path*, dynamic-programming}
  02-python/                        6 bài · 4 khung
    01-overview/{python-overview*}
    02-language-core/{memory-model-mutability, data-model-dunder*, iterator-generator, decorator-context-manager}
    03-builtin-structures/{list-tuple-set*, dict-hash-table}
    04-concurrency/{thread-process-gil, asyncio}
    05-toolkit/{leetcode-toolkit*}
  03-cs-fundamentals/                        2 bài · 7 khung
    01-overview/{cs-overview*}
    02-os/{process-thread-scheduling*, memory-virtual-paging*, lock-deadlock-race*}
    03-networking/{dns-tls*, tcp-http, caching, rest-api-design*, load-balancing*}
  04-database/                        3 bài · 12 khung
    01-overview/{db-overview*}
    02-relational-basics/{relational-model*, constraints-integrity*, db-normalization*, er-modeling*}
    03-sql-basics/{sql-select-filter*, sql-join*, sql-group-aggregate*, sql-subquery-cte*}
    04-sql-advanced/{sql-window-functions, sql-index-query-plan, transaction-isolation, query-tuning*}
    05-beyond-sql/{nosql-landscape*, sharding-replication*}
  05-machine-learning/                        10 bài · 18 khung
    01-overview/{ml-overview*}
    02-math-foundations/{probability-basics*, expectation-variance*, bayes-theorem*, linear-algebra-ml*, gradient-optimization*, mle-map*}
    03-core-concepts/{supervised-unsupervised*, bias-variance-tradeoff*, train-val-test-cv*, overfitting-regularization, feature-engineering*}
    04-classical-ml/{linear-regression, logistic-regression, svm*, knn*, naive-bayes*}
    05-tree-models/{tree-family-overview, decision-tree, random-forest, gradient-boosting}
    06-unsupervised/{kmeans-clustering*, pca-dimensionality*}
    07-evaluation/{metrics-confusion-matrix, roc-auc-pr*, calibration*}
    08-statistics/{statistics, ab-testing}
  06-deep-learning/                        4 bài · 9 khung
    01-overview/{dl-overview*}
    02-neural-network/{perceptron-mlp*, activation-functions*, backpropagation, weight-initialization, normalization, optimizer-sgd-adam*, dropout-regularization*}
    03-cnn/{convolution-basics*, cnn-mobilenet}
    04-sequence/{rnn-lstm-gru*}
    05-training/{training-recipe*, debug-training*}
  07-llm/                        6 bài · 11 khung
    01-overview/{llm-overview*}
    02-transformer/{tokenization*, embedding*, positional-encoding*, self-attention, transformer-architecture}
    03-training/{pretraining*, sft-alignment, peft-lora-qlora}
    04-inference/{decoding-strategies*, quantization*, inference-optimization}
    05-rag/{rag-end-to-end, chunking-strategy*, vector-database*, reranking*}
    06-agents/{agent-tool-use*}
  08-ml-system-design/                        1 bài · 4 khung
    01-overview/{mlsd-overview*}
    02-frameworks/{ml-system-design}
    03-case-studies/{recommendation-system*, search-ranking*, llm-rag-system*}
  09-mlops/                        1 bài · 8 khung
    01-overview/{mlops-overview*}
    02-engineering/{git-workflow*, docker-container*, linux-shell*, fastapi-service*}
    03-lifecycle/{experiment-tracking*, ci-cd-ml*, mlops-serving}
    04-infra/{gpu-inference*}
tools/build.py                   ← quét content/ sinh lại catalog.js + search-index.js
archive/mazeai-single-file.html  ← bản gốc gộp 1 file, KHÔNG đụng vào, giữ để đối chiếu

* = khung bài: dàn ý đã chốt, nội dung chưa viết (data-skeleton="1")
```

Số thứ tự ở tên thư mục quyết định thứ tự hiển thị. Thứ tự bài trong một nhóm nằm ở `books`
trong `category.json`. Kệ chỉ có đúng một nhóm thì trang chủ không hiện tiêu đề nhóm.

## Sau mỗi lần sửa nội dung

```bash
python3 tools/build.py
```

Sinh lại `assets/catalog.js` và `assets/search-index.js`, đồng thời báo các chỗ lệch: thư mục bài
chưa được liệt kê, khai báo trỏ tới thư mục không tồn tại, thiếu `index.html`. **Không chạy lại thì
bài mới không hiện ở trang chủ và không tìm được.** Hai file `assets/*.js` có gắn dấu sinh tự động
— đừng sửa tay, lần build sau sẽ ghi đè.

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

## Khung bài (`data-skeleton="1"`)

Một bài có thể tồn tại ở dạng **khung**: hero + các mục + mỗi mục một dòng ghi sẽ viết gì.
Đánh dấu bằng `data-skeleton="1"` trên `<article>`. `build.py` mang cờ đó ra `catalog.js`,
và giao diện tự xử lý:

- trang thư viện: hàng bài mờ đi, vạch trái gạch đứt, nhãn đổi thành `khung · N mục`;
- **không tính vào tiến độ** và không tính vào ô "bài" ở trang bìa — chỉ bài có nội dung mới tính;
- đầu mỗi kệ hiện thêm `+N khung`.

Viết nội dung xong thì **xoá `data-skeleton="1"`** và chạy lại `build.py` — không phải sửa gì khác.

Quy ước dàn ý một khung bài, theo đúng thứ tự: **overview → cơ bản → nâng cao**.
Mỗi kệ lớn có một bài `*-overview` dùng khuôn của
[Bản đồ nhánh cây](content/05-machine-learning/05-tree-models/tree-family-overview/index.html):
vấn đề → ý tưởng đầu tiên → vì sao chưa đủ → dòng thời gian → các nhánh → học theo thứ tự nào →
từ điển bỏ túi → học xong làm được gì.

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

Ba quy tắc khi soạn: mỗi mục **một** hình (cần hai hình thường là dấu hiệu mục đó nên tách đôi);
hình phải **thay được** đoạn văn chứ không minh hoạ thêm cho nó; chữ trong hình càng ít càng tốt.

Chỉ dùng SVG khi hình có đường cong, đường chéo hoặc trục toạ độ thật — mẫu ở
[mục mảng xoay](content/01-dsa/03-algorithms/binary-search/index.html#binsearch-s9):
`viewBox="0 0 560 200"`, cột rộng 60, cách nhau 12, đáy y=158. Giữ nguyên khung này thì mọi
biểu đồ cột trong kho nhìn như một bộ.

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

Hiện có **46 mục pattern** kèm **151 bài LeetCode riêng biệt** (160 lượt link, vài bài dùng lại
ở chủ đề khác). Bài mới trong `01-dsa` phải theo đúng khuôn này. Các kệ khác tự do hơn nhưng vẫn giữ
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

Khung thư mục đã dựng đủ cho cả syllabus — **83 khung bài** chờ viết nội dung. Mở bài ra là thấy
dàn ý đã chốt; viết xong thì xoá `data-skeleton="1"` rồi chạy `tools/build.py`.

| Kệ | Khung bài chờ viết |
|---|---|
| DSA — data structures & algorithms | DSA overview · Array & string · Linked list · Hash map & set · Trie · Sorting · Prefix sum & difference array · Greedy · Interval · Shortest path |
| Python | Python overview · Data model & dunder · List, tuple & set · LeetCode toolkit |
| CS fundamentals | CS fundamentals overview · Process, thread & scheduling · Virtual memory & paging · Lock, deadlock & race condition · DNS & TLS · REST API design · Load balancing & scaling |
| Database & SQL | Database overview · Relational model · Constraints & integrity · Normalization & denormalization · Schema design · SELECT, WHERE & ORDER BY · JOIN · GROUP BY & aggregate · Subquery & CTE · Query tuning · NoSQL — four families · Replication & sharding |
| Machine learning | Machine learning overview · Probability · Expectation & variance · Bayes' theorem · Linear algebra for ML · Gradient & optimization · MLE & MAP · Supervised, unsupervised & reinforcement · Bias–variance tradeoff · Train/val/test & cross-validation · Feature engineering · SVM · KNN · Naive Bayes · K-means & clustering · PCA & dimensionality reduction · ROC-AUC & PR curve · Probability calibration |
| Deep learning | Deep learning overview · Perceptron & MLP · Activation functions · Optimizer — SGD tới Adam · Dropout & regularization · Convolution · RNN, LSTM & GRU · Training recipe · Debugging training |
| Transformer · LLM · GenAI | LLM overview · Tokenization · Embedding · Positional encoding · Pretraining · Decoding strategies · Quantization · Chunking strategy · Vector database · Reranking & hybrid search · Agent & tool use |
| ML system design | ML system design overview · Recommendation system · Search & ranking · LLM/RAG system |
| MLOps & engineering | MLOps overview · Git · Docker · Linux & shell · Model serving API · Experiment tracking & versioning · CI/CD cho ML · GPU & inference |
