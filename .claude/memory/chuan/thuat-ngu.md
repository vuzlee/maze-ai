---
name: thuat-ngu
description: "Luật thuật ngữ: phép dịch ngược để biết chữ nào giữ tiếng Anh, tách riêng theo từng kệ, năm bề mặt phải đồng bộ, và bắt buộc phủ kiến thức phổ biến của chủ đề"
metadata:
  type: feedback
updated: 2026-09-08
---

Gộp từ `thuat-ngu-chuan-va-nguon-tham-khao` + `dat-ten-tach-theo-ke`.
Kiểm tự động ở phép 6 của `tools/soat.py` — xem [[cong-cu-va-cach-kiem]].

## Phép quyết định: DỊCH NGƯỢC

**Dịch ngược ra đúng MỘT cụm tiếng Anh có tên riêng → là thuật ngữ, giữ tiếng Anh.**
Ra nhiều cụm khác nhau → từ thường, để tiếng Việt.

- Thuật ngữ: "chuyển ngữ cảnh" → `context switching` · "khoá chết" → `deadlock` ·
  "điều kiện tranh" → `race condition` · "lề" → `margin` · "siêu phẳng" → `hyperplane` ·
  "hàng xóm gần nhất" → `nearest neighbor`.
- Từ thường: *sắp xếp, ràng buộc, chuẩn hoá, khởi tạo, suy luận, phân cụm, giảm chiều, lập lịch*.

**Ba bẫy đã dính, đều cùng một kiểu — từ càng nghe xuôi càng khó thấy:**

1. `lề` → `margin`: đọc như tiếng Việt phổ thông nên qua mọi vòng soát. Người đọc chỉ ra.
2. `siêu phẳng` → `hyperplane`: bản dịch **đã có trong sách giáo khoa tiếng Việt**, nên không có
   vẻ gì là dịch sai. Vẫn phải giữ tiếng Anh.
3. `hàng xóm gần nhất` → `nearest neighbor`: dịch nghe xuôi **vẫn là dịch sai**.

**Nhưng giữ tiếng Anh không có nghĩa là thay máy móc mọi lần xuất hiện.** Cùng chữ `margin` ở §04
của `svm` mang **nghĩa khác** (yᵢ·F(xᵢ)) — chỗ đó gọi "dải" mới xuôi. "hiện ra như một **đường
cong**" nói *hình dạng nhìn thấy*, không gọi tên đối tượng toán học — giữ tiếng Việt.

Chống tiếng lai: **đổi cả cụm hoặc không đổi gì.** `Metric cho regression` được;
~~`Metric hồi quy`~~ nửa nọ nửa kia thì thà giữ nguyên tiếng Việt.

## Năm bề mặt — sót một chỗ là hỏng tìm kiếm

Một thuật ngữ sống ở: **văn xuôi · đầu mục · nhãn SVG · `aria-label` · `data-blurb`** (cộng
`<title>` và câu hỏi trong `details.qa`). Sót nhãn SVG hay `aria-label` → `search-index.js` vẫn
còn từ cũ; sót `data-blurb` → meta trong `<head>` sai theo (build đọc từ đó ra).

**Đếm cả hai cách viết trong kho trước khi đổi:** `overfit` 84 chỗ vs `quá khớp` 1 · `greedy` 25
vs `tham lam` 13 · `async` 92 vs `bất đồng bộ` 8. Bên đông là chuẩn của kho, sửa theo bên đó.

## Chỉ áp vào chỗ chuỗi chữ đó LÀ TÊN của thao tác

| Áp | Không áp |
|---|---|
| ô tiêu đề bảng so sánh, ô cột đầu bảng tra | câu văn xuôi trong `p.key`, `.why`, `figcaption` |
| nhãn SVG khi nhãn đó gọi tên một bước | nhãn SVG là một câu (*"đọc ngẫu nhiên đắt hơn"*) |
| đầu mục `<h2>` khi cả mục nói về thao tác đó | đầu mục là một câu hỏi hoặc một mệnh đề |

## Tách luật theo từng kệ lớn

Người dùng 2026-09-06: *"nên tách bạch rule của các kệ lớn ra để tránh lộn xộn"*. Lý do: cùng chữ
"tìm" là **thuật ngữ** ở DSA (`search`, có độ phức tạp riêng, hỏi phỏng vấn bằng đúng chữ đó)
nhưng là **động từ thường** ở ML. Quét cả kho bằng một danh sách động từ ra 58 đầu mục dính, đọc
tay thì gần hết là tiếng Việt thường.

- **01-dsa** — tên thao tác luôn giữ tiếng Anh: `access search insert delete remove push pop
  traverse merge union find sort`. Kệ duy nhất được hỏi thẳng bằng tiếng Anh khi phỏng vấn, nên
  bảng độ phức tạp phải mang đúng chữ đó. Chỉ **ô bảng và nhãn hình** mới bắt buộc.
