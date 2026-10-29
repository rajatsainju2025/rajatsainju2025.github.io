# Design brief: an editorial, data-driven personal site

This is the prompt behind the `feature/editorial-dataviz` branch. It rewrites
a prompt originally written for narrating a podcast episode, aimed instead at
this website.

---

Redesign my personal website as an illustrated, interactive story of my
research. It should read like a long-form feature from The New Yorker or a
New York Times data story, and work like a good portfolio.

**The story to tell.** Narrate one arc in three chapters:

1. *Seeing materials change.* In-situ electron microscopy of oxidation,
   reduction and irradiation, at the scale of single nanoparticles.
2. *Teaching computers to see.* Deep learning that segments and tracks
   defects in microscopy images and videos (DefectSegNet, DefectTrack).
3. *Machines that read the facility.* LLM systems, retrieval and agents
   that help run the Advanced Photon Source (APS-RAG, agents in production).

In each chapter, pull out the one or two insights a curious reader should
leave with, and say them plainly, like pull quotes. Then make the reader *feel*
the idea through an interactive explainer.

**Data visualization.** Use only real data: my publications, co-authors,
venues, live citation counts (Semantic Scholar) and repository stats (GitHub).
Good candidates are a research timeline that shows how the themes shifted, a
co-author network, and a filterable publication index. Method explainers may
use simulated data (for example, a tracker following defects in a synthetic
microscope video), but label every simulation clearly. Never invent numbers,
results or quotes.

**Illustration.** Add watercolor illustrations throughout, made with an
OpenCV pipeline (edge-preserving smoothing, pigment pooling, darkened wet
edges, granulation, paper grain, deckled edges) so they share one hand. Where
possible, include historical photos (the first electron microscope, Chicago
Pile-1 and the founding of Argonne, early synchrotrons), watercolorized, from
public-domain sources, each with a credit line.

**Process.** Design it first on a Claude Design canvas: a style sheet
(type, color, illustration, chart grammar) and the full page. Then build it.
Screenshot it at desktop and phone widths, critique it honestly, and iterate
until it is something to be proud of.

**Constraints.**

- Static site on GitHub Pages: no server, no build step, no frameworks.
  Libraries and fonts are vendored so the site works on its own.
- All content still lives in `assets/js/data.js`, so editing stays simple.
- Accessible: readable contrast, keyboard-friendly controls, alt text,
  `prefers-reduced-motion` respected.
- Fast and mobile-first: every section works at phone width.
- Better than the inspiration (mattdeitke.com): not just a list of papers,
  but an argument about what the work means.
