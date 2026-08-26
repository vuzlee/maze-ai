(function(){
/* ---------------- lab 1: gradient descent ---------------- */
const BASE_PTS = [[1,2.1],[2,3.9],[3,6.2],[4,7.8],[5,10.1],[6,12.2],[7,13.8],[8,16.1],[9,18.0],[10,20.2]];
let GW = 0, GB = 0, GSTEPS = 0, GTIMER3 = null;

function gPts(){
  const p = BASE_PTS.map(x => [...x]);
  if(document.getElementById("gout").checked) p.push([9.5, 2.0]);
  return p;
}
function gOLS(pts){
  const n = pts.length;
  const mx = pts.reduce((s,p) => s+p[0], 0)/n, my = pts.reduce((s,p) => s+p[1], 0)/n;
  let num = 0, den = 0;
  pts.forEach(([x,y]) => { num += (x-mx)*(y-my); den += (x-mx)**2; });
  const w = num/den;
  return [w, my - w*mx];
}
function gLoss(pts, w, b){
  return pts.reduce((s,[x,y]) => s + (w*x + b - y)**2, 0) / pts.length;
}
function gStep(){
  const pts = gPts(), lr = +document.getElementById("glr").value || 0.03, n = pts.length;
  let dw = 0, db = 0;
  pts.forEach(([x,y]) => { const e = GW*x + GB - y; dw += 2*e*x/n; db += 2*e/n; });
  GW -= lr*dw; GB -= lr*db; GSTEPS++;
}
function gRender(){
  const pts = gPts();
  const [ow, ob] = gOLS(pts);
  const W = 560, H = 220, pad = 30;
  const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]).concat([0, 22]);
  const xmin = 0, xmax = Math.max(...xs) + 1, ymin = Math.min(...ys, 0), ymax = Math.max(...ys);
  const sx = x => pad + (x - xmin) / (xmax - xmin) * (W - 2*pad);
  const sy = y => H - pad - (y - ymin) / (ymax - ymin) * (H - 2*pad);
  const line = (w, b, col, dash) => {
    const y1 = w*xmin + b, y2 = w*xmax + b;
    return `<line x1="${sx(xmin)}" y1="${sy(Math.max(ymin, Math.min(ymax, y1)))}"
      x2="${sx(xmax)}" y2="${sy(Math.max(ymin, Math.min(ymax, y2)))}"
      stroke="${col}" stroke-width="2" ${dash ? 'stroke-dasharray="5 4"' : ''}/>`;
  };
  const dots = pts.map(([x,y], i) =>
    `<circle cx="${sx(x)}" cy="${sy(y)}" r="4" fill="${i === 10 ? 'var(--tomb)' : 'var(--muted)'}"/>`).join("");
  document.getElementById("gview3").innerHTML =
    `<figure style="margin:0"><svg viewBox="0 0 ${W} ${H}">
       <line x1="${pad}" y1="${H-pad}" x2="${W-pad}" y2="${H-pad}" stroke="var(--rule)"/>
       <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${H-pad}" stroke="var(--rule)"/>
       ${line(ow, ob, "var(--ok)", true)}
       ${line(GW, GB, "var(--probe)", false)}
       ${dots}
       <text class="sv-l" x="${W-pad}" y="${H-pad+16}" text-anchor="end">x</text>
     </svg>
     <figcaption>vàng: đường hiện tại của gradient descent · xanh nét đứt: nghiệm tối ưu OLS · đỏ: điểm ngoại lai</figcaption></figure>`;
  document.getElementById("gw").textContent = GW.toFixed(3);
  document.getElementById("gb").textContent = GB.toFixed(3);
  const L = gLoss(pts, GW, GB);
  document.getElementById("gloss").textContent = isFinite(L) ? L.toFixed(3) : "phân kỳ";
  document.getElementById("gsteps").textContent = GSTEPS;
  document.getElementById("gopt").textContent = `w=${ow.toFixed(3)} b=${ob.toFixed(3)}`;
}
function gReset3(){ gStop3(); GW = 0; GB = 0; GSTEPS = 0; gRender(); }
function gStop3(){ if(GTIMER3){ clearInterval(GTIMER3); GTIMER3 = null;
  document.getElementById("gauto3").textContent = "Tự chạy"; } }

document.getElementById("ggo").addEventListener("click", () => { for(let i=0;i<10;i++) gStep(); gRender(); });
document.getElementById("grst3").addEventListener("click", gReset3);
document.getElementById("gout").addEventListener("change", gReset3);
document.getElementById("gauto3").addEventListener("click", () => {
  if(GTIMER3) return gStop3();
  document.getElementById("gauto3").textContent = "Dừng";
  GTIMER3 = setInterval(() => { for(let i=0;i<3;i++) gStep(); gRender(); }, 120);
});
gReset3();

/* ---------------- lab 2: ngưỡng quyết định ---------------- */
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
