# rajatsainju2025.github.io

Source for my personal website, served by GitHub Pages at
https://rajatsainju2025.github.io.

This branch (`feature/editorial-dataviz`) tries an editorial design: the site
reads as an illustrated story in three chapters, with interactive charts built
from the papers' own numbers. The brief behind it is in
[`docs/DESIGN_BRIEF.md`](docs/DESIGN_BRIEF.md).

It is a plain static site: no framework and no build step. Fonts are
self-hosted, so the page works without third-party requests (only the live
citation and star counts call out).

## Editing

- [`assets/js/data.js`](assets/js/data.js): profile, news, papers, abstracts
  and software, exactly as on `main`. The paper index, the dispatches, the
  software list and the co-author network are all generated from it.
- [`assets/js/story.js`](assets/js/story.js): the numbers behind the story's
  charts, each copied from a paper and labelled with its source, plus the
  theme (vision, materials, language) and field (fission, fusion) of each
  paper.
- [`index.html`](index.html): the story text itself.

A new paper in `data.js` shows up everywhere automatically. Give it a theme in
`PAPER_THEME` (and a field in `PAPER_FIELD` if it is nuclear work) and a short
label in `PAPER_SHORT`.

## Illustrations

Every painting comes from one pipeline, so they share a hand:

```bash
pip install opencv-python-headless playwright
python tools/scenes.py              # flat SVG scenes -> Chromium -> watercolor
python tools/scenes.py tokamak      # just one scene
python tools/watercolor.py photo.jpg out.jpg --seed 3   # any image
```

`tools/scenes.py` draws each scene as flat SVG shapes and renders it with
Chromium. `tools/watercolor.py` then paints it: edge-preserving smoothing and
colour quantization for flat washes, a noise field that wobbles every edge,
darkened wet edges, granulation and blooms, subtractive glazing onto warm
paper, a faint pencil under-drawing, and a deckled border. If Playwright's
bundled Chromium is missing, point `CHROMIUM` at a Chrome binary.

The news thumbnails in `assets/img/wc/news_*.jpg` are the originals run
through the same filter; the page falls back to the original if one is
missing.

## Previewing locally

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Layout

```
index.html               the story
assets/css/editorial.css styles
assets/js/data.js        content shared with main
assets/js/story.js       chart data from the papers
assets/js/editorial.js   renders charts, simulations, network and lists
assets/img/wc/           watercolor illustrations
assets/img/              paper figures and original news art
assets/fonts/            Newsreader and Libre Franklin (SIL Open Font License)
tools/                   illustration pipeline
docs/DESIGN_BRIEF.md     the design brief
```

Paper figures are reproduced from open-access publications (CC BY 4.0).
