(function(){
/* ---------------- lab: converging ends (Two Sum II) step by step ---------------- */
let A = [2,3,5,8,11,15], T = 13;
let L = 0, R = 0, steps = 0, timer = null, done = false, hit = null;

function parseArr(raw){
  const xs = String(raw).split(/[,\s]+/).map(Number).filter(v => Number.isFinite(v));
  return (xs.length >= 2 ? xs : [2,3,5,8,11,15]).slice(0, 14).sort((a,b) => a - b);
}

function render(note){
  const cells = A.map((v, i) => {
    const out  = i < L || i > R;                       /* already ruled out for good */
    const isL  = i === L, isR = i === R;
    const win  = hit && (i === hit[0] || i === hit[1]);
    let bg = "var(--raise)", fg = "var(--muted)", bd = "var(--rule)";
    if (isL || isR){ bg = "var(--probe)"; fg = "var(--on-fill)"; bd = "var(--probe)"; }
    if (win){ bg = "var(--ok)"; fg = "var(--on-fill)"; bd = "var(--ok)"; }
    return `<div class="slot" style="border-color:${bd};opacity:${out ? .26 : 1}">
              <i>${isL && isR ? "LR" : isL ? "L" : isR ? "R" : i}</i>
              <u style="background:${bg};color:${fg};font-weight:${isL||isR||win ? 600 : 400}">${v}</u>
            </div>`;
  }).join("");
  document.getElementById("view").innerHTML =
    `<div class="rail" style="grid-template-columns:repeat(${A.length},minmax(0,1fr))">${cells}</div>`;

  const s = (L < R || hit) ? A[L] + A[R] : null;
  document.getElementById("cur").textContent  = hit ? `a[${hit[0]}] + a[${hit[1]}]` : (L < R ? `a[${L}] + a[${R}]` : "none");
  document.getElementById("sum").textContent  = s === null ? "–" : `${s} / ${T}`;
  document.getElementById("steps").textContent = steps;
  document.getElementById("brute").textContent = (A.length * (A.length - 1) / 2) + " pairs";

  if (note){
    const log = document.getElementById("log");
    log.insertAdjacentHTML("afterbegin",
      `<div><span>step ${steps}</span><span>L=${L} R=${R}</span><span>${note}</span></div>`);
    while (log.children.length > 8) log.removeChild(log.lastChild);
  }
}

function step(){
  if (done) return;
  if (L >= R){ done = true; stopAuto(); render("the ends met — no pair satisfies it"); return; }
  steps++;
  const s = A[L] + A[R];
  if (s === T){
    hit = [L, R]; done = true; stopAuto();
    render(`${A[L]} + ${A[R]} = ${T} → found`);
  } else if (s < T){
    const old = L; L++;
    render(`${s} < ${T} → need larger → drop ${A[old]}, L ${old}→${L}`);
    if (L >= R){ done = true; stopAuto(); render("the ends met — no pair satisfies it"); }
  } else {
    const old = R; R--;
    render(`${s} > ${T} → need smaller → drop ${A[old]}, R ${old}→${R}`);
    if (L >= R){ done = true; stopAuto(); render("the ends met — no pair satisfies it"); }
  }
}

function reset(){
  stopAuto();
  A = parseArr(document.getElementById("arr").value);
  document.getElementById("arr").value = A.join(", ");   /* show that it has been sorted */
  const t = Number(document.getElementById("tgt").value);
  T = Number.isFinite(t) ? t : 13;
  L = 0; R = A.length - 1; steps = 0; hit = null; done = false;
  document.getElementById("log").innerHTML = "";
  render(null);
}
function stopAuto(){
  if (timer){ clearInterval(timer); timer = null;
    document.getElementById("auto").textContent = "Auto run"; }
}

document.getElementById("step").addEventListener("click", step);
document.getElementById("rst").addEventListener("click", reset);
document.getElementById("arr").addEventListener("change", reset);
document.getElementById("tgt").addEventListener("change", reset);
document.getElementById("auto").addEventListener("click", () => {
  if (timer) return stopAuto();
  if (done) reset();
  document.getElementById("auto").textContent = "Stop";
  timer = setInterval(() => { step(); if (done) stopAuto(); }, 700);
});
reset();
})();
