---
name: soat-ke-05-machine-learning
description: Soát kệ 05-machine-learning 2026-09-03 — chất lượng lệch; đã viết lại random-forest + gradient-boosting và đồng bộ cả kệ, còn nợ mấy bài overview
metadata:
  type: project
updated: 2026-09-03
---

Người dùng đọc thử [Random forest & bagging](../../content/05-machine-learning/06-tree-models/random-forest/index.html)
thấy khó hiểu và nhận xét chất lượng cả kệ **chưa đồng đều**. Soát cả 38 bài, đo tỉ lệ văn xuôi
(chữ nằm trong đoạn văn ≥15 từ / tổng chữ) — con số này bám khá sát cảm giác "dễ đọc":

| Nhóm | Văn xuôi |
|---|---|
| 05-classical-ml | 41% — dễ nhất kệ |
| 03-statistics · 04-core-concepts · 02-math | 30–34% |
| **06-tree-models** | **27%** — random-forest 28%, gradient-boosting 22% |
| 07-clustering · 09-evaluation | 26% |

## Bốn lỗi của random-forest, xếp theo mức gây khó

1. **Ký hiệu dùng trước khi định nghĩa** — `Var = ρσ² + (1-ρ)σ²/B` ở mục 02, cả bài không định
   nghĩa ρ, σ, B lần nào. Đối chiếu cách làm đúng: xgboost dán nhãn ngay dưới từng ký hiệu Taylor.
2. **Định nghĩa nằm sau chỗ dùng** — pseudo-code "Bagging = Bootstrap AGGregatING" nằm cuối mục 02,
   sau khi đã lập luận cả mục về tương quan giữa các cây. Phải đảo lên đầu mục.
3. **Gần như không có văn xuôi** — bốn mục nội dung, mục mở đầu 0 đoạn văn; chỉ `.key` + gạch đầu
   dòng + hình, nên đọc thành danh sách sự kiện rời, không thành mạch.
4. **Lặp 4 lượt trong 1.358 từ** — bẫy gain importance nói lại ở `.key` mục 04, gạch đầu dòng mục 04,
   thẻ `.card.bad` mục 05 và Hỏi đáp #4. Hỏi đáp chép lại thân bài chứ không thêm góc nhìn.

Thiếu so với bài cùng nhóm: bảng siêu tham số, mục *Đánh đổi · khi nào chọn*, Extra Trees, link về
bias-variance (cả bài là một lập luận về variance mà không trỏ tới bài chủ).

## Lệch chuẩn toàn kệ (sửa rẻ)

- **So sánh ngang hàng bị viết lại nhiều nơi**, trái quy ước "so sánh chỉ nằm ở overview":
  RF↔boosting ở tree-family-overview §05 + gradient-boosting §01 + random-forest Hỏi đáp #3;
  XGBoost↔LightGBM có bảng ở cả gradient-boosting, xgboost, lightgbm.
- **decision-tree lệch khuôn**: mục cuối tên *Tự kiểm tra* (cả kệ dùng *Hỏi đáp*), không có
  *Lỗi hay gặp*, tag `Overview` trong khi ba bài boosting cùng nhóm gắn `Ensemble`.
- **eyebrow có 4 kiểu** trong riêng nhóm cây: `Deep dive · Machine learning · nhánh cây` /
  `Machine learning · Tree models` / `Nhập môn · bài 1 của nhánh cây`.
- **Đầu mục còn đếm số**: Ba núm để hãm cây lại · Bốn giả định và hệ quả khi vi phạm ·
  Năm cái bẫy thực tế · Bốn đại lượng gắn nhau.
- random-forest và decision-tree là **hai bài ML duy nhất** còn để công thức trong
  `<pre class="core">` thay vì khuôn `.eq` — xem [[khuon-eq-cong-thuc]].

Build sạch, 0 link gãy, không bài nào thiếu Hỏi đáp ngoài decision-tree.

## Đã sửa xong 2026-09-03 — cả 4 bước

1. **random-forest viết lại** — 6 mục → 8. Định nghĩa bagging đưa lên đầu; công thức variance đổi
   sang `.eq` có `<dl>` giải nghĩa ρ, σ, B; thêm *Siêu tham số* và *Đánh đổi · khi nào chọn nó*
   (kèm Extra Trees); gỡ 3 trong 4 lượt lặp bẫy gain importance; link về bias-variance.
2. **gradient-boosting viết lại** — 5 mục → 9, thêm *Vì sao gọi là gradient* (`.eq` dẫn
   phần dư = −∂L/∂F) và *Vì sao boosting vẫn thắng deep learning trên dữ liệu bảng*.
3. **So sánh ngang hàng dồn hết về tree-family-overview**: §05 nhận bảng RF↔GBM + `.cmp` chọn cái
   nào + ghi chú cách trả lời phỏng vấn; §06 mới *Chọn XGBoost hay LightGBM* (bảng 5 dòng +
   CatBoost). lightgbm §04 đổi thành *Đánh đổi và khi nào chọn nó* rồi trỏ về overview.
4. **Đồng bộ toàn kệ**: 13 eyebrow + 4 footer về đúng `Machine learning · <Tên nhóm>` /
   `… · mở đầu nhóm <Tên>`; tag decision-tree `Overview`→`ML`, linear/logistic `Foundations`→`ML`;
   6 đầu mục đếm số đổi tên; decision-tree tách *Lỗi hay gặp* thành mục riêng (thêm 2 thẻ),
   đổi *Tự kiểm tra*→*Hỏi đáp*, hai công thức Gini/gain sang `.eq`.

Build sạch, 0 link gãy, 0 anchor gãy.

> **Cảnh báo — chỉ số "tỉ lệ văn xuôi" ở trên là SAI hướng.** Ngày 2026-09-03 người dùng đọc lại
> `random-forest` sau đợt sửa này và vẫn không hiểu gì. Thêm văn xuôi làm bài dài thêm chứ không
> dễ hơn; chuẩn thật là **ít chữ, nhiều hình** — xem [[it-chu-nhieu-hinh]]. Các thay đổi về cấu
> trúc, đồng bộ eyebrow/tag và dồn so sánh về overview vẫn đúng, chỉ riêng phép đo là bỏ.

**Đợt sửa sau (2026-09-03, theo chuẩn đúng):** rà cả kho theo số chữ/hình, đổi bảng và danh sách
dài thành khuôn hình, vẽ thêm hình cho những mục chỉ có chữ. Kết quả toàn kho: bài tệ nhất
529 → 428 chữ/hình, trung vị 286 → 257, số bài trên 400 từ 13 còn 1.
