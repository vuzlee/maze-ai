(function(){
/* ---------------- lab: DSU từng bước ---------------- */
let UE = [], UI = 0, UP = [], USZ = [], UHOPS = 0, UCYC = 0, UDONE = false, UTIMER = null, UN = 8, UHOT = [];

function uParse(){
  const raw = (document.getElementById("uedges").value || "").split(/[\s,]+/).filter(Boolean);
  const es = [];
  let maxv = 0;
  raw.forEach(t => {
    const m = t.split("-").map(Number);
    if(m.length === 2 && !isNaN(m[0]) && !isNaN(m[1])){
      es.push(m); maxv = Math.max(maxv, m[0], m[1]);
    }
  });
  UN = Math.max(maxv + 1, 2);
  return es.slice(0, 14);
}
function uFind(x){
  const comp = document.getElementById("ucomp").checked;
  while(UP[x] !== x){
    UHOPS++;
    if(comp) UP[x] = UP[UP[x]];
    x = UP[x];
  }
  return x;
}
function uRender(note){
  const cells = UP.map((p, i) => {
    const hot = UHOT.includes(i);
    const root = p === i;
    let bg = root ? "var(--ok)" : "var(--raise)";
    let fg = root ? "#14110E" : "var(--text)";
    if(hot){ bg = "var(--probe)"; fg = "#14110E"; }
    return `<div class="slot" style="min-width:40px;border-color:${hot?'var(--probe)':'var(--rule)'}">
      <i>${i}</i><u style="background:${bg};color:${fg};font-weight:600">${p}</u></div>`;
  }).join("");
  let groups = 0;
  for(let i = 0; i < UN; i++) if(UP[i] === i) groups++;
  document.getElementById("uview").innerHTML =
    `<p class="legend" style="margin:2px 0 6px"><span>parent[i] — ô xanh là gốc của một nhóm</span></p>
     <div style="display:flex;gap:4px;flex-wrap:wrap">${cells}</div>
     <p class="legend" style="margin-top:10px"><span>cạnh còn lại: ${
       UE.slice(UI).map(e => e[0]+"–"+e[1]).join(", ") || "hết"}</span></p>`;
  document.getElementById("ugroups").textContent = groups;
  document.getElementById("uhops").textContent = UHOPS;
  document.getElementById("ucycles").textContent = UCYC;
  if(note){
    const log = document.getElementById("ulog");
    log.insertAdjacentHTML("afterbegin", `<div><span>#${UI}</span><span>${note}</span><span>${UHOPS} bước leo</span></div>`);
    while(log.children.length > 8) log.removeChild(log.lastChild);
  }
}
function uStep(){
  if(UDONE) return;
  if(UI >= UE.length){ UDONE = true; UHOT = []; uRender("hết cạnh"); return; }
  const [a, b] = UE[UI++];
  const ra = uFind(a), rb = uFind(b);
  UHOT = [a, b];
  if(ra === rb){ UCYC++; uRender(`${a}–${b}: đã cùng nhóm → union trả False, cạnh tạo chu trình`); return; }
  let x = ra, y = rb;
  if(document.getElementById("usize").checked && USZ[x] < USZ[y]){ x = rb; y = ra; }
  UP[y] = x; USZ[x] += USZ[y];
  uRender(`${a}–${b}: gộp gốc ${y} vào gốc ${x} (nhóm mới ${USZ[x]} phần tử)`);
}
function uReset(){
  uStop();
  UE = uParse();
  if(!UE.length){ UE = [[0,1],[1,2],[2,3],[3,4],[5,6],[6,7],[4,5],[0,7]]; UN = 8; }
  UP = Array.from({length: UN}, (_, i) => i);
  USZ = new Array(UN).fill(1);
  UI = 0; UHOPS = 0; UCYC = 0; UDONE = false; UHOT = [];
  document.getElementById("ulog").innerHTML = "";
  uRender(null);
}
function uStop(){ if(UTIMER){ clearInterval(UTIMER); UTIMER = null;
  document.getElementById("uauto").textContent = "Tự chạy"; } }

document.getElementById("ustep").addEventListener("click", uStep);
document.getElementById("urst").addEventListener("click", uReset);
["uedges","ucomp","usize"].forEach(id => document.getElementById(id).addEventListener("change", uReset));
document.getElementById("uauto").addEventListener("click", () => {
  if(UTIMER) return uStop();
  if(UDONE) uReset();
  document.getElementById("uauto").textContent = "Dừng";
  UTIMER = setInterval(() => { uStep(); if(UDONE) uStop(); }, 700);
});
uReset();
})();
