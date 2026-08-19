(function(){
/* ---------------- lab: dựng heap ---------------- */
let HA = [], HMODE = "heapify", HQ = [], HCMP = 0, HSWP = 0, HDONE = false, HTIMER = null, HHI = [];

function hParse(){
  return (document.getElementById("harr").value || "")
    .split(/[\s,]+/).filter(Boolean).map(Number).filter(x => !isNaN(x)).slice(0, 15);
}
function hRender(note){
  const n = HA.length;
  let rows = "", i = 0, w = 1;
  while(i < n){
    const cells = [];
    for(let k = 0; k < w && i < n; k++, i++){
      const hot = HHI.includes(i);
      const bg = hot ? "var(--probe)" : "var(--raise)";
      const fg = hot ? "#0E141B" : "var(--text)";
      cells.push(`<div class="slot" style="border-color:${hot?'var(--probe)':'var(--rule)'};min-width:44px">
        <i>${i}</i><u style="background:${bg};color:${fg};font-weight:${hot?600:400}">${HA[i]}</u></div>`);
    }
    rows += `<div style="display:flex;gap:4px;justify-content:center;margin-bottom:4px">${cells.join("")}</div>`;
    w *= 2;
  }
  document.getElementById("hview").innerHTML =
    rows + `<p class="legend" style="margin-top:8px"><span>mảng: [${HA.join(", ")}]</span></p>`;
  document.getElementById("hcmp").textContent = HCMP;
  document.getElementById("hswp").textContent = HSWP;
  document.getElementById("hstate").textContent = HDONE ? "xong — đã là heap" : "đang dựng";
  if(note){
    const log = document.getElementById("hlog");
    log.insertAdjacentHTML("afterbegin", `<div><span>${HSWP} đổi</span><span>${note}</span><span></span></div>`);
    while(log.children.length > 8) log.removeChild(log.lastChild);
  }
}
function siftDownOnce(i, n){
  const l = 2*i+1, r = 2*i+2;
  let m = i;
  if(l < n){ HCMP++; if(HA[l] < HA[m]) m = l; }
  if(r < n){ HCMP++; if(HA[r] < HA[m]) m = r; }
  if(m === i) return -1;
  [HA[i], HA[m]] = [HA[m], HA[i]]; HSWP++;
  return m;
}
function hStep(){
  if(HDONE) return;
  if(HMODE === "heapify"){
    if(!HQ.length){ HDONE = true; HHI = []; hRender("hết nút cần sift — mảng đã là heap"); return; }
    let i = HQ[0];
    const m = siftDownOnce(i, HA.length);
    if(m === -1){ HQ.shift(); HHI = [i]; hRender(`nút ${i} đã đúng chỗ`); }
    else { HQ[0] = m; HHI = [i, m]; hRender(`đổi ${i} ↔ ${m} — tiếp tục chìm`); }
  } else {
    if(HQ.length === 0){ HDONE = true; HHI = []; hRender("đã push hết — mảng là heap"); return; }
    let i = HQ[0];
    if(i === 0){ HQ.shift(); HHI = [0]; hRender("phần tử 0 không có cha"); return; }
    const p = (i - 1) >> 1;
    HCMP++;
    if(HA[p] <= HA[i]){ HQ.shift(); HHI = [i]; hRender(`a[${p}] ≤ a[${i}] → đúng chỗ, push tiếp`); }
    else {
      [HA[p], HA[i]] = [HA[i], HA[p]]; HSWP++;
      HQ[0] = p; HHI = [p, i]; hRender(`đổi ${i} ↔ ${p} — tiếp tục nổi lên`);
    }
  }
}
function hReset(){
  hStop();
  HA = hParse(); if(!HA.length) HA = [9,4,7,1,8,2,6,3];
  document.getElementById("harr").value = HA.join(" ");
  HMODE = document.getElementById("hmode").value;
  HCMP = 0; HSWP = 0; HDONE = false; HHI = [];
  HQ = [];
  if(HMODE === "heapify"){ for(let i = (HA.length >> 1) - 1; i >= 0; i--) HQ.push(i); }
  else { for(let i = 1; i < HA.length; i++) HQ.push(i); }
  if(!HQ.length) HDONE = true;
  document.getElementById("hlog").innerHTML = "";
  hRender(null);
}
function hStop(){ if(HTIMER){ clearInterval(HTIMER); HTIMER = null;
  document.getElementById("hauto").textContent = "Tự chạy"; } }

document.getElementById("hstep").addEventListener("click", hStep);
document.getElementById("hrst").addEventListener("click", hReset);
["harr","hmode"].forEach(id => document.getElementById(id).addEventListener("change", hReset));
document.getElementById("hauto").addEventListener("click", () => {
  if(HTIMER) return hStop();
  if(HDONE) hReset();
  document.getElementById("hauto").textContent = "Dừng";
  HTIMER = setInterval(() => { hStep(); if(HDONE) hStop(); }, 550);
});
hReset();
})();
