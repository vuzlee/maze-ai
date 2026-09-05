---
name: dot-luat-1-ke-04-database
description: "Áp luật 1 lên kệ 04-database — xong sql-window-functions, sql-index-query-plan, sharding-replication; danh sách nợ còn lại của 01→05 sắp theo độ dài"
metadata:
  type: project
updated: 2026-09-05
---

Nối tiếp [[dot-luat-1-ke-02-python]] và [[thi-diem-transaction-isolation]]. Người dùng:
*"được chốt theo hướng tốt nhất, trong quá trình làm thấy vấn đề hay cải thiện gì hay thì cứ
linh hoạt áp dụng, chung quy vẫn là để dễ học nhất"* — nên chọn bài theo phép 8 của
[[soat-tu-dong-8-phep]], **dài nhất làm trước**.

## Đã xong — `sql-window-functions`

Bài dài nhất của 01→05: 3.501 từ · 16 mục · 2 hình → **2.917 từ · 15 mục · 13 hình** (225 chữ/hình).

Bản đồ 6 ô, và bố cục của nó *là* câu định nghĩa: hộp `Không gộp` (ba dòng vào → ba dòng ra +
một cột mới) → mũi tên → hộp `OVER ( … )` **chứa** ba ô con `PARTITION BY` · `ORDER BY` ·
`ROWS / RANGE` → mũi tên → hộp `Hàm chạy trên cửa sổ` → gạch đứt → ô đỏ `Tính SAU khi WHERE`.
Quan hệ chứa/rồi-tới nói đúng thứ tự thực thi, nên mục 04 chỉ cần tô sáng ô đỏ là xong.

Cái đáng chép lại cho bài sau: **có hình rồi thì phải cắt chữ đã bị hình nói mất.** Cắt được
584 từ mà không mất ý nào — `.stack` liệt kê ba phần của `OVER` (mục 03), `.stack` chuỗi thực
thi (04), bảng ba hàm xếp hạng + `.stack` bốn hàm (06), `.strip` sáu ô thời gian + bảng bốn
frame (09), hai `.stack` `EXPLAIN` (12), bảng nhận diện đề (13, thay bằng 3 gạch đầu dòng nói
*cách đọc* bảng thay vì lặp lại bảng). Không cắt thì bài phình ra chứ không dễ học hơn.

Mục *Tổng kết một hình* ở cuối bị xoá — bản đồ ở mục 01 đã thay nó, và giữ cả hai là nói hai lần.

## Đã xong — `sql-index-query-plan`

3.435 từ · 15 mục · 1 hình → **1.659 từ · 14 mục · 12 hình** (138 chữ/hình, sát mức
`random-forest` 123). Cắt được 1.776 từ — đợt cắt mạnh nhất tới giờ.

Bản đồ 6 ô, bố cục nói luôn câu định nghĩa *"bạn không ra lệnh, planner tự chọn"*:
`Câu SQL nói MUỐN GÌ` → mũi tên → hộp `PLANNER` **chứa** ba ô con `Thống kê` · `Các cách lấy`
(index chỉ là MỘT lựa chọn thêm) · `Chi phí` → mũi tên → `Kế hoạch thực thi — EXPLAIN cho xem`
→ gạch đứt → ô đỏ `Index phải trả giá ở mọi lệnh ghi`. Ô đỏ nằm **ngoài** chuỗi mũi tên vì nó
không giúp gì cho `SELECT` — đó chính là lý do "cứ index hết cho chắc" sai.

Ba việc cắt đáng chép lại:

- **Khối `<pre>` kể lại đúng thứ hình vừa vẽ thì xoá**, không giữ cả hai. Mục 07 (`CREATE INDEX
  idx ON orders (user_id, status, created_at)`) và mục 08 (hai lệnh `CREATE INDEX` cùng chú
  thích `→ Index Scan` / `→ Index Only Scan`) đã nằm nguyên trong hình.
- **Code là *dữ liệu* của hình thì để trước hình**, không để sau. Mục 04: khối `EXPLAIN ANALYZE`
  phải đứng trên, hình bóc bốn con số của chính khối đó nằm dưới — ngược lại thì đọc hụt.
- Chú thích dưới lab (mục 05) rút còn một câu: hai câu kia đã thành band vàng trong hình.

Mục *Tổng kết một hình* xoá như bài trước; số mục 14→13, 15→14. Đã quét `grep` toàn kho:
không bài nào link tới `#sqlindex-sN` nên đánh số lại an toàn — **nhớ quét trước khi đổi số**.

Nhân tiện sửa phép 4 (đầu mục đếm số): `Ba thuật toán JOIN` → `Thuật toán JOIN`,
`Ba hàm xếp hạng` → `Hàm xếp hạng` ở bài window.

## Đã xong — `sharding-replication`

3.237 từ · 8 mục · 2 hình → **1.743 từ · 11 mục · 9 hình** (194 chữ/hình). Bài **duy nhất tới giờ
tăng số mục**: mục 01 cũ nhồi bốn chủ đề (leader–follower, multi-leader, đồng bộ/bất đồng bộ,
replication lag) nên tách thành bốn mục 01–04. Luật 1 đòi *mỗi mục một hình*, mà một hình không
kể nổi bốn thứ — **mục nhồi thì phải tách trước rồi mới vẽ**, đừng cố gộp vào một hình.

Bản đồ 7 ô, bố cục là câu định nghĩa: hộp `Một máy không còn đủ` → **hai nhánh song song**, hộp
`REPLICATION — nhân bản TOÀN BỘ` (chứa `Leader ghi · follower đọc` · `Đồng bộ · bất đồng bộ` ·
`Replication lag`) rồi mũi tên *"nhưng mỗi bản vẫn chứa hết"* xuống hộp `SHARDING — chia TỪNG PHẦN`
(chứa `Partitioning` · `Shard key`) → gạch đứt → ô đỏ `Mất join · transaction · unique`. Ô đỏ chỉ
dính nhánh sharding, đó là điểm phân biệt hai nhánh mà bài cũ phải nói bằng ba đoạn văn.

Hai hình cũ trong bài (sơ đồ leader/follower ở mục 01, vòng consistent hashing ở mục 04) bị thay
hẳn bằng s02 và s07 — hình cũ vẽ **màu hex cứng** `#EDB44A`, `#8CA9F2`, không theo token.

Cái đáng chép lại: `check.py` báo 0 lỗi mà PNG vẫn hỏng **ba lần** ở bài này — caption `sv-s`
đặt sau một hàng ô cao 30–34px thì đè lên hàng đó (s06, s08 lúc đầu; s04 mục "Ba cách né" lúc
sau). `check.py` chỉ bắt text-đè-text và text tràn rect, **không bắt text đè viền rect**. Nên
sau mỗi hàng ô còn có chữ bên dưới thì bước `y` phải ≥ chiều cao ô + 18, không phải + 8.


## Nợ còn lại của 01→05, dài trước

`tcp-http` 3036 ·
`metrics-confusion-matrix` 2862 · `data-quality` 2668 · `linear-regression` 2663 ·
`query-tuning` 2613 · `statistics` 2462 · `dynamic-programming` (1233 từ nhưng 11 mục, 1 hình).

Bốn bài tree-models (`random-forest`, `gradient-boosting`, `decision-tree`, `xgboost`) là loại
nợ nhẹ hơn: đã có `figure.gist` nhưng thiếu hình bóc ô ở từng mục.

Tổng `soat.py` sau ba bài: **55** (60 → 59 → 56 → 55).
