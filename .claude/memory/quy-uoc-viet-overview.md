---
name: quy-uoc-viet-overview
description: Cách viết và soát bài *-overview — kể một mạch từ toàn cảnh xuống chi tiết, không ép khuôn, không nhồi timeline
metadata:
  type: feedback
updated: 2026-09-02
---

Không bịa, không bôi thêm cho dài. Viết rõ, ngắn, đúng và đủ phần cốt lõi. Bài phải là **một mạch
hiểu liền**: mở bằng bức tranh toàn cảnh cho người chưa biết gì, rồi đi dần xuống chi tiết — không
phải nhặt từng khái niệm rời rồi ghép lại.

**Vì sao:** Sau nhiều lượt sửa `python-overview`, `oop-python`, `language-core-overview`, lỗi lặp
nhiều nhất là ép mọi overview vào đúng một khuôn *Vấn đề → Ý tưởng đầu tiên → Vì sao chưa đủ →
Dòng thời gian → Các nhánh*. Khuôn đó sinh ra cho [[tree-family-overview]], nơi thật sự có nhiều
giải pháp cạnh tranh nhau qua thời gian (bagging vs boosting, RNN vs Transformer). Ép nó vào một
ngôn ngữ hay một hệ thống mạch lạc thì hỏng, và đã hỏng theo đúng những cách sau:

- đặt tên mục theo khuôn dù nội dung không khớp — "Ý tưởng đầu tiên" cho một quy tắc nền đúng mãi
  mãi, trong khi tên đó hàm ý một bước đệm rồi sẽ bị thay thế;
- nhồi timeline và trivia lịch sử không giúp hiểu hay nhớ gì thêm;
- overview vẽ lại đúng cơ chế mà bài con nó trỏ tới đã vẽ rồi;
- ba mục khác nhau (các nhánh · bảng so sánh · lộ trình học) mô tả lại cùng một danh sách bốn bài;
- gán nhiều sự kiện khác nguồn gốc vào chung một nguyên nhân cho câu văn gọn — thành sai kiến thức;
- tên mục tự bình luận lý do tồn tại ("hay bị hỏi") thay vì nói thẳng nội dung.

Hai lỗi phát sinh khi tự chữa: đổi tên mục để né khuôn cũ nhưng làm rơi mất từ khoá cốt lõi khỏi
mục lục ("Object model — mọi thứ là object" bị rút thành "Quy tắc nền", quét mục lục không còn
thấy chữ *object*); và overview cấp nhóm tự cho phép mình sâu hơn overview cấp kệ chỉ vì phạm vi
hẹp hơn.

**Áp dụng thế nào:** Trước khi viết hay sửa bất kỳ bài `*-overview` nào, hỏi: chủ đề này có thật là
nhiều giải pháp cạnh tranh nhau qua lịch sử không? Có → khuôn tree-family hợp. Không (một ngôn ngữ,
một hệ thống, các phần chỉ là chương mục nối tiếp) → dùng khung ngắn: nó là gì → vì sao đáng quan
tâm → học theo thứ tự nào; đừng dựng timeline và nhánh giả.

Ba thứ soát lại mỗi lần: **(1)** mục này có đang vẽ lại cơ chế của bài con không — có thì cắt còn
1–2 câu kèm link; **(2)** tiêu đề có gọi thẳng tên khái niệm đang dạy không, người quét mục lục
phải nhận ra ngay, không đoán qua cái tên thơ mộng; **(3)** overview cấp nhóm giữ đúng tầng
overview như cấp kệ — bảng ngắn hoặc một câu là đủ, còn SVG cơ chế, phân biệt `is`/`==`,
shallow/deep copy là việc của bài con.
