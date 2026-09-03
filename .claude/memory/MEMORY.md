# Bộ nhớ của kho MazeAI

Chỉ mục các ghi chú giữa các phiên. Một ghi chú = một file = một điều đáng nhớ.
Hai thư mục, phân theo tuổi thọ:

- **`chuan/`** — luật viết bài, còn đúng mãi. Đọc hết trước khi sửa bất kỳ bài nào.
- **`nhat-ky/`** — việc đã làm tới đâu ở từng kệ. Chỉ mở kệ đang đụng tới.

## chuan/ — luật viết bài

- [Bài mẫu: Random forest & bagging](chuan/chuan-bai-mau.md) — **đọc đầu tiên**; tám luật + số đo cụ thể để so
- [Ít chữ, nhiều hình](chuan/it-chu-nhieu-hinh.md) — đo bằng chữ/hình; chỉ số "tỉ lệ văn xuôi" cũ là sai hướng
- [Thuật ngữ chuẩn & nguồn tham khảo](chuan/thuat-ngu-chuan-va-nguon-tham-khao.md) — tên tiếng Anh chuẩn dán lên hình, mỗi tầng một màu; rút gọn được cắt câu, không cắt tên
- [Quy ước viết bài overview](chuan/quy-uoc-viet-overview.md) — macro→micro, không ép khuôn, không nhồi timeline
- [Khuôn .eq cho công thức](chuan/khuon-eq-cong-thuc.md) — chọn HTML thay KaTeX; ranh giới .eq vs `<pre>`; vẽ đường cong bằng SVG
- [Cách trả lời: thật ngắn](chuan/cach-tra-loi-ngan-gon.md) — phần giao diện nói kết quả nhìn thấy, đừng kể tên class

## nhat-ky/ — tiến độ

- [Tiến độ nội dung](nhat-ky/tien-do-noi-dung.md) — bài đã viết / khung còn lại theo từng kệ
- [Đợt sửa theo chuẩn bài mẫu](nhat-ky/dot-sua-theo-chuan-bai-mau.md) — kệ 01→05 đã cắt bullet + thêm mục tổng kết một hình; mật độ hình còn xa [[chuan-bai-mau]]
- [Soát kệ 02-python](nhat-ky/soat-ke-02-python.md) — 2026-09-02: tách bài memory, gộp mục trùng, thêm 2 bài
- [Soát kệ 04-database](nhat-ky/soat-ke-04-database.md) — 2026-09-02: 2 khung cuối, 2 chỗ trùng, 4 lỗ hổng
- [Soát kệ 05-machine-learning](nhat-ky/soat-ke-05-machine-learning.md) — 2026-09-03: viết lại tree-models, đồng bộ cả kệ
- [Tách bài overfitting → Core concepts](nhat-ky/tach-bai-overfitting-core-concepts.md) — trùng thì tách, đừng viết mới

## Cách dùng thư mục này

**Đọc** — đầu phiên đọc file này; mở hết `chuan/` khi sắp sửa nội dung, mở `nhat-ky/` của đúng kệ
đang làm.

**Ghi** — đáng ghi là: phản hồi của người dùng về *cách làm việc* (kèm lý do), quyết định về nội
dung/lộ trình không suy ra được từ code, trạng thái công việc dài hơi. **Không ghi** thứ đã có
trong `CLAUDE.md`, `TAXONOMY.md`, cây thư mục hay lịch sử git.

Mỗi file mở đầu bằng frontmatter:

```markdown
---
name: <slug-gach-ngang>
description: <một dòng, dùng để quyết định có cần mở file này không>
metadata:
  type: feedback | project | reference
updated: YYYY-MM-DD
---
```

Loại `feedback` thì thân bài phải có **Vì sao** và **Áp dụng thế nào**. Ngày tháng viết tuyệt đối.
Nối sang ghi chú khác bằng `[[tên-slug]]` — slug là duy nhất trong cả hai thư mục, không cần ghi
đường dẫn.

Sửa xong một file thì cập nhật luôn dòng ở chỉ mục này. Ghi chú sai thì **xoá**, đừng để lại kèm
đính chính.
