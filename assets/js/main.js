// Renders the page from data.js. No framework, no build step.

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const LINK_META = {
  paper:  ["fa-regular fa-file-lines", "Paper"],
  pdf:    ["fa-regular fa-file-pdf", "PDF"],
  arxiv:  ["fa-solid fa-scroll", "arXiv"],
  github: ["fa-brands fa-github", "GitHub"],
  data:   ["fa-solid fa-database", "Data"],
  website:["fa-solid fa-globe", "Website"],
  demo:   ["fa-solid fa-play", "Demo"],
  blog:   ["fa-regular fa-newspaper", "Blog"],
};

const LANG_COLORS = {
  Python: "#3572A5", PyTorch: "#ee4c2c", TensorFlow: "#ff8f00", Jupyter: "#DA5B0B",
  JavaScript: "#f1e05a", React: "#61dafb",
};

function renderSidebar() {
  const L = SITE.links;
  const social = [
    [L.github, "fa-brands fa-github", "GitHub"],
    [L.scholar, "fa-brands fa-google-scholar", "Google Scholar"],
    [L.linkedin, "fa-brands fa-linkedin", "LinkedIn"],
    [L.twitter, "fa-brands fa-x-twitter", "X"],
  ].filter(([url]) => url)
   .map(([url, icon, label]) => `<a href="${url}" title="${label}" aria-label="${label}"><i class="${icon}"></i></a>`)
   .join("");

  const contact = [];
  if (SITE.email) contact.push(`<li><i class="fa-regular fa-envelope"></i><a href="mailto:${SITE.email}" style="color:inherit">${SITE.email}</a></li>`);
  if (SITE.location) contact.push(`<li><i class="fa-solid fa-location-dot"></i>${esc(SITE.location)}</li>`);
  if (SITE.cv) contact.push(`<li><i class="fa-regular fa-address-card"></i><span><a href="${SITE.cv}">CV</a>${SITE.cvNote ? ` (${esc(SITE.cvNote)})` : ""}</span></li>`);

  $("sidebar").innerHTML = `
    <img class="photo" src="${SITE.photo}" alt="${esc(SITE.name)}">
    <div class="side-name">${esc(SITE.name)}</div>
    <div class="side-title">${esc(SITE.title)}</div>
    <div class="socials">${social}</div>
    <hr class="side-rule">
    <ul class="contact">${contact.join("")}</ul>`;
}

function renderNews() {
  $("news").innerHTML = NEWS.map((n) => {
    const media = n.image
      ? `<img src="${n.image}" alt="" loading="lazy">`
      : `<div class="tile tint-${n.tint || "slate"}">${n.emoji || "📰"}</div>`;
    return `<div class="news-card">${media}<div class="text">${n.text}</div><div class="date">${esc(n.date)}</div></div>`;
  }).join("");

  const strip = $("news"), left = $("news-left"), right = $("news-right");
  const update = () => {
    left.hidden = strip.scrollLeft < 8;
    right.hidden = strip.scrollLeft + strip.clientWidth > strip.scrollWidth - 8;
  };
  left.onclick = () => strip.scrollBy({ left: -strip.clientWidth * 0.8 });
  right.onclick = () => strip.scrollBy({ left: strip.clientWidth * 0.8 });
  strip.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
}

function authorsHTML(list, idx) {
  const fmt = (a) => (a === SITE.me ? `<span class="me">${esc(a)}</span>` : esc(a));
  const LIMIT = 12;
  if (list.length <= LIMIT) return list.map(fmt).join(", ");
  // Long author lists: show the first few (always including me), then a toggle.
  const meAt = list.indexOf(SITE.me);
  const shown = list.slice(0, Math.max(8, meAt + 1));
  const rest = list.length - shown.length;
  return `<span id="authors-${idx}">${shown.map(fmt).join(", ")}, <button class="more" data-idx="${idx}">and ${rest} more</button></span>`;
}

