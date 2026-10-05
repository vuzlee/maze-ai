(function(){
/* ---------------- lab: chunk & retrieval ---------------- */
const DOC = "Sales policy in effect from January 2026. Customers buying in store or on the website get exactly the same terms under this policy. The warranty period for all premium-line products is 24 months from the invoice date. Products in the standard line have a 12-month warranty period. Exchanges within the first 7 days are free of charge if the product's seal is still intact. After 7 days, the exchange fee is 200k per exchange. The store also offers installments via credit card with 6-month and 12-month terms, at 0 percent interest for the 6-month term.";
const RQS = [
  {q: "How long is the warranty period?", gold: "The warranty period for all premium-line products is 24 months from the invoice date."},
  {q: "How much is the exchange fee?", gold: "After 7 days, the exchange fee is 200k per exchange."},
  {q: "Are installments available?", gold: "The store also offers installments via credit card with 6-month and 12-month terms, at 0 percent interest for the 6-month term."}
];
function rTok(s){
  return s.toLowerCase().replace(/[.,?]/g, " ").split(/\s+/).filter(w => w.length > 1);
}
function rCalc(){
  const size = Math.max(40, +document.getElementById("rsize").value || 180);
  const ovPct = Math.max(0, Math.min(50, +document.getElementById("rov").value || 0));
  const k = Math.max(1, +document.getElementById("rk").value || 2);
  const qi = +document.getElementById("rq").value;
  const {q, gold} = RQS[qi];

  const step = Math.max(20, Math.round(size * (1 - ovPct/100)));
  const chunks = [];
  for(let i = 0; i < DOC.length; i += step){
    chunks.push({text: DOC.slice(i, i + size), start: i});
    if(i + size >= DOC.length) break;
  }
  /* score = keyword overlap, standing in for a real embedding */
  const qt = new Set(rTok(q));
  chunks.forEach(c => {
    const ct = rTok(c.text);
    let hit = 0;
    ct.forEach(w => { if(qt.has(w)) hit++; });
    c.score = hit / Math.sqrt(ct.length || 1);
    c.hasGold = c.text.includes(gold);
  });
  const ranked = [...chunks].sort((a,b) => b.score - a.score);
  const top = ranked.slice(0, k);
  const goldExists = chunks.some(c => c.hasGold);
  const goldRetrieved = top.some(c => c.hasGold);

  const verdict = !goldExists
    ? ["the answer sentence is CUT IN TWO — no chunk holds all of it. The system is bound to be wrong.", "var(--tomb)"]
    : (goldRetrieved
       ? ["the chunk holding the answer is in the top-k — retrieval succeeded.", "var(--ok)"]
       : ["the chunk holding the answer exists but was NOT retrieved. Raise k, or add a reranker.", "var(--probe)"]);

  const list = chunks.map((c, i) => {
    const inTop = top.includes(c);
    const border = c.hasGold ? "var(--ok)" : (inTop ? "var(--probe)" : "var(--rule)");
    return `<div style="border:1px solid ${border};border-left-width:3px;border-radius:5px;
      padding:8px 11px;margin-bottom:6px;background:${inTop?'var(--panel)':'transparent'}">
      <div style="font-family:var(--mono);font-size:10.5px;color:var(--muted);margin-bottom:3px">
        chunk ${i+1} · ${c.text.length} chars · score ${c.score.toFixed(3)}
        ${inTop ? '<span style="color:var(--probe)"> · RETRIEVED</span>' : ''}
        ${c.hasGold ? '<span style="color:var(--ok)"> · HOLDS THE FULL ANSWER</span>' : ''}
      </div>
      <div style="font-size:12.5px;color:${inTop?'var(--text)':'var(--muted)'}">${c.text}</div></div>`;
  }).join("");

  document.getElementById("rview").innerHTML =
    `<div class="note" style="border-left-color:${verdict[1]};margin:0 0 14px">
       <h4 style="color:${verdict[1]}">result</h4>
       <p style="margin:0 0 6px;font-size:13.5px">question: <b>${q}</b></p>
       <p style="margin:0 0 6px;font-size:13.5px">answer sentence: <span style="color:var(--ok)">${gold}</span></p>
       ${verdict[0]}</div>
     <p class="legend" style="margin:0 0 8px"><span>${chunks.length} chunk · stride ${step} chars · overlap ${ovPct}%</span></p>
     ${list}`;
}
["rsize","rov","rk","rq"].forEach(id => {
  document.getElementById(id).addEventListener("input", rCalc);
  document.getElementById(id).addEventListener("change", rCalc);
});
rCalc();
})();
