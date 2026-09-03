---
name: dot-sua-theo-chuan-bai-mau
description: "Đợt sửa 115 bài của kệ 01→05 theo chuẩn bài mẫu random-forest — số đo thật, đã làm gì, còn gì"
metadata:
  type: project
updated: 2026-09-04
---

Ngày 2026-09-03, sau khi chốt [[chuan-bai-mau]], người dùng yêu cầu *"sửa lại các bài đã làm từ
đầu cho tới ML"* — tức 115 bài đã viết của năm kệ 01→05 (bỏ qua bài khung).

## Cách đo cho đúng — đọc trước khi tin số

Bảng "số đo trước" của bản ghi cũ **sai**, đã xoá. Script đo đầu tiên đếm hình bằng
`count('<figure')` cộng thêm số class khuôn nên **đếm đôi**, và bắt bullet bằng `<li.*?</li>`
nên nuốt cả list lồng, đẻ ra bullet ma 956 từ và con số "50% bullet quá 25 từ".

Hai regex đúng, dùng lại khi cần đo:

- hình: `class="[^"]*\b(?:flow|strip|cmp|stack|mtx|axis|seq|bars|eq)\b` cộng `count('<svg')`
- bullet không lồng: `<li[^>]*>((?:(?!</?li).)*?)</li>`

## Đã làm

- **Bullet**: bảy lượt cắt, ~145 bullet ở kệ 02→05. Giờ 1011 bullet, trung bình **20,8 từ**,
  dài nhất **25**, không còn bullet nào quá giới hạn. Cắt câu chứ không cắt tên —
  xem [[thuat-ngu-chuan-va-nguon-tham-khao]].
- **Mục *Tổng kết một hình*** thêm cho 74 bài, đúng khuôn §11 của `random-forest`:
  `.key` một câu → `<figure class="scrollx">` bọc SVG tự vẽ, vùng đánh dấu ①②③④⑤ →
  `<figcaption>` chỉ cách đọc → `.why` bốn bullet, mỗi bullet gọi tên một khái niệm kèm số vùng.
- **Sửa lỗi hình**: 34 SVG có chữ rơi khỏi `viewBox` (bị cắt âm thầm) — nâng chiều cao lên
  `max(y)+8`. Không SVG nào dùng `--clay`; mọi SVG có `aria-label`.
- **Vị trí mục tổng kết**: phải là mục nội dung cuối, ngay trước *Lỗi hay gặp* / *Hỏi đáp*.
  Bốn bài đặt sai (`mle-map`, `ab-testing`, `overfitting-regularization`, `train-val-test-cv`)
  đã dời xuống.

| Kệ | Bài | Trạng thái |
|---|---|---|
| 01 DSA | 23 | **bỏ qua có chủ ý** — CLAUDE.md chốt khuôn DSA riêng, mục 01 đã là "1 hình + 1 câu chốt" |
| 02 Python | 17 | xong — 13 bài có mục tổng kết |
| 03 CS fundamentals | 14 | xong — 11 bài |
| 04 Database | 23 | xong — 19 bài |
| 05 Machine learning | 38 | xong — 31 bài (`random-forest` là bài mẫu) |

Bài **không** thêm mục tổng kết, cố ý: mọi bài `*-overview` (bản thân nó đã là bản đồ),
`leetcode-toolkit` (mục *Bảng tra nhanh* chính là bản tổng kết), `list-tuple-set`
(lõi bài là bảng chi phí ở mục 01, vẽ lại chỉ là chép bảng).

## Còn lại

**Mật độ hình vẫn xa bài mẫu.** `random-forest` là 123 chữ/hình; trung vị hiện tại theo kệ:
DSA 448 · Python 406 · CS 339 · Database 367 · ML 326. Đợt này mới cắt chữ và thêm một hình
tổng kết cho mỗi bài; việc *đưa hình về hình dạng chính của bài* trong từng mục thân bài thì
chưa đụng tới. Muốn kéo trung vị xuống thì phải đi lại từng mục, thay đoạn văn bằng khuôn hình —
xem [[it-chu-nhieu-hinh]].

## 2026-09-04 — đặt tên đầu mục + animation cho cả nhóm tree-models

Người dùng: *"Hai núm bù nhau? đừng đặt tên kiểu này với cả mới có random forest có animation"*.

**Tên gọi.** "Núm" là tiếng lóng tự chế, vi phạm luật đầu mục của CLAUDE.md. Đã quét sạch chữ
"núm" khỏi cả 6 bài (0 chỗ còn lại), kể cả trong `data-blurb`/meta và chữ trong SVG. Thay bằng
`hyperparameter` khi nói về khái niệm, `tham số` khi nói về một cái cụ thể.

**Animation.** Trước đó chỉ `random-forest` và `decision-tree` có lab. Đã viết thêm ba lab, mỗi
lab bám đúng cơ chế lõi của bài chứ không phải widget chung:

| Bài | Lab dựng cái gì |
|---|---|
| gradient-boosting | bảng phần dư co lại sau mỗi cây; nút η 0,1 / 0,3 / 1 — MSE 32,44 → 1,96 sau 6 cây |
| xgboost | gain và giá trị lá tính thẳng từ công thức của bài; hai núm λ, γ; 7 ngưỡng bấm được |
| lightgbm | hai cây mọc song song **cùng ngân sách lá** — leaf-wise vs level-wise |

`tree-family-overview` là bài overview, không có lab — đã xoá `lab.js` rỗng và thẻ `<script>` trỏ vào nó.

