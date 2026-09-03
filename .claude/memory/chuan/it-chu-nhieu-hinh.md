---
name: it-chu-nhieu-hinh
description: "Chuẩn chất lượng bài học: ít chữ, nhiều hình, đọc tuyến tính — đo bằng số chữ trên mỗi hình"
metadata:
  type: feedback
updated: 2026-09-03
---

Ngày 2026-09-03, sau khi tôi viết lại `random-forest` theo hướng **tăng tỉ lệ văn xuôi**, người dùng
đọc lại và nói *"tôi mới đọc Random forest & bagging thôi mà chả hiểu gì?"*, rồi nhắc lại chuẩn đã
nói từ trước: **ít chữ, hình minh hoạ đẹp để dễ học, nội dung tuyến tính dễ hiểu cho người mới**.

**Vì sao.** Tôi đã chẩn đoán ngược. "Khó đọc" không phải vì thiếu văn xuôi — thêm văn xuôi làm bài
dài thêm và khó hơn. Người dùng học bằng **hình**: một `.stack`, `.cmp two`, `.strip` hay `.flow`
thay được cả đoạn văn và nhìn phát hiểu. Chỉ số cũ (tỉ lệ văn xuôi) **sai hướng — đừng dùng lại**.

**Áp dụng thế nào.** Chỉ số đúng là **số chữ trên mỗi hình** (bỏ qua bài khung):

```python
v = len(re.findall(r'<figure|<svg |class="(?:strip|flow|cmp|stack|mtx|axis|seq|bars|eq|cellrow|cells)\b', s))
t = re.sub(r'<svg.*?</svg>', '', s, flags=re.S); t = re.sub(r'<[^>]+>', ' ', t)
ratio = len(t.split()) / max(v, 1)
```

Mốc: bài mẫu [[chuan-bai-mau]] `random-forest` **123 chữ/hình**; trên **250 là đáng soát**, trên
**300 là phải sửa**. Trung vị cả kho (kệ 01→05) hiện là **260** — tức quá nửa kho cần soát.
Cách sửa, theo thứ tự ưu tiên:

1. **Bảng so sánh văn xuôi → khuôn hình** (`.cmp two` cho hai cột, `.stack` cho danh sách nhiều
   dòng, `.axis` cho thứ có thứ tự, `.bars` cho số chênh nhau nhiều lần). Bảng tra thật (bảng độ
   phức tạp, bảng API, cheat-sheet) thì **để yên** — đó là bảng đúng chỗ.
2. **`<ol>`/`<ul class="why">` dài → `.stack`** — checklist debug, danh sách bẫy, các bước.
3. **Đoạn văn lẽ ra nên là hình** — chỗ này mới là việc thật ở những bài không có bảng nào: vẽ mới
   `.strip`/`.flow`/SVG cho cơ chế đang được kể bằng lời.
4. Bảng Hỏi đáp → `details.qa` (vừa gọn vừa tăng thẻ ôn cho `quiz-index.js`).

Caption của `.axiscap` và `.stripnote` là **flex ba `<span>`**: nhãn trái · `<em>` giữa · nhãn phải.
Viết một câu trơn vào đó là hỏng bố cục.

Chạy `python3 tools/build.py` sau mỗi đợt sửa, không được có cảnh báo. Báo cáo cho người dùng theo
[[cach-tra-loi-ngan-gon]] — nói thấy khác gì trên màn hình, không kể tên class.
