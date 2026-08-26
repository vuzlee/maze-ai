(function(){
/* ---------------- lab 1: attention heatmap ---------------- */
const TOK = ["Con","mèo","đen","đang","ngủ","."];
/* điểm số cơ sở ở d_k = 8, đặt tay để có ngữ nghĩa hợp lý */
const BASE = [
 [ 1.8,  0.3, -0.2,  0.1, -0.4, -0.9],
 [ 1.2,  1.9,  0.8, -0.1,  0.4, -0.8],
 [ 0.2,  1.6,  1.4, -0.3,  0.1, -0.7],
 [-0.1,  0.5, -0.2,  1.5,  0.9, -0.6],
 [ 0.3,  1.7,  0.6,  1.1,  1.6, -0.5],
 [ 0.1,  0.9,  0.2,  0.4,  1.3,  1.0]
];
const el = id => document.getElementById(id);

function softmax(row){
  const m = Math.max(...row.filter(v=>isFinite(v)));
  const ex = row.map(v => isFinite(v) ? Math.exp(v-m) : 0);
  const s = ex.reduce((a,b)=>a+b,0);
  return ex.map(v=>v/s);
}
function color(w){
  const t = Math.min(1, Math.pow(w,0.6));
  const r = Math.round(29+(108-29)*t), g = Math.round(40+(140-40)*t), b = Math.round(54+(255-54)*t);
  return `rgb(${r},${g},${b})`;
}
function drawAttn(){
  const dk = +el("dk").value, temp = Math.max(0.1,+el("temp").value||1);
  const scaled = el("scale").checked, causal = el("causal").checked;
  const grow = Math.sqrt(dk/8);                 /* tích vô hướng lớn dần theo căn d_k */
  const div = scaled ? Math.sqrt(dk) : 1;
  const norm = Math.sqrt(8);                    /* giữ mức tham chiếu dễ đọc ở d_k = 8 */

  let rows=[], sds=[], ents=[], mx=0;
  for(let i=0;i<6;i++){
    const raw = BASE[i].map(v => v*grow);
    sds.push(Math.sqrt(raw.reduce((a,b)=>a+b*b,0)/6));
    const sc = raw.map((v,j)=> (causal && j>i) ? -Infinity : v/div*norm/temp);
    const w = softmax(sc);
    let e=0; w.forEach(p=>{ if(p>1e-9) e -= p*Math.log2(p); });
    ents.push(e); mx = Math.max(mx, ...w);
    rows.push({w, masked: sc.map(v=>!isFinite(v))});
  }
  let h = "<table><tr><th></th>" + TOK.map(t=>`<th>${t}</th>`).join("") + "</tr>";
  rows.forEach((r,i)=>{
    h += `<tr><td class="rl">${TOK[i]}</td>` + r.w.map((w,j)=>{
      if(r.masked[j]) return `<td><div class="cell mask">·</div></td>`;
      return `<td><div class="cell" style="background:${color(w)}">${w.toFixed(2)}</div></td>`;
    }).join("") + "</tr>";
  });
  el("hm").innerHTML = h + "</table>";
  el("sd").textContent  = (sds.reduce((a,b)=>a+b,0)/6).toFixed(2);
  el("ent").textContent = (ents.reduce((a,b)=>a+b,0)/6).toFixed(2) + " bit";
  el("mx").textContent  = mx.toFixed(2);
}
["dk","temp","scale","causal"].forEach(id=>{
  el(id).addEventListener("input",drawAttn);
  el(id).addEventListener("change",drawAttn);
});
el("reset").addEventListener("click",()=>{
  el("dk").value="64"; el("temp").value="1"; el("scale").checked=true; el("causal").checked=true; drawAttn();
});
drawAttn();
})();
