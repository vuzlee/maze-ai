---
name: dot-luat-1-ke-05-ml
description: "Áp luật 1 lên kệ 05-machine-learning — xong cả nhánh tree-models (gb, dt, xgb); hình dạng bản đồ phải tương phản với bài anh em; danh sách nợ còn lại của 01→05"
metadata:
  type: project
updated: 2026-09-05
---

Nối tiếp [[dot-luat-1-ke-04-database]]. Người dùng: *"làm các bài khó trước và trong quá trình làm
cải thiện memory dần, tự self-improve rồi làm tới các bài dễ hơn. làm hết từ đầu cho tới hết kệ ML
đi"* — nên **dài nhất trước**, và mỗi bài rút được bài học chung thì vá thẳng vào
`tools/svgkit` chứ không giữ riêng (xem [[bo-ve-hinh-svgkit]]).

## Đã xong — `gradient-boosting`

3.154 từ · 10 mục · 3 hình → **1.809 từ · 11 mục · 10 hình** (181 chữ/hình).

**Hình dạng bản đồ phải tương phản với bài anh em.** `random-forest` là năm ô **xếp thẳng
xuống** (trồng song song rồi lấy trung bình). Nên bản đồ boosting cố ý dựng ngược lại: ba ô
① Phần dư · ② Cây nông · ③ Cộng vào nằm **trong một hộp có mũi tên quặt ngược** — một vòng lặp
đóng. Ai đọc cả hai bài thì thấy khác biệt bagging/boosting **ở hình học trước khi đọc chữ**.

Ô đỏ `Cộng vào rồi thì không gỡ ra` đặt **ngoài** vòng lặp, dưới gạch đứt — đó chính là lý do
vòng lặp phải có chỗ cắt từ bên ngoài (early stopping), chứ nó không tự dừng. Bố cục nói được
điều đó thì mục 07 chỉ cần tô sáng ô đỏ.

Cái giữ nguyên chữ gốc, không viết lại: lab `#gblab` (bảng phần dư co lại), khối `.eq` `∂L/∂F`,
4 thẻ `card.bad`, 4 `details.qa`. Cái xoá: mục *Tổng kết một hình* ở cuối, và các `details.deep`
mà hình đã nói hết.

181 chữ/hình là **đặc hơn mốc `random-forest` 123–149**, vẫn trong khoảng 123–225 của kho —
bài này nhiều công thức nên chữ khó cắt thêm mà không mất ý.

## Đã xong — `decision-tree`

2.723 từ · 14 mục · 6 hình → **1.853 từ · 13 mục · 12 hình** (154 chữ/hình).

Bản đồ là hình thứ ba của nhánh và phải khác **cả hai** bài kia: không phải cột thẳng
(random-forest), không phải vòng lặp đóng (gradient-boosting), mà **một hộp "MỘT NÚT — LÀM ĐÚNG
HAI VIỆC" đẻ ra hai nhánh con, rồi mũi tên đứt nét từ nhánh con quặt ngược lên chính hộp đó**.
Hình học nói được câu chính của bài — *không có thuật toán riêng cho "cả cây"* — trước khi đọc
chữ. Ô đỏ `Không cấm thì chia tới từng mẫu` lại nằm ngoài phần đệ quy, giống hai bài kia: cùng
một quy ước "thứ chặn vòng lặp đứng ngoài vòng lặp" ở cả ba bản đồ.

Giữ nguyên chữ gốc: lab `#splab`, hai khối `.eq` (Gini và gain), `ul.steps` scikit-learn,
6 `card.bad`, 6 `details.qa`. Xoá: mục *Tổng kết một hình*, và bốn SVG vẽ tay cũ (chúng hardcode
hex `#8CA9F2…` — svgkit dùng `var(--…)` nên đổi bảng màu là cả kho theo).

