---
name: sua-bai-memory-management-gc
description: "2026-09-04 bài Memory management & GC: một bản đồ vẽ lại ở mọi mục, mental model lên mục 01, và số pymalloc cũ trên mạng đã sai"
metadata:
  type: project
updated: 2026-09-04
---

Người dùng: *"vẫn hơi nhiều chữ ít hình, phải có hình tổng thể liên quan tới các bài liên quan mới
dễ hiểu chứ"*. Bài đi từ **249 → 158 chữ/hình** (17 hình, mốc bài mẫu là 123), 6 → 10 mục,
bullet trung bình 14,3 từ, không còn khối code nào ngoài `details.deep`.

**Khung "bốn tầng" là thứ giữ cả bài lại.** Hình mở bài và mục *Tổng kết một hình* vẽ **cùng một
bốn tầng** — cấp phát → reference counting → cyclic GC → pymalloc — mỗi tầng đưa một câu hỏi
xuống tầng dưới. Bảy hình giữa bài là bảy lát cắt của đúng khung đó, nên đọc xong nhìn lại hình
cuối là ráp được. Trước đây bài kể bốn cơ chế rời nhau, đó mới là lý do "khó hiểu", không phải
thiếu chữ.

**Vẽ cơ chế xong vẫn chưa đủ — thiếu định nghĩa thì bài vô nghĩa.** Lượt sau người dùng:
*"gc viết hẳn ra, với cả học xong thì phải hiểu GC là gì chứ, đọc mãi k hiểu"*. Bài lúc đó đi
thẳng vào bốn tầng cơ chế mà **chưa chỗ nào nói garbage collection là gì**, và chữ GC chỉ có
trên tiêu đề dưới dạng viết tắt. Thêm hai mục mở đầu: *Garbage collection là gì*
(reachability từ root set — hình chia ba vùng root · sống · rác) và *Hai cách nhận ra rác*
(đếm tham chiếu vs truy vết, và vì sao CPython dùng cả hai). Bài từ 10 lên 12 mục.

**Luật rút ra:** mọi bài mang chữ viết tắt trong tên phải **viết đủ chữ đó ra ở câu lede**, và mục
01 phải trả lời *"thứ này là gì"* trước khi bất kỳ mục nào nói *"nó chạy thế nào"*. Hình đẹp không
thay được câu định nghĩa.

**Số của pymalloc trên blog gần như đều cũ.** Hầu hết còn ghi *arena 256 KB · pool 4 KB*; CPython
3.10+ đã là **arena 1 MiB · pool 16 KiB** (`ARENA_BITS 20`, `POOL_BITS 14` trong
`Include/internal/pycore_obmalloc.h`). `devguide.python.org/garbage_collector/` giờ chỉ còn trang
chuyển hướng — muốn chắc thì `curl` thẳng source theo nhánh, đừng tin bài viết lại.

Câu "`__slots__` tiết kiệm 40–50%" cũng sai: đo lại bằng `tracemalloc` được **40% cho class hai
thuộc tính, 29% cho tám** — càng nhiều thuộc tính càng ít lợi, vì phần tiết kiệm là cái `__dict__`
chứ không phải dữ liệu.

**Rút ra:** mọi số hiện trên hình đều `assert` trong script sinh, chạy trên chính máy này
(CPython 3.12, 64-bit) — xem luật 9 ở [[chuan-bai-mau]]. Và bắt buộc chụp màn hình soát: hình mở
bài lúc đầu **mất hẳn tầng thứ tư** vì vòng lặp chỉ cộng `y` bên trong nhánh có mũi tên; đọc markup
không đời nào thấy.


## Lượt ba: cắt về core phỏng vấn, và "một bản đồ cho cả bài"

Người dùng dán một cheatsheet GC 17 mục rồi chốt: *"đừng lấy hết, lấy những cái phổ biến hay được
hỏi trong pv với độ nhận diện cao, nhưng quan trọng nhất là bức tranh toàn cảnh đơn giản dễ thuộc,
mental model, nói chung là core ngắn gọn"*. Bài từ **12 mục → 9 mục**, 3.239 → 2.111 chữ,
21 → 8 hình.

