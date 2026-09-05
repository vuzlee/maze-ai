---
name: chuan-bai-mau
description: "Random forest & bagging là bài mẫu của kho — chín luật rút ra từ nó, dùng để sửa mọi bài khác"
metadata:
  type: feedback
updated: 2026-09-04
---

Ngày 2026-09-03, sau khoảng mười lượt review liên tiếp riêng bài
[Random forest & bagging](../../../content/05-machine-learning/06-tree-models/random-forest/index.html),
người dùng chốt: *"hãy coi đây là 1 bài chất lượng"* và yêu cầu sửa các bài đã viết theo nó.

**Vì sao.** Trước đó mỗi lượt sửa chỉ chữa một triệu chứng (chữ nhiều quá, hình rối, bullet dài,
công thức khó). Bài random-forest là chỗ đầu tiên cả bảy thứ cùng đúng một lúc, nên nó thành
**thước đo cụ thể** thay cho các nhận xét rời rạc — có số để đo, không phải cảm tính.

**Số đo của bài mẫu:** 2.577 chữ · 21 hình · **123 chữ/hình** · 43 bullet, trung bình **14,7 từ**,
dài nhất 24 · 13 mục · **0 khối `<pre>`**.

## Tám luật

1. **Chỉ hai hình dạng: bảng dữ liệu và cây.** *"cứ đưa về hình thù dạng data bảng / cây cho thân
   thiện chứ không mỗi bài lại 1 hình thì rất mệt để hiểu"* — mỗi bài chọn 1–2 hình dạng rồi lặp
   lại chúng suốt bài. Người đọc học cách đọc hình **một lần**, không phải học lại ở mỗi mục.
   Hình dạng chọn theo chủ đề: DSA thì mảng + con trỏ, database thì bảng + sơ đồ quan hệ,
   networking thì `.seq` + `.stack`.

   **Dạng mạnh nhất của luật này: một bản đồ duy nhất, mỗi mục sáng đúng một ô.** Ý của người dùng,
   2026-09-04: mental model là tổng quan, mỗi mục dưới là **phóng to một ô của chính nó**. Cách vẽ:
   bản đồ được vẽ lại **nguyên xi ở mọi hình**; ô đang học đủ màu, phần còn lại xám (`--rule` +
   `--faint` + nền `--panel`), và một đường gạch nối sang panel phóng to bên phải. Người đọc học
   cách đọc hình đúng một lần, và **luôn biết mình đang đứng ở đâu** trong bức tranh chung.
   Cài bằng một hàm `frame(hl)` trả về danh sách phần tử — thêm mục mới chỉ là gọi với ô khác,
   không vẽ lại bố cục. Mẫu:
   [Memory management & GC](../../../content/02-python/02-language-core/memory-management-gc/index.html)
   — tám hình, một bản đồ bốn ô.

   **Người dùng chốt lại sau khi thấy bản làm xong** (2026-09-04): *"1 hình mental, xong bóc tách
   dần nó rất liên kết tuần tự và dễ hiểu, đúng như ý tưởng học dễ, tuyến tính mà tôi cố gắng
   truyền tải"*. Nên đây **không phải quy ước vẽ hình, mà là thứ tự học**: hình mental model ở mục
   01 là *toàn bộ bài nói trước một lần*, mỗi mục sau **bóc ra đúng một ô** theo thứ tự đã có sẵn
   trên hình. Người đọc không bao giờ gặp khái niệm rơi từ trên trời — trước khi học nó, họ đã
   nhìn thấy ô của nó và biết nó nằm cạnh cái gì.

   Hệ quả về cách soạn: **thứ tự các mục phải đọc ra được từ chính bản đồ**. Vẽ bản đồ trước, dàn ý
   là hệ quả — không phải viết mục trước rồi vẽ hình minh hoạ sau. Bố cục bản đồ mà không gợi ra
   được một đường đi tuyến tính thì bản đồ sai, không phải dàn ý sai. Ở bài mẫu: bản đồ hai nhánh
   nên bài đi *cơ chế chính (03) → lỗ hổng của nó (04) → thứ vá lỗ hổng (05)*, và ba mục cuối là ba
   ô còn lại của bản đồ.

