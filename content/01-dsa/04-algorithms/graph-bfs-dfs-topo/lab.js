(function(){
/* ---------------- lab: BFS vs DFS on a grid ---------------- */
const GR = 6, GC = 9;
const WALLS = new Set(["1-2","2-2","3-2","4-2","1-5","2-5","3-5","0-7","1-7","4-6","5-6"]);
const GSTART = "2-0", GGOAL = "3-8";
const GDIRS = [[-1,0],[1,0],[0,-1],[0,1]];
let GFRONT = [], GSEEN = new Map(), GORDER = 0, GDONE = false, GTIMER = null, GHOT = null, GFOUND = null;

function gKey(r,c){ return r + "-" + c; }
function gRender(){
  let html = "";
  for(let r = 0; r < GR; r++){
    const cells = [];
    for(let c = 0; c < GC; c++){
      const k = gKey(r,c);
      let bg = "var(--raise)", fg = "var(--muted)", txt = "·";
      if(WALLS.has(k)){ bg = "var(--strong)"; fg = "var(--rule)"; txt = "▓"; }
      else if(GSEEN.has(k)){ bg = "var(--filled)"; fg = "var(--on-fill)"; txt = GSEEN.get(k); }
      if(k === GSTART){ bg = "var(--ok)"; fg = "var(--on-fill)"; txt = "S"; }
      if(k === GGOAL){ bg = GFOUND !== null ? "var(--ok)" : "var(--tomb)"; fg = "var(--on-fill)"; txt = "G"; }
      if(k === GHOT && k !== GSTART && k !== GGOAL){ bg = "var(--probe)"; fg = "var(--on-fill)"; }
      cells.push(`<div class="slot" style="min-width:30px;border-color:${k===GHOT?'var(--probe)':'var(--rule)'}">
        <u style="background:${bg};color:${fg};padding:5px 0;font-weight:600">${txt}</u></div>`);
    }
    html += `<div style="display:flex;gap:3px;justify-content:center;margin-bottom:3px">${cells.join("")}</div>`;
  }
  document.getElementById("gview").innerHTML = html;
  document.getElementById("gvis").textContent = GSEEN.size;
  document.getElementById("gfront").textContent = GFRONT.length;
  document.getElementById("gfound").textContent =
    GFOUND === null ? (GDONE ? "unreachable" : "–") : GFOUND + " steps";
}
function gStep(){
  if(GDONE) return;
  const mode = document.getElementById("gmode").value;
  if(!GFRONT.length){ GDONE = true; GHOT = null; gRender(); return; }
  const cur = mode === "bfs" ? GFRONT.shift() : GFRONT.pop();
  const [r, c, d] = cur;
  const k = gKey(r,c);
  if(mode === "dfs" && GSEEN.has(k)) return gStep();
  GORDER++;
  GSEEN.set(k, GORDER);
  GHOT = k;
  if(k === GGOAL){ GFOUND = d; GDONE = true; gRender(); return; }
  for(const [dr, dc] of GDIRS){
    const nr = r + dr, nc = c + dc, nk = gKey(nr,nc);
    if(nr < 0 || nr >= GR || nc < 0 || nc >= GC) continue;
    if(WALLS.has(nk) || GSEEN.has(nk)) continue;
    if(mode === "bfs"){
      if(GFRONT.some(x => gKey(x[0],x[1]) === nk)) continue;   /* BFS: not already in the queue */
      GFRONT.push([nr, nc, d+1]);
    } else {
      GFRONT.push([nr, nc, d+1]);                              /* DFS: push anyway, filter on pop */
    }
  }
  gRender();
}
function gReset(){
  gStop();
  const [sr, sc] = GSTART.split("-").map(Number);
  GFRONT = [[sr, sc, 0]]; GSEEN = new Map(); GORDER = 0;
  GDONE = false; GHOT = null; GFOUND = null;
  gRender();
}
function gStop(){ if(GTIMER){ clearInterval(GTIMER); GTIMER = null;
  document.getElementById("gauto").textContent = "Auto run"; } }

document.getElementById("gstep").addEventListener("click", gStep);
document.getElementById("grst").addEventListener("click", gReset);
document.getElementById("gmode").addEventListener("change", gReset);
document.getElementById("gauto").addEventListener("click", () => {
  if(GTIMER) return gStop();
  if(GDONE) gReset();
  document.getElementById("gauto").textContent = "Stop";
  GTIMER = setInterval(() => { gStep(); if(GDONE) gStop(); }, 180);
});
gReset();
})();
