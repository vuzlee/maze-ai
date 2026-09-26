---
name: so-classical-ml
description: "Sáu bài classical ML đã có bản chốt trong bai-mau/ — số liệu đọc thẳng từ đó, ghi chú này chỉ nói vì sao không chép số ra ngoài"
metadata:
  type: project
updated: 2026-09-25
---

`logistic-regression` · `ridge-lasso-elasticnet` · `svm` · `knn` · `linear-regression` ·
`naive-bayes` **đã có bản chốt của người dùng** (2026-09-25), giữ ở [`bai-mau/`](../bai-mau/)
cùng bốn bản trước. Nội dung trong `content/` đúng bằng sáu bản đó. Cả `05-classical-ml` giờ chỉ
còn `classical-models-overview` là chưa theo bản chốt.

**Số liệu không chép ra ghi chú.** Bản trước của file này ghi lại một bộ số tự tính, và bộ số đó
**lệch với bản chốt** — bản chốt dùng 18 điểm cho SVM (không phải 24), một bộ 4 cột cho Ridge, và
bộ xác suất khác cho logistic. Hai chỗ ghi cùng một con số thì sẽ lệch nhau; bài mẫu là bản gốc,
mở file ra là thấy.

Thứ duy nhất đáng giữ: **vì sao ba bài phải dùng bộ ví dụ riêng thay vì sáu khách A–F.**

- **SVM** — sáu điểm thì gần như điểm nào cũng thành support vector, hình mất nghĩa. Bản chốt nói
  thẳng điều đó trong bài, kèm bộ 18 điểm hai chiều.
- **Ridge/Lasso** — cần ít nhất hai cột tương quan và hai cột nhiễu mới thấy L1 bỏ cột còn L2 giữ.
  Sáu khách hai cột không đủ.
- **KNN** — vẫn chạy trên sáu khách A–F, nhưng điểm cần đoán phải chọn sao cho thô và chuẩn hoá ra
  **hai đáp án khác nhau**; chọn sai điểm là hình thành vô nghĩa.

Luật chung rút ra: bộ ví dụ chung của kệ là mặc định, nhưng **khi nó làm hình mất nghĩa thì đổi bộ
và nói rõ trong bài là đang đổi** — xem [[chuan-bai-mau]] mục *Một bộ ví dụ cho cả bài*.
