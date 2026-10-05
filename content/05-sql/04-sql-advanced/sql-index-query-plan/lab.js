(function(){
/* ---------------- lab: điểm giao nhau index vs seq scan ---------------- */
function qCalc(){
  const rows = Math.max(100, +document.getElementById("qrows").value || 100);
  const selPct = Math.min(100, Math.max(0.001, +document.getElementById("qsel").value || 0.1));
  const ppp = Math.max(1, +document.getElementById("qppp").value || 100);
  const rnd = Math.max(1, +document.getElementById("qrnd").value || 4);

  const pages = Math.ceil(rows / ppp);
  const matched = Math.max(1, Math.round(rows * selPct / 100));

  /* seq scan: đọc mọi trang, tuần tự (chi phí 1 mỗi trang) */
  const seqCost = pages;
  /* index scan: ~3 trang index, rồi mỗi dòng khớp là một lần đọc ngẫu nhiên
     (chặn trên bởi số trang của bảng — không đọc quá cả bảng) */
  const idxPages = Math.min(matched, pages);
  const idxCost = 3 + idxPages * rnd;
  /* index only scan: không chạm bảng */
  const onlyCost = 3 + Math.ceil(matched / (ppp * 4));

  /* điểm giao: matched * rnd = pages  →  selectivity = pages / (rnd * rows) */
  const crossPct = Math.min(100, 100 * pages / (rnd * rows));

  const rowsOut = [
    ["Seq Scan", seqCost, `đọc ${pages.toLocaleString("vi-VN")} trang tuần tự`, "var(--muted)"],
    ["Index Scan", idxCost, `3 trang index + ${idxPages.toLocaleString("vi-VN")} lần đọc ngẫu nhiên × ${rnd}`, "var(--filled)"],
    ["Index Only Scan", onlyCost, "không chạm bảng — cần index bao phủ", "var(--ok)"]
  ];
  const worst = Math.max(...rowsOut.map(r => r[1]));
  const best = Math.min(...rowsOut.map(r => r[1]));

  let h = `<table><tr><th>Phương án</th><th>Chi phí ước lượng (trang)</th><th>Chi tiết</th></tr>`;
  rowsOut.forEach(([name, c, d, col]) => {
    const w = Math.max(2, Math.round(100 * c / worst));
    h += `<tr>
      <td style="color:${col};font-family:var(--mono);font-size:12.5px">${name}${c === best ? " ★" : ""}</td>
      <td><div style="display:flex;align-items:center;gap:8px">
        <div style="height:9px;width:${w}%;background:${col};border-radius:2px;min-width:3px"></div>
        <span style="font-family:var(--mono);font-size:12px">${Math.round(c).toLocaleString("vi-VN")}</span>
      </div></td>
      <td style="font-size:12.5px;color:var(--muted)">${d}</td></tr>`;
  });
  h += `</table>
    <p style="font-family:var(--mono);font-size:12.5px;margin-top:12px;color:var(--text)">
      dòng khớp: <b style="color:var(--probe)">${matched.toLocaleString("vi-VN")}</b> / ${rows.toLocaleString("vi-VN")}
      &nbsp;·&nbsp; điểm giao nhau ở khoảng
      <b style="color:var(--probe)">${crossPct < 0.01 ? crossPct.toExponential(1) : crossPct.toFixed(2)}%</b>
      — vượt mức này thì planner nên chọn Seq Scan
    </p>`;
  document.getElementById("qview").innerHTML = h;
}
["qrows","qsel","qppp","qrnd"].forEach(id =>
  document.getElementById(id).addEventListener("input", qCalc));
qCalc();
})();
