# MazeAI

Kho deep dive chuẩn bị phỏng vấn Big Tech. Site tĩnh thuần, **không cần build, không cần server** —
mở thẳng `index.html` bằng trình duyệt là chạy.

## Cây thư mục = đúng những gì nhìn thấy trên giao diện

```
index.html                     ← trang thư viện (các kệ sách)
assets/
  style.css                    ← toàn bộ CSS
  app.js                       ← mục lục, scrollspy, bài trước/sau, tìm kiếm
  catalog.js                   ← SINH TỰ ĐỘNG: danh mục kệ + bài
  search-index.js              ← SINH TỰ ĐỘNG: chỉ mục tìm kiếm toàn văn
content/
  01-algorithms/               ← 1 thư mục = 1 kệ trên trang chủ
    category.json              ← tên kệ, ghi chú, thứ tự bài
    big-o-complexity/          ← 1 thư mục = 1 bài
      index.html               ← nội dung bài (trang đọc được luôn)
      lab.js                   ← script cho các lab tương tác của riêng bài đó
    two-pointers-sliding-window/
    binary-search/
    …
  02-python/
  03-databases/
  04-networking/
  05-machine-learning/
  06-deep-learning/
  07-llm/
  08-system-design/
tools/
  build.py                     ← quét content/ rồi sinh lại catalog.js + search-index.js
archive/
  mazeai-single-file.html      ← bản gốc gộp 1 file, giữ lại để đối chiếu
```

Số thứ tự ở tên thư mục kệ quyết định thứ tự các kệ trên trang chủ.
Thứ tự bài trong một kệ nằm ở `books` trong `category.json`.

## Kệ hiện có

| Thư mục | Kệ | Số bài |
|---|---|---|
| `01-algorithms` | Giải thuật & cấu trúc dữ liệu | 10 |
| `02-python` | Python & nền tảng CS | 4 |
| `03-databases` | SQL & cơ sở dữ liệu | 3 |
| `04-networking` | Mạng & giao thức | 1 |
| `05-machine-learning` | Machine learning | 5 |
| `06-deep-learning` | Deep learning | 3 |
| `07-llm` | LLM & GenAI | 4 |
| `08-system-design` | Thiết kế hệ thống & MLOps | 2 |

## Thêm một bài mới

1. Chép một thư mục bài có sẵn sang kệ mong muốn, đổi tên thư mục.
2. Sửa `index.html` của nó:
   - thẻ `<article class="doc" id="art-SLUG" data-title="…" data-tag="…" data-blurb="…">`
     — `id` phải là duy nhất trong cả kho, `data-*` chính là nội dung thẻ card ngoài trang chủ;
   - mỗi mục là một `<section id="SLUG-sN">` mở đầu bằng
     `<div class="sh"><b>01</b><h2>Tên mục</h2></div>` — mục lục bên trái tự dựng từ đây,
     không phải khai báo ở đâu khác.
3. Thêm tên thư mục vào `books` trong `category.json` của kệ (đặt đúng vị trí muốn nó xuất hiện).
4. Chạy `python3 tools/build.py`.

Thêm một kệ mới: tạo `content/NN-ten-ke/category.json` với `{"name", "note", "books": []}` rồi làm như trên.

## Sau mỗi lần sửa nội dung

```bash
python3 tools/build.py
```

Lệnh này sinh lại `assets/catalog.js` và `assets/search-index.js`. Nó cũng báo các chỗ lệch:
thư mục bài chưa được liệt kê trong `category.json`, khai báo trỏ tới thư mục không tồn tại,
thiếu `index.html`. Không chạy lại thì bài mới sẽ không hiện ở trang chủ và không tìm được.
