---
name: kiem-lai-chinh-cai-thuoc
description: "Trước khi tin một bảng nghiệm thu toàn số 0, phải kiểm chính cái thước — hai lỗi đo 07/09 từng cho ra số 0 giả và làm hỏng 81 file"
metadata:
  type: feedback
updated: 2026-09-07
---

Một bảng nghiệm thu toàn số 0 **không chứng minh gì** nếu chưa kiểm cái thước sinh ra nó.
Ngày 07/09 hai lỗi đo liên tiếp lọt qua, chi tiết ở [[ban-do-ver-bai-toan-kho]].

**Why:** thước hỏng và bài sạch in ra **cùng một dòng**. Không có cảnh báo nào phân biệt hộ.
Tệ hơn: thước sai theo hướng ngược lại (đếm dư) thì mình **hành động** theo nó — lần đó tách nhầm
những đoạn luật không quản, hỏng 81 file.

**How to apply:**

1. **Thước nhận danh sách file thì phải in số file đã đọc.** `TONG 0` mà không kèm `128 bài` là
   vô nghĩa — có thể `sys.argv[1:]` rỗng. Đây đúng là chuyện đã xảy ra.
2. **Chép regex từ file chuẩn, đừng viết lại từ trí nhớ.** Bản chép thiếu `(?![^>]*class=)` biến
   10 vi phạm thành 144. Regex chuẩn của luật 8 ở `chuan-bai-mau.md:398`.
3. **Chạy thử trên một chỗ đã biết là SAI trước.** Thước không bắt được chỗ sai đã biết thì thước
   hỏng; đó là phép thử rẻ nhất và bỏ qua nó là gốc của cả hai lỗi trên.
4. **Số vi phạm cao bất thường = nghi thước trước, nghi bài sau.** 144 chỗ hỏng sau một đợt vừa
   nghiệm thu sạch là chuyện vô lý — lẽ ra phải dừng lại đọc script ngay chỗ đó.
5. **Sao lưu trước mọi lượt sửa hàng loạt**, và khôi phục bằng `cp` từng file. `rm -rf` cả cây rồi
   chép đè là đánh đổi 200 bài lấy một bản sao chưa ai kiểm.
6. Hợp với [[bo-ve-hinh-svgkit]]: máy bắt "hình sai hình học", không bắt "hình đúng hình học mà
   sai ý" — nên trục người đọc không thay thế được bằng thêm script.
