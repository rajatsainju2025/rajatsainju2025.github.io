// Renders the editorial page from data.js and story.js. No framework, no build step.

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const INK = "#1F1D1A", INK3 = "#5B554C", RULE = "#E3DACB", FAINT = "#A79F92", PAPER = "#F6F1E7";

// "Scientific Reports 2022" or "IPAC'26".
const yearOf = (p) => {
  const full = p.venue.match(/(19|20)\d\d/), short = p.venue.match(/['’](\d\d)\b/);
  return full ? +full[0] : short ? 2000 + +short[1] : 0;
};
const venueLine = (p) => p.venue.replace(/\s*((19|20)\d\d)$/, " · $1").replace(/['’](\d\d)$/, (m, y) => ` · 20${y}`);
// Papers without an entry in story.js are classified from their title.
const themeKey = (p) => PAPER_THEME[p.s2]
  || (/\b(agent|RAG|LLM|language|BERT|transformer|accelerator)/i.test(p.title) ? "language"
    : /deep learning|segmentation|tracking|neural|machine learning|\bAI\b|automated/i.test(p.title) ? "vision" : "materials");
const fieldOf = (p) => PAPER_FIELD[p.s2]
  || (/\bfusion\b|tungsten|plasma/i.test(p.title) ? "fusion" : /irradiat|radiation|neutron|HT-9|nuclear/i.test(p.title) ? "fission" : "");
const themeOf = (p) => THEMES[themeKey(p)];
const shortOf = (p) => PAPER_SHORT[p.s2] || (p.card && p.card.line2) || "";
const citations = {};  // s2 id -> count, filled by loadCitations()

// Small seeded random, so layouts and simulations look the same on every visit.
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

// Charts redraw at their container's width; this keeps text readable on phones.
const redraws = [];
function responsive(el, draw) {
  const run = () => { el.innerHTML = draw(Math.max(280, el.clientWidth)); };
  redraws.push(run);
  run();
}
let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => redraws.forEach((f) => f()), 150);
});

// ---------------------------------------------------------------- tooltip --

const tip = $("tip");
function showTip(html, x, y) {
  tip.innerHTML = html;
  tip.hidden = false;
  const w = tip.offsetWidth, h = tip.offsetHeight;
  tip.style.left = `${clamp(x + 14, 8, window.innerWidth - w - 8)}px`;
  tip.style.top = `${y + h + 24 > window.innerHeight ? y - h - 14 : y + 16}px`;
}
function hideTip() { tip.hidden = true; }
// Hover, keyboard focus and tap all show the same tooltip for an element with data-tip.
function bindTips(root, lookup) {
  const at = (e, t) => {
    const r = t.getBoundingClientRect();
    return e && e.clientX ? [e.clientX, e.clientY] : [r.left + r.width / 2, r.bottom];
  };
  root.addEventListener("pointerover", (e) => {
    const t = e.target.closest("[data-tip]");
    if (t) showTip(lookup(t.dataset.tip), ...at(e, t));
  });
  root.addEventListener("pointermove", (e) => {
    if (!tip.hidden && e.target.closest("[data-tip]")) showTip(tip.innerHTML, e.clientX, e.clientY);
  });
  root.addEventListener("pointerout", (e) => { if (e.target.closest("[data-tip]")) hideTip(); });
  root.addEventListener("focusin", (e) => {
    const t = e.target.closest("[data-tip]");
    if (t) showTip(lookup(t.dataset.tip), ...at(null, t));
  });
  root.addEventListener("focusout", hideTip);
}
document.addEventListener("scroll", hideTip, { passive: true });

// ---------------------------------------------------------------- profile --

const ICON = {
  github: '<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M8 0a8 8 0 0 0-2.53 15.59c.4.07.55-.17.55-.38v-1.33c-2.23.48-2.7-1.07-2.7-1.07-.36-.92-.89-1.17-.89-1.17-.73-.5.06-.49.06-.49.8.06 1.23.83 1.23.83.72 1.22 1.87.87 2.33.66.07-.52.28-.87.5-1.07-1.78-.2-3.65-.89-3.65-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.6 7.6 0 0 1 4 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.28.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48v2.2c0 .21.15.46.55.38A8 8 0 0 0 8 0Z"/></svg>',
  scholar: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3 1 9l11 6 9-4.9V17h2V9L12 3Zm-6.5 9.9V16c0 1.9 2.9 3.5 6.5 3.5s6.5-1.6 6.5-3.5v-3.1L12 16.5l-6.5-3.6Z"/></svg>',
  linkedin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20 2H4a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2ZM8 19H5V9h3v10ZM6.5 7.7a1.7 1.7 0 1 1 0-3.4 1.7 1.7 0 0 1 0 3.4ZM19 19h-3v-5c0-1.2-.4-2-1.5-2-.8 0-1.3.6-1.5 1.1-.1.2-.1.5-.1.8V19h-3V9h3v1.3c.4-.6 1.1-1.5 2.7-1.5 2 0 3.4 1.3 3.4 4V19Z"/></svg>',
  twitter: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.2-8.3L1.8 3h6.4l4.4 5.8L17.8 3Zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5Z"/></svg>',
  mail: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M3 5h18v14H3z M3 6l9 7 9-7"/></svg>',
  pin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
  cv: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M6 2h9l4 4v16H6z M14 2v5h5 M9 12h7 M9 16h7"/></svg>',
};

function renderProfile() {
  if ($("bio")) $("bio").innerHTML = SITE.bio;
  $("year").textContent = new Date().getFullYear();
  const L = SITE.links;
  $("links").innerHTML = [
    [L.github, "GitHub"], [L.scholar, "Google Scholar"], [L.linkedin, "LinkedIn"], [L.twitter, "X"],
    [SITE.email && `mailto:${SITE.email}`, SITE.email], [SITE.cv, "CV"],
  ].filter(([u]) => u).map(([u, label]) => `<li><a href="${u}">${esc(label)}</a></li>`).join("");

  const years = PROJECTS.map(yearOf);
  $("stat-papers").textContent = PROJECTS.length;
  $("stat-years").textContent = `${Math.min(...years)} to ${Math.max(...years)}`;
  $("stat-nuclear").textContent = PROJECTS.filter(fieldOf).length
    + ABSTRACTS.filter((a) => NUCLEAR_ABSTRACT.test(a.title)).length;
  $("stat-coauthors").textContent = people().size - 1;
}

// The About page's profile card, in the spirit of the first version of the site.
function renderAbout() {
  const L = SITE.links;
  $("photo").src = SITE.photo;
  $("photo").alt = `Portrait of ${SITE.name}`;
  $("p-name").textContent = $("about-name").textContent = SITE.name;
  $("p-title").textContent = SITE.title;
  $("about-bio").innerHTML = SITE.bio;
  $("p-icons").innerHTML = [[L.github, "github", "GitHub"], [L.scholar, "scholar", "Google Scholar"],
    [L.linkedin, "linkedin", "LinkedIn"], [L.twitter, "twitter", "X"]]
    .filter(([u]) => u).map(([u, icon, label]) => `<li><a href="${u}" aria-label="${label}" title="${label}">${ICON[icon]}</a></li>`).join("");
  $("p-contact").innerHTML = [
    SITE.email && `<li>${ICON.mail}<a href="mailto:${SITE.email}">${esc(SITE.email)}</a></li>`,
    SITE.location && `<li>${ICON.pin}<span>${esc(SITE.location)}</span></li>`,
    SITE.cv && `<li>${ICON.cv}<span><a href="${SITE.cv}">CV</a>${SITE.cvNote ? ` (${esc(SITE.cvNote)})` : ""}</span></li>`,
  ].filter(Boolean).join("");
}

// News as a row of cards that scrolls sideways, with arrow buttons.
function renderNewsCards() {
  const strip = $("news-cards");
  const img = (src) => `<img src="${src.replace("assets/img/", "assets/img/wc/")}" data-orig="${src}" alt="" loading="lazy">`;
  strip.innerHTML = NEWS.map((n) => `<li>${n.image ? img(n.image) : `<span class="news-tile">${n.emoji || ""}</span>`}<p>${n.text}</p><time>${esc(n.date)}</time></li>`).join("");
  strip.querySelectorAll("img").forEach((el) => el.addEventListener("error", () => { el.src = el.dataset.orig; }, { once: true }));
  const left = $("news-left"), right = $("news-right");
  const update = () => {
    left.hidden = strip.scrollLeft < 8;
    right.hidden = strip.scrollLeft + strip.clientWidth > strip.scrollWidth - 8;
  };
  const by = (dir) => strip.scrollBy({ left: dir * strip.clientWidth * 0.8, behavior: REDUCED ? "auto" : "smooth" });
  left.addEventListener("click", () => by(-1));
  right.addEventListener("click", () => by(1));
  strip.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
}

// Co-authors, merging spelling variants such as "Michael Prince" and "Michael H. Prince".
function personKey(name) {
  const parts = name.replace(/\./g, " ").trim().split(/\s+/);
  return `${parts[parts.length - 1].toLowerCase()}|${parts[0][0].toLowerCase()}`;
}
let peopleCache;
function people() {
  if (peopleCache) return peopleCache;
  peopleCache = new Map();
  PROJECTS.forEach((p, i) => p.authors.forEach((a) => {
    const k = personKey(a);
    const v = peopleCache.get(k) || { name: a, papers: [] };
    if (a.length > v.name.length) v.name = a;
    if (!v.papers.includes(i)) v.papers.push(i);
    peopleCache.set(k, v);
  }));
  return peopleCache;
}

// --------------------------------------------------- Ni critical thickness --

const PBR = 1.65;  // NiO / Ni volume ratio (Pilling–Bedworth), for the drawing only
function renderNi() {
  const svg = $("ni-svg"), slider = $("ni-radius"), out = $("ni-radius-out");
  const stage = $("ni-stage"), outcome = $("ni-outcome"), play = $("ni-play");
  const h = NI_OXIDATION.criticalNm, err = NI_OXIDATION.criticalErrNm;
  const K = 4, CX = 200, CY = 138;  // 4 px per nm
  let anim = null;

  function geometry(r, t) {
    const hollow = r > h;
    const s1 = clamp(hollow ? t / 0.4 : t);
    const s2 = hollow ? clamp((t - 0.4) / 0.6) : 0;
    let core, cavity, outer;
    if (!hollow || s2 === 0) {
      core = r - Math.min(h, r) * s1;
      cavity = core;
      outer = Math.cbrt(core ** 3 + PBR * (r ** 3 - core ** 3));
    } else {
      cavity = r - h;
      core = cavity * Math.cbrt(1 - s2);
      outer = Math.cbrt(cavity ** 3 + PBR * (r ** 3 - core ** 3));
    }
    return { hollow, s1, s2, core, cavity, outer, large: r >= 20 };
  }

  function draw(t) {
    const r = +slider.value, g = geometry(r, t);
    // Large particles: the shell thickens faster on one side, so the cavity drifts off-centre.
    const drift = g.large ? (g.outer - g.cavity) * 0.45 * g.s2 : 0;
    const vx = CX + drift * K * 0.7, vy = CY - drift * K * 0.7;
    // The nickel core stays in contact with the shell on the slow side.
    const coreOff = g.large ? (g.cavity - g.core) : 0;
    const nx = vx - coreOff * K * 0.7, ny = vy + coreOff * K * 0.7;
    const parts = [
      `<circle cx="${CX}" cy="${CY}" r="${g.outer * K}" fill="#B4532A"/>`,
      g.s1 > 0 || g.s2 > 0 ? `<circle cx="${vx}" cy="${vy}" r="${g.cavity * K}" fill="${PAPER}" stroke="#29A3A3" stroke-width="${g.s2 > 0 ? 2 : 0}" stroke-dasharray="4 3"/>` : "",
      g.core > 0.05 ? `<circle cx="${g.s2 > 0 ? nx : CX}" cy="${g.s2 > 0 ? ny : CY}" r="${g.core * K}" fill="#9DB39A"/>` : "",
      `<circle cx="${CX}" cy="${CY}" r="${r * K}" fill="none" stroke="${INK}" stroke-width="1" stroke-dasharray="2 4" opacity=".55"/>`,
      r > h ? `<circle cx="${CX}" cy="${CY}" r="${(r - h) * K}" fill="none" stroke="${INK}" stroke-width="1.5" stroke-dasharray="6 4"/>` : "",
      // Uncertainty of the critical thickness, as a faint band.
      r > h - err ? `<circle cx="${CX}" cy="${CY}" r="${Math.max(0, r - h) * K}" fill="none" stroke="${INK}" stroke-opacity=".08" stroke-width="${err * 2 * K}"/>` : "",
    ];
    const legend = [["#9DB39A", "Ni metal"], ["#B4532A", "NiO oxide"], [PAPER, "void"]]
      .map(([c, l], i) => `<g transform="translate(${20 + i * 104} 286)"><rect width="14" height="14" y="-11" fill="${c}" stroke="${i === 2 ? "#29A3A3" : "none"}" stroke-dasharray="3 2"/><text x="20" font-size="13" fill="${INK3}">${l}</text></g>`)
      .join("");
    const bar = `<g transform="translate(330 270)"><line x1="0" x2="${10 * K}" stroke="${INK}" stroke-width="3"/><text x="${5 * K}" y="16" font-size="12" text-anchor="middle" fill="${INK3}">10 nm</text></g>`;
    svg.innerHTML = parts.join("") + legend + bar;
  }

  function describe() {
    const r = +slider.value;
    out.textContent = `${r} nm`;
    let text;
    if (r < h - err) {
      text = `A radius of ${r} nm is below the critical thickness, so stage one consumes all the nickel. It ends as a solid NiO sphere. Small particles in the study finished in ${NI_OXIDATION.smallDuration}.`;
    } else if (r <= h + err) {
      text = `A radius of ${r} nm sits within the ±${err} nm uncertainty of the critical thickness. It could end solid, or with a small void.`;
    } else if (r < 20) {
      text = `A radius of ${r} nm is larger than the critical thickness. Kirkendall voids open at the metal–oxide interface (after ${NI_OXIDATION.mediumVoids} for medium particles in the study) and merge into a centred void: a hollow shell.`;
    } else {
      text = `Like the study's large particles (${NI_OXIDATION.largeDiameterNm} nm across): a primary void opens after ${NI_OXIDATION.largeVoids} and grows off-centre as the shell thickens faster on one side. An asymmetric hollow shell.`;
    }
    outcome.textContent = text;
  }

  function animate() {
    cancelAnimationFrame(anim);
    const r = +slider.value, dur = r > h ? 4200 : 2200, t0 = performance.now();
    play.disabled = true;
    const step = (now) => {
      const t = clamp((now - t0) / dur);
      draw(t);
      const g = geometry(r, t);
      stage.textContent = t >= 1 ? "Done." : g.s2 > 0
        ? "Stage 2 · Ni²⁺ diffuses out through the oxide; vacancies gather into a void (Wagner)."
        : "Stage 1 · Oxide nucleates and eats inward (Avrami–Erofeev).";
      if (t < 1) anim = requestAnimationFrame(step); else play.disabled = false;
    };
    anim = requestAnimationFrame(step);
  }

  slider.addEventListener("input", () => { cancelAnimationFrame(anim); play.disabled = false; stage.textContent = ""; describe(); draw(1); });
  play.addEventListener("click", () => (REDUCED ? draw(1) : animate()));
  describe();
  draw(1);
}

// ------------------------------------------------------- W nanofuzz bars --

function renderW() {
  $("w-kp400").textContent = `${W_NANOFUZZ.kp400} µg² cm⁻⁴ min⁻¹`;
  responsive($("w-bars"), (w) => {
    const lab = w < 480 ? 96 : 120, bw = w - lab - 4, small = bw / W_NANOFUZZ.slowerAt500;
    return `<svg viewBox="0 0 ${w} 110" role="img" aria-label="Pristine tungsten oxidizes about seven times faster than tungsten nanofuzz at 500 degrees Celsius">
      <text x="0" y="29" font-size="14" fill="${INK}">Pristine W</text>
      <rect x="${lab}" y="12" width="${bw}" height="26" fill="${INK3}"/>
      <text x="${lab + 10}" y="30" font-size="13" fill="#fff">≈ ${W_NANOFUZZ.slowerAt500}× faster</text>
      <text x="0" y="85" font-size="14" font-weight="600" fill="${INK}">W nanofuzz</text>
      <rect x="${lab}" y="68" width="${small}" height="26" fill="#B4532A"/>
      <text x="${lab + small + 8}" y="86" font-size="13" fill="${INK}">${W_NANOFUZZ.kp500} µg² cm⁻⁴ min⁻¹</text>
    </svg>`;
  });
}

// ----------------------------------------------------- tracker simulation --

function renderTracker() {
  const canvas = $("tracker-canvas"), ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height, F = DEFECTTRACK_FACTS;
  const rand = rng(7), PAL = ["#E4572E", "#F3A712", "#29A3A3", "#9B5DE5", "#4F9D4F", "#F15BB5", "#00BBF9", "#FEE440"];
  const MEAN_FRAMES = 38, BINS = 11, BIN_MS = 100;

  // A few frames of grainy, gently varying background, cycled for shimmer.
  const base = new Float32Array(W * H);
  for (let k = 0; k < 9; k++) {
    const bx = rand() * W, by = rand() * H, br = 90 + rand() * 160, amp = (rand() - 0.5) * 34;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const d = ((x - bx) ** 2 + (y - by) ** 2) / (br * br);
      base[y * W + x] += amp * Math.exp(-d);
    }
  }
  const frames = [];
  for (let f = 0; f < 6; f++) {
    const img = ctx.createImageData(W, H);
    for (let i = 0; i < W * H; i++) {
      const v = 136 + base[i] + (rand() + rand() + rand() - 1.5) * 46;
      img.data[i * 4] = img.data[i * 4 + 1] = img.data[i * 4 + 2] = v;
      img.data[i * 4 + 3] = 255;
    }
    frames.push(img);
  }

  let defects = [], nextId = 1, frame = 0, finished = 0, running = !REDUCED, boxes = true, visible = false, last = 0, acc = 0;
  const hist = new Array(BINS).fill(0);

  const spawn = () => {
    const life = Math.max(2, Math.round(-Math.log(1 - rand()) * MEAN_FRAMES));
    defects.push({ id: nextId++, x: 20 + rand() * (W - 40), y: 20 + rand() * (H - 40), age: 0, life, c0: 0.55 + rand() * 0.45, rot: rand() * 6.28 });
  };
  for (let i = 0; i < 22; i++) { spawn(); defects[i].age = Math.floor(rand() * defects[i].life); }

  function step() {
    frame++;
    if (rand() < 0.62) spawn();
    defects.forEach((d) => d.age++);
    defects = defects.filter((d) => {
      if (d.age < d.life) return true;
      hist[Math.min(BINS - 1, Math.floor((d.life * F.msPerFrame) / BIN_MS))]++;
      finished++;
      return false;
    });
    if (finished > 4000) { hist.fill(0); finished = 0; }
  }

  function paint() {
    ctx.putImageData(frames[frame % frames.length], 0, 0);
    defects.forEach((d) => {
      const a = d.c0 * (1 - 0.75 * (d.age / d.life));
      const ox = Math.cos(d.rot) * 2.6, oy = Math.sin(d.rot) * 2.6;
      ctx.fillStyle = `rgba(22,22,24,${a})`;
      ctx.beginPath(); ctx.arc(d.x - ox, d.y - oy, 6.5, 0, 6.29); ctx.fill();
      ctx.fillStyle = `rgba(238,238,238,${a * 0.75})`;
      ctx.beginPath(); ctx.arc(d.x + ox, d.y + oy, 4.5, 0, 6.29); ctx.fill();
      d.missed = a < 0.4 && ((d.id * 31 + frame) % 7) < 3;
    });
    if (boxes) {
      ctx.lineWidth = 2;
      ctx.font = "700 11px 'Libre Franklin', Arial, sans-serif";
      defects.forEach((d) => {
        const c = PAL[d.id % PAL.length];
        ctx.strokeStyle = c;
        ctx.setLineDash(d.missed ? [4, 3] : []);
        ctx.strokeRect(d.x - 11, d.y - 11, 22, 22);
        ctx.fillStyle = c;
        ctx.fillText(d.id, d.x - 11, d.y - 14);
      });
      ctx.setLineDash([]);
    }
    $("tracker-clock").textContent = `${(frame * F.msPerFrame).toLocaleString("en-US", { minimumFractionDigits: 1, maximumFractionDigits: 1 })} ms`;
  }

  function drawHist() {
    const max = Math.max(1, ...hist), bw = 260 / BINS;
    $("tracker-hist").innerHTML = hist.map((n, i) =>
      `<rect x="${i * bw + 1}" y="${126 - (n / max) * 120}" width="${bw - 2}" height="${(n / max) * 120}" fill="#1F6F6B"/>`).join("")
      + `<line x1="0" y1="126.5" x2="260" y2="126.5" stroke="${INK}"/>`
      + `<text x="0" y="144" font-size="11" fill="${INK3}">0</text>`
      + `<text x="${bw * 5}" y="144" font-size="11" fill="${INK3}" text-anchor="middle">0.5 s</text>`
      + `<text x="260" y="144" font-size="11" fill="${INK3}" text-anchor="end">1 s +</text>`;
    $("tracker-count").textContent = `${finished.toLocaleString()} tracks finished`;
  }

  function loop(now) {
    if (running && visible) {
      acc += Math.min(100, now - (last || now));
      let n = 0;
      while (acc >= F.msPerFrame && n < 6) { step(); acc -= F.msPerFrame; n++; }
      if (n) { paint(); if (frame % 12 === 0) drawHist(); }
    }
    last = now;
    requestAnimationFrame(loop);
  }

  $("tracker-play").addEventListener("click", (e) => {
    running = !running;
    e.currentTarget.textContent = running ? "Pause" : "Play";
  });
  $("tracker-boxes").addEventListener("click", (e) => {
    boxes = !boxes;
    e.currentTarget.setAttribute("aria-pressed", boxes);
    e.currentTarget.textContent = boxes ? "Boxes on" : "Boxes off";
    paint();
  });
  $("tracker-play").textContent = running ? "Pause" : "Play";
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);
  for (let i = 0; i < 400; i++) step();  // warm up so the histogram has a shape
  paint();
  drawHist();
  requestAnimationFrame(loop);
}

