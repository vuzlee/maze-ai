---
name: soat-tu-dong-8-phep
description: "tools/soat.py giữ 8 phép soát tự động — luật viết bài nào kiểm được bằng máy thì nằm ở đó, đừng viết script tạm nữa"
metadata:
  type: feedback
updated: 2026-09-05
---

Luật nào **kiểm được bằng máy** thì phải nằm trong `tools/soat.py`, không viết script tạm rồi vứt.
Chạy `python3 tools/soat.py` in ra 8 nhóm, mỗi nhóm một tổng, cuối cùng là tổng chung.

| # | Phép soát | Ngưỡng / cách bắt |
|---|---|---|
| 1 | Link trỏ vào bài còn là khung | `data-skeleton="1"` |
| 2 | Màu viết cứng trong bài | hex ngoài `:root` — thêm token mới chứ đừng để hex |
| 3 | `--clay` dùng trong hình | cam đất là màu thương hiệu, không mang nghĩa nội dung |
| 4 | Đầu mục đếm số | "Ba bẫy", "Bốn thao tác" |
| 5 | Dòng code quá 92 ký tự | tràn ngang trên mobile |
| 6 | Thuật ngữ bị dịch | bảng `DICH` + tập miễn trừ `MIEN` |
| 7 | `<title>` lệch `data-title` | phải **mở đầu** bằng `data-title` |
| 8 | Nợ luật 1 | >2500 từ **hoặc** >10 mục mà chưa có `figure.gist`, hoặc có mà `nsvg < nsec-2` |

**Vì sao.** Ba lần gần nhất tôi đều viết lại từ đầu một đoạn Python để đếm cùng những thứ đó,
mỗi lần một kiểu, nên số đo giữa các phiên không so được với nhau. Đưa vào `soat.py` thì con số
có nghĩa cố định và tụt dần thấy được.

**Áp dụng thế nào.**

1. **Phép 6 — quyết định "có phải thuật ngữ không" bằng hai bước, không bằng cảm giác.**
   Dịch ngược ra **đúng một** cụm tiếng Anh có tên riêng → là thuật ngữ (xem
   [[thuat-ngu-chuan-va-nguon-tham-khao]]). Rồi **đếm cả hai cách viết trong kho** trước khi
   đổi: `overfit` 84 chỗ vs `quá khớp` 1, `greedy` 25 vs `tham lam` 13, `async` 92 vs
   `bất đồng bộ` 8, `linked list` 19 vs 5 — bên đông là cách viết đã thành chuẩn của kho, sửa
   theo bên đó. Từ tiếng Việt thường (*sắp xếp, chuẩn hoá, phân cụm, giảm chiều, lập lịch*)
   dịch ngược ra nhiều cụm nên **không** vào bảng `DICH`.
2. **Một thuật ngữ sống trên năm bề mặt** — văn xuôi · đầu mục · nhãn SVG · `aria-label` ·
   `data-blurb`. Phép 6 soát cả năm và in ra bề mặt nào sai. Sót nhãn SVG hay `aria-label` là
   `search-index.js` vẫn còn từ cũ; sót `data-blurb` là meta trong `<head>` sai theo (build đọc
   từ đó ra).
3. **Phép 7 nới đúng một mức**: phụ đề sau dấu — thì được (`binary search — mọi biến thể`),
   `<h1>` được thay hẳn phụ đề (`DSA — bản đồ`). Sai là khi chính **cái tên** khác nhau —
   `stack-monotonic-queue` từng thừa chữ "& queue" trong `<title>`.
4. **Phép 8 là danh sách việc, không phải pass/fail.** Sắp theo số từ giảm dần và làm từ dài
   xuống — bài dài là bài khó đọc nhất, và cũng là bài lợi nhất khi có bản đồ.
5. **Số của `soat.py` không thay được mắt.** Ở `sql-window-functions`, `check.py` báo 0 lỗi hình
   học nhưng ảnh chụp cho thấy hai chú thích cột nằm dưới **sai cột**, và khung nét đứt đè lên
   hàng nhãn. Đổi hình học là phải chụp ([[sua-nhanh-it-vong-kiem]]).
