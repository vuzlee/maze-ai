(function(){
/* ---------------- lab: activation qua các lớp ---------------- */
let LCG = 12345;
function rnd(){                                  /* sinh số giả ngẫu nhiên tất định */
  LCG = (LCG * 1103515245 + 12345) & 0x7fffffff;
  return LCG / 0x7fffffff;
}
function gauss(){                                /* Box-Muller */
  const u = Math.max(1e-9, rnd()), v = rnd();
  return Math.sqrt(-2*Math.log(u)) * Math.cos(2*Math.PI*v);
}
function nSim(){
  LCG = 12345;
  const scheme = document.getElementById("ninit").value;
  const act = document.getElementById("nact").value;
  const useNorm = document.getElementById("nnorm").checked;
  const W = Math.max(8, Math.min(512, +document.getElementById("nwidth").value || 128));
  const L = 20;

  let x = Array.from({length: W}, () => gauss());     /* đầu vào std = 1 */
  const stds = [];
  for(let l = 0; l < L; l++){
    let std;
    if(scheme === "tiny") std = 0.01;
    else if(scheme === "big") std = 0.5;
    else if(scheme === "xavier") std = Math.sqrt(1/W);
    else std = Math.sqrt(2/W);

    /* z_j = Σ_i w_ji x_i — tính bằng cách lấy mẫu ngẫu nhiên trọng số */
    const z = new Array(W).fill(0);
    for(let j = 0; j < W; j++){
      let s = 0;
      for(let i = 0; i < W; i++) s += gauss() * std * x[i];
      z[j] = s;
    }
    let a = act === "relu" ? z.map(v => Math.max(0, v))
          : act === "tanh" ? z.map(v => Math.tanh(v)) : z;
    if(useNorm){
      const m = a.reduce((s,v) => s+v, 0)/W;
      const sd = Math.sqrt(a.reduce((s,v) => s + (v-m)**2, 0)/W + 1e-5);
      a = a.map(v => (v-m)/sd);
    }
    const mm = a.reduce((s,v) => s+v, 0)/W;
    const sd2 = Math.sqrt(a.reduce((s,v) => s + (v-mm)**2, 0)/W);
    stds.push(sd2);
    x = a;
  }
  return stds;
}
function nRender3(){
  const stds = nSim();
  const mx = Math.max(...stds, 1e-9);
  const bars = stds.map((v, i) => {
    const h = Math.max(1, Math.round(70 * Math.min(1, v/mx)));
    const dead = v < 1e-3, blow = v > 20;
    const col = dead ? "var(--tomb)" : (blow ? "var(--probe)" : "var(--filled)");
    return `<div style="display:flex;flex-direction:column;justify-content:flex-end;align-items:center;width:24px">
      <div style="height:${h}px;width:13px;background:${col};border-radius:2px"></div>
      <span style="font-family:var(--mono);font-size:8.5px;color:var(--muted);margin-top:3px">${i+1}</span></div>`;
  }).join("");
  const first = stds[0], last = stds[stds.length-1];
  const ratio = last / (first || 1e-9);
  const verdict = last < 1e-3 ? ["tín hiệu TẮT — mạng không học được", "var(--tomb)"]
    : last > 20 ? ["tín hiệu NỔ — mất mát sẽ thành NaN", "var(--tomb)"]
    : (ratio > 0.3 && ratio < 3) ? ["ổn định — độ lớn giữ gần như phẳng", "var(--ok)"]
    : ["trôi dạt — còn học được nhưng không tối ưu", "var(--probe)"];
  document.getElementById("nview3").innerHTML =
    `<p class="legend" style="margin:2px 0 8px"><span>độ lệch chuẩn của activation ở từng lớp (1 → 20)</span></p>
     <div style="display:flex;gap:3px;align-items:flex-end;height:92px">${bars}</div>
     <div class="stat" style="margin-top:12px">
       <u>lớp 1 <b>${first.toExponential(2)}</b></u>
       <u>lớp 20 <b>${last.toExponential(2)}</b></u>
       <u>tỉ lệ cuối/đầu <b>${ratio.toExponential(2)}</b></u>
       <u>kết luận <b style="color:${verdict[1]}">${verdict[0]}</b></u>
     </div>`;
}
["ninit","nact","nnorm","nwidth"].forEach(id => {
  document.getElementById(id).addEventListener("input", nRender3);
  document.getElementById(id).addEventListener("change", nRender3);
});
nRender3();
})();
