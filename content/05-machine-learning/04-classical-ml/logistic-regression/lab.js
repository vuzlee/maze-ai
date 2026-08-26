(function(){
/* ---------------- lab: ngưỡng quyết định ---------------- */
const CASES = {
  balanced: [[0.95,1],[0.88,1],[0.82,1],[0.71,1],[0.66,0],[0.58,1],[0.52,0],[0.47,1],[0.41,0],[0.33,0],[0.22,0],[0.11,0]],
  rare: [[0.91,1],[0.72,0],[0.61,0],[0.44,1],[0.38,0],[0.31,0],[0.24,0],[0.18,0],[0.12,0],[0.07,0]]
};
function thrCalc(){
  const t = Math.min(1, Math.max(0, +document.getElementById("thr").value || 0.5));
  const data = CASES[document.getElementById("tcase").value];
  let tp=0, fp=0, tn=0, fn=0;
  data.forEach(([p, y]) => {
    const pred = p >= t ? 1 : 0;
    if(pred === 1 && y === 1) tp++;
    else if(pred === 1 && y === 0) fp++;
    else if(pred === 0 && y === 0) tn++;
    else fn++;
  });
  const prec = tp+fp ? tp/(tp+fp) : NaN, rec = tp+fn ? tp/(tp+fn) : NaN;
  const f1 = (prec && rec) ? 2*prec*rec/(prec+rec) : NaN;
  const acc = (tp+tn)/data.length;
  const bars = data.map(([p, y]) => {
    const pred = p >= t;
    const ok = pred === (y === 1);
    const col = ok ? (y === 1 ? "var(--ok)" : "var(--rule)") : "var(--tomb)";
    return `<div class="slot" style="min-width:38px;border-color:${col}">
      <i>${y === 1 ? "dương" : "âm"}</i>
      <u style="background:${pred?col:'var(--raise)'};color:${pred?'#14110E':'var(--muted)'};font-weight:600">${p.toFixed(2)}</u></div>`;
  }).join("");
  const fmt = v => isNaN(v) ? "–" : (100*v).toFixed(0) + "%";
  document.getElementById("thrview").innerHTML =
    `<p class="legend" style="margin:2px 0 6px"><span>xác suất model dự đoán · ô tô màu là được dự đoán DƯƠNG · đỏ là dự đoán sai</span></p>
     <div style="display:flex;gap:4px;flex-wrap:wrap">${bars}</div>
     <table style="margin-top:16px"><tr><th>Chỉ số</th><th>Giá trị</th><th>Ý nghĩa</th></tr>
       <tr><td class="mono">precision</td><td style="color:var(--probe);font-family:var(--mono)">${fmt(prec)}</td>
           <td style="font-size:13px;color:var(--muted)">trong ${tp+fp} ca báo dương, ${tp} ca đúng</td></tr>
       <tr><td class="mono">recall</td><td style="color:var(--probe);font-family:var(--mono)">${fmt(rec)}</td>
           <td style="font-size:13px;color:var(--muted)">trong ${tp+fn} ca dương thật, bắt được ${tp}</td></tr>
       <tr><td class="mono">F1</td><td style="font-family:var(--mono)">${fmt(f1)}</td>
           <td style="font-size:13px;color:var(--muted)">trung bình điều hoà của hai chỉ số trên</td></tr>
       <tr><td class="mono">accuracy</td><td style="font-family:var(--mono)">${fmt(acc)}</td>
           <td style="font-size:13px;color:var(--muted)">TP=${tp} FP=${fp} FN=${fn} TN=${tn}</td></tr>
     </table>`;
}
["thr","tcase"].forEach(id => document.getElementById(id).addEventListener("input", thrCalc));
document.getElementById("tcase").addEventListener("change", thrCalc);
thrCalc();
})();
