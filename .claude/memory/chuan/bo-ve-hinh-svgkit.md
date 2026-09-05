---
name: bo-ve-hinh-svgkit
description: tools/svgkit là bộ vẽ hình dùng chung cho luật 1 — dùng nó, đừng chép sang /tmp; và ba chỗ máy soát KHÔNG bắt được
metadata:
  type: reference
updated: 2026-09-05
---

# Bộ vẽ hình luật 1 nằm ở `tools/svgkit/`, không ở `/tmp`

Ba đợt đầu áp luật 1 tôi chép `frame.py` / `check.py` / `shot.py` sang `/tmp` mỗi bài một bản,
và **cùng một lỗi lọt lưới ba lần** vì bản vá ở `/tmp/A` không về được `/tmp/B`. Giờ ba file
dùng chung nằm trong kho, chỉ `map.py` + `gen.py` của từng bài mới ở `/tmp/<slug>/`.

**Luật:** thấy một lỗi hình học lặp lại được ở bài sau thì **vá vào `check.py`**, không vá tay
ở bài đang làm. Vá xong chạy lại toàn bộ `.svg` của những bài đã xong để chắc bản vá không sinh
báo nhầm — `python3 tools/svgkit/check.py /tmp/rf/r*.svg /tmp/gb/g*.svg`.

## Hệ số bề rộng chữ phải ĐO, không được ước

Bảng `W` trong check.py là ước lượng "cỡ chữ × hệ số một ký tự". Ba đợt đầu tôi ước bằng mắt,
và hai lớp nhãn chữ hoa `sv-h` / `sv-hv` (có `letter-spacing`) ước hụt gần 30% — nên **mọi nhãn
panel dài đều lọt qua phép 1** mà máy vẫn báo sạch. Cách đo: dựng một trang chỉ có `<text>` mẫu,
mở bằng chrome headless, đọc `getComputedTextLength()` chia cho `len(s) × font-size`. Số thật là
`0.78` / `0.80`. Đo lại mỗi khi đổi font hoặc đổi `style.css`.

## Năm chỗ máy soát không bắt được

**1. Hình đúng hình học mà sai ý.** Biểu đồ early stopping của `gradient-boosting` vẽ **lộn
ngược**: trong SVG trục y tăng *xuống dưới*, nên "lỗi giảm dần" ra thành đường đi lên. check.py
báo 0 lỗi, mắt thấy ngay. **Mắc lại y hệt ở `xgboost`** (đường loss của hình x03) dù đã có ghi
chú này — đọc ghi chú không đủ, phải *dùng* hàm đổi trục ngay từ dòng đầu tiên của hàm vẽ. Vẽ đường cong thì viết hẳn một hàm đổi trục
(`py = lambda v: GY + 12 + (1 - v) * (GH - 24)`) rồi mọi điểm đi qua nó, thay vì tính nhẩm
từng toạ độ. Và **mốc đáng chú thích thì tính ra, đừng đoán**: `tstar = min(ts, key=val)` cho
chấm "điểm dừng" rơi đúng đáy thật của đường validation.

**2. Số trong hình bịa.** Bảng minh hoạ mà cộng không ra thì người đọc kỹ sẽ mất lòng tin vào
cả bài. Chốt bằng `assert` ngay trong hàm vẽ:
`assert abs(sum(abs(x) for x in r1) - 3.0) < 1e-9, 'phần dư phải co lại một nửa'`.
Chi phí gần bằng 0, và nó chặn được đúng loại lỗi không ai soát lại.

**3. Chữ SÁT chữ, không đè.** Hình d04 của `decision-tree` render ra `0,50lẫn nhất` vì cột chú
thích đặt cách con số đúng 2px. Phép "chữ đè chữ" chỉ bắt khi hai hộp **giao nhau thật** — sát
nhau thì nó im. Đã vá thành phép 5 (hở dưới 5px là báo), nhưng bài học chung còn đúng: mọi phép
soát viết theo kiểu "giao nhau" đều mù với "kề nhau", mà mắt thì không phân biệt hai thứ đó.

**4. Đường kẻ cắt ngang chữ.** Cả sáu phép đều so **chữ với chữ** hoặc **chữ với ô** — không
phép nào so chữ với một `<line>`/`<path>`. Hình x03 của `xgboost` có đường đứt nét gióng từ đáy
parabol xuống trục, chạy xuyên qua đúng giữa nhãn `đáy f* = − g/h`; máy báo sạch. Vẽ đường gióng
thì hoặc bỏ hẳn, hoặc đặt nhãn lệch sang bên. Ảnh chụp là cách duy nhất thấy được.

**5. Chạy check.py trên cả `index.html`.** Một bài mười hình, mỗi hình một hệ toạ độ riêng;
gộp phẳng thành một mặt phẳng thì sinh hàng chục va chạm ma. **Chạy từng file `.svg`** mới là
bản đúng.

## Bẫy Python đã mắc

`hl=()` — tô sáng *không ô nào*, dùng cho hình "cả bản đồ tắt". Tập rỗng là **falsy**, nên
`keys and not (keys & LOOP)` short-circuit và hộp vẫn sáng trắng. Phải viết
`keys is not None and not (...)`. Cùng loại với mọi chỗ phân biệt "rỗng" với "không truyền".

Xem thêm [[chuan-bai-mau]] (luật 1 là gì), [[it-chu-nhieu-hinh]] (đo bằng chữ/hình),
[[sua-nhanh-it-vong-kiem]] (khi nào cần chụp ảnh).
