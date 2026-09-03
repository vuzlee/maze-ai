---
name: soat-ke-05-machine-learning
description: Nhật ký kệ 05-machine-learning — đợt soát 2026-09-03, đã viết lại tree-models và đồng bộ cả kệ
metadata:
  type: project
updated: 2026-09-03
---

Ngày 2026-09-03 người dùng đọc [Random forest & bagging](../../../content/05-machine-learning/06-tree-models/random-forest/index.html)
và nói không hiểu. Soát cả 38 bài, tìm ra bốn lỗi của bài đó — đều là lỗi chung của kệ:

1. **Ký hiệu dùng trước khi định nghĩa** — `Var = ρσ² + (1-ρ)σ²/B` mà cả bài không định nghĩa
   ρ, σ, B lần nào.
2. **Định nghĩa nằm sau chỗ dùng** — "Bagging = Bootstrap AGGregatING" nằm cuối mục, sau khi đã
   lập luận cả mục về tương quan giữa các cây.
3. **Đọc thành danh sách sự kiện rời**, không thành mạch.
4. **Lặp 4 lượt trong 1.358 từ** — bẫy gain importance nói lại ở `.key`, gạch đầu dòng,
   thẻ `.card.bad` và Hỏi đáp.

Thiếu so với bài cùng nhóm: bảng hyperparameter, mục *Đánh đổi · khi nào chọn*, Extra Trees,
link về bias-variance.

## Đã sửa trong ngày

1. **random-forest và gradient-boosting viết lại** — thêm định nghĩa lên đầu, công thức đổi sang
   khuôn `.eq` có `<dl>` giải nghĩa từng ký hiệu, thêm *Hyperparameter* và
   *Đánh đổi · khi nào chọn nó*, gỡ 3 trong 4 lượt lặp, nối link về bias-variance.
2. **So sánh ngang hàng dồn hết về `tree-family-overview`** (RF↔GBM, XGBoost↔LightGBM↔CatBoost),
   đúng luật "so sánh chỉ nằm ở overview".
3. **Đồng bộ toàn kệ**: 13 eyebrow + 4 footer về đúng `Machine learning · <Tên nhóm>`;
   tag decision-tree/linear/logistic về `ML`; 6 đầu mục đếm số đổi tên; decision-tree tách
   *Lỗi hay gặp* thành mục riêng và đổi *Tự kiểm tra* → *Hỏi đáp*.
4. **Rà cả kho theo số chữ/hình** ([[it-chu-nhieu-hinh]]): bài tệ nhất 529 → 428 chữ/hình,
   trung vị 286 → 257.

Sau đó random-forest còn được người dùng review kỹ thêm nhiều lượt nữa và trở thành **bài mẫu**
của cả kho — chuẩn rút ra ghi ở [[chuan-bai-mau]].

Build sạch, 0 link gãy, 0 anchor gãy.
