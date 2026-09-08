# Bộ nhớ của kho MazeAI

Chín ghi chú, hai thư mục:

- **`chuan/`** — luật viết bài, còn đúng mãi. **Đọc hết trước khi sửa bất kỳ bài nào.**
- **`nhat-ky/`** — trạng thái và bài học của việc đang làm.

Ranh giới với `CLAUDE.md`: file đó mô tả kho **đang như thế nào** (cấu trúc, cách build);
memory ghi **vì sao chọn cách đó** và **đang làm tới đâu**. Cùng một điều đừng viết ở cả hai chỗ.

## chuan/ — luật viết bài

| Ghi chú | Nội dung |
|---|---|
| [Bài mẫu — Random forest](chuan/chuan-bai-mau.md) | **đọc đầu tiên.** Thước của cả kho: mười luật + số đo. Luật 1 = §01 gồm câu định nghĩa + một hình mental model 3–5 ô, mỗi mục sau bóc một ô. Luật 10 = cặp mục `Ưu và nhược` (bảng) rồi `Chọn khi nào` (.stack) đóng phần thân. Kèm ngữ pháp của một hình (ô là kết quả, mũi tên là hành động) và bố cục phải nói đúng quan hệ |
| [Tối thiểu để hiểu](chuan/toi-thieu-de-hieu.md) | chín luật A→I về **nội dung**: không chữ meta trong bài · có cấu trúc dữ liệu thì vẽ đúng hình dạng nó · chỉ giữ mức tối thiểu · nội dung là chữ thì dùng khuôn HTML đừng vẽ SVG · **cả bài + lab chạy trên đúng MỘT bộ ví dụ** · lab chỉ hỏi một câu · viết cho người MỚI · cắt thì cắt cả ở *Lỗi hay gặp* và *Hỏi đáp*. Kèm quy trình review sáu phép |
| [Trình bày bài](chuan/trinh-bay-bai.md) | luật **trình bày**: ít chữ nhiều hình (đo bằng chữ/hình, mốc 123) · **rất ít note** · câu đơn mỗi dòng một ý (áp **cả trong `details.qa`** vì nó sinh ra thẻ ôn) · **công thức dáng LaTeX** · ký hiệu dùng bảng tra `dl.defs` · **mỗi mục kể 2+ trường hợp thì mỗi trường hợp một ô hình** (không dừng ở Mental model — `.axis` không thay được hình) · hiểu ý trước rồi mới chi tiết · **không ví von** — ba họ ẩn dụ bị cấm (kinh tế · vật lý · đồ vật), soát **cả chữ trong `<svg>`**. Kèm khuôn `*-overview` (chọn theo bản chất nhóm) và cách báo cáo cho người dùng — **thật ngắn, đừng kể tên class** |
| [Thuật ngữ](chuan/thuat-ngu.md) | phép **dịch ngược** để biết chữ nào giữ tiếng Anh · ba bẫy "nghe xuôi vẫn là dịch sai" (chữ Việt ở cột trái bảng `DICH` trong `tools/soat.py`) · luật tách riêng theo từng kệ · **năm bề mặt** phải đồng bộ không thì hỏng tìm kiếm · thuật ngữ phải nằm trên hình và sống sót qua mọi lần rút gọn |
| [Hai bài mẫu — SVM và KNN](chuan/bai-mau-svm-knn.md) | thước riêng cho kệ ML, chốt 2026-09-08. Khung xương 8 mục dùng lại được cho mọi bài model · mười chi tiết chỉ thấy khi đọc kĩ (một `p.key` một `<em>` · `dl.defs` đặt SAU `.eq` · mấy trường hợp thì mấy panel trong cùng một `<svg>` trên cùng bộ ví dụ · `<em>` giải nghĩa từng nửa công thức · `<pattern>` thay vì đổi hình dạng) · ba chỗ `knn` còn thua `svm` · mục *Hỏi đáp* của `svm` là chuẩn của cả kho |
| [Khuôn .eq cho công thức](chuan/khuon-eq-cong-thuc.md) | vì sao chọn HTML thay KaTeX · dáng LaTeX phải phủ **cả ba chỗ**: `.eq` (display) · **`.mth`** (ký hiệu trong văn xuôi — đừng dùng `<code>`) · **`sv-m`** (công thức trong `<svg>` — đừng dùng `sv-h`) · ranh giới `<code>` vs `.mth` · `<tspan>` chỉ hợp lệ trong SVG · quy ước vẽ đường cong bằng SVG |
| [Công cụ và cách kiểm](chuan/cong-cu-va-cach-kiem.md) | `soat.py` 8 phép · `svgkit` dùng chung đừng chép sang `/tmp` · **kiểm lại chính cái thước** (bảng toàn số 0 không chứng minh gì) · `check.py` là sàng, `getBBox` là trọng tài · bảy chỗ máy KHÔNG bắt được · chạy bao nhiêu vòng cho mỗi loại sửa |

## nhat-ky/ — đang làm tới đâu

| Ghi chú | Nội dung |
|---|---|
| [Trạng thái kho](nhat-ky/trang-thai-kho.md) | **mốc số liệu duy nhất.** 200 bài · 72 khung còn lại ở kệ 06→10 · kệ 01→05 sạch cả sáu trục **luật**. Kèm **trục thứ bảy — chất lượng trình bày**, đo lần đầu 2026-09-08: note ở kệ 06→10 gấp 8–12 lần mức cho phép · 18 bài quá 250 chữ/hình · công thức LaTeX chỉ có ở kệ ML · 30 bài ML còn khối Hỏi đáp dài. Và luật **mọi báo cáo phải ghi rõ sửa theo TRỤC NÀO** |
| [Bài học soạn nội dung](nhat-ky/bai-hoc-soan-noi-dung.md) | bẫy lặp bốn lần: việc thật là **tách bài** chứ không phải viết mới · bốn lỗi khiến người đọc không hiểu · hình dạng bản đồ phải tương phản với bài anh em |

## Cách dùng

**Đọc** — đầu phiên đọc file này; mở hết `chuan/` khi sắp sửa nội dung.

**Ghi** — đáng ghi là: phản hồi của người dùng về *cách làm việc* (kèm lý do), quyết định về nội
dung/lộ trình không suy ra được từ code, trạng thái công việc dài hơi. **Không ghi** thứ đã có
trong `CLAUDE.md`, `TAXONOMY.md`, cây thư mục hay lịch sử git.

**Giữ gọn.** Chín file là mức trần — bộ nhớ phình ra thì không ai đọc hết, và luật trùng nhau ở
hai file thì sẽ lệch nhau. Trước khi tạo file mới, tìm chỗ đã có: **thêm một dòng vào bảng có sẵn
tốt hơn viết một mục mới**. Số liệu chỉ khai ở [[trang-thai-kho]], đừng rải ra các file luật.
Ghi chú sai thì **xoá**, đừng để lại kèm đính chính.

Frontmatter mỗi file: `name` · `description` · `metadata.type` (`feedback`/`project`/`reference`) ·
`updated: YYYY-MM-DD`. Loại `feedback` phải có **Vì sao** và **Áp dụng thế nào**. Ngày viết tuyệt
đối. Nối sang ghi chú khác bằng `[[tên-slug]]`.
