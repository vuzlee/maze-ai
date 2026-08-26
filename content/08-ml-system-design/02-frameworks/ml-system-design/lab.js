(function(){
/* ---------------- lab: ngân sách hệ thống ---------------- */
function mCalc4(){
  const qps = Math.max(1, +document.getElementById("mqps").value || 1);
  const budget = Math.max(10, +document.getElementById("mbudget").value || 200);
  const feat = Math.max(0, +document.getElementById("mfeat").value || 0);
  const cand = Math.max(0, +document.getElementById("mcand").value || 0);
  const rank = Math.max(0, +document.getElementById("mrank").value || 0);
  const conc = Math.max(1, +document.getElementById("mconc").value || 1);
  const cost = Math.max(0, +document.getElementById("mcost").value || 0);
  const hit = Math.min(95, Math.max(0, +document.getElementById("mcache").value || 0)) / 100;

  const NET = 20, POST = 10;
  const used = NET + feat + cand + rank + POST;
  const slack = budget - used;
  const effQps = qps * (1 - hit);

  /* thông lượng mỗi máy = số request song song / thời gian xử lý (giây) */
  const procMs = feat + cand + rank + POST;
  const perNode = conc / (procMs / 1000);
  const nodes = Math.ceil(effQps / perNode * 1.3);          /* 30% dự trữ cho đỉnh */
  const monthly = nodes * cost * 24 * 30;

  const stages = [
    ["mạng &amp; load balancing", NET, "var(--rule)"],
    ["lấy đặc trưng", feat, "var(--filled)"],
    ["sinh ứng viên", cand, "var(--probe)"],
    ["xếp hạng", rank, "var(--tomb)"],
    ["sắp lại &amp; hậu xử lý", POST, "var(--rule)"],
    ["dự trữ còn lại", Math.max(0, slack), slack >= 0 ? "var(--ok)" : "var(--tomb)"]
  ];
  const bars = stages.map(([n, ms, col]) => {
    const w = Math.max(0.5, 100 * ms / budget);
    return `<div style="display:flex;align-items:center;gap:10px;margin-bottom:5px">
      <span style="width:150px;font-size:12px;color:var(--muted);text-align:right">${n}</span>
      <div style="flex:1;background:var(--bg);border-radius:3px;height:15px;position:relative">
        <div style="height:15px;width:${Math.min(100,w)}%;background:${col};border-radius:3px"></div>
      </div>
      <span style="width:52px;font-family:var(--mono);font-size:11.5px">${ms} ms</span></div>`;
  }).join("");

  const ok = slack >= 0;
  document.getElementById("mview4").innerHTML =
    `<p class="legend" style="margin:2px 0 8px"><span>ngân sách p99 = ${budget} ms</span></p>
     ${bars}
     <div class="note" style="border-left-color:${ok?'var(--ok)':'var(--tomb)'};margin:14px 0 0">
       <h4 style="color:${ok?'var(--ok)':'var(--tomb)'}">
         ${ok ? `vừa ngân sách — còn ${slack} ms dự trữ` : `VỠ ngân sách ${-slack} ms`}</h4>
       ${ok ? "Dự trữ nên chiếm khoảng 20% ngân sách để chịu đỉnh và đuôi p99."
            : "Cắt bớt: giảm số ứng viên vào tầng xếp hạng, dùng model nhẹ hơn, hoặc cache đặc trưng."}
     </div>
     <table style="margin-top:14px">
       <tr><th>Hạng mục</th><th>Giá trị</th><th>Cách tính</th></tr>
       <tr><td>QPS thực tới model</td><td style="font-family:var(--mono)">${Math.round(effQps).toLocaleString("vi-VN")}</td>
           <td style="font-size:12.5px;color:var(--muted)">${qps.toLocaleString("vi-VN")} × (1 − ${(100*hit).toFixed(0)}% cache hit)</td></tr>
       <tr><td>thông lượng mỗi máy</td><td style="font-family:var(--mono)">${perNode.toFixed(0)} req/s</td>
           <td style="font-size:12.5px;color:var(--muted)">${conc} song song / ${procMs} ms</td></tr>
       <tr><td><strong>số máy cần</strong></td>
           <td style="font-family:var(--mono);font-size:15px;color:var(--probe)">${nodes.toLocaleString("vi-VN")}</td>
           <td style="font-size:12.5px;color:var(--muted)">kèm 30% dự trữ cho đỉnh</td></tr>
       <tr><td><strong>chi phí mỗi tháng</strong></td>
           <td style="font-family:var(--mono);font-size:15px;color:var(--probe)">$${Math.round(monthly).toLocaleString("vi-VN")}</td>
           <td style="font-size:12.5px;color:var(--muted)">${nodes} máy × $${cost}/giờ × 720 giờ</td></tr>
     </table>`;
}
["mqps","mbudget","mfeat","mcand","mrank","mconc","mcost","mcache"].forEach(id =>
  document.getElementById(id).addEventListener("input", mCalc4));
mCalc4();
})();