function projectHTML(p, i) {
    const media = p.image
    ? `<img class="thumb" src="${p.image}" alt="${esc(p.title)}" loading="lazy">`
    : `<div class="title-card tint-${p.card.tint}"><div class="l1">${esc(p.card.line1)}</div><div class="l2">${esc(p.card.line2)}</div></div>`;
  const href = p.links.paper || p.links.arxiv || p.links.pdf || "#";
  const links = Object.entries(p.links)
    .filter(([, url]) => url)
    .map(([k, url]) => { const [icon, label] = LINK_META[k] || ["fa-solid fa-link", k];
      return `<a href="${url}"><i class="${icon}"></i>${label}</a>`; })
    .join("");
  const s2 = /^[0-9a-f]{40}$/.test(p.s2 || "") ? `<a href="https://www.semanticscholar.org/paper/${p.s2}"><i class="fa-solid fa-graduation-cap"></i>Semantic Scholar</a>` : "";
  const cites = p.s2 ? `<span class="cites" data-s2="${p.s2}" hidden><i class="fa-solid fa-quote-left"></i><span></span></span>` : "";
  return `
    <div class="project">
      ${p.figure
        ? `<a href="${p.figure}" class="fig-link" data-cap="${esc(p.figCaption || "")}" data-title="${esc(p.title)}" title="View figure">${media}<span class="zoom"><i class="fa-solid fa-magnifying-glass-plus"></i></span></a>`
        : `<a href="${href}">${media}</a>`}
      <div>
        <h4>${esc(p.title)}</h4>
        <div class="authors">${authorsHTML(p.authors, i)}</div>
        <div class="venue">${esc(p.venue)}</div>
        <div class="tldr"><span class="badge">TLDR</span>${p.tldr}</div>
        <div class="plinks">${cites}${links}${s2}</div>
      </div>
    </div>`;
}

const isMM = (p) => /^(Microscopy & Microanalysis|NAPAC)/.test(p.venue);   // conference papers
const MM_SHOWN = 3;   // how many conference papers to show before "Show all"

function renderProjects() {
  const indexed = PROJECTS.map((p, i) => [p, i]);
  const pubs = indexed.filter(([p]) => !isMM(p));
  const mm = indexed.filter(([p]) => isMM(p));

  // Publications: papers marked `more: true` stay hidden until "Show all".
  $("projects").innerHTML = pubs.map(([p, i]) => p.more
    ? projectHTML(p, i).replace('<div class="project">', '<div class="project pub-more" hidden>')
    : projectHTML(p, i)).join("");
  const pubMore = pubs.filter(([p]) => p.more).length, pubToggle = $("pub-toggle");
  if (!pubMore) pubToggle.hidden = true;
  else {
    let open = false;
    const pubLabel = () => open
      ? `<i class="fa-solid fa-chevron-up"></i> Show fewer`
      : `<i class="fa-solid fa-chevron-down"></i> Show all ${pubs.length} publications`;
    pubToggle.innerHTML = pubLabel();
    pubToggle.onclick = () => {
      open = !open;
      document.querySelectorAll(".pub-more").forEach((el) => { el.hidden = !open; });
      pubToggle.innerHTML = pubLabel();
      if (!open) pubToggle.scrollIntoView({ block: "center" });
    };
  }
  $("mm").innerHTML = mm.slice(0, MM_SHOWN).map(([p, i]) => projectHTML(p, i)).join("");

  const extra = mm.slice(MM_SHOWN);
  $("mm-more").innerHTML = extra.map(([p, i]) => projectHTML(p, i)).join("")
    + (ABSTRACTS.length ? `<h5 class="more-head">More abstracts</h5><ul class="abstract-list">${ABSTRACTS
        .map((a) => `<li><span class="yr">${a.year}</span><a href="${a.url}">${esc(a.title)}</a></li>`).join("")}</ul>` : "");

  const hiddenCount = extra.length + ABSTRACTS.length;
  const toggle = $("mm-toggle"), more = $("mm-more");
  if (!hiddenCount) { toggle.hidden = true; return; }
  const label = () => more.hidden
    ? `<i class="fa-solid fa-chevron-down"></i> Show all ${mm.length + ABSTRACTS.length} conference papers`
    : `<i class="fa-solid fa-chevron-up"></i> Show fewer`;
  toggle.innerHTML = label();
  toggle.onclick = () => {
    more.hidden = !more.hidden; toggle.innerHTML = label();
    if (more.hidden) $("mm-section").scrollIntoView({ block: "start" });
  };

  document.querySelectorAll(".authors .more").forEach((btn) => {
    btn.onclick = () => {
      const p = PROJECTS[btn.dataset.idx];
      $(`authors-${btn.dataset.idx}`).innerHTML = p.authors
        .map((a) => (a === SITE.me ? `<span class="me">${esc(a)}</span>` : esc(a))).join(", ");
    };
  });
}

