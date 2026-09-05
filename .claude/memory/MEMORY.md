# Bộ nhớ của kho MazeAI

Chỉ mục các ghi chú giữa các phiên. Một ghi chú = một file = một điều đáng nhớ.
Hai thư mục, phân theo tuổi thọ:

- **`chuan/`** — luật viết bài, còn đúng mãi. Đọc hết trước khi sửa bất kỳ bài nào.
- **`nhat-ky/`** — việc đã làm tới đâu ở từng kệ. Chỉ mở kệ đang đụng tới.

## chuan/ — luật viết bài

- [Bài mẫu: Random forest & bagging](chuan/chuan-bai-mau.md) — **đọc đầu tiên**; chín luật + số đo cụ thể để so. Luật 1 = mục 01 gồm câu định nghĩa + một hình mental model 3–5 ô, mỗi mục sau bóc một ô (overview và kệ DSA miễn)
- [Bố cục hình phải nói đúng quan hệ](chuan/chuan-bai-mau.md) — trong bài mẫu: chứa / rồi tới / hay / dựng trên / sinh ra — mỗi quan hệ một bố cục; che chữ đi phải đọc ra câu định nghĩa
- [Ít chữ, nhiều hình](chuan/it-chu-nhieu-hinh.md) — đo bằng chữ/hình; chỉ số "tỉ lệ văn xuôi" cũ là sai hướng
- [Thuật ngữ chuẩn & nguồn tham khảo](chuan/thuat-ngu-chuan-va-nguon-tham-khao.md) — tên tiếng Anh chuẩn dán lên hình; dịch ngược ra đúng một cụm tiếng Anh thì là thuật ngữ, giữ nguyên
- [Quy ước viết bài overview](chuan/quy-uoc-viet-overview.md) — macro→micro, không ép khuôn, không nhồi timeline
- [Khuôn .eq cho công thức](chuan/khuon-eq-cong-thuc.md) — chọn HTML thay KaTeX; ranh giới .eq vs `<pre>`; vẽ đường cong bằng SVG
- [Cách trả lời: thật ngắn](chuan/cach-tra-loi-ngan-gon.md) — phần giao diện nói kết quả nhìn thấy, đừng kể tên class
- [Soát tự động: 8 phép](chuan/soat-tu-dong-8-phep.md) — luật kiểm được bằng máy thì nằm ở `tools/soat.py`; thuật ngữ sống trên 5 bề mặt; cách quyết định một chữ có phải thuật ngữ
- [Bộ vẽ hình svgkit](chuan/bo-ve-hinh-svgkit.md) — `tools/svgkit` dùng chung, đừng chép sang `/tmp`; ba chỗ máy soát KHÔNG bắt: hình đúng hình học mà sai ý, số bịa, chạy trên cả `index.html`
- [Sửa nhanh, ít vòng kiểm](chuan/sua-nhanh-it-vong-kiem.md) — chụp ảnh xác minh chỉ khi đổi hình học, không phải mọi lần sửa chữ

## nhat-ky/ — tiến độ

- [Tiến độ nội dung](nhat-ky/tien-do-noi-dung.md) — bài đã viết / khung còn lại theo từng kệ
- [Đợt sửa theo chuẩn bài mẫu](nhat-ky/dot-sua-theo-chuan-bai-mau.md) — kệ 01→05: bullet và đoạn văn quá 33 từ đã về 0; **83 bài còn nợ luật 1**, riêng 01→05 là **71** (69 bài để *Tổng kết một hình* ở cuối; 39/127 bài là ngoại lệ có chủ ý)
- [Soát kệ 02-python](nhat-ky/soat-ke-02-python.md) — 2026-09-02: tách bài memory, gộp mục trùng, thêm 2 bài
- [Sửa bài Memory management & GC](nhat-ky/sua-bai-memory-management-gc.md) — 2026-09-04: một bản đồ vẽ lại ở mọi mục, mental model lên 01, bóc dần từng ô thành thứ tự học — chỗ khai sinh ra luật 1
- [Sửa 3 bài kệ 02-python](nhat-ky/sua-3-bai-ke-02-python.md) — 2026-09-05: dict, iterator, memory-model theo khuôn một bản đồ; cách đo để chọn bài cần sửa
- [Thí điểm luật 1 — transaction-isolation](nhat-ky/thi-diem-transaction-isolation.md) — 2026-09-05: bài khó nhất (16 mục) làm trước; bộ công cụ frame/check/apply dùng lại được + bốn bẫy
- [Áp luật 1 cho kệ 02-python](nhat-ky/dot-luat-1-ke-02-python.md) — 2026-09-05: xong `thread-process-gil`, `asyncio`, `oop-python` (7/17 bài); ba bẫy mới: ô nửa bề rộng, regex bắt nhầm `<path>`, check sạch mà hình vẫn đè nhau
- [Áp luật 1 cho kệ 04-database](nhat-ky/dot-luat-1-ke-04-database.md) — 2026-09-05: xong `sql-window-functions` (bài dài nhất 01→05); có hình rồi thì phải cắt chữ hình đã nói; danh sách nợ còn lại
- [Áp luật 1 cho kệ 05-machine-learning](nhat-ky/dot-luat-1-ke-05-ml.md) — 2026-09-05: xong `gradient-boosting`; hình dạng bản đồ phải tương phản với bài anh em (vòng lặp đóng vs xếp thẳng)
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
