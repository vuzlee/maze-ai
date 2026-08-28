/* Lab array — đếm phép dịch khi chèn đầu so với chèn cuối. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("arlab")) return;

  var mode = "front";

  var guess = el("aguess"), ans = guess.querySelector(".ans");
  [].slice.call(guess.querySelectorAll(".opts button")).forEach(function (b) {
    b.onclick = function () {
      [].slice.call(guess.querySelectorAll(".opts button")).forEach(function (x) { x.classList.remove("pick"); });
      b.classList.add("pick");
      var v = b.getAttribute("data-v");
      ans.hidden = false;
      ans.innerHTML = (v === "50000000" ? "<b>Đúng — khoảng 50 triệu.</b> " : "<b>Đáp án: khoảng 50 triệu.</b> ") +
        "Lần chèn thứ i phải dịch i phần tử, nên tổng là <b>n(n−1)/2</b> ≈ 50 triệu với n = 10.000. " +
        "Chèn vào cuối thì tổng số phép dịch là <b>0</b>.";
    };
  });

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
    /* nới mảng: cấp phát gấp đôi → log2(n) lần chép, tổng ~2n phần tử được chép */
    var grows = Math.ceil(Math.log2(Math.max(2, n)));

    el("ashift").textContent = fmt(shift);
    el("agrow").textContent = grows + " lần · ~" + fmt(2 * n) + " phần tử";
    el("abig").textContent = mode === "front" ? "O(n²)" : "O(n) tổng · O(1) amortized mỗi lần";

    /* thanh so sánh: lấy ca chèn đầu làm mốc 100% */
    var worst = n * (n - 1) / 2;
    var pctShift = worst ? Math.max(0.4, 100 * shift / worst) : 0.4;
    var pctGrow = worst ? Math.max(0.4, 100 * (2 * n) / worst) : 40;
    el("aview").innerHTML =
      '<div class="bars">' +
      '<div class="b' + (mode === "front" ? " bad" : "") + '"><i>dịch phần tử</i><u style="width:' +
        pctShift.toFixed(2) + '%"></u><b>' + fmt(shift) + "</b></div>" +
      '<div class="b hi"><i>chép do nới mảng</i><u style="width:' + pctGrow.toFixed(2) + '%"></u><b>~' +
        fmt(2 * n) + "</b></div></div>";

    el("anote").innerHTML = mode === "front"
      ? "<span>tổng phép dịch = <em>n(n−1)/2</em></span><span>phần nới mảng nhỏ tới mức <em>không nhìn thấy</em> trên thanh</span>"
      : "<span>không phải dịch phần tử nào</span><span><em>chi phí duy nhất là ~2n phép chép khi nới mảng</em></span>";
  }

  draw();
})();
