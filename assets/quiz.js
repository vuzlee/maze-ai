/* MazeAI — trang ôn tập bằng thẻ lật (quiz.html).

   Nguồn thẻ là assets/quiz-index.js, do tools/build.py bóc từ chính các
   <details class="qa"> trong bài — không có bản sao câu hỏi nào phải bảo trì riêng.

   Cách học: đọc bài → xem lab → sang đây tự kiểm. Với kệ DSA thì thẻ chỉ hỏi
   ý tưởng; thực hành vẫn là LeetCode trong chính bài, nên thẻ DSA trỏ ngược về đó. */
(function () {
  var page = document.getElementById("quizpage");
  if (!page) return;

  var CARDS = window.QUIZ || [];
  var CAT = window.CATALOG || [];
  var KEY = "mazeai.quiz";          /* { id: lần nhớ liên tiếp } */

  var mast = document.querySelector(".quizmast");
  var pick = document.getElementById("qpick");
  var run = document.getElementById("qrun");
  var done = document.getElementById("qdone");

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function readMem() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function writeMem(m) { try { localStorage.setItem(KEY, JSON.stringify(m)); } catch (e) {} }

  /* --- tra ngược từ đường dẫn bài về metadata trong catalog: lấy số bài LeetCode --- */
  var BOOK = {};
  CAT.forEach(function (c) {
    c.groups.forEach(function (g) {
      g.books.forEach(function (b) { BOOK[b.path] = { book: b, cat: c }; });
    });
  });
  function pathOf(u) { return u.split("#")[0]; }

  /* --- gom thẻ theo kệ, giữ đúng thứ tự kệ ngoài trang chủ --- */
  var SHELF = [];
  CAT.forEach(function (c) {
    var ids = {};
    c.groups.forEach(function (g) { g.books.forEach(function (b) { ids[b.path] = 1; }); });
    var mine = CARDS.filter(function (k) { return ids[pathOf(k.u)]; });
    if (mine.length) SHELF.push({ dir: c.dir, name: c.name, cards: mine });
  });

  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* ================= màn chọn bộ thẻ ================= */
  function paintPick() {
    var mem = readMem();
    function stat(list) {
      var got = 0;
      list.forEach(function (k) { if (mem[k.id]) got++; });
      return got;
    }
    var allGot = stat(CARDS);
    var weak = CARDS.filter(function (k) { return !mem[k.id]; });

    var rows = SHELF.map(function (s, i) {
      var g = stat(s.cards);
      var pct = Math.round(100 * g / s.cards.length);
      return '<button class="qshelf" data-i="' + i + '">' +
        '<i>' + String(i + 1).padStart(2, "0") + "</i>" +
        "<b>" + esc(s.name) + "</b>" +
        '<span class="qn">' + g + " / " + s.cards.length + " thẻ</span>" +
        '<span class="qtrack"><i style="width:' + pct + '%"></i></span>' +
        "</button>";
    }).join("");

    pick.innerHTML =
      '<ul class="counts">' +
      "<li><b>" + CARDS.length + "</b><span>thẻ</span></li>" +
      "<li><b>" + SHELF.length + "</b><span>kệ</span></li>" +
      "<li><b>" + allGot + "</b><span>đã nhớ</span></li>" +
      "</ul>" +
      '<div class="qtop">' +
      '<button class="btn primary" id="qAll">Ôn ngẫu nhiên toàn kho</button>' +
      (weak.length && weak.length < CARDS.length
        ? '<button class="btn ghost" id="qWeak">Chỉ thẻ chưa nhớ · ' + weak.length + "</button>" : "") +
      (allGot ? '<button class="btn ghost" id="qReset">Xoá tiến độ ôn</button>' : "") +
      "</div>" +
      '<p class="qhint">Chọn một kệ, hoặc ôn trộn cả kho. Thẻ nào bấm <b>Chưa nhớ</b> sẽ quay lại ở cuối lượt.</p>' +
      '<div class="qshelves">' + rows + "</div>";

    document.getElementById("qAll").onclick = function () { start(shuffle(CARDS), "Toàn kho"); };
    var w = document.getElementById("qWeak");
    if (w) w.onclick = function () { start(shuffle(weak), "Thẻ chưa nhớ"); };
    var r = document.getElementById("qReset");
    if (r) r.onclick = function () {
      if (confirm("Xoá toàn bộ tiến độ ôn tập?")) { writeMem({}); paintPick(); }
    };
    [].slice.call(pick.querySelectorAll(".qshelf")).forEach(function (b) {
      b.onclick = function () {
        var s = SHELF[+b.getAttribute("data-i")];
        start(shuffle(s.cards), s.name);
      };
    });
  }

  /* ================= chạy một lượt ================= */
  var deck = [], at = 0, label = "", nGot = 0, seen = 0;

  function start(list, name) {
    deck = list; at = 0; label = name; nGot = 0; seen = 0;
    pick.hidden = true; done.hidden = true; run.hidden = false;
    if (mast) mast.hidden = true;
    window.scrollTo(0, 0);
    paintCard();
  }

  function paintCard() {
    if (at >= deck.length) return finish();
    var k = deck[at];
    var meta = BOOK[pathOf(k.u)];
    var lc = meta && meta.book.lc;

    document.getElementById("qwhere").innerHTML =
      "<em>" + esc(k.c) + "</em>" + esc(k.b);
    document.getElementById("qcount").textContent = (at + 1) + " / " + deck.length;
    document.getElementById("qbar").style.width =
      Math.round(100 * at / deck.length) + "%";

    document.getElementById("qq").textContent = k.q;
    var ans = document.getElementById("qa2");
    ans.innerHTML = k.a + (lc
      ? '<p class="qlc">Hiểu ý rồi thì luyện tay: bài này có <b>' + lc +
        " bài LeetCode</b> ở cuối trang gốc.</p>" : "");
    ans.hidden = true;

    document.getElementById("qflip").hidden = false;
    document.getElementById("qacts").hidden = true;
    document.getElementById("qsrc").href = k.u;
    document.getElementById("qcard").classList.remove("open");
  }

  function flip() {
    document.getElementById("qa2").hidden = false;
    document.getElementById("qflip").hidden = true;
    document.getElementById("qacts").hidden = false;
    document.getElementById("qcard").classList.add("open");
  }

  function mark(ok) {
    var k = deck[at];
    var mem = readMem();
    if (ok) { mem[k.id] = (mem[k.id] || 0) + 1; nGot++; }
    else { delete mem[k.id]; deck.push(k); }   /* chưa nhớ thì quay lại cuối lượt */
    writeMem(mem);
    seen++; at++;
    paintCard();
  }

  function finish() {
    run.hidden = true; done.hidden = false;
    var pct = seen ? Math.round(100 * nGot / seen) : 0;
    done.innerHTML =
      "<h2>Xong lượt <em>" + esc(label) + "</em></h2>" +
      '<ul class="counts">' +
      "<li><b>" + nGot + "</b><span>nhớ rồi</span></li>" +
      "<li><b>" + (seen - nGot) + "</b><span>lật lại</span></li>" +
      "<li><b>" + pct + "%</b><span>lần đầu đúng</span></li>" +
      "</ul>" +
      "<p>" + (pct >= 80
        ? "Nắm chắc rồi. Sang kệ khác, hoặc quay về bài để làm phần thực hành."
        : "Còn vài chỗ chưa vào. Đọc lại bài rồi ôn lại bộ này — thẻ nào lật lại sẽ quay đúng vào đó.") + "</p>" +
      '<div class="qtop">' +
      '<button class="btn primary" id="qMore">Ôn bộ khác</button>' +
      '<a class="btn ghost" href="index.html">Về thư viện</a></div>';
    document.getElementById("qMore").onclick = backToPick;
  }

  document.getElementById("qflip").onclick = flip;
  document.getElementById("qgot").onclick = function () { mark(true); };
  document.getElementById("qagain").onclick = function () { mark(false); };
  function backToPick() {
    run.hidden = true; done.hidden = true; pick.hidden = false;
    if (mast) mast.hidden = false;
    window.scrollTo(0, 0); paintPick();
  }
  document.getElementById("qstop").onclick = backToPick;

  /* phím tắt: cách lật, 1 chưa nhớ, 2 nhớ rồi */
  document.addEventListener("keydown", function (e) {
    if (run.hidden) return;
    var t = e.target.tagName;
    if (t === "INPUT" || t === "TEXTAREA") return;
    if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      if (document.getElementById("qa2").hidden) flip(); else mark(true);
    } else if (e.key === "1") { if (!document.getElementById("qa2").hidden) mark(false); }
    else if (e.key === "2") { if (!document.getElementById("qa2").hidden) mark(true); }
  });

  /* --- mở thẳng một bộ khi tới từ link ?b=<đường dẫn bài> hoặc ?s=<thư mục kệ> --- */
  function fromQuery() {
    var m = /[?&]b=([^&]+)/.exec(location.search);
    if (m) {
      var path = decodeURIComponent(m[1]);
      var mine = CARDS.filter(function (k) { return pathOf(k.u) === path; });
      if (mine.length) { start(shuffle(mine), BOOK[path] ? BOOK[path].book.title : "Bài này"); return true; }
    }
    m = /[?&]s=([^&]+)/.exec(location.search);
    if (m) {
      var dir = decodeURIComponent(m[1]);
      for (var i = 0; i < SHELF.length; i++) {
        if (SHELF[i].dir === dir) { start(shuffle(SHELF[i].cards), SHELF[i].name); return true; }
      }
    }
    return false;
  }

  paintPick();
  fromQuery();
})();
