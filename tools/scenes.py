"""Flat-colour scenes for the story's illustrations.

    python tools/scenes.py            # renders tools/out/*.png, then paints assets/img/wc/*.jpg

Each scene is drawn as plain SVG shapes, rendered with Chromium (Playwright),
and painted by tools/watercolor.py, so every illustration shares one hand.
"""
import math
import os
import random
import sys

import cv2

sys.path.insert(0, os.path.dirname(__file__))
from watercolor import watercolor  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "out")
DST = os.path.join(HERE, "..", "assets", "img", "wc")


def doc(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>')


def lin(id_, stops, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def cloud(x, y, s, fill="#fbf7ef", op=0.95):
    puffs = [(0, 0, 60), (55, -18, 48), (105, 2, 52), (-50, 8, 40), (150, 14, 36)]
    return "".join(f'<ellipse cx="{x + dx * s}" cy="{y + dy * s}" rx="{r * s * 1.25}" ry="{r * s * 0.8}" '
                   f'fill="{fill}" opacity="{op}"/>' for dx, dy, r in puffs)


def tree(x, y, s, c1="#4f7a4a", c2="#3b6340", trunk="#6b4f3a"):
    return (f'<rect x="{x - 4 * s}" y="{y - 30 * s}" width="{8 * s}" height="{30 * s}" fill="{trunk}"/>'
            f'<ellipse cx="{x}" cy="{y - 58 * s}" rx="{34 * s}" ry="{40 * s}" fill="{c1}"/>'
            f'<ellipse cx="{x + 12 * s}" cy="{y - 48 * s}" rx="{22 * s}" ry="{26 * s}" fill="{c2}"/>')


# ---------------------------------------------------------------- the ring ----

def scene_ring():
    """Aerial view of a storage-ring light source at dawn."""
    W, H = 1600, 900
    cx, cy = 800, 575
    defs = (lin("sky", [(0, "#a9c3d6"), (0.55, "#e9dcc4"), (1, "#f3d9b0")])
            + lin("field", [(0, "#b9c08a"), (1, "#8fa266")])
            + lin("roof", [(0, "#d9d6cf"), (1, "#b9b6b0")]))
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
         '<circle cx="1260" cy="250" r="70" fill="#fbe6b8" opacity=".9"/>',
         cloud(240, 150, 1.3), cloud(620, 95, 0.9), cloud(1050, 170, 1.1, op=0.8), cloud(1420, 110, 0.8)]
    # Fields to the horizon.
    b.append(f'<rect y="330" width="{W}" height="{H - 330}" fill="url(#field)"/>')
    for i, (y, c) in enumerate([(330, "#9aa9a0"), (352, "#a7b07c"), (382, "#c2b77e"), (420, "#9db06e")]):
        b.append(f'<path d="M0 {y} Q400 {y - 8} 800 {y + 3} T1600 {y - 2} V{H} H0Z" fill="{c}"/>')
    rnd = random.Random(3)
    for x in range(-20, W + 40, 26):  # distant tree line
        b.append(f'<ellipse cx="{x}" cy="{336 + rnd.uniform(-3, 3)}" rx="{rnd.uniform(18, 30)}" '
                 f'ry="{rnd.uniform(10, 16)}" fill="#6f8a6c" opacity=".9"/>')
    # Ring building: front wall, roof annulus, infield.
    ro_x, ro_y, ri_x, ri_y, wall = 600, 205, 500, 160, 46
    b.append(f'<ellipse cx="{cx}" cy="{cy + wall + 12}" rx="{ro_x + 30}" ry="{ro_y + 22}" fill="#7d8f5c" opacity=".55"/>')
    b.append(f'<path d="M{cx - ro_x} {cy} A{ro_x} {ro_y} 0 0 0 {cx + ro_x} {cy} V{cy + wall} '
             f'A{ro_x} {ro_y} 0 0 1 {cx - ro_x} {cy + wall}Z" fill="#a39f98"/>')
    for k in range(1, 40):  # wall panels
        t = math.pi * k / 40
        x = cx - ro_x * math.cos(t)
        y = cy + ro_y * math.sin(t)
        b.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + wall}" stroke="#8d8981" stroke-width="2"/>')
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{ro_x}" ry="{ro_y}" fill="url(#roof)"/>')
    # Lab and office modules on the outside of the ring.
    for ang in [200, 245, 290, 335, 20, 65, 110, 155]:
        t = math.radians(ang)
        x, y = cx + (ro_x + 40) * math.cos(t), cy + (ro_y + 16) * math.sin(t)
        s = 0.75 + 0.25 * (math.sin(t) + 1) / 2
        bw, bh, bd = 70 * s, 26 * s, 22 * s
        b.append(f'<rect x="{x - bw / 2}" y="{y - bh / 2}" width="{bw}" height="{bh}" fill="#ece6da"/>'
                 f'<rect x="{x - bw / 2}" y="{y + bh / 2}" width="{bw}" height="{bd}" fill="#b6ab98"/>'
                 + "".join(f'<rect x="{x - bw / 2 + 6 * s + i * 12 * s}" y="{y + bh / 2 + 6 * s}" '
                           f'width="{6 * s}" height="{8 * s}" fill="#6f7f8f"/>' for i in range(5)))
    b.append(f'<ellipse cx="{cx}" cy="{cy - 4}" rx="{ri_x}" ry="{ri_y}" fill="#8e9f62"/>')
    b.append(f'<path d="M{cx - ri_x} {cy - 4} A{ri_x} {ri_y} 0 0 1 {cx + ri_x} {cy - 4} '
             f'V{cy + 14} A{ri_x} {ri_y} 0 0 0 {cx - ri_x} {cy + 14}Z" fill="#9a968e"/>')
    b.append(f'<ellipse cx="{cx}" cy="{cy + 10}" rx="{ri_x - 4}" ry="{ri_y - 6}" fill="#a3b06e"/>')
    for i in range(26):  # infield trees
        t = rnd.uniform(0, 2 * math.pi)
        r = math.sqrt(rnd.uniform(0.05, 0.75))
        b.append(tree(cx + (ri_x - 60) * r * math.cos(t), cy + 30 + (ri_y - 40) * r * math.sin(t),
                      rnd.uniform(0.35, 0.55)))
    # The electron orbit and beamlines fanning out tangentially.
    b.append(f'<ellipse cx="{cx}" cy="{cy - 2}" rx="{(ro_x + ri_x) / 2}" ry="{(ro_y + ri_y) / 2}" '
             f'fill="none" stroke="#f0b44c" stroke-width="5" opacity=".95"/>')
    for ang in range(15, 360, 30):
        t = math.radians(ang)
        a, bb = (ro_x + ri_x) / 2, (ro_y + ri_y) / 2
        x0, y0 = cx + a * math.cos(t), cy - 2 + bb * math.sin(t)
        tx, ty = -a * math.sin(t), bb * math.cos(t)
        n = math.hypot(tx, ty)
        L = 95
        b.append(f'<line x1="{x0}" y1="{y0}" x2="{x0 + tx / n * L}" y2="{y0 + ty / n * L}" '
                 f'stroke="#e9a23b" stroke-width="3" opacity=".75"/>')
    # Foreground trees.
    for x, s in [(60, 2.2), (170, 1.7), (1450, 2.0), (1560, 2.4), (1330, 1.4), (300, 1.2)]:
        b.append(tree(x, H + 10, s, "#466b45", "#365a3a"))
    return W, H, doc(W, H, "".join(b), defs)


# ------------------------------------------------------------- microscope ----

def scene_microscope():
    """An environmental TEM in a lab, a nanoparticle on its monitor."""
    W, H = 1200, 900
    defs = lin("wall", [(0, "#efe3cf"), (1, "#e2d2b8")]) + lin("col", [(0, "#d8d5ce"), (0.5, "#f4f1ea"), (1, "#bdb9b1")], 1, 0)
    b = [f'<rect width="{W}" height="{H}" fill="url(#wall)"/>',
         # Window with daylight.
         '<rect x="70" y="120" width="300" height="380" fill="#c9dbe4"/>',
         '<rect x="70" y="120" width="300" height="380" fill="none" stroke="#a48f72" stroke-width="14"/>',
         '<line x1="220" y1="120" x2="220" y2="500" stroke="#a48f72" stroke-width="10"/>',
         '<path d="M80 470 Q160 420 220 450 T360 430 V490 H80Z" fill="#9db58a"/>',
         '<polygon points="370,120 520,900 120,900 70,500" fill="#fff6dc" opacity=".35"/>',
         # Floor.
         f'<rect y="760" width="{W}" height="140" fill="#b9a68a"/>',
         f'<rect y="760" width="{W}" height="10" fill="#a08c70"/>']
    # Console desk.
    b.append('<rect x="440" y="600" width="660" height="40" fill="#8f99a3"/>'
             '<rect x="460" y="640" width="620" height="140" fill="#a9b2ba"/>'
             '<rect x="480" y="660" width="170" height="100" fill="#99a3ad"/>'
             '<rect x="890" y="660" width="170" height="100" fill="#99a3ad"/>')
    # The column: gun tank, stacked lenses, specimen stage.
    x, wcol = 700, 150
    b.append(f'<rect x="{x - 120}" y="90" width="240" height="120" rx="60" fill="#c7cdd3"/>')
    b.append(f'<ellipse cx="{x}" cy="92" rx="120" ry="22" fill="#dfe4e8"/>')
    y = 200
    for i, (hh, ww) in enumerate([(70, wcol), (30, wcol + 40), (80, wcol), (30, wcol + 50),
                                  (60, wcol + 10), (26, wcol + 70), (70, wcol)]):
        c = "url(#col)" if i % 2 == 0 else "#7f8a94"
        b.append(f'<rect x="{x - ww / 2}" y="{y}" width="{ww}" height="{hh}" fill="{c}"/>')
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="{ww / 2}" ry="10" fill="#e9ecee"/>')
        y += hh
    b.append(f'<rect x="{x - 26}" y="{y - 140}" width="200" height="22" rx="8" fill="#5f6b76"/>')  # stage rod
    b.append(f'<circle cx="{x + 176}" cy="{y - 129}" r="18" fill="#3f4a55"/>')
    b.append(f'<rect x="{x - 110}" y="{y}" width="220" height="70" fill="#6e7a86"/>')  # viewing chamber
    b.append(f'<circle cx="{x}" cy="{y + 35}" r="22" fill="#2f5966"/><circle cx="{x}" cy="{y + 35}" r="10" fill="#7cc6c9"/>')
    # Monitor with a grainy micrograph and one particle with an oxide shell.
    b.append('<rect x="890" y="370" width="250" height="190" rx="6" fill="#2d3238"/>'
             '<rect x="904" y="384" width="222" height="162" fill="#7e8287"/>'
             '<circle cx="1010" cy="465" r="52" fill="#b9bcbf"/>'
             '<circle cx="1010" cy="465" r="36" fill="#55595e"/>'
             '<circle cx="955" cy="415" r="14" fill="#5d6166"/>'
             '<circle cx="1090" cy="520" r="18" fill="#5d6166"/><circle cx="1090" cy="520" r="26" fill="none" stroke="#b0b3b6" stroke-width="7"/>'
             '<rect x="1000" y="560" width="30" height="40" fill="#2d3238"/>')
    # Chair and a plant.
    b.append('<rect x="520" y="690" width="120" height="20" rx="8" fill="#3f566b"/>'
             '<rect x="560" y="710" width="12" height="60" fill="#2f3c48"/>'
             '<path d="M520 690 Q510 600 540 590 H610 Q640 600 630 690Z" fill="#4a6680"/>')
    b.append('<rect x="160" y="690" width="80" height="80" fill="#b2603e"/>'
             + "".join(f'<ellipse cx="{200 + dx}" cy="{650 + dy}" rx="18" ry="46" fill="#55804f" '
                       f'transform="rotate({r} {200 + dx} {650 + dy})"/>'
                       for dx, dy, r in [(-30, 0, -30), (0, -20, 0), (30, 0, 30), (-14, 20, -60), (16, 22, 60)]))
    # Electron beam, dashed down the column.
    b.append(f'<line x1="{x}" y1="150" x2="{x}" y2="{y + 20}" stroke="#7fd0f0" stroke-width="4" '
             f'stroke-dasharray="10 12" opacity=".8"/>')
    return W, H, doc(W, H, "".join(b), defs)


# ----------------------------------------------------------------- frames ----

def scene_frames():
    """Video frames from an in-situ experiment, with tracking boxes."""
    W, H = 1200, 900
    defs = ('<filter id="tem" x="0" y="0" width="100%" height="100%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="5"/>'
            '<feColorMatrix type="saturate" values="0"/>'
            '<feComponentTransfer><feFuncR type="linear" slope=".55" intercept=".2"/>'
            '<feFuncG type="linear" slope=".55" intercept=".2"/><feFuncB type="linear" slope=".55" intercept=".22"/></feComponentTransfer>'
            '</filter>')
    b = [f'<rect width="{W}" height="{H}" fill="#d7c7a9"/>',
         '<path d="M0 0 H1200 V900 H0Z" fill="#cdbb99" opacity=".5"/>']
    rnd = random.Random(11)
    colors = ["#e4572e", "#f3a712", "#29a3a3", "#7b5ea7", "#4f9d4f", "#d1495b"]
    frames = [(110, 140, -6), (430, 200, 3), (750, 130, -2), (260, 500, 4), (640, 520, -4)]
    defects = [(rnd.uniform(0.15, 0.85), rnd.uniform(0.15, 0.85), rnd.choice(colors), rnd.randint(12, 240))
               for _ in range(7)]
    for i, (fx, fy, rot) in enumerate(frames):
        fw, fh = 330, 250
        g = [f'<rect x="-12" y="-12" width="{fw + 24}" height="{fh + 46}" fill="#f6f1e6"/>',
             f'<rect width="{fw}" height="{fh}" fill="#888"/>',
             f'<rect width="{fw}" height="{fh}" filter="url(#tem)"/>']
        for j, (dx, dy, c, n) in enumerate(defects):
            if (i + j) % 3 == 0:
                continue
            px, py = dx * fw + (i - 2) * 6, dy * fh + (i % 2) * 5
            g.append(f'<ellipse cx="{px}" cy="{py}" rx="7" ry="5" fill="#2f2f33"/>'
                     f'<rect x="{px - 16}" y="{py - 16}" width="32" height="32" fill="none" stroke="{c}" stroke-width="4"/>'
                     f'<text x="{px - 12}" y="{py + 32}" font-family="Arial" font-weight="700" font-size="15" fill="#fff">{n}</text>')
        g.append(f'<rect x="16" y="{fh - 26}" width="60" height="7" fill="#fff"/>')
        g.append(f'<text x="{fw - 112}" y="30" font-family="Arial" font-size="22" font-weight="700" fill="#fff">{1.1 + i * 0.29:.2f} s</text>')
        b.append(f'<g transform="translate({fx} {fy}) rotate({rot})">{"".join(g)}</g>')
    # A pencil and a ruler on the desk.
    b.append('<g transform="rotate(-18 1000 780)"><rect x="840" y="770" width="300" height="20" fill="#f2c14e"/>'
             '<polygon points="1140,770 1175,780 1140,790" fill="#e8c9a0"/><rect x="820" y="770" width="24" height="20" fill="#d88a8a"/></g>')
    b.append('<g transform="rotate(8 200 830)"><rect x="40" y="815" width="360" height="40" fill="#e7dcc4"/>'
             + "".join(f'<line x1="{50 + k * 14}" y1="815" x2="{50 + k * 14}" y2="{830 if k % 5 else 840}" stroke="#7a6a50" stroke-width="2"/>' for k in range(25))
             + '</g>')
    return W, H, doc(W, H, "".join(b), defs)


# ---------------------------------------------------------------- tokamak ----

def scene_tokamak():
    """A fusion tokamak with its top cut away: the plasma ring glowing inside
    the vessel, copper field coils around it, tungsten tiles on the walls."""
    W, H = 1200, 900
    cx, cy = 600, 470
    defs = (lin("hall", [(0, "#27304a"), (1, "#454d66")])
            + lin("steel", [(0, "#a4acb8"), (1, "#6f7887")])
            + '<radialGradient id="glow"><stop offset="0" stop-color="#ffd6f6" stop-opacity=".9"/>'
              '<stop offset=".6" stop-color="#e08ad6" stop-opacity=".45"/><stop offset="1" stop-color="#b65fc0" stop-opacity="0"/></radialGradient>')
    b = [f'<rect width="{W}" height="{H}" fill="url(#hall)"/>',
         f'<rect y="760" width="{W}" height="140" fill="#3a3f52"/>',
         '<rect y="756" width="1200" height="8" fill="#555c73"/>']
    for x in range(60, W, 140):  # hall columns
        b.append(f'<rect x="{x}" y="0" width="34" height="760" fill="#323a52" opacity=".8"/>')
    ox, oy, ix, iy, wall = 450, 190, 170, 72, 170
    coil = "#c47a43"
    def coil_at(deg, front):
        t = math.radians(deg)
        x, y = cx + (ox + 18) * math.cos(t), cy + (oy + 8) * math.sin(t)
        w = 16 + 22 * abs(math.sin(t))
        h = wall + 36 if front else wall + 150
        top = y - 6 if front else y - 150
        return f'<rect x="{x - w / 2}" y="{top}" width="{w}" height="{h}" rx="{w / 2}" fill="{coil}"/>'
    angles = list(range(0, 360, 30))
    b += [coil_at(d, False) for d in angles if math.sin(math.radians(d)) < -0.05]
    # Outer face of the vessel (front half) and the floor shadow.
    b.append(f'<ellipse cx="{cx}" cy="{cy + wall + 20}" rx="{ox + 60}" ry="{oy + 30}" fill="#22283a" opacity=".6"/>')
    b.append(f'<path d="M{cx - ox} {cy} A{ox} {oy} 0 0 0 {cx + ox} {cy} V{cy + wall} A{ox} {oy} 0 0 1 {cx - ox} {cy + wall}Z" fill="url(#steel)"/>')
    for k in range(1, 18):  # vessel ports
        t = math.pi * k / 18
        x, y = cx - ox * math.cos(t), cy + oy * math.sin(t)
        b.append(f'<rect x="{x - 9}" y="{y + 50}" width="18" height="26" rx="4" fill="#59616f"/>')
    # Open top: dark interior, tiled inner wall, glowing plasma ring.
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{ox}" ry="{oy}" fill="#c3c9d1"/>')
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{ox - 22}" ry="{oy - 12}" fill="#1d2232"/>')
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{ox * 0.66}" ry="{oy * 0.62}" fill="url(#glow)"/>')
    for wdt, op, col in [(120, .22, "#c870c6"), (78, .42, "#e08ad6"), (44, .75, "#f3b6ee"), (16, .95, "#fff0fb")]:
        b.append(f'<ellipse cx="{cx}" cy="{cy - 6}" rx="{ox * 0.66}" ry="{oy * 0.6}" fill="none" stroke="{col}" stroke-width="{wdt}" opacity="{op}"/>')
    # Central column with tungsten tiles on its face.
    b.append(f'<ellipse cx="{cx}" cy="{cy - 8}" rx="{ix}" ry="{iy}" fill="#2a3044"/>')
    b.append(f'<path d="M{cx - ix + 40} {cy - 8} V{cy - 200} H{cx + ix - 40} V{cy - 8}Z" fill="#8a929f"/>')
    b.append(f'<ellipse cx="{cx}" cy="{cy - 200}" rx="{ix - 40}" ry="34" fill="#b7bdc6"/>')
    for r in range(6):
        for c in range(7):
            x = cx - ix + 46 + c * 31
            y = cy - 190 + r * 30
            b.append(f'<rect x="{x}" y="{y}" width="26" height="25" fill="#737b88"/>')
    b.append(f'<rect x="{cx - 34}" y="{cy - 330}" width="68" height="130" fill="{coil}"/>')  # solenoid
    b.append(f'<ellipse cx="{cx}" cy="{cy - 330}" rx="34" ry="10" fill="#dc9a68"/>')
    b += [coil_at(d, True) for d in angles if math.sin(math.radians(d)) >= -0.05]
    # Two people on the hall floor, for scale.
    for x in (1010, 1046):
        b.append(f'<circle cx="{x}" cy="{708}" r="9" fill="#e6d3bf"/><rect x="{x - 9}" y="{718}" width="18" height="40" rx="6" fill="#d8a23a"/>')
    return W, H, doc(W, H, "".join(b), defs)


# ---------------------------------------------------------------- fission ----

def scene_fission():
    """A pool-type fission research reactor seen from the bridge: the core
    glows Cherenkov blue under metres of water."""
    W, H = 1200, 900
    defs = (lin("water", [(0, "#2f6f8f"), (1, "#123a5a")])
            + '<radialGradient id="cher"><stop offset="0" stop-color="#d6f6ff" stop-opacity="1"/>'
              '<stop offset=".35" stop-color="#6fd3ff" stop-opacity=".85"/><stop offset="1" stop-color="#1f7fc4" stop-opacity="0"/></radialGradient>')
    b = [f'<rect width="{W}" height="{H}" fill="#d9d3c7"/>',
         # Pool rim, walls converging to the floor.
         '<polygon points="120,70 1080,70 1150,860 50,860" fill="#ece8df"/>',
         '<polygon points="170,110 1030,110 1090,820 110,820" fill="url(#water)"/>',
         '<polygon points="170,110 1030,110 830,330 370,330" fill="#3f86a6" opacity=".55"/>',
         '<polygon points="170,110 370,330 370,640 110,820" fill="#215a7c" opacity=".55"/>',
         '<polygon points="1030,110 830,330 830,640 1090,820" fill="#1c5172" opacity=".55"/>',
         '<polygon points="370,640 830,640 1090,820 110,820" fill="#0f3352" opacity=".5"/>']
    for k in range(1, 9):  # wall tiles
        y = 110 + k * 26
        b.append(f'<line x1="{170 - k * 7}" y1="{y + k * 2}" x2="{1030 + k * 7}" y2="{y + k * 2}" stroke="#5c9cba" stroke-width="2" opacity=".35"/>')
    # Cherenkov glow and the core: a grid of fuel assemblies.
    b.append('<ellipse cx="600" cy="500" rx="330" ry="250" fill="url(#cher)"/>')
    gx, gy, n, cell = 470, 400, 6, 44
    for r in range(n):
        for c in range(n):
            if (r in (0, n - 1)) and (c in (0, n - 1)):
                continue
            x, y = gx + c * cell, gy + r * cell * 0.8
            col = "#e9fbff" if (r + c) % 5 else "#9edfff"
            b.append(f'<rect x="{x}" y="{y}" width="{cell - 8}" height="{cell * 0.8 - 7}" rx="3" fill="{col}" opacity=".92"/>')
    for c in (1, 3, 5):  # control-rod drive lines rising out of the water
        x = gx + c * cell - 4
        b.append(f'<line x1="{x}" y1="{gy - 4}" x2="{x - 60 + c * 20}" y2="110" stroke="#a7c7d6" stroke-width="5" opacity=".75"/>')
    for k in range(9):  # light on the water surface
        y = 150 + k * 70
        b.append(f'<path d="M{180 + k * 10} {y} q120 -14 240 0 t240 0 t240 0" stroke="#bfe9ff" stroke-width="3" fill="none" opacity=".35"/>')
    # The bridge in the foreground, with a railing.
    b.append('<polygon points="0,800 1200,770 1200,900 0,900" fill="#b9b2a5"/>'
             '<polygon points="0,800 1200,770 1200,786 0,818" fill="#8f887c"/>')
    for x in range(20, 1200, 60):
        y = 800 - x * 30 / 1200
        b.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 64}" stroke="#d6a43a" stroke-width="6"/>')
    b.append('<line x1="0" y1="736" x2="1200" y2="706" stroke="#e0b24a" stroke-width="9"/>')
    return W, H, doc(W, H, "".join(b), defs)


# --------------------------------------------------------------- logbooks ----

def scene_logbooks():
    """A desk at night: logbooks, a laptop, threads of light to one answer."""
    W, H = 1200, 900
    defs = (lin("night", [(0, "#24304a"), (1, "#3b4766")])
            + '<radialGradient id="lamp" cx=".5" cy=".2" r=".8"><stop offset="0" stop-color="#ffe3a3" stop-opacity=".95"/>'
              '<stop offset="1" stop-color="#ffe3a3" stop-opacity="0"/></radialGradient>')
    b = [f'<rect width="{W}" height="{H}" fill="url(#night)"/>',
         # Window: the ring building lit at night.
         '<rect x="640" y="70" width="480" height="300" fill="#1b2438"/>',
         '<ellipse cx="880" cy="300" rx="200" ry="44" fill="#56607a"/>',
         '<ellipse cx="880" cy="296" rx="160" ry="32" fill="#2a3550"/>',
         '<ellipse cx="880" cy="298" rx="180" ry="38" fill="none" stroke="#f0b44c" stroke-width="3"/>'
         + "".join(f'<circle cx="{660 + k * 37}" cy="{100 + (k * 53) % 120}" r="2.5" fill="#f6efd8"/>' for k in range(13)),
         '<rect x="640" y="70" width="480" height="300" fill="none" stroke="#6b5844" stroke-width="16"/>',
         '<line x1="880" y1="70" x2="880" y2="370" stroke="#6b5844" stroke-width="10"/>',
         # Desk and lamp light.
         f'<rect y="560" width="{W}" height="{H - 560}" fill="#6b4a33"/>',
         f'<rect y="560" width="{W}" height="14" fill="#83593b"/>',
         '<ellipse cx="380" cy="620" rx="420" ry="220" fill="url(#lamp)"/>',
         '<path d="M150 560 L180 300 L230 300" stroke="#2f3540" stroke-width="12" fill="none"/>',
         '<path d="M200 270 L320 270 L350 330 L170 330Z" fill="#3e6f73"/>',
         '<rect x="100" y="550" width="120" height="16" rx="6" fill="#2f3540"/>']
    # Stacks of logbooks with labelled spines.
    spine = ["#a7443a", "#2f5d8a", "#c9973a", "#4a7a4f", "#7b5ea7", "#b9683d"]
    y = 548
    for i in range(6):
        w = 230 - (i % 2) * 14
        b.append(f'<rect x="{260 + (i % 3) * 6}" y="{y - 34}" width="{w}" height="34" fill="{spine[i]}"/>'
                 f'<rect x="{300 + (i % 3) * 6}" y="{y - 24}" width="70" height="12" fill="#efe4cc" opacity=".85"/>')
        y -= 34
    y = 548
    for i in range(4):
        b.append(f'<rect x="{30 + (i % 2) * 8}" y="{y - 40}" width="190" height="40" fill="{spine[(i + 2) % 6]}"/>'
                 f'<rect x="{60 + (i % 2) * 8}" y="{y - 26}" width="60" height="12" fill="#efe4cc" opacity=".85"/>')
        y -= 40
    # Open logbook.
    b.append('<path d="M250 700 Q380 670 520 705 L520 820 Q380 790 250 820Z" fill="#f6efdc"/>'
             '<path d="M520 705 Q660 670 790 700 L790 820 Q660 790 520 820Z" fill="#efe6cf"/>'
             + "".join(f'<line x1="{275}" y1="{720 + k * 16}" x2="{500 - (k % 3) * 30}" y2="{716 + k * 16}" stroke="#7c8aa6" stroke-width="3"/>' for k in range(5))
             + "".join(f'<line x1="{545}" y1="{716 + k * 16}" x2="{760 - (k % 2) * 40}" y2="{712 + k * 16}" stroke="#7c8aa6" stroke-width="3"/>' for k in range(5)))
    # Laptop with a chat.
    b.append('<polygon points="830,560 1130,560 1150,600 810,600" fill="#9aa3ad"/>'
             '<rect x="850" y="400" width="260" height="160" rx="6" fill="#2b3038"/>'
             '<rect x="862" y="412" width="236" height="136" fill="#f3f0e8"/>'
             '<rect x="940" y="426" width="146" height="26" rx="13" fill="#cfd9e8"/>'
             '<rect x="874" y="462" width="190" height="62" rx="12" fill="#ffffff"/>'
             '<rect x="886" y="476" width="150" height="7" fill="#9aa3ad"/><rect x="886" y="490" width="120" height="7" fill="#9aa3ad"/>'
             '<rect x="886" y="504" width="26" height="10" rx="3" fill="#e9a23b"/><rect x="918" y="504" width="26" height="10" rx="3" fill="#e9a23b"/>')
    # Threads of light from the books to the answer.
    for sx, sy in [(380, 380), (320, 470), (120, 430), (400, 720), (650, 720), (130, 520)]:
        b.append(f'<path d="M{sx} {sy} Q{(sx + 960) / 2} {min(sy, 490) - 120} 960 492" stroke="#f3c063" '
                 f'stroke-width="3" fill="none" opacity=".85"/>')
    return W, H, doc(W, H, "".join(b), defs)


# ---------------------------------------------------------------- skyline ----

def scene_skyline():
    """Chicago at dusk over Lake Michigan."""
    W, H = 1600, 700
    defs = lin("dusk", [(0, "#41456e"), (0.45, "#a0708a"), (0.8, "#f0a77a"), (1, "#f7cf98")])
    b = [f'<rect width="{W}" height="{H}" fill="url(#dusk)"/>', cloud(300, 120, 1.1, "#c78f9b", 0.6),
         cloud(1150, 90, 1.3, "#b88498", 0.5)]
    base = 470
    rnd = random.Random(7)
    x = 140
    while x < 1460:  # generic towers
        w = rnd.uniform(40, 90)
        h = rnd.uniform(60, 200)
        b.append(f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" fill="#3d3a55"/>')
        x += w + rnd.uniform(-10, 14)
    # Landmarks, simplified: a stepped black tower with twin antennas, a tapered one, a tall white slab.
    b.append(f'<path d="M560 {base} V{base - 330} H600 V{base - 400} H640 V{base - 360} H660 V{base}Z" fill="#2a2840"/>'
             f'<rect x="592" y="{base - 470}" width="5" height="70" fill="#2a2840"/><rect x="622" y="{base - 465}" width="5" height="65" fill="#2a2840"/>')
    b.append(f'<path d="M1060 {base} L1080 {base - 340} H1130 L1150 {base}Z" fill="#2d2b44"/>'
             f'<rect x="1092" y="{base - 410}" width="5" height="70" fill="#2d2b44"/><rect x="1114" y="{base - 410}" width="5" height="70" fill="#2d2b44"/>')
    b.append(f'<rect x="860" y="{base - 330}" width="70" height="330" fill="#4a4762"/>')
    b.append(f'<path d="M760 {base} V{base - 280} L800 {base - 330} L840 {base - 280} V{base}Z" fill="#35334e"/>')
    for k in range(260):  # lit windows
        wx, wy = rnd.uniform(150, 1450), rnd.uniform(base - 300, base - 10)
        b.append(f'<rect x="{wx}" y="{wy}" width="4" height="6" fill="#ffd98a" opacity="{rnd.uniform(.4, .9):.2f}"/>')
    # Lake with reflections.
    b.append(f'<rect y="{base}" width="{W}" height="{H - base}" fill="#5d6d8f"/>')
    for k in range(40):
        y = base + 10 + k * 5.5
        b.append(f'<line x1="{rnd.uniform(200, 900)}" y1="{y}" x2="{rnd.uniform(900, 1500)}" y2="{y}" '
                 f'stroke="#f0b48a" stroke-width="2.5" opacity="{0.45 - k * 0.01:.2f}"/>')
    return W, H, doc(W, H, "".join(b), defs)


SCENES = {
    "ring": (scene_ring, 2),
    "microscope": (scene_microscope, 5),
    "frames": (scene_frames, 9),
    "tokamak": (scene_tokamak, 4),
    "fission": (scene_fission, 12),
    "logbooks": (scene_logbooks, 8),
    "skyline": (scene_skyline, 6),
}


def main(names):
    from playwright.sync_api import sync_playwright
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(DST, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        for name in names:
            fn, seed = SCENES[name]
            w, h, svg = fn()
            pg = br.new_page(viewport={"width": w, "height": h})
            pg.set_content(f'<html><body style="margin:0">{svg}</body></html>')
            raw = os.path.join(RAW, f"{name}.png")
            pg.screenshot(path=raw)
            pg.close()
            out = watercolor(cv2.imread(raw), seed=seed)
            cv2.imwrite(os.path.join(DST, f"{name}.jpg"), out, [cv2.IMWRITE_JPEG_QUALITY, 84])
            print("painted", name)
        br.close()


if __name__ == "__main__":
    main(sys.argv[1:] or list(SCENES))