2. **Bullet ngắn nhất có thể** — *"nội dung các bullet cả bài cần ngắn gọn nhất, tối giản nhất"*.
   Mốc: **trung bình ≤ 15 từ, không câu nào quá 25**. Cả kho hiện có 737 bullet, **50% đang quá
   25 từ** — đây là việc sửa nhiều nhất.

3. **Dãy việc nối tiếp dùng `ul.steps`, ý song song dùng `ul.why` không gạch ngang.**
   *"mấy cái bullet này cứ bị có gạch ngang làm mất sự liên kết của mắt"*. `.steps` là số thứ tự
   trong vòng tròn nối bằng một vạch dọc liền, mục cuối gắn `class="end"` thành dấu ✓.

4. **Không để code trong mục khái niệm** — *"đừng để code ở đây"*. `<pre><code>` chỉ còn đúng chỗ
   của nó: bài DSA mục *Mẫu code cần thuộc*, bài Python/SQL dạy cú pháp. Câu "gọi hàm nào của thư
   viện" viết thành một dòng chữ, không phải một khối code.

5. **Công thức dùng `.eq` + `<dl>` giải nghĩa từng ký hiệu tại chỗ** ([[khuon-eq-cong-thuc]]).
   Không ký hiệu nào được xuất hiện trước khi có nhãn của nó. Kết bằng `<p class="read">` nói
   công thức **đọc ra nghĩa gì**.

6. **Lab là bảng dữ liệu thật, và tự chạy tiếp khi đủ điều kiện.** *"người nhìn vào cách lấy dữ
   liệu từ 1 bảng sẽ gần gũi hơn là dạng list thế kia"*, *"hình dạng bảng, ô, trực quan to đọc dễ
   hơn, rõ ràng từng ô"*, *"cái trồng cây tự động đi khi rút đủ"*. Ô to, viền rõ từng ô, chữ căn
   giữa; đừng cắt bớt cột cho gọn — gọn là ở cách trình bày, không phải ở lượng dữ liệu.

7. **Mỗi bài đóng bằng một mục "Tổng kết một hình"** — một hình duy nhất ráp lại toàn bài,
   dán đúng thuật ngữ chuẩn ([[thuat-ngu-chuan-va-nguon-tham-khao]]), rồi 3–4 bullet nối các
   khái niệm đã học vào đúng vị trí của chúng trên hình.

   **Ngoại lệ — bài cheatsheet ôn phỏng vấn thì hình đó lên mục 01, tên là *Mental model*.**
   Ngày 2026-09-04, người dùng: *"phải để lên đầu mới hợp lý, cho cả người mới và người học lại,
   nhìn cái thì não trigger ngay"*. Bài dạng ôn thì người học lại **chỉ mở bài, nhìn hình, đóng** —
   mở bài mới là chỗ đắt nhất, chốt lại ở cuối thì không ai đọc tới. Bài như vậy không có mục tổng
   kết cuối; `figure.gist` chính là mental model, và mục cuối là Hỏi đáp. Xem
   [Memory management & GC](../../../content/02-python/02-language-core/memory-management-gc/index.html)
   và [[sua-bai-memory-management-gc]].

8. **Mặt bài là cheatsheet, chiều sâu nằm trong `details.deep`.** Ngày 2026-09-04, người dùng:
   *"bị quá nhiều chữ, ví dụ bài Gradient boosting, tôi muốn phong cách như cheatsheet nhưng chi
   tiết hơn để học kĩ hơn"*. Đoạn văn dài **không cắt bỏ** — gập nguyên văn vào một
   `<details class="deep">` với `<summary>` là một câu hỏi, mặt bài chỉ còn `p.key` + hình +
   bullet ngắn. Không mất kiến thức nào, mà quét mắt vẫn nhanh.
   Mốc: **không đoạn văn mặt bài nào quá 33 từ** (trần của bài mẫu).

