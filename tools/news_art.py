# Regenerate: python tools/news_art.py <outdir>   (needs: pip install playwright)
"""Hand-built 'good vibes' illustrations for the News cards.
Each scene is SVG with a painterly displacement filter and paper grain,
rendered to PNG with Chromium."""
import math, random

W = 800

DEFS = """
<defs>
  <filter id="paint" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="4" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="14" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="9"/>
    <feColorMatrix values="0 0 0 0 0.25  0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0.16 0"/>
  </filter>
  <filter id="strokes">
    <feTurbulence type="fractalNoise" baseFrequency="0.012 0.12" numOctaves="2" seed="21"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.10 -0.02"/>
  </filter>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="14"/>
  </filter>
  <filter id="soft"><feGaussianBlur stdDeviation="3"/></filter>
</defs>"""

def svg(body, bg):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}">
{DEFS}
<g filter="url(#paint)">
{bg}
{body}
</g>
<rect width="{W}" height="{W}" filter="url(#strokes)"/>
<rect width="{W}" height="{W}" filter="url(#grain)"/>
</svg>"""

def sky(id_, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient><rect width="{W}" height="{W}" fill="url(#{id_})"/>'

def radial(id_, cx, cy, r, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{id_}">{s}</radialGradient><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{id_})"/>'

def hill(d, fill, op=1):
    return f'<path d="{d}" fill="{fill}" opacity="{op}"/>'

def sparkles(n, seed, box, colors, rmin=3, rmax=9):
    rnd = random.Random(seed); x0, y0, x1, y1 = box; out = []
    for _ in range(n):
        x, y, r = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(rmin, rmax)
        c = rnd.choice(colors)
        out.append(f'<path d="M{x} {y-r*2} Q{x} {y} {x+r*2} {y} Q{x} {y} {x} {y+r*2} Q{x} {y} {x-r*2} {y} Q{x} {y} {x} {y-r*2}Z" fill="{c}" opacity="{rnd.uniform(.6,1):.2f}"/>')
    return "".join(out)

def robot(x, y, s=1.0, body="#f2f4f8", accent="#ff8a65", wave=False, prop=""):
    """Friendly robot, centred at (x, y) = feet."""
    def S(v): return v * s
    arm_l = f'<path d="M{x-S(48)} {y-S(118)} q{-S(30)} {S(20)} {-S(34)} {S(52)}" stroke="{body}" stroke-width="{S(14)}" stroke-linecap="round" fill="none"/>'
    if wave:
        arm_r = f'<path d="M{x+S(48)} {y-S(122)} q{S(34)} {-S(14)} {S(40)} {-S(58)}" stroke="{body}" stroke-width="{S(14)}" stroke-linecap="round" fill="none"/>'
    else:
        arm_r = f'<path d="M{x+S(48)} {y-S(118)} q{S(30)} {S(20)} {S(34)} {S(52)}" stroke="{body}" stroke-width="{S(14)}" stroke-linecap="round" fill="none"/>'
    return f"""<g>
  <ellipse cx="{x}" cy="{y+S(4)}" rx="{S(58)}" ry="{S(10)}" fill="#000" opacity=".15"/>
  <rect x="{x-S(30)}" y="{y-S(40)}" width="{S(18)}" height="{S(40)}" rx="{S(8)}" fill="#c9d1dc"/>
  <rect x="{x+S(12)}" y="{y-S(40)}" width="{S(18)}" height="{S(40)}" rx="{S(8)}" fill="#c9d1dc"/>
  {arm_l}{arm_r}
  <rect x="{x-S(52)}" y="{y-S(140)}" width="{S(104)}" height="{S(106)}" rx="{S(26)}" fill="{body}"/>
  <circle cx="{x}" cy="{y-S(88)}" r="{S(16)}" fill="{accent}" opacity=".9"/>
  <path d="M{x-S(7)} {y-S(90)} l{S(5)} {S(6)} l{S(10)} {-S(12)}" stroke="#fff" stroke-width="{S(4)}" fill="none" stroke-linecap="round"/>
  <rect x="{x-S(62)}" y="{y-S(236)}" width="{S(124)}" height="{S(92)}" rx="{S(30)}" fill="{body}"/>
  <rect x="{x-S(46)}" y="{y-S(220)}" width="{S(92)}" height="{S(60)}" rx="{S(22)}" fill="#26324a"/>
  <ellipse cx="{x-S(20)}" cy="{y-S(192)}" rx="{S(9)}" ry="{S(11)}" fill="#7ef0ff"/>
  <ellipse cx="{x+S(20)}" cy="{y-S(192)}" rx="{S(9)}" ry="{S(11)}" fill="#7ef0ff"/>
  <path d="M{x-S(14)} {y-S(173)} q{S(14)} {S(12)} {S(28)} 0" stroke="#7ef0ff" stroke-width="{S(4)}" fill="none" stroke-linecap="round"/>
  <circle cx="{x-S(34)}" cy="{y-S(176)}" r="{S(6)}" fill="#ff9eb5" opacity=".7"/>
  <circle cx="{x+S(34)}" cy="{y-S(176)}" r="{S(6)}" fill="#ff9eb5" opacity=".7"/>
  <line x1="{x}" y1="{y-S(236)}" x2="{x}" y2="{y-S(262)}" stroke="#c9d1dc" stroke-width="{S(6)}"/>
  <circle cx="{x}" cy="{y-S(268)}" r="{S(16)}" fill="{accent}" filter="url(#glow)" opacity=".8"/>
  <circle cx="{x}" cy="{y-S(268)}" r="{S(9)}" fill="{accent}"/>
  {prop}
