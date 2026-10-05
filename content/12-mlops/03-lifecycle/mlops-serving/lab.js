(function(){
/* ---------------- lab: deployment strategies ---------------- */
const DSTRAT = {
  shadow:    {pct: 0,   label: "shadow",            note: "new model receives traffic but does NOT return results to users"},
  canary:    {pct: null, label: "canary",           note: "only a small share of users is affected; ramp up while guardrails stay clean"},
  bluegreen: {pct: 100, label: "blue-green",        note: "switch everything at once; very fast rollback but blast radius is 100%"},
  all:       {pct: 100, label: "direct rollout",    note: "no protection layer at all"}
};
function dCalc(){
  const st = document.getElementById("dstrat").value;
  const qps = Math.max(1, +document.getElementById("dqps").value || 1);
  let pct = Math.min(100, Math.max(0, +document.getElementById("dpct").value || 0));
  const det = Math.max(1, +document.getElementById("ddet").value || 1);
  const rb = Math.max(0, +document.getElementById("drb").value || 0);
  const err = Math.min(100, Math.max(0, +document.getElementById("derr").value || 0));

  const cfg = DSTRAT[st];
  if(cfg.pct !== null) pct = cfg.pct;
  document.getElementById("dpct").value = pct;
  document.getElementById("dpct").disabled = cfg.pct !== null;

  const minutes = det + rb;
  const affectedReq = qps * 60 * minutes * (pct/100) * (err/100);
  const userVisible = st === "shadow" ? 0 : affectedReq;

  const rows = Object.entries(DSTRAT).map(([k, c]) => {
    const p = c.pct === null ? pct : c.pct;
    const a = k === "shadow" ? 0 : qps * 60 * minutes * (p/100) * (err/100);
    const cur = k === st;
    return `<tr>
      <td style="font-family:var(--mono);font-size:12.5px;color:${cur?'var(--probe)':'var(--muted)'}">
        ${c.label}${cur?" ←":""}</td>
      <td style="font-family:var(--mono);font-size:12px">${p}%</td>
      <td style="font-family:var(--mono);font-size:12px;color:${a===0?'var(--ok)':(a>100000?'var(--tomb)':'var(--text)')}">
        ${Math.round(a).toLocaleString("en-US")}</td>
      <td style="font-size:12.5px;color:var(--muted)">${c.note}</td></tr>`;
  }).join("");

  const col = userVisible === 0 ? "var(--ok)" : (userVisible > 100000 ? "var(--tomb)" : "var(--probe)");
  document.getElementById("depview").innerHTML =
    `<div class="note" style="border-left-color:${col};margin:0 0 14px">
       <h4 style="color:${col}">blast radius</h4>
       <p style="margin:0;font-family:var(--mono);font-size:13px">
         ${qps.toLocaleString("en-US")} QPS × ${minutes} min × ${pct}% traffic × ${err}% errors
         = <b style="font-size:15px">${Math.round(userVisible).toLocaleString("en-US")}</b> failed requests
         ${userVisible === 0 ? " — users see NOTHING" : ""}</p>
     </div>
     <table><tr><th>Strategy</th><th>traffic</th><th>affected requests</th><th>notes</th></tr>${rows}</table>
     <p style="font-size:12.5px;color:var(--muted);margin-top:10px">
       Exposure time = ${det} min to detect + ${rb} min to roll back = <b>${minutes} min</b>.
       Cutting detection time is worth as much as cutting the traffic share — both multiply directly into the blast radius.</p>`;
}
["dstrat","dqps","dpct","ddet","drb","derr"].forEach(id => {
  document.getElementById(id).addEventListener("input", dCalc);
  document.getElementById(id).addEventListener("change", dCalc);
});
dCalc();
})();