- **02-python** — chuẩn hơn cả từ tiếng Anh là **chính đoạn code**: `x.remove(v)`,
  `list.insert(0, x)`, `d[k]`, `for x in it`. Không viết `remove` trần, càng không "xoá theo giá
  trị". `dunder __len__ GIL context manager closure LEGB` giữ nguyên.
- **03-cs · 04-database** — từ khoá lĩnh vực là thuật ngữ: `primary/foreign/candidate/composite
  key · index · join · aggregate · partition · lock · deadlock · isolation level ·
  context switching · race condition · cache invalidation`. Nhưng `read`/`write` trong nhãn hình
  là hành động đời thường, để tiếng Việt. *gộp nhóm, lọc, sắp xếp* chỉ thành thuật ngữ khi đứng
  cạnh từ khoá SQL — mà lúc đó viết thẳng `GROUP BY`/`WHERE`/`ORDER BY` là xong.
- **05-ml** — giữ tiếng Anh: `regression classification clustering feature label overfitting bias
  variance precision recall` + tên mọi model. **Đừng đổi động từ**: *"phân loại bài toán"*, *"gộp
  câu trả lời của cả rừng"* là động từ tiếng Việt. Chỗ phải đổi là khi **danh từ** bị dịch:
  `Hồi quy hay phân loại` → `Regression hay classification`.

**`KE_RIENG` trong `tools/soat.py`** khoanh một chữ vào đúng một kệ (khác `MIEN` là miễn một bài).
Thêm `'hàng xóm':'neighbor'` vào `DICH` thì phép 6 kêu cả ở DSA và OS — nơi «hàng xóm» là từ
thường (ô kề, khối nhớ liền kề). Cách chữa đúng là giới hạn phạm vi, không phải bỏ chữ khỏi `DICH`:

```python
KE_RIENG = {'hàng xóm': '05-machine-learning'}   # ngay sau MIEN
if vi in KE_RIENG and KE_RIENG[vi] not in p: continue
```

Luật con: **từ nào có nghĩa thường song song thì chỉ bắt dạng đủ cụm** — thêm `lề mềm`→`soft
margin`, `lề cứng`→`hard margin`, không thêm `lề` trần (lề trang, lề trái sẽ kêu oan hàng loạt).

## Thuật ngữ phải nằm TRÊN HÌNH, và sống sót qua mọi lần rút gọn

Người dùng học để **ôn kĩ và đi phỏng vấn**. Hình chú thích bằng lời thường thì hiểu lúc đọc,
nhưng gặp lại đúng từ khoá ở chỗ khác là không nhận ra.

1. **Dán nhãn từng bộ phận bằng tên tiếng Anh** (`root node`, `internal node`, `leaf node`,
   `branch`, `depth`), rồi mới giải nghĩa tiếng Việt ở `figcaption`. Hình nhiều tầng thì mỗi tầng
   **một màu cố định**, và **cùng chủ đề phải cùng màu ở mọi bài** (đã đồng bộ `decision-tree` ↔
   `random-forest`) — người đọc nhận ra tầng bằng màu, không phải đọc lại chú thích.
2. **Một khái niệm — một chữ, dùng y hệt từ đầu tới cuối bài.** Hình toàn cảnh ghi ① BOOTSTRAP ·
   ② RANDOM FEATURES · ③ AGGREGATING thì ba tiêu đề mục sau phải mang đúng ba chữ đó. Không đổi
   sang từ đồng nghĩa cho "đỡ lặp".
3. **Rút gọn được cắt CÂU, không được cắt TÊN.** Khi rút gọn `random-forest` tôi đổi `out-of-bag`
   trong lab thành "bỏ ngoài" và gọi ρ là "mức sàn" — người dùng bắt lỗi ngay: *"bỏ ngoài vẫn để
   đúng thuật ngữ out-of-bag để liên kết xuyên suốt bài"*. Cách nói thường chỉ được đứng **cạnh**
   tên chuẩn để giải nghĩa lần đầu (`OOB = out-of-bag, nghĩa đen là nằm ngoài túi`).
4. **Bài con dùng lại thuật ngữ của bài prerequisite**, nói thẳng ở khối "Cần đọc trước".

## Phủ đủ kiến thức phổ biến của chủ đề

*"tham khảo nhiều nguồn để lấy ra những phần kiến thức độ nhận diện cao nhất, phổ biến là phải có"*.

Trước khi viết/sửa một bài kỹ thuật, tra vài nguồn dạy chủ đề đó (StatQuest, Analytics Vidhya,
Towards Data Science, KDnuggets, các bộ câu hỏi phỏng vấn) và liệt kê những mảnh **nguồn nào cũng
dạy**; thiếu mảnh nào thì bù. Với random forest danh sách đó là: bootstrap ~63,2% / OOB ~36,8% ·
bốc tập con cột ở **mỗi lần chia** · `max_features` √p và p/3 · majority vote vs averaging ·
**decorrelate** · MDI vs MDA · bẫy cột nhiều giá trị · bagging vs boosting · Extra Trees ·
không cần feature scaling.
