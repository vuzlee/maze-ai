---
name: dat-ten-tach-theo-ke
description: "Luật giữ thuật ngữ tiếng Anh tách riêng cho từng kệ lớn — DSA dùng tên thao tác, Python dùng cú pháp thật, Database dùng từ khoá SQL, ML dùng tên metric/model"
metadata:
  type: feedback
updated: 2026-09-07
---

Ngày 2026-09-06 người dùng nói: *"thuật ngữ chưa để tiếng anh, như tra/Tìm trong cấu trúc dữ liệu
nên để thành search, tương tự với add insert, delete, remove,… (**nên tách bạch rule của các kệ
lớn ra để tránh lộn xộn**, ví dụ DSA như bây giờ cũng không phải sửa gì thêm nhiều nhưng các kệ
khác vẫn còn nhiều vấn đề)"*.

**Vì sao phải tách theo kệ.** Luật chung trong CLAUDE.md — *"cụm danh từ chuyên ngành giữ tiếng
Anh, từ tiếng Việt thông thường để nguyên"* — đúng nhưng **quá thô để quét tự động**. Cùng một chữ
"tìm" là **thuật ngữ** ở DSA (`search`, có độ phức tạp riêng, hỏi phỏng vấn bằng đúng chữ đó) nhưng
là **động từ thường** ở ML (*"tìm ba dấu hiệu này trước"*). Quét cả kho bằng một danh sách động từ
ra 58 đầu mục dính, đọc tay thì gần hết là tiếng Việt thường. Tách theo kệ mới quét đúng.

## Luật chung, đúng cho mọi kệ

**Chỉ áp vào chỗ mà bản thân chuỗi chữ đó *là tên của thao tác/khái niệm*:**

| Áp | Không áp |
|---|---|
| ô tiêu đề bảng so sánh, ô cột đầu bảng tra | câu văn xuôi trong `p.key`, `.why`, `figcaption` |
| nhãn trong SVG khi nhãn đó gọi tên một bước | nhãn SVG là một câu (*"đọc ngẫu nhiên đắt hơn"*) |
| đầu mục `<h2>` khi cả mục nói về đúng thao tác đó | đầu mục là một câu hỏi hoặc một mệnh đề |

Phép thử vẫn là *dịch ngược* của [[thuat-ngu-chuan-va-nguon-tham-khao]]: ra **đúng một** cụm tiếng
Anh có tên riêng → thuật ngữ, giữ tiếng Anh. Ra nhiều cụm khác nhau → từ thường, để tiếng Việt.

Và một luật chống tiếng lai: **đổi cả cụm hoặc không đổi gì**. `Metric cho regression` được;
~~`Metric hồi quy`~~ nửa nọ nửa kia thì thà giữ nguyên tiếng Việt.

## 01-dsa — tên thao tác là thuật ngữ, luôn giữ tiếng Anh

Bộ từ bắt buộc: `access` · `search` · `insert` · `delete` · `remove` · `push` · `pop` ·
`traverse` · `merge` · `union` · `find` · `sort`.

Đây là kệ **duy nhất** mà tên thao tác được hỏi thẳng bằng tiếng Anh khi phỏng vấn ("what's the
insert complexity"), nên bảng độ phức tạp phải mang đúng chữ đó. Văn xuôi vẫn tiếng Việt bình
thường (*"chèn vào đầu thì phải dịch cả dãy"*) — chỉ **ô bảng và nhãn hình** mới bắt buộc.

## 02-python — dùng thẳng cú pháp Python, đừng dịch sang tiếng Anh trần

Kệ này có thứ chuẩn hơn cả từ tiếng Anh: **chính đoạn code**. Ô bảng thao tác viết
`x.remove(v)`, `list.insert(0, x)`, `d[k]`, `for x in it` — không viết `remove` trần và càng không
viết "xoá theo giá trị". Bảng trong `list-tuple-set` đã làm đúng ở 5/8 dòng (`x[i]`, `x in s`,
`append / add`, `insert(0, x) · pop(0)`, `pop() cuối`) — các dòng còn lại phải theo.

Dunder, `__len__`, `GIL`, `context manager`, `closure`, `LEGB` giữ nguyên — đã đúng sẵn.

## 03-cs-fundamentals · 04-database — từ khoá của lĩnh vực là thuật ngữ

Database: `primary key` · `foreign key` · `candidate key` · `composite key` · `index` · `join` ·
`aggregate` · `partition` · `lock` · `deadlock` · `isolation level`. Chữ **"khoá"** dịch ngược ra
đúng `key`/`lock` có tên riêng → là thuật ngữ. Nhưng *gộp nhóm, lọc, sắp xếp* trong câu văn thì để
tiếng Việt — chúng chỉ thành thuật ngữ khi đứng cạnh từ khoá SQL (`GROUP BY`, `WHERE`, `ORDER BY`),
mà lúc đó viết thẳng từ khoá SQL là xong.

CS fundamentals: `read`/`write` trong nhãn hình là **hành động đời thường**, để tiếng Việt (*"ghi
vào leader"*); còn `context switching`, `race condition`, `deadlock`, `cache invalidation` là
thuật ngữ, giữ nguyên — đã có luật riêng ở [[thuat-ngu-chuan-va-nguon-tham-khao]].

## 05-machine-learning — tên model, metric, kỹ thuật giữ tiếng Anh; động từ thì không

Giữ tiếng Anh: `regression` · `classification` · `clustering` · `feature` · `label` ·
`overfitting` · `bias` · `variance` · `precision` · `recall` · tên mọi model.

**Nhưng đừng đổi động từ.** *"phân loại bài toán"*, *"đánh giá đang trả lời câu hỏi nào"*,
*"gộp câu trả lời của cả rừng"* — đây là động từ tiếng Việt, đổi sang tiếng Anh thành thứ tiếng lai
đọc không xuôi, đúng thứ CLAUDE.md cấm. Chỗ duy nhất phải đổi là khi **danh từ** bị dịch:
`Hồi quy hay phân loại` (tên hai họ bài toán) → `Regression hay classification`.

## Quét lại thế nào

`/tmp/ops2.py` và `/tmp/opcell.py` (giữ lại được): quét ô bảng + nhãn `<text>` ngắn ≤26 ký tự bắt
đầu bằng một động từ thao tác, in ra theo kệ. **Đừng quét văn xuôi** — nhiễu 90%.
