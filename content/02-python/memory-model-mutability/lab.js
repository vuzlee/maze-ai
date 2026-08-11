(function(){
/* ---------------- lab: theo dõi tham chiếu ---------------- */
const MSCEN = {
  assign: [
    {code: "a = [1, 2]",     names: {a: "o1"}, objs: {o1: "[1, 2]"},                       note: "tạo list, tên a trỏ tới nó"},
    {code: "b = a",          names: {a: "o1", b: "o1"}, objs: {o1: "[1, 2]"},              note: "KHÔNG sao chép — b là tên thứ hai của cùng object"},
    {code: "b.append(3)",    names: {a: "o1", b: "o1"}, objs: {o1: "[1, 2, 3]"},           note: "sửa object → cả a và b đều thấy"},
    {code: "b = [9]",        names: {a: "o1", b: "o2"}, objs: {o1: "[1, 2, 3]", o2: "[9]"}, note: "gán lại TÊN b → a không đổi"}
  ],
  copy: [
    {code: "a = [[1], [2]]", names: {a: "o1"}, objs: {o1: "[ →o2, →o3 ]", o2: "[1]", o3: "[2]"}, note: "list ngoài chứa hai tham chiếu"},
    {code: "b = a[:]",       names: {a: "o1", b: "o4"}, objs: {o1: "[ →o2, →o3 ]", o4: "[ →o2, →o3 ]", o2: "[1]", o3: "[2]"}, note: "shallow: o4 mới, nhưng CHỈ TỚI CÙNG o2, o3"},
    {code: "b[0].append(99)",names: {a: "o1", b: "o4"}, objs: {o1: "[ →o2, →o3 ]", o4: "[ →o2, →o3 ]", o2: "[1, 99]", o3: "[2]"}, note: "sửa o2 → a cũng thấy! Đây là bẫy shallow copy"},
    {code: "c = deepcopy(a)",names: {a: "o1", b: "o4", c: "o5"}, objs: {o1: "[ →o2, →o3 ]", o4: "[ →o2, →o3 ]", o5: "[ →o6, →o7 ]", o2: "[1, 99]", o3: "[2]", o6: "[1, 99]", o7: "[2]"}, note: "deep: sao chép đệ quy, o5 không dùng chung gì"}
  ],
  func: [
    {code: "a = [1, 2, 3]",       names: {a: "o1"}, objs: {o1: "[1, 2, 3]"}, note: "trước khi gọi hàm"},
    {code: "f1(a)  # lst.append(4)", names: {a: "o1", "lst (trong f1)": "o1"}, objs: {o1: "[1, 2, 3, 4]"}, note: "lst là tên mới trên CÙNG object → sửa thì a thấy"},
    {code: "f2(a)  # lst = [9, 9]",  names: {a: "o1", "lst (trong f2)": "o2"}, objs: {o1: "[1, 2, 3, 4]", o2: "[9, 9]"}, note: "gán lại tên cục bộ → a không hề bị ảnh hưởng"},
    {code: "# sau khi f2 trả về",  names: {a: "o1"}, objs: {o1: "[1, 2, 3, 4]"}, note: "o2 mất tham chiếu cuối → được giải phóng ngay"}
  ],
  mul: [
    {code: "row = [0] * 3",           names: {row: "o1"}, objs: {o1: "[0, 0, 0]"}, note: "một dòng bình thường"},
    {code: "grid = [row] * 3",        names: {row: "o1", grid: "o2"}, objs: {o2: "[ →o1, →o1, →o1 ]", o1: "[0, 0, 0]"}, note: "BA tham chiếu tới CÙNG một dòng"},
    {code: "grid[0][0] = 1",          names: {row: "o1", grid: "o2"}, objs: {o2: "[ →o1, →o1, →o1 ]", o1: "[1, 0, 0]"}, note: "sửa o1 → cả ba dòng cùng đổi"},
    {code: "grid = [[0]*3 for _ in range(3)]", names: {grid: "o3"}, objs: {o3: "[ →o4, →o5, →o6 ]", o4: "[0, 0, 0]", o5: "[0, 0, 0]", o6: "[0, 0, 0]"}, note: "comprehension: ba list riêng biệt — cách đúng"}
  ]
};
const OCOL = {o1: "var(--filled)", o2: "var(--ok)", o3: "var(--probe)", o4: "var(--tomb)",
              o5: "#9B7BD4", o6: "#4FA8C7", o7: "#C79A4F"};
let MSTEP = 0, MTIMER2 = null;

function mRender2(){
  const scen = MSCEN[document.getElementById("mscen").value];
  const st = scen[MSTEP];
  const names = Object.entries(st.names).map(([n, o]) =>
    `<div class="slot" style="min-width:auto;border-color:${OCOL[o]||'var(--rule)'}">
       <i>${n}</i><u style="color:${OCOL[o]||'var(--text)'};font-weight:600;padding:6px 10px">→ ${o}</u></div>`).join("");
  const objs = Object.entries(st.objs).map(([o, v]) =>
    `<div class="slot" style="min-width:auto;border-color:${OCOL[o]||'var(--rule)'}">
       <i style="color:${OCOL[o]||'var(--muted)'}">${o}</i>
       <u style="font-weight:600;padding:6px 10px">${v}</u></div>`).join("");
  document.getElementById("mview2").innerHTML =
    `<pre style="margin:0 0 14px">${scen.map((s, i) =>
        (i === MSTEP ? '<span class="kw">▸ ' + s.code + '</span>' : (i < MSTEP ? s.code : '<span class="cm">' + s.code + '</span>'))).join("\n")}</pre>
     <p class="legend" style="margin:0 0 6px"><span>tên → object</span></p>
     <div style="display:flex;gap:6px;flex-wrap:wrap">${names}</div>
     <p class="legend" style="margin:14px 0 6px"><span>object trong bộ nhớ</span></p>
     <div style="display:flex;gap:6px;flex-wrap:wrap">${objs}</div>`;
  const log = document.getElementById("mlog2");
  log.insertAdjacentHTML("afterbegin", `<div><span>dòng ${MSTEP+1}</span><span>${st.note}</span><span></span></div>`);
  while(log.children.length > 6) log.removeChild(log.lastChild);
}
function mStep2(){
  const scen = MSCEN[document.getElementById("mscen").value];
  if(MSTEP < scen.length - 1){ MSTEP++; mRender2(); }
  else mStop2();
}
function mReset2(){ mStop2(); MSTEP = 0;
  document.getElementById("mlog2").innerHTML = ""; mRender2(); }
function mStop2(){ if(MTIMER2){ clearInterval(MTIMER2); MTIMER2 = null;
  document.getElementById("mauto2").textContent = "Tự chạy"; } }

document.getElementById("mstep2").addEventListener("click", mStep2);
document.getElementById("mrst2").addEventListener("click", mReset2);
document.getElementById("mscen").addEventListener("change", mReset2);
document.getElementById("mauto2").addEventListener("click", () => {
  if(MTIMER2) return mStop2();
  const scen = MSCEN[document.getElementById("mscen").value];
  if(MSTEP >= scen.length - 1) mReset2();
  document.getElementById("mauto2").textContent = "Dừng";
  MTIMER2 = setInterval(mStep2, 1500);
});
mReset2();
})();
