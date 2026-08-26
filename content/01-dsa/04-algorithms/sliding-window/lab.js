(function(){
/* ---------------- lab: sliding window step-through ---------------- */
let S = "abcabcbb", L = 0, R = -1, best = 0, steps = 0, last = {}, timer = null, done = false;

function render(note){
  const cells = [...S].map((ch, i) => {
    const inWin = i >= L && i <= R;
    const bg = inWin ? "var(--filled)" : "var(--raise)";
    const fg = inWin ? "#14110E" : "var(--muted)";
    const mark = i === L ? "L" : (i === R ? "R" : "");
    return `<div class="slot" style="border-color:${inWin?'var(--filled)':'var(--rule)'}">
              <i>${mark || i}</i>
              <u style="background:${bg};color:${fg};font-weight:${inWin?600:400}">${ch}</u>
            </div>`;
  }).join("");
  document.getElementById("view").innerHTML =
    `<div class="rail" style="grid-template-columns:repeat(${Math.min(S.length,16)},minmax(0,1fr))">${cells}</div>`;
  document.getElementById("cur").textContent = R < L ? "rỗng" : S.slice(L, R+1) + ` (${R-L+1})`;
  document.getElementById("best").textContent = best;
  document.getElementById("steps").textContent = steps;
  if(note){
    const log = document.getElementById("log");
    log.insertAdjacentHTML("afterbegin",
      `<div><span>R=${R}</span><span>${note}</span><span>max ${best}</span></div>`);
    while(log.children.length > 8) log.removeChild(log.lastChild);
  }
}
function step(){
  if(done) return;
  R++;
  if(R >= S.length){ done = true; stopAuto(); render("xong — kết quả " + best); return; }
  steps++;
  const ch = S[R];
  let note;
  if(last[ch] !== undefined && last[ch] >= L){
    const old = L; L = last[ch] + 1;
    note = `'${ch}' đã có ở ${last[ch]} → L nhảy ${old}→${L}`;
  } else {
    note = `thêm '${ch}' — cửa sổ vẫn hợp lệ`;
  }
  last[ch] = R;
  best = Math.max(best, R - L + 1);
  render(note);
}
function reset(){
  stopAuto();
  S = (document.getElementById("str").value || "abcabcbb").slice(0, 16);
  L = 0; R = -1; best = 0; steps = 0; last = {}; done = false;
  document.getElementById("log").innerHTML = "";
  render(null);
}
function stopAuto(){ if(timer){ clearInterval(timer); timer = null;
  document.getElementById("auto").textContent = "Tự chạy"; } }

document.getElementById("step").addEventListener("click", step);
document.getElementById("rst").addEventListener("click", reset);
document.getElementById("str").addEventListener("change", reset);
document.getElementById("auto").addEventListener("click", () => {
  if(timer) return stopAuto();
  if(done) reset();
  document.getElementById("auto").textContent = "Dừng";
  timer = setInterval(() => { step(); if(done) stopAuto(); }, 650);
});
reset();
})();
