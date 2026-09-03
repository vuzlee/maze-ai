(function () {
/* ---------------- lab: sáu thuật toán sort trên cùng một mảng ----------------
   Mỗi cột là một phần tử có danh tính riêng: nó trượt sang chỗ mới chứ không
   biến mất rồi hiện lại, nên mắt theo được đúng cái đang bị di chuyển.        */

var el = function (id) { return document.getElementById(id); };

var DATA = {
  rand:   [7, 2, 9, 4, 12, 1, 6, 11, 3, 8, 5, 10],
  sorted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  rev:    [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
};
var SCEN = [["rand", "lộn xộn"], ["sorted", "đã sắp sẵn"], ["rev", "đảo ngược"]];
var SPEED = [["chậm", 620], ["vừa", 300], ["nhanh", 130]];

var ALGO = {
  bub: { name: "Bubble",    idea: "đổi chỗ hai cái kề nhau cho tới khi hết sai", mem: "O(1)",     run: rBubble },
  sel: { name: "Selection", idea: "mỗi vòng quét tìm cái nhỏ nhất, đem ra đầu",  mem: "O(1)",     run: rSelect },
  ins: { name: "Insertion", idea: "lấy từng cái, lùi về cắm vào đúng chỗ",       mem: "O(1)",     run: rInsert },
  mer: { name: "Merge",     idea: "trộn từng cặp đoạn đã sắp, đoạn dài dần lên", mem: "O(n)",     run: rMerge  },
  qui: { name: "Quick",     idea: "chọn chốt, dồn nhỏ sang trái lớn sang phải",  mem: "O(log n)", run: rQuick  },
  hea: { name: "Heap",      idea: "dựng heap rồi rút dần cái lớn nhất về cuối",  mem: "O(1)",     run: rHeap   }
};

/* ---------------- bộ sinh bước ----------------
   Phần tử là {v, id}: id không đổi suốt cả lượt chạy, nhờ đó khi vẽ biết
   cột nào vừa đi từ đâu tới đâu. Mỗi bước là một ảnh chụp thứ tự các id.   */

function Rec(vals) {
  var self = {
    a: vals.map(function (v, i) { return { v: v, id: i }; }),
    cmp: 0, swp: 0, done: {}, F: [],

    v: function (i) { return self.a[i].v; },

    snap: function (o) {
      o = o || {};
      self.F.push({
        ord:  self.a.map(function (x) { return x.id; }),
        hi:   o.hi   || [],
        lift: o.lift || [],
        pin:  o.pin === undefined ? -1 : o.pin,
        cold: o.cold || null,          /* [từ, tới) — phần ngoài cuộc lúc này */
        done: Object.keys(self.done).map(Number),
        cmp: self.cmp, swp: self.swp, ph: o.ph || ""
      });
    },

    swap: function (i, j) { var t = self.a[i]; self.a[i] = self.a[j]; self.a[j] = t; self.swp++; },

    allDone: function () {
      for (var i = 0; i < self.a.length; i++) self.done[i] = 1;
      self.snap({ ph: "xong — mảng đã sắp" });
      return self.F;
    }
  };
  self.snap({ ph: "mảng ban đầu" });
  return self;
}

function rBubble(vals) {
  var r = Rec(vals), n = r.a.length;
  for (var i = 0; i < n; i++) {
    var moved = false;
    for (var j = 0; j < n - i - 1; j++) {
      r.cmp++;
      r.snap({ hi: [j, j + 1], ph: "so " + r.v(j) + " với " + r.v(j + 1) });
      if (r.v(j) > r.v(j + 1)) {
        var big = r.v(j);
        r.swap(j, j + 1); moved = true;
        r.snap({ hi: [j, j + 1], lift: [j + 1], ph: big + " lớn hơn → đổi chỗ, nó trôi thêm một ô về phải" });
      }
    }
    r.done[n - i - 1] = 1;
    r.snap({ ph: "cái lớn nhất còn lại đã nổi tới cuối — chốt ô đó lại" });
    if (!moved) { r.snap({ ph: "một lượt không phải đổi chỗ lần nào → dừng sớm" }); break; }
  }
  return r.allDone();
}

function rSelect(vals) {
  var r = Rec(vals), n = r.a.length;
  for (var i = 0; i < n - 1; i++) {
    var m = i;
    r.snap({ hi: [i], pin: m, ph: "quét cả phần chưa sắp để tìm cái nhỏ nhất" });
    for (var j = i + 1; j < n; j++) {
      r.cmp++;
      r.snap({ hi: [j], pin: m, ph: "so " + r.v(j) + " với nhỏ nhất đang giữ là " + r.v(m) });
      if (r.v(j) < r.v(m)) { m = j; r.snap({ hi: [j], pin: m, ph: r.v(m) + " nhỏ hơn → đổi mốc sang đây" }); }
    }
    if (m !== i) {
      var sm = r.v(m);
      r.swap(i, m);
      r.snap({ hi: [i, m], lift: [i], ph: "đem " + sm + " về đầu phần chưa sắp" });
    }
    r.done[i] = 1;
    r.snap({ ph: "quét hết cả đoạn mới đổi đúng một lần" });
  }
  return r.allDone();
}

function rInsert(vals) {
  var r = Rec(vals), n = r.a.length;
  r.done[0] = 1;
  r.snap({ ph: "coi ô đầu tiên là đoạn đã sắp, dài đúng một ô" });
  for (var i = 1; i < n; i++) {
    var x = r.v(i), j = i;
    r.snap({ hi: [i], lift: [i], ph: "cầm " + x + " lên, lùi về trái tìm chỗ cắm" });
    while (j > 0) {
      r.cmp++;
      r.snap({ hi: [j - 1, j], lift: [j], ph: "so " + x + " đang cầm với " + r.v(j - 1) + " bên trái" });
      if (r.v(j - 1) > x) {
        r.swap(j - 1, j); j--;
        r.snap({ hi: [j, j + 1], lift: [j], ph: r.v(j + 1) + " lớn hơn → " + x + " bước qua nó sang trái" });
      } else {
        r.snap({ hi: [j - 1, j], lift: [j], ph: r.v(j - 1) + " nhỏ hơn rồi → dừng, đây là chỗ của " + x });
        break;
      }
    }
    for (var d = 0; d <= i; d++) r.done[d] = 1;
    r.snap({ ph: "đoạn đã sắp dài thêm một ô, giờ là " + (i + 1) + " ô" });
  }
  return r.allDone();
}

function rMerge(vals) {
  var r = Rec(vals), n = r.a.length, buf = new Array(n);
  for (var w = 1; w < n; w *= 2) {
    for (var lo = 0; lo < n; lo += 2 * w) {
      var mid = Math.min(lo + w, n), hi = Math.min(lo + 2 * w, n);
      if (mid >= hi) continue;
      var seg = [];
      for (var q = lo; q < hi; q++) seg.push(q);
      r.snap({ hi: seg, cold: [lo, hi], ph: "hai đoạn dài " + w + " này đều đã sắp sẵn → trộn lại" });
      var i = lo, j = mid, k = lo;
      while (i < mid && j < hi) { r.cmp++; buf[k++] = (r.a[i].v <= r.a[j].v) ? r.a[i++] : r.a[j++]; }
      while (i < mid) buf[k++] = r.a[i++];
      while (j < hi)  buf[k++] = r.a[j++];
      for (var t = lo; t < hi; t++) { r.a[t] = buf[t]; r.swp++; }
      r.snap({ hi: seg, cold: [lo, hi], ph: "mỗi lần chỉ so hai cái đầu hai đoạn → ra đoạn dài " + (hi - lo) + " đã sắp" });
    }
    if (w * 2 >= n) for (var d = 0; d < n; d++) r.done[d] = 1;
    r.snap({ ph: "hết một vòng — các đoạn sắp sẵn dài gấp đôi, còn " + Math.ceil(n / (2 * w)) + " đoạn" });
  }
  return r.allDone();
}

function rQuick(vals) {
  var r = Rec(vals), st = [[0, r.a.length - 1]];
  while (st.length) {
    var s = st.pop(), lo = s[0], hi = s[1];
    if (lo > hi) continue;
    if (lo === hi) { r.done[lo] = 1; r.snap({ hi: [lo], cold: [lo, hi + 1], ph: "đoạn còn đúng một ô → xong" }); continue; }
    var p = r.v(hi), i = lo;
    r.snap({ pin: hi, cold: [lo, hi + 1], ph: "lấy " + p + " ở cuối đoạn làm chốt" });
    for (var j = lo; j < hi; j++) {
      r.cmp++;
      r.snap({ hi: [j], pin: hi, cold: [lo, hi + 1], ph: "so " + r.v(j) + " với chốt " + p });
      if (r.v(j) < p) {
        if (i !== j) { var mv = r.v(j); r.swap(i, j); r.snap({ hi: [i, j], lift: [i], pin: hi, cold: [lo, hi + 1], ph: mv + " nhỏ hơn chốt → đẩy về bên trái" }); }
        i++;
      }
    }
    r.swap(i, hi); r.done[i] = 1;
    r.snap({ hi: [i], lift: [i], cold: [lo, hi + 1], ph: "chốt " + p + " về đúng chỗ — trái nó toàn nhỏ hơn, phải nó toàn lớn hơn" });
    st.push([lo, i - 1]); st.push([i + 1, hi]);
  }
  return r.allDone();
}

function rHeap(vals) {
  var r = Rec(vals), n = r.a.length;

  function sift(root, end, note) {
    while (true) {
      var big = root, l = 2 * root + 1, rr = 2 * root + 2;
      if (l < end)  { r.cmp++; if (r.v(l) > r.v(big)) big = l; }
      if (rr < end) { r.cmp++; if (r.v(rr) > r.v(big)) big = rr; }
      if (big === root) return;
      r.snap({ hi: [root, big], cold: [0, end], ph: note });
      var up = r.v(big);
      r.swap(root, big);
      r.snap({ hi: [root, big], lift: [root], cold: [0, end], ph: up + " lớn hơn cha → đổi chỗ, nó leo lên một tầng" });
      root = big;
    }
  }

  for (var i = Math.floor(n / 2) - 1; i >= 0; i--) sift(i, n, "dựng heap: xét ô " + i + " với hai con của nó");
  r.snap({ hi: [0], ph: "heap dựng xong — cái lớn nhất luôn bị đẩy lên ô đầu" });
  for (var e = n - 1; e > 0; e--) {
    var top = r.v(0);
    r.swap(0, e); r.done[e] = 1;
    r.snap({ hi: [0, e], lift: [e], cold: [0, e], ph: "đưa " + top + " về cuối, thu vùng heap lại một ô" });
    sift(0, e, "cái vừa đưa lên đầu thì nhỏ, cho nó chìm xuống");
  }
  r.done[0] = 1;
  return r.allDone();
}

/* ---------------- vẽ ---------------- */

var FR = [], IDX = 0, TIMER = null, SCE = "rand", DUR = 300, BARS = null, VAL = [];
var H = 132, GAP = 4, LIFT = 12;

function slot(i, n) { return "calc((100% - " + ((n - 1) * GAP) + "px) / " + n + " * " + i + " + " + (i * GAP) + "px)"; }

function build() {
  var k = el("salgo").value, A = ALGO[k];
  FR = A.run(DATA[SCE]);
  VAL = DATA[SCE];
  IDX = 0;

  var n = VAL.length, mx = Math.max.apply(null, VAL), view = el("sview");
  view.innerHTML = "";
  view.style.cssText = "position:relative;height:" + (H + LIFT + 22) + "px";

  BARS = [];
  for (var id = 0; id < n; id++) {
    var col = document.createElement("div");
    col.style.cssText =
      "position:absolute;bottom:0;top:0;width:calc((100% - " + ((n - 1) * GAP) + "px) / " + n + ");" +
      "display:flex;flex-direction:column;justify-content:flex-end;" +
      "transition:left " + DUR + "ms var(--ease),opacity .2s";
    col.innerHTML =
      '<u style="display:block;text-decoration:none;border-radius:2px 2px 0 0;' +
      'transition:background ' + Math.round(DUR * .5) + "ms,transform " + DUR + 'ms var(--ease)"></u>' +
      '<i style="font-style:normal;text-align:center;font-family:var(--mono);font-size:10.5px;' +
      'line-height:22px;height:22px;transition:color ' + Math.round(DUR * .5) + 'ms">' + VAL[id] + "</i>";
    view.appendChild(col);
    BARS.push({ col: col, bar: col.firstChild, lab: col.lastChild });
    BARS[id].bar.style.height = (16 + (VAL[id] / mx) * (H - 16)).toFixed(0) + "px";
  }

  el("smem").textContent = A.mem;
  el("snote").children[0].innerHTML = "<b>" + A.name + "</b> — " + A.idea;
  el("snote").children[1].innerHTML = "<em>" + (FR.length - 1) + " bước trên mảng này</em>";
  render();
}

function render() {
  var f = FR[IDX], n = f.ord.length;
  var hi = {}, dn = {}, lf = {};
  f.hi.forEach(function (p) { hi[f.ord[p]] = 1; });
  f.done.forEach(function (p) { dn[f.ord[p]] = 1; });
  f.lift.forEach(function (p) { lf[f.ord[p]] = 1; });
  var pin = f.pin >= 0 ? f.ord[f.pin] : -1;

  for (var pos = 0; pos < n; pos++) {
    var id = f.ord[pos], b = BARS[id];
    var cold = f.cold && (pos < f.cold[0] || pos >= f.cold[1]) && !dn[id];

    b.col.style.left = slot(pos, n);
    b.col.style.opacity = cold ? ".3" : "1";

    var c = "var(--filled)", t = "var(--muted)";
    if (dn[id])            { c = "var(--ok)";    t = "var(--ok)"; }
    if (id === pin)        { c = "var(--tomb)";  t = "var(--tomb)"; }
    if (hi[id])            { c = "var(--probe)"; t = "var(--probe)"; }
    b.bar.style.background = c;
    b.lab.style.color = t;
    b.bar.style.transform = lf[id] ? "translateY(-" + LIFT + "px)" : "none";
  }

  el("scmp").textContent = f.cmp;
  el("sswp").textContent = f.swp;
  el("sphase").textContent = f.ph;
  el("sbar").style.width = (IDX / (FR.length - 1) * 100).toFixed(1) + "%";
  el("sidx").textContent = IDX + " / " + (FR.length - 1);
}

function stop() { if (TIMER) { clearInterval(TIMER); TIMER = null; el("sauto").textContent = "Tự chạy"; } }
function step() { if (IDX < FR.length - 1) { IDX++; render(); } else stop(); }
function back() { if (IDX > 0) { IDX--; render(); } }

/* ---------------- nối vào giao diện ---------------- */

var sc = el("sscen");
SCEN.forEach(function (s, i) {
  var b = document.createElement("button");
  b.textContent = s[1];
  if (i === 0) b.className = "on";
  b.onclick = function () {
    [].slice.call(sc.children).forEach(function (x) { x.classList.remove("on"); });
    b.classList.add("on"); SCE = s[0]; stop(); build();
  };
  sc.appendChild(b);
});

var sp = el("sspeed");
SPEED.forEach(function (s, i) {
  var b = document.createElement("button");
  b.textContent = s[0];
  if (i === 1) b.className = "on";
  b.onclick = function () {
    [].slice.call(sp.children).forEach(function (x) { x.classList.remove("on"); });
    b.classList.add("on");
    DUR = s[1];
    var running = !!TIMER;
    stop();
    var keep = IDX; build(); IDX = keep; render();
    if (running) el("sauto").onclick();
  };
  sp.appendChild(b);
});

el("sstep").onclick = function () { stop(); step(); };
el("sback").onclick = function () { stop(); back(); };
el("srst").onclick  = function () { stop(); build(); };
el("salgo").onchange = function () { stop(); build(); };
el("sauto").onclick = function () {
  if (TIMER) return stop();
  if (IDX >= FR.length - 1) { IDX = 0; render(); }
  el("sauto").textContent = "Dừng";
  TIMER = setInterval(step, DUR + 40);
};

build();
})();
