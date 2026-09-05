---
name: dot-luat-1-ke-02-python
description: "Đợt áp luật 1 (một bản đồ xuyên bài) lên các bài khó của kệ 02-python — đã xong 3 bài, số đo và các bẫy công cụ mới"
metadata:
  type: project
updated: 2026-09-05
---

Người dùng, sau bài thí điểm `transaction-isolation`: *"thử áp dụng vào các bài khó của python
tôi xem đã"*. Chọn bài theo cách đếm ở [[dot-sua-theo-chuan-bai-mau]] — bài nào nhiều mục mà ít
hình thì khó nhất.

## Đã xong

| Bài | Bản đồ mấy ô | Hình | Chữ | Chữ/hình |
|---|---|---|---|---|
| `thread-process-gil` | 5 | 9 | 1.207 | 134 |
| `asyncio` | 5 | 7 | 1.052 | 150 |
| `oop-python` | 6 | 7 | 952 | 119 |

Cả ba: `check.py` 0 lỗi · `build.py` sạch · probe 490px không tràn · 0 đoạn quá 33 từ.
Thước đo `random-forest` là 123 chữ/hình.

Kệ 02-python giờ **7/17 bài** theo luật 1 (thêm 4 bài cũ: `iterator-generator`,
`memory-management-gc`, `memory-model-mutability`, `dict-hash-table`).

## Bản đồ của từng bài — vẽ ra mới thấy xương sống thật

- `asyncio`: event loop → await → được (task vài KB) / mất (chặn là treo hết) → hệ thống thật.
  Ô cuối cố ý bắt tay sang bản đồ của `thread-process-gil` — hai bài cạnh nhau nên nối được.
- `oop-python`: **một** cơ chế (tra tên theo chuỗi instance → class → lớp cha) → **bốn** trụ dựng
  trên nó → ranh giới quy ước/ép buộc. Vẽ xong mới lộ ra ý chốt của bài: Python chỉ ép ở **đúng
  hai chỗ** (`@abstractmethod`, MRO không dựng được), còn lại đều là quy ước. Ý đó trước khi vẽ
  nằm rải rác khắp bài, không mục nào nói thẳng.

## Ba bẫy mới, sẽ dính lại

**Ô nửa bề rộng không chứa nổi tiếng Việt.** Bản đầu của bản đồ `oop-python` xếp bốn trụ thành
lưới 2×2 (ô rộng 163px, chữ được 147px) → **30 lỗi "chữ thò khỏi ô"**. Rút chữ chỉ về được 23.
Cách chữa đúng là **đổi cấu trúc**: bốn trụ xếp dọc hết bề rộng (h=42, bước 48), mỗi ô một dòng
phụ. Bản đồ dọc nhiều hàng dễ vừa hơn lưới, dùng nó làm mặc định.

**Regex đo đoạn dài bắt nhầm `<path>`.** `<p(?!re\b)[^>]*>` khớp luôn `<path .../>` trong SVG
inline, đẻ ra 7 "đoạn văn" 181–266 từ toàn nhãn hình. Phải **bỏ `<svg>…</svg>` trước khi đo**
và siết thành `<p(?![a-zA-Z])[^>]*>`.

**check.py sạch không có nghĩa là hình sạch.** Sơ đồ kim cương MRO của `o06` qua được check
(không chữ nào thò khỏi ô) nhưng ảnh chụp cho thấy hai ghi chú bên cạnh **đè lên** hộp B và C —
check chỉ đo bề rộng chữ, không đo va chạm giữa các phần tử. Hình có bố cục tự do (không phải
hàng/dải) thì **bắt buộc chụp ảnh xem**, đừng tin check.

## Còn lại của kệ này — 10 bài

`typing-dataclass` · `decorator-context-manager` · `exception-handling` · `scope-legb` ·
`data-model-dunder` · `performance-profiling` · `list-tuple-set` · `leetcode-toolkit` ·
và hai bài overview (`python-overview`, `language-core-overview`) — overview là **ngoại lệ
có chủ ý** theo luật 1, không tính là nợ.
