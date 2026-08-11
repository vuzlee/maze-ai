(function(){
/* ---------------- lab: tìm điểm chia ---------------- */
/* 12 mẫu 1 chiều: [giá trị, lớp] */
const SPTS = [[1,0],[2,0],[3,0],[4,1],[5,0],[6,1],[7,1],[8,1],[9,0],[10,1],[11,1],[12,1]];

function imp(pts, crit){
  const n = pts.length;
  if(!n) return 0;
  const p1 = pts.filter(p => p[1] === 1).length / n, p0 = 1 - p1;
  if(crit === "gini") return 1 - p1*p1 - p0*p0;
  const lg = p => p > 0 ? p * Math.log2(p) : 0;
  return -(lg(p1) + lg(p0));
}
function sGain(thr, crit){
  const L = SPTS.filter(p => p[0] < thr), R = SPTS.filter(p => p[0] >= thr);
  const n = SPTS.length;
  const parent = imp(SPTS, crit);
  const g = parent - (L.length/n * imp(L, crit) + R.length/n * imp(R, crit));
  return {L, R, parent, iL: imp(L, crit), iR: imp(R, crit), gain: g};
}
function sRender(){
  const thr = +document.getElementById("sthr").value || 5.5;
  const crit = document.getElementById("scrit").value;
  const {L, R, parent, iL, iR, gain} = sGain(thr, crit);

  const cells = SPTS.map(([x, c]) => {
    const left = x < thr;
    const col = c === 1 ? "var(--ok)" : "var(--tomb)";
    return `<div class="slot" style="min-width:38px;border-color:${left?'var(--filled)':'var(--probe)'}">
      <i style="color:${left?'var(--filled)':'var(--probe)'}">${left ? "T" : "P"}</i>
      <u style="background:${col};color:#0E141B;font-weight:600">${x}</u></div>`;
  }).join("");

  /* quét mọi ngưỡng để vẽ đường gain */
  const cands = [];
  for(let t = 1.5; t <= 12; t += 0.5) cands.push([t, sGain(t, crit).gain]);
  const maxG = Math.max(...cands.map(c => c[1]));
  const bars = cands.map(([t, g]) => {
    const h = Math.max(1, Math.round(38 * g / (maxG || 1)));
    const hot = Math.abs(t - thr) < 0.26;
    return `<div style="display:flex;flex-direction:column;justify-content:flex-end;align-items:center;width:20px">
      <div style="height:${h}px;width:11px;background:${hot?'var(--probe)':'var(--rule)'};border-radius:2px"></div>
      <span style="font-family:var(--mono);font-size:8.5px;color:${hot?'var(--probe)':'var(--muted)'};margin-top:3px">${t}</span></div>`;
  }).join("");

  document.getElementById("sview").innerHTML =
    `<p class="legend" style="margin:2px 0 6px"><span>
       <b style="background:var(--ok)"></b>lớp 1 &nbsp;
       <b style="background:var(--tomb)"></b>lớp 0 &nbsp;·&nbsp; T = nhánh trái, P = nhánh phải</span></p>
     <div style="display:flex;gap:4px;flex-wrap:wrap">${cells}</div>
     <p class="legend" style="margin:16px 0 6px"><span>information gain theo từng ngưỡng có thể</span></p>
     <div style="display:flex;gap:2px;align-items:flex-end;height:56px">${bars}</div>`;
  document.getElementById("sp").textContent = parent.toFixed(3);
  document.getElementById("sl").textContent = `${L.length} mẫu · ${iL.toFixed(3)}`;
  document.getElementById("sr").textContent = `${R.length} mẫu · ${iR.toFixed(3)}`;
  document.getElementById("sg").textContent = gain.toFixed(4);
}
document.getElementById("sbest").addEventListener("click", () => {
  const crit = document.getElementById("scrit").value;
  let best = 1.5, bg = -1;
  for(let t = 1.5; t <= 12; t += 0.5){
    const g = sGain(t, crit).gain;
    if(g > bg){ bg = g; best = t; }
  }
  document.getElementById("sthr").value = best;
  sRender();
});
document.getElementById("srst").addEventListener("click", () => {
  document.getElementById("sthr").value = 5.5; sRender();
});
["sthr","scrit"].forEach(id => {
  document.getElementById(id).addEventListener("input", sRender);
  document.getElementById(id).addEventListener("change", sRender);
});
sRender();
})();
