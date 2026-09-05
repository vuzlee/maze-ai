# svgkit — bộ vẽ hình cho luật 1

Ba đợt đầu áp luật 1 tôi chép lại `frame.py` / `check.py` / `shot.py` sang `/tmp`
mỗi lần một bản, và cùng một lỗi lọt lưới ba lần. Đây là bản dùng chung.

## Ba file

| File | Việc |
|---|---|
| `base.py` | primitive SVG + ba khuôn hàng của panel phải. Không chứa bản đồ nào. |
| `check.py` | soát chồng lấn bằng ước lượng bề rộng chữ — **6 phép** |
| `shot.py` | chụp ảnh từng hình, hoặc chụp cả trang bài |

Bản đồ riêng của từng bài viết trong thư mục nháp của bài (`/tmp/<slug>/map.py`),
không đưa vào đây — mỗi bài một mental model, không dùng lại được.

## Khuôn một bài

```python
import sys; sys.path.insert(0, 'tools/svgkit')
from base import *
from map import frame          # frame(hl) -> (elems, bottom_y)

def d05(e):                    # phần bóc ô của mục 05
    e.append(lens(196, 46))    # đường cong nối ô đang sáng sang panel
    y = title(e, 'Câu tiêu đề của panel', 'var(--ok)')
    y = row(e, y, 'nhãn trái', 'giải thích phải', *GREEN)
    y = band(e, y, PANW, *AMBER, 'Câu đậm', 'Câu nhỏ nằm trong ô')
    return y

e, bot = frame('cell_key')
e.append(panel('PHÓNG TO — TÊN Ô'))
y = d05(e)
build(e, max(bot, y), 's05', 'mô tả cho screen reader', '/tmp/slug')
```

## Ba khuôn hàng, chọn theo chỗ đặt chú thích

- `band(...)` — câu đậm + câu nhỏ, **cả hai nằm trong ô**. An toàn nhất.
- `row(...)` — ô có viền bên trái, chú thích trần bên phải, **cùng một dòng**.
- `stack(...)` — ô có viền, chú thích **nằm dưới ô**. Đây là chỗ hay sinh lỗi:
  bước `y` phải vượt qua viền dưới, nên hàm tự cộng `GAP = 18`. Tự viết tay
  `y += 8` sau một hàng ô là tái tạo đúng lỗi đã mắc ba lần.

## check.py — sáu phép, và cái nó KHÔNG làm

1. chữ tràn khỏi viewBox · 1b. **ô tràn khỏi viewBox** · 2. chữ đè chữ
3. chữ thò ngang khỏi ô bao nó
4. **chữ cắt ngang viền một ô** — hoặc nằm hẳn trong, hoặc nằm hẳn ngoài.
5. **chữ sát chữ dưới 5px** — không đè nhau nên phép 2 im, mà mắt đọc ra dính liền.

Phép 1b sinh ở bài `gradient-boosting`: phép 1 chỉ soi `<text>`, nên một ô vẽ
hụt xuống dưới đáy khung thì máy im lặng — chỉ ảnh chụp mới thấy nó bị cắt ngang.

Phép 5 sinh ở bài `decision-tree`: hình d04 rendered ra `0,50lẫn nhất` vì cột chú
thích đặt cách con số đúng 2px. Phép 2 chỉ bắt khi hai hộp **giao nhau thật**, sát
nhau thì im — nên khoảng hở dưới 5px giờ cũng bị báo. Cặp nằm hai bên máng bản
đồ | panel (`x = PANX`) được miễn, vì ở đó khoảng hở thật là 32px và cái "dính" chỉ
là phần ước bề rộng dư ra.

Phép 4 sinh sau ba đợt đầu, khi bản kiểm cũ báo sạch mà ảnh chụp vẫn thấy caption
đè lên viền dưới của hàng ô ngay trên nó. Chỗ tinh: chữ **có dấu tiếng Việt vươn
cao hơn** chữ Latin trần (mũ chồng dấu thanh), nên `ASC_ACCENT = 1.0` chứ không
dùng chung `0.8` — dùng chung là lý do lỗi lọt.

Hệ số bề rộng trong bảng `W` **đo bằng máy**, đừng ước bằng mắt: dựng một trang
chỉ có `<text>` mẫu, mở bằng chrome headless rồi đọc `getComputedTextLength()`.
Hai lớp nhãn chữ hoa `sv-h`/`sv-hv` có `letter-spacing` nên rộng hơn hẳn — đo ra
`0.78`/`0.80` chứ không phải `0.72`/`0.62` như bản đầu, và chính chỗ ước hụt đó
làm mọi nhãn panel dài lọt qua phép 1.

Nó chỉ đúng với hình **sinh từ `base.py`**. Chạy trên hình cũ vẽ tay sẽ ra hàng
trăm báo nhầm, vì bề rộng chữ là ước lượng và `text-anchor` bên đó dùng khác.
Đừng dùng nó làm máy quét toàn kho.

Một chỗ mù còn lại, theo cấu trúc: cả sáu phép so **chữ với chữ** hoặc **chữ với ô**, không
phép nào so chữ với một `<line>`/`<path>`. Đường gióng của hình x03 (`xgboost`) chạy xuyên qua
giữa nhãn `đáy f* = − g/h` mà máy báo sạch. Vẽ đường gióng thì hoặc bỏ, hoặc đặt nhãn lệch bên.

Và nó **không thay được mắt**: nó không biết hình có nói đúng ý không, bố cục có
đọc ra câu định nghĩa không, màu có đúng nghĩa không. Chụp ảnh vẫn là bước cuối.
Bằng chứng: biểu đồ early stopping của `gradient-boosting` vẽ **lộn ngược** —
trong SVG trục y tăng xuống dưới, nên "lỗi giảm dần" ra thành đường đi lên. Máy
báo 0 lỗi, mắt thấy ngay. Vẽ đường cong thì viết hẳn một hàm đổi trục
(`py = lambda v: GY + 12 + (1 - v) * (GH - 24)`) thay vì tính nhẩm từng điểm.

Còn một chỗ hay báo nhầm: **đừng chạy nó trên cả file `index.html`**. Một bài có
mười hình, mỗi hình một hệ toạ độ riêng; gộp lại một mặt phẳng thì sinh hàng chục
va chạm ma. Chạy từng file `.svg` mới là bản đúng.
