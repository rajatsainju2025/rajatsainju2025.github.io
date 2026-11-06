# Run after editing assets/js/data.js, main.js or style.css:
#     python tools/prerender.py            (needs: pip install playwright)
"""Bake the page content into index.html so it is plain HTML for search engines.

main.js renders the page from data.js. This script opens the site in Chromium,
lets main.js render, and saves the result back to index.html. main.js still runs
in the browser and re-renders the same content, so the page and the HTML never
disagree for visitors. The script also:
  - refreshes the saved citation counts (CITES in data.js) from Semantic Scholar,
    keeping the old numbers if it does not answer,
  - sets each ?v= cache-busting tag to a hash of that file, and
  - sets <lastmod> in sitemap.xml to today.
"""
import datetime, functools, hashlib, http.server, json, pathlib, re, threading, urllib.request
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ["assets/css/style.css", "assets/js/data.js", "assets/js/main.js"]


def refresh_citations():
    data_js = ROOT / "assets/js/data.js"
    text = data_js.read_text(encoding="utf-8")
    ids = list(dict.fromkeys(re.findall(r'\bs2:\s*"([^"]+)"', text)))
    block = re.search(r"// CITES-START\nconst CITES = (\{.*?\});[^\n]*\n// CITES-END", text, re.S)
    saved = json.loads(re.sub(r",\s*}", "}", block.group(1)))
    try:
        req = urllib.request.Request(
            "https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount",
            data=json.dumps({"ids": ids}).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            live = json.load(r)
    except Exception as e:  # busy, rate-limited or offline
        print("citations: kept saved counts (Semantic Scholar did not answer:", e, ")")
        return
    for i, paper in zip(ids, live):
        if paper and paper.get("citationCount"):
            saved[i] = paper["citationCount"]
    body = ",\n".join(f'  "{k}": {v}' for k, v in saved.items())
    today = datetime.date.today().isoformat()
    new = f"// CITES-START\nconst CITES = {{\n{body},\n}};  // updated {today}\n// CITES-END"
    data_js.write_text(text[:block.start()] + new + text[block.end():], encoding="utf-8")
    print("citations: refreshed", len(saved), "counts")


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def render(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        # Only load the site itself: live citation counts and star counts stay out of the HTML.
        page.route("**/*", lambda r: r.continue_() if r.request.url.startswith(url) else r.abort())
        page.goto(url + "index.html", wait_until="domcontentloaded")
        page.wait_for_function("document.querySelectorAll('#projects .project').length > 0")
        html = page.evaluate("""() => {
            document.querySelectorAll('.lightbox').forEach((el) => el.remove());
            const b = document.body;   // keep trailing whitespace stable across runs
            while (b.lastChild && b.lastChild.nodeType === 3 && !b.lastChild.textContent.trim()) b.lastChild.remove();
            b.appendChild(document.createTextNode('\\n'));
            return '<!doctype html>\\n' + document.documentElement.outerHTML + '\\n';
        }""")
        browser.close()
    return html


def main():
    refresh_citations()
    srv = serve()
    try:
        html = render(f"http://127.0.0.1:{srv.server_address[1]}/")
    finally:
        srv.shutdown()
    for asset in ASSETS:
        tag = hashlib.sha1((ROOT / asset).read_bytes()).hexdigest()[:8]
        html, n = re.subn(re.escape(asset) + r"\?v=[\w.-]+", f"{asset}?v={tag}", html)
        assert n == 1, f"expected one reference to {asset}"
    (ROOT / "index.html").write_text(html, encoding="utf-8")

    sitemap = ROOT / "sitemap.xml"
    today = datetime.date.today().isoformat()
    sitemap.write_text(re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{today}</lastmod>", sitemap.read_text()))
    print("index.html prerendered;", "sitemap lastmod", today)


if __name__ == "__main__":
    main()
