(function(){
/* ---------------- lab: KV cache ---------------- */
function iCalc(){
  const L = Math.max(1, +document.getElementById("iL").value || 32);
  const hd = Math.max(8, +document.getElementById("ihd").value || 128);
  const nq = Math.max(1, +document.getElementById("inq").value || 32);
  const att = document.getElementById("iatt").value;
  const seq = Math.max(128, +document.getElementById("iseq").value || 8192);
  const bs = Math.max(1, +document.getElementById("ibs").value || 1);
  const dt = +document.getElementById("idt").value;
  const vram = Math.max(1, +document.getElementById("ivram").value || 64);

  const nkv = att === "mha" ? nq : (att === "gqa" ? Math.max(1, Math.round(nq/4)) : 1);
  const perToken = 2 * L * nkv * hd * dt;              /* bytes per token */
  const perReq = perToken * seq;
  const totalB = perReq * bs;
  const vramB = vram * 1024**3;
  const maxReq = Math.floor(vramB / perReq);
  const fits = totalB <= vramB;

  /* compare the three attention types */
  const cmp = [["MHA", nq], ["GQA", Math.max(1, Math.round(nq/4))], ["MQA", 1]].map(([n, k]) => {
    const pt = 2 * L * k * hd * dt;
    return {n, k, pt, req: pt*seq, max: Math.floor(vramB/(pt*seq))};
  });
  const K = b => b >= 1024**3 ? (b/1024**3).toFixed(2)+" GB"
              : b >= 1024**2 ? (b/1024**2).toFixed(1)+" MB" : (b/1024).toFixed(0)+" KB";

  document.getElementById("iview").innerHTML =
    `<table>
      <tr><th>Item</th><th>Value</th><th>Formula</th></tr>
      <tr><td>KV heads</td><td style="font-family:var(--mono)">${nkv}</td>
          <td style="font-size:12.5px;color:var(--muted)">${att === "mha" ? "= Q heads" : att === "gqa" ? "= Q heads / 4" : "= 1"}</td></tr>
      <tr><td>cache per token</td><td style="font-family:var(--mono)">${K(perToken)}</td>
          <td style="font-size:12.5px;color:var(--muted)">2 × ${L} × ${nkv} × ${hd} × ${dt} bytes</td></tr>
      <tr><td>cache per request</td><td style="font-family:var(--mono);color:var(--probe)">${K(perReq)}</td>
          <td style="font-size:12.5px;color:var(--muted)">× ${seq.toLocaleString("en-US")} tokens of context</td></tr>
      <tr><td><strong>total for batch ${bs}</strong></td>
          <td style="font-family:var(--mono);font-size:15px;color:${fits?'var(--ok)':'var(--tomb)'}">${K(totalB)}</td>
          <td style="font-size:12.5px;color:${fits?'var(--muted)':'var(--tomb)'}">
            ${fits ? `fits in ${vram} GB` : `EXCEEDS ${vram} GB — out of VRAM`}</td></tr>
      <tr><td><strong>max concurrent requests</strong></td>
          <td style="font-family:var(--mono);font-size:15px;color:var(--probe)">${maxReq.toLocaleString("en-US")}</td>
          <td style="font-size:12.5px;color:var(--muted)">${vram} GB / cache per request</td></tr>
     </table>
     <p class="legend" style="margin:16px 0 6px"><span>three attention types compared, rest of the config unchanged</span></p>
     <table><tr><th>Type</th><th>head KV</th><th>cache / token</th><th>cache / request</th><th>max concurrent requests</th></tr>
     ${cmp.map(c => `<tr>
        <td style="font-family:var(--mono);font-size:12.5px;color:${c.n.toLowerCase()===att?'var(--probe)':'var(--muted)'}">
          ${c.n}${c.n.toLowerCase()===att?" ←":""}</td>
        <td style="font-family:var(--mono);font-size:12px">${c.k}</td>
        <td style="font-family:var(--mono);font-size:12px">${K(c.pt)}</td>
        <td style="font-family:var(--mono);font-size:12px">${K(c.req)}</td>
        <td style="font-family:var(--mono);font-size:12px;color:var(--ok)">${c.max.toLocaleString("en-US")}</td></tr>`).join("")}
     </table>`;
}
["iL","ihd","inq","iatt","iseq","ibs","idt","ivram"].forEach(id => {
  document.getElementById(id).addEventListener("input", iCalc);
  document.getElementById(id).addEventListener("change", iCalc);
});
iCalc();
})();
