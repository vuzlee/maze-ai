---
name: soat-ke-02-python
description: Kệ 02-python đã soát và sửa xong 2026-09-02 — tách bài memory, gộp mục trùng, thêm Scope & LEGB và Exception handling
metadata:
  type: project
updated: 2026-09-02
---

Soát ngày 2026-09-02 rồi sửa luôn trong cùng phiên. Kệ 02 giờ **17 bài, không còn khung**, nhóm
`02-language-core` từ 5 lên 8 bài. Người dùng đã tự review kệ 01 và xác nhận đạt.

**Đã sửa:**

1. Tách [memory-model-mutability](../../../content/02-python/02-language-core/memory-model-mutability/index.html)
   (15 mục, gánh ba chủ đề) thành hai: bài gốc còn 11 mục về tên/object/copy/truyền tham số, và
   bài mới **memory-management-gc** nhận refcount, `__slots__`, rò rỉ. Link chéo hai chiều ở hero,
   footer và một `stripnote` cuối bài gốc. Lab ở lại bài gốc, bài mới không tham chiếu `lab.js`.
2. Gộp hai mục "Lỗi hay gặp" trùng trong bài memory (§08 + §14) và trong
   [iterator-generator](../../../content/02-python/02-language-core/iterator-generator/index.html)
   (§09 + §10). Ba bẫy vốn không thuộc bài iterator (biến vòng lặp trong closure, đối số mặc định
   khả biến, `lru_cache` giữ `self`) được trỏ về bài chủ thay vì chép lại.
3. Thêm **scope-legb** (LEGB, `global`/`nonlocal`, `UnboundLocalError`, `*args`/`**kwargs`) và
   **exception-handling** (bốn khối, cây `Exception`, exception tự viết, `raise from`, EAFP).
4. Cập nhật `category.json`, `language-core-overview` (roadmap 4→7 bài, bảng §01, từ điển 6→8 từ)
   và `python-overview`.

**Bỏ qua có chủ ý:** f-string, walrus, `match` — kệ này dạy bản chất, không dạy cú pháp; `pytest`
hợp kệ 10 MLOps hơn.

**Quy tắc rút ra khi tách bài:** giữ nguyên câu chữ gốc, chỉ viết mới phần mở đầu và mục Hỏi đáp
cho nửa mới; bốc từng thẻ `.card.bad` và `details.qa` sang đúng bên thay vì viết lại. Kiểm sau khi
tách: link chết, `data-base`, thẻ `<script src="lab.js">` ở nửa không có lab, và `id="art-*"` không
trùng toàn kho. Xem thêm [[tien-do-noi-dung]].
