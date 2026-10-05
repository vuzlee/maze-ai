/* Lab hash map — insert keys one by one, watch collisions and resizes. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("hmlab")) return;

  var keys, i, size, slots, used, collisions, resizes, log, timer = null, lastIx = -1, probed = [];

  function h(s) {                       /* a tiny hash function, spreads well enough for the lab */
    var v = 0;
    for (var k = 0; k < s.length; k++) v = (v * 131 + s.charCodeAt(k)) >>> 0;
    return v;
  }

  function build() {
    stopAuto();
    keys = (el("hkeys").value || "").trim().split(/\s+/).filter(Boolean).slice(0, 14);
    i = 0; size = 8; slots = new Array(size).fill(null);
    used = 0; collisions = 0; resizes = 0; log = []; lastIx = -1; probed = [];
    draw();
  }

  function insert(key) {
    var ix = h(key) % size, hops = 0;
    probed = [];
    while (slots[ix] !== null && slots[ix] !== key) {
      probed.push(ix);
      collisions++; hops++;
      ix = (ix + 1) % size;                 /* linear probing so it is easy to see */
    }
    var fresh = slots[ix] === null;
    slots[ix] = key;
    if (fresh) used++;
    lastIx = ix;
    return { ix: ix, hops: hops };
  }

  function grow() {
    var old = slots;
    size *= 2; slots = new Array(size).fill(null); used = 0; resizes++;
    old.forEach(function (k) { if (k !== null) { var ix = h(k) % size; while (slots[ix] !== null) ix = (ix + 1) % size; slots[ix] = k; used++; } });
    probed = []; lastIx = -1;
    log.unshift(["resize", size / 2 + " → " + size + " slots", "rehash " + used + " keys"]);
  }

  function step() {
    if (i >= keys.length) return;
    var key = keys[i++];
    var r = insert(key);
    log.unshift([key, "slot " + r.ix, r.hops ? "probed " + r.hops + " more" : "direct hit"]);
    if (used * 3 > size * 2) grow();       /* Python resizes once past 2/3 full */
    draw();
  }

  function draw() {
    var h2 = '<div class="strip">';
    slots.forEach(function (k, ix) {
      var cls = k === null ? "" : (ix === lastIx ? " on" : " t");
      if (probed.indexOf(ix) >= 0) cls = " f";
      h2 += '<div class="c' + cls + '"><i>' + ix + "</i><b>" + (k === null ? "·" : k) + "</b></div>";
    });
    el("hmview").innerHTML = h2 + "</div>";

    el("hmlf").textContent = used + " / " + size + " (" + Math.round(100 * used / size) + "%)";
    el("hmcol").textContent = collisions;
    el("hmres").textContent = resizes;
    el("hmlog").innerHTML = log.slice(0, 6).map(function (r) {
      return "<div><span>" + r[0] + "</span><span>" + r[1] + "</span><span>" + r[2] + "</span></div>";
    }).join("");
  }

  function stopAuto() { if (timer) { clearInterval(timer); timer = null; el("hmauto").textContent = "Auto run"; } }
  el("hmstep").onclick = function () { stopAuto(); step(); };
  el("hmauto").onclick = function () {
    if (timer) { stopAuto(); return; }
    el("hmauto").textContent = "Stop";
    timer = setInterval(function () { if (i >= keys.length) { stopAuto(); return; } step(); }, 700);
  };
  el("hmrst").onclick = build;
  el("hkeys").addEventListener("change", build);

  build();
})();
