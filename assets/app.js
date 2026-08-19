/* MazeAI — kịch bản dùng chung cho mọi trang.
   Trang chủ  : dựng các kệ sách từ CATALOG.
   Trang bài  : dựng mục lục từ chính các <section>, scrollspy, nút bài trước/sau.
   Mọi trang  : ô tìm kiếm toàn kho (đọc SEARCH_INDEX). */
(function () {
  var BASE = document.documentElement.getAttribute("data-base") || "";
  var CAT = window.CATALOG || [];
  var IDX = window.SEARCH_INDEX || [];

  var lib = document.getElementById("library");
  var reader = document.getElementById("reader");
  var results = document.getElementById("results");
  var qin = document.getElementById("q");
  var doc = document.querySelector(".doc");

  var FLAT = [];
  CAT.forEach(function (c) {
    c.groups.forEach(function (g) {
      g.books.forEach(function (b) { FLAT.push({ book: b, group: g, cat: c }); });
    });
  });

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---------------- chuyển khung nhìn ---------------- */
  function show(which) {
    if (lib) lib.hidden = which !== "page";
    if (reader) reader.hidden = which !== "page";
    if (results) results.hidden = which !== "res";
  }

  /* ---------------- trang chủ: dựng kệ ---------------- */
  function card(b) {
    return '<a class="bk" href="' + BASE + b.path + '">' +
      '<div class="tag">' + esc(b.tag) + "</div>" +
      "<h3>" + esc(b.title) + "</h3>" +
      "<p>" + esc(b.blurb) + "</p>" +
      '<div class="meta"><span>' + b.n + " mục</span><b>đọc →</b></div></a>";
  }

  if (lib) {
    lib.innerHTML = CAT.map(function (c) {
      var total = 0;
      c.groups.forEach(function (g) { total += g.books.length; });
      /* kệ chỉ có một nhóm thì không cần tiêu đề nhóm */
      var body = c.groups.map(function (g) {
        var cards = '<div class="cards">' + g.books.map(card).join("\n") + "</div>";
        if (c.groups.length < 2) return cards;
        return '<h3 class="sub">' + esc(g.name) +
          '<span class="gc">' + g.books.length + " bài</span></h3>" + cards;
      }).join("\n");
      return '<div class="shelf"><h2>' + esc(c.name) +
        '<span class="gc">' + total + " bài</span></h2>" +
        '<p class="gnote">' + esc(c.note) + "</p>" + body + "</div>";
    }).join("\n");
  }

  /* ---------------- trang bài: mục lục + scrollspy ---------------- */
  var tocBox = document.getElementById("toc");
  if (doc && tocBox) {
    var secs = [].slice.call(doc.querySelectorAll("section"));
    tocBox.innerHTML = secs.map(function (s) {
      var h = s.querySelector(".sh h2"), n = s.querySelector(".sh b");
      if (!h) return "";
      return '<a href="#' + s.id + '"><span>' + (n ? n.textContent : "") + "</span>" + h.textContent + "</a>";
    }).join("");

    var links = [].slice.call(tocBox.querySelectorAll("a"));
    var targets = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var ix = targets.indexOf(e.target);
        links.forEach(function (l, j) { l.classList.toggle("on", j === ix); });
      });
    }, { rootMargin: "-10% 0px -78% 0px" });
    targets.forEach(function (t) { if (t) io.observe(t); });
  }

  /* ---------------- trang bài: breadcrumb + bài trước / bài sau ---------------- */
  var np = document.getElementById("np");
  var crumb = document.getElementById("crumbTitle");
  var slug = doc ? doc.id.replace("art-", "") : "";
  var i = -1;
  FLAT.forEach(function (x, k) { if (x.book.slug === slug) i = k; });

  if (doc && crumb && i >= 0) {
    var here = FLAT[i];
    crumb.innerHTML = esc(here.cat.name) +
      (here.cat.groups.length > 1 ? " · " + esc(here.group.name) : "") +
      " · " + esc(here.book.title);
  }

  if (doc && np) {
    var p = i > 0 ? FLAT[i - 1] : null, n = i >= 0 ? FLAT[i + 1] : null;
    np.innerHTML =
      (p ? '<a href="' + BASE + p.book.path + '"><span>bài trước · ' + esc(p.cat.name) + "</span><b>" + esc(p.book.title) + "</b></a>" : "") +
      (n ? '<a href="' + BASE + n.book.path + '"><span>bài sau · ' + esc(n.cat.name) + "</span><b>" + esc(n.book.title) + "</b></a>" : "");
  }

  /* ---------------- tìm kiếm ---------------- */
  function rx(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

  function snippet(text, q) {
    var i = text.toLowerCase().indexOf(q.toLowerCase());
    if (i < 0) return esc(text.slice(0, 150)) + "…";
    var a = Math.max(0, i - 70);
    var cut = (a > 0 ? "…" : "") + text.slice(a, i + 130) + "…";
    return esc(cut).replace(new RegExp(rx(esc(q)), "ig"), function (m) { return "<mark>" + m + "</mark>"; });
  }

  function search(q) {
    if (!results) return;
    q = q.trim();
    if (!q) { show("page"); return; }
    var lo = q.toLowerCase();
    var hits = IDX.filter(function (e) {
      return e.t.toLowerCase().indexOf(lo) >= 0 || e.x.toLowerCase().indexOf(lo) >= 0;
    }).slice(0, 40);
    results.innerHTML =
      "<h2>Kết quả cho “" + esc(q) + "”</h2><p class=\"cnt\">" + hits.length + " mục</p>" +
      (hits.length
        ? hits.map(function (e) {
            return '<a class="hit" href="' + BASE + e.u + '"><div class="src">' + esc(e.b) + " · mục " + esc(e.n) + "</div>" +
              "<h3>" + esc(e.t) + "</h3><p>" + snippet(e.x, q) + "</p></a>";
          }).join("")
        : '<p style="color:var(--muted)">Không có mục nào khớp. Thử từ khoá ngắn hơn, hoặc tên tiếng Anh của khái niệm.</p>');
    show("res");
    window.scrollTo(0, 0);
  }

  if (qin) {
    var t = null;
    qin.addEventListener("input", function (e) {
      clearTimeout(t);
      var v = e.target.value;
      t = setTimeout(function () { search(v); }, 160);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== qin) { e.preventDefault(); qin.focus(); }
      if (e.key === "Escape" && document.activeElement === qin) { qin.value = ""; qin.blur(); show("page"); }
    });
  }

  /* mở thẳng một truy vấn: trang.html?q=tombstone */
  var q0 = (location.search.match(/[?&]q=([^&]*)/) || [])[1];
  if (q0 && qin) {
    qin.value = decodeURIComponent(q0.replace(/\+/g, " "));
    search(qin.value);
  } else {
    show("page");
  }
})();

