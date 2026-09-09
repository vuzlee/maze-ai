(function(){
/* ---------------- lab: ngưỡng quyết định ---------------- */
const CASES = {
  balanced: [[0.95,1],[0.88,1],[0.82,1],[0.71,1],[0.66,0],[0.58,1],[0.52,0],[0.47,1],[0.41,0],[0.33,0],[0.22,0],[0.11,0]]
};
function thrCalc(){
  const raw = parseFloat(document.getElementById("thr").value);
  const t = Math.min(1, Math.max(0, isNaN(raw) ? 0.5 : raw));   // 0 là ngưỡng hợp lệ, đừng để || nuốt mất
  const data = CASES.balanced;
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
  const X0 = 60, X1 = 830;                              // trục xác suất 0..1
  const px = p => X0 + (X1 - X0) * p;
  const rows = data.map(([p, y], i) => {
    const pred = p >= t;
    const ok = pred === (y === 1);
    const cy = 54 + i * 21;
    const col = ok ? (y === 1 ? "var(--ok)" : "var(--rule-hi)") : "var(--tomb)";
    const r = y === 1 ? 5.5 : 4.5;
    const shape = y === 1
      ? `<circle cx="${px(p).toFixed(1)}" cy="${cy}" r="${r}" fill="${col}"/>`
      : `<rect x="${(px(p)-r).toFixed(1)}" y="${cy-r}" width="${2*r}" height="${2*r}" rx="1" fill="none" stroke="${col}" stroke-width="1.6"/>`;
    return `<line x1="${X0}" y1="${cy}" x2="${px(p).toFixed(1)}" y2="${cy}" stroke="var(--rule)" stroke-width="1"/>
      ${shape}
      <text class="sv-l" x="${(px(p)+11).toFixed(1)}" y="${cy+4}" fill="${col}">${p.toFixed(2)}</text>`;
  }).join("");
  const xt = px(t).toFixed(1);
  const chart = `<svg viewBox="0 0 900 340" role="img" aria-label="Mười hai mẫu xếp theo xác suất model dự đoán, đường ngưỡng cắt chúng thành hai bên: bên phải bị gọi là dương, bên trái bị gọi là âm">
  <text class="sv-hv" x="0" y="16">MỖI HÀNG LÀ MỘT MẪU · VỊ TRÍ LÀ XÁC SUẤT MODEL ĐOÁN</text>
  <rect x="${xt}" y="34" width="${(X1-px(t)).toFixed(1)}" height="${12+data.length*21}" fill="rgba(var(--amber-a),.07)"/>
  <line x1="${xt}" y1="30" x2="${xt}" y2="${46+data.length*21}" stroke="var(--probe)" stroke-width="1.8" stroke-dasharray="5 3"/>
  <text class="sv-m" x="${xt}" y="24" text-anchor="middle" fill="var(--probe)">ngưỡng ${t.toFixed(2)}</text>
  <text class="sv-d" x="${(+xt-9).toFixed(1)}" y="${76+data.length*21}" text-anchor="end">← gọi là ÂM</text>
  <text class="sv-d" x="${(+xt+9).toFixed(1)}" y="${76+data.length*21}" fill="var(--probe)">gọi là DƯƠNG →</text>
  <line x1="${X0}" y1="${40+data.length*21}" x2="${X1}" y2="${40+data.length*21}" stroke="var(--rule-hi)"/>
  <text class="sv-l" x="${X0}" y="${56+data.length*21}" text-anchor="middle">0</text>
  <text class="sv-l" x="${X1}" y="${56+data.length*21}" text-anchor="middle">1</text>
  ${rows}</svg>`;
  const fmt = v => isNaN(v) ? "–" : (100*v).toFixed(0) + "%";
  document.getElementById("thrview").innerHTML =
    `<figure class="scrollx" style="margin:2px 0 0">${chart}</figure>
     <p class="legend"><span><b style="background:var(--ok)"></b>nhãn thật DƯƠNG</span><span><b style="border:1.6px solid var(--rule-hi);background:none"></b>nhãn thật ÂM</span><span><b style="background:var(--tomb)"></b>model gọi sai</span></p>
     <div class="mtx" style="margin:18px 0 0">
       <div class="hd"></div><div class="hd">DỰ ĐOÁN DƯƠNG</div><div class="hd">DỰ ĐOÁN ÂM</div>
       <div class="hd rl">THẬT DƯƠNG</div>
       <div class="q ok"><b>TP = ${tp}</b><span>bắt đúng</span></div>
       <div class="q bad"><b>FN = ${fn}</b><span>bỏ sót</span></div>
       <div class="hd rl">THẬT ÂM</div>
       <div class="q bad"><b>FP = ${fp}</b><span>báo nhầm</span></div>
       <div class="q ok"><b>TN = ${tn}</b><span>bỏ qua đúng</span></div>
     </div>
     <table style="margin-top:14px"><tr><th>Chỉ số</th><th>Giá trị</th><th>Tính từ ô nào</th></tr>
       <tr><td class="mono">precision</td><td style="color:var(--probe);font-family:var(--mono)">${fmt(prec)}</td>
           <td style="font-size:13px;color:var(--muted)">TP / cột dự đoán dương = ${tp} / ${tp+fp}</td></tr>
       <tr><td class="mono">recall</td><td style="color:var(--probe);font-family:var(--mono)">${fmt(rec)}</td>
           <td style="font-size:13px;color:var(--muted)">TP / hàng thật dương = ${tp} / ${tp+fn}</td></tr>
       <tr><td class="mono">F1</td><td style="font-family:var(--mono)">${fmt(f1)}</td>
           <td style="font-size:13px;color:var(--muted)">trung bình điều hoà của hai chỉ số trên</td></tr>
       <tr><td class="mono">accuracy</td><td style="font-family:var(--mono)">${fmt(acc)}</td>
           <td style="font-size:13px;color:var(--muted)">hai ô chéo xanh / cả bốn ô</td></tr>
     </table>`;
}
document.getElementById("thr").addEventListener("input", thrCalc);
thrCalc();
})();
