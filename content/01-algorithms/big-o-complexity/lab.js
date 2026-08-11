(function(){
/* ---------------- lab: ngưỡng n ---------------- */
const CLASSES = [
  ["O(1)",        n => 1],
  ["O(log n)",    n => Math.log2(Math.max(n,2))],
  ["O(n)",        n => n],
  ["O(n log n)",  n => n * Math.log2(Math.max(n,2))],
  ["O(n²)",       n => n * n],
  ["O(n³)",       n => n * n * n],
  ["O(2ⁿ)",       n => n > 90 ? Infinity : Math.pow(2, n)],
  ["O(n!)",       n => { if(n > 20) return Infinity; let r = 1; for(let i = 2; i <= n; i++) r *= i; return r; }]
];
function human(x){
  if(!isFinite(x)) return "vô cùng lớn";
  if(x < 1e4) return Math.round(x).toLocaleString("vi-VN");
  const e = Math.floor(Math.log10(x));
  return (x / Math.pow(10, e)).toFixed(1) + " × 10^" + e;
}
function dur(sec){
  if(!isFinite(sec)) return "không bao giờ xong";
  if(sec < 1e-6) return "< 1 µs";
  if(sec < 1e-3) return (sec*1e6).toFixed(0) + " µs";
  if(sec < 1)    return (sec*1e3).toFixed(0) + " ms";
  if(sec < 60)   return sec.toFixed(1) + " giây";
  if(sec < 3600) return (sec/60).toFixed(1) + " phút";
  if(sec < 86400)return (sec/3600).toFixed(1) + " giờ";
  if(sec < 3.15e9) return (sec/86400).toFixed(0) + " ngày";
  return human(sec/3.15e7) + " năm";
}
function verdict(sec){
  if(sec < 0.01) return ["tức thì", "var(--ok)"];
  if(sec < 1)    return ["thoải mái", "var(--ok)"];
  if(sec < 10)   return ["sát ngưỡng", "var(--probe)"];
  return ["vô vọng", "var(--tomb)"];
}
function drawBig(){
  const n = Math.max(1, +document.getElementById("n").value || 1);
  const ops = +document.getElementById("ops").value;
  let h = "<table><tr><th>Độ phức tạp</th><th>Số phép tính</th><th>Thời gian</th><th>Kết luận</th></tr>";
  CLASSES.forEach(([name, f]) => {
    const c = f(n), sec = c / ops, [v, col] = verdict(sec);
    h += `<tr><td><code>${name}</code></td><td>${human(c)}</td><td>${dur(sec)}</td>
          <td style="color:${col};font-family:var(--mono);font-size:12px">${v}</td></tr>`;
  });
  document.getElementById("bigout").innerHTML = h + "</table>";
}
["n","ops"].forEach(id => document.getElementById(id).addEventListener("input", drawBig));
document.getElementById("ops").addEventListener("change", drawBig);
document.getElementById("quick").addEventListener("change", e => {
  if(e.target.value){ document.getElementById("n").value = e.target.value; drawBig(); }
});
drawBig();
})();
