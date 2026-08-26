/* Lab binary search — kể chuyện thay vì bảng điều khiển.
   Bốn phần: đoán trước → kịch bản → chạy từng bước có tô dòng code → câu chốt. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("bslab")) return;

  /* ---------- phần 1: đoán trước khi chạy ---------- */
  var guess = el("bguess");
  var ans = guess.querySelector(".ans");
  [].slice.call(guess.querySelectorAll(".opts button")).forEach(function (b) {
    b.onclick = function () {
      [].slice.call(guess.querySelectorAll(".opts button")).forEach(function (x) { x.classList.remove("pick"); });
      b.classList.add("pick");
      var v = b.getAttribute("data-v");
      ans.hidden = false;
      ans.innerHTML = (v === "20"
        ? "<b>Đúng — 20 bước.</b> "
        : "<b>Đáp án là 20 bước.</b> ") +
        "Mỗi bước bỏ đi một nửa, nên số bước là log₂(1.000.000) ≈ 20. " +
        "Mảng 1 tỉ phần tử cũng chỉ cần 30. Tăng dữ liệu gấp nghìn lần chỉ thêm 10 bước — " +
        "đó là lý do log n gần như miễn phí.";
    };
  });

  /* ---------- kịch bản ---------- */
  var A = [1, 3, 4, 4, 4, 7, 9, 11, 15, 20];

  var CODE = {
    lower: [
      { t: 'lo, hi = 0, len(a)', k: 'init' },
      { t: 'while lo < hi:', k: 'loop' },
      { t: '    mid = lo + (hi - lo) // 2', k: 'mid' },
      { t: '    if a[mid] < t:', k: 'cmp' },
      { t: '        lo = mid + 1', k: 'left' },
      { t: '    else:', k: 'cmp2' },
      { t: '        hi = mid', k: 'right' },
      { t: 'return lo', k: 'done' }
    ],
    upper: [
      { t: 'lo, hi = 0, len(a)', k: 'init' },
      { t: 'while lo < hi:', k: 'loop' },
      { t: '    mid = lo + (hi - lo) // 2', k: 'mid' },
      { t: '    if a[mid] <= t:', k: 'cmp' },
      { t: '        lo = mid + 1', k: 'left' },
      { t: '    else:', k: 'cmp2' },
      { t: '        hi = mid', k: 'right' },
      { t: 'return lo', k: 'done' }
    ],
    exact: [
      { t: 'lo, hi = 0, len(a) - 1', k: 'init' },
      { t: 'while lo <= hi:', k: 'loop' },
      { t: '    mid = lo + (hi - lo) // 2', k: 'mid' },
      { t: '    if a[mid] == t: return mid', k: 'cmp' },
      { t: '    elif a[mid] < t: lo = mid + 1', k: 'left' },
      { t: '    else:            hi = mid - 1', k: 'right' },
      { t: 'return -1', k: 'done' }
    ]
  };

  var SCEN = [
    { id: "lower", t: 4, mode: "lower", label: "tìm mép TRÁI của 4",
      ask: "Nhóm ba số 4 nằm ở chỉ số 2, 3, 4. lower_bound phải dừng đúng ở 2.",
      end: function (r) { return "Trả về <b>" + r + "</b> — chỉ số đầu tiên có a[i] ≥ 4. Đây là <b>mép trái</b> của nhóm trùng, dùng cho câu hỏi “vị trí xuất hiện đầu tiên”."; } },
    { id: "upper", t: 4, mode: "upper", label: "tìm mép PHẢI của 4",
      ask: "Cùng mảng, cùng target, chỉ đổi một dấu = trong điều kiện so sánh.",
      end: function (r) { return "Trả về <b>" + r + "</b> — chỉ số đầu tiên có a[i] > 4. Số lần xuất hiện của 4 = 5 − 2 = <b>3</b>."; } },
    { id: "miss", t: 5, mode: "lower", label: "tìm số KHÔNG có (5)",
      ask: "Số 5 không nằm trong mảng. Đoán xem hàm trả về gì thay vì báo lỗi?",
      end: function (r) { return "Trả về <b>" + r + "</b> — vị trí <b>đáng lẽ phải chèn vào</b>, không phải −1. Vì vậy luôn phải kiểm <code>i &lt; len(a) and a[i] == t</code> trước khi dùng."; } },
    { id: "exact", t: 4, mode: "exact", label: "mẫu 1 tìm 4",
      ask: "Cùng mảng có ba số 4. Mẫu 1 sẽ dừng ở cái nào trong ba?",
      end: function (r) { return "Trả về <b>" + r + "</b> — một vị trí <b>bất kỳ</b> trong nhóm trùng, không phải mép trái. Đó là lý do mẫu 1 không trả lời được câu hỏi về biên."; } }
  ];

  /* ---------- máy trạng thái ---------- */
  var cur, lo, hi, mid, step, phase, result, timer = null;

  function build(sc) {
    stopAuto();
    cur = sc;
    var closed = sc.mode === "exact";
    lo = 0; hi = closed ? A.length - 1 : A.length;
    mid = null; step = 0; result = null; phase = "init";
    el("bverdict").hidden = true;
    el("bstep").disabled = false;
    draw();
    say("Trạng thái ban đầu", sc.ask);
  }

  function alive() {
    return cur.mode === "exact" ? lo <= hi : lo < hi;
  }

  function next() {
    if (result !== null) return;
    if (phase === "init" || phase === "move") {
      if (!alive()) { finish(cur.mode === "exact" ? -1 : lo); return; }
      phase = "mid";
      mid = lo + Math.floor((hi - lo) / 2);
      step++;
      draw();
      say("Bước " + step + " — lấy điểm giữa",
        "mid = " + lo + " + (" + hi + " − " + lo + ") // 2 = <b>" + mid + "</b>, giá trị a[" + mid + "] = <b>" + A[mid] + "</b>.");
      return;
    }
    if (phase === "mid") {
      var v = A[mid], t = cur.t, goRight;
      if (cur.mode === "exact") {
        if (v === t) { phase = "cmp"; draw(); finish(mid); return; }
        goRight = v < t;
      } else if (cur.mode === "lower") {
        goRight = v < t;
      } else {
        goRight = v <= t;
      }
      phase = goRight ? "left" : "right";
      var why;
      if (goRight) {
        why = "a[" + mid + "] = " + v + (cur.mode === "upper" ? " ≤ " : " < ") + t +
          " → mid <b>chắc chắn không phải</b> đáp án, loại luôn nó: <code>lo = mid + 1</code>.";
        lo = mid + 1;
      } else {
        why = "a[" + mid + "] = " + v + (cur.mode === "upper" ? " > " : " ≥ ") + t +
          " → mid <b>có thể chính là</b> đáp án, nên giữ lại: <code>hi = mid</code>.";
        hi = cur.mode === "exact" ? mid - 1 : mid;
      }
      if (cur.mode === "exact") {
        why = goRight
          ? "a[" + mid + "] = " + v + " < " + t + " → đáp án nằm bên phải: <code>lo = mid + 1</code>."
          : "a[" + mid + "] = " + v + " > " + t + " → đáp án nằm bên trái: <code>hi = mid - 1</code>.";
      }
      draw();
      say("Bước " + step + " — so sánh rồi thu hẹp", why);
      phase = "move";
      return;
    }
  }

  function finish(r) {
    result = r;
    phase = "done";
    mid = null;
    el("bstep").disabled = true;
    stopAuto();
    draw();
    say("Xong sau " + step + " bước", "Vòng lặp dừng vì khoảng đã rỗng." +
      (cur.mode === "exact" ? "" : " Lúc này <b>lo == hi == " + lo + "</b> — chính là ranh giới cần tìm."));
    var v = el("bverdict");
    v.hidden = false;
    v.innerHTML = cur.end(r) + " Mảng 10 phần tử, đi hết <b>" + step + " bước</b> — log₂(10) ≈ 3,3.";
  }

  /* ---------- vẽ ---------- */
  function draw() {
    var closed = cur.mode === "exact";
    var hiIx = closed ? hi : hi - 1;      /* ô cuối còn trong khoảng */
    var h = '<div class="strip">';
    for (var i = 0; i < A.length; i++) {
      var out = result === null ? (i < lo || i > hiIx) : (i !== result);
      var mk = "";
      if (i === lo && result === null) mk += "lo";
      if (i === mid) mk += (mk ? " " : "") + "mid";
      if (i === hiIx && result === null) mk += (mk ? " " : "") + "hi";
      if (result !== null && i === result) mk = "kết quả";
      h += '<div class="c' + (i === mid ? " on" : "") + (out ? " out" : "") + '">' +
        "<i>" + i + "</i><b>" + A[i] + "</b><u>" + mk + "</u></div>";
    }
    el("bview").innerHTML = h + "</div>";

    var note = el("bnote");
    note.innerHTML = "<span>target = <em>" + cur.t + "</em> · khoảng còn lại <em>" +
      (result !== null ? "rỗng" : (closed ? "[" + lo + ", " + hi + "]" : "[" + lo + ", " + hi + ")")) +
      "</em> · còn <em>" + Math.max(0, hiIx - lo + 1) + "</em> ô chưa loại</span>" +
      "<span>bước <em>" + step + "</em></span>";

    /* code + dòng đang chạy */
    var lines = CODE[cur.mode];
    var active = { init: "init", mid: "mid", left: "left", right: "right", move: "loop", done: "done" }[phase] || "loop";
    el("bcode").innerHTML = lines.map(function (l) {
      var txt = l.t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      txt = txt.replace(/\b(while|if|elif|else|return|len)\b/g, '<span class="kw">$1</span>');
      return '<div class="ln' + (l.k === active ? " on" : "") + '">' + txt + "</div>";
    }).join("");

    el("bstat").textContent = result !== null
      ? "đã xong · " + step + " bước"
      : "đã đi " + step + " bước";
  }

  function say(head, body) {
    el("bexp").innerHTML = "<h6>" + head + "</h6><p>" + body + "</p>" +
      '<p class="vals">lo = <b>' + lo + "</b> · mid = <b>" + (mid === null ? "–" : mid) +
      "</b> · hi = <b>" + hi + "</b></p>";
  }

  /* ---------- điều khiển ---------- */
  function stopAuto() {
    if (timer) { clearInterval(timer); timer = null; el("bauto").textContent = "Tự chạy"; }
  }
  el("bstep").onclick = function () { stopAuto(); next(); };
  el("bauto").onclick = function () {
    if (timer) { stopAuto(); return; }
    el("bauto").textContent = "Dừng";
    timer = setInterval(function () {
      if (result !== null) { stopAuto(); return; }
      next();
    }, 900);
  };
  el("brst").onclick = function () { build(cur); };

  el("bscen").innerHTML = SCEN.map(function (s, i) {
    return '<button data-i="' + i + '"' + (i === 0 ? ' class="on"' : "") + ">" + s.label + "</button>";
  }).join("");
  [].slice.call(el("bscen").querySelectorAll("button")).forEach(function (b) {
    b.onclick = function () {
      [].slice.call(el("bscen").querySelectorAll("button")).forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      build(SCEN[+b.getAttribute("data-i")]);
    };
  });

  build(SCEN[0]);
})();
