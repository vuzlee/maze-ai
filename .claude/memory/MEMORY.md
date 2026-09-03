# Bộ nhớ của kho MazeAI

Chỉ mục các ghi chú giữa các phiên làm việc. Một ghi chú = một file = một điều đáng nhớ.
Quy ước ghi/đọc nằm ở cuối file này.

## Ghi chú hiện có

- [Quy ước viết bài overview](quy-uoc-viet-overview.md) — macro→micro, không ép khuôn, không nhồi timeline
- [Tiến độ nội dung](tien-do-noi-dung.md) — bài đã viết / khung còn lại theo từng kệ; bốn kệ nền đã xong, khung còn lại nằm hết ở nửa AI
- [Soát kệ 02-python](soat-ke-02-python.md) — kết quả review 2026-09-02: chỗ đã ổn, mục trùng, hai lỗ hổng nội dung
- [Soát kệ 04-database](soat-ke-04-database.md) — review 2026-09-02: 2 khung cuối đã viết, 2 chỗ trùng đã gỡ, 4 lỗ hổng đã bù
- [Tách bài overfitting → Core concepts](tach-bai-overfitting-core-concepts.md) — đọc bài đã viết trước khi viết khung cạnh nó; trùng thì tách, đừng viết mới
- [Cách trả lời: thật ngắn](cach-tra-loi-ngan-gon.md) — phần giao diện/CSS nói kết quả nhìn thấy, đừng kể thuật ngữ
- [Soát kệ 05-machine-learning](soat-ke-05-machine-learning.md) — review 2026-09-03: đã viết lại random-forest + gradient-boosting, dồn so sánh về overview, đồng bộ cả kệ (phép đo văn xuôi trong đó đã bị bác bỏ)
- [Ít chữ, nhiều hình](it-chu-nhieu-hinh.md) — chuẩn chất lượng bài học, đo bằng chữ/hình; chỉ số "tỉ lệ văn xuôi" cũ là sai hướng
- [Thuật ngữ chuẩn & nguồn tham khảo](thuat-ngu-chuan-va-nguon-tham-khao.md) — tra nhiều nguồn lấy phần kiến thức phổ biến nhất; dán tên tiếng Anh chuẩn (root/internal/leaf node) lên hình, mỗi tầng một màu
- [Khuôn .eq cho công thức](khuon-eq-cong-thuc.md) — chọn HTML thay KaTeX; ranh giới .eq vs <pre>; quy ước vẽ đường cong bằng SVG; đã áp dụng xong 14 khối

## Cách dùng thư mục này

**Đọc** — đầu phiên, đọc file này trước; chỉ mở file con khi việc đang làm chạm tới nó.

**Ghi** — đáng ghi là: phản hồi của người dùng về *cách làm việc* (kèm lý do), quyết định về nội
dung/lộ trình không suy ra được từ code, trạng thái công việc dài hơi. **Không ghi** thứ đã có
trong `CLAUDE.md`, `TAXONOMY.md`, cây thư mục hay lịch sử git — trùng lặp thì sau này lệch nhau.

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

Loại `feedback` thì thân bài phải có **Vì sao** và **Áp dụng thế nào**. Ngày tháng viết tuyệt đối,
không viết "tuần trước". Nối sang ghi chú khác bằng `[[tên-slug]]`.

Sửa xong một file thì cập nhật luôn dòng tương ứng ở chỉ mục trên. Ghi chú sai thì **xoá**, đừng
để lại kèm ghi chú đính chính.