**Cắt gì.** Kích thước object / `__slots__` / `getsizeof` — thuộc về
[Performance & profiling](../../../content/02-python/08-performance/performance-profiling/index.html),
đúng luật *một khái niệm một chủ*. Chi tiết block→pool→arena của pymalloc — giữ đúng một ý
*"RSS cao ≠ rò rỉ"* trong mục memory leak. Thuật toán trừ tham chiếu nội bộ và `tp_clear`,
`gc.freeze()`/copy-on-write — gập hết vào `details.deep`. Ba thế hệ thôi làm mục riêng, gộp
vào Cyclic GC còn ba dòng.

**Ngoại lệ luật 7 của [[chuan-bai-mau]]: hình tổng kết chuyển lên mục 01.** Người dùng:
*"nên thay Tổng kết một hình thành mental model cho đúng thuật ngữ, và phải để lên đầu mới hợp lý,
cho cả người mới và người học lại, nhìn cái thì não trigger ngay"*. Với bài dạng cheatsheet ôn
phỏng vấn thì mở bài **là** chỗ đắt nhất — người học lại chỉ mở bài, nhìn hình, đóng. Nên bài này
không có mục tổng kết cuối; `figure.gist` chính là mental model, và mục 09 là Hỏi đáp.

**Ý lớn nhất, do người dùng nghĩ ra: một bản đồ duy nhất, mỗi mục sáng đúng một ô.** Bản đồ bốn ô
— *code của bạn · reference counting · cyclic GC · vạch GC lo bộ nhớ* — được vẽ lại **nguyên xi ở
cả tám hình**; mục nào đang học thì ô đó đủ màu, bảy phần còn lại xám, và một đường gạch nối sang
panel phóng to bên phải. Đây là luật 1 ở dạng mạnh nhất: người đọc học cách đọc hình **đúng một
lần**, và luôn biết mình đang đứng ở đâu trong bức tranh chung.

Cài bằng `frame(hl)` trong `/tmp/memgc/frame.py`: `hl ∈ {None, code, rc, gc, rule}`, `None` là
sáng hết (dùng cho mục 01 và 02). Hàm `lens(from_y, to_y)` vẽ đường nối. Thêm mục mới chỉ là gọi
`frame()` với ô khác — không vẽ lại bố cục.

**Bốn lỗi render, đều chỉ lộ khi chụp màn hình:** ô cuối bản đồ bị cắt vì `viewBox` thấp hơn chiều
cao bản đồ; câu trả lời thuộc lòng tràn khỏi khung; nhãn "PHÓNG TO" đè lên cột đầu của panel;
và hai chú thích cạnh nhau đè lên nhau vì để một dòng dài. Cách chữa chung: **nhãn trong hình phải
ngắn tới mức không cần đo** — dài quá thì tách hai dòng, hoặc đẩy câu đó xuống `figcaption`.

## Người dùng nghiệm thu: cái được là *thứ tự học*, không phải bộ hình

*"bạn thấy việc 1 hình mental, xong bóc tách dần nó rất liên kết tuần tự và dễ hiểu và đúng như ý
tưởng học dễ, tuyến tính mà tôi cố gắng truyền tải chứ"*.

Đáng ghi lại vì nó **đổi nghĩa của việc vừa làm**: tưởng là mẹo trình bày (vẽ lại bản đồ, làm mờ
bảy ô) nhưng thứ thật sự đem lại kết quả là bài **có một đường đi tuyến tính** và đường đi đó
**hiện sẵn trên hình mở bài**. Trước khi học một khái niệm, người đọc đã thấy ô của nó và biết nó
nằm cạnh cái gì — nên không mục nào rơi từ trên trời.

Luật đã ghi vào luật 1 của [[chuan-bai-mau]]: vẽ bản đồ trước, dàn ý là hệ quả. Bản đồ không gợi
ra được một đường đi tuyến tính thì bản đồ sai, không phải dàn ý sai.
