(function(){
/* ---------------- lab: bảng edit distance ---------------- */
let DA = "kitten", DB = "sitting", DT = [], DI = 1, DJ = 1, DDONE = false, DTIMER = null, DPICK = null;

function dInit(){
  DA = (document.getElementById("sa").value || "kitten").slice(0, 8);
  DB = (document.getElementById("sb").value || "sitting").slice(0, 8);
  document.getElementById("sa").value = DA;
  document.getElementById("sb").value = DB;
  const n = DA.length, m = DB.length;
  DT = Array.from({length: n+1}, () => new Array(m+1).fill(null));
  for(let i = 0; i <= n; i++) DT[i][0] = i;
  for(let j = 0; j <= m; j++) DT[0][j] = j;
  DI = 1; DJ = 1; DDONE = false; DPICK = null;
}
function dRender(){
  const n = DA.length, m = DB.length;
  let h = `<div class="hm"><table><tr><th></th><th>ε</th>` +
          [...DB].map(c => `<th>${c}</th>`).join("") + `</tr>`;
  for(let i = 0; i <= n; i++){
    h += `<tr><td class="rl">${i === 0 ? "ε" : DA[i-1]}</td>`;
    for(let j = 0; j <= m; j++){
      const v = DT[i][j];
      let bg = "var(--raise)", fg = "var(--muted)", bold = 400;
      if(v !== null){ bg = "var(--panel)"; fg = "var(--text)"; }
      if(i === 0 || j === 0){ bg = "#111922"; fg = "var(--muted)"; }
      const isSrc = DPICK && DPICK.src.some(s => s[0] === i && s[1] === j);
      if(isSrc){ bg = "var(--filled)"; fg = "#0E141B"; bold = 600; }
      if(!DDONE && i === DI && j === DJ){ bg = "var(--probe)"; fg = "#0E141B"; bold = 600; }
      if(DDONE && i === n && j === m){ bg = "var(--ok)"; fg = "#0E141B"; bold = 600; }
      h += `<td><div class="cell" style="background:${bg};color:${fg};font-weight:${bold}">${v === null ? "·" : v}</div></td>`;
    }
    h += `</tr>`;
  }
  document.getElementById("dview").innerHTML = h + `</table></div>`;
  document.getElementById("dcell").textContent = DDONE ? "xong" : `(${DI}, ${DJ})`;
  document.getElementById("dop").textContent = DPICK ? DPICK.op : "–";
  document.getElementById("dres").textContent = DDONE ? DT[n][m] + " phép" : "đang chạy";
}
function dStep(){
  if(DDONE) return;
  const n = DA.length, m = DB.length;
  if(DA[DI-1] === DB[DJ-1]){
    DT[DI][DJ] = DT[DI-1][DJ-1];
    DPICK = {op: `'${DA[DI-1]}' khớp → lấy ô chéo, không cộng`, src: [[DI-1, DJ-1]]};
  } else {
    const del = DT[DI-1][DJ], ins = DT[DI][DJ-1], rep = DT[DI-1][DJ-1];
    const best = Math.min(del, ins, rep);
    DT[DI][DJ] = best + 1;
    const name = best === rep ? "thay" : (best === del ? "xoá" : "chèn");
    DPICK = {op: `'${DA[DI-1]}' ≠ '${DB[DJ-1]}' → ${name}, ${best} + 1`,
             src: [[DI-1,DJ],[DI,DJ-1],[DI-1,DJ-1]]};
  }
  DJ++;
  if(DJ > m){ DJ = 1; DI++; }
  if(DI > n){ DDONE = true; DPICK = null; }
  dRender();
}
function dReset(){ dStop(); dInit(); dRender(); }
function dStop(){ if(DTIMER){ clearInterval(DTIMER); DTIMER = null;
  document.getElementById("dauto").textContent = "Tự chạy"; } }

document.getElementById("dstep").addEventListener("click", dStep);
document.getElementById("drst").addEventListener("click", dReset);
["sa","sb"].forEach(id => document.getElementById(id).addEventListener("change", dReset));
document.getElementById("dauto").addEventListener("click", () => {
  if(DTIMER) return dStop();
  if(DDONE) dReset();
  document.getElementById("dauto").textContent = "Dừng";
  DTIMER = setInterval(() => { dStep(); if(DDONE) dStop(); }, 260);
});
dReset();
})();
