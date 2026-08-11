(function(){
/* ---------------- lab: binary search step-through ---------------- */
let A = [], T = 4, LO = 0, HI = 0, MID = -1, MODE = "lower", ST = 0, DONE = false, RES = null;

function bParse(){
  return (document.getElementById("arr").value || "")
    .split(/[\s,]+/).filter(Boolean).map(Number).filter(x => !isNaN(x)).slice(0, 16);
}
function bRender(note){
  const cells = A.map((v, i) => {
    const inRange = MODE === "exact" ? (i >= LO && i <= HI) : (i >= LO && i < HI);
    let mark = "";
    if(i === MID) mark = "mid";
    else if(i === LO) mark = "lo";
    else if(MODE === "exact" && i === HI) mark = "hi";
    let bg = "var(--raise)", fg = "var(--muted)";
    if(inRange){ bg = "var(--panel)"; fg = "var(--text)"; }
    if(i === MID){ bg = "var(--probe)"; fg = "#0E141B"; }
    if(DONE && RES !== null && i === RES){ bg = "var(--ok)"; fg = "#0E141B"; }
    return `<div class="slot" style="border-color:${i===MID?'var(--probe)':'var(--rule)'}">
      <i>${mark || i}</i><u style="background:${bg};color:${fg};font-weight:${inRange?600:400}">${v}</u></div>`;
  }).join("");
  document.getElementById("bview").innerHTML =
    `<div class="rail" style="grid-template-columns:repeat(${Math.max(A.length,1)},minmax(0,1fr))">${cells}</div>`;
  document.getElementById("brange").textContent =
    MODE === "exact" ? `[${LO}, ${HI}]` : `[${LO}, ${HI})`;
  document.getElementById("bsteps").textContent = ST;
  if(note){
    const log = document.getElementById("blog");
    log.insertAdjacentHTML("afterbegin", `<div><span>bước ${ST}</span><span>${note}</span><span></span></div>`);
    while(log.children.length > 8) log.removeChild(log.lastChild);
  }
}
function bStep(){
  if(DONE) return;
  const over = MODE === "exact" ? LO > HI : LO >= HI;
  if(over){
    DONE = true; MID = -1;
    if(MODE === "exact"){ RES = null; document.getElementById("bres").textContent = "không tìm thấy"; }
    else {
      RES = LO < A.length ? LO : null;
      document.getElementById("bres").textContent =
        `chỉ số ${LO}` + (LO < A.length ? ` (giá trị ${A[LO]})` : " — hết mảng");
    }
    bRender("khoảng rỗng → dừng");
    return;
  }
  ST++;
  MID = LO + ((HI - LO) >> 1);
  const v = A[MID];
  let note;
  if(MODE === "exact"){
    if(v === T){ DONE = true; RES = MID;
      document.getElementById("bres").textContent = `tìm thấy ở chỉ số ${MID}`;
      bRender(`a[${MID}] = ${v} = target → xong`); return; }
    if(v < T){ note = `a[${MID}]=${v} &lt; ${T} → lo = ${MID+1}`; LO = MID + 1; }
    else     { note = `a[${MID}]=${v} &gt; ${T} → hi = ${MID-1}`; HI = MID - 1; }
  } else if(MODE === "lower"){
    if(v < T){ note = `a[${MID}]=${v} &lt; ${T} → loại mid, lo = ${MID+1}`; LO = MID + 1; }
    else     { note = `a[${MID}]=${v} ≥ ${T} → giữ mid, hi = ${MID}`; HI = MID; }
  } else {
    if(v <= T){ note = `a[${MID}]=${v} ≤ ${T} → loại mid, lo = ${MID+1}`; LO = MID + 1; }
    else      { note = `a[${MID}]=${v} &gt; ${T} → giữ mid, hi = ${MID}`; HI = MID; }
  }
  bRender(note);
}
function bReset(){
  A = bParse(); if(!A.length) A = [1,3,4,4,4,7,9,11,15,20];
  A.sort((x,y) => x - y);
  document.getElementById("arr").value = A.join(" ");
  T = +document.getElementById("tgt").value || 0;
  MODE = document.getElementById("mode").value;
  LO = 0; HI = MODE === "exact" ? A.length - 1 : A.length;
  MID = -1; ST = 0; DONE = false; RES = null;
  document.getElementById("blog").innerHTML = "";
  document.getElementById("bres").textContent = "đang chạy";
  bRender(null);
}
document.getElementById("bstep").addEventListener("click", bStep);
document.getElementById("brst").addEventListener("click", bReset);
["arr","tgt","mode"].forEach(id => document.getElementById(id).addEventListener("change", bReset));
bReset();
})();
