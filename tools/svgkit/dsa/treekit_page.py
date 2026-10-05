"""Splice generated figures into a lesson page (tree-bst-traversal, trie, union-find).

build(page, figs_json, art_attrs, hero, sections, footer)
  sections = [(h2, key, [(h3, skey_html, fig_key, sig_html or None, probs_html or None), ...]), ...]
Everything between <article ...> and </article> is regenerated; <head>, topbar, toc and the
scripts at the bottom are kept, except <script src="lab.js">, which is removed.
"""
import re, json

REPLAY = '''<script>
/* Figures start when first scrolled into view, play once and hold the last frame. Click a figure to replay. */
(function () {
  if (!window.IntersectionObserver || !document.getAnimations) return;
  var svgs = [].slice.call(document.querySelectorAll("figure svg[data-anim]"));
  if (!svgs.length) return;
  function anims(s) {
    return document.getAnimations().filter(function (a) { var t = a.effect && a.effect.target; return t && s.contains(t); });
  }
  function restart(s) { anims(s).forEach(function (a) { a.currentTime = 0; a.play(); }); }
  svgs.forEach(function (s) { anims(s).forEach(function (a) { a.pause(); a.currentTime = 0; }); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting || e.target.__played) return;
      e.target.__played = true; restart(e.target); io.unobserve(e.target);
    });
  }, { threshold: 0.4 });
  svgs.forEach(function (s) {
    io.observe(s); s.style.cursor = "pointer";
    s.addEventListener("click", function () { restart(s); });
  });
})();
</script>'''


def probs_of(html):
    """all <div class="probs">…</div> blocks of the original page, in order."""
    return re.findall(r'<div class="probs">.*?</div>', html, re.S)


def build(page, figs_json, art_open, hero, slug, sections, footer, orig=None):
    s = open(page).read()
    figs = json.load(open(figs_json))
    out = [art_open, hero]
    for si, (h2, key, subs) in enumerate(sections, 1):
        out.append('\n<section id="%s-s%d" class="lesson">\n  <div class="sh"><b>%02d</b><h2>%s</h2></div>\n  <p class="key">%s</p>' % (slug, si, si, h2, key))
        for ji, (h3, skey, fk, sig, probs) in enumerate(subs, 1):
            out.append('  <div class="subsec" id="%s-s%d-%d">\n    <h3 class="ssh"><b>%d.%d</b>%s</h3>\n    <p class="skey">%s</p>\n%s' % (slug, si, ji, si, ji, h3, skey, figs[fk]))
            if sig: out.append('    <p class="sig">Signals: %s</p>' % sig)
            if probs: out.append('    ' + probs)
            out.append('  </div>')
        out.append('</section>')
    out.append('\n' + REPLAY + '\n\n<footer>%s</footer>\n\n      ' % footer)
    a = s.index('<article'); b = s.index('</article>')
    s = s[:a] + '\n'.join(out) + s[b:]
    s = s.replace('<script src="lab.js"></script>\n', '')
    open(page, 'w').write(s)
