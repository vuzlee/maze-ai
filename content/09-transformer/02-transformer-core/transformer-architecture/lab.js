(function(){
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
  const attn = v.L * (2*v.d*v.d + 2*v.d*(v.KH*dHead));   /* W_q, W_o full size; W_k, W_v scale with kv heads */
  const ffn  = v.L * 2 * v.d * v.F;
  const emb  = v.V * v.d;
  const tot  = attn + ffn + emb;
  const kvPerTok = 2 * v.L * v.KH * dHead * B;
  const kvSeq = kvPerTok * v.S;
  const flops = 2 * v.S * v.S * v.d * v.L;              /* only the Q·K and weights·V part */

  el("out").innerHTML = `
  <table>
    <tr><th>Item</th><th>Value</th><th>Note</th></tr>
    <tr><td>Attention (all layers)</td><td>${fmt(attn)}</td><td>W_q, W_o full size; W_k, W_v shrink with the number of kv heads</td></tr>
    <tr><td>FFN (all layers)</td><td>${fmt(ffn)}</td><td>${(100*ffn/tot).toFixed(0)}% of all parameters</td></tr>
    <tr><td>Embedding</td><td>${fmt(emb)}</td><td>${(100*emb/tot).toFixed(0)}% — a large share in small models</td></tr>
    <tr><td><strong>Total parameters</strong></td><td><strong>${fmt(tot)}</strong></td><td>weights take ${bytes(tot*B)} at ${B} bytes per value</td></tr>
    <tr><td>KV cache / token</td><td>${bytes(kvPerTok)}</td><td>2 × ${v.L} layers × ${v.KH} kv heads × ${dHead} dims × ${B} bytes</td></tr>
    <tr><td>KV cache at ${v.S} tokens</td><td>${bytes(kvSeq)}</td><td>for <em>one</em> request; multiply by the number of concurrent requests</td></tr>
    <tr><td>Attention FLOPs</td><td>${fmt(flops)}</td><td>Q·K and weights·V only, grows with the square of length</td></tr>
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
