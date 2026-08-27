(function(){
/* ---------------- lab: chiến lược triển khai ---------------- */
const DSTRAT = {
  shadow:    {pct: 0,   label: "shadow",            note: "model mới nhận lưu lượng nhưng KHÔNG trả kết quả cho người dùng"},
  canary:    {pct: null, label: "canary",           note: "chỉ một phần nhỏ người dùng bị ảnh hưởng; tăng dần khi guardrail sạch"},
  bluegreen: {pct: 100, label: "blue-green",        note: "chuyển toàn bộ một lần; quay lại rất nhanh nhưng bán kính rủi ro là 100%"},
  all:       {pct: 100, label: "triển khai thẳng",  note: "không có lớp bảo vệ nào"}
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
        ${Math.round(a).toLocaleString("vi-VN")}</td>
      <td style="font-size:12.5px;color:var(--muted)">${c.note}</td></tr>`;
  }).join("");

  const col = userVisible === 0 ? "var(--ok)" : (userVisible > 100000 ? "var(--tomb)" : "var(--probe)");
  document.getElementById("depview").innerHTML =
    `<div class="note" style="border-left-color:${col};margin:0 0 14px">
       <h4 style="color:${col}">bán kính rủi ro</h4>
       <p style="margin:0;font-family:var(--mono);font-size:13px">
         ${qps.toLocaleString("vi-VN")} QPS × ${minutes} phút × ${pct}% lưu lượng × ${err}% lỗi
         = <b style="font-size:15px">${Math.round(userVisible).toLocaleString("vi-VN")}</b> request bị lỗi
         ${userVisible === 0 ? " — người dùng KHÔNG thấy gì" : ""}</p>
     </div>
     <table><tr><th>Chiến lược</th><th>lưu lượng</th><th>request bị ảnh hưởng</th><th>đặc điểm</th></tr>${rows}</table>
     <p style="font-size:12.5px;color:var(--muted);margin-top:10px">
       Thời gian phơi nhiễm = ${det} phút phát hiện + ${rb} phút quay lại = <b>${minutes} phút</b>.
       Giảm thời gian phát hiện có giá trị tương đương với giảm tỉ lệ lưu lượng — cả hai đều nhân trực tiếp vào bán kính rủi ro.</p>`;
}
["dstrat","dqps","dpct","ddet","drb","derr"].forEach(id => {
  document.getElementById(id).addEventListener("input", dCalc);
  document.getElementById(id).addEventListener("change", dCalc);
});
dCalc();
})();
