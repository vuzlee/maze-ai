(function(){
/* ---------------- lab: ngân sách RTT ---------------- */
const NVER = {
  h11_12: {label: "HTTP/1.1 + TLS 1.2", tcp: 1, tls: 2, mux: false},
  h11_13: {label: "HTTP/1.1 + TLS 1.3", tcp: 1, tls: 1, mux: false},
  h2:     {label: "HTTP/2 + TLS 1.3",   tcp: 1, tls: 1, mux: true},
  h3:     {label: "HTTP/3 (QUIC)",      tcp: 0, tls: 1, mux: true}   /* QUIC gộp transport + TLS */
};
function nCalc4(){
  const rtt = Math.max(1, +document.getElementById("nrtt").value || 80);
  const v = NVER[document.getElementById("nver").value];
  const dnsCached = document.getElementById("ndns").checked;
  const reuse = document.getElementById("nreuse").checked;
  const proc = Math.max(0, +document.getElementById("nproc").value || 0);
  const seq = Math.max(1, +document.getElementById("nseq").value || 1);

  const dns = dnsCached ? 0 : 1;
  const setup = reuse ? 0 : (v.tcp + v.tls);
  const firstRtt = dns + setup + 1;
  const firstMs = firstRtt * rtt + proc;

  /* request tiếp theo: nếu tái dùng thì chỉ 1 RTT; nếu không, bắt tay lại */
  const nextRtt = reuse ? 1 : (v.tcp + v.tls + 1);
  const totalMs = firstMs + (seq - 1) * (nextRtt * rtt + proc);

  const parts = [
    ["DNS", dns, dnsCached ? "đã cache" : "phân giải tên miền"],
    [v.tcp ? "TCP bắt tay" : "QUIC bắt tay", reuse ? 0 : v.tcp, reuse ? "tái dùng kết nối" : "ba bước"],
    ["TLS bắt tay", reuse ? 0 : v.tls, reuse ? "tái dùng kết nối" : (v.tls === 1 ? "TLS 1.3 hoặc QUIC" : "TLS 1.2")],
    ["request đầu tiên", 1, "gửi và nhận"]
  ];
  const bars = parts.map(([n, r, note]) => {
    const ms = r * rtt;
    const w = Math.max(0, 100 * ms / Math.max(firstMs, 1));
    const col = r === 0 ? "var(--rule)" : "var(--filled)";
    return `<div style="display:flex;align-items:center;gap:10px;margin-bottom:5px">
      <span style="width:120px;font-size:12px;color:var(--muted);text-align:right">${n}</span>
      <div style="flex:1;background:var(--bg);border-radius:3px;height:14px">
        <div style="height:14px;width:${w}%;background:${col};border-radius:3px"></div></div>
      <span style="width:78px;font-family:var(--mono);font-size:11.5px">${r} RTT · ${ms} ms</span>
      <span style="width:150px;font-size:11px;color:var(--muted)">${note}</span></div>`;
  }).join("");

  document.getElementById("nview4").innerHTML =
    `<p class="legend" style="margin:2px 0 8px"><span>${v.label} · RTT ${rtt} ms${v.mux ? " · ghép luồng" : ""}</span></p>
     ${bars}
     <div style="display:flex;align-items:center;gap:10px;margin-top:4px;padding-top:8px;border-top:1px solid var(--rule)">
       <span style="width:120px;font-size:12px;color:var(--muted);text-align:right">server xử lý</span>
       <div style="flex:1"></div>
       <span style="width:78px;font-family:var(--mono);font-size:11.5px">${proc} ms</span>
       <span style="width:150px"></span></div>
     <table style="margin-top:14px">
       <tr><th>Hạng mục</th><th>Giá trị</th><th>Ghi chú</th></tr>
       <tr><td>RTT trước byte đầu tiên</td>
           <td style="font-family:var(--mono);color:var(--probe)">${firstRtt}</td>
           <td style="font-size:12.5px;color:var(--muted)">${reuse ? "chỉ còn chính request" : "cộng cả bắt tay"}</td></tr>
       <tr><td><strong>request đầu tiên</strong></td>
           <td style="font-family:var(--mono);font-size:15px;color:var(--probe)">${firstMs} ms</td>
           <td style="font-size:12.5px;color:var(--muted)">${firstRtt} × ${rtt} + ${proc} xử lý</td></tr>
       <tr><td>mỗi request sau đó</td>
           <td style="font-family:var(--mono)">${nextRtt * rtt + proc} ms</td>
           <td style="font-size:12.5px;color:var(--muted)">${nextRtt} RTT${reuse ? "" : " — phải bắt tay lại!"}</td></tr>
       <tr><td><strong>tổng cho ${seq} request nối tiếp</strong></td>
           <td style="font-family:var(--mono);font-size:15px;color:${totalMs > 1000 ? 'var(--tomb)' : 'var(--ok)'}">
             ${totalMs >= 1000 ? (totalMs/1000).toFixed(2) + " s" : totalMs + " ms"}</td>
           <td style="font-size:12.5px;color:var(--muted)">
             ${v.mux && seq > 1 ? "HTTP/2 và 3 có thể chạy SONG SONG — con số này là trường hợp nối tiếp" : ""}</td></tr>
     </table>`;
}
["nrtt","nver","ndns","nreuse","nproc","nseq"].forEach(id => {
  document.getElementById(id).addEventListener("input", nCalc4);
  document.getElementById(id).addEventListener("change", nCalc4);
});
nCalc4();
})();
