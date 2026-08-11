(function(){
/* ---------------- lab: confusion matrix ---------------- */
const NBIN = 20, NTOTAL = 10000;
function mSim(){
  const prev = +document.getElementById("mprev").value / 100;
  const sep = +document.getElementById("msep").value;
  const thr = Math.min(0.95, Math.max(0.05, +document.getElementById("mthr").value || 0.5));

  /* phân phối điểm: dương lệch về phải, âm lệch về trái — dùng hàm mũ đơn giản, tất định */
  const posD = [], negD = [];
  for(let i = 0; i < NBIN; i++){
    const s = (i + 0.5) / NBIN;
    posD.push(Math.exp(sep * s));
    negD.push(Math.exp(sep * (1 - s)));
  }
  const nz = a => { const t = a.reduce((x,y) => x+y, 0); return a.map(v => v/t); };
  const P = nz(posD), N = nz(negD);
  const nPos = NTOTAL * prev, nNeg = NTOTAL * (1 - prev);

  /* confusion tại ngưỡng */
  let tp = 0, fn = 0, fp = 0, tn = 0;
  for(let i = 0; i < NBIN; i++){
    const s = (i + 0.5) / NBIN;
    if(s >= thr){ tp += nPos * P[i]; fp += nNeg * N[i]; }
    else        { fn += nPos * P[i]; tn += nNeg * N[i]; }
  }
  /* quét ngưỡng để tính AUC */
  const roc = [], pr = [];
  for(let k = NBIN; k >= 0; k--){
    let TP = 0, FP = 0;
    for(let i = k; i < NBIN; i++){ TP += nPos * P[i]; FP += nNeg * N[i]; }
    const tpr = TP / nPos, fpr = FP / nNeg;
    const prec = (TP + FP) > 0 ? TP / (TP + FP) : 1;
    roc.push([fpr, tpr]); pr.push([tpr, prec]);
  }
  const auc = arr => {
    let a = 0;
    for(let i = 1; i < arr.length; i++) a += (arr[i][0] - arr[i-1][0]) * (arr[i][1] + arr[i-1][1]) / 2;
    return a;
  };
  return {tp, fp, fn, tn, prev, thr, rocAuc: auc(roc), prAuc: auc(pr)};
}
function mRender3(){
  const r = mSim();
  const R = v => Math.round(v).toLocaleString("vi-VN");
  const prec = r.tp + r.fp > 0 ? r.tp/(r.tp+r.fp) : NaN;
  const rec  = r.tp + r.fn > 0 ? r.tp/(r.tp+r.fn) : NaN;
  const f1   = (prec && rec) ? 2*prec*rec/(prec+rec) : NaN;
  const acc  = (r.tp + r.tn) / NTOTAL;
  const pct = v => isNaN(v) ? "–" : (100*v).toFixed(1) + "%";

  const cell = (v, lab, col) =>
    `<td><div class="cell" style="background:${col};color:#0E141B;padding:11px 6px">
      <div style="font-size:14px">${R(v)}</div>
      <div style="font-size:9.5px;opacity:.75">${lab}</div></div></td>`;

  document.getElementById("mview3").innerHTML =
    `<div class="hm"><table style="min-width:380px">
      <tr><th></th><th>thực tế DƯƠNG</th><th>thực tế ÂM</th></tr>
      <tr><td class="rl">dự đoán DƯƠNG</td>${cell(r.tp,"TP","var(--ok)")}${cell(r.fp,"FP","var(--tomb)")}</tr>
      <tr><td class="rl">dự đoán ÂM</td>${cell(r.fn,"FN","var(--tomb)")}${cell(r.tn,"TN","var(--raise)")}</tr>
    </table></div>
    <table style="margin-top:14px">
      <tr><th>Metric</th><th>Giá trị</th><th>Nhận xét</th></tr>
      <tr><td class="mono">accuracy</td><td style="font-family:var(--mono)">${pct(acc)}</td>
          <td style="font-size:13px;color:var(--muted)">${r.prev <= 0.1 ? "đẹp giả tạo — lớp âm chi phối" : "dùng được khi cân bằng"}</td></tr>
      <tr><td class="mono">precision</td><td style="color:var(--probe);font-family:var(--mono)">${pct(prec)}</td>
          <td style="font-size:13px;color:var(--muted)">trong ${R(r.tp+r.fp)} ca báo dương có ${R(r.tp)} ca đúng</td></tr>
      <tr><td class="mono">recall</td><td style="color:var(--probe);font-family:var(--mono)">${pct(rec)}</td>
          <td style="font-size:13px;color:var(--muted)">bắt được ${R(r.tp)} / ${R(r.tp+r.fn)} ca dương thật</td></tr>
      <tr><td class="mono">F1</td><td style="font-family:var(--mono)">${pct(f1)}</td>
          <td style="font-size:13px;color:var(--muted)">trung bình điều hoà</td></tr>
      <tr><td class="mono">ROC-AUC</td><td style="color:var(--filled);font-family:var(--mono)">${r.rocAuc.toFixed(3)}</td>
          <td style="font-size:13px;color:var(--muted)">gần như KHÔNG đổi khi tỉ lệ lớp đổi</td></tr>
      <tr><td class="mono">PR-AUC</td><td style="color:var(--filled);font-family:var(--mono)">${r.prAuc.toFixed(3)}</td>
          <td style="font-size:13px;color:var(--muted)">mức cơ sở ngẫu nhiên = ${r.prev.toFixed(3)}</td></tr>
    </table>`;
}
["mprev","mthr","msep"].forEach(id => {
  document.getElementById(id).addEventListener("input", mRender3);
  document.getElementById(id).addEventListener("change", mRender3);
});
mRender3();
})();
