(function(){
/* ---------------- lab: gradient descent ---------------- */
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
})();