## Luật 9 — hình mở bài: nhìn phát hiểu bài nói gì

Ngay dưới lede, trước mục 01, đặt **đúng một** `figure.gist`: hình vẽ lại chính câu lede,
kèm `figcaption` một câu. Tiêu chí người dùng đặt ra: **nhìn phát hiểu luôn**, không phải đọc
mới hiểu. Nó không thay mục *Tổng kết một hình* ở cuối — đầu bài là lời hứa, cuối bài là chốt lại.

Cả nhóm dùng **chung một bộ từ vựng hình**: cùng kiểu khung bo góc, cùng mũi tên có nhãn, cùng
glyph cây, cùng bốn màu ngữ nghĩa. Học đọc một hình mở bài là đọc được cả năm cái còn lại —
đúng tinh thần luật 1.

**Hình phải vẽ cơ chế đang chạy, không phải ảnh chụp từng chặng.** Ba tầng dọc
*dữ liệu → Train → cây/model → Predict → kết quả*, mũi tên có tên, và vòng hồi tiếp nếu thuật
toán có lặp. Bố cục tự nó phải nói lên cơ chế: tuần tự thì các cột nối nhau, song song thì các cột
rời nhau rồi mới gặp ở ô gộp. Cột cuối luôn là **lúc đã hội tụ** — vẽ ba bước đầu mà chưa thấy
kết quả thì hình vô nghĩa.

**Các bài cùng cơ chế phải dùng chung một khung hình**, cùng dữ liệu và cùng các mốc, để đặt cạnh
nhau là so được từng con số. Bài nào chỉ khác một chi tiết thì **giữ nguyên khung, làm mờ phần
giống, tô sáng đúng ô khác** rồi phóng to ô đó ra — đọc phát thấy ngay "y hệt bài kia, khác mỗi
chỗ này". Ngược lại, cơ chế khác thật thì bố cục phải khác thật.

Ba thứ dễ hỏng, đã dính đủ cả ba ở nhóm tree-models:

- **Nhãn mũi tên đè lên khung bên cạnh.** Chỉ lộ ra khi render thật; phải chụp màn hình soát,
  đọc markup không thấy.
- **Hình nói dối.** Bản đầu của hình LightGBM vẽ hai cây khác số lá trong khi cả bài nói "cùng
  ngân sách lá". Số nào hình khoe thì phải `assert` trong script sinh, hoặc tính lại từ chính
  thuật toán của lab.
- **Chữ trong hình quá dài.** Nhãn dài tràn khỏi khung ở màn hẹp. Nhãn là *nhãn*, không phải câu
  văn — câu văn để `figcaption`. Mốc thực dụng rút ra ở bài memory-management-gc: **nhãn phải ngắn
  tới mức không cần đo**; dài quá thì tách hai dòng, hoặc đẩy hẳn xuống `figcaption`.
- **`viewBox` thấp hơn hình.** Ô cuối bị cắt cụt mà markup vẫn đúng hoàn toàn. Hàm sinh khung nên
  **trả về `y` cuối cùng** để chiều cao tính ra từ đó, đừng chép số cứng.
- **Hai dòng vai trò ngang nhau thì phải cùng độ đậm.** Trong một danh sách các ý *cùng cấp*,
  mọi dòng dùng chung một cặp màu — không được dòng này `--dim` dòng kia `--faint`. Người đọc
  hiểu chênh lệch sáng là chênh lệch **tầm quan trọng**, nên vô tình dìm một ý xuống hàng phụ.
  Độ sáng chỉ được dùng cho **thứ bậc thật**: ô đang sáng vs ô đã mờ, tiêu đề vs chú thích.
