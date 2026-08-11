(function(){
/* ---------------- lab: LoRA & bộ nhớ ---------------- */
const FPRESET = {
  "7b":  {d: 4096, L: 32, ff: 11008},
  "13b": {d: 5120, L: 40, ff: 13824},
  "70b": {d: 8192, L: 80, ff: 28672}
};
function fCalc(){
  const d = Math.max(64, +document.getElementById("fd").value || 4096);
  const L = Math.max(1, +document.getElementById("fL").value || 32);
  const ff = Math.max(64, +document.getElementById("fff").value || 11008);
  const r = Math.max(1, +document.getElementById("fr").value || 16);
  const tgt = document.getElementById("ftgt").value;

  /* tham số của model: attention 4·d² + MLP 3·d·d_ff mỗi lớp */
  const perLayer = 4*d*d + 3*d*ff;
  const total = L * perLayer;

  /* LoRA: mỗi lớp tuyến tính (in,out) thêm r·(in+out) */
  let lora = L * 4 * r * (d + d);                     /* q, k, v, o */
  if(tgt === "all") lora += L * (2 * r * (d + ff) + r * (ff + d));  /* gate, up, down */

  const pct = 100 * lora / total;
  /* bộ nhớ: trọng số 2B + grad 2B + Adam m,v 8B + master fp32 4B ≈ 16B mỗi tham số huấn luyện */
  const memFull = total * 16;
  const memLora = total * 2 + lora * 16;
  const memQ = total * 0.5 + lora * 16;

  const P = n => n >= 1e9 ? (n/1e9).toFixed(2)+" B" : n >= 1e6 ? (n/1e6).toFixed(1)+" M" : (n/1e3).toFixed(0)+" K";
  const G = b => (b/1024**3).toFixed(1) + " GB";
  document.getElementById("fview").innerHTML =
    `<table>
      <tr><th>Hạng mục</th><th>Tham số</th><th>% tổng</th><th>Bộ nhớ huấn luyện</th></tr>
      <tr><td>Toàn model</td><td style="font-family:var(--mono)">${P(total)}</td><td>100%</td>
          <td style="font-family:var(--mono)">—</td></tr>
      <tr><td><strong>Full fine-tune</strong></td><td style="font-family:var(--mono)">${P(total)}</td><td>100%</td>
          <td style="font-family:var(--mono);color:var(--tomb)">${G(memFull)}</td></tr>
      <tr><td><strong>LoRA</strong> r=${r}</td>
          <td style="font-family:var(--mono);color:var(--ok)">${P(lora)}</td>
          <td style="color:var(--probe);font-family:var(--mono)">${pct.toFixed(2)}%</td>
          <td style="font-family:var(--mono);color:var(--probe)">${G(memLora)}</td></tr>
      <tr><td><strong>QLoRA</strong> nền 4-bit</td>
          <td style="font-family:var(--mono);color:var(--ok)">${P(lora)}</td>
          <td style="color:var(--probe);font-family:var(--mono)">${pct.toFixed(2)}%</td>
          <td style="font-family:var(--mono);color:var(--ok)">${G(memQ)}</td></tr>
      <tr><td colspan="4" style="font-size:12.5px;color:var(--muted)">
        Ước lượng theo 16 byte mỗi tham số huấn luyện (trọng số bf16 + gradient + hai trạng thái Adam + bản fp32),
        cộng bộ nhớ giữ model nền. Chưa tính activation — phần này phụ thuộc batch size và độ dài chuỗi.</td></tr>
    </table>`;
}
document.getElementById("fpreset").addEventListener("change", e => {
  const p = FPRESET[e.target.value];
  if(p){
    document.getElementById("fd").value = p.d;
    document.getElementById("fL").value = p.L;
    document.getElementById("fff").value = p.ff;
  }
  fCalc();
});
["fd","fL","fff","fr","ftgt"].forEach(id => {
  document.getElementById(id).addEventListener("input", fCalc);
  document.getElementById(id).addEventListener("change", fCalc);
});
fCalc();
})();
