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
  /* Khi mở kết quả tìm kiếm thì cất hết phần trang chủ đi, để kết quả
     nằm ngay đầu màn hình chứ không bị đẩy xuống dưới hero. */
  function show(which) {
    var page = which === "page";
    [lib, reader, document.getElementById("libcols"),
     document.querySelector(".mast"), document.querySelector(".libbar")]
      .forEach(function (el) { if (el) el.hidden = !page; });
    if (results) results.hidden = which !== "res";
  }

  /* ---------------- trang chủ: dựng kệ ---------------- */
  function card(b, n) {
    return '<a class="bk' + (b.skeleton ? " wip" : "") + (b.v2 ? " s-done" : b.skeleton ? "" : b.progress ? " s-prog" : " s-todo") + '" data-slug="' + esc(b.slug) +
      '" href="' + BASE + b.path + '">' +
      '<span class="ix">' + String(n).padStart(2, "0") + "</span>" +
      '<span class="tt"><b>' + esc(b.title) + "</b><i>" + esc(b.blurb) + "</i></span>" +
      '<span class="tag">' + (b.skeleton ? "outline · " + b.n + " sections" : esc(b.tag) + " · " + b.n + " sections") +
        (b.skeleton ? "" : b.v2 ? '<i class="st done">Reviewed</i>' : b.progress ? '<i class="st prog">In progress</i>' : '<i class="st todo">To do</i>') + "</span>" +
      '<span class="go">→</span></a>';
  }

  if (lib) {
    var OPEN_KEY = "mazeai.open";
    var openSet = {};
    try { openSet = JSON.parse(localStorage.getItem(OPEN_KEY)) || {}; } catch (e) {}
    var saveOpen = function () { try { localStorage.setItem(OPEN_KEY, JSON.stringify(openSet)); } catch (e) {} };

    var shelfHTML = function (c, ci) {
      var total = 0, skel = 0, v2 = 0;
      c.groups.forEach(function (g) { g.books.forEach(function (b) {
        if (b.skeleton) skel++; else total++; if (b.v2) v2++; }); });
      var n = 0;
      var body = c.groups.map(function (g) {
        var rows = '<div class="cards">' +
          g.books.map(function (b) { return card(b, ++n); }).join("\n") + "</div>";
        if (c.groups.length < 2) return rows;
        return '<h3 class="sub">' + esc(g.name) +
          '<span class="gc">' + g.books.length + (g.books.length == 1 ? " lesson" : " lessons") + "</span></h3>" + rows;
      }).join("\n");
      var pct = total ? Math.round(100 * v2 / (total + skel)) : 0;
      return '<details class="shelf" id="shelf-' + ci + '"' + (openSet[ci] ? " open" : "") + ">" +
        '<summary class="shelfhead">' +
          '<span class="num">' + String(ci + 1).padStart(2, "0") + "</span>" +
          "<div><h2>" + esc(c.name) + "</h2>" +
          '<p class="gnote">' + esc(c.note) + "</p></div>" +
          '<div class="shelfstat"><b>' + total + (total == 1 ? " lesson" : " lessons") + "</b>" +
          (skel ? '<i class="sk">+' + skel + " outlines</i>" : "") +
          '<span class="track" title="' + v2 + ' reviewed in the new style"><i style="width:' + pct + '%"></i></span></div>' +
          '<span class="chev" aria-hidden="true"></span>' +
        "</summary>" + '<div class="shelfbody">' + body + "</div></details>";
    };

    lib.innerHTML = CAT.map(function (c, ci) { return shelfHTML(c, ci); }).join("\n");

    /* smooth open/close: animate the <details> height instead of snapping */
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    [].slice.call(lib.querySelectorAll("details.shelf > summary")).forEach(function (sm) {
      sm.addEventListener("click", function (e) {
        if (reduce) return;
        var d = sm.parentNode;
        e.preventDefault();
        if (d.classList.contains("anim")) return;
        var start = d.offsetHeight;
        d.classList.add("anim");
        var done = function (cb) {            /* end the animation once, by event or by timer */
          var fired = false;
          var fin = function () { if (fired) return; fired = true; d.removeEventListener("transitionend", onEnd); cb(); d.style.height = ""; d.classList.remove("anim"); };
          var onEnd = function (ev) { if (ev.target === d && ev.propertyName === "height") fin(); };
          d.addEventListener("transitionend", onEnd);
          setTimeout(fin, 420);
        };
        d.style.height = start + "px";
        if (d.open) {
          var end = sm.offsetHeight;
          d.offsetHeight;                     /* commit the start height before changing it */
          d.style.height = end + "px";
          done(function () { d.open = false; });
        } else {
          d.open = true;
          var end2 = sm.offsetHeight + d.querySelector(".shelfbody").offsetHeight + 12;
          d.offsetHeight;
          d.style.height = end2 + "px";
          done(function () {});
        }
      });
    });
    [].slice.call(lib.querySelectorAll("details.shelf")).forEach(function (d) {
      d.addEventListener("toggle", function () {
        var i = d.id.replace("shelf-", "");
        if (d.open) openSet[i] = 1; else delete openSet[i];
        saveOpen();
      });
    });
    /* a link to #shelf-N opens that shelf */
    var openFromHash = function () {
      var m = /^#shelf-(\d+)$/.exec(location.hash);
      if (!m) return;
      var d = document.getElementById("shelf-" + m[1]);
      if (d && !d.open) d.open = true;
    };
    window.addEventListener("hashchange", openFromHash);
    openFromHash();

    /* --- left index: tracks with their shelves; the shelf in view lights up --- */
    var nav = document.getElementById("side");
    if (nav) {
      nav.innerHTML =
        '<p class="sidehead">Library · ' + CAT.length + " shelves</p>" +
        '<div class="list">' +
        CAT.map(function (c, ci) {
          var k = 0;
          c.groups.forEach(function (g) { g.books.forEach(function (b) { if (!b.skeleton) k++; }); });
          return '<a href="#shelf-' + ci + '"><i>' + String(ci + 1).padStart(2, "0") + "</i>" +
            "<span>" + esc(c.name) + "</span><em>" + k + "</em></a>";
        }).join("") + "</div>" +
        '<p class="sidefoot"><kbd>/</kbd> search the library</p>';

      var chips = [].slice.call(nav.querySelectorAll("a"));
      var shelves = chips.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
      chips.forEach(function (a, i) {
        a.addEventListener("click", function () { if (shelves[i]) shelves[i].open = true; });
      });
      var last = -1, ticking = false;
      var spy = function () {
        ticking = false;
        var top = window.innerHeight * 0.3, cur = 0;
        for (var i = 0; i < shelves.length; i++) { if (shelves[i] && shelves[i].getBoundingClientRect().top < top) cur = i; else break; }
        if (cur === last) return;
        last = cur;
        chips.forEach(function (a, i) { a.classList.toggle("on", i === cur); });
      };
      var onSpy = function () { if (!ticking) { ticking = true; requestAnimationFrame(spy); } };
      window.addEventListener("scroll", onSpy, { passive: true });
      spy();
    }

    /* --- ba con số: quy mô kho, thấy ngay từ màn đầu --- */
    var facts = document.getElementById("counts");
    if (facts) {
      var nb = 0, ns = 0;
      CAT.forEach(function (c) {
        c.groups.forEach(function (g) { g.books.forEach(function (b) {
          if (b.skeleton) return; nb++; ns += b.n || 0; }); });
      });
      facts.innerHTML =
        "<li><b>" + nb + "</b><span>lessons</span></li>" +
        "<li><b>" + CAT.length + "</b><span>shelves</span></li>" +
        "<li><b>" + ns + "</b><span>sections</span></li>";
    }

    /* --- nút "Bắt đầu học" trỏ vào kệ đầu tiên, nút tìm mở ô tìm kiếm --- */
    var gf = document.getElementById("goFind");
    if (gf && qin) gf.onclick = function () { qin.focus(); };
  }

  /* ---------------- trang bài: mục lục + scrollspy ---------------- */
  var tocBox = document.getElementById("toc");
  if (doc && tocBox) {
    var secs = [].slice.call(doc.querySelectorAll("section"));
    tocBox.innerHTML = secs.map(function (s) {
      var h = s.querySelector(".sh h2"), n = s.querySelector(".sh b");
      if (!h) return "";
      var subs = [].slice.call(s.querySelectorAll(".subsec")).map(function (u) {
        var t = u.querySelector("h3.ssh"), k = t && t.querySelector("b");
        if (!t) return "";
        return '<a class="sub" href="#' + u.id + '"><span>' + (k ? k.textContent : "") + "</span>" +
          t.textContent.replace(k ? k.textContent : "", "") + "</a>";
      }).join("");
      return '<a href="#' + s.id + '"><span>' + (n ? n.textContent : "") + "</span>" + h.textContent + "</a>" + subs;
    }).join("");

    /* scrollspy: the reading line sits 22% down the viewport; the last section or subsection whose top has
       passed it is the one being read. A subsection lights up itself and, softer, its parent section. */
    var links = [].slice.call(tocBox.querySelectorAll("a"));
    var targets = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    function spy() {
      var line = innerHeight * 0.22, cur = -1;
      targets.forEach(function (t, j) { if (t && t.getBoundingClientRect().top <= line) cur = j; });
      if (cur < 0) cur = 0;
      var par = cur;
      while (par > 0 && links[par].classList.contains("sub")) par--;
      links.forEach(function (l, j) {
        l.classList.toggle("on", j === cur);
        l.classList.toggle("in", j === par && par !== cur);
      });
    }
    var spyQ = false;
    addEventListener("scroll", function () {
      if (spyQ) return; spyQ = true;
      requestAnimationFrame(function () { spyQ = false; spy(); });
    }, { passive: true });
    addEventListener("resize", spy);
    spy();
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
      (p ? '<a href="' + BASE + p.book.path + '"><span>previous · ' + esc(p.cat.name) + "</span><b>" + esc(p.book.title) + "</b></a>" : "") +
      (n ? '<a href="' + BASE + n.book.path + '"><span>next · ' + esc(n.cat.name) + "</span><b>" + esc(n.book.title) + "</b></a>" : "");
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
      "<h2>Results for <em>" + esc(q) + "</em></h2><p class=\"cnt\">" + hits.length + " sections</p>" +
      (hits.length
        ? hits.map(function (e) {
            return '<a class="hit" href="' + BASE + e.u + '"><div class="src">' + esc(e.b) + " · section " + esc(e.n) + "</div>" +
              "<h3>" + esc(e.t) + "</h3><p>" + snippet(e.x, q) + "</p></a>";
          }).join("")
        : '<div class="empty-res">No matching sections. Try a shorter keyword.</div>');
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
   - mở/đóng toàn bộ phần hỏi đáp để tự kiểm tra
   - phím tắt j / k
   ============================================================ */
(function () {
  var BASE = document.documentElement.getAttribute("data-base") || "";
  var CAT = window.CATALOG || [];
  var doc = document.querySelector(".doc");
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---------------- thanh tiến độ đọc ---------------- */
  var prog = document.createElement("div");
  prog.id = "prog";
  document.body.appendChild(prog);

  var tocLinks = [].slice.call(document.querySelectorAll("#toc a:not(.sub)"));
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
    prog.style.transform = "scaleX(" + (max > 0 ? Math.min(1, h.scrollTop / max) : 0) + ")";

    var passed = 0;
    secs.forEach(function (s, i) {
      if (!s) return;
      var seen = s.getBoundingClientRect().top < h.clientHeight * 0.4;
      tocLinks[i].classList.toggle("seen", seen);
      if (seen) passed = i + 1;
    });
    var txt = "Contents<b>" + String(passed).padStart(2, "0") + " / " + secs.length + "</b>";
    if (head.innerHTML !== txt) head.innerHTML = txt;
  }
  var pend = false;
  window.addEventListener("scroll", function () {
    if (pend) return; pend = true;
    requestAnimationFrame(function () { pend = false; onScroll(); });
  }, { passive: true });
  onScroll();

  /* ---------------- mở / đóng toàn bộ hỏi đáp ---------------- */
  [].slice.call(doc.querySelectorAll("section")).forEach(function (sec) {
    var qa = [].slice.call(sec.querySelectorAll("details.qa"));
    if (qa.length < 2) return;
    var sh = sec.querySelector(".sh");
    if (!sh) return;
    var b = document.createElement("button");
    b.className = "tool";
    b.textContent = "expand all";
    b.onclick = function () {
      var open = qa.some(function (d) { return !d.open });
      qa.forEach(function (d) { d.open = open; });
      b.textContent = open ? "collapse all" : "expand all";
    };
    sh.appendChild(b);

    /* cùng bộ câu hỏi này còn nằm trong trang ôn tập, ở dạng thẻ lật */
    var me = null;
    CAT.forEach(function (c) { c.groups.forEach(function (g) { g.books.forEach(function (bk) {
      if (bk.slug === doc.id.replace("art-", "")) me = bk; }); }); });
    if (me) {
      var a = document.createElement("a");
      a.className = "tool";
      a.href = BASE + "quiz.html?b=" + encodeURIComponent(me.path);
      a.textContent = "review as flashcards";
      sh.appendChild(a);
    }
  });

  /* thứ tự đọc đúng phải là: hết bài → bài kế → dòng chân trang.
     Trong file bài, <footer> nằm trong <article> nên phải đẩy nó xuống cuối. */
  var np = document.getElementById("np");
  var ft = doc.querySelector("footer");
  if (ft && np && np.parentNode) np.parentNode.appendChild(ft);

  /* ---------------- phím tắt ---------------- */
  var hint = document.createElement("p");
  hint.className = "hint";
  hint.innerHTML = "<kbd>j</kbd>next section &nbsp; <kbd>k</kbd>previous<br><kbd>/</kbd>search";
  var nav = document.querySelector("nav.toc");
  if (nav) nav.appendChild(hint);

  document.addEventListener("keydown", function (e) {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" || e.metaKey || e.ctrlKey) return;
    if (e.key !== "j" && e.key !== "k") return;
    e.preventDefault();
    var cur = 0;
    secs.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < 90) cur = i; });
    var to = secs[Math.max(0, Math.min(secs.length - 1, cur + (e.key === "j" ? 1 : -1)))];
    if (to) to.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
