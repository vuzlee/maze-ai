(function(){
/* ---------------- lab: window function ---------------- */
const EMP = [
  {name: "An",   dept: "eng",   salary: 6000},
  {name: "Bình", dept: "eng",   salary: 5000},
  {name: "Cường",dept: "eng",   salary: 5000},
  {name: "Dung", dept: "eng",   salary: 4000},
  {name: "Giang",dept: "sales", salary: 4500},
  {name: "Hà",   dept: "sales", salary: 4500},
  {name: "Khoa", dept: "sales", salary: 3000}
];
const WLABEL = {
  row_number: "ROW_NUMBER()", rank: "RANK()", dense_rank: "DENSE_RANK()",
  sum: "SUM(salary)", avg: "AVG(salary)", lag: "LAG(salary)",
  pct: "100 * salary / SUM(salary)"
};
function wCalc(){
  const fn = document.getElementById("wfn").value;
  const part = document.getElementById("wpart").checked;
  const ord = document.getElementById("word").value;

  const orderSql = ord === "name" ? "name" : (ord === "salary_asc" ? "salary ASC" : "salary DESC");
  const needOrder = ["row_number","rank","dense_rank","sum","lag"].includes(fn);
  const over = (part ? "PARTITION BY dept" : "") +
               (needOrder ? (part ? " " : "") + "ORDER BY " + orderSql : "");
  document.getElementById("wsql").textContent =
    `SELECT name, dept, salary,\n       ${WLABEL[fn]} OVER (${over}) AS result\nFROM employees;`;

  /* chia nhóm */
  const groups = {};
  EMP.forEach(e => {
    const k = part ? e.dept : "_all";
    (groups[k] = groups[k] || []).push({...e});
  });
  /* sắp trong nhóm */
  Object.values(groups).forEach(g => g.sort((a,b) =>
    ord === "name" ? a.name.localeCompare(b.name, "vi")
    : ord === "salary_asc" ? a.salary - b.salary : b.salary - a.salary));

  const out = [];
  Object.entries(groups).forEach(([k, g]) => {
    const total = g.reduce((s, e) => s + e.salary, 0);
    let run = 0;
    g.forEach((e, i) => {
      let v;
      if(fn === "row_number") v = i + 1;
      else if(fn === "rank"){
        v = 1 + g.filter(o => (ord === "salary_asc" ? o.salary < e.salary : o.salary > e.salary)).length;
        if(ord === "name") v = i + 1;
      }
      else if(fn === "dense_rank"){
        const vals = [...new Set(g.map(o => ord === "name" ? o.name : o.salary))];
        v = vals.indexOf(ord === "name" ? e.name : e.salary) + 1;
      }
      else if(fn === "sum"){ run += e.salary; v = run.toLocaleString("vi-VN"); }
      else if(fn === "avg") v = Math.round(total / g.length).toLocaleString("vi-VN");
      else if(fn === "lag") v = i === 0 ? "NULL" : g[i-1].salary.toLocaleString("vi-VN");
      else v = (100 * e.salary / total).toFixed(1) + "%";
      out.push({...e, group: k, result: v, first: i === 0});
    });
  });

  let h = `<div class="hm"><table><tr><th>name</th><th>dept</th><th>salary</th>
    <th style="color:var(--probe)">result</th></tr>`;
  out.forEach(r => {
    const sep = r.first && part ? "border-top:2px solid var(--rule)" : "";
    h += `<tr style="${sep}">
      <td class="rl" style="text-align:left;color:var(--text)">${r.name}</td>
      <td style="font-family:var(--mono);font-size:11.5px;color:var(--muted)">${r.dept}</td>
      <td style="font-family:var(--mono);font-size:11.5px">${r.salary.toLocaleString("vi-VN")}</td>
      <td><div class="cell" style="background:var(--probe);color:#14110E">${r.result}</div></td></tr>`;
  });
  document.getElementById("wview").innerHTML = h + `</table></div>`;
}
["wfn","wpart","word"].forEach(id =>
  document.getElementById(id).addEventListener("change", wCalc));
wCalc();
})();
