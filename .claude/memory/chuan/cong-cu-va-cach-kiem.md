---
name: cong-cu-va-cach-kiem
description: "Bộ công cụ kiểm (soat.py 8 phép, svgkit) + luật kiểm lại chính cái thước + chạy bao nhiêu vòng cho mỗi loại sửa"
metadata:
  type: reference
updated: 2026-09-08
---

Gộp từ `soat-tu-dong-8-phep` + `bo-ve-hinh-svgkit` + `kiem-lai-chinh-cai-thuoc` + `sua-nhanh-it-vong-kiem`.

## Luật gốc: luật kiểm được bằng máy thì nằm trong `tools/`, không viết script tạm

Ba lần liền tôi viết lại từ đầu một đoạn Python đếm cùng những thứ đó, mỗi lần một kiểu, nên số đo
giữa các phiên không so được. `tools/soat.py` in 8 nhóm + tổng chung; `tools/svgkit/` là bộ vẽ và
kiểm hình dùng chung — **đừng chép sang `/tmp`** (ba đợt đầu chép đi chép lại, cùng một lỗi lọt
lưới ba lần vì bản vá ở `/tmp/A` không về được `/tmp/B`). Chỉ `map.py` + `gen.py` của từng bài mới
ở `/tmp/<slug>/`. Thấy lỗi hình học lặp được ở bài sau thì **vá vào `check.py`**, rồi chạy lại
toàn bộ `.svg` của những bài đã xong để chắc bản vá không sinh báo nhầm.

## `tools/soat.py` — 8 phép

| # | Phép soát | Ngưỡng / cách bắt |
|---|---|---|
| 1 | Link trỏ vào bài còn là khung | `data-skeleton="1"` |
| 2 | Màu viết cứng trong bài | hex ngoài `:root` — thêm token chứ đừng để hex |
| 3 | `--clay` dùng trong hình | cam đất là màu thương hiệu, không mang nghĩa nội dung |
| 4 | Đầu mục đếm số | "Ba bẫy", "Bốn thao tác" |
| 5 | Dòng code quá 92 ký tự | tràn ngang trên mobile |
| 6 | Thuật ngữ bị dịch | bảng `DICH` + `MIEN` (miễn một bài) + `KE_RIENG` (khoanh một kệ) |
| 7 | `<title>` lệch `data-title` | phải **mở đầu** bằng `data-title` |
| 8 | Nợ luật 1 | >2500 từ **hoặc** >10 mục mà chưa có `figure.gist`, hoặc có mà `nsvg < nsec-2` |

Ghi chú vận hành: phép 6 quyết định "có phải thuật ngữ không" theo [[thuat-ngu]], không theo cảm
giác. Phép 7 nới đúng một mức — phụ đề sau dấu — thì được (`binary search — mọi biến thể`), sai là
khi chính **cái tên** khác nhau. **Phép 8 là danh sách việc, không phải pass/fail**: sắp theo số
từ giảm dần, làm từ bài dài xuống.

**Bẫy:** cắt một hình ra khỏi mục có thể **làm vỡ phép 8** (nó đếm theo mục thiếu hình). Đã dính ở
`linear-regression` §08 — chữa bằng cách thay khối bị cắt bằng một `.bars` gọn, không phải bằng
cách trả lại đoạn văn cũ.

## Kiểm lại chính cái thước — quan trọng hơn cả kết quả

Một bảng nghiệm thu **toàn số 0 không chứng minh gì** nếu chưa kiểm cái thước sinh ra nó. Thước
hỏng và bài sạch in ra **cùng một dòng**, không có cảnh báo nào phân biệt hộ. Ngày 07/09 hai lỗi
đo liên tiếp lọt qua, và lỗi đếm dư khiến tôi **hành động** theo nó — tách nhầm, **hỏng 81 file**.

1. **Thước nhận danh sách file thì phải in số file đã đọc.** `TONG 0` mà không kèm `128 bài` là vô
   nghĩa — có thể `sys.argv[1:]` rỗng. Đây đúng là chuyện đã xảy ra.
2. **Chép regex từ file chuẩn, đừng viết lại từ trí nhớ.** Bản chép thiếu `(?![^>]*class=)` biến
   10 vi phạm thành 144. Regex chuẩn của luật 8 ở `chuan-bai-mau.md:398`.
3. **Chạy thử trên một chỗ đã biết là SAI trước.** Thước không bắt được chỗ sai đã biết thì thước
   hỏng. Phép thử rẻ nhất, và bỏ qua nó là gốc của cả hai lỗi trên.
4. **Số vi phạm cao bất thường = nghi thước trước, nghi bài sau.**
5. **Sao lưu trước mọi lượt sửa hàng loạt**, khôi phục bằng `cp` từng file — đừng `rm -rf` cả cây.
6. Bẫy đo đã dính: quên bỏ `<details>`/`<figure>` thì số thổi lên 7 lần (469 → thật là 65);
   `s.count('</b>')` bắt luôn `</body>` nên báo lệch ở đúng 116/116 file — **đếm chuỗi không thay
   được `html.parser`**.

