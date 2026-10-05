(function(){
/* ---------------- lab: monotonic stack step-through ---------------- */
let MA = [], MI = -1, MST = [], MRES = [], MOPS = 0, MDONE = false, MT = null;

function mParse(){
  return (document.getElementById("marr").value || "")
    .split(/[\s,]+/).filter(Boolean).map(Number).filter(x => !isNaN(x)).slice(0, 14);
}
function mRender(note){
  const cells = MA.map((v, i) => {
    const onStack = MST.includes(i);
    let bg = "var(--raise)", fg = "var(--muted)";
    if(onStack){ bg = "var(--filled)"; fg = "var(--on-fill)"; }
    if(i === MI){ bg = "var(--probe)"; fg = "var(--on-fill)"; }
    if(MRES[i] !== undefined && MRES[i] !== -1 && !onStack && i !== MI){ bg = "var(--panel)"; fg = "var(--ok)"; }
    return `<div class="slot"><i>${i}</i>
      <u style="background:${bg};color:${fg};font-weight:${onStack||i===MI?600:400}">${v}</u></div>`;
  }).join("");
  const res = MA.map((_, i) => {
    const r = MRES[i];
    return `<div class="slot"><i>${i}</i><u style="color:${r===undefined?'var(--rule)':'var(--ok)'}">${r===undefined?"?":r}</u></div>`;
  }).join("");
  const cols = Math.max(MA.length, 1);
  document.getElementById("mview").innerHTML =
    `<p class="legend" style="margin:2px 0 5px"><span>array — amber is the element being considered, blue is currently in the stack</span></p>
     <div class="rail" style="grid-template-columns:repeat(${cols},minmax(0,1fr))">${cells}</div>
     <p class="legend" style="margin:14px 0 5px"><span>result — nearest larger element to the right</span></p>
     <div class="rail" style="grid-template-columns:repeat(${cols},minmax(0,1fr))">${res}</div>`;
  document.getElementById("mstack").textContent = MST.length ? "[" + MST.join(", ") + "]" : "empty";
  document.getElementById("mops").textContent = MOPS;
  if(note){
    const log = document.getElementById("mlog");
    log.insertAdjacentHTML("afterbegin", `<div><span>i=${MI}</span><span>${note}</span><span></span></div>`);
    while(log.children.length > 8) log.removeChild(log.lastChild);
  }
}
function mStep(){
  if(MDONE) return;
  MI++;
  if(MI >= MA.length){
    MDONE = true; mStop();
    MST.forEach(i => { if(MRES[i] === undefined) MRES[i] = -1; });
    MST = []; MI = -1;
    mRender("end of array — whatever is left in the stack has nothing larger → -1");
    return;
  }
  const x = MA[MI];
  let popped = [];
  while(MST.length && MA[MST[MST.length-1]] < x){
    const j = MST.pop(); MRES[j] = x; MOPS++; popped.push(j);
  }
  MST.push(MI); MOPS++;
  const note = popped.length
    ? `${x} resolves index ${popped.join(", ")} → pop, then push ${MI}`
    : `nothing smaller than ${x} on top → just push ${MI}`;
  mRender(note);
}
function mReset(){
  mStop();
  MA = mParse(); if(!MA.length) MA = [2,1,5,6,2,3];
  document.getElementById("marr").value = MA.join(" ");
  MI = -1; MST = []; MRES = []; MOPS = 0; MDONE = false;
  document.getElementById("mlog").innerHTML = "";
  mRender(null);
}
function mStop(){ if(MT){ clearInterval(MT); MT = null;
  document.getElementById("mauto").textContent = "Auto run"; } }

document.getElementById("mstep").addEventListener("click", mStep);
document.getElementById("mrst").addEventListener("click", mReset);
document.getElementById("marr").addEventListener("change", mReset);
document.getElementById("mauto").addEventListener("click", () => {
  if(MT) return mStop();
  if(MDONE) mReset();
  document.getElementById("mauto").textContent = "Stop";
  MT = setInterval(() => { mStep(); if(MDONE) mStop(); }, 800);
});
mReset();
})();