</g>"""

def clouds(seed, n, box, col="#fff", op=.85):
    rnd = random.Random(seed); out = []
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y, s = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(.6, 1.3)
        out.append(f'<g opacity="{op}" fill="{col}"><ellipse cx="{x}" cy="{y}" rx="{70*s}" ry="{24*s}"/><circle cx="{x-25*s}" cy="{y-14*s}" r="{26*s}"/><circle cx="{x+15*s}" cy="{y-22*s}" r="{32*s}"/></g>')
    return "".join(out)

SCENES = {}

# 1. Sep 2026 - AI agents at a user facility: robots waving in front of a synchrotron ring at sunrise
SCENES["news_agents"] = svg(
    clouds(3, 4, (60, 120, 740, 260), "#fff4e8", .8)
    + radial("sun1", 400, 380, 230, [(0, "#fff3c4", 1), (.5, "#ffd38a", .7), (1, "#ffb38a", 0)])
    + '<circle cx="400" cy="400" r="110" fill="#fff1b8"/>'
    # storage ring building: flattened torus on the plain
    + '<ellipse cx="400" cy="560" rx="330" ry="92" fill="#e8ecf6"/>'
    + '<ellipse cx="400" cy="548" rx="330" ry="88" fill="#f8f9fd"/>'
    + '<ellipse cx="400" cy="552" rx="230" ry="52" fill="#9fc7a5"/>'
    + '<ellipse cx="400" cy="548" rx="228" ry="50" fill="#b6dcb4"/>'
    + "".join(f'<rect x="{400+300*math.cos(a)-8}" y="{548+80*math.sin(a)-14}" width="16" height="10" rx="3" fill="#ffd38a" opacity=".9"/>' for a in [i*math.pi/7 for i in range(14)])
    + hill("M0 640 Q200 600 400 630 T800 620 V800 H0Z", "#8fcf9a")
    + hill("M0 700 Q260 660 520 700 T800 690 V800 H0Z", "#6fbf88")
    + robot(230, 760, .62, accent="#ff8a65", wave=True)
    + robot(400, 780, .72, accent="#7c6cff", body="#fdf6ec",
            prop='<rect x="430" y="640" width="46" height="58" rx="6" fill="#fff" stroke="#c9d1dc" stroke-width="4" transform="rotate(10 453 669)"/><line x1="440" y1="660" x2="466" y2="664" stroke="#9aa8b7" stroke-width="3"/><line x1="438" y1="672" x2="462" y2="676" stroke="#9aa8b7" stroke-width="3"/>')
    + robot(575, 760, .6, accent="#3ccf91", wave=True)
    + sparkles(16, 11, (60, 80, 740, 420), ["#fff", "#ffe08a", "#ffc4d6"]),
    "<defs>" + "</defs>" + sky("s1", [(0, "#a8c8ff"), (.45, "#ffd6e5"), (.75, "#ffe7c2"), (1, "#fff3d6")]),
)

# 2. Jul 2026 - APS-RAG: robot librarian with flying glowing pages, rocket launching
def book(x, y, w, h, c, rot=0):
    return f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/><rect x="{x+4}" y="{y+6}" width="{w-8}" height="5" fill="#fff" opacity=".6"/></g>'
pages = "".join(
    f'<g transform="translate({x} {y}) rotate({r})"><rect x="-26" y="-34" width="52" height="68" rx="5" fill="#fffdf5"/><line x1="-16" y1="-18" x2="16" y2="-18" stroke="#c8b98e" stroke-width="4"/><line x1="-16" y1="-6" x2="16" y2="-6" stroke="#c8b98e" stroke-width="4"/><line x1="-16" y1="6" x2="8" y2="6" stroke="#c8b98e" stroke-width="4"/><circle cx="0" cy="0" r="46" fill="#fff4b0" opacity=".25" filter="url(#glow)"/></g>'
    for x, y, r in [(150, 250, -18), (290, 170, 12), (520, 200, -8), (640, 300, 16), (430, 120, 4)])
shelves = "".join(book(40 + i * 34, 430 - (i % 3) * 8, 28, 120 + (i % 3) * 8, c) for i, c in enumerate(["#e57373", "#64b5f6", "#ffd54f", "#81c784", "#ba68c8", "#4db6ac", "#ff8a65"]))
shelves += "".join(book(520 + i * 34, 430 - (i % 2) * 10, 28, 120 + (i % 2) * 10, c) for i, c in enumerate(["#9575cd", "#4fc3f7", "#f06292", "#aed581", "#ffb74d", "#7986cb", "#4db6ac"]))
SCENES["news_apsrag"] = svg(
    radial("lamp", 400, 260, 360, [(0, "#fff6d8", .9), (1, "#fff6d8", 0)])
    + '<rect x="0" y="550" width="800" height="250" fill="#c98b5b"/><rect x="0" y="550" width="800" height="16" fill="#a86d43"/>'
    + '<rect x="30" y="540" width="250" height="14" rx="4" fill="#8d5a36"/><rect x="510" y="540" width="260" height="14" rx="4" fill="#8d5a36"/>'
    + shelves + pages
    + '<g transform="translate(690 120) rotate(30)"><path d="M0 -50 Q22 -20 18 30 H-18 Q-22 -20 0 -50Z" fill="#fff"/><circle cx="0" cy="-8" r="9" fill="#64b5f6"/><path d="M-18 18 L-32 40 L-18 34Z M18 18 L32 40 L18 34Z" fill="#ff8a65"/><path d="M-10 32 Q0 80 10 32Z" fill="#ffcc4d"/><path d="M-6 32 Q0 62 6 32Z" fill="#fff3b0"/></g>'
    + robot(400, 770, .95, accent="#ffcc4d", body="#f6f2ff",
            prop='<g transform="translate(470 690) scale(.7)"><rect x="-70" y="-30" width="70" height="88" rx="6" fill="#5c6bc0" transform="rotate(-8)"/><rect x="0" y="-30" width="70" height="88" rx="6" fill="#7986cb" transform="rotate(8)"/><rect x="-62" y="-22" width="58" height="72" rx="4" fill="#fffdf5" transform="rotate(-8)"/><rect x="4" y="-22" width="58" height="72" rx="4" fill="#fffdf5" transform="rotate(8)"/></g>')
    + sparkles(18, 5, (40, 60, 760, 520), ["#ffe08a", "#fff", "#ffd1dc"]),
    sky("s2", [(0, "#ffe9c7"), (1, "#ffd5b0")]),
)

# 3. Oct 2025 - carbon gasification: glowing catalyst particle, curly carbon filaments turning into sparks
def coil(x, y, n, r, c="#4a3530"):
    d = f"M{x} {y}"
    for i in range(n):
        d += f" c {r} {-r*1.4} {r*2.2} {-r*0.2} {r*1.4} {r*0.6} c {-r*0.6} {r*0.6} {-r*0.2} {-r*1.6} {r*1.2} {-r*1.2}"
    return f'<path d="{d}" stroke="{c}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".75"/>'
def flame(x, y, s=1.0):
    return (f'<path d="M{x} {y} q{-18*s} {-24*s} {-2*s} {-56*s} q{6*s} {18*s} {16*s} {22*s} q{10*s} {-12*s} {4*s} {-30*s} q{24*s} {24*s} {12*s} {58*s}Z" fill="#ff9f43"/>'
            f'<path d="M{x+2*s} {y} q{-8*s} {-14*s} {2*s} {-30*s} q{10*s} {14*s} {6*s} {30*s}Z" fill="#ffe08a"/>')
fil = (coil(220, 500, 3, 14) + coil(470, 520, 3, 13) + coil(300, 545, 2, 12) + coil(520, 470, 2, 11)
       + flame(330, 500, 1.0) + flame(612, 510, 1.1) + flame(392, 548, .8) + flame(586, 470, .7))
embers = "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".9"/>'
    for x, y, r, c in [(250, 230, 7, "#ffd166"), (310, 160, 5, "#ff9f43"), (420, 120, 8, "#ffd166"), (520, 170, 6, "#ff7b54"), (585, 240, 7, "#ffd166"), (360, 200, 4, "#fff3b0"), (470, 210, 5, "#fff3b0"), (650, 150, 4, "#ffd166")])
SCENES["news_gasification"] = svg(
    radial("fire", 400, 420, 330, [(0, "#ffe7a3", 1), (.55, "#ffb36b", .55), (1, "#ff8a65", 0)])
    + hill("M0 600 Q220 540 400 560 T800 540 V800 H0Z", "#c97b63")
    + hill("M0 660 Q300 610 560 650 T800 640 V800 H0Z", "#a95f4f")
    + '<ellipse cx="400" cy="500" rx="210" ry="90" fill="#f4d9b8"/>'
    + '<ellipse cx="400" cy="488" rx="200" ry="82" fill="#fbead2"/>'
    + '<circle cx="410" cy="420" r="80" fill="#ffb347" filter="url(#glow)"/>'
    + '<circle cx="410" cy="420" r="56" fill="#ffcf70"/><circle cx="392" cy="402" r="17" fill="#fff4cf" opacity=".85"/>'
    + '<ellipse cx="392" cy="426" rx="6" ry="8" fill="#7a4a2a"/><ellipse cx="428" cy="426" rx="6" ry="8" fill="#7a4a2a"/><path d="M398 446 q12 10 24 0" stroke="#7a4a2a" stroke-width="4" fill="none" stroke-linecap="round"/>'
    + fil + embers
    + "".join(f'<g opacity=".55"><circle cx="{x}" cy="{y}" r="18" fill="#fff"/><circle cx="{x-16}" cy="{y+8}" r="12" fill="#fff"/><circle cx="{x+16}" cy="{y+8}" r="12" fill="#fff"/></g>' for x, y in [(230, 120), (560, 90), (660, 210)])
    + sparkles(14, 8, (80, 60, 720, 380), ["#fff3b0", "#ffd166"]),
    sky("s3", [(0, "#ffd29d"), (.6, "#ffb38a"), (1, "#f78f6f")]),
)

# 4. Jun 2025 - NiO reduction: a cracked hollow shell releasing shiny nickel droplets with H2 bubbles, underwater-teal
bubbles = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#ffffff" stroke-width="3" opacity=".7"/><circle cx="{x-r*.35}" cy="{y-r*.35}" r="{r*.25}" fill="#fff" opacity=".8"/>'
                  for x, y, r in [(150, 520, 18), (190, 420, 11), (640, 480, 16), (680, 380, 10), (600, 250, 13), (220, 260, 9), (120, 340, 7), (700, 560, 8)])
nickel = ('<radialGradient id="ni" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#e3e8ef"/><stop offset="1" stop-color="#8a97a8"/></radialGradient>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="{r+14}" fill="#e9fffb" opacity=".5" filter="url(#glow)"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#ni)" stroke="#6e7b8c" stroke-width="2"/>'
                    f'<path d="M{x-r-14} {y+r*0.6} q{-10} {14} {-4} {30}" stroke="#ffffff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/>'
                    for x, y, r in [(290, 255, 30), (420, 175, 36), (548, 262, 26), (352, 120, 18), (500, 100, 16), (610, 175, 14)]))
SCENES["news_reduction"] = svg(
    radial("light4", 420, 120, 420, [(0, "#e8fffb", .9), (1, "#e8fffb", 0)])
    + hill("M0 660 Q200 610 400 640 T800 630 V800 H0Z", "#5fb8a8")
    + "".join(f'<path d="M{x} 800 q-20 -80 10 -150 q20 -50 -6 -100" stroke="#3f9d8b" stroke-width="12" fill="none" stroke-linecap="round"/>' for x in [80, 110, 700, 730])
    # hollow NiO shell cracked open, green grains
    + '<circle cx="410" cy="470" r="150" fill="#6b8f5a"/>'
    + "".join(f'<path d="M410 470 L{410+150*math.cos(a)} {470+150*math.sin(a)} A150 150 0 0 1 {410+150*math.cos(a+math.pi/6)} {470+150*math.sin(a+math.pi/6)}Z" fill="{c}" stroke="#4e6e42" stroke-width="4"/>'
              for a, c in zip([i * math.pi / 6 for i in range(12)], ["#7fa36a", "#8db475", "#76995f", "#91b87b"] * 3))
    + '<circle cx="410" cy="470" r="96" fill="#2f5a55"/>'
    + '<path d="M300 370 L360 420 L330 450 L410 470 L380 520" stroke="#e9fff8" stroke-width="5" fill="none" opacity=".8"/>'
    + '<circle cx="410" cy="470" r="70" fill="#bff6ff" opacity=".35" filter="url(#glow)"/>'
    + nickel + bubbles
    + sparkles(12, 4, (100, 60, 700, 380), ["#fff", "#c9fff4"]),
    sky("s4", [(0, "#c6f6ef"), (.6, "#9fe3d8"), (1, "#7ccfc4")]),
)

# 5. Oct 2024 - tungsten nanofuzz: a fluffy silver "fuzzball" creature on a hill under an aurora (fusion plasma)
fuzz = "".join(f'<line x1="400" y1="500" x2="{400+math.cos(a)*r}" y2="{500+math.sin(a)*r}" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
               for a, r, c in [(i * 0.13, 120 + 18 * math.sin(i * 1.7), ["#d9dee8", "#b8c0ce", "#eef1f6"][i % 3]) for i in range(49)])
SCENES["news_tungsten"] = svg(
    "".join(f'<path d="M-50 {y} C 200 {y-120} 450 {y+90} 850 {y-60}" stroke="{c}" stroke-width="{w}" fill="none" opacity=".55" filter="url(#soft)"/>'
            for y, c, w in [(160, "#8ef7c8", 46), (220, "#c58bff", 38), (120, "#7fd4ff", 30), (270, "#ff9ad5", 26)])
    + sparkles(40, 2, (20, 20, 780, 420), ["#fff", "#e0f7ff"], 1.5, 4)
    + hill("M0 620 Q260 520 520 590 T800 560 V800 H0Z", "#3d3a6b")
    + hill("M0 700 Q300 650 560 690 T800 680 V800 H0Z", "#2e2b55")
    + '<circle cx="400" cy="500" r="150" fill="#c8f0ff" opacity=".35" filter="url(#glow)"/>'
    + fuzz
    + '<circle cx="400" cy="500" r="92" fill="#cfd5e0"/>'
    + '<ellipse cx="370" cy="490" rx="12" ry="15" fill="#2a2f45"/><ellipse cx="430" cy="490" rx="12" ry="15" fill="#2a2f45"/>'
    + '<circle cx="374" cy="485" r="4" fill="#fff"/><circle cx="434" cy="485" r="4" fill="#fff"/>'
    + '<path d="M385 528 q15 14 30 0" stroke="#2a2f45" stroke-width="5" fill="none" stroke-linecap="round"/>'
    + '<circle cx="352" cy="520" r="9" fill="#ffadc6" opacity=".7"/><circle cx="448" cy="520" r="9" fill="#ffadc6" opacity=".7"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffd27a" opacity=".85"/>' for x, y, r in [(290, 380, 8), (520, 370, 6), (560, 450, 9), (250, 470, 5)]),
    sky("s5", [(0, "#151a45"), (.55, "#2f2d6b"), (1, "#5a4a8a")]),
)

# 6. Sep 2022 - DefectTrack: a telescope-microscope on a hill tracking glowing stars with coloured boxes and trails
stars = []
rnd = random.Random(42)
for i, (x, y, c) in enumerate([(200, 180, "#7cf29b"), (330, 120, "#ff9ad5"), (470, 210, "#ffd166"), (600, 140, "#7fd4ff"), (680, 270, "#c58bff"), (260, 320, "#ffb38a"), (520, 330, "#7cf29b")]):
    trail = f'<path d="M{x-90} {y+40} q 40 -10 {90-10} {-36}" stroke="{c}" stroke-width="4" fill="none" stroke-dasharray="6 9" opacity=".8"/>'
    stars.append(trail + f'<circle cx="{x}" cy="{y}" r="16" fill="#fff8d6" filter="url(#glow)"/><circle cx="{x}" cy="{y}" r="7" fill="#fffbe6"/><rect x="{x-24}" y="{y-24}" width="48" height="48" rx="6" fill="none" stroke="{c}" stroke-width="5"/><text x="{x+28}" y="{y-14}" font-family="Arial" font-weight="700" font-size="22" fill="{c}">{i+1}</text>')
SCENES["news_defecttrack"] = svg(
    sparkles(70, 6, (10, 10, 790, 520), ["#ffffff", "#dfe8ff"], 1, 3)
    + "".join(stars)
    + '<circle cx="680" cy="90" r="38" fill="#fff4cf"/><circle cx="696" cy="80" r="34" fill="#2a3166"/>'
    + hill("M0 600 Q240 520 470 580 T800 560 V800 H0Z", "#2d5a5a")
    + hill("M0 690 Q300 630 560 680 T800 670 V800 H0Z", "#244a4a")
    # microscope / telescope on the hill
    + '<g transform="translate(190 590)"><rect x="-40" y="40" width="110" height="18" rx="6" fill="#e9edf3"/><rect x="0" y="-60" width="22" height="100" rx="8" fill="#e9edf3"/><g transform="rotate(-38 10 -60)"><rect x="-10" y="-150" width="44" height="120" rx="14" fill="#f8fafc"/><rect x="-4" y="-170" width="32" height="30" rx="8" fill="#ffd166"/></g><circle cx="11" cy="-60" r="16" fill="#9aa8b7"/></g>'
    + robot(330, 690, .45, accent="#7cf29b", wave=True),
    sky("s6", [(0, "#0f1640"), (.6, "#28306e"), (1, "#3f4a8a")]),
)

# 7. Apr 2022 - single-nanoparticle oxidation: little planets with growing oxide 'coats' floating at sunset
planets = "".join(
    f'<circle cx="{x}" cy="{y}" r="{r+s}" fill="#5aa38c" opacity=".9"/><circle cx="{x}" cy="{y}" r="{r}" fill="#d9dee8"/><circle cx="{x-r*.35}" cy="{y-r*.35}" r="{r*.3}" fill="#fff" opacity=".85"/><ellipse cx="{x}" cy="{y}" rx="{(r+s)*1.6}" ry="{(r+s)*.38}" fill="none" stroke="#ffd166" stroke-width="5" opacity=".7" transform="rotate(-18 {x} {y})"/>'
    for x, y, r, s in [(180, 260, 20, 6), (330, 180, 34, 14), (520, 260, 52, 26), (650, 140, 16, 4), (430, 420, 26, 10)])
SCENES["news_oxidation"] = svg(
    clouds(8, 5, (40, 420, 760, 560), "#ffe0ec", .85)
    + radial("sun7", 400, 640, 420, [(0, "#fff2c7", 1), (.5, "#ffc79e", .6), (1, "#ff9fb2", 0)])
    + planets
    + sparkles(20, 13, (30, 40, 770, 460), ["#fff", "#fff3b0"], 2, 6)
    + hill("M0 680 Q200 630 420 660 T800 650 V800 H0Z", "#c86f8c")
    + hill("M0 730 Q300 700 560 728 T800 720 V800 H0Z", "#a8577a")
    + robot(620, 760, .5, accent="#ffd166", wave=True),
    sky("s7", [(0, "#8fb4ff"), (.45, "#c8a8ff"), (.8, "#ffb3c7"), (1, "#ffd3a8")]),
)

# 8. Sep 2019 - DefectSegNet: a magnifying glass over a steel landscape, revealing glowing segmented lines like a neural-network tree
lines = "".join(f'<path d="{d}" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>' for d, c in [
    ("M250 360 q60 40 120 10 t140 30", "#7cf2e0"), ("M270 450 q80 -30 150 20 t120 -10", "#ffd166"),
    ("M320 300 q20 60 -10 120 t30 120", "#7cf2e0"), ("M470 300 q-30 70 10 130 t-20 110", "#ff9ad5"),
    ("M240 520 q100 20 200 -10 t120 10", "#7cf2e0")])
SCENES["news_segmentation"] = svg(
    hill("M0 560 L120 420 L220 500 L360 330 L480 470 L600 360 L800 540 V800 H0Z", "#9aa7b8")
    + hill("M0 620 L160 520 L300 600 L470 500 L640 590 L800 520 V800 H0Z", "#7d8a9c")
    + hill("M0 700 Q240 660 480 690 T800 680 V800 H0Z", "#5f6b7d")
    + "".join(f'<path d="{d}" stroke="#4a5568" stroke-width="5" fill="none" opacity=".6"/>' for d in ["M80 640 q60 -30 120 0", "M520 650 q50 -40 110 -10", "M300 720 q80 -20 150 10"])
    + '<circle cx="400" cy="420" r="190" fill="#0f2537"/>'
    + f'<g>{lines}</g>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" opacity=".9"/>' for x, y in [(370, 370), (510, 400), (420, 470), (300, 420), (480, 330), (440, 530)])
    + '<circle cx="400" cy="420" r="190" fill="#bff6ff" opacity=".12"/>'
    + '<circle cx="400" cy="420" r="190" fill="none" stroke="#f3c26b" stroke-width="26"/>'
    + '<circle cx="400" cy="420" r="176" fill="none" stroke="#ffe3a3" stroke-width="6" opacity=".8"/>'
    + '<path d="M335 300 a150 150 0 0 1 120 -30" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".6"/>'
    + '<rect x="540" y="560" width="46" height="190" rx="20" fill="#b07a4f" transform="rotate(-38 563 655)"/>'
    + sparkles(14, 21, (60, 60, 740, 260), ["#fff", "#ffe08a"]),
    sky("s8", [(0, "#cfe3ff"), (.6, "#e9e4ff"), (1, "#fde8f1")]),
)

# 9. Apr 2023 - outstanding graduate student speaker: podium and microphone in a spotlight, confetti
def confetti(n, seed, box, colors):
    rnd = random.Random(seed); x0, y0, x1, y1 = box
    return "".join(f'<rect x="{rnd.uniform(x0, x1):.0f}" y="{rnd.uniform(y0, y1):.0f}" width="{rnd.uniform(8, 16):.0f}" height="{rnd.uniform(5, 9):.0f}" rx="2" fill="{rnd.choice(colors)}" transform="rotate({rnd.uniform(-60, 60):.0f} 400 400)"/>'
                   for _ in range(n))
curtain_l = ('<path d="M0 0 H190 Q150 200 196 400 Q160 600 206 800 H0Z" fill="#c0435b"/>'
             + "".join(f'<path d="M{x} 60 q-24 360 8 740" stroke="#9e3149" stroke-width="10" fill="none" opacity=".7"/>' for x in (50, 110, 160)))
curtain_r = f'<g transform="translate({W} 0) scale(-1 1)">{curtain_l}</g>'
valance = '<rect x="0" y="0" width="800" height="54" fill="#d4566c"/>' + "".join(f'<circle cx="{x}" cy="54" r="40" fill="#d4566c"/>' for x in range(40, 800, 80))
SCENES["news_speaker"] = svg(
    '<polygon points="320,0 480,0 640,800 160,800" fill="#fff4c4" opacity=".22"/>'
    + '<rect x="0" y="650" width="800" height="150" fill="#8a4a5c"/><rect x="0" y="650" width="800" height="12" fill="#a65d70"/>'
    + '<ellipse cx="400" cy="705" rx="250" ry="44" fill="#ffe9a8" opacity=".55"/>'
    + '<circle cx="400" cy="420" r="210" fill="#fff1b8" opacity=".25" filter="url(#glow)"/>'
    + curtain_l + curtain_r + valance
    # podium with a gold star
    + '<path d="M300 480 H500 L482 700 H318Z" fill="#f3e3c3"/><path d="M300 480 H340 L350 700 H318Z" fill="#e4cfa8"/>'
    + '<rect x="288" y="462" width="224" height="26" rx="9" fill="#fff3da"/>'
    + '<circle cx="400" cy="585" r="42" fill="#ffcf5a"/><circle cx="400" cy="585" r="34" fill="none" stroke="#fff3b0" stroke-width="4"/>'
    + '<path d="M400 560 L407 577 L425 578 L411 589 L416 607 L400 597 L384 607 L389 589 L375 578 L393 577Z" fill="#fff8dc"/>'
    # microphone and sound waves
    + '<path d="M420 466 q6 -40 30 -70" stroke="#4a4f63" stroke-width="8" fill="none" stroke-linecap="round"/>'
    + '<g transform="rotate(30 458 378)"><rect x="442" y="350" width="32" height="50" rx="16" fill="#4a4f63"/><rect x="446" y="354" width="24" height="26" rx="12" fill="#8e95ab"/></g>'
    + "".join(f'<path d="M{486+r*.3} {350-r*.6} a{r} {r} 0 0 1 {r*.2} {r*1.1}" stroke="#ffe08a" stroke-width="7" fill="none" stroke-linecap="round" opacity="{o}"/>' for r, o in [(30, .95), (55, .75), (80, .55)])
    # rosette ribbon
    + '<g transform="translate(300 250)"><path d="M-14 20 L-30 92 L-10 80 L0 100 L6 24Z" fill="#4f7cff"/><path d="M10 20 L30 92 L10 80 L0 100 L-4 24Z" fill="#7aa2ff"/>'
    + "".join(f'<circle cx="{34*math.cos(a):.1f}" cy="{34*math.sin(a):.1f}" r="16" fill="#ffd166"/>' for a in [i * math.pi / 6 for i in range(12)])
    + '<circle r="32" fill="#ffcf5a"/><circle r="22" fill="#fff3c4"/></g>'
    + confetti(46, 17, (210, 80, 600, 430), ["#ffd166", "#7cf2e0", "#ff9ad5", "#9db8ff", "#fff"])
    + sparkles(12, 23, (220, 90, 580, 440), ["#fff", "#ffe08a"]),
    sky("s9", [(0, "#2f2350"), (.55, "#5b3a78"), (1, "#a75a7a")]),
)

# 10. Aug 2022 - M&M 2022 Student Scholar Award (Portland): a gold medal before Mt. Hood, its face tracking a defect
medal_face = ('<path d="M352 448 q24 -10 40 -34" stroke="#7cf29b" stroke-width="5" fill="none" stroke-dasharray="6 7"/>'
              '<circle cx="404" cy="408" r="15" fill="#fff8d6" filter="url(#glow)"/><circle cx="404" cy="408" r="8" fill="#fffbe6"/>'
              '<rect x="380" y="384" width="48" height="48" rx="7" fill="none" stroke="#2f8f5f" stroke-width="6"/>')
SCENES["news_scholar"] = svg(
    clouds(5, 3, (60, 90, 740, 200), "#fff", .85)
    + '<path d="M90 640 L370 250 L410 268 L455 232 L720 640Z" fill="#8fa3c9"/>'
    + '<path d="M318 322 L370 250 L410 268 L455 232 L512 312 L486 322 L462 298 L438 330 L410 302 L382 334 L356 312Z" fill="#fbfcff"/>'
    + hill("M0 620 Q220 560 420 600 T800 580 V800 H0Z", "#7cc49a")
    + "".join(f'<path d="M{x} {y} l{-18*s} {50*s} h{36*s}Z M{x} {y+22*s} l{-22*s} {50*s} h{44*s}Z" fill="#3f7f63"/>' for x, y, s in [(70, 560, 1.1), (120, 580, .9), (690, 548, 1.2), (740, 570, .9), (640, 580, .8)])
    + hill("M0 700 Q300 660 560 696 T800 690 V800 H0Z", "#5fae86")
    # ribbon and medal
    + '<path d="M300 0 L380 330 L420 330 L360 0Z" fill="#4f7cff"/><path d="M500 0 L420 330 L380 330 L440 0Z" fill="#7aa2ff"/>'
    + '<path d="M336 0 L392 330 L404 330 L350 0Z M464 0 L408 330 L396 330 L450 0Z" fill="#fff" opacity=".7"/>'
    + '<circle cx="400" cy="420" r="130" fill="#fff1b8" opacity=".55" filter="url(#glow)"/>'
    + '<radialGradient id="gold" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff3c4"/><stop offset=".45" stop-color="#ffcf5a"/><stop offset="1" stop-color="#d99a2b"/></radialGradient>'
    + '<circle cx="400" cy="420" r="96" fill="url(#gold)"/><circle cx="400" cy="420" r="78" fill="none" stroke="#fff3c4" stroke-width="5" opacity=".9"/>'
    + '<circle cx="400" cy="420" r="66" fill="#ffe08a" opacity=".6"/>'
    + medal_face
    + robot(640, 770, .5, accent="#ff8a65", wave=True)
    + sparkles(18, 31, (80, 60, 720, 520), ["#fff", "#ffe08a", "#ffd1dc"]),
    sky("s10", [(0, "#bfe6ff"), (.6, "#ffe9cf"), (1, "#ffd6b5")]),
)

# 11. Aug 2021 - virtual M&M 2021 talk on nanocatalyst sintering: a laptop at night showing particles merge and split
def particle(x, y, r, mask):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffcf5a"/><circle cx="{x-r*.3}" cy="{y-r*.3}" r="{r*.3}" fill="#fff6d6"/>'
            f'<circle cx="{x}" cy="{y}" r="{r+6}" fill="none" stroke="{mask}" stroke-width="4" stroke-dasharray="7 5"/>')
screen = ('<rect x="200" y="280" width="400" height="230" rx="8" fill="#163445"/>'
          '<rect x="200" y="452" width="400" height="58" fill="#2d5566"/>'
          + particle(240, 440, 9, "#ff9ad5") + particle(266, 432, 7, "#7cf2e0") + particle(254, 410, 8, "#ffd166") + particle(282, 446, 6, "#9db8ff")
          + '<path d="M300 430 h36 m-12 -10 l12 10 l-12 10" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
          + particle(400, 426, 24, "#ff9ad5")
          + '<path d="M450 430 h36 m-12 -10 l12 10 l-12 10" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
          + particle(524, 440, 8, "#7cf2e0") + particle(552, 424, 9, "#ffd166") + particle(566, 448, 7, "#9db8ff") + particle(540, 410, 6, "#ff9ad5")
          + '<circle cx="222" cy="302" r="8" fill="#ff5c6c"/><rect x="520" y="296" width="64" height="44" rx="6" fill="#2d5566"/><circle cx="552" cy="312" r="8" fill="#9fc7d6"/><path d="M538 336 q14 -18 28 0" fill="#9fc7d6"/>')
SCENES["news_mm2021"] = svg(
    # window with night sky
    '<rect x="70" y="70" width="230" height="170" rx="12" fill="#2a3166"/><rect x="70" y="70" width="230" height="170" rx="12" fill="none" stroke="#f3e3c3" stroke-width="12"/>'
    + '<line x1="185" y1="70" x2="185" y2="240" stroke="#f3e3c3" stroke-width="8"/>'
    + '<circle cx="250" cy="120" r="22" fill="#fff4cf"/><circle cx="262" cy="112" r="20" fill="#2a3166"/>'
    + sparkles(8, 40, (90, 90, 280, 220), ["#fff", "#ffe08a"], 1.5, 3.5)
    # plant
    + '<path d="M690 600 L676 500 H744 L730 600Z" fill="#e08a5c"/>'
    + "".join(f'<path d="M710 500 q{dx} {-60} {dx*1.6} {-120}" stroke="#4fae7c" stroke-width="16" fill="none" stroke-linecap="round"/>' for dx in (-30, 0, 26))
    + '<rect x="0" y="600" width="800" height="200" fill="#c98b5b"/><rect x="0" y="600" width="800" height="14" fill="#a86d43"/>'
    # laptop
    + '<circle cx="400" cy="400" r="240" fill="#bff6ff" opacity=".18" filter="url(#glow)"/>'
    + '<rect x="180" y="260" width="440" height="270" rx="18" fill="#3a4060"/>' + screen
    + '<path d="M150 560 H650 L620 600 H180Z" fill="#d7dce6"/><rect x="150" y="548" width="500" height="16" rx="6" fill="#eef1f6"/>'
    # mug
    + '<rect x="90" y="530" width="60" height="70" rx="10" fill="#7c6cff"/><path d="M150 548 q26 6 0 36" stroke="#7c6cff" stroke-width="9" fill="none"/>'
    + "".join(f'<path d="M{x} 520 q-12 -20 0 -40 t0 -40" stroke="#fff" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/>' for x in (110, 130))
    + sparkles(10, 41, (320, 80, 740, 240), ["#fff", "#ffe08a"]),
    sky("s11", [(0, "#cbbcf2"), (.7, "#e9d8f4"), (1, "#f6e3ea")]),
)

# 12. Mar 2021 - tungsten oxidation (Materials Characterization): a tungsten cube on a hot plate,
#     growing a yellow oxide crust that is thick on one face and thin on another
def on_face(seed, A, B, D, n, smin, smax, cols):
    rnd = random.Random(seed); out = []
    for _ in range(n):
        u, v = rnd.uniform(.04, .96), rnd.uniform(.04, .96)
        x = A[0] + u * (B[0] - A[0]) + v * (D[0] - A[0]); y = A[1] + u * (B[1] - A[1]) + v * (D[1] - A[1])
        s = rnd.uniform(smin, smax)
        out.append(f'<rect x="{x-s/2:.1f}" y="{y-s/2:.1f}" width="{s:.1f}" height="{s*.7:.1f}" rx="{s*.2:.1f}" fill="{rnd.choice(cols)}" transform="rotate({rnd.uniform(-40, 40):.0f} {x:.1f} {y:.1f})"/>')
    return "".join(out)
ox = ["#f2d14b", "#e7c23a", "#d6d65a", "#ffe27a"]
o2 = "".join(f'<g transform="rotate({r} {x} {y})"><circle cx="{x-9}" cy="{y}" r="11" fill="#ff7b7b"/><circle cx="{x+9}" cy="{y}" r="11" fill="#ff9a9a"/></g>'
             for x, y, r in [(170, 300, 20), (250, 180, -15), (590, 200, 30), (650, 320, -10), (420, 150, 5)])
SCENES["news_matchar"] = svg(
    '<circle cx="400" cy="440" r="250" fill="#fff4cf" opacity=".5" filter="url(#glow)"/>'
    + hill("M0 650 Q260 610 520 640 T800 630 V800 H0Z", "#b9a6d9")
    + hill("M0 720 Q300 690 560 716 T800 710 V800 H0Z", "#a08cc7")
    # hot plate
    + '<rect x="190" y="580" width="420" height="80" rx="20" fill="#6a5a7a"/>'
    + '<ellipse cx="400" cy="580" rx="210" ry="40" fill="#ff9f6b"/><ellipse cx="400" cy="580" rx="230" ry="60" fill="#ff8a5b" opacity=".5" filter="url(#glow)"/>'
    + "".join(f'<ellipse cx="400" cy="580" rx="{r}" ry="{r*.19:.0f}" fill="none" stroke="#ffe08a" stroke-width="5"/>' for r in (70, 120, 170))
    + "".join(f'<path d="M{x} 560 q-12 -24 0 -48 t0 -48 t0 -48" stroke="#ffb36b" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>' for x in (230, 570, 610))
    # tungsten cube: thick oxide on the left face, medium on top, thin on the right
    + '<polygon points="280,360 400,420 400,570 280,510" fill="#b8c2d3" stroke="#f2d14b" stroke-width="22" stroke-linejoin="round"/>'
    + '<polygon points="280,360 400,300 520,360 400,420" fill="#e9edf5" stroke="#f2d14b" stroke-width="10" stroke-linejoin="round"/>'
    + '<polygon points="400,420 520,360 520,510 400,570" fill="#cdd5e2" stroke="#f2d14b" stroke-width="4" stroke-linejoin="round"/>'
    + on_face(1, (280, 360), (400, 420), (280, 510), 70, 14, 26, ox)
    + on_face(2, (280, 360), (400, 300), (400, 420), 26, 9, 16, ox)
    + on_face(3, (400, 420), (520, 360), (400, 570), 14, 4, 7, ox)
    + '<ellipse cx="446" cy="462" rx="8" ry="10" fill="#2a2f45"/><ellipse cx="482" cy="444" rx="8" ry="10" fill="#2a2f45"/>'
    + '<circle cx="449" cy="458" r="3" fill="#fff"/><circle cx="485" cy="440" r="3" fill="#fff"/>'
    + '<path d="M452 492 q20 4 34 -16" stroke="#2a2f45" stroke-width="5" fill="none" stroke-linecap="round"/>'
    + '<circle cx="432" cy="490" r="7" fill="#ffadc6" opacity=".7"/><circle cx="500" cy="462" r="7" fill="#ffadc6" opacity=".7"/>'
    + o2
    + sparkles(14, 12, (80, 60, 720, 280), ["#fff", "#ffe08a"]),
    sky("s12", [(0, "#d9d4ff"), (.6, "#f3e6ff"), (1, "#fff0d0")]),
)

# 13. Sep 2020 - DOE Office of Science highlight of DefectSegNet: a featured article with a segmented micrograph
micro = ('<rect x="220" y="250" width="360" height="210" rx="6" fill="#273a52"/>'
         + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#3b5270" opacity=".9"/>' for x, y, rx, ry in [(270, 300, 30, 18), (380, 330, 44, 22), (500, 290, 34, 20), (320, 410, 40, 20), (470, 400, 50, 24)])
         + "".join(f'<path d="{d}" stroke="{c}" stroke-width="5" fill="none" stroke-linecap="round"/>' for d, c in [
             ("M236 280 q60 30 120 0 t120 20 t90 -10", "#7cf2e0"), ("M240 360 q70 -30 150 10 t170 -20", "#ffd166"),
             ("M300 260 q-10 80 20 190", "#ff9ad5"), ("M450 262 q30 90 -10 190", "#7cf2e0")])
         + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="#fff" stroke-width="3"/>' for x, y in [(410, 300), (350, 380), (520, 360)]))
SCENES["news_doe"] = svg(
    clouds(14, 3, (60, 70, 740, 160), "#fff", .8)
    + hill("M0 640 Q240 600 470 630 T800 620 V800 H0Z", "#8fd3b6")
    + hill("M0 710 Q300 680 560 706 T800 700 V800 H0Z", "#6cbf9d")
    + '<rect x="192" y="166" width="440" height="470" rx="20" fill="#000" opacity=".12"/>'
    + '<rect x="180" y="150" width="440" height="470" rx="20" fill="#fffdf7"/>'
    + '<path d="M180 170 a20 20 0 0 1 20 -20 h400 a20 20 0 0 1 20 20 v60 h-440Z" fill="#2f6f9f"/>'
    + '<rect x="214" y="176" width="220" height="14" rx="7" fill="#fff"/><rect x="214" y="200" width="150" height="10" rx="5" fill="#cfe4f5"/>'
    + micro
    + "".join(f'<rect x="220" y="{y}" width="{w}" height="12" rx="6" fill="#d9dee8"/>' for y, w in [(490, 360), (516, 330), (542, 350), (568, 240)])
    + '<circle cx="606" cy="170" r="56" fill="#fff1b8" opacity=".6" filter="url(#glow)"/>'
    + '<circle cx="606" cy="170" r="44" fill="#ffcf5a"/><circle cx="606" cy="170" r="35" fill="none" stroke="#fff3c4" stroke-width="4"/>'
    + '<path d="M606 146 L613 163 L631 164 L617 175 L622 193 L606 183 L590 193 L595 175 L581 164 L599 163Z" fill="#fff8dc"/>'
    + robot(120, 770, .5, accent="#ffd166", wave=True)
    + sparkles(14, 15, (60, 60, 740, 300), ["#fff", "#ffe08a"]),
    sky("s13", [(0, "#cdeffd"), (.6, "#e3f7ef"), (1, "#fff3e0")]),
)

# 14. Mar 2020 - Scientific Reports Top 100 in Materials Science: a gold "100" trophy on a stack of journals
laurel = "".join(
    f'<ellipse cx="{400 + side*(150*math.sin(t))}" cy="{390 - 150*math.cos(t)}" rx="22" ry="10" fill="{c}" transform="rotate({side*(math.degrees(t)+60)} {400 + side*(150*math.sin(t))} {390 - 150*math.cos(t)})"/>'
    for side in (-1, 1) for t, c in [(1.2 + i*0.27, ["#5fae86", "#7cc49a"][i % 2]) for i in range(8)])
SCENES["news_top100"] = svg(
    hill("M0 680 Q240 640 470 670 T800 660 V800 H0Z", "#c9a7e8")
    + '<circle cx="400" cy="380" r="200" fill="#fff1b8" opacity=".45" filter="url(#glow)"/>'
    + laurel
    + "".join(book(x, y, w, 34, c) for x, y, w, c in [(250, 650, 300, "#5c6bc0"), (270, 616, 260, "#4db6ac"), (240, 582, 290, "#f06292"), (280, 548, 240, "#ffb74d")])
    # trophy cup
    + '<path d="M298 300 q-58 0 -50 60 q8 50 72 60" stroke="#e8a93a" stroke-width="16" fill="none"/><path d="M502 300 q58 0 50 60 q-8 50 -72 60" stroke="#e8a93a" stroke-width="16" fill="none"/>'
    + '<path d="M290 280 H510 Q505 440 400 460 Q295 440 290 280Z" fill="url(#gold)"/>'
    + '<radialGradient id="gold" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff3c4"/><stop offset=".45" stop-color="#ffcf5a"/><stop offset="1" stop-color="#d99a2b"/></radialGradient>'
    + '<rect x="384" y="456" width="32" height="50" fill="#e8a93a"/><rect x="330" y="500" width="140" height="40" rx="10" fill="#d99a2b"/><rect x="342" y="510" width="116" height="18" rx="6" fill="#ffcf5a"/>'
    + '<ellipse cx="400" cy="282" rx="110" ry="16" fill="#fff3c4"/>'
    + '<text x="400" y="392" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="64" fill="#b87a1e">100</text>'
    + confetti(40, 29, (150, 70, 650, 330), ["#ffd166", "#7cf2e0", "#ff9ad5", "#9db8ff", "#fff"])
    + sparkles(14, 33, (80, 60, 720, 300), ["#fff", "#ffe08a"]),
    sky("s14", [(0, "#c7dcff"), (.55, "#f0daff"), (1, "#ffe0e9")]),
)

# 15. Feb 2023 - Argonne feature story on DefectTrack: a story book on a snowy night, tracked "defects" flying out
fly = "".join(
    f'<path d="M400 520 Q{(400+x)/2 + 30} {(520+y)/2 + 40} {x} {y}" stroke="{c}" stroke-width="4" fill="none" stroke-dasharray="6 9" opacity=".7"/>'
    f'<circle cx="{x}" cy="{y}" r="15" fill="#fff8d6" filter="url(#glow)"/><circle cx="{x}" cy="{y}" r="7" fill="#fffbe6"/>'
    f'<rect x="{x-22}" y="{y-22}" width="44" height="44" rx="6" fill="none" stroke="{c}" stroke-width="5"/>'
    for x, y, c in [(220, 260, "#7cf29b"), (330, 170, "#ff9ad5"), (470, 150, "#ffd166"), (590, 230, "#7fd4ff"), (650, 360, "#c58bff"), (170, 390, "#ffb38a")])
snow = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".85"/>' for x, y, r in
               [(random.Random(i).uniform(10, 790), random.Random(i + 99).uniform(10, 600), random.Random(i + 7).uniform(2, 5)) for i in range(60)])
pine = lambda x, y, s: (f'<path d="M{x} {y} l{-40*s} {80*s} h{80*s}Z M{x} {y+40*s} l{-50*s} {90*s} h{100*s}Z" fill="#2f5d58"/>'
                        f'<path d="M{x} {y} l{-18*s} {36*s} q{18*s} {-8*s} {36*s} 0Z M{x} {y+40*s} l{-22*s} {40*s} q{22*s} {-8*s} {44*s} 0Z" fill="#fff" opacity=".9"/>')
SCENES["news_feature"] = svg(
    '<circle cx="660" cy="110" r="40" fill="#fff4cf"/><circle cx="676" cy="98" r="36" fill="#262d5e"/>'
    + snow + fly
    + hill("M0 600 Q240 540 460 580 T800 560 V800 H0Z", "#dfe7f5")
    + pine(90, 470, 1.1) + pine(170, 510, .8) + pine(700, 470, 1.0)
    + hill("M0 690 Q300 650 560 690 T800 680 V800 H0Z", "#eef3fb")
    # open book
    + '<circle cx="400" cy="560" r="170" fill="#fff4cf" opacity=".5" filter="url(#glow)"/>'
    + '<path d="M400 540 Q320 500 230 520 V640 Q320 620 400 660Z" fill="#fffdf5"/><path d="M400 540 Q480 500 570 520 V640 Q480 620 400 660Z" fill="#f6efe0"/>'
    + '<path d="M230 640 Q320 620 400 660 Q480 620 570 640 V656 Q480 636 400 676 Q320 636 230 656Z" fill="#c0435b"/>'
    + "".join(f'<path d="M{x0} {y} q40 -14 {dx} -4" stroke="#c8b98e" stroke-width="4" fill="none" stroke-linecap="round"/>' for x0, y, dx in [(250, 560, 120), (250, 584, 110), (250, 608, 90), (420, 556, 120), (420, 580, 110), (420, 604, 96)])
    + robot(640, 770, .48, accent="#7cf29b", wave=True),
    sky("s15", [(0, "#1d2550"), (.6, "#38407a"), (1, "#6b6fa8")]),
)

# 16. Jul 2025 - LLMOps talk at BISCUIT: a cheerful biscuit with chat bubbles and gears, next to a cup of tea
def gear(cx, cy, r, teeth, c):
    pts = []
    for i in range(teeth * 2):
        a = i * math.pi / teeth; rr = r if i % 2 == 0 else r * .78
        pts += [f"{cx + rr*math.cos(a - math.pi/teeth/2):.1f},{cy + rr*math.sin(a - math.pi/teeth/2):.1f}", f"{cx + rr*math.cos(a + math.pi/teeth/2):.1f},{cy + rr*math.sin(a + math.pi/teeth/2):.1f}"]
    return f'<polygon points="{" ".join(pts)}" fill="{c}"/><circle cx="{cx}" cy="{cy}" r="{r*.32}" fill="#ffe9cf"/>'
def bubble(x, y, w, c):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="60" rx="30" fill="{c}"/><path d="M{x+30} {y+56} l-12 22 l30 -18Z" fill="{c}"/>'
            + "".join(f'<circle cx="{x + w/2 + dx}" cy="{y+30}" r="7" fill="#fff"/>' for dx in (-22, 0, 22)))
SCENES["news_biscuit"] = svg(
    gear(170, 170, 60, 10, "#f4b183") + gear(250, 110, 38, 8, "#f6c39b") + gear(640, 150, 50, 9, "#f4b183")
    + bubble(300, 150, 150, "#7c9cff") + bubble(470, 230, 130, "#4fc3a1") + bubble(260, 270, 110, "#ff8fab")
    + '<rect x="0" y="600" width="800" height="200" fill="#b97a50"/><rect x="0" y="600" width="800" height="14" fill="#9c6340"/>'
    + '<ellipse cx="420" cy="610" rx="230" ry="40" fill="#fdf6ec"/><ellipse cx="420" cy="602" rx="200" ry="30" fill="#ffffff"/>'
    # biscuit
    + '<circle cx="420" cy="470" r="140" fill="#cf8a45"/><circle cx="420" cy="462" r="132" fill="#e2a65b"/><circle cx="420" cy="462" r="112" fill="#ebb76e"/>'
    + "".join(f'<circle cx="{420 + 80*math.cos(a):.0f}" cy="{462 + 80*math.sin(a):.0f}" r="6" fill="#b9783a"/>' for a in [i*math.pi/4 + .4 for i in range(8)])
    + '<ellipse cx="385" cy="450" rx="11" ry="14" fill="#5a3418"/><ellipse cx="455" cy="450" rx="11" ry="14" fill="#5a3418"/>'
    + '<circle cx="389" cy="445" r="4" fill="#fff"/><circle cx="459" cy="445" r="4" fill="#fff"/>'
    + '<path d="M395 488 q25 22 50 0" stroke="#5a3418" stroke-width="6" fill="none" stroke-linecap="round"/>'
    + '<circle cx="362" cy="482" r="11" fill="#ff9a7a" opacity=".6"/><circle cx="478" cy="482" r="11" fill="#ff9a7a" opacity=".6"/>'
    # teacup
    + '<path d="M90 520 H210 Q205 600 150 604 Q95 600 90 520Z" fill="#fff"/><path d="M208 540 q34 4 18 36 q-8 12 -24 12" stroke="#fff" stroke-width="10" fill="none"/>'
    + '<ellipse cx="150" cy="522" rx="60" ry="12" fill="#c98b5b"/><ellipse cx="150" cy="608" rx="80" ry="12" fill="#fff" opacity=".9"/>'
    + "".join(f'<path d="M{x} 500 q-12 -20 0 -40 t0 -40" stroke="#fff" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>' for x in (135, 165))
    + sparkles(12, 51, (60, 60, 740, 360), ["#fff", "#fff3b0"]),
    sky("s16", [(0, "#ffe9cf"), (.7, "#ffd9b5"), (1, "#ffc9a3")]),
)

# 17. Jul 2025 - TPC25 in San Jose, RAG search for the APS: a magnifier finding a document in a glowing network at sunset
rnd17 = random.Random(77)
nodes = [(rnd17.uniform(120, 680), rnd17.uniform(90, 400)) for _ in range(26)]
edges = "".join(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#ffe7f0" stroke-width="2.5" opacity=".55"/>'
                for i, a in enumerate(nodes) for b in nodes[i+1:] if math.dist(a, b) < 150)
dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#fff5d6" opacity=".7" filter="url(#glow)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fffbe6"/>' for x, y in nodes)
palm = lambda x, y, h: (f'<path d="M{x} {y} q10 {-h/2} {-6} {-h}" stroke="#3b2a5a" stroke-width="12" fill="none" stroke-linecap="round"/>'
                        + "".join(f'<path d="M{x-6} {y-h} q{dx*.5} {-30} {dx} {dy}" stroke="#3b2a5a" stroke-width="10" fill="none" stroke-linecap="round"/>' for dx, dy in [(-80, 10), (-60, 40), (70, 14), (56, 44), (0, -50)]))
SCENES["news_tpc"] = svg(
    '<circle cx="400" cy="600" r="150" fill="#ffe7a8"/><circle cx="400" cy="600" r="220" fill="#ffd29d" opacity=".5" filter="url(#glow)"/>'
    + edges + dots
    # magnifier showing a retrieved page
    + '<circle cx="470" cy="250" r="92" fill="#fffdf5" opacity=".95"/>'
    + '<rect x="438" y="206" width="64" height="86" rx="6" fill="#fff" stroke="#c8b98e" stroke-width="3"/>'
    + "".join(f'<line x1="448" y1="{y}" x2="{x2}" y2="{y}" stroke="#7c6cff" stroke-width="4" stroke-linecap="round"/>' for y, x2 in [(224, 492), (238, 488), (252, 492), (266, 478)])
    + '<circle cx="470" cy="250" r="92" fill="none" stroke="#f3c26b" stroke-width="20"/><circle cx="470" cy="250" r="80" fill="none" stroke="#ffe3a3" stroke-width="4" opacity=".8"/>'
    + '<rect x="540" y="320" width="34" height="140" rx="15" fill="#8a5a3c" transform="rotate(-40 557 390)"/>'
    + hill("M0 640 Q220 600 420 630 T800 610 V800 H0Z", "#5b3f7a")
    + hill("M0 710 Q300 680 560 706 T800 700 V800 H0Z", "#45306a")
    + palm(110, 700, 200) + palm(180, 720, 150) + palm(700, 700, 190)
    + sparkles(10, 79, (60, 60, 740, 300), ["#fff", "#ffe08a"]),
    sky("s17", [(0, "#6a5acd"), (.55, "#ff8fab"), (1, "#ffd29d")]),
)

# 18. Apr 2026 - Beams and Applications Seminar: a talk on AI for accelerator operations, ring + maintenance chart on screen
ring = ('<ellipse cx="270" cy="270" rx="100" ry="70" fill="none" stroke="#9db8ff" stroke-width="16"/>'
        + "".join(f'<rect x="{270 + 100*math.cos(a) - 7:.0f}" y="{270 + 70*math.sin(a) - 7:.0f}" width="14" height="14" rx="3" fill="#ffd166"/>' for a in [i*math.pi/5 for i in range(10)])
        + '<circle cx="370" cy="270" r="16" fill="#bff6ff" filter="url(#glow)"/><circle cx="370" cy="270" r="8" fill="#fff"/>'
        + '<circle cx="270" cy="270" r="26" fill="#7c6cff"/><path d="M258 270 l8 8 l14 -16" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>')
chart = ('<rect x="430" y="190" width="200" height="160" rx="10" fill="#f3f6fb"/>'
         + '<path d="M445 300 L480 296 L500 270 L515 310 L540 292 L565 296 L585 240 L600 250 L615 246" stroke="#3f9d8b" stroke-width="5" fill="none" stroke-linejoin="round"/>'
         + '<circle cx="585" cy="240" r="10" fill="#ff5c6c"/><circle cx="585" cy="240" r="20" fill="#ff5c6c" opacity=".3"/>'
         + '<g transform="translate(470 220) rotate(-35)"><rect x="-4" y="-2" width="8" height="34" rx="3" fill="#7d8a9c"/><circle cx="0" cy="-8" r="12" fill="#7d8a9c"/><rect x="-5" y="-22" width="10" height="14" fill="#f3f6fb"/></g>')
seats = "".join(f'<rect x="{x}" y="{y}" width="90" height="70" rx="22" fill="{c}"/>' for y, c, xs in [(610, "#5c6bc0", range(40, 800, 110)), (690, "#4a58a8", range(-15, 800, 110))] for x in xs)
heads = "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="{c}"/>' for x, y, c in [(85, 600, "#3a2e2a"), (305, 598, "#6b4a3a"), (525, 600, "#2f2a3a"), (690, 598, "#8a5a3c"), (140, 680, "#4a3a2e"), (470, 678, "#2f2a3a")])
SCENES["news_seminar"] = svg(
    '<rect x="112" y="72" width="576" height="366" rx="14" fill="#c9d1dc"/>'
    + '<rect x="130" y="90" width="540" height="330" rx="8" fill="#ffffff"/>'
    + '<rect x="130" y="90" width="540" height="64" fill="#2f5fa8"/><rect x="130" y="90" width="12" height="64" fill="#5aa0ff"/>'
    + '<rect x="160" y="108" width="300" height="14" rx="7" fill="#fff"/><rect x="160" y="130" width="200" height="10" rx="5" fill="#cfe0ff"/>'
    + '<g transform="translate(0 40)">' + ring + '</g>' + '<g transform="translate(0 30)">' + chart + '</g>'
    + '<path d="M370 310 q30 -30 60 -20" stroke="#9aa8b7" stroke-width="4" fill="none" stroke-dasharray="6 6"/>'
    + '<path d="M690 600 L676 520 H744 L730 600Z" fill="#e08a5c"/>'
    + "".join(f'<path d="M710 520 q{dx} -50 {dx*1.4} -100" stroke="#4fae7c" stroke-width="14" fill="none" stroke-linecap="round"/><circle cx="{710 + dx*1.4}" cy="420" r="12" fill="{c}"/>' for dx, c in [(-26, "#ff9ad5"), (0, "#ffd166"), (24, "#ff8a65")])
    + '<rect x="0" y="560" width="800" height="240" fill="#e6dccb"/>'
    + heads + seats
    + sparkles(10, 81, (140, 160, 660, 420), ["#ffd166", "#9db8ff"], 2, 5),
    sky("s18", [(0, "#dff0ff"), (.7, "#e9f6ec"), (1, "#f4f1e6")]),
)

if __name__ == "__main__":
    import sys
    from playwright.sync_api import sync_playwright
    out, only = sys.argv[1], set(sys.argv[2:])   # optional: names of scenes to render
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": W})
        for name, s in SCENES.items():
            if only and name not in only:
                continue
            pg.set_content(f'<html><body style="margin:0">{s}</body></html>')
            pg.screenshot(path=f"{out}/{name}.png", clip={"x": 0, "y": 0, "width": W, "height": W})
            print("rendered", name)
