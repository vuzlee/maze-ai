---
name: sua-nhanh-it-vong-kiem
description: "Người dùng phàn nàn 'sửa cái gì cũng lâu' — cắt bớt vòng chụp ảnh xác minh, chỉ chụp lại khi thay hình học"
metadata:
  type: feedback
updated: 2026-09-05
---

*"tôi thấy sao sửa cái gì cũng lâu vậy?"* — nói về quy trình của tôi, không phải về nội dung.

Quy trình ba chặng trong [[sua-3-bai-ke-02-python]] đúng khi **dựng mới** một bài, nhưng tôi
đang chạy đủ cả ba cho **mọi** sửa đổi, kể cả sửa một câu chữ. Chặng 3 (chụp hình 2×, chụp cả
trang 1180px và 490px, cắt lát, đọc từng ảnh) tốn nhiều lượt nhất mà thường không phát hiện gì.

**Vì sao:** ảnh chụp chỉ bắt được lỗi **nghĩa** — nhãn viết tắt khó hiểu, `figcaption` mô tả sai
hình. Sửa câu chữ hay đổi màu thì không sinh ra loại lỗi đó; `check.py` (hình học) đã đủ.

**Áp dụng thế nào:**

| Loại sửa | Chạy gì |
|---|---|
| Chỉ chữ trong bài, lede, figcaption | `gen` → `build` → `tools/build.py`. Không chụp. |
| Đổi màu / class / token CSS | thêm `check.py`. Chụp **một** hình đại diện, không chụp cả trang. |
| Đổi toạ độ, thêm/bớt ô trong hình | đủ ba chặng — nhưng chụp **một** hình + **một** ảnh top trang, không cắt lát toàn bài. |
| Dựng bài mới | đủ ba chặng, chụp hết. |

Và gộp lệnh: sinh cả ba bài + `tools/build.py` trong **một** lượt bash thay vì mỗi bài một lượt.
