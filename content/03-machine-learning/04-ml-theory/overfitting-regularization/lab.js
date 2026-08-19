(function(){
/* ---------------- lab: bậc đa thức ---------------- */
/* dữ liệu: y = 1 + 2x - 0.6x² + nhiễu, x trong [-1, 1] */
const OX = [-1,-0.82,-0.64,-0.45,-0.27,-0.09,0.09,0.27,0.45,0.64,0.82,1];
const ONOISE = [0.12,-0.18,0.09,0.21,-0.14,0.06,-0.22,0.16,-0.08,0.19,-0.11,0.13];
function otrue(x){ return 1 + 2*x - 0.6*x*x; }

function solve(A, b){                       /* Gauss với chọn trục từng phần */
  const n = b.length;
  const M = A.map((r,i) => [...r, b[i]]);
  for(let c = 0; c < n; c++){
    let p = c;
    for(let r = c+1; r < n; r++) if(Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    if(Math.abs(M[p][c]) < 1e-12) return null;
    [M[c], M[p]] = [M[p], M[c]];
    for(let r = 0; r < n; r++){
      if(r === c) continue;
      const f = M[r][c] / M[c][c];
      for(let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
    }
  }
  return M.map((r,i) => r[n] / r[i]);
}
function polyfit(xs, ys, d){
  const n = d + 1;
  const A = Array.from({length:n}, () => new Array(n).fill(0));
  const b = new Array(n).fill(0);
  for(let i = 0; i < n; i++){
    for(let j = 0; j < n; j++) A[i][j] = xs.reduce((s,x) => s + Math.pow(x, i+j), 0);
    b[i] = xs.reduce((s,x,k) => s + ys[k] * Math.pow(x, i), 0);
  }
  return solve(A, b) || [0];
}
const eva = (c, x) => c.reduce((s,v,i) => s + v * Math.pow(x, i), 0);

function oRender(){
  const d = Math.max(0, Math.min(5, +document.getElementById("odeg").value || 0));
  const useNoise = document.getElementById("onoise").checked;
  /* train: điểm chỉ số chẵn · validation: chỉ số lẻ */
  const trX = [], trY = [], vaX = [], vaY = [];
  OX.forEach((x, i) => {
    const y = otrue(x) + (useNoise ? ONOISE[i] : 0);
    if(i % 2 === 0){ trX.push(x); trY.push(y); } else { vaX.push(x); vaY.push(y); }
  });
  const c = polyfit(trX, trY, Math.min(d, trX.length - 1));
  const mse = (xs, ys) => xs.reduce((s,x,i) => s + (eva(c,x) - ys[i])**2, 0) / xs.length;
  const etr = mse(trX, trY), eva_ = mse(vaX, vaY);

  const W = 560, H = 210, pad = 26;
  const sx = x => pad + (x + 1) / 2 * (W - 2*pad);
  const sy = y => H - pad - (y + 1.2) / 4.4 * (H - 2*pad);
  let path = "";
  for(let i = 0; i <= 120; i++){
    const x = -1 + 2*i/120, y = Math.max(-1.2, Math.min(3.2, eva(c, x)));
    path += (i ? " L" : "M") + sx(x) + " " + sy(y);
  }
  let tpath = "";
  for(let i = 0; i <= 60; i++){
    const x = -1 + 2*i/60;
    tpath += (i ? " L" : "M") + sx(x) + " " + sy(otrue(x));
  }
  const dots = (xs, ys, col) => xs.map((x,i) =>
    `<circle cx="${sx(x)}" cy="${sy(ys[i])}" r="4" fill="${col}"/>`).join("");

  document.getElementById("oview").innerHTML =
    `<figure style="margin:0"><svg viewBox="0 0 ${W} ${H}">
      <path d="${tpath}" stroke="var(--rule)" stroke-width="2" fill="none" stroke-dasharray="4 4"/>
      <path d="${path}" stroke="var(--probe)" stroke-width="2" fill="none"/>
      ${dots(trX, trY, "var(--filled)")}
      ${dots(vaX, vaY, "var(--ok)")}
    </svg><figcaption>vàng: đa thức bậc ${d} vừa fit · xám nét đứt: hàm thật ·
      xanh dương: điểm train · xanh lá: điểm validation</figcaption></figure>`;
  document.getElementById("oetr").textContent = etr.toFixed(4);
  document.getElementById("oeva").textContent = eva_.toFixed(4);
  const diag = eva_ > 4*Math.max(etr, 1e-6) && d >= 4 ? "overfit"
             : (etr > 0.15 ? "underfit" : "vừa đủ");
  const col = diag === "vừa đủ" ? "var(--ok)" : "var(--tomb)";
  document.getElementById("odiag").innerHTML = `<span style="color:${col}">${diag}</span>`;
}
["odeg","onoise"].forEach(id => {
  document.getElementById(id).addEventListener("input", oRender);
  document.getElementById(id).addEventListener("change", oRender);
});
document.getElementById("orst").addEventListener("click", () => {
  document.getElementById("odeg").value = 3;
  document.getElementById("onoise").checked = true; oRender();
});
oRender();
})();
