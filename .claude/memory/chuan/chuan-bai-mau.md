---
name: chuan-bai-mau
description: "Random forest & bagging là bài mẫu của kho — tám luật rút ra từ nó, dùng để sửa mọi bài khác"
metadata:
  type: feedback
updated: 2026-09-04
---

Ngày 2026-09-03, sau khoảng mười lượt review liên tiếp riêng bài
[Random forest & bagging](../../../content/05-machine-learning/06-tree-models/random-forest/index.html),
người dùng chốt: *"hãy coi đây là 1 bài chất lượng"* và yêu cầu sửa các bài đã viết theo nó.

**Vì sao.** Trước đó mỗi lượt sửa chỉ chữa một triệu chứng (chữ nhiều quá, hình rối, bullet dài,
công thức khó). Bài random-forest là chỗ đầu tiên cả bảy thứ cùng đúng một lúc, nên nó thành
**thước đo cụ thể** thay cho các nhận xét rời rạc — có số để đo, không phải cảm tính.

**Số đo của bài mẫu:** 2.577 chữ · 21 hình · **123 chữ/hình** · 43 bullet, trung bình **14,7 từ**,
dài nhất 24 · 13 mục · **0 khối `<pre>`**.

## Tám luật

1. **Chỉ hai hình dạng: bảng dữ liệu và cây.** *"cứ đưa về hình thù dạng data bảng / cây cho thân
   thiện chứ không mỗi bài lại 1 hình thì rất mệt để hiểu"* — mỗi bài chọn 1–2 hình dạng rồi lặp
   lại chúng suốt bài. Người đọc học cách đọc hình **một lần**, không phải học lại ở mỗi mục.
   Hình dạng chọn theo chủ đề: DSA thì mảng + con trỏ, database thì bảng + sơ đồ quan hệ,
   networking thì `.seq` + `.stack`.

2. **Bullet ngắn nhất có thể** — *"nội dung các bullet cả bài cần ngắn gọn nhất, tối giản nhất"*.
   Mốc: **trung bình ≤ 15 từ, không câu nào quá 25**. Cả kho hiện có 737 bullet, **50% đang quá
   25 từ** — đây là việc sửa nhiều nhất.

3. **Dãy việc nối tiếp dùng `ul.steps`, ý song song dùng `ul.why` không gạch ngang.**
   *"mấy cái bullet này cứ bị có gạch ngang làm mất sự liên kết của mắt"*. `.steps` là số thứ tự
   trong vòng tròn nối bằng một vạch dọc liền, mục cuối gắn `class="end"` thành dấu ✓.

4. **Không để code trong mục khái niệm** — *"đừng để code ở đây"*. `<pre><code>` chỉ còn đúng chỗ
   của nó: bài DSA mục *Mẫu code cần thuộc*, bài Python/SQL dạy cú pháp. Câu "gọi hàm nào của thư
   viện" viết thành một dòng chữ, không phải một khối code.

5. **Công thức dùng `.eq` + `<dl>` giải nghĩa từng ký hiệu tại chỗ** ([[khuon-eq-cong-thuc]]).
   Không ký hiệu nào được xuất hiện trước khi có nhãn của nó. Kết bằng `<p class="read">` nói
   công thức **đọc ra nghĩa gì**.

6. **Lab là bảng dữ liệu thật, và tự chạy tiếp khi đủ điều kiện.** *"người nhìn vào cách lấy dữ
   liệu từ 1 bảng sẽ gần gũi hơn là dạng list thế kia"*, *"hình dạng bảng, ô, trực quan to đọc dễ
   hơn, rõ ràng từng ô"*, *"cái trồng cây tự động đi khi rút đủ"*. Ô to, viền rõ từng ô, chữ căn
   giữa; đừng cắt bớt cột cho gọn — gọn là ở cách trình bày, không phải ở lượng dữ liệu.

7. **Mỗi bài đóng bằng một mục "Tổng kết một hình"** — một hình duy nhất ráp lại toàn bài,
   dán đúng thuật ngữ chuẩn ([[thuat-ngu-chuan-va-nguon-tham-khao]]), rồi 3–4 bullet nối các
   khái niệm đã học vào đúng vị trí của chúng trên hình.

8. **Mặt bài là cheatsheet, chiều sâu nằm trong `details.deep`.** Ngày 2026-09-04, người dùng:
   *"bị quá nhiều chữ, ví dụ bài Gradient boosting, tôi muốn phong cách như cheatsheet nhưng chi
   tiết hơn để học kĩ hơn"*. Đoạn văn dài **không cắt bỏ** — gập nguyên văn vào một
   `<details class="deep">` với `<summary>` là một câu hỏi, mặt bài chỉ còn `p.key` + hình +
   bullet ngắn. Không mất kiến thức nào, mà quét mắt vẫn nhanh.
   Mốc: **không đoạn văn mặt bài nào quá 33 từ** (trần của bài mẫu).

**Áp dụng thế nào.** Trước khi sửa một bài, đo bằng script ở [[it-chu-nhieu-hinh]] và script đếm
bullet dưới đây; sau khi sửa đo lại. Thứ tự việc: (1) bullet dài → cắt; (2) `<pre>` khái niệm →
bỏ hoặc đổi thành hình; (3) hình lạ → đưa về hình dạng chính của bài; (4) công thức trần → `.eq`;
(5) thiếu mục tổng kết → vẽ. Không viết thêm chữ mới trừ khi đang bù kiến thức thiếu.

```python
lis = re.findall(r'<li[^>]*>((?:(?!</?li).)*?)</li>', s, flags=re.S)
ws = [len(re.sub(r'<[^>]+>', ' ', x).split()) for x in lis]   # tb ≤15, max ≤25

# đoạn văn *mặt bài*: bắt buộc bỏ <details> và <figure> trước,
# không thì <text> trong SVG bị đếm thành văn xuôi và ra số ảo
b = re.sub(r'<(details|figure).*?</\1>', '', art, flags=re.S)
ps = re.findall(r'<p(?![^>]*class=)[^>]*>((?:(?!</?p[ >]).)*?)</p>', b, flags=re.S)  # max ≤33
```

Báo cáo kết quả theo [[cach-tra-loi-ngan-gon]].
