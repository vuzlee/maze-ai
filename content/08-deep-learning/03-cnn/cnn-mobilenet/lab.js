(function(){
/* ---------------- lab: shape & cost ---------------- */
function cCalc(){
  const H = Math.max(1, +document.getElementById("cH").value || 1);
  const Ci = Math.max(1, +document.getElementById("cCi").value || 1);
  const Co = Math.max(1, +document.getElementById("cCo").value || 1);
  const k = Math.max(1, +document.getElementById("cK").value || 1);
  const s = Math.max(1, +document.getElementById("cS").value || 1);
  const p = Math.max(0, +document.getElementById("cP").value || 0);

  const Ho = Math.floor((H + 2*p - k)/s) + 1;
  if(Ho < 1){
    document.getElementById("cview3").innerHTML =
      `<p class="legend"><span style="color:var(--tomb)">kernel larger than input — no valid output</span></p>`;
    return;
  }
  const stdP = k*k*Ci*Co + Co;
  const stdM = Ho*Ho*k*k*Ci*Co;
  const dwP = k*k*Ci + Ci;
  const pwP = Ci*Co + Co;
  const dsP = dwP + pwP;
  const dsM = Ho*Ho*k*k*Ci + Ho*Ho*Ci*Co;
  const ratioP = stdP/dsP, ratioM = stdM/dsM;
  const limit = 1/(1/Co + 1/(k*k));

  const F = n => n >= 1e9 ? (n/1e9).toFixed(2)+" G" : n >= 1e6 ? (n/1e6).toFixed(2)+" M"
             : n >= 1e3 ? (n/1e3).toFixed(1)+" K" : String(n);
  document.getElementById("cview3").innerHTML =
    `<table>
      <tr><th>Item</th><th>Standard conv</th><th>Depthwise separable</th><th>Ratio</th></tr>
      <tr><td>output shape</td>
          <td colspan="2" style="font-family:var(--mono);text-align:center">${Ho} × ${Ho} × ${Co}
            <span style="color:var(--muted);font-size:11.5px"> ← ⌊(${H}+2·${p}−${k})/${s}⌋+1</span></td>
          <td>—</td></tr>
      <tr><td>parameters</td>
          <td style="font-family:var(--mono)">${F(stdP)}</td>
          <td style="font-family:var(--mono);color:var(--ok)">${F(dsP)}</td>
          <td style="color:var(--probe);font-family:var(--mono)">${ratioP.toFixed(1)}×</td></tr>
      <tr><td>multiply-accumulates (MAC)</td>
          <td style="font-family:var(--mono)">${F(stdM)}</td>
          <td style="font-family:var(--mono);color:var(--ok)">${F(dsM)}</td>
          <td style="color:var(--probe);font-family:var(--mono)">${ratioM.toFixed(1)}×</td></tr>
      <tr><td>depthwise separable breakdown</td>
          <td colspan="3" style="font-size:12.5px;color:var(--muted);font-family:var(--mono)">
            depthwise ${F(dwP)} params + pointwise 1×1 ${F(pwP)} params</td></tr>
      <tr><td>theoretical limit</td>
          <td colspan="3" style="font-size:12.5px;color:var(--muted)">
            1 / (1/C_out + 1/k²) = 1 / (1/${Co} + 1/${k*k}) =
            <b style="color:var(--probe)">${limit.toFixed(2)}×</b> — approaches k² = ${k*k} as C_out grows</td></tr>
    </table>`;
}
["cH","cCi","cCo","cK","cS","cP"].forEach(id =>
  document.getElementById(id).addEventListener("input", cCalc));
cCalc();
})();
