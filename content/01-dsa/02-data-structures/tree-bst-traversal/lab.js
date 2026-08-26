(function(){
/* ---------------- lab: duyệt cây ---------------- */
/* BST: 8 / 3,10 / 1,6,-,14 / -,-,4,7,-,-,13,- */
const TV = {8:{l:3,r:10}, 3:{l:1,r:6}, 10:{l:null,r:14}, 1:{l:null,r:null},
            6:{l:4,r:7}, 14:{l:13,r:null}, 4:{l:null,r:null}, 7:{l:null,r:null}, 13:{l:null,r:null}};
const ROWS = [[8],[3,10],[1,6,null,14],[null,null,4,7,null,null,13,null]];

let TQ = [], TORDER = [], TCUR = null, TDONE = false, TTIMER = null, TSTACK = [];

function tBuild(){
  const mode = document.getElementById("tmode").value;
  TQ = []; TORDER = []; TCUR = null; TDONE = false; TSTACK = [];
  if(mode === "level"){
    const q = [8];
    while(q.length){ const v = q.shift(); TQ.push({v, depth: 0});
      if(TV[v].l !== null) q.push(TV[v].l);
      if(TV[v].r !== null) q.push(TV[v].r); }
  } else {
    const seq = [];
    (function go(v, d){
      if(v === null) return;
      if(mode === "pre") seq.push({v, depth: d});
      go(TV[v].l, d+1);
      if(mode === "in") seq.push({v, depth: d});
      go(TV[v].r, d+1);
      if(mode === "post") seq.push({v, depth: d});
    })(8, 1);
    TQ = seq;
  }
}
function tRender(note){
  let html = "";
  ROWS.forEach(row => {
    const cells = row.map(v => {
      if(v === null) return `<div class="slot" style="border-color:transparent;min-width:40px"><i>&nbsp;</i><u style="color:var(--rule)">·</u></div>`;
      const done = TORDER.includes(v);
      const hot = v === TCUR;
      let bg = "var(--raise)", fg = "var(--muted)";
      if(done){ bg = "var(--ok)"; fg = "#14110E"; }
      if(hot){ bg = "var(--probe)"; fg = "#14110E"; }
      return `<div class="slot" style="border-color:${hot?'var(--probe)':'var(--rule)'};min-width:40px">
        <i>${done ? TORDER.indexOf(v)+1 : "&nbsp;"}</i>
        <u style="background:${bg};color:${fg};font-weight:${done||hot?600:400}">${v}</u></div>`;
    }).join("");
    html += `<div style="display:flex;gap:4px;justify-content:center;margin-bottom:4px">${cells}</div>`;
  });
  document.getElementById("tview").innerHTML =
    html + `<p class="legend" style="margin-top:8px"><span>số nhỏ phía trên ô là thứ tự thăm</span></p>`;
  document.getElementById("torder").textContent = TORDER.length ? TORDER.join(" → ") : "chưa thăm nút nào";
  document.getElementById("tdepth").textContent = TSTACK.length;
  if(note){
    const log = document.getElementById("tlog");
    log.insertAdjacentHTML("afterbegin", `<div><span>#${TORDER.length}</span><span>${note}</span><span></span></div>`);
    while(log.children.length > 8) log.removeChild(log.lastChild);
  }
}
function tStep(){
  if(TDONE) return;
  if(!TQ.length){ TDONE = true; TCUR = null; TSTACK = [];
    tRender("xong — " + TORDER.join(" ")); return; }
  const {v, depth} = TQ.shift();
  TCUR = v; TORDER.push(v);
  TSTACK = new Array(depth).fill(0);
  const mode = document.getElementById("tmode").value;
  const why = mode === "in"   ? "xong nhánh trái → thăm nút này"
            : mode === "post" ? "xong cả hai nhánh → thăm nút này"
            : mode === "pre"  ? "gặp nút → thăm ngay"
            :                   "lấy ra từ hàng đợi";
  tRender(`thăm ${v} — ${why}`);
}
function tReset(){
  tStop(); tBuild();
  document.getElementById("tlog").innerHTML = "";
  tRender(null);
}
function tStop(){ if(TTIMER){ clearInterval(TTIMER); TTIMER = null;
  document.getElementById("tauto").textContent = "Tự chạy"; } }

document.getElementById("tstep").addEventListener("click", tStep);
document.getElementById("trst").addEventListener("click", tReset);
document.getElementById("tmode").addEventListener("change", tReset);
document.getElementById("tauto").addEventListener("click", () => {
  if(TTIMER) return tStop();
  if(TDONE) tReset();
  document.getElementById("tauto").textContent = "Dừng";
  TTIMER = setInterval(() => { tStep(); if(TDONE) tStop(); }, 600);
});
tReset();
})();