> **`check.py` là SÀNG, `getBBox` là TRỌNG TÀI.** `check.py` kêu 21 chỗ ở 9 bài, `getBBox` thật đo
> **0** ở cả 9. Chỉ sửa hình khi bbox thật cũng kêu — sửa theo mình `check.py` là đi dời chữ trong
> những hình vốn không sao. Ngược lại, cả hai thước cùng chỉ một chỗ thì đó là thật.

Ba lỗi của chính `check.py` đã sửa: đưa cả file HTML vào `check()` (nó nhận đúng MỘT `<svg>`) làm
`parse()` vớ phải icon kính lúp 24×24 → `svm` báo 190 lỗi ma · bảng bề rộng lấy theo chữ rộng nhất,
phồng ~10% · phép 3 đoán ô bao bằng ô nhỏ nhất phủ điểm neo nên chữ `text-anchor="end"` rơi vào ô
bên cạnh. **Hệ số bề rộng chữ phải ĐO, không ước** — dựng trang mẫu, chrome headless,
`getComputedTextLength()/(len×font-size)`; số thật là `0.78`/`0.80`. Đo lại mỗi khi đổi font/CSS.

## Bảy chỗ máy soát KHÔNG bắt được

1. **Hình đúng hình học mà sai ý.** Trục y của SVG tăng *xuống dưới*, nên "lỗi giảm dần" vẽ ra
   thành đường đi lên — dính ở `gradient-boosting` rồi **dính lại y hệt ở `xgboost`** dù đã có ghi
   chú. Đọc ghi chú không đủ: viết hẳn một hàm đổi trục (`py = lambda v: GY+12+(1-v)*(GH-24)`) rồi
   mọi điểm đi qua nó. Mốc đáng chú thích thì **tính ra** (`tstar = min(ts, key=val)`), đừng đoán.
2. **Số trong hình bịa.** Chốt bằng `assert` ngay trong hàm vẽ. Chi phí gần bằng 0.
3. **Chữ SÁT chữ, không đè.** `0,50lẫn nhất` vì cột chú thích cách con số đúng 2px. Mọi phép viết
   theo kiểu "giao nhau" đều mù với "kề nhau", mà mắt thì không phân biệt hai thứ đó.
4. **Đường kẻ cắt ngang chữ.** Không phép nào so chữ với `<line>`/`<path>`. Ảnh chụp là cách duy nhất.
5. **Chạy `check.py` trên cả `index.html`** — mười hình mười hệ toạ độ, gộp phẳng sinh va chạm ma.
   **Chạy từng file `.svg`.**
6. **Hình học của khuôn HTML nói ngược đoạn văn.** `.cmp two` là hai cột song song = "chọn A hoặc
   B"; `dsa-overview` §02 dùng nó cho *giải thuật / cấu trúc dữ liệu* trong khi câu dưới nói giải
   thuật **chạy trên** cấu trúc. Soát tay: đọc hình trước, đọc chữ sau, hỏi hai thứ có nói cùng
   một câu không.
7. **Một màu một nghĩa — tính TRONG từng hình.** `--tomb` không được vừa làm màu nhấn vừa mang
   nghĩa "sai" trong cùng một hình.

Bẫy Python: `hl=()` (tô sáng không ô nào) là **falsy**, nên `keys and not (keys & LOOP)`
short-circuit và hộp vẫn sáng. Phải viết `keys is not None and not (…)`.

## Chạy bao nhiêu vòng — đừng chụp ảnh cho mọi lần sửa

*"tôi thấy sao sửa cái gì cũng lâu vậy?"* — nói về quy trình, không phải nội dung. Ảnh chụp chỉ
bắt được lỗi **nghĩa** (nhãn khó hiểu, figcaption mô tả sai hình); sửa câu chữ không sinh loại lỗi đó.

| Loại sửa | Chạy gì |
|---|---|
| Chỉ chữ trong bài, lede, figcaption | `gen` → `build` → `tools/build.py`. **Không chụp.** |
| Đổi màu / class / token CSS | thêm `check.py`. Chụp **một** hình đại diện. |
| Đổi toạ độ, thêm/bớt ô trong hình | đủ ba chặng — chụp **một** hình + **một** ảnh top trang. |
| Dựng bài mới | đủ ba chặng, chụp hết. |

Và **gộp lệnh**: sinh cả ba bài + `tools/build.py` trong một lượt bash.
Chụp headless ở 430px thì trang nào cũng bị cắt, kể cả trang chưa sửa — tật của công cụ, không
phải lỗi bố cục. Muốn xem nhiều khối `.eq` cùng lúc thì sinh trang gộp ở `/tmp` **nhúng
`assets/style.css` đọc lại từ đĩa**, không thì ảnh chụp nói dối bằng CSS cũ.
