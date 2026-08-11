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
    c.books.forEach(function (b) { FLAT.push({ book: b, cat: c }); });
  });

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---------------- chuyển khung nhìn ---------------- */
  function show(which) {
    if (lib) lib.hidden = which !== "page";
    if (reader) reader.hidden = which !== "page";
    if (results) results.hidden = which !== "res";
  }

  /* ---------------- trang chủ: dựng kệ ---------------- */
  if (lib) {
    lib.innerHTML = CAT.map(function (c) {
      var cards = c.books.map(function (b) {
        return '<a class="bk" href="' + BASE + b.path + '">' +
          '<div class="tag">' + esc(b.tag) + "</div>" +
          "<h3>" + esc(b.title) + "</h3>" +
          "<p>" + esc(b.blurb) + "</p>" +
          '<div class="meta"><span>' + b.n + " mục</span><b>đọc →</b></div></a>";
      }).join("\n");
      return '<div class="shelf"><h2>' + esc(c.name) +
        '<span class="gc">' + c.books.length + " bài</span></h2>" +
        '<p class="gnote">' + esc(c.note) + "</p>" +
        '<div class="cards">' + cards + "</div></div>";
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

  /* ---------------- trang bài: bài trước / bài sau ---------------- */
  var np = document.getElementById("np");
  if (doc && np) {
    var slug = doc.id.replace("art-", "");
    var i = -1;
    FLAT.forEach(function (x, k) { if (x.book.slug === slug) i = k; });
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