function renderSoftware() {
  $("software").innerHTML = SOFTWARE.map((s) => {
    const [owner, name] = s.repo.split("/");
    const url = `https://github.com/${s.repo}`;
    return `
      <div class="repo" data-repo="${s.repo.toLowerCase()}">
        <div class="head"><i class="fa-solid fa-book-bookmark"></i>
          <a href="${url}"><span class="owner">${esc(owner)}/</span><span class="rname">${esc(name)}</span></a>
          <span class="tag">${esc(s.tag)}</span></div>
        <div class="desc">${esc(s.desc)}</div>
        <div class="meta">
          <span><span class="dot" style="background:${LANG_COLORS[s.lang] || "#999"}"></span>${esc(s.lang)}</span>
          <a href="${url}/stargazers"><i class="fa-regular fa-star"></i> <span class="stars">${s.stars}</span></a>
          <a href="${url}/forks"><i class="fa-solid fa-code-fork"></i> <span class="forks">${s.forks}</span></a>
        </div>
      </div>`;
  }).join("");
}

// Live numbers. Both requests are optional; the page is complete without them.
async function loadCitationCounts() {
  const ids = PROJECTS.map((p) => p.s2).filter(Boolean);
  try {
    const r = await fetch("https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ids }),
    });
    if (!r.ok) return;
    const data = await r.json();
    data.forEach((paper, i) => {
      if (!paper || !paper.citationCount) return;
      const el = document.querySelector(`.cites[data-s2="${ids[i]}"]`);
      if (el) { el.querySelector("span").textContent = paper.citationCount; el.hidden = false; }
    });
  } catch (e) { /* offline or rate-limited: leave counts hidden */ }
}

async function loadRepoStats() {
  try {
    const owners = [...new Set(SOFTWARE.map((s) => s.repo.split("/")[0]))];
    for (const owner of owners) {
      const r = await fetch(`https://api.github.com/users/${owner}/repos?per_page=100`);
      if (!r.ok) continue;
      for (const repo of await r.json()) {
        const card = document.querySelector(`.repo[data-repo="${repo.full_name.toLowerCase()}"]`);
        if (!card) continue;
        card.querySelector(".stars").textContent = repo.stargazers_count;
        card.querySelector(".forks").textContent = repo.forks_count;
      }
    }
  } catch (e) { /* keep fallback numbers */ }
}

// Figure viewer: click a thumbnail to see the full figure from the paper.
function setupLightbox() {
  const box = document.createElement("div");
  box.className = "lightbox"; box.hidden = true;
  box.innerHTML = `<figure><button class="lb-close" aria-label="Close"><i class="fa-solid fa-xmark"></i></button>
    <img alt=""><figcaption></figcaption></figure>`;
  document.body.appendChild(box);
  const img = box.querySelector("img"), cap = box.querySelector("figcaption");
  const close = () => { box.hidden = true; img.src = ""; document.body.style.overflow = ""; };
  document.addEventListener("click", (e) => {
    const a = e.target.closest(".fig-link");
    if (a) {
      e.preventDefault();
      img.src = a.getAttribute("href"); img.alt = a.dataset.title;
      cap.innerHTML = `<b>${a.dataset.title}</b><br>${a.dataset.cap}`;
      box.hidden = false; document.body.style.overflow = "hidden";
    } else if (!box.hidden && (e.target === box || e.target.closest(".lb-close"))) close();
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !box.hidden) close(); });
}

$("name").textContent = SITE.name;
$("bio").innerHTML = SITE.bio;
$("year").textContent = new Date().getFullYear();
renderSidebar();
renderNews();
renderProjects();
renderSoftware();
loadCitationCounts();
loadRepoStats();
setupLightbox();
