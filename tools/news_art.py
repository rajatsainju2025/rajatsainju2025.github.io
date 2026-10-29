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
