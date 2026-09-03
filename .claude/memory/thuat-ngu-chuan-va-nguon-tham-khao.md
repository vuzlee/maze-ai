---
name: thuat-ngu-chuan-va-nguon-tham-khao
description: "Bài phải chứa phần kiến thức phổ biến nhất của chủ đề, và hình phải dán đúng thuật ngữ chuẩn lên từng bộ phận"
metadata:
  type: feedback
updated: 2026-09-03
---

Ngày 2026-09-03, sau khi tôi vẽ lại hình cho `random-forest` mà chỉ chú thích bằng tiếng Việt
("ô vàng là câu hỏi ở gốc", "chấm xanh là lá"), người dùng nói rõ ý *"phân tầng level các node"*
mà họ yêu cầu từ lượt trước là: **root node · internal node · leaf node** — tên gọi chuẩn phải
có mặt trên hình. Kèm yêu cầu chung: *"tham khảo nhiều nguồn để lấy ra những phần kiến thức độ
nhận diện cao nhất, phổ biến là phải có nhé"*.

**Vì sao.** Người dùng học để **ôn kĩ và đi phỏng vấn**, không phải để hiểu mang máng. Một hình
chú thích bằng lời thường ngày thì hiểu được lúc đọc, nhưng gặp lại đúng từ khoá ở nơi khác
(bài giảng, câu hỏi phỏng vấn, tài liệu thư viện) là không nhận ra. Từ khoá chuẩn chính là thứ
giúp nối bài trong kho với cả phần còn lại của thế giới — và `search-index.js` cũng chỉ tìm được
những chữ thật sự nằm trong bài.

**Áp dụng thế nào.**

1. **Trước khi viết/sửa một bài kỹ thuật, tra vài nguồn dạy chủ đề đó** (StatQuest, Analytics
   Vidhya, Towards Data Science, KDnuggets, các bộ câu hỏi phỏng vấn) và liệt kê ra những mảnh
   kiến thức **nguồn nào cũng dạy**. Thiếu mảnh nào thì phải bù. Với random forest, danh sách đó
   là: bootstrap ~63,2% / OOB ~36,8%, bốc tập con cột ở **mỗi lần chia**, `max_features` mặc định
   √p và p/3, majority vote vs averaging, **decorrelate**, MDI vs MDA (permutation), bẫy cột
   nhiều giá trị, bagging vs boosting, Extra Trees, không cần chuẩn hoá thang đo.
2. **Thuật ngữ chuẩn phải nằm trên hình**, không chỉ trong văn xuôi — dán nhãn từng bộ phận bằng
   đúng tên tiếng Anh (`root node`, `internal node`, `leaf node`, `branch`, `depth`), rồi mới
   giải thích nghĩa bằng tiếng Việt ở figcaption. Hình nhiều tầng thì mỗi tầng **một màu cố định**
   và có nhãn tầng ở lề trái: root = xanh dữ liệu viền đậm, internal = ô `.sv-b` trung tính,
   leaf = xanh lá/đỏ theo kết luận. Cùng một chủ đề thì màu tầng phải **giống nhau ở mọi bài**
   (đã đồng bộ `decision-tree` và `random-forest`) — người đọc nhận ra tầng bằng màu, không phải
   đọc lại chú thích.
3. **Bài con dùng lại thuật ngữ của bài prerequisite**, và nói thẳng ở khối "Cần đọc trước" —
   ví dụ `random-forest` mở đầu bằng đúng ba từ root/internal/leaf mà `decision-tree` vừa dạy.
   Đó là cách người mới thấy được "rừng là nhiều cây" chứ không phải một khái niệm mới.
4. Quy ước cũ vẫn giữ nguyên: ít chữ, nhiều hình ([[it-chu-nhieu-hinh]]), câu tiếng Việt thường,
   **chỉ giữ tiếng Anh ở cụm danh từ chuyên ngành**, và mở bài bằng "nó là gì" trước khi bàn vì
   sao cần nó.
