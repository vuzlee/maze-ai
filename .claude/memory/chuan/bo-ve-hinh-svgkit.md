---
name: bo-ve-hinh-svgkit
description: tools/svgkit là bộ vẽ hình dùng chung cho luật 1 — dùng nó, đừng chép sang /tmp; và bảy chỗ máy soát KHÔNG bắt được
metadata:
  type: reference
updated: 2026-09-07
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

## Bảy chỗ máy soát không bắt được

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

**6. Hình học của khuôn HTML nói ngược lại đoạn văn.** `.cmp two` là hai cột song song — hình
học đó có nghĩa **"chọn A hoặc B"**. `dsa-overview` §02 dùng nó cho *giải thuật / cấu trúc dữ
liệu*, trong khi câu ngay dưới nói giải thuật **chạy trên** cấu trúc. Không phép nào bắt được vì
lỗi nằm giữa hình và chữ, không nằm trong hình. Soát tay: **đọc hình trước, đọc chữ sau, hỏi hai
thứ có nói cùng một câu không** — hình sai ý tệ hơn không có hình.

**7. Một màu một nghĩa — tính TRONG từng hình.** Quy ước bốn màu là toàn kho, nhưng chặt hơn:
trong một hình, `--tomb` không được vừa làm màu nhấn cho một mục vừa mang nghĩa "sai". Bản đầu
của `cs-map` tô lớp Messaging đỏ chỉ để phân biệt với ba lớp kia; sửa thành cả bốn lớp xanh, đỏ
chỉ dành cho kiểu hỏng mà mỗi lớp mua thêm.

## Bẫy Python đã mắc

`hl=()` — tô sáng *không ô nào*, dùng cho hình "cả bản đồ tắt". Tập rỗng là **falsy**, nên
`keys and not (keys & LOOP)` short-circuit và hộp vẫn sáng trắng. Phải viết
`keys is not None and not (...)`. Cùng loại với mọi chỗ phân biệt "rỗng" với "không truyền".

Xem thêm [[chuan-bai-mau]] (luật 1 là gì), [[it-chu-nhieu-hinh]] (đo bằng chữ/hình),
[[sua-nhanh-it-vong-kiem]] (khi nào cần chụp ảnh).

## `check.py` là SÀNG, `getBBox` là TRỌNG TÀI (07/09)

Ba lỗi chồng nhau, tìm ra khi soát `svm` sau đợt sửa `hard margin`:

1. **`__main__` đưa cả file HTML vào `check()`** — mà `check()` nhận đúng MỘT `<svg>`. `parse()`
   vớ phải `viewBox` đầu tiên là **icon kính lúp 24×24** trong thanh tìm kiếm, rồi đo mọi hình
   bằng khung 24×24 → `svm` báo **190 lỗi**, toàn bộ là ma. Đã sửa: lặp từng `<svg>` có `<text>`,
   và in kèm `[svg i]` để biết hình nào.
2. **Bảng bề rộng lấy theo chữ RỘNG NHẤT**, phồng ~10%. Đo thật bằng `getBBox` trên vài trăm nhãn:
   `sv-s` thật tối đa 5,58/ký tự chứ không phải 6,33. Đã hiệu chỉnh cả bảng theo trần đo thật + 3%.
3. **Phép 3 đoán ô bao bằng ô nhỏ nhất phủ điểm neo** — chữ `text-anchor="end"/"middle"` neo ở mép
   nên rơi vào ô hàng xóm rồi bị kết là "thò ra". Không chữa được bằng nới `TOL`; đã ghi rõ trong
   header của `check.py`.

Kết cục: `check.py` kêu 21 chỗ ở 9 bài, **`getBBox` thật đo 0 ở cả 9**. `TOL` nâng 0,5 → 12px cho
đúng biên sai số của phép ước theo ký tự.

> **Luật:** `check.py` chỉ khoanh vùng nghi. **Chỉ sửa bài khi bbox thật cũng kêu.** Sửa theo mình
> `check.py` là đi dời chữ trong những hình vốn không sao.

Ngược lại, cả hai thước cùng chỉ một chỗ thì đó là thật: 5 cặp nhãn ở `iterator-generator` và
`memory-management-gc` xếp cách nhau 14px (chuẩn của kho là 18px) — nới ra 17–18px là hết.
Xem thêm [[kiem-lai-chinh-cai-thuoc]].