- **Chữ phụ trong hình dùng `--muted`, đừng dùng `--faint`.** Trên nền `--panel`, `--faint`
  (#7A6F63) chỉ đạt **3,6:1** — dưới mốc AA 4,5:1, mà `.sv-d` lại chỉ 10,5px. `--muted` (#9A8F81)
  đạt 5,56:1 và vẫn lùi rõ so với `--text`. Mặc định của `.sv-d`/`.sv-h` trong `style.css` đã đổi
  sang `--muted`; `--faint` để dành cho chữ **cố tình phải mờ** (ô đã bị làm xám).
- **Dấu tiếng Việt rơi trong font mono.** JetBrains Mono — tức hai class `sv-l` và `sv-h` — vẽ
  `số` thành `sô´`. Hai class đó **chỉ dùng cho chữ không dấu**: tên biến, số, nhãn hoa tiếng Anh.
  Nhãn hoa **có dấu** dùng `sv-hv` (Be Vietnam Pro 600, cùng cỡ cùng letter-spacing, nhìn như một
  bộ với `sv-h`); nhãn thường có dấu dùng `sv-d`/`sv-t`. Lỗi im lặng hoàn toàn, chỉ ảnh chụp mới lộ.
  Cách chắc ăn: để `txt()` trong `frame.py` **tự đổi class** khi thấy ký tự có dấu, đừng nhớ bằng tay.
- **Đừng truyền `var(--faint)` thẳng vào `txt()`.** Mặc định CSS của `.sv-d`/`.sv-h` đã là `--muted`,
  nhưng script sinh hình lại ghi đè `fill` về `--faint` ở từng nhãn nên bài mới vẫn tụt xuống 3,6:1.
  Cho `txt()` nâng `--faint` → `--muted` ngay tại chỗ; chỉ ô **đã bị xám hoá** mới cố ý mờ hơn.

## Ngữ pháp của một hình: ô là kết quả, mũi tên là hành động

Ngày 2026-09-05, người dùng nhìn hình *"key → hash(key) → hash % size → số ô cần đọc"* và sửa lại
bố cục: *"có thể để tên các bước hành động ở mũi tên còn các ô là kết quả, ví dụ `key "user"`
--`hash(key)`--> `hash value` --`hash % size`--> `slot index`"*.

Đó là một luật đọc hình, không phải một sở thích: khi ô chứa cả hành động lẫn kết quả, người đọc
phải tự đoán ô nào là *cái đang có* và ô nào là *việc đang làm*. Tách ra thì hình tự nói:

- **trong ô** — một danh từ: thứ đang cầm trên tay ở bước đó (`key` · `hash value` · `slot index`),
  dòng dưới là ví dụ cụ thể của chính nó (`"user"` · `một số nguyên` · `số thứ tự slot`);
- **trên mũi tên** — phép biến đổi, viết bằng `sv-l` (mono) cùng màu mũi tên: `hash(key)`, `% size`.

Cài bằng `arr_r_lbl(y, x1, x2, màu, nhãn)` trong `frame.py`. Chừa khe **≥ 64px** giữa hai ô —
nhãn mũi tên nằm giữa khe, khe hẹp hơn thì nhãn thò sang đè khung bên cạnh (checker bắt được:
`CHỮ TRÀN KHUNG`).

### Luật đó áp cho cả `.flow` trong HTML, không riêng SVG

2026-09-05: *"còn cái flow nữa, để hành động ở mũi tên ý"*. `.flow` trước đây để mũi tên trần
`<div class="a">→</div>` và nhồi cả động từ lẫn kết quả vào ô — sai đúng cái đã sửa ở SVG.
Khuôn mới (`style.css`, mẫu trong `kit.html`):

```html
<div class="n"><h5>Dữ liệu thô</h5><p>còn nằm ngoài kho đích</p></div>
<div class="a act"><i>Transform</i>→</div>
<div class="n ok"><h5>Dữ liệu đã sạch</h5><p>đã chuẩn hoá, tính lại</p></div>
```

- `h5` là **danh từ** — thứ đang cầm ở bước đó; `p` là mô tả chính nó, không phải việc kế tiếp.
- `<i>` là **động từ**, mono, màu `--probe`. **≤ 30 ký tự** — dài hơn thì cột lệch hẳn.
- Không phải hành động (`·`, `+`, `≠`, `↻`) thì để mũi tên trần, đừng gán `act`.
- **≤ 4–5 ô một flow.** 6 ô thì ô cuối rớt xuống dòng riêng chiếm hết bề ngang, nhìn như lỗi
  (đã dính ở `sql-basics-overview`). Gộp hai chặng vào một nhãn mũi tên: `<i>GROUP BY rồi HAVING</i>`.
- Mobile: `.a` trần bị ẩn, nhưng `.a.act` **phải hiện** — nó thành một dòng riêng nằm ngang,
  vì mất nhãn là mất nửa nội dung. Đã có sẵn trong `@media(max-width:900px)`.

Đã sửa 44 flow ở năm kệ đầu bằng `/tmp/dh/flowfix.py` (spec khai báo + thay khối theo dòng,
thay từ dưới lên để chỉ số dòng không lệch).

## Margin: chrome hẹp lại để hình rộng ra

*"tôi thấy bạn đang để margin hơi to, khiến nội dung như hình vẽ đôi khi bị hẹp chỗ"*. Hình SVG
có `viewBox` cố định nên cột nội dung hẹp đi bao nhiêu là hình bị thu nhỏ bấy nhiêu — margin
không phải chuyện thẩm mỹ, nó ăn thẳng vào cỡ chữ trong hình. Số hiện tại trong `style.css`:

| | cũ | nay |
|---|---|---|
| `.wrap` max-width · padding | 1240 · 28 | **1320 · 22** |
| `.cols` cột mục lục · gap · padding dọc | 186 · 32 | **172 · 26** |
| `nav.toc` margin-left (≥1280px) | −64 | **−52** |
| padding ngang mobile | 20 | **17** |

Đổi mấy số này thì soát lại hai mốc: **1400px** (mục lục không được chồng lên bài) và **490px**
(không tràn ngang).

## Thuật ngữ: gọi đúng tên, đừng gọi bằng từ đời thường

Cùng lượt đó: *""ô" thì dùng từ cho đúng thuật ngữ"*. Cả bài `dict-hash-table` đang gọi slot là
"ô" — nghe dễ, nhưng người đọc đi phỏng vấn cần **đúng chữ mà người phỏng vấn dùng**, và "ô" còn
trùng nghĩa với ô của bản đồ mental model nên đọc lên bị lẫn. Đổi hết sang `slot` / `slot index`
(cả `frame.py`, mọi hình, văn xuôi, và `lab.js`).

Luật rút ra: **danh từ chuyên ngành thì giữ tiếng Anh xuyên suốt** — đã có trong `CLAUDE.md` cho
tên bài, nhưng nó áp cho **cả chữ trong hình và trong lab**, không chỉ tiêu đề. Còn khi bản đồ
mental model cũng có "ô" theo nghĩa hình học thì càng phải tách hai từ ra, không dùng chung.

## Chữ nhỏ không được mang kết luận — thêm class `.sv-s`

Người dùng: *"chữ to chữ nhỏ mà chữ nhỏ để kết luận thì không nhìn rõ gì, thay đổi phong cách…
nói chung sao cho UX/UI tốt"*.

Lỗi cụ thể: nhãn `sv-t` 12,5px `Hai key cùng một slot`, và ngay dưới là `sv-d` 10,5px `--muted`
*"probe đi tiếp theo một đường cố định"* — mà **dòng dưới mới là bài học**. Chữ nhỏ + mờ nói với
mắt rằng "cái này phụ", đúng ngược lại ý định.

Chữa bằng một bậc chữ mới giữa `sv-t` và `sv-d`, đã thêm vào `style.css`:

```css
.sv-s{font-family:"Be Vietnam Pro",sans-serif;font-size:11.5px;font-weight:500;fill:var(--dim)}
```

11,5px · weight 500 · `--dim` (9,2:1) — vẫn lùi sau nhãn chính nhưng đọc được ở cỡ thật. Quy ước
ba bậc từ nay: **`sv-t` = nhãn** · **`sv-s` = dòng mang kết luận** · **`sv-d` = chú thích thật sự
phụ** (nguồn, đơn vị, ghi chú bên lề). Nhớ đăng ký class mới vào bảng `W` của script kiểm hình,
không thì nó `KeyError` chứ không cảnh báo.

**Hai biến thể của cùng lỗi này, cả hai đều tìm được bằng máy** — dò cặp *nhãn `sv-t` + dòng ngay
dưới nó* (cùng `x` ±3, cách 8–26px, dài > 26 ký tự):

1. dòng dưới là `sv-d` → nó đang mang kết luận mà lại mờ nhất → nâng lên `sv-s`.
   Đã sửa **72 dòng / 7 bài** (`/tmp/dh/promote.py --apply`).
2. dòng dưới là `sv-l` **có dấu tiếng Việt** → sai hai lần: mono rơi dấu, *và* kết luận bị nhét
   vào bậc phụ → cũng thành `sv-s`. Đã sửa **20 dòng / 12 bài** (`/tmp/dh/promote2.py --apply`).

Viết detector rồi sửa hàng loạt, đừng soi từng bài — lỗi này rải đều cả kho và mắt không bắt được.

## Chi tiết CPython: hiểu ý, không thuộc công thức

*"cái gì liên quan chi tiết tới CPython thì không cần hiểu sâu, hiểu ý tưởng là được"* — mở rộng
của bảng Bỏ/Giữ ở trên, và lần này áp cả vào **hình**. Ô giữa hình 04 từng in nguyên
`i = (i*5 + perturb + 1) % size`; thay bằng một câu nói **công thức đó làm gì**: *"CPython trộn
thêm bit cao của hash vào bước nhảy"*. Deep dive cũng bỏ công thức, chỉ còn hai vai trò — phân tán
và phủ hết bảng — vì đó mới là thứ suy ra được lại công thức.

Kiểm nhanh cả bài: `grep` các dấu vết mức-cài-đặt (`perturb`, `i*5`, `& (size-1)`, `phép AND`,
`lũy thừa 2`) rồi hỏi từng chỗ *"câu này có trong buổi phỏng vấn không"*. Không → nâng lên một bậc
trừu tượng, đừng xoá trắng để lại lỗ.

## Đặt tên nhãn: đọc phát hiểu, không cần suy

Lượt này tôi đã **vi phạm một luật đã ghi sẵn** — `CLAUDE.md`: *"Đầu mục là danh từ, đọc là hiểu"*
— khi đặt tên panel `BA THỨ CHỐNG ĐỠ CHO PHÉP TÍNH TRÊN` và các ô `HAI KEY CÙNG MỘT Ô` /
`XOÁ ĐỂ LẠI VẾT`. Người dùng bắt đúng: *"không đặt tên mơ hồ kiểu này, tôi đã đề cập trong memory
rồi mà nhỉ?"*. Luật đó áp cho **nhãn trong hình** y như cho đầu mục — trước khi sinh hình phải
đọc lại nó.

Khuôn thay thế đã dùng: mỗi ô là một cặp **nguyên nhân → cách chữa**, viết như câu nói thường:

| Mơ hồ | Đọc phát hiểu |
|---|---|
| `HAI KEY CÙNG MỘT Ô` | `Hai key ra cùng một slot` · *thì dò sang slot khác — probe sequence* |
| `XOÁ ĐỂ LẠI VẾT` | `Xoá làm đứt đường dò` · *thì để lại vết xoá — tombstone* |
| `ĐẦY 2/3 THÌ NHÂN ĐÔI` | `Bảng chật thì đường dò dài ra` · *thì nhân đôi bảng — resize* |
| `BA THỨ CHỐNG ĐỠ NÓ` | `BA CHUYỆN LÀM HỎNG PHÉP TÍNH ĐÓ` |

Hoa toàn bộ chỉ dành cho **nhãn nhóm** (`sv-h`); tên một ô viết chữ thường như câu nói — hoa toàn
bộ vừa khó đọc vừa ép phải rút ngắn tới mức mất nghĩa.

Ngoài hình, một chỗ nữa cùng loại "markup đúng mà màn hình sai": **`<h2>` của mục không được chứa
`<code>`** — `app.js` dựng mục lục bằng `textContent`, nên thẻ rơi thẳng vào sidebar. Tiêu đề kiểu
`__hash__ & __eq__` phải viết dạng chữ trơn.

Sinh bằng script Python dùng chung (`box/txt/arrow/tree/put`), `put()` phải idempotent (xoá
`figure.gist` cũ trước khi chèn) để chỉnh toạ độ rồi chạy lại thoải mái.

**Soát overlap bằng máy, đừng soát bằng mắt.** Ước lượng bề rộng chữ từ class
(`sv-t` ≈ 0,55 × cỡ chữ mỗi ký tự, `sv-d` ≈ 0,52, `sv-l` ≈ 0,60, `sv-h` ≈ 0,72) rồi kiểm bốn thứ:
chữ đè chữ · chữ thò khỏi `rect` bao nó · `rect` đè `rect` không lồng nhau · tràn khỏi `viewBox`.
Thêm một lượt **vạch cắt chữ** — mũi tên vòng hai chiều rất hay chạy xuyên qua nhãn trong ô,
mắt nhìn ảnh chụp cả trang thu nhỏ thì không thấy. Cách chụp để soát: render **một hình một trang**
(nhúng `assets/style.css` vào file tạm) rồi
`google-chrome --headless --force-device-scale-factor=2 --screenshot` — phóng to gấp đôi và không
có chữ xung quanh, lỗi 2–3px hiện ra ngay.

**Áp dụng thế nào.** Trước khi sửa một bài, đo bằng script ở [[it-chu-nhieu-hinh]] và script đếm
bullet dưới đây; sau khi sửa đo lại. Thứ tự việc: (1) bullet dài → cắt; (2) `<pre>` khái niệm →
bỏ hoặc đổi thành hình; (3) hình lạ → đưa về hình dạng chính của bài; (4) công thức trần → `.eq`;
(5) thiếu mục tổng kết → vẽ. Không viết thêm chữ mới trừ khi đang bù kiến thức thiếu.

```python
lis = re.findall(r'<li[^>]*>((?:(?!</?li).)*?)</li>', s, flags=re.S)
ws = [len(re.sub(r'<[^>]+>', ' ', x).split()) for x in lis]   # tb ≤15, max ≤25

# đoạn văn *mặt bài*: bắt buộc bỏ <details> và <figure> trước,
# không thì <text> trong SVG bị đếm thành văn xuôi và ra số ảo
b = re.sub(r'<(details|figure).*?</\1>', '', art, flags=re.S)
# (?!re\b) là bắt buộc — thiếu nó thì <pre> khớp luôn vào <p...> và số bị thổi lên
ps = re.findall(r'<p(?!re\b)(?![^>]*class=)[^>]*>((?:(?!</?p[ >]).)*?)</p>', b, flags=re.S)  # max ≤33
# đo theo từng dòng <br>, không đo cả khối: nhãn lab ngắt dòng bằng <br> là hợp lệ
```

Báo cáo kết quả theo [[cach-tra-loi-ngan-gon]].


## Hình *Mental model* và câu lede — hai chỗ người dùng đọc đầu tiên

**Panel phải của hình gist chỉ được chứa các ý, không chứa "câu trả lời thuộc lòng" bằng tiếng Anh.**
Đã từng đặt một khối tiếng Anh 3 dòng lên đầu panel (kiểu *"Assignment binds a name to an object…"*).
Người dùng bắt đúng: nó **trùng nghĩa** với dòng ý ngay dưới nó, mà lại chiếm chỗ đẹp nhất và bắt
người đọc chuyển ngôn ngữ ngay ở giây đầu. Bỏ khối đó, các ý dâng lên đầy panel — hình thấp đi
86px và không mất một chữ nội dung nào.

**Chữ trong SVG không tự xuống dòng, nên phải tự dùng hết bề ngang.** Panel rộng 500px (x 360→860);
`sv-t` 12,5px chứa được **~72 ký tự** một dòng. Ngắt dòng sớm ở 45–50 ký tự là để trống một phần ba
panel một cách vô cớ. Đo trước khi ngắt: `len(chuỗi) * 12.5 * 0.55` phải vừa trong `500 - 32`.

**Câu lede: không được có ẩn dụ cần giải thích thêm.** Viết *"cả bài gói trong một bản đồ hai nhánh"*
là bắt người đọc hỏi lại "hai nhánh là gì" ngay câu đầu — hỏng đúng chỗ đáng lẽ phải dễ nhất.
Khuôn dùng được: **(1) hai khái niệm gốc là gì · (2) hệ quả trực tiếp của chúng · (3) tên bài nằm
ở đâu trong đó** — ba câu, không nhắc tới chữ "bản đồ", không hứa hẹn về cấu trúc bài. Hình gist
ngay dưới đã nói giúp phần cấu trúc rồi.

**Ý nào liệt kê được thì cho thành bullet, đừng nhồi vào câu.** Người dùng: *"thì 2 cái việc đó
thành 2 cái bullet… mọi thứ gãy gọn là tốt nhất."* Lede nào có dạng *"chỉ làm một trong hai việc —
A, hoặc B"* thì cắt ở dấu hai chấm rồi đẩy A, B xuống `<ul class="ledelist">` (đã có trong
`style.css`: mỗi ý một vạch `--clay`, tên ý `<b>`, phần giải thích `<em>` màu `--muted`). Câu chốt
còn lại vẫn là `<p class="lede">` đứng sau danh sách. Luật này áp cho **mọi** chỗ, không riêng lede:
đếm được thì xuống dòng được.

