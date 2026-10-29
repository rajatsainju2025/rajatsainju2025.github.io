# rajatsainju2025.github.io

Source for my personal website, served by GitHub Pages at
https://rajatsainju2025.github.io.

It is a plain static site: no framework and no build step.

## Editing

All content is in [`assets/js/data.js`](assets/js/data.js):

- `SITE`: name, title, bio, email, location, CV and social links. An empty
  string hides that item.
- `NEWS`: the scrolling news cards, newest first. Each card uses an `image`,
  or an `emoji` with a `tint` (violet, amber, teal, rose, sky, slate, lime).
- `PROJECTS`: papers, each with a thumbnail `image` or a text `card`, a TLDR
  and links. `s2` is the Semantic Scholar paper ID used for the live citation
  count.
- `ABSTRACTS`: conference abstracts, shown in a collapsed list.
- `SOFTWARE`: repository cards. Stars and forks are fetched live from GitHub.

Push to `main` and the site updates within a minute or two.

## Previewing locally

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Layout

```
index.html            page shell
assets/css/style.css  styles
assets/js/data.js     content
assets/js/main.js     renders the content
assets/img/           thumbnails (figures from the papers)
```

The layout is modelled on [mattdeitke.com](https://mattdeitke.com/) and was
written from scratch. Paper figures are reproduced from open-access
publications (CC BY 4.0).

After editing `data.js`, `main.js` or `style.css`, bump the `?v=` tag on its
`<link>`/`<script>` line in `index.html` so browsers fetch the new version.