// ------------------------------------------------------------- KS chart --

function renderKS() {
  const el = $("ks-svg");
  responsive(el, (w) => {
    const lab = w < 520 ? 150 : 210, x0 = lab, x1 = w - 12, rowH = 32, top = 22;
    const xs = (p) => x0 + (p / 0.8) * (x1 - x0);
    const fs = w < 520 ? 12 : 13;
    const rows = DEFECTTRACK_KS.map((r, i) => {
      const y = top + i * rowH + 14;
      const sig = r.p < 0.05;
      const fill = r.model ? "#1F6F6B" : sig ? "#B4532A" : PAPER;
      const stroke = r.model || sig ? "none" : INK;
      return `<text x="0" y="${y + 4}" font-size="${fs}" fill="${INK}" font-weight="${sig ? 600 : 400}">${esc(r.who)}</text>
        <line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" stroke="${RULE}"/>
        <circle cx="${xs(r.p)}" cy="${y}" r="8" fill="${fill}" stroke="${stroke}" stroke-width="2" tabindex="0" data-tip="${i}" role="img" aria-label="${esc(r.who)}: p = ${r.p}"/>
        ${sig ? `<text x="${xs(0.05) + 8}" y="${y + 4}" font-size="12" fill="#B4532A">p = ${r.p}</text>` : ""}`;
    }).join("");
    const bottom = top + DEFECTTRACK_KS.length * rowH + 6;
    const ticks = (w < 520 ? [0, 0.4, 0.8] : [0, 0.2, 0.4, 0.6, 0.8]).map((t) =>
      `<text x="${xs(t)}" y="${bottom + 18}" font-size="12" fill="${INK3}" text-anchor="${t === 0 ? "start" : t === 0.8 ? "end" : "middle"}">${t === 0.8 ? "0.8 p-value" : t}</text>`).join("");
    return `<svg viewBox="0 0 ${w} ${bottom + 26}" role="group" aria-label="p-values of the Kolmogorov–Smirnov test for DefectTrack and four experts">
      <rect x="${x0}" y="0" width="${xs(0.05) - x0}" height="${bottom}" fill="#F3DFD2"/>
      <text x="${xs(0.05) + 4}" y="12" font-size="12" fill="#B4532A">p = 0.05</text>
      <line x1="${xs(0.05)}" x2="${xs(0.05)}" y1="0" y2="${bottom}" stroke="#B4532A"/>
      ${rows}
      <line x1="${x0}" x2="${x1}" y1="${bottom}" y2="${bottom}" stroke="${INK}"/>
      ${ticks}
    </svg>`;
  });
  bindTips(el, (i) => {
    const r = DEFECTTRACK_KS[i];
    return `<b>${esc(r.who)}</b>${r.n.toLocaleString()} defects tracked<br>KS statistic D = ${r.d}<br>p = ${r.p}${r.p < 0.05 ? " · differs from the truth" : " · consistent with the truth"}`;
  });
}