## Độ sâu: dừng ở mức phỏng vấn hỏi, không đi tới mức thiết kế phần cứng

Người dùng, về bài `dict-hash-table`: *"hơi chi tiết quá, chỉ cần core mà phỏng vấn bigtech cho
swe ai ml engineer hay hỏi, còn chi tiết từng phần nào dùng bit nào thì giống thiết kế tối ưu phần
cứng quá… vẫn đủ hiểu cả flow nhưng cái gì không core thì không đi sâu."*

Ranh giới đi qua **mức trừu tượng**, không qua độ dài. Cùng một cơ chế, viết ở mức nào:

| Bỏ — mức cài đặt | Giữ — mức khái niệm |
|---|---|
| `hash & (size-1)`, "cắt bit thấp", size là lũy thừa của 2 | `hash % size` ra số ô; CPython viết thành phép AND cho nhanh |
| `perturb >>= 5`, PERTURB_SHIFT, vì sao là số 5 và số 1 | probe phải **xác định** và **đi hết bảng** — hai điều kiện, gọi tên `perturb` là đủ |
| primary vs secondary clustering, LCG chu kỳ đầy đủ | Python không dùng `i+1` vì nó dồn key thành dải liền kề |
| `hash(-1) == hash(-2) == -2` | `1 == 1.0 == True` nên ba key thành một |

Test nhanh: **câu này có xuất hiện trong một buổi phỏng vấn SWE/ML không?** Không → hoặc bỏ, hoặc
gập vào một `details.deep` viết ở mức "biết tên là đủ". Chi tiết cài đặt bỏ đi thì phải **thay bằng
lý do**, đừng để lại lỗ: chỗ nói "cắt bit thấp nên trùng ô" đổi thành "nén một khoảng rất lớn xuống
8 chỗ nên trùng là tất yếu" — cùng một sự thật, mức trừu tượng cao hơn một bậc.

**Lab cũng theo luật đó: một lab, một ý.** Lab cũ của `dict-hash-table` có ba phần (stepper, ba
hash cùng ô đầu, mô phỏng clustering linear vs Python) — phần thứ ba là một bài nghiên cứu nhỏ,
không phải chỗ để học. Rút còn stepper, và ba dòng `.why` dưới lab **nói người học nên tự thử gì**
(chạy lại cùng hash · đổi hash một chút · đổi size) thay vì kết luận hộ họ.
