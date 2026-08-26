(function(){
/* ---------------- lab: cỡ mẫu & power ---------------- */
/* CDF chuẩn qua xấp xỉ erf (Abramowitz & Stegun 7.1.26) */
function erf(x){
  const s = x < 0 ? -1 : 1; x = Math.abs(x);
  const t = 1/(1 + 0.3275911*x);
  const y = 1 - (((((1.061405429*t - 1.453152027)*t) + 1.421413741)*t - 0.284496736)*t + 0.254829592)*t*Math.exp(-x*x);
  return s*y;
}
const Phi = z => 0.5*(1 + erf(z/Math.SQRT2));
function zOf(p){                             /* nghịch đảo bằng chia đôi */
  let lo = -8, hi = 8;
  for(let i = 0; i < 80; i++){ const m = (lo+hi)/2; if(Phi(m) < p) lo = m; else hi = m; }
  return (lo+hi)/2;
}
function pCalc(){
  const p1 = Math.min(0.9, Math.max(0.001, (+document.getElementById("pbase").value || 5)/100));
  const rel = Math.max(0.01, (+document.getElementById("plift").value || 10)/100);
  const alpha = +document.getElementById("palpha").value;
  const power = +document.getElementById("ppower").value;
  const traffic = Math.max(10, +document.getElementById("ptraffic").value || 20000);

  const p2 = Math.min(0.999, p1 * (1 + rel));
  const delta = p2 - p1;
  const za = zOf(1 - alpha/2), zb = zOf(power);
  const n = Math.ceil(Math.pow(za + zb, 2) * (p1*(1-p1) + p2*(1-p2)) / (delta*delta));
  const total = 2*n;
  const days = total / traffic;

  /* MDE phát hiện được nếu chỉ chạy 7 và 14 ngày */
  const mdeFor = d => {
    const nn = Math.max(1, d * traffic / 2);
    const se = Math.sqrt(2 * p1 * (1 - p1) / nn);
    const dd = (za + zb) * se;
    return 100 * dd / p1;
  };
  const R = v => Math.round(v).toLocaleString("vi-VN");
  document.getElementById("pview3").innerHTML =
    `<table>
      <tr><th>Đại lượng</th><th>Giá trị</th><th>Ghi chú</th></tr>
      <tr><td>tỉ lệ nền → mục tiêu</td><td style="font-family:var(--mono)">${(100*p1).toFixed(2)}% → ${(100*p2).toFixed(2)}%</td>
          <td style="font-size:13px;color:var(--muted)">tăng tuyệt đối ${(100*delta).toFixed(3)} điểm %</td></tr>
      <tr><td><strong>cỡ mẫu mỗi nhóm</strong></td>
          <td style="color:var(--probe);font-family:var(--mono);font-size:15px">${R(n)}</td>
          <td style="font-size:13px;color:var(--muted)">tổng ${R(total)} người dùng</td></tr>
      <tr><td><strong>thời gian chạy</strong></td>
          <td style="color:var(--probe);font-family:var(--mono);font-size:15px">${days < 1 ? "&lt; 1" : days.toFixed(1)} ngày</td>
          <td style="font-size:13px;color:var(--muted)">${days > 28 ? "quá dài — cân nhắc lại MDE hoặc metric" : (days < 7 ? "vẫn nên chạy đủ 7 ngày để phủ chu kỳ tuần" : "hợp lý")}</td></tr>
      <tr><td>nếu chỉ chạy 7 ngày</td><td style="font-family:var(--mono)">phát hiện được ≥ ${mdeFor(7).toFixed(1)}%</td>
          <td style="font-size:13px;color:var(--muted)">mức tăng tương đối nhỏ nhất</td></tr>
      <tr><td>nếu chạy 14 ngày</td><td style="font-family:var(--mono)">phát hiện được ≥ ${mdeFor(14).toFixed(1)}%</td>
          <td style="font-size:13px;color:var(--muted)">gấp đôi thời gian chỉ cải thiện √2 lần</td></tr>
      <tr><td>z dùng trong công thức</td><td style="font-family:var(--mono)">z<sub>α/2</sub>=${za.toFixed(3)} · z<sub>β</sub>=${zb.toFixed(3)}</td>
          <td style="font-size:13px;color:var(--muted)">alpha ${alpha} · power ${power}</td></tr>
    </table>`;
}
["pbase","plift","palpha","ppower","ptraffic"].forEach(id => {
  document.getElementById(id).addEventListener("input", pCalc);
  document.getElementById(id).addEventListener("change", pCalc);
});
pCalc();
})();