// --------------------------------------------------- DefectSegNet errors --

function segRows() {
  return DEFECTSEGNET.map((m) => {
    const e = (v) => Math.abs(v - m.truth) / m.truth;
    const experts = m.experts.map(e);
    return { what: m.what, model: e(m.model), experts, avg: experts.reduce((a, b) => a + b, 0) / experts.length };
  });
}
function renderSeg() {
  const rows = segRows();
  const wins = rows.filter((r) => r.model < r.avg).length;
  document.querySelector("#seg-chart .g-title").textContent =
    `A segmentation network beat the expert average on ${wins} of ${rows.length} measurements`;
  const el = $("seg-svg");
  responsive(el, (w) => {
    const lab = w < 520 ? 150 : 210, x0 = lab, x1 = w - 40, rowH = 34, top = 8, fs = w < 520 ? 12 : 13;
    const xs = (v) => x0 + clamp(v) * (x1 - x0);
    const body = rows.map((r, i) => {
      const y = top + i * rowH + 14;
      const over = r.experts.filter((v) => v > 1);
      return `<g data-tip="${i}" tabindex="0" role="img" aria-label="${esc(r.what)}: DefectSegNet ${(r.model * 100).toFixed(0)} percent, expert average ${(r.avg * 100).toFixed(0)} percent">
        <rect x="0" y="${y - rowH / 2}" width="${w}" height="${rowH}" fill="transparent"/>
        <text x="0" y="${y + 4}" font-size="${fs}" fill="${INK}">${esc(r.what)}</text>
        <line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" stroke="${RULE}"/>
        ${r.experts.map((v) => `<circle cx="${xs(v)}" cy="${y}" r="4.5" fill="${FAINT}"/>`).join("")}
        ${over.map((v) => `<text x="${x1 + 4}" y="${y + 4}" font-size="11" fill="${INK3}">${Math.round(v * 100)}%→</text>`).join("")}
        <circle cx="${xs(r.avg)}" cy="${y}" r="7.5" fill="none" stroke="${INK}" stroke-width="2"/>
        <circle cx="${xs(r.model)}" cy="${y}" r="7.5" fill="#1F6F6B"/>
      </g>`;
    }).join("");
    const bottom = top + rows.length * rowH + 4;
    const ticks = (w < 520 ? [0, 0.5, 1] : [0, 0.25, 0.5, 0.75, 1]).map((t) =>
      `<text x="${xs(t)}" y="${bottom + 18}" font-size="12" fill="${INK3}" text-anchor="${t === 0 ? "start" : t === 1 ? "end" : "middle"}">${t * 100}%${t === 1 ? " error" : ""}</text>`).join("");
    return `<svg viewBox="0 0 ${w} ${bottom + 26}" role="group" aria-label="Percent error of DefectSegNet and human experts for ten defect measurements">
      ${body}<line x1="${x0}" x2="${x1}" y1="${bottom}" y2="${bottom}" stroke="${INK}"/>${ticks}</svg>`;
  });
  bindTips(el, (i) => {
    const r = rows[i], pct = (v) => `${(v * 100).toFixed(1)}%`;
    return `<b>${esc(r.what)}</b>DefectSegNet: ${pct(r.model)} error<br>Expert average: ${pct(r.avg)}<br>Experts: ${r.experts.map((v) => Math.round(v * 100) + "%").join(", ")}`;
  });
}