Đầu mục cũ *"Ba tên gọi và một đường đọc thành luật"* bị phép "đầu mục không đếm số" của
`soat.py` bắt — đổi thành *"Tên gọi từng phần và đường đọc thành luật"*. Đặt lại đầu mục thì
**chạy `soat.py` ngay sau khi apply**, đừng đợi tới cuối.

## Đã xong — `xgboost`

2.610 từ · 8 mục · 4 hình → **1.989 từ · 11 mục · 9 hình** (221 chữ/hình).

Bản đồ thứ tư của nhánh, và là bài đầu tiên hình dạng **không có mũi tên nào**: ba ô ① Xấp xỉ ·
② Giải đỉnh · ③ So hai đỉnh nối nhau bằng **dấu `=`**. Chủ ý — chúng không phải ba *bước xảy ra
lần lượt* mà là **cùng một hàm mục tiêu viết lại ba lần bằng đại số**; vẽ mũi tên là hình nói dối.
Bốn bản đồ của nhánh giờ tương phản đủ: cột thẳng (rf) · vòng lặp đóng (gb) · đệ quy tự gọi (dt) ·
chuỗi đẳng thức (xgb). Ô đỏ `Gradient boosting gốc: chỉ có độ dốc` nằm **trên**, ngoài khung — chỗ
hở mà bài này sinh ra để vá; ô kỹ thuật nằm **dưới gạch đứt** vì bỏ nó đi thì XGBoost vẫn đúng,
chỉ chậm.

**Cắt được nhiều nhất là chỗ hình đã nói bằng bảng.** Bản đầu ra 247 chữ/hình — trên trần 225 của
kho. Ba khối cắt đi: `div.note key` §06 (hình x06 đã có công thức gain và cả câu "mọc cây và chống
overfit là một việc"), bảng ba mẹo kỹ thuật §07 (x07 là đúng bảng đó cộng thêm cột so 100.000 vs
256 ngưỡng), bảng mạnh/yếu §09 (x09 là đúng bảng đó cộng thứ tự chỉnh hyperparameter). Xuống 221 —
**bảng HTML là thứ nên nghi ngờ trước tiên** khi vượt trần, vì hình vẽ được bảng còn bảng không vẽ
được hình.

Giữ nguyên chữ gốc: lab `#xgblab`, khối `.eq` (`Obj`, `w*`, `Obj*`), 6 `card.bad`, 5 `details.qa`.
Xoá: `figure.gist` ở hero, mục *Tổng kết một hình*, hai SVG vẽ tay hardcode hex.

Hai lỗi mắc lại dù memory đã ghi: **trục y lộn ngược** ở đường loss x03 (check.py 0 lỗi, ảnh chụp
thấy ngay) và **đầu mục đếm số** "Ba mẹo làm nó chạy được…" → *Kỹ thuật làm nó…*. Thêm một lỗi
mới thành mục 4 của [[bo-ve-hinh-svgkit]]: **đường gióng cắt ngang nhãn chữ** — cả sáu phép soát
đều so chữ-với-chữ hoặc chữ-với-ô, không phép nào so chữ với `<line>`.

## Nợ còn lại của 01→05, dài trước

`tcp-http` 3036 · `metrics-confusion-matrix` 2862 · `data-quality` 2668 · `linear-regression`
2663 · `query-tuning` 2613 · `statistics` 2462 · `dynamic-programming` 1233 (11 mục, 1 hình).

Dưới ngưỡng phép 8 còn một tầng 2.000–2.500 từ chưa hiện ra — hết tầng trên thì hạ ngưỡng
trong `tools/soat.py` để thấy tiếp.

Tổng `soat.py`: 55 → 53 (gradient-boosting) → 52 (decision-tree) → **51** (xgboost).

Nhánh `06-tree-models` **đã xong cả bốn bài kỹ thuật** — hết bài này thì luật 1 rời khỏi nhánh
cây, bài tiếp theo dài nhất trong kệ là `metrics-confusion-matrix`.
