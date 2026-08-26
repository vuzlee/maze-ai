(function(){
/* ---------------- lab: đường ống lười ---------------- */
const SRC = [1,2,3,4,5,6,7,8,9,10,11,12];
let PTRACE = [], PI = 0, POPS = 0, PGOT = 0, PDONE = false, PTIMER = null, PSTATE = [];

/* đường ống: nguồn → lọc số chẵn → nhân đôi → lấy n */
function pBuild(){
  const take = Math.max(1, Math.min(8, +document.getElementById("ptake").value || 3));
  const mode = document.getElementById("pmode").value;
  const ev = [];
  if(mode === "gen"){
    let got = 0;
    for(const x of SRC){
      ev.push({stage: 0, v: x, note: `nguồn phát ${x}`});
      if(x % 2 !== 0){ ev.push({stage: 1, v: x, note: `${x} lẻ → lọc bỏ`, drop: true}); continue; }
      ev.push({stage: 1, v: x, note: `${x} chẵn → cho qua`});
      ev.push({stage: 2, v: x*2, note: `nhân đôi → ${x*2}`});
      got++;
      ev.push({stage: 3, v: x*2, note: `lấy phần tử thứ ${got}`, out: true});
      if(got === take){ ev.push({stage: 3, v: null, note: "đủ hàng → đường ống DỪNG, phần còn lại không bị chạm tới", stop: true}); break; }
    }
  } else {
    SRC.forEach(x => ev.push({stage: 0, v: x, note: `nguồn dựng list: thêm ${x}`}));
    SRC.forEach(x => ev.push({stage: 1, v: x, note: `lọc: ${x} ${x%2===0?"chẵn, giữ":"lẻ, bỏ"}`, drop: x%2!==0}));
    SRC.filter(x => x%2===0).forEach(x => ev.push({stage: 2, v: x*2, note: `nhân đôi: ${x} → ${x*2}`}));
    SRC.filter(x => x%2===0).slice(0, take).forEach((x, i) =>
      ev.push({stage: 3, v: x*2, note: `cắt lấy phần tử thứ ${i+1}`, out: true}));
    ev.push({stage: 3, v: null, note: "xong — nhưng đã xử lý TOÀN BỘ 12 phần tử ở mỗi tầng", stop: true});
  }
  PTRACE = ev;
}
function pRender(note, ev){
  const names = ["nguồn (12 số)", "lọc số chẵn", "nhân đôi", "lấy n phần tử"];
  const cells = names.map((nm, i) => {
    const hot = ev && ev.stage === i;
    return `<div style="flex:1;min-width:110px;background:${hot?'var(--probe)':'var(--panel)'};
      color:${hot?'#14110E':'var(--muted)'};border:1px solid ${hot?'var(--probe)':'var(--rule)'};
      border-radius:6px;padding:9px 11px;font-family:var(--mono);font-size:11.5px;font-weight:${hot?600:400}">
      ${nm}${hot && ev.v !== null ? `<br><span style="font-size:14px">${ev.v}</span>` : "<br><span style='font-size:14px'>·</span>"}</div>`;
  }).join(`<div style="align-self:center;color:var(--rule);font-family:var(--mono)">→</div>`);
  const outs = PSTATE.map(v =>
    `<span style="font-family:var(--mono);font-size:12px;background:var(--raise);border:1px solid var(--ok);
      color:var(--ok);border-radius:4px;padding:2px 8px;margin:0 4px 4px 0;display:inline-block">${v}</span>`).join("");
  document.getElementById("pview").innerHTML =
    `<div style="display:flex;gap:8px;flex-wrap:wrap">${cells}</div>
     <p class="legend" style="margin:14px 0 6px"><span>kết quả lấy được</span></p>
     <div>${outs || '<span class="legend"><span>chưa có</span></span>'}</div>`;
  document.getElementById("pops").textContent = POPS;
  document.getElementById("pgot").textContent = PGOT;
  document.getElementById("pstate").textContent = PDONE ? "xong" : "đang chạy";
  if(note){
    const log = document.getElementById("plog");
    log.insertAdjacentHTML("afterbegin", `<div><span>#${PI}</span><span>${note}</span><span></span></div>`);
    while(log.children.length > 9) log.removeChild(log.lastChild);
  }
}
function pStep(){
  if(PDONE) return;
  if(PI >= PTRACE.length){ PDONE = true; pStop(); pRender("hết", null); return; }
  const ev = PTRACE[PI++];
  if(!ev.stop) POPS++;
  if(ev.out){ PGOT++; PSTATE.push(ev.v); }
  if(ev.stop){ PDONE = true; pStop(); }
  pRender(ev.note, ev);
}
function pReset(){
  pStop(); pBuild();
  PI = 0; POPS = 0; PGOT = 0; PDONE = false; PSTATE = [];
  document.getElementById("plog").innerHTML = "";
  pRender(null, null);
}
function pStop(){ if(PTIMER){ clearInterval(PTIMER); PTIMER = null;
  document.getElementById("pauto").textContent = "Tự chạy"; } }

document.getElementById("pstep").addEventListener("click", pStep);
document.getElementById("prst").addEventListener("click", pReset);
["pmode","ptake"].forEach(id => document.getElementById(id).addEventListener("change", pReset));
document.getElementById("pauto").addEventListener("click", () => {
  if(PTIMER) return pStop();
  if(PDONE) pReset();
  document.getElementById("pauto").textContent = "Dừng";
  PTIMER = setInterval(() => { pStep(); if(PDONE) pStop(); }, 420);
});
pReset();
})();