// ------------------------------------------------------------------ RAG --

function renderRag() {
  const list = $("rag-steps");
  list.innerHTML = RAG_STEPS.map((s, i) =>
    `<li><button type="button" data-step="${i}" aria-pressed="${i === 1}"><span>STEP ${i + 1}</span>${esc(s.name)}</button></li>`).join("");
  $("rag-sources").innerHTML = RAG_SOURCES.map((s) => `<li>${esc(s)}</li>`).join("");
  const pick = (i) => {
    list.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", +b.dataset.step === i));
    $("rag-text").textContent = RAG_STEPS[i].text;
    document.querySelectorAll("#rag-sources li").forEach((li) => li.classList.toggle("lit", i === 1 || i === 4));
  };
  list.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (b) pick(+b.dataset.step);
  });
  pick(1);
}

// ------------------------------------------------------------- timeline --

function citeRadius(p) {
  const c = citations[p.s2];
  return c == null ? 13 : 9 + Math.sqrt(c) * 2.1;
}
function renderTimeline() {
  const el = $("timeline");
  const years = PROJECTS.map(yearOf).concat(ABSTRACTS.map((a) => a.year));
  const y0 = Math.min(...years), y1 = Math.max(...years);
  responsive(el, (w) => {
    const pad = 30, xs = (y) => pad + ((y - y0) / (y1 - y0)) * (w - 2 * pad);
    const byYear = {};
    PROJECTS.forEach((p, i) => (byYear[yearOf(p)] = byYear[yearOf(p)] || []).push(i));
    const stackH = Math.max(...Object.values(byYear).map((ids) => ids.reduce((s, i) => s + 2 * citeRadius(PROJECTS[i]) + 14, 0)));
    const legendH = w < 640 ? 94 : 34, axis = legendH + stackH + 16;
    let dots = "";
    Object.entries(byYear).forEach(([yr, ids]) => {
      let y = axis - 4;
      ids.forEach((i) => {
        const p = PROJECTS[i], r = citeRadius(p);
        y -= r;
        if (fieldOf(p)) dots += `<circle cx="${xs(+yr)}" cy="${y}" r="${r + 4}" fill="none" stroke="#E0A33A" stroke-width="3"/>`;
        dots += `<circle class="dot" cx="${xs(+yr)}" cy="${y}" r="${r}" fill="${themeOf(p).color}" tabindex="0" data-tip="${i}" role="img" aria-label="${esc(p.title)}, ${yr}"/>`;
        y -= r + 14;
      });
    });
    const abByYear = {};
    ABSTRACTS.forEach((a) => (abByYear[a.year] = (abByYear[a.year] || 0) + 1));
    const rings = Object.entries(abByYear).map(([yr, n]) =>
      Array.from({ length: n }, (_, k) => `<circle cx="${xs(+yr) + (k - (n - 1) / 2) * 15}" cy="${axis + 34}" r="5.5" fill="none" stroke="${FAINT}" stroke-width="2"/>`).join("")).join("");
    const ticks = [];
    for (let y = y0; y <= y1; y++) ticks.push(`<text x="${xs(y)}" y="${axis + 18}" font-size="12" fill="${INK3}" text-anchor="middle">${w < 560 ? "’" + String(y).slice(2) : y}</text>`);
    const items = Object.values(THEMES).map((t) => [`<circle cx="6" cy="-4" r="6" fill="${t.color}"/>`, t.label])
      .concat([[`<circle cx="6" cy="-4" r="7" fill="none" stroke="#E0A33A" stroke-width="3"/>`, "Fission or fusion"]]);
    const leg = items.map(([mark, label], i) => {
      const x = w < 640 ? 0 : [0, 236, 420, 744][i], y = w < 640 ? 16 + i * 20 : 16;
      return `<g transform="translate(${x} ${y})">${mark}<text x="18" font-size="13" fill="${INK}">${label}</text></g>`;
    }).join("");
    return `<svg viewBox="0 0 ${w} ${axis + 48}" role="group" aria-label="Timeline of papers by year and theme">
      ${leg}<line x1="0" x2="${w}" y1="${axis}" y2="${axis}" stroke="${INK}"/>${dots}${ticks.join("")}${rings}</svg>`;
  });
  bindTips(el, (i) => {
    const p = PROJECTS[i], c = citations[p.s2];
    const f = fieldOf(p);
    return `<b>${esc(p.title)}</b>${esc(p.venue)} · ${themeOf(p).short}${f ? ` · ${FIELDS[f].label}` : ""}${c != null ? ` · ${c} citations` : ""}`;
  });
}

