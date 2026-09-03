---
name: soat-ke-04-database
description: Kệ 04-database đã soát và đóng xong 2026-09-02 — viết 2 khung cuối, gỡ 2 chỗ trùng, bù 4 lỗ hổng kiến thức
metadata:
  type: project
updated: 2026-09-02
---

Soát ngày 2026-09-02 rồi sửa luôn trong cùng phiên. Kệ 04 giờ **23 bài, không còn khung**.

**Đã viết mới:**

- **er-modeling** → đổi `data-title` thành *Schema design*: từ đoạn mô tả nghiệp vụ ra sơ đồ rồi ra
  bảng. Là bài ráp lại của nhóm `02-relational-basics` — dùng khoá, ràng buộc, chuẩn hoá đã học ở
  ba bài trước, không giới thiệu lý thuyết mới. Đầu mục *Cardinality* (không phải "1-1, 1-n, n-n"
  như dàn ý khung, để đúng luật đầu mục là danh từ tiếng Anh).
- **data-quality**: 6 chiều đo (completeness, uniqueness, validity, consistency, accuracy,
  timeliness) → ba chốt kiểm (nguồn / pipeline / nơi dùng) + fail fast vs quarantine → data
  contract → 4 tín hiệu observability. **Không** giảng lại drift, chỉ trỏ sang `10-mlops/03-lifecycle/mlops-serving`.

**Hai chỗ trùng đã gỡ** (luật "một khái niệm, một chủ"):

1. `sql-index-query-plan` §12 N+1 + §13 checklist trùng nguyên với `query-tuning` §04 và §01 →
   thay bằng một mục **Giới hạn của index** (ba loại chậm index không chữa được) trỏ sang
   `query-tuning`; bỏ luôn thẻ Hỏi đáp về N+1. Bài rút từ 15 xuống 14 mục.
2. `cap-theorem-consistency` (kệ 03) §04 dạy lại leader–follower như `sharding-replication` →
   viết lại để chỉ giữ phần **quorum W+R>N**, tức phần thuộc về câu chuyện consistency, và trỏ
   topology sang bài Database. §05 Sharding vốn đã trỏ đúng, để nguyên.

**Bốn lỗ hổng đã bù** (đều là thứ chắc chắn bị hỏi mà cả kho không có một chữ nào):

- `sql-subquery-cte` thêm §05 **View và materialized view** — trước đó `CREATE VIEW` không xuất
  hiện ở đâu trong kho. Đặt ở đây vì view là "CTE đặt tên vĩnh viễn".
- `sharding-replication` thêm §03 **Partitioning trong một node** — nấc thang giữa index và
  sharding, kèm khung "ba nấc: index → partition → shard".
- `etl-elt` §04 thêm bảng **timestamp vs CDC**, giải thích vì sao CDC làm mờ ranh giới batch/stream.
- `data-warehouse-lake` thiếu hẳn mục *Lỗi hay gặp* (bài ngắn nhất kệ, 852 từ) → thêm 6 thẻ và
  một thẻ Hỏi đáp về lakehouse.

**Bỏ qua có chủ ý:** stored procedure/trigger (kiến thức đang lụi, hiếm bị hỏi), LSM tree (đúng
chủ hơn ở NoSQL nhưng quá sâu cho mức phỏng vấn kệ này), slowly-changing dimension, soft delete,
timezone/collation — đều là chi tiết vận hành, không phải cơ chế.

Xem thêm [[tien-do-noi-dung]].