/* ============================================================
   CÔNG CỤ HỌC
   Chạy sau khối trên, khi trang chủ và mục lục đã dựng xong.
   - thanh tiến độ đọc
   - mục lục đánh dấu phần đã đi qua + đếm 06/15
   - đánh dấu "đã học" từng bài, nhớ trong localStorage
   - mở/đóng toàn bộ phần hỏi đáp để tự kiểm tra
   - phím tắt j / k / m
   ============================================================ */
(function () {
  var BASE = document.documentElement.getAttribute("data-base") || "";
  var CAT = window.CATALOG || [];
  var doc = document.querySelector(".doc");
  var KEY = "mazeai.done";

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function readDone() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function writeDone(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
  }

  /* ---------------- trang chủ: tiến độ + lọc bài chưa học ---------------- */
  var lib = document.getElementById("library");
  if (lib) {
    var all = [];
    CAT.forEach(function (c) { c.groups.forEach(function (g) { g.books.forEach(function (b) { all.push(b); }); }); });

    var bar = document.createElement("div");
    bar.className = "libbar";
    lib.parentNode.insertBefore(bar, lib);

    var onlyTodo = false;
    function paint() {
      var done = readDone();
      var n = 0;
      [].slice.call(lib.querySelectorAll(".bk")).forEach(function (a) {
        var slug = a.getAttribute("data-slug");
        var is = done.indexOf(slug) >= 0;
        a.classList.toggle("done", is);
        a.hidden = onlyTodo && is;
        if (is) n++;
      });
      /* kệ nào trống sau khi lọc thì ẩn luôn cho gọn */
      [].slice.call(lib.querySelectorAll(".shelf")).forEach(function (s) {
        var vis = [].slice.call(s.querySelectorAll(".bk")).filter(function (a) { return !a.hidden; });
        s.classList.toggle("empty", vis.length === 0);
      });
      var pct = all.length ? Math.round(100 * n / all.length) : 0;
      bar.innerHTML =
        "<span>đã học <b>" + n + "/" + all.length + "</b> bài</span>" +
        '<span class="track"><i style="width:' + pct + '%"></i></span>' +
        "<span>" + pct + "%</span>" +
        '<button id="fTodo"' + (onlyTodo ? ' class="on"' : "") + ">chỉ bài chưa học</button>" +
        (n ? '<button id="fReset">xoá đánh dấu</button>' : "");
      document.getElementById("fTodo").onclick = function () { onlyTodo = !onlyTodo; paint(); };
      var r = document.getElementById("fReset");
      if (r) r.onclick = function () { if (confirm("Xoá toàn bộ đánh dấu đã học?")) { writeDone([]); paint(); } };
    }
    /* gắn slug lên từng card để biết card nào ứng với bài nào */
    var ix = 0;
    [].slice.call(lib.querySelectorAll(".bk")).forEach(function (a) { a.setAttribute("data-slug", all[ix++].slug); });
    paint();
  }

  if (!doc) return;

  /* ---------------- thanh tiến độ đọc ---------------- */
  var prog = document.createElement("div");
  prog.id = "prog";
  document.body.appendChild(prog);

  var tocLinks = [].slice.call(document.querySelectorAll("#toc a"));
  var secs = tocLinks.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });

  /* đầu mục lục: số mục đã đi qua / tổng số */
  var tocBox = document.getElementById("toc");
  var head = document.createElement("p");
  head.className = "head";
  if (tocBox) tocBox.parentNode.insertBefore(head, tocBox);
  var label = document.querySelector("nav.toc > p:not(.head)");
  if (label) label.remove();

  function onScroll() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    prog.style.width = (max > 0 ? Math.min(100, 100 * h.scrollTop / max) : 0) + "%";

    var passed = 0;
    secs.forEach(function (s, i) {
      if (!s) return;
      var seen = s.getBoundingClientRect().top < h.clientHeight * 0.4;
      tocLinks[i].classList.toggle("seen", seen);
      if (seen) passed = i + 1;
    });
    head.innerHTML = "Mục lục<b>" + String(passed).padStart(2, "0") + " / " + secs.length + "</b>";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------------- mở / đóng toàn bộ hỏi đáp ---------------- */
  [].slice.call(doc.querySelectorAll("section")).forEach(function (sec) {
    var qa = [].slice.call(sec.querySelectorAll("details.qa"));
    if (qa.length < 2) return;
    var sh = sec.querySelector(".sh");
    if (!sh) return;
    var b = document.createElement("button");
    b.className = "tool";
    b.textContent = "mở tất cả";
    b.onclick = function () {
      var open = qa.some(function (d) { return !d.open });
      qa.forEach(function (d) { d.open = open; });
      b.textContent = open ? "đóng tất cả" : "mở tất cả";
    };
    sh.appendChild(b);
  });

  /* ---------------- đánh dấu đã học ---------------- */
  var slug = doc.id.replace("art-", "");
  var np = document.getElementById("np");
  var barD = document.createElement("div");
  barD.className = "donebar";
  if (np) np.parentNode.insertBefore(barD, np);

  function paintDone() {
    var is = readDone().indexOf(slug) >= 0;
    barD.innerHTML = '<button id="mk"' + (is ? ' class="on"' : "") + ">" +
      (is ? "✓ đã học" : "đánh dấu đã học") + "</button>" +
      "<span>" + (is ? "bài này đã xong — hiện dấu ✓ ở trang chủ" : "phím tắt: m") + "</span>";
    document.getElementById("mk").onclick = toggleDone;
  }
  function toggleDone() {
    var list = readDone(), i = list.indexOf(slug);
    if (i >= 0) list.splice(i, 1); else list.push(slug);
    writeDone(list);
    paintDone();
  }
  paintDone();

  /* ---------------- phím tắt ---------------- */
  var hint = document.createElement("p");
  hint.className = "hint";
  hint.innerHTML = "<kbd>j</kbd>mục sau &nbsp; <kbd>k</kbd>mục trước<br><kbd>m</kbd>đánh dấu đã học &nbsp; <kbd>/</kbd>tìm";
  var nav = document.querySelector("nav.toc");
  if (nav) nav.appendChild(hint);

  document.addEventListener("keydown", function (e) {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" || e.metaKey || e.ctrlKey) return;
    if (e.key === "m") { e.preventDefault(); toggleDone(); return; }
    if (e.key !== "j" && e.key !== "k") return;
    e.preventDefault();
    var cur = 0;
    secs.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < 90) cur = i; });
    var to = secs[Math.max(0, Math.min(secs.length - 1, cur + (e.key === "j" ? 1 : -1)))];
    if (to) to.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