// -------------------------------------------------------------- network --

function layoutNetwork() {
  const rand = rng(42), ppl = [...people().values()].filter((v) => v.name !== SITE.me);
  const nodes = [{ kind: "me", x: 0, y: 0, fixed: true }];
  PROJECTS.forEach((p, i) => {
    const a = (i / PROJECTS.length) * Math.PI * 2;
    nodes.push({ kind: "paper", i, x: Math.cos(a) * 160, y: Math.sin(a) * 160 });
  });
  ppl.forEach((v) => {
    const home = nodes[1 + v.papers[0]];
    nodes.push({ kind: "person", v, x: home.x * 1.5 + (rand() - 0.5) * 60, y: home.y * 1.5 + (rand() - 0.5) * 60 });
  });
  const links = [];
  PROJECTS.forEach((_, i) => links.push([0, 1 + i, 170]));
  nodes.forEach((n, k) => {
    if (n.kind !== "person") return;
    n.v.papers.forEach((i) => links.push([k, 1 + i, 34 + Math.sqrt(PROJECTS[i].authors.length) * 6]));
  });
  for (let it = 0, alpha = 1; it < 360; it++, alpha *= 0.988) {
    for (let a = 0; a < nodes.length; a++) for (let b = a + 1; b < nodes.length; b++) {
      const A = nodes[a], B = nodes[b];
      let dx = B.x - A.x, dy = B.y - A.y, d2 = dx * dx + dy * dy + 0.01;
      const s = (A.kind === "person" && B.kind === "person" ? 260 : A.kind === "paper" && B.kind === "paper" ? 9000 : 1400) / d2 * alpha;
      const d = Math.sqrt(d2); dx /= d; dy /= d;
      if (!A.fixed) { A.x -= dx * s; A.y -= dy * s; }
      if (!B.fixed) { B.x += dx * s; B.y += dy * s; }
    }
    links.forEach(([a, b, L]) => {
      const A = nodes[a], B = nodes[b], dx = B.x - A.x, dy = B.y - A.y, d = Math.hypot(dx, dy) || 1;
      const s = ((d - L) / d) * 0.08 * alpha;
      if (!A.fixed) { A.x += dx * s; A.y += dy * s; }
      if (!B.fixed) { B.x -= dx * s; B.y -= dy * s; }
    });
  }
  return { nodes, links };
}
function renderNetwork() {
  const el = $("network"), net = layoutNetwork();
  const xs = net.nodes.map((n) => n.x), ys = net.nodes.map((n) => n.y);
  const bx = [Math.min(...xs), Math.max(...xs)], by = [Math.min(...ys), Math.max(...ys)];
  responsive(el, (w) => {
    const h = w < 600 ? 520 : 600, m = 46;
    const sx = (x) => m + ((x - bx[0]) / (bx[1] - bx[0])) * (w - 2 * m);
    const sy = (y) => m + ((y - by[0]) / (by[1] - by[0])) * (h - 2 * m);
    const lines = net.links.map(([a, b]) => {
      const A = net.nodes[a], B = net.nodes[b];
      const paper = B.i;
      return `<line data-paper="${paper}" data-who="${a}" x1="${sx(A.x)}" y1="${sy(A.y)}" x2="${sx(B.x)}" y2="${sy(B.y)}" stroke="${a === 0 ? "#cfc5b3" : RULE}" stroke-width="${a === 0 ? 1.5 : 1}"/>`;
    }).join("");
    const dots = net.nodes.map((n, k) => {
      if (n.kind === "me") return `<circle cx="${sx(n.x)}" cy="${sy(n.y)}" r="15" fill="${INK}"/><text x="${sx(n.x)}" y="${sy(n.y) + 32}" font-size="13" font-weight="600" text-anchor="middle" fill="${INK}">Rajat</text>`;
      if (n.kind === "paper") {
        const p = PROJECTS[n.i];
        return `<g class="pnode" data-tip="p${n.i}" data-paper="${n.i}" tabindex="0" role="img" aria-label="${esc(p.title)}"><circle cx="${sx(n.x)}" cy="${sy(n.y)}" r="11" fill="${themeOf(p).color}"/>
          ${shortOf(p) ? `<text x="${sx(n.x)}" y="${sy(n.y) - 16}" font-size="12" font-weight="600" text-anchor="middle" fill="${INK}" paint-order="stroke" stroke="${PAPER}" stroke-width="4">${esc(shortOf(p))}</text>` : ""}</g>`;
      }
      const many = n.v.papers.length > 1;
      return `<circle class="person" data-tip="a${k}" data-k="${k}" cx="${sx(n.x)}" cy="${sy(n.y)}" r="${many ? 6 : 4}" fill="${many ? INK3 : FAINT}" tabindex="${many ? 0 : -1}"/>`;
    }).join("");
    return `<svg viewBox="0 0 ${w} ${h}" role="group" aria-label="Network of papers and co-authors">${lines}${dots}</svg>`;
  });
  const highlight = (pred) => el.querySelectorAll("line").forEach((l) => {
    const on = pred(l);
    l.setAttribute("stroke", on ? INK : l.dataset.who === "0" ? "#cfc5b3" : RULE);
    l.setAttribute("stroke-width", on ? 2 : 1);
  });
  el.addEventListener("pointerover", (e) => {
    const t = e.target.closest("[data-tip]");
    if (!t) return;
    const key = t.dataset.tip;
    if (key[0] === "a") highlight((l) => l.dataset.who === key.slice(1));
    else highlight((l) => l.dataset.paper === key.slice(1));
  });
  el.addEventListener("pointerout", () => highlight(() => false));
  bindTips(el, (key) => {
    if (key[0] === "p") { const p = PROJECTS[+key.slice(1)]; return `<b>${esc(p.title)}</b>${esc(p.venue)} · ${p.authors.length} authors`; }
    const n = net.nodes[+key.slice(1)];
    return `<b>${esc(n.v.name)}</b>${n.v.papers.map((i) => esc(shortOf(PROJECTS[i]) || PROJECTS[i].title)).join("<br>")}`;
  });
}

