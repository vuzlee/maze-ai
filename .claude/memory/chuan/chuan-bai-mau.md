---
name: chuan-bai-mau
description: "Random forest & bagging là bài mẫu của kho — chín luật rút ra từ nó, dùng để sửa mọi bài khác"
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

   **Dạng mạnh nhất của luật này: một bản đồ duy nhất, mỗi mục sáng đúng một ô.** Ý của người dùng,
   2026-09-04: mental model là tổng quan, mỗi mục dưới là **phóng to một ô của chính nó**. Cách vẽ:
   bản đồ được vẽ lại **nguyên xi ở mọi hình**; ô đang học đủ màu, phần còn lại xám (`--rule` +
   `--faint` + nền `--panel`), và một đường gạch nối sang panel phóng to bên phải. Người đọc học
   cách đọc hình đúng một lần, và **luôn biết mình đang đứng ở đâu** trong bức tranh chung.
   Cài bằng một hàm `frame(hl)` trả về danh sách phần tử — thêm mục mới chỉ là gọi với ô khác,
   không vẽ lại bố cục. Mẫu:
   [Memory management & GC](../../../content/02-python/02-language-core/memory-management-gc/index.html)
   — tám hình, một bản đồ bốn ô.

   **Người dùng chốt lại sau khi thấy bản làm xong** (2026-09-04): *"1 hình mental, xong bóc tách
   dần nó rất liên kết tuần tự và dễ hiểu, đúng như ý tưởng học dễ, tuyến tính mà tôi cố gắng
   truyền tải"*. Nên đây **không phải quy ước vẽ hình, mà là thứ tự học**: hình mental model ở mục
   01 là *toàn bộ bài nói trước một lần*, mỗi mục sau **bóc ra đúng một ô** theo thứ tự đã có sẵn
   trên hình. Người đọc không bao giờ gặp khái niệm rơi từ trên trời — trước khi học nó, họ đã
   nhìn thấy ô của nó và biết nó nằm cạnh cái gì.

   Hệ quả về cách soạn: **thứ tự các mục phải đọc ra được từ chính bản đồ**. Vẽ bản đồ trước, dàn ý
   là hệ quả — không phải viết mục trước rồi vẽ hình minh hoạ sau. Bố cục bản đồ mà không gợi ra
   được một đường đi tuyến tính thì bản đồ sai, không phải dàn ý sai. Ở bài mẫu: bản đồ hai nhánh
   nên bài đi *cơ chế chính (03) → lỗ hổng của nó (04) → thứ vá lỗ hổng (05)*, và ba mục cuối là ba
   ô còn lại của bản đồ.

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

   **Ngoại lệ — bài cheatsheet ôn phỏng vấn thì hình đó lên mục 01, tên là *Mental model*.**
   Ngày 2026-09-04, người dùng: *"phải để lên đầu mới hợp lý, cho cả người mới và người học lại,
   nhìn cái thì não trigger ngay"*. Bài dạng ôn thì người học lại **chỉ mở bài, nhìn hình, đóng** —
   mở bài mới là chỗ đắt nhất, chốt lại ở cuối thì không ai đọc tới. Bài như vậy không có mục tổng
   kết cuối; `figure.gist` chính là mental model, và mục cuối là Hỏi đáp. Xem
   [Memory management & GC](../../../content/02-python/02-language-core/memory-management-gc/index.html)
   và [[sua-bai-memory-management-gc]].

8. **Mặt bài là cheatsheet, chiều sâu nằm trong `details.deep`.** Ngày 2026-09-04, người dùng:
   *"bị quá nhiều chữ, ví dụ bài Gradient boosting, tôi muốn phong cách như cheatsheet nhưng chi
   tiết hơn để học kĩ hơn"*. Đoạn văn dài **không cắt bỏ** — gập nguyên văn vào một
   `<details class="deep">` với `<summary>` là một câu hỏi, mặt bài chỉ còn `p.key` + hình +
   bullet ngắn. Không mất kiến thức nào, mà quét mắt vẫn nhanh.
   Mốc: **không đoạn văn mặt bài nào quá 33 từ** (trần của bài mẫu).

## Luật 9 — hình mở bài: nhìn phát hiểu bài nói gì

