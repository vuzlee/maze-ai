# Bộ nhớ của kho MazeAI

Tám ghi chú, hai thư mục, và **một bài mẫu để mở ra xem**:

- **`bai-mau/random-forest.html`** — bản người dùng chốt 2026-09-24 là *"bản tôi kì vọng"*.
  **Mở bằng trình duyệt trước khi sửa bất kỳ bài nào.** Đọc luật không thay được việc nhìn nó.
- **`chuan/`** — luật viết bài, còn đúng mãi. Đọc hết trước khi sửa nội dung.
- **`nhat-ky/`** — trạng thái và bài học của việc đang làm.

Ranh giới với `CLAUDE.md`: file đó mô tả kho **đang như thế nào** (cấu trúc, cách build);
memory ghi **vì sao chọn cách đó** và **đang làm tới đâu**. Cùng một điều đừng viết ở cả hai chỗ.

## chuan/ — luật viết bài

| Ghi chú | Nội dung |
|---|---|
| [Bài mẫu — Random forest](chuan/chuan-bai-mau.md) | **đọc đầu tiên, kèm mở file HTML ra xem.** Thước của cả kho, chốt 2026-09-24. Khung **9 mục** (không *Lỗi hay gặp*, không lab, không *Chọn khi nào* riêng) · **57 chữ/hình** · 0 note, 0 `<pre>` · hero có `ul.ledelist` ba gạch · tên mục = đúng chữ trên hình §01 · **hình động bằng keyframe trong `<style>` của từng `<svg>`**: chỉ `opacity`+`transform`, luôn bọc `prefers-reduced-motion:no-preference`, hiện dần rồi giữ tới mốc 87%, hình so sánh để tĩnh · `aria-label` kể trọn chuỗi động · **được tô nền mờ + viền màu** · chữ trong hình dùng một lớp `sv-d` · in đậm `<b>`, link là chữ cam · một bộ ví dụ chạy xuyên bài |
| [Tối thiểu để hiểu](chuan/toi-thieu-de-hieu.md) | chín luật A→I về **nội dung**: không chữ meta trong bài · có cấu trúc dữ liệu thì vẽ đúng hình dạng nó (phép `circle+path` chỉ là sàng — ô chữ nhật **là ô bảng** thì vẫn đúng) · chỉ giữ mức tối thiểu · nội dung là chữ thì dùng khuôn HTML đừng vẽ SVG · **cả bài chạy trên đúng MỘT bộ ví dụ** · viết cho người MỚI · cắt thì cắt cả ở *Hỏi đáp*. Kèm quy trình review sáu phép |
| [Trình bày bài](chuan/trinh-bay-bai.md) | luật **trình bày**: ít chữ nhiều hình (mốc **57**, trên 100 là còn phải cắt) · **không dùng note** · câu đơn mỗi dòng một ý (áp **cả trong `details.qa`** vì nó sinh ra thẻ ôn) · **công thức dáng LaTeX** · ký hiệu dùng bảng tra `dl.defs` · **mỗi mục kể 2+ trường hợp thì mỗi trường hợp một ô hình** · **bài quá kĩ thì cắt CHỮ đừng cắt MỤC** · **không ví von** — bốn họ ẩn dụ bị cấm, soát **cả chữ trong `<svg>`** · in đậm bằng `<b>`, không `.hl`. Kèm khuôn `*-overview` và cách báo cáo cho người dùng — **thật ngắn, đừng kể tên class** |
| [Thuật ngữ](chuan/thuat-ngu.md) | phép **dịch ngược** để biết chữ nào giữ tiếng Anh · ba bẫy "nghe xuôi vẫn là dịch sai" · luật tách riêng theo từng kệ · **năm bề mặt** phải đồng bộ không thì hỏng tìm kiếm · thuật ngữ phải nằm trên hình và sống sót qua mọi lần rút gọn |
| [Khuôn .eq cho công thức](chuan/khuon-eq-cong-thuc.md) | vì sao chọn HTML thay KaTeX · dáng LaTeX phải phủ **cả ba chỗ**: `.eq` (display) · **`.mth`** (ký hiệu trong văn xuôi — đừng dùng `<code>`) · **`sv-m`** (công thức trong `<svg>`) · ranh giới `<code>` vs `.mth` · quy ước vẽ đường cong bằng SVG |
| [Công cụ và cách kiểm](chuan/cong-cu-va-cach-kiem.md) | `soat.py` 8 phép · `svgkit` dùng chung đừng chép sang `/tmp` · **kiểm lại chính cái thước** · `check.py` là sàng, `getBBox` là trọng tài · bảy chỗ máy KHÔNG bắt được · **hình động máy không kiểm được — phải tắt hoạt hoạ xem lại và xem trọn một chu kỳ** · bẫy khi sửa `.eq` · chạy bao nhiêu vòng cho mỗi loại sửa |

## nhat-ky/ — đang làm tới đâu

| Ghi chú | Nội dung |
|---|---|
| [Trạng thái kho](nhat-ky/trang-thai-kho.md) | **mốc số liệu duy nhất.** 200 bài · 72 khung còn lại ở kệ 06→10 · kệ 01→05 sạch cả sáu trục **luật**. Kèm **trục thứ bảy — chất lượng trình bày**. Và luật **mọi báo cáo phải ghi rõ sửa theo TRỤC NÀO** |
| [Bài học soạn nội dung](nhat-ky/bai-hoc-soan-noi-dung.md) | bẫy lặp bốn lần: việc thật là **tách bài** chứ không phải viết mới · bốn lỗi khiến người đọc không hiểu · hình dạng bản đồ phải tương phản với bài anh em |

## Cách dùng

**Đọc** — đầu phiên đọc file này; mở hết `chuan/` **và mở `bai-mau/random-forest.html`** khi sắp
sửa nội dung.

**Ghi** — đáng ghi là: phản hồi của người dùng về *cách làm việc* (kèm lý do), quyết định về nội
dung/lộ trình không suy ra được từ code, trạng thái công việc dài hơi. **Không ghi** thứ đã có
trong `CLAUDE.md`, `TAXONOMY.md`, cây thư mục hay lịch sử git — **và không ghi thứ đọc ra được từ
chính bài mẫu**. Bài mẫu là bản gốc; ghi chú chỉ nói *vì sao*.

**Giữ gọn.** Tám file là mức trần — bộ nhớ phình ra thì không ai đọc hết, và luật trùng nhau ở hai
file thì sẽ lệch nhau. Trước khi tạo file mới, tìm chỗ đã có: **thêm một dòng vào bảng có sẵn tốt
hơn viết một mục mới**. Số liệu chỉ khai ở [[trang-thai-kho]] và [[chuan-bai-mau]], đừng rải ra các
file luật. Ghi chú sai thì **xoá**, đừng để lại kèm đính chính — 2026-09-24 đã xoá cả ghi chú
`bai-mau-svm-knn` vì bài mẫu mới thay hẳn nó.

Frontmatter mỗi file: `name` · `description` · `metadata.type` (`feedback`/`project`/`reference`) ·
`updated: YYYY-MM-DD`. Loại `feedback` phải có **Vì sao** và **Áp dụng thế nào**. Ngày viết tuyệt
đối. Nối sang ghi chú khác bằng `[[tên-slug]]`.