// --------------------------------------------------------------- papers --

const LINK_LABEL = { paper: "Paper", pdf: "PDF", arxiv: "arXiv", github: "Code", data: "Data", website: "Website", demo: "Demo", blog: "Blog" };
function authorsHTML(list, idx) {
  const fmt = (a) => (a === SITE.me ? `<span class="me">${esc(a)}</span>` : esc(a));
  if (list.length <= 12) return list.map(fmt).join(", ");
  const meAt = list.indexOf(SITE.me), shown = list.slice(0, Math.max(8, meAt + 1));
  return `${shown.map(fmt).join(", ")}, <button type="button" data-more="${idx}">and ${list.length - shown.length} more</button>`;
}
function renderIndex() {
  const filters = [["all", "All", INK], ["nuclear", "Fission & fusion", "#8A5A10"], ...Object.entries(THEMES).map(([k, t]) => [k, t.short, t.color])];
  $("filters").innerHTML = filters.map(([k, label, c]) =>
    `<button type="button" data-theme="${k}" aria-pressed="${k === "all"}" style="color:${c}">${label}</button>`).join("");
  const paint = () => $("filters").querySelectorAll("button").forEach((b) => {
    b.style.background = b.getAttribute("aria-pressed") === "true" ? b.style.color : "transparent";
  });
  $("index").innerHTML = PROJECTS.map((p, i) => {
    const t = themeOf(p);
    const media = p.image
      ? `<img class="thumb" src="${p.image}" alt="" loading="lazy">`
      : `<div class="tcard" style="background:${t.color}"><small>${esc(p.card.line1)}</small><span>${esc(p.card.line2)}</span></div>`;
    const href = p.links.paper || p.links.arxiv || p.links.pdf || "#";
    const links = Object.entries(p.links).filter(([, u]) => u)
      .map(([k, u]) => `<a href="${u}">${LINK_LABEL[k] || k}</a>`).join("");
    const field = fieldOf(p);
    return `<li data-theme="${themeKey(p)}" data-nuclear="${field ? "yes" : "no"}">
      <a href="${href}" tabindex="-1" aria-hidden="true">${media}</a>
      <div>
        <h3><a href="${href}" style="color:inherit;text-decoration:none">${esc(p.title)}</a></h3>
        <p class="authors" id="authors-${i}">${authorsHTML(p.authors, i)}</p>
        <p class="meta"><span class="venue">${esc(venueLine(p))}</span><span class="theme-tag" style="color:${t.color}">${t.short}</span>${field ? `<span class="theme-tag field-tag">${FIELDS[field].label}</span>` : ""}<span class="cites" data-s2="${p.s2}"></span></p>
        <p class="tldr">${p.tldr}</p>
        <p class="meta links">${links}${p.s2 && !p.s2.startsWith("DOI:") ? `<a href="https://www.semanticscholar.org/paper/${p.s2}">Semantic Scholar</a>` : ""}</p>
      </div>
    </li>`;
  }).join("");
  $("index").addEventListener("click", (e) => {
    const b = e.target.closest("[data-more]");
    if (!b) return;
    const p = PROJECTS[b.dataset.more];
    $(`authors-${b.dataset.more}`).innerHTML = p.authors.map((a) => (a === SITE.me ? `<span class="me">${esc(a)}</span>` : esc(a))).join(", ");
  });
  // Paging: the newest PAGE papers first, then PAGE more at a time, or all at once.
  const PAGE = 5;
  let filter = "all", shown = PAGE;
  const matches = (li) => filter === "all" || (filter === "nuclear" ? li.dataset.nuclear === "yes" : li.dataset.theme === filter);
  function apply(focusFrom) {
    const rows = [...document.querySelectorAll("#index li")].filter(matches);
    document.querySelectorAll("#index li").forEach((li) => { li.hidden = true; });
    rows.forEach((li, i) => { li.hidden = i >= shown; });
    const n = rows.length, visible = Math.min(shown, n);
    const buttons = [];
    if (visible < n) {
      buttons.push(`<button type="button" class="btn ghost" data-page="next">Show next ${Math.min(PAGE, n - visible)}</button>`);
      buttons.push(`<button type="button" class="btn" data-page="all">Show all ${n}</button>`);
    } else if (n > PAGE) {
      buttons.push(`<button type="button" class="btn ghost" data-page="fewer">Show fewer</button>`);
    }
    $("pager").innerHTML = `<p class="pager-count" aria-live="polite">Showing ${visible} of ${n} papers</p><div class="btn-row">${buttons.join("")}</div>`;
    if (focusFrom != null && rows[focusFrom]) rows[focusFrom].querySelector("h3 a").focus();
  }
  $("pager").addEventListener("click", (e) => {
    const b = e.target.closest("[data-page]");
    if (!b) return;
    const before = shown;
    if (b.dataset.page === "next") shown += PAGE;
    if (b.dataset.page === "all") shown = Infinity;
    if (b.dataset.page === "fewer") { shown = PAGE; $("papers").scrollIntoView({ behavior: REDUCED ? "auto" : "smooth" }); }
    apply(b.dataset.page === "fewer" ? null : before);
  });
  $("filters").addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    $("filters").querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", x === b));
    paint();
    filter = b.dataset.theme;
    shown = PAGE;
    apply();
  });
  paint();
  apply();
  $("abstracts").innerHTML = ABSTRACTS.map((a) => `<li>${a.year} · <a href="${a.url}">${esc(a.title)}</a></li>`).join("");
}