Ngay dưới lede, trước mục 01, đặt **đúng một** `figure.gist`: hình vẽ lại chính câu lede,
kèm `figcaption` một câu. Tiêu chí người dùng đặt ra: **nhìn phát hiểu luôn**, không phải đọc
mới hiểu. Nó không thay mục *Tổng kết một hình* ở cuối — đầu bài là lời hứa, cuối bài là chốt lại.

Cả nhóm dùng **chung một bộ từ vựng hình**: cùng kiểu khung bo góc, cùng mũi tên có nhãn, cùng
glyph cây, cùng bốn màu ngữ nghĩa. Học đọc một hình mở bài là đọc được cả năm cái còn lại —
đúng tinh thần luật 1.

**Hình phải vẽ cơ chế đang chạy, không phải ảnh chụp từng chặng.** Ba tầng dọc
*dữ liệu → Train → cây/model → Predict → kết quả*, mũi tên có tên, và vòng hồi tiếp nếu thuật
toán có lặp. Bố cục tự nó phải nói lên cơ chế: tuần tự thì các cột nối nhau, song song thì các cột
rời nhau rồi mới gặp ở ô gộp. Cột cuối luôn là **lúc đã hội tụ** — vẽ ba bước đầu mà chưa thấy
kết quả thì hình vô nghĩa.

**Các bài cùng cơ chế phải dùng chung một khung hình**, cùng dữ liệu và cùng các mốc, để đặt cạnh
nhau là so được từng con số. Bài nào chỉ khác một chi tiết thì **giữ nguyên khung, làm mờ phần
giống, tô sáng đúng ô khác** rồi phóng to ô đó ra — đọc phát thấy ngay "y hệt bài kia, khác mỗi
chỗ này". Ngược lại, cơ chế khác thật thì bố cục phải khác thật.

Ba thứ dễ hỏng, đã dính đủ cả ba ở nhóm tree-models:

- **Nhãn mũi tên đè lên khung bên cạnh.** Chỉ lộ ra khi render thật; phải chụp màn hình soát,
  đọc markup không thấy.
- **Hình nói dối.** Bản đầu của hình LightGBM vẽ hai cây khác số lá trong khi cả bài nói "cùng
  ngân sách lá". Số nào hình khoe thì phải `assert` trong script sinh, hoặc tính lại từ chính
  thuật toán của lab.
- **Chữ trong hình quá dài.** Nhãn dài tràn khỏi khung ở màn hẹp. Nhãn là *nhãn*, không phải câu
  văn — câu văn để `figcaption`. Mốc thực dụng rút ra ở bài memory-management-gc: **nhãn phải ngắn
  tới mức không cần đo**; dài quá thì tách hai dòng, hoặc đẩy hẳn xuống `figcaption`.
- **`viewBox` thấp hơn hình.** Ô cuối bị cắt cụt mà markup vẫn đúng hoàn toàn. Hàm sinh khung nên
  **trả về `y` cuối cùng** để chiều cao tính ra từ đó, đừng chép số cứng.

Sinh bằng script Python dùng chung (`box/txt/arrow/tree/put`), `put()` phải idempotent (xoá
`figure.gist` cũ trước khi chèn) để chỉnh toạ độ rồi chạy lại thoải mái.

**Soát overlap bằng máy, đừng soát bằng mắt.** Ước lượng bề rộng chữ từ class
(`sv-t` ≈ 0,55 × cỡ chữ mỗi ký tự, `sv-d` ≈ 0,52, `sv-l` ≈ 0,60, `sv-h` ≈ 0,72) rồi kiểm bốn thứ:
chữ đè chữ · chữ thò khỏi `rect` bao nó · `rect` đè `rect` không lồng nhau · tràn khỏi `viewBox`.
Thêm một lượt **vạch cắt chữ** — mũi tên vòng hai chiều rất hay chạy xuyên qua nhãn trong ô,
mắt nhìn ảnh chụp cả trang thu nhỏ thì không thấy. Cách chụp để soát: render **một hình một trang**
(nhúng `assets/style.css` vào file tạm) rồi
`google-chrome --headless --force-device-scale-factor=2 --screenshot` — phóng to gấp đôi và không
có chữ xung quanh, lỗi 2–3px hiện ra ngay.

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
