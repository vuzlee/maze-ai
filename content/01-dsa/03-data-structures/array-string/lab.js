/* Lab array — đếm phép dịch khi chèn đầu so với chèn cuối. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("arlab")) return;

  var mode = "front";

  el("amode").innerHTML =
    '<button data-m="front" class="on">insert(0, x) — chèn đầu</button>' +
    '<button data-m="back">append(x) — chèn cuối</button>';
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
    return n >= 1e6 ? (n / 1e6).toFixed(1).replace(".", ",") + " triệu"
         : n >= 1e3 ? (n / 1e3).toFixed(1).replace(".", ",") + " nghìn" : String(n);
  }

  function draw() {
    var n = Math.max(10, Math.min(200000, +el("an").value || 10));
    /* chèn đầu: lần thứ i dịch i phần tử. chèn cuối: không dịch phần tử nào */
    var shift = mode === "front" ? n * (n - 1) / 2 : 0;
    /* nới mảng: CPython dùng new = n + (n>>3) + 6, làm tròn lên bội của 4
       — hệ số ~1,125 chứ không phải gấp đôi, nên nở nhiều lần hơn và chép ~8n */
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
    el("agrow").textContent = grows + " lần · " + fmt(copied) + " phần tử";
    el("abig").textContent = mode === "front" ? "O(n²)" : "O(n) tổng · O(1) amortized mỗi lần";

    /* thanh so sánh: lấy ca chèn đầu làm mốc 100% */
    var worst = n * (n - 1) / 2;
    var pctShift = worst ? Math.max(0.4, 100 * shift / worst) : 0.4;
    var pctGrow = worst ? Math.max(0.4, 100 * copied / worst) : 40;
    el("aview").innerHTML =
      '<div class="bars">' +
      '<div class="b' + (mode === "front" ? " bad" : "") + '"><i>dịch phần tử</i><u style="width:' +
        pctShift.toFixed(2) + '%"></u><b>' + fmt(shift) + "</b></div>" +
      '<div class="b hi"><i>chép do nới mảng</i><u style="width:' + pctGrow.toFixed(2) + '%"></u><b>' +
        fmt(copied) + "</b></div></div>";

    el("anote").innerHTML = mode === "front"
      ? "<span>tổng phép dịch = <em>n(n−1)/2</em></span><span>phần nới mảng nhỏ tới mức <em>không nhìn thấy</em> trên thanh</span>"
      : "<span>không phải dịch phần tử nào</span><span>chi phí duy nhất là <em>≈ 8n</em> phép chép khi nới mảng</span>";
  }

  draw();
})();