function renderNews() {
  // Watercolor versions live in assets/img/wc/ (tools/watercolor.py); fall back to the original.
  const img = (src) => `<img src="${src.replace("assets/img/", "assets/img/wc/")}" data-orig="${src}" alt="" loading="lazy">`;
  $("news").innerHTML = NEWS.map((n) => `<li><time>${esc(n.date)}</time>${n.image ? img(n.image) : "<span></span>"}<p>${n.text}</p></li>`).join("");
  $("news").querySelectorAll("img").forEach((el) => el.addEventListener("error", () => { el.src = el.dataset.orig; }, { once: true }));
}

// Software as terminal-style cards: clone command, language mix, live GitHub stats,
// and a link to the paper each repository accompanies.
const LANG_COLOR = {
  Python: "#3572A5", "Jupyter Notebook": "#DA5B0B", Jupyter: "#DA5B0B", Shell: "#89E051", JavaScript: "#F1E05A",
  TypeScript: "#3178C6", HTML: "#E34C26", CSS: "#563D7C", "C++": "#F34B7D", Dockerfile: "#384D54",
  PyTorch: "#EE4C2C", TensorFlow: "#FF8F00",
};
const repoUrl = (s) => `https://github.com/${s.repo}`;
function paperFor(s) {
  const url = repoUrl(s).toLowerCase();
  return PROJECTS.find((p) => Object.values(p.links || {}).some((u) => u && u.toLowerCase().replace(/\/$/, "") === url));
}
const plainDesc = (d) => d.replace(/^[^\p{L}\p{N}]+/u, "");
function renderSoftware() {
  const rows = SOFTWARE.map((s) => {
    const name = s.repo.split("/")[1], url = repoUrl(s), paper = paperFor(s);
    const paperLink = paper ? ` <a class="t-paper" href="${paper.links.paper || paper.links.arxiv || paper.links.pdf || "#papers"}">paper ↗</a>` : "";
    return `<li data-repo="${s.repo.toLowerCase()}">
      <span class="t-main"><span class="t-head"><a class="t-name" href="${url}">${esc(name)}</a>${paperLink}</span>
        <span class="t-desc">${esc(plainDesc(s.desc))}</span></span>
      <span class="t-lang"><i style="background:${LANG_COLOR[s.lang] || "#8B8478"}"></i><span>${esc(s.lang)}</span></span>
      <span class="t-stars" title="Stars">★ <b class="stars">${s.stars}</b></span>
      <span class="t-updated sw-updated"></span>
      <button type="button" class="t-copy" data-copy="git clone ${url}" aria-label="Copy git clone command for ${esc(name)}" title="Copy git clone command">
        <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>
      </button>
    </li>`;
  }).join("");
  const owner = SOFTWARE[0] ? SOFTWARE[0].repo.split("/")[0] : "";
  $("software-list").innerHTML = `
    <div class="term-bar"><span class="sw-dots" aria-hidden="true"><i></i><i></i><i></i></span><span>~/code — <a href="https://github.com/${owner}">github.com/${esc(owner)}</a></span></div>
    <p class="term-cmd"><span class="sw-prompt" aria-hidden="true">$</span> ls ~/code <span class="term-note" id="sw-summary"></span></p>
    <ul class="term-list">${rows}</ul>
    <p class="term-cmd term-end"><span class="sw-prompt" aria-hidden="true">$</span> <span class="term-cursor" aria-hidden="true"></span><span class="term-toast" id="sw-toast" aria-live="polite"></span></p>`;
  $("software-list").addEventListener("click", async (e) => {
    const b = e.target.closest(".t-copy");
    if (!b) return;
    let ok = true;
    try { await navigator.clipboard.writeText(b.dataset.copy); } catch (err) { ok = false; }
    $("sw-toast").textContent = ok ? `copied: ${b.dataset.copy}` : b.dataset.copy;
    clearTimeout(b._t);
    b._t = setTimeout(() => { $("sw-toast").textContent = ""; }, 2400);
  });
  summarizeSoftware();
}
function summarizeSoftware() {
  const el = $("sw-summary");
  if (!el) return;
  const stars = [...document.querySelectorAll("#software-list .stars")].reduce((a, b) => a + (+b.textContent || 0), 0);
  el.textContent = `# ${SOFTWARE.length} repositories · ${stars} star${stars === 1 ? "" : "s"}`;
}