**Bẫy đã dính, đừng dính lại:** bản đầu của lab lightgbm cho bên level-wise mở *cả tầng* mỗi lượt,
nên sau 8 lượt là **256 lá vs 9 lá** và cây level-wise lại *sâu hơn* — ngược hẳn điều bài dạy.
Đúng phải là **mỗi lượt mỗi bên mọc thêm đúng một lá**, có vậy so sánh mới công bằng và mới ra
được kết quả đúng: 9 lá vs 9 lá, bên leaf-wise sâu 6 tầng còn level-wise 4, gain 41,3 vs 36,1.

Kiểm bằng Chrome headless: 6 bài, 0 lỗi JS, `scrollWidth` 480 ≤ 490 (không tràn ngang), auto-run chạy.

### Hình mở bài cho cả nhóm tree-models

Sáu bài của `06-tree-models` giờ đều có một `figure.gist` ngay dưới lede — xem luật 9 ở
[[chuan-bai-mau]]. Mỗi hình vẽ lại đúng câu lede của bài đó:

| Bài | Hình nói gì |
|---|---|
| tree-family-overview | một cây hay sai → rẽ hai hướng: song song lấy số đông, tuần tự chữa lỗi |
| decision-tree | cây yes/no ba tầng + bảng chấm điểm ngưỡng, ngưỡng thắng tô amber |
| random-forest | ba cột song song: mẫu bootstrap → Train → cây sâu → Predict → phiếu → gộp lại |
| gradient-boosting | ba cột nối nhau: dữ liệu → Train → cây nông → Predict → phần còn sai, phần sai vòng xuống làm dữ liệu cột sau; MSE 32,44 → 20,48 → 11,85 → 0,06 |
| xgboost | **cùng khung ba tầng như gradient-boosting**, cùng bộ 8 căn nhà, cùng mốc cây 1·2·20 — khác mỗi ô cây: hai lá ra thẳng từ `w* = − G / (H + λ)` |
| lightgbm | cột trái là vòng lặp boosting làm mờ, **chỉ ô cây tô sáng**, mũi tên "phóng to" sang hai cách mọc cây cùng 8 lá + khung "cái giá phải trả" |

Script sinh nằm ở `/tmp/gist_*.py` dùng chung `/tmp/gist_lib.py` — không commit, viết lại được
từ luật 9 nếu cần. CSS: `figure.gist` trong `assets/style.css`.

### Sửa lần hai: hình phải vẽ *cơ chế đang chạy*, không phải ba khung tĩnh

Người dùng đưa hình tham khảo (kiểu sơ đồ boosting hay gặp trên blog/sách): ba tầng
**dữ liệu → Train → cây → Predict → phần còn sai**, rồi mũi tên vòng phần còn sai xuống làm dữ
liệu cho cây kế tiếp. Bản đầu của hai hình `gradient-boosting` và `random-forest` chỉ là mấy khung
đặt cạnh nhau — thấy *kết quả* thay đổi nhưng không thấy *cái gì chảy đi đâu*, nên không nhớ được.

Rút ra, áp cho mọi hình mở bài sau này:

- **Vẽ đường đi của dữ liệu, đừng vẽ ảnh chụp từng chặng.** Có mũi tên đặt tên (`Train`,
  `Predict`) và có vòng hồi tiếp thì người đọc mới thấy được vòng lặp.
- **Bố cục phải khác nhau khi cơ chế khác nhau.** Boosting = chuỗi nối tiếp (mũi tên xanh vòng
  sang cột sau); random forest = ba cột song song không nối nhau, chỉ gặp nhau ở ô gộp phiếu.
  Nhìn hai hình cạnh nhau là thấy ngay khác biệt bagging vs boosting, không cần đọc chữ.
- **Cột cuối phải là lúc đã hội tụ.** Bản đầu vẽ cây 1·2·3, phần dư gần như không đổi nên hình vô
  nghĩa. Đổi cột ba thành **cây 20** (MSE 0,06, các vạch phẳng và xanh) thì mới thấy được kết quả.
  Số lấy từ chính lab của bài chạy lại bằng Python.
- **Nhãn trong hình phải ngắn.** "mọc hết cỡ · mỗi nút bốc ngẫu nhiên vài feature" tràn sang cột
  bên cạnh; tách phần giải thích ra cột chú thích bên phải.

### Sửa lần ba: bốn bài boosting phải dùng chung một khung hình

Người dùng: *"sao hình không còn tương đồng với gradient, tôi cần tương đồng cho có cảm giác cùng
style"*. Đúng — XGBoost và LightGBM **cũng là boosting**, mà hình lại vẽ theo bố cục riêng, nên đọc
xong không thấy chúng cùng một họ.

Cách chữa, dùng lại được cho mọi nhóm mà các bài là biến thể của nhau:

- **Cùng cơ chế thì cùng khung hình.** Ba bài boosting giờ dùng đúng một bố cục ba tầng
  (dữ liệu → Train → cây → Predict → phần còn sai), cùng toạ độ, cùng cỡ chữ. Random forest cố ý
  *khác* bố cục (ba cột song song) vì cơ chế nó khác thật.
- **Cùng dữ liệu, cùng mốc.** XGBoost chạy lại trên **đúng 8 căn nhà** của gradient-boosting, cùng
  ba mốc cây 1 · 2 · 20 (`g = F − y`, `h = 1`, `λ = 1`, `η = 0,3`, MSE 32,44 → 22,74 → 15,80 → 0,15).
  Đặt hai hình cạnh nhau là so được từng con số — không so được thì "cùng style" chỉ là trang trí.
- **Chỗ khác nhau thì tô sáng, phần giống thì làm mờ.** Hình LightGBM giữ nguyên vòng lặp nhưng
  bôi xám hết, chỉ ô *cây* để màu, rồi mũi tên "phóng to" kéo sang phần so sánh hai cách mọc.
  Người đọc thấy ngay: mọi thứ y hệt XGBoost, khác đúng một ô.
