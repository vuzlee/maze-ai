(function(){
/* ---------------- lab: bốn mô hình đồng thời ---------------- */
const SCEN = {
  io:  {n: 20, cpu: 5,   io: 300, cores: 4},
  cpu: {n: 8,  cpu: 500, io: 0,   cores: 4},
  mix: {n: 12, cpu: 120, io: 250, cores: 4}
};
function cCalc(){
  const n = Math.max(1, +document.getElementById("ntask").value || 1);
  const cpu = Math.max(0, +document.getElementById("cpums").value || 0);
  const io = Math.max(0, +document.getElementById("iows").value || 0);
  const cores = Math.max(1, +document.getElementById("cores").value || 1);

  const seq = n * (cpu + io);
  /* thread: bytecode tuần tự hoá vì GIL, phần chờ chồng lấn */
  const thr = Math.max(n * cpu, cpu + io) + n * 0.05;
  /* async: như thread nhưng chi phí mỗi task nhỏ hơn nhiều */
  const asy = Math.max(n * cpu, cpu + io) + n * 0.005;
  /* process: phần tính chia cho số lõi, cộng chi phí khởi tạo */
  const spawn = 40;
  const pro = Math.max(Math.ceil(n / cores) * cpu, cpu + io) + Math.min(n, cores) * spawn;

  const rows = [
    ["tuần tự",        seq, "n × (tính + chờ)", "var(--muted)"],
    ["threading",      thr, "max(n × tính, tính + chờ) + chi phí luồng", "var(--filled)"],
    ["asyncio",        asy, "max(n × tính, tính + chờ) + chi phí task", "var(--ok)"],
    ["multiprocessing", pro, "max(⌈n/lõi⌉ × tính, tính + chờ) + khởi tạo", "var(--probe)"]
  ];
  const worst = Math.max(...rows.map(r => r[1]));
  const best = Math.min(...rows.map(r => r[1]));

  let h = `<table><tr><th>Mô hình</th><th>Thời gian ước lượng</th><th>So với tuần tự</th><th>Công thức</th></tr>`;
  rows.forEach(([name, t, f, col]) => {
    const w = Math.max(2, Math.round(100 * t / worst));
    const speed = (seq / t).toFixed(1);
    h += `<tr>
      <td style="color:${col};font-family:var(--mono);font-size:12.5px">${name}${t === best ? " ★" : ""}</td>
      <td><div style="display:flex;align-items:center;gap:8px">
        <div style="height:9px;width:${w}%;background:${col};border-radius:2px;min-width:3px"></div>
        <span style="font-family:var(--mono);font-size:12px">${t < 1000 ? Math.round(t) + " ms" : (t/1000).toFixed(2) + " s"}</span>
      </div></td>
      <td style="font-family:var(--mono);font-size:12px">${speed}×</td>
      <td style="font-size:12.5px;color:var(--muted)">${f}</td></tr>`;
  });
  document.getElementById("cview").innerHTML = h + `</table>`;
}
["ntask","cpums","iows","cores"].forEach(id =>
  document.getElementById(id).addEventListener("input", cCalc));
document.getElementById("scen").addEventListener("change", e => {
  const s = SCEN[e.target.value];
  if(s){
    document.getElementById("ntask").value = s.n;
    document.getElementById("cpums").value = s.cpu;
    document.getElementById("iows").value = s.io;
    document.getElementById("cores").value = s.cores;
  }
  cCalc();
});
cCalc();
})();
