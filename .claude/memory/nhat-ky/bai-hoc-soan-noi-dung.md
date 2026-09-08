---
name: bai-hoc-soan-noi-dung
description: "Bài học rút từ các đợt soạn/sửa nội dung kệ 01→05 — bẫy 'việc thật là tách bài', bốn lỗi khiến người đọc không hiểu, hình dạng bản đồ phải tương phản với bài anh em"
metadata:
  type: project
updated: 2026-09-08
---

Gộp từ chín nhật ký đợt sửa cũ. Số liệu đã bỏ hết (xem [[trang-thai-kho]]) — chỉ giữ thứ **dùng
lại được** khi soạn kệ 06→10.

## Bẫy lặp bốn lần: việc thật là TÁCH BÀI, không phải viết mới

Bốn nhóm liên tiếp ở kệ 04–05 có khung chưa viết, nhưng bài đã viết cạnh nó **đã ôm sẵn** nội dung
của khung:

| Nhóm | Bài đã ôm sẵn | Cách gỡ |
|---|---|---|
| ML / Core concepts | `overfitting-regularization` 15 mục ôm cả bias–variance + CV + rò rỉ | tách ra `bias-variance-tradeoff` và `train-val-test-cv` |
| ML / Model evaluation | `metrics-confusion-matrix` 15 mục ôm cả ROC-AUC, PR-AUC, calibration — **không có gì để viết mới** | tách ra `roc-auc-pr` và `calibration` |
| ML / Tree models | `gradient-boosting` ôm hình mọc-theo-lá + bảng so XGBoost/LightGBM | **chuyển** hình sang `lightgbm`, rút §03 bài cha còn bảng trỏ đường |
| Python / language-core | `memory-model-mutability` 15 mục gánh ba chủ đề | tách ra `memory-management-gc` |

> **Trước khi viết bất kỳ khung nào, đọc toàn văn các bài đã viết cùng nhóm.** Bài deep dive cũ
> hay ôm rộng hơn tên gọi của chúng. Tách thì **giữ nguyên câu chữ**, chia thẻ `.card.bad` và
> `details.qa` về đúng bên rồi viết bù cho đủ, đánh số lại từ 01, và bỏ `<script src="lab.js">` ở
> bên không giữ lab. Quy trình đầy đủ ở `CLAUDE.md` §"Tách một bài làm hai".

## Bốn lỗi khiến người dùng đọc `random-forest` mà "không hiểu gì"

Soát cả 38 bài kệ ML thì bốn lỗi đó là lỗi chung của kệ:

1. **Ký hiệu dùng trước khi định nghĩa** — `Var = ρσ² + (1-ρ)σ²/B` mà cả bài không định nghĩa ρ, σ, B.
2. **Định nghĩa nằm sau chỗ dùng** — "Bagging = Bootstrap AGGregatING" nằm cuối mục.
3. **Đọc thành danh sách sự kiện rời**, không thành mạch.
4. **Lặp 4 lượt trong 1.358 từ** — cùng một ý nói lại ở `.key`, gạch đầu dòng, `.card.bad` và Hỏi đáp.

Kèm thiếu sót so với bài cùng nhóm: bảng hyperparameter, mục *Ưu và nhược*, link về bias-variance.

## Hình dạng bản đồ phải TƯƠNG PHẢN với bài anh em

`random-forest` là năm ô **xếp thẳng xuống** (trồng song song rồi lấy trung bình). Nên bản đồ
`gradient-boosting` cố ý dựng ngược: ba ô ① Phần dư · ② Cây nông · ③ Cộng vào nằm **trong một hộp
có mũi tên quặt ngược** — một vòng lặp đóng. Ai đọc cả hai bài thì thấy khác biệt bagging/boosting
**ở hình học trước khi đọc chữ**.

Cùng luật ở overview: hình không được vẽ lại thứ nằm cạnh nó; chỗ trùng thì đổi thành **ví dụ
chứng minh** câu `ul.why`. Và bố cục hình *là* câu định nghĩa — bản đồ `sql-window-functions` dựng
hộp `Không gộp` → hộp `OVER ( … )` **chứa** ba ô con → hộp `Hàm chạy trên cửa sổ` → ô đỏ `Tính SAU
khi WHERE`; quan hệ chứa/rồi-tới nói đúng thứ tự thực thi, nên mục sau chỉ cần tô sáng ô đỏ.

## Vụn nhặt còn dùng được

- **Có hình rồi thì phải cắt chữ mà hình đã nói.** Thêm hình mà giữ nguyên đoạn văn là làm bài dài
  thêm, không phải dễ hơn.
- **Gỡ chỗ trùng theo luật "một khái niệm, một chủ"**: thay bằng một mục *giới hạn của X* trỏ sang
  bài chủ, đừng chép lại. Ví dụ `sql-index-query-plan` §12–13 trùng `query-tuning` → thay bằng
  *Giới hạn của index*, bài rút 15 → 14 mục.
- **Chuyển quyền sở hữu khái niệm là cách cắt tốt nhất**: drift/skew/feature-store → `mlops-serving`,
  bảng chọn metric → `evaluation-overview`, thiết kế nhiều phép so → `ab-testing`,
  hình học L1 vs L2 → `ridge-lasso-elasticnet`. Chỗ cũ để lại con trỏ bốn nhịp — **vẫn phải gọi
  thẳng tên các nhánh** vì `search-index.js` đọc chữ trong mục.
- **`details.deep` là quy ước đã chết** (TAXONOMY §A4) — cả kho đã sạch, đừng dựng lại.
- **Dời nhóm** = đổi tiền tố thư mục + sửa mọi link tương đối trong kệ + `dir` trong
  `category.json` + đoạn *Học theo thứ tự nào* ở bài overview của kệ. Dùng `git mv` để giữ lịch sử.
- Bẫy dựng hình đã dính khi áp luật 1: ô nửa bề rộng · regex bắt nhầm `<path>` · `check.py` báo
  sạch mà hình vẫn đè nhau (xem [[cong-cu-va-cach-kiem]]).
