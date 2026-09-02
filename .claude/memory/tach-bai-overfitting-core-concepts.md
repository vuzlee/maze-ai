---
name: tach-bai-overfitting-core-concepts
description: Vì sao nhóm 03 Core concepts được viết bằng cách tách overfitting-regularization thay vì viết bài mới
metadata:
  type: project
updated: 2026-09-02
---

Nhóm `05-machine-learning/04-core-concepts` có 5 khung, nhưng bài `overfitting-regularization`
(đã viết sẵn, 15 mục) **đã ôm sẵn nội dung của hai khung khác** — bias–variance và
train/val/test/CV/rò rỉ dữ liệu. Viết hai khung đó thành bài mới là chép lại chính nó,
trái luật "một khái niệm, một chủ".

Việc đã làm: **tách** theo quy trình trong `CLAUDE.md` §"Tách một bài làm hai" —

| Bài | Nhận gì |
|---|---|
| `bias-variance-tradeoff` | phân rã sai số + bảng bias/variance + `.note.key` "Nhớ một câu" + **cả lab.js** (`git mv`) |
| `train-val-test-cv` | ba tập · k-fold · kiểu chia · 6 nguồn rò rỉ · nested CV · checklist |
| `overfitting-regularization` | còn lại chẩn đoán · learning curve · regularize · hyperparameter · production skew |

**Why:** Đọc hết bài đã viết *trước* khi viết khung cạnh nó là bước bắt buộc ở kệ này — các bài
deep dive cũ hay ôm rộng hơn tên gọi của chúng.

**How to apply:** Trước khi viết bất kỳ khung nào, đọc toàn văn các bài đã viết cùng nhóm.
Trùng thì tách chứ đừng viết mới. Khi tách: `git mv` lab.js theo nửa của nó, xoá thẻ
`<script src="lab.js">` ở nửa còn lại, đánh số lại `<b>NN</b>` + `id="slug-sN"` từ 01,
và mỗi bên phải có link chéo hai chiều ở thân bài lẫn `<footer>`.
