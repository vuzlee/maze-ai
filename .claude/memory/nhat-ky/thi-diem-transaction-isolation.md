---
name: thi-diem-transaction-isolation
description: "2026-09-05 · bài thí điểm luật 1 khó nhất (transaction-isolation, 16 mục): bộ công cụ sinh hình dùng lại được, và bốn bẫy phát hiện khi làm thật"
metadata:
  type: project
updated: 2026-09-05
---

Người dùng: *"hãy làm bài khó nhất để có thể rút ra được những improvements hay lỗi, nhằm sau áp
dụng lên tất cả"*. Chọn bài bằng cách xếp hạng **nhiều mục nhất × ít SVG sẵn nhất**:
`transaction-isolation` — 16 mục, 2 SVG, 3.677 chữ. Xong: **14 hình**, mục 01 mang bản đồ,
mục *Tổng kết một hình* cũ đã xoá, còn **2.656 chữ**, 0 đoạn quá 33 từ, `build.py` sạch.

## Bản đồ 6 ô, và vì sao dàn ý đổi theo

Bản đồ đọc ra từ chính nội dung bài, không phải từ danh sách mục:

```
Transaction  →  chạy song song  →  Hiện tượng ĐỌC | Hiện tượng GHI
                                        ↓ chữa bằng ↓
                                 Isolation level  | Sửa ở câu lệnh
                                 ─────── Cái giá ───────
```

Vẽ xong thì **dàn ý cũ lộ ra là sai**: mục 03 cũ tên *"Bốn hiện tượng dị thường"* gộp cả lost
update vào — nhưng lost update thuộc ô GHI, ba cái kia thuộc ô ĐỌC. Đã tách thành *Ba hiện tượng
đọc* (03) và *Lost update* (04). Đây đúng là điều luật 1 hứa: **hình sai thì dàn ý sai theo**,
và hình bắt được lỗi phân loại mà đọc chữ không thấy.

Ô `cost` sinh ra vì ba mục cuối (deadlock · transaction dài · thử lại) không thuộc ô nào —
dấu hiệu bản đồ thiếu nhánh, không phải dấu hiệu bài thừa mục.

## Bộ công cụ — chép lại cho bài sau, đừng viết lại

Bốn file ở `/tmp/`, không commit (hình đã nằm trong HTML rồi):

| File | Việc |
|---|---|
| `frame.py` | `frame(hl)` → `(elems, bottom_y)`; `hl` nhận **một tên ô hoặc một tập tên ô** (lab sáng 3 ô cùng lúc). Kèm `txt/rect/vline/hline/lens/panel` |
| `gen2.py` | mỗi mục một hàm `dNN(e)` vẽ panel phải; `SPECS` ghép (ô sáng, tiêu đề panel, hàm vẽ, tên file, aria-label) |
| `check.py` | đo bề rộng chữ theo đúng font-size của `style.css`, bắt ba lỗi: chữ ra ngoài `viewBox`, chữ đè chữ, chữ tràn khỏi khung `rect` của nó |
| `apply.py` | ráp HTML: mỗi mục là một chuỗi trong list `S`, hình chèn bằng `fig(name, caption)`; đánh số `<b>NN</b>` và `id` tự sinh |

Toạ độ chốt: bản đồ rộng **340**, panel phóng to từ **x=372 rộng 488**, `viewBox="0 0 860 H"`.
`figure.gist` cho mục 01, `figure.scrollx` cho các mục sau (SVG min-width 640 / 720 trong CSS).

**`check.py` đáng giá nhất.** Nó bắt được 4 chỗ chữ tràn panel mà mắt nhìn ảnh chụp không thấy.
Quy trình: sinh → `check.py` phải 0 lỗi → mới chụp ảnh xem bố cục.

## Bốn bẫy, sẽ dính lại ở bài sau

1. **Số hình phải bằng số mục nội dung.** Bản đầu chỉ vẽ 7 hình cho 16 mục vì vẽ theo *ô* (6 ô →
   7 hình). Sai: mỗi **mục** một hình, nhiều mục cùng soi một ô thì panel phải khác nhau —
   `iso` có 3 hình (bốn mức · MVCC · snapshot chụp lúc nào), `cost` có 3.
2. **`figcaption` lặp là rác.** Bản đầu mỗi hình đều mở đầu bằng cùng một câu 25 từ dạy cách đọc
   bản đồ → 11 lần lặp, cộng ~275 chữ vô ích. Cách đọc bản đồ nói **đúng một lần** ở
   `figcaption` mục 01; caption các mục sau chỉ nói **phần panel phải**.
3. **Hình thay được khối code thì phải xoá khối code.** Mục *Khoá* có `<pre>` liệt kê 4 biến thể
   `FOR UPDATE`, mà hình đã liệt kê đúng bốn dòng đó — giữ cả hai là chép hai lần. Giữ lại đúng
   dòng cú pháp chính. Đây là luật 2 (hình *thay* văn xuôi) áp cho `<pre>`, dễ quên.
4. **Đo lại đoạn dài sau khi ráp.** Ráp xong đẻ ra 4 đoạn mới quá 33 từ (câu nối vào hình).
   Regex đo phải bỏ `<details>` (Hỏi đáp) và `p.lede` — hai thứ này có ngoại lệ riêng, không bỏ
   thì báo động giả 11 lỗi.

## Số đo — mật độ hình

`random-forest` là 123 chữ/hình. Bài này giờ **2.656 chữ / 14 hình = 190 chữ/hình**, từ mức cũ
1.839 (3.677 chữ / 2 hình). Trung vị kệ 04 trước đợt là 367. Nghĩa là **làm đúng luật 1 kéo mật
độ về gần bài mẫu mà không cần cắt nội dung** — chữ giảm 28% chỉ nhờ bỏ caption lặp, bỏ code
trùng hình, và bỏ mục tổng kết cuối.

## Còn nợ của chính bài này

Khuôn `.seq`/`.stack`/`.cmp`/`<table>` trong bài **về 0** — mọi hình giờ là SVG bản đồ. Chưa rõ
đó là tốt tuyệt đối hay mất đi cái lợi "khuôn rẻ, tự co giãn" của [kit.html](../../../kit.html);
bài `memory-management-gc` cũng 0 khuôn nên có thể đây là hình dạng đúng. **Xem lại sau vài bài.**

Xem [[chuan-bai-mau]] luật 1, [[dot-sua-theo-chuan-bai-mau]] cho danh sách 85 bài còn nợ.
