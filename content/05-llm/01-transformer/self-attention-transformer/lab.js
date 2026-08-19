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

/* ---------------- lab 2: param & memory calculator ---------------- */
const PRESETS = {
  gpt2s:  {d:768,  L:12, H:12, KH:12, F:3072,  V:50257, S:1024},
  llama7: {d:4096, L:32, H:32, KH:32, F:11008, V:32000, S:4096},
  llama70:{d:8192, L:80, H:64, KH:8,  F:28672, V:32000, S:4096}
};
const fields = ["d","L","H","KH","F","V","S"];
function fmt(n){
  if(n >= 1e9) return (n/1e9).toFixed(2)+" B";
  if(n >= 1e6) return (n/1e6).toFixed(1)+" M";
  if(n >= 1e3) return (n/1e3).toFixed(1)+" K";
  return n.toFixed(0);
}
function bytes(n){
  if(n >= 1024**3) return (n/1024**3).toFixed(2)+" GB";
  if(n >= 1024**2) return (n/1024**2).toFixed(1)+" MB";
  if(n >= 1024)    return (n/1024).toFixed(1)+" KB";
  return n.toFixed(0)+" B";
}
function calc(){
  const v = {}; fields.forEach(f => v[f] = Math.max(1,+el(f).value||1));
  const B = +el("B").value;
  const dHead = v.d / v.H;
  const attn = v.L * (2*v.d*v.d + 2*v.d*(v.KH*dHead));   /* W_q, W_o đủ chiều; W_k, W_v theo số kv head */
  const ffn  = v.L * 2 * v.d * v.F;
  const emb  = v.V * v.d;
  const tot  = attn + ffn + emb;
  const kvPerTok = 2 * v.L * v.KH * dHead * B;
  const kvSeq = kvPerTok * v.S;
  const flops = 2 * v.S * v.S * v.d * v.L;              /* riêng phần Q·K và weights·V */

  el("out").innerHTML = `
  <table>
    <tr><th>Hạng mục</th><th>Giá trị</th><th>Ghi chú</th></tr>
    <tr><td>Attention (mọi lớp)</td><td>${fmt(attn)}</td><td>W_q, W_o đủ chiều; W_k, W_v thu nhỏ theo số kv head</td></tr>
    <tr><td>FFN (mọi lớp)</td><td>${fmt(ffn)}</td><td>${(100*ffn/tot).toFixed(0)}% tổng tham số</td></tr>
    <tr><td>Embedding</td><td>${fmt(emb)}</td><td>${(100*emb/tot).toFixed(0)}% — chiếm tỉ trọng lớn ở model nhỏ</td></tr>
    <tr><td><strong>Tổng tham số</strong></td><td><strong>${fmt(tot)}</strong></td><td>trọng số chiếm ${bytes(tot*B)} ở ${B} byte mỗi giá trị</td></tr>
    <tr><td>KV cache / token</td><td>${bytes(kvPerTok)}</td><td>2 × ${v.L} lớp × ${v.KH} kv head × ${dHead} chiều × ${B} byte</td></tr>
    <tr><td>KV cache ở ${v.S} token</td><td>${bytes(kvSeq)}</td><td>cho <em>một</em> request; nhân lên theo số request đồng thời</td></tr>
    <tr><td>FLOPs của attention</td><td>${fmt(flops)}</td><td>riêng Q·K và weights·V, tăng theo bình phương độ dài</td></tr>
  </table>`;
}
el("preset").addEventListener("change",()=>{
  const p = PRESETS[el("preset").value];
  if(p){ fields.forEach(f => el(f).value = p[f]); }
  calc();
});
fields.forEach(f => el(f).addEventListener("input",()=>{ el("preset").value="custom"; calc(); }));
el("B").addEventListener("change",calc);
calc();
})();
