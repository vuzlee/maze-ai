(function(){
/* ---------------- lab: hai đầu chụm (Two Sum II) từng bước ---------------- */
let A = [2,3,5,8,11,15], T = 13;
let L = 0, R = 0, steps = 0, timer = null, done = false, hit = null;

function parseArr(raw){
  const xs = String(raw).split(/[,\s]+/).map(Number).filter(v => Number.isFinite(v));
  return (xs.length >= 2 ? xs : [2,3,5,8,11,15]).slice(0, 14).sort((a,b) => a - b);
}

function render(note){
  const cells = A.map((v, i) => {
    const out  = i < L || i > R;                       /* đã bị loại hẳn */
    const isL  = i === L, isR = i === R;
    const win  = hit && (i === hit[0] || i === hit[1]);
    let bg = "var(--raise)", fg = "var(--muted)", bd = "var(--rule)";
    if (isL || isR){ bg = "var(--probe)"; fg = "#14110E"; bd = "var(--probe)"; }
    if (win){ bg = "var(--ok)"; fg = "#14110E"; bd = "var(--ok)"; }
    return `<div class="slot" style="border-color:${bd};opacity:${out ? .26 : 1}">
              <i>${isL && isR ? "LR" : isL ? "L" : isR ? "R" : i}</i>
              <u style="background:${bg};color:${fg};font-weight:${isL||isR||win ? 600 : 400}">${v}</u>
            </div>`;
  }).join("");
  document.getElementById("view").innerHTML =
    `<div class="rail" style="grid-template-columns:repeat(${A.length},minmax(0,1fr))">${cells}</div>`;

  const s = (L < R || hit) ? A[L] + A[R] : null;
  document.getElementById("cur").textContent  = hit ? `a[${hit[0]}] + a[${hit[1]}]` : (L < R ? `a[${L}] + a[${R}]` : "hết");
  document.getElementById("sum").textContent  = s === null ? "–" : `${s} / ${T}`;
  document.getElementById("steps").textContent = steps;
  document.getElementById("brute").textContent = (A.length * (A.length - 1) / 2) + " cặp";

  if (note){
    const log = document.getElementById("log");
    log.insertAdjacentHTML("afterbegin",
      `<div><span>bước ${steps}</span><span>L=${L} R=${R}</span><span>${note}</span></div>`);
    while (log.children.length > 8) log.removeChild(log.lastChild);
  }
}

function step(){
  if (done) return;
  if (L >= R){ done = true; stopAuto(); render("hai đầu gặp nhau — không có cặp nào thoả"); return; }
  steps++;
  const s = A[L] + A[R];
  if (s === T){
    hit = [L, R]; done = true; stopAuto();
    render(`${A[L]} + ${A[R]} = ${T} → tìm thấy`);
  } else if (s < T){
    const old = L; L++;
    render(`${s} < ${T} → cần lớn hơn → bỏ ${A[old]}, L ${old}→${L}`);
    if (L >= R){ done = true; stopAuto(); render("hai đầu gặp nhau — không có cặp nào thoả"); }
  } else {
    const old = R; R--;
    render(`${s} > ${T} → cần nhỏ hơn → bỏ ${A[old]}, R ${old}→${R}`);
    if (L >= R){ done = true; stopAuto(); render("hai đầu gặp nhau — không có cặp nào thoả"); }
  }
}

function reset(){
  stopAuto();
  A = parseArr(document.getElementById("arr").value);
  document.getElementById("arr").value = A.join(", ");   /* cho thấy nó đã được sắp xếp */
  const t = Number(document.getElementById("tgt").value);
  T = Number.isFinite(t) ? t : 13;
  L = 0; R = A.length - 1; steps = 0; hit = null; done = false;
  document.getElementById("log").innerHTML = "";
  render(null);
}
function stopAuto(){
  if (timer){ clearInterval(timer); timer = null;
    document.getElementById("auto").textContent = "Tự chạy"; }
}

document.getElementById("step").addEventListener("click", step);
document.getElementById("rst").addEventListener("click", reset);
document.getElementById("arr").addEventListener("change", reset);
document.getElementById("tgt").addEventListener("change", reset);
document.getElementById("auto").addEventListener("click", () => {
  if (timer) return stopAuto();
  if (done) reset();
  document.getElementById("auto").textContent = "Dừng";
  timer = setInterval(() => { step(); if (done) stopAuto(); }, 700);
});
reset();
})();
