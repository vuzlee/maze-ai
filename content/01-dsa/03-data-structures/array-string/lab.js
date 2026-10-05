/* Lab array — count shifts when inserting at the front vs at the end. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("arlab")) return;

  var mode = "front";

  el("amode").innerHTML =
    '<button data-m="front" class="on">insert(0, x) — at front</button>' +
    '<button data-m="back">append(x) — at end</button>';
  [].slice.call(el("amode").querySelectorAll("button")).forEach(function (b) {
    b.onclick = function () {
      [].slice.call(el("amode").querySelectorAll("button")).forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      mode = b.getAttribute("data-m");
      draw();
    };
  });
  el("an").addEventListener("input", draw);

  function fmt(n) {
    return n >= 1e6 ? (n / 1e6).toFixed(1) + "M"
         : n >= 1e3 ? (n / 1e3).toFixed(1) + "k" : String(n);
  }

  function draw() {
    var n = Math.max(10, Math.min(200000, +el("an").value || 10));
    /* front insert: the i-th call shifts i elements. end insert: shifts none */
    var shift = mode === "front" ? n * (n - 1) / 2 : 0;
    /* growth: CPython uses new = n + (n>>3) + 6, rounded up to a multiple of 4
       — a factor of ~1.125 rather than doubling, so it grows more often and copies ~8n */
    var grows = 0, copied = 0, alloc = 0;
    for (var i = 1; i <= n; i++) {
      if (i > alloc) {
        copied += i - 1;
        var nw = i + (i >> 3) + (i < 9 ? 3 : 6);
        alloc = (nw + 3) & ~3;
        grows++;
      }
    }

    el("ashift").textContent = fmt(shift);
    el("agrow").textContent = grows + " times · " + fmt(copied) + " elements";
    el("abig").textContent = mode === "front" ? "O(n²)" : "O(n) total · O(1) amortized each";

    /* comparison bar: the front-insert case is the 100% baseline */
    var worst = n * (n - 1) / 2;
    var pctShift = worst ? Math.max(0.4, 100 * shift / worst) : 0.4;
    var pctGrow = worst ? Math.max(0.4, 100 * copied / worst) : 40;
    el("aview").innerHTML =
      '<div class="bars">' +
      '<div class="b' + (mode === "front" ? " bad" : "") + '"><i>element shifts</i><u style="width:' +
        pctShift.toFixed(2) + '%"></u><b>' + fmt(shift) + "</b></div>" +
      '<div class="b hi"><i>copies from growth</i><u style="width:' + pctGrow.toFixed(2) + '%"></u><b>' +
        fmt(copied) + "</b></div></div>";

    el("anote").innerHTML = mode === "front"
      ? "<span>total shifts = <em>n(n−1)/2</em></span><span>the growth part is so small it is <em>invisible</em> on the bar</span>"
      : "<span>no elements shifted</span><span>the only cost is <em>≈ 8n</em> copies during growth</span>";
  }

  draw();
})();
