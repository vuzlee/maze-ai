(function(){
/* ---------------- lab: mạng 2-2-1 ---------------- */
const sig = z => 1/(1 + Math.exp(-z));
let NW1, NB1, NW2, NB2, NSTEP = 0, NUPD = 0, NTIMER = null, NST = {};
const NX = [1.0, 0.5];

function nReset(){
  nStop();
  NW1 = [[0.5, -0.3], [0.8, 0.2]];
  NB1 = [0.1, -0.1];
  NW2 = [0.7, -0.4];
  NB2 = 0.2;
  NSTEP = 0; NUPD = 0;
  document.getElementById("blog3").innerHTML = "";
  nCompute(); nRender();
}
function nCompute(){
  const y = +document.getElementById("by").value;
  const z1 = [NW1[0][0]*NX[0] + NW1[0][1]*NX[1] + NB1[0],
              NW1[1][0]*NX[0] + NW1[1][1]*NX[1] + NB1[1]];
  const a1 = z1.map(sig);
  const z2 = NW2[0]*a1[0] + NW2[1]*a1[1] + NB2;
  const a2 = sig(z2);
  const L = -(y*Math.log(a2) + (1-y)*Math.log(1-a2));
  const dz2 = a2 - y;
  const dW2 = [dz2*a1[0], dz2*a1[1]];
  const db2 = dz2;
  const da1 = [NW2[0]*dz2, NW2[1]*dz2];
  const dz1 = [da1[0]*a1[0]*(1-a1[0]), da1[1]*a1[1]*(1-a1[1])];
  const dW1 = [[dz1[0]*NX[0], dz1[0]*NX[1]], [dz1[1]*NX[0], dz1[1]*NX[1]]];
  NST = {y, z1, a1, z2, a2, L, dz2, dW2, db2, da1, dz1, dW1, db1: dz1};
}
const NSTEPS = [
  {t:"forward", k:"z₁", f:s => `z₁ = W₁x + b₁ = [${s.z1.map(v=>v.toFixed(4)).join(", ")}]`},
  {t:"forward", k:"a₁", f:s => `a₁ = σ(z₁) = [${s.a1.map(v=>v.toFixed(4)).join(", ")}]`},
  {t:"forward", k:"z₂", f:s => `z₂ = W₂a₁ + b₂ = ${s.z2.toFixed(4)}`},
  {t:"forward", k:"a₂", f:s => `a₂ = σ(z₂) = ${s.a2.toFixed(4)}  ← dự đoán`},
  {t:"forward", k:"L",  f:s => `L = -[y·log a₂ + (1-y)·log(1-a₂)] = ${s.L.toFixed(4)}`},
  {t:"backward",k:"dz₂",f:s => `∂L/∂z₂ = a₂ - y = ${s.dz2.toFixed(4)}  ← gọn nhờ sigmoid + log loss`},
  {t:"backward",k:"dW₂",f:s => `∂L/∂W₂ = dz₂ · a₁ = [${s.dW2.map(v=>v.toFixed(4)).join(", ")}]`},
  {t:"backward",k:"db₂",f:s => `∂L/∂b₂ = dz₂ = ${s.db2.toFixed(4)}`},
  {t:"backward",k:"da₁",f:s => `∂L/∂a₁ = W₂ᵀ · dz₂ = [${s.da1.map(v=>v.toFixed(4)).join(", ")}]`},
  {t:"backward",k:"dz₁",f:s => `∂L/∂z₁ = ∂L/∂a₁ ⊙ a₁(1-a₁) = [${s.dz1.map(v=>v.toFixed(4)).join(", ")}]`},
  {t:"backward",k:"dW₁",f:s => `∂L/∂W₁ = dz₁ · xᵀ = [[${s.dW1[0].map(v=>v.toFixed(4)).join(", ")}], [${s.dW1[1].map(v=>v.toFixed(4)).join(", ")}]]`}
];
function nRender(note){
  const rows = NSTEPS.map((st, i) => {
    const done = i < NSTEP;
    const active = i === NSTEP - 1;
    const col = st.t === "forward" ? "var(--filled)" : "var(--probe)";
    const bg = active ? col : (done ? "var(--panel)" : "transparent");
    const fg = active ? "#14110E" : (done ? "var(--text)" : "var(--rule)");
    return `<div style="background:${bg};color:${fg};border:1px solid ${done||active?col:'var(--rule)'};
      border-radius:5px;padding:6px 10px;margin-bottom:4px;font-family:var(--mono);font-size:12px;
      font-weight:${active?600:400}">
      <span style="opacity:.6;font-size:10px">${st.t === "forward" ? "→" : "←"}</span>
      ${done || active ? st.f(NST) : st.k + " = ?"}</div>`;
  }).join("");
  const wtab = `<table style="margin-top:14px"><tr><th>Trọng số</th><th>Giá trị hiện tại</th></tr>
    <tr><td class="mono">W₁</td><td style="font-family:var(--mono);font-size:12px">[[${NW1[0].map(v=>v.toFixed(4)).join(", ")}], [${NW1[1].map(v=>v.toFixed(4)).join(", ")}]]</td></tr>
    <tr><td class="mono">b₁</td><td style="font-family:var(--mono);font-size:12px">[${NB1.map(v=>v.toFixed(4)).join(", ")}]</td></tr>
    <tr><td class="mono">W₂</td><td style="font-family:var(--mono);font-size:12px">[${NW2.map(v=>v.toFixed(4)).join(", ")}]</td></tr>
    <tr><td class="mono">b₂</td><td style="font-family:var(--mono);font-size:12px">${NB2.toFixed(4)}</td></tr></table>`;
  document.getElementById("bview3").innerHTML =
    `<p class="legend" style="margin:2px 0 8px"><span>
      x = [1.0, 0.5] · y = ${NST.y} ·
      <b style="background:var(--filled)"></b>forward &nbsp;
      <b style="background:var(--probe)"></b>backward</span></p>${rows}${wtab}`;
  document.getElementById("bloss").textContent = NST.L.toFixed(4);
  document.getElementById("bupdn").textContent = NUPD;
  if(note){
    const log = document.getElementById("blog3");
    log.insertAdjacentHTML("afterbegin", `<div><span>#${NUPD}</span><span>${note}</span><span></span></div>`);
    while(log.children.length > 6) log.removeChild(log.lastChild);
  }
}
function nStep(){
  if(NSTEP < NSTEPS.length){ NSTEP++; nRender(); }
  else nStop();
}
function nUpdate(){
  const lr = +document.getElementById("blr").value || 0.5;
  for(let i = 0; i < 2; i++){
    for(let j = 0; j < 2; j++) NW1[i][j] -= lr * NST.dW1[i][j];
    NB1[i] -= lr * NST.db1[i];
    NW2[i] -= lr * NST.dW2[i];
  }
  NB2 -= lr * NST.db2;
  const old = NST.L;
  NUPD++; NSTEP = NSTEPS.length;
  nCompute();
  nRender(`cập nhật với η = ${lr} — mất mát ${old.toFixed(4)} → ${NST.L.toFixed(4)}`);
}
function nStop(){ if(NTIMER){ clearInterval(NTIMER); NTIMER = null;
  document.getElementById("bauto3").textContent = "Tự chạy"; } }

document.getElementById("bstep3").addEventListener("click", nStep);
document.getElementById("brst3").addEventListener("click", nReset);
document.getElementById("bupd").addEventListener("click", nUpdate);
document.getElementById("by").addEventListener("change", () => { nCompute(); nRender(); });
document.getElementById("bauto3").addEventListener("click", () => {
  if(NTIMER) return nStop();
  if(NSTEP >= NSTEPS.length) NSTEP = 0;
  document.getElementById("bauto3").textContent = "Dừng";
  NTIMER = setInterval(() => { nStep(); if(NSTEP >= NSTEPS.length) nStop(); }, 700);
});
nReset();
})();
