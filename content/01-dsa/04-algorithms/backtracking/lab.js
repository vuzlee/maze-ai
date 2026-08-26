(function(){
/* ---------------- lab: decision tree backtracking ---------------- */
let KTRACE = [], KI = 0, KPATH = [], KRES = [], KCH = 0, KUN = 0, KDONE = false, KTIMER = null, KDEPTH = 0;

function kParse(){
  return (document.getElementById("karr").value || "")
    .split(/[\s,]+/).filter(Boolean).slice(0, 4);
}
/* sinh sẵn toàn bộ chuỗi sự kiện: choose / record / undo */
function kBuild(){
  const a = kParse().length ? kParse() : ["1","2","3"];
  document.getElementById("karr").value = a.join(" ");
  const mode = document.getElementById("kmode").value;
  const ev = [];
  const path = [];
  if(mode === "subsets"){
    (function go(start){
      ev.push({t:"rec", p: path.slice(), d: path.length});
      for(let i = start; i < a.length; i++){
        path.push(a[i]);
        ev.push({t:"ch", v:a[i], p: path.slice(), d: path.length});
        go(i+1);
        ev.push({t:"un", v:a[i], p: path.slice(0,-1), d: path.length-1});
        path.pop();
      }
    })(0);
  } else if(mode === "perm"){
    const used = a.map(() => false);
    (function go(){
      if(path.length === a.length){ ev.push({t:"rec", p: path.slice(), d: path.length}); return; }
      for(let i = 0; i < a.length; i++){
        if(used[i]) continue;
        used[i] = true; path.push(a[i]);
        ev.push({t:"ch", v:a[i], p: path.slice(), d: path.length});
        go();
        ev.push({t:"un", v:a[i], p: path.slice(0,-1), d: path.length-1});
        path.pop(); used[i] = false;
      }
    })();
  } else {
    const K = 2;
    (function go(start){
      if(path.length === K){ ev.push({t:"rec", p: path.slice(), d: path.length}); return; }
      for(let i = start; i < a.length; i++){
        path.push(a[i]);
        ev.push({t:"ch", v:a[i], p: path.slice(), d: path.length});
        go(i+1);
        ev.push({t:"un", v:a[i], p: path.slice(0,-1), d: path.length-1});
        path.pop();
      }
    })(0);
  }
  KTRACE = ev;
}
function kRender(note){
  const bars = KPATH.map(v =>
    `<div class="slot" style="min-width:38px;border-color:var(--probe)">
       <u style="background:var(--probe);color:#14110E;font-weight:600">${v}</u></div>`).join("");
  const res = KRES.map(r =>
    `<span style="font-family:var(--mono);font-size:11.5px;background:var(--raise);border:1px solid var(--rule);
      border-radius:4px;padding:2px 7px;margin:0 4px 4px 0;display:inline-block;color:var(--ok)">
      [${r.join(",")}]</span>`).join("");
  document.getElementById("kview").innerHTML =
    `<p class="legend" style="margin:2px 0 5px"><span>đang dựng — mỗi ô là một lựa chọn đã chọn</span></p>
     <div style="display:flex;gap:4px;min-height:44px">${bars || '<span class="legend"><span>rỗng</span></span>'}</div>
     <p class="legend" style="margin:14px 0 6px"><span>kết quả đã ghi (${KRES.length})</span></p>
     <div>${res || '<span class="legend"><span>chưa có</span></span>'}</div>`;
  document.getElementById("kpath").textContent = "[" + KPATH.join(",") + "]";
  document.getElementById("kdepth").textContent = KDEPTH;
  document.getElementById("kcnt").textContent = KCH + " / " + KUN;
  document.getElementById("kres").textContent = KRES.length;
  if(note){
    const log = document.getElementById("klog");
    log.insertAdjacentHTML("afterbegin", `<div><span>#${KI}</span><span>${note}</span><span></span></div>`);
    while(log.children.length > 8) log.removeChild(log.lastChild);
  }
}
function kStep(){
  if(KDONE) return;
  if(KI >= KTRACE.length){ KDONE = true; kStop();
    kRender(`xong — ${KRES.length} kết quả, ${KCH} lần chọn, ${KUN} lần hoàn tác`); return; }
  const e = KTRACE[KI++];
  KPATH = e.p; KDEPTH = e.d;
  if(e.t === "ch"){ KCH++; kRender(`chọn ${e.v} → đi sâu`); }
  else if(e.t === "un"){ KUN++; kRender(`hoàn tác ${e.v} → thử nhánh khác`); }
  else { KRES.push(e.p.slice()); kRender(`ghi kết quả [${e.p.join(",")}] — nhớ chép, không lưu tham chiếu`); }
}
function kReset(){
  kStop(); kBuild();
  KI = 0; KPATH = []; KRES = []; KCH = 0; KUN = 0; KDONE = false; KDEPTH = 0;
  document.getElementById("klog").innerHTML = "";
  kRender(null);
}
function kStop(){ if(KTIMER){ clearInterval(KTIMER); KTIMER = null;
  document.getElementById("kauto").textContent = "Tự chạy"; } }

document.getElementById("kstep").addEventListener("click", kStep);
document.getElementById("krst").addEventListener("click", kReset);
["kmode","karr"].forEach(id => document.getElementById(id).addEventListener("change", kReset));
document.getElementById("kauto").addEventListener("click", () => {
  if(KTIMER) return kStop();
  if(KDONE) kReset();
  document.getElementById("kauto").textContent = "Dừng";
  KTIMER = setInterval(() => { kStep(); if(KDONE) kStop(); }, 420);
});
kReset();
})();
