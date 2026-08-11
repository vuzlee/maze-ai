(function(){
/* ---------------- lab: chunk & truy xuất ---------------- */
const DOC = "Chính sách bán hàng áp dụng từ tháng 1 năm 2026. Khách hàng mua sản phẩm tại cửa hàng hoặc trên website đều được hưởng chính sách như nhau. Thời hạn bảo hành cho toàn bộ sản phẩm thuộc dòng cao cấp là 24 tháng kể từ ngày xuất hoá đơn. Sản phẩm thuộc dòng phổ thông có thời hạn bảo hành 12 tháng. Phí đổi hàng trong 7 ngày đầu là 0 đồng nếu sản phẩm còn nguyên tem. Sau 7 ngày, phí đổi hàng là 200 nghìn đồng cho mỗi lần đổi. Cửa hàng có hỗ trợ trả góp qua thẻ tín dụng với kỳ hạn 6 tháng và 12 tháng, lãi suất 0 phần trăm cho kỳ hạn 6 tháng.";
const RQS = [
  {q: "Thời hạn bảo hành là bao lâu?", gold: "Thời hạn bảo hành cho toàn bộ sản phẩm thuộc dòng cao cấp là 24 tháng kể từ ngày xuất hoá đơn."},
  {q: "Phí đổi hàng bao nhiêu?", gold: "Sau 7 ngày, phí đổi hàng là 200 nghìn đồng cho mỗi lần đổi."},
  {q: "Có hỗ trợ trả góp không?", gold: "Cửa hàng có hỗ trợ trả góp qua thẻ tín dụng với kỳ hạn 6 tháng và 12 tháng, lãi suất 0 phần trăm cho kỳ hạn 6 tháng."}
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
  /* điểm = độ trùng từ khoá, thay cho embedding thật */
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
    ? ["câu chứa đáp án BỊ CẮT ĐÔI — không chunk nào chứa đủ. Hệ thống chắc chắn sai.", "var(--tomb)"]
    : (goldRetrieved
       ? ["đoạn chứa đáp án nằm trong top-k — truy xuất thành công.", "var(--ok)"]
       : ["đoạn chứa đáp án tồn tại nhưng KHÔNG được lấy về. Tăng k, hoặc thêm reranker.", "var(--probe)"]);

  const list = chunks.map((c, i) => {
    const inTop = top.includes(c);
    const border = c.hasGold ? "var(--ok)" : (inTop ? "var(--probe)" : "var(--rule)");
    return `<div style="border:1px solid ${border};border-left-width:3px;border-radius:5px;
      padding:8px 11px;margin-bottom:6px;background:${inTop?'var(--panel)':'transparent'}">
      <div style="font-family:var(--mono);font-size:10.5px;color:var(--muted);margin-bottom:3px">
        chunk ${i+1} · ${c.text.length} ký tự · điểm ${c.score.toFixed(3)}
        ${inTop ? '<span style="color:var(--probe)"> · ĐƯỢC LẤY VỀ</span>' : ''}
        ${c.hasGold ? '<span style="color:var(--ok)"> · CHỨA ĐỦ CÂU ĐÁP ÁN</span>' : ''}
      </div>
      <div style="font-size:12.5px;color:${inTop?'var(--text)':'var(--muted)'}">${c.text}</div></div>`;
  }).join("");

  document.getElementById("rview").innerHTML =
    `<div class="note" style="border-left-color:${verdict[1]};margin:0 0 14px">
       <h4 style="color:${verdict[1]}">kết quả</h4>
       <p style="margin:0 0 6px;font-size:13.5px">câu hỏi: <b>${q}</b></p>
       <p style="margin:0 0 6px;font-size:13.5px">câu chứa đáp án: <span style="color:var(--ok)">${gold}</span></p>
       ${verdict[0]}</div>
     <p class="legend" style="margin:0 0 8px"><span>${chunks.length} chunk · bước nhảy ${step} ký tự · overlap ${ovPct}%</span></p>
     ${list}`;
}
["rsize","rov","rk","rq"].forEach(id => {
  document.getElementById(id).addEventListener("input", rCalc);
  document.getElementById(id).addEventListener("change", rCalc);
});
rCalc();
})();