// ----------------------------------------------------------- live data --

async function loadCitations() {
  const ids = PROJECTS.map((p) => p.s2).filter(Boolean);
  try {
    const r = await fetch("https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ids }),
    });
    if (!r.ok) throw new Error(r.status);
    (await r.json()).forEach((paper, i) => { if (paper && paper.citationCount != null) citations[ids[i]] = paper.citationCount; });
  } catch (e) { /* offline or rate-limited: the page works without counts */ }
  const total = Object.values(citations).reduce((a, b) => a + b, 0);
  $("stat-cites").textContent = Object.keys(citations).length ? total.toLocaleString() : "—";
  document.querySelectorAll(".cites[data-s2]").forEach((el) => {
    const c = citations[el.dataset.s2];
    if (c) el.textContent = `${c} citation${c === 1 ? "" : "s"}`;
  });
  redraws.forEach((f) => f());
}

async function loadRepoStats() {
  if (!$("software-list")) return;
  const since = (iso) => {
    const d = Math.floor((Date.now() - Date.parse(iso)) / 864e5);
    return d < 1 ? "today" : d < 31 ? `${d}d ago` : d < 365 ? `${Math.round(d / 30)}mo ago` : `${Math.round(d / 365)}y ago`;
  };
  try {
    for (const owner of [...new Set(SOFTWARE.map((s) => s.repo.split("/")[0]))]) {
      const r = await fetch(`https://api.github.com/users/${owner}/repos?per_page=100`);
      if (!r.ok) continue;
      for (const repo of await r.json()) {
        const li = document.querySelector(`#software-list li[data-repo="${repo.full_name.toLowerCase()}"]`);
        if (!li) continue;
        li.querySelector(".stars").textContent = repo.stargazers_count;
        if (repo.pushed_at) li.querySelector(".sw-updated").textContent = since(repo.pushed_at);
      }
    }
  } catch (e) { /* keep fallback numbers */ }
  summarizeSoftware();
}

// ------------------------------------------------- reading progress, reveal --

function renderChrome() {
  const bar = $("progress");
  const chapters = [["ch1", "#B4532A"], ["ch2", "#1F6F6B"], ["ch3", "#2E4A87"]].map(([id, c]) => [$(id).closest("section"), c]);
  const update = () => {
    const doc = document.documentElement;
    bar.style.width = `${(doc.scrollTop / (doc.scrollHeight - doc.clientHeight)) * 100}%`;
    let color = "#B4532A";
    chapters.forEach(([sec, c]) => { if (sec.getBoundingClientRect().top < window.innerHeight * 0.5) color = c; });
    bar.style.background = color;
  };
  document.addEventListener("scroll", update, { passive: true });
  update();

  if (REDUCED || !("IntersectionObserver" in window)) return;
  const io = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".prose, .graphic, .chapter, .block").forEach((el) => {
    if (el.getBoundingClientRect().top > window.innerHeight) { el.classList.add("reveal"); io.observe(el); }
  });
}

// Each part renders only on the page that has it (index.html or about.html).
[["stats", renderProfile], ["profile", renderAbout], ["ni-svg", renderNi], ["w-bars", renderW],
 ["tracker-canvas", renderTracker], ["ks-svg", renderKS], ["seg-svg", renderSeg], ["rag-steps", renderRag],
 ["timeline", renderTimeline], ["network", renderNetwork], ["index", renderIndex], ["news", renderNews],
 ["news-cards", renderNewsCards], ["software-list", renderSoftware], ["progress", renderChrome]]
  .forEach(([id, render]) => { if ($(id)) render(); });
loadCitations();
loadRepoStats();
