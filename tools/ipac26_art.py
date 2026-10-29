# Regenerate: python tools/ipac26_art.py <outdir>   (needs: pip install playwright)
"""Scientific-style illustrations for the two IPAC'26 papers (rendered with Chromium)."""
import math, random

W, H = 1600, 880
FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"

DEFS = f"""<defs>
 <filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="#1e293b" flood-opacity=".16"/></filter>
 <filter id="sh2" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#1e293b" flood-opacity=".18"/></filter>
 <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
 <marker id="ar" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#64748b"/></marker>
 <marker id="arb" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#2563eb"/></marker>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8fafc"/><stop offset="1" stop-color="#eef2f7"/></linearGradient>
 <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2e8f0"/><stop offset=".5" stop-color="#f8fafc"/><stop offset="1" stop-color="#94a3b8"/></linearGradient>
 <linearGradient id="motor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset=".45" stop-color="#60a5fa"/><stop offset="1" stop-color="#1e3a8a"/></linearGradient>
 <linearGradient id="volute" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fb923c"/><stop offset=".5" stop-color="#fdba74"/><stop offset="1" stop-color="#c2410c"/></linearGradient>
 <linearGradient id="screen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#1e293b"/></linearGradient>
</defs>"""

def T(x, y, s, size=18, w=500, c="#1e293b", anchor="start", style=""):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{w}" fill="{c}" text-anchor="{anchor}" {style}>{s}</text>'

def card(x, y, w, h, fill="#ffffff", stroke="#e2e8f0", r=16, sh="sh"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" filter="url(#{sh})"/>'

def arrow(d, c="ar", col="#64748b", w=3, dash=""):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" marker-end="url(#{c})" {"stroke-dasharray=%s" % dash if dash else ""} stroke-linecap="round"/>'

def cylinder(x, y, w, h, top, side, label_icon=""):
    ry = w * 0.18
    return (f'<g filter="url(#sh2)"><path d="M{x} {y} v{h} a{w/2} {ry} 0 0 0 {w} 0 v{-h}" fill="{side}"/>'
            f'<ellipse cx="{x+w/2}" cy="{y}" rx="{w/2}" ry="{ry}" fill="{top}"/>'
            f'<path d="M{x} {y+h*0.4} a{w/2} {ry} 0 0 0 {w} 0" fill="none" stroke="#ffffff" stroke-opacity=".5" stroke-width="2"/></g>{label_icon}')

# ------------------------------------------------------------------ APS-RAG
def aps_rag():
    o = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    # faint storage-ring arcs in the background
    for r, op in [(980, .07), (1010, .05)]:
        o.append(f'<circle cx="800" cy="1500" r="{r}" fill="none" stroke="#2563eb" stroke-width="10" stroke-opacity="{op}"/>')
    o.append(T(60, 70, "APS-RAG", 34, 800, "#0f172a") + T(222, 70, "domain-aware hybrid retrieval for accelerator operations", 22, 400, "#475569"))

    # --- sources
    o.append(card(40, 110, 300, 470, "#ffffff"))
    o.append(T(190, 150, "Operational sources", 20, 700, "#0f172a", "middle"))
    src = [("BELY logbook", "#fde68a", "#f59e0b", "📓"), ("Teams ops chats", "#c7d2fe", "#6366f1", "💬"),
           ("ICMS documents", "#bae6fd", "#0284c7", "📄"), ("Work requests", "#fecaca", "#dc2626", "🔧")]
    for i, (name, top, side, ic) in enumerate(src):
        yy = 185 + i * 96
        o.append(cylinder(70, yy + 10, 64, 50, top, side))
        o.append(T(102, yy + 52, ic, 24, 400, "#000", "middle"))
        o.append(T(152, yy + 44, name, 19, 600, "#1e293b"))
    o.append(T(190, 560, "10,000+ unique documents", 17, 600, "#2563eb", "middle"))

    # --- ingestion -> indexes
    o.append(arrow("M340 300 C 390 300 400 250 450 250"))
    o.append(arrow("M340 420 C 390 420 400 450 450 450"))
    o.append(card(452, 120, 330, 210, "#eff6ff", "#bfdbfe"))
    o.append(T(617, 160, "Dense index", 22, 700, "#1d4ed8", "middle"))
    o.append(T(617, 188, "Qdrant · e5-large-v2 · 1024-d", 16, 500, "#334155", "middle"))
    rnd = random.Random(3)
    for i in range(70):  # embedding point cloud
        cx, cy = 617 + rnd.gauss(0, 70), 262 + rnd.gauss(0, 26)
        col = rnd.choice(["#60a5fa", "#818cf8", "#38bdf8", "#f59e0b", "#f87171"])
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rnd.uniform(2.5,5):.1f}" fill="{col}" opacity=".75"/>')
    o.append(card(452, 360, 330, 210, "#f0fdf4", "#bbf7d0"))
    o.append(T(617, 400, "Sparse index", 22, 700, "#15803d", "middle"))
    o.append(T(617, 428, "Elasticsearch · BM25", 16, 500, "#334155", "middle"))
    for i, (term, wt) in enumerate([("LTS:H1", .95), ("injection", .8), ("kicker", .7), ("RF trip", .55), ("S35", .4)]):
        yy = 455 + i * 21
        o.append(T(480, yy + 14, term, 15, 600, "#166534"))
        o.append(f'<rect x="580" y="{yy+3}" width="{170*wt:.0f}" height="13" rx="6" fill="#22c55e" opacity="{.35+.6*wt:.2f}"/>')

    # --- query path (bottom)
    o.append(card(40, 640, 420, 170, "#ffffff"))
    o.append(T(66, 680, "👤  Staff question", 19, 700, "#0f172a"))
    o.append(f'<rect x="66" y="700" width="368" height="86" rx="14" fill="#f1f5f9"/>')
    o.append(T(84, 735, "“Why did the beam dump during", 18, 500, "#334155"))
    o.append(T(84, 763, "injection last night?”", 18, 500, "#334155"))
    o.append(arrow("M460 725 L 520 725"))
    o.append(card(522, 640, 250, 170, "#ffffff"))
    o.append(T(647, 676, "Query preprocessing", 18, 700, "#0f172a", "middle"))
    for i, s in enumerate(["dates · acronyms · synonyms", "5 paraphrases (multi-query)"]):
        o.append(T(647, 712 + i * 30, s, 15.5, 500, "#475569", "middle"))
    o.append(f'<g>' + "".join(f'<rect x="{560+i*36}" y="{768}" width="28" height="18" rx="5" fill="#c7d2fe"/>' for i in range(5)) + '</g>')
    # parallel search arrows up to both indexes
    o.append(arrow("M700 640 C 720 600 760 560 760 572", dash="7 7"))
    o.append(arrow("M650 640 C 650 470 690 360 700 332", dash="7 7"))

    # --- fusion + rerank + LLM
    o.append(arrow("M782 225 C 840 225 850 330 880 360"))
    o.append(arrow("M782 465 C 840 465 850 420 880 400"))
    o.append(card(882, 300, 200, 170, "#fff7ed", "#fed7aa"))
    o.append(T(982, 340, "Reciprocal", 19, 700, "#c2410c", "middle") + T(982, 364, "Rank Fusion", 19, 700, "#c2410c", "middle"))
    for i, (wd, col) in enumerate([(120, "#fb923c"), (100, "#60a5fa"), (86, "#22c55e"), (70, "#fb923c"), (54, "#60a5fa")]):
        o.append(f'<rect x="{922}" y="{384+i*16}" width="{wd}" height="11" rx="5" fill="{col}" opacity=".8"/>')
    o.append(arrow("M1082 385 L 1130 385"))
    o.append(card(1132, 300, 200, 170, "#fdf4ff", "#f5d0fe"))
    o.append(T(1232, 340, "Cross-encoder", 19, 700, "#a21caf", "middle") + T(1232, 364, "rerank", 19, 700, "#a21caf", "middle"))
    for i, sc in enumerate([.97, .91, .84, .62]):
        o.append(f'<rect x="1162" y="{382+i*20}" width="{110*sc:.0f}" height="13" rx="6" fill="#d946ef" opacity="{.3+.65*sc:.2f}"/>' + T(1300, 393 + i * 20, f"{sc:.2f}", 13, 600, "#86198f", "end"))
    o.append(arrow("M1232 300 C 1232 250 1280 230 1300 230"))
    o.append(card(1302, 150, 260, 150, "#0f172a", "#0f172a"))
    o.append(f'<circle cx="1352" cy="225" r="34" fill="#38bdf8" opacity=".35" filter="url(#glow)"/>')
    o.append(f'<circle cx="1352" cy="225" r="24" fill="none" stroke="#7dd3fc" stroke-width="3"/>' + "".join(f'<circle cx="{1352+18*math.cos(a)}" cy="{225+18*math.sin(a)}" r="4" fill="#7dd3fc"/>' for a in [i*math.pi/3 for i in range(6)]))
    o.append(T(1395, 214, "LLM synthesis", 19, 700, "#f8fafc") + T(1395, 240, "via ARGO gateway", 16, 500, "#cbd5e1"))
    o.append(T(1395, 266, "top-k context in", 15, 500, "#94a3b8"))

    # --- answer card
    o.append(arrow("M1432 300 C 1432 360 1432 420 1432 520", "arb", "#2563eb"))
    o.append(card(1262, 522, 300, 290, "#ffffff", "#bfdbfe"))
    o.append(T(1286, 560, "✓ Answer with citations", 19, 700, "#1d4ed8"))
    for i in range(5):
        o.append(f'<rect x="1286" y="{582+i*26}" width="{[250,236,252,210,160][i]}" height="11" rx="5" fill="#e2e8f0"/>')
    chips = [("BELY_12345", "#f59e0b"), ("WRQ_678", "#dc2626"), ("ICMS_901", "#0284c7")]
    for i, (c, col) in enumerate(chips):
        x = 1286 + i * 94
        o.append(f'<rect x="{x}" y="725" width="86" height="28" rx="14" fill="{col}" opacity=".14" stroke="{col}"/>' + T(x + 43, 744, c, 12.5, 700, col, "middle"))
    o.append(T(1286, 790, "click → source record", 15, 500, "#64748b"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{"".join(o)}</svg>'

# ------------------------------------------------------------------ pump monitoring
def pump():
    o = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    o.append(T(60, 70, "Pump anomaly detection", 34, 800, "#0f172a") + T(470, 70, "low-cost vibration sensors + machine learning at the APS", 22, 400, "#475569"))
    # floor
    o.append(f'<path d="M30 640 L 640 640 L 600 700 L 0 700 Z" fill="#cbd5e1"/>')
    # --- pump assembly (side view)
    o.append('<g filter="url(#sh)">')
    o.append('<rect x="70" y="590" width="520" height="40" rx="6" fill="#64748b"/>')                       # skid
    o.append('<rect x="90" y="380" width="250" height="200" rx="26" fill="url(#motor)"/>')                  # motor
    for i in range(9): o.append(f'<rect x="{102+i*26}" y="388" width="10" height="184" rx="4" fill="#1e40af" opacity=".35"/>')  # fins
    o.append('<rect x="70" y="420" width="30" height="120" rx="10" fill="#1e3a8a"/>')                      # fan cover
    o.append('<rect x="338" y="455" width="70" height="50" rx="8" fill="url(#steel)"/>')                    # coupling guard
    o.append('<circle cx="485" cy="480" r="88" fill="url(#volute)"/>')                                       # volute
    o.append('<circle cx="485" cy="480" r="40" fill="#ea580c" opacity=".5"/>')
    o.append('<rect x="455" y="330" width="60" height="70" rx="6" fill="url(#steel)"/><rect x="440" y="318" width="90" height="22" rx="5" fill="#94a3b8"/>')  # discharge
    o.append('<rect x="560" y="455" width="80" height="50" rx="6" fill="url(#steel)"/><rect x="630" y="440" width="22" height="80" rx="5" fill="#94a3b8"/>')  # suction
    o.append('</g>')
    # pipes to the right edge (cooling water)
    o.append('<path d="M652 480 H 700" stroke="#94a3b8" stroke-width="40" stroke-linecap="butt"/>')
    o.append('<path d="M485 318 V 240 H 700" stroke="#94a3b8" stroke-width="34" fill="none"/>')
    o.append(T(600, 205, "≈10,000 gpm cooling water", 16, 600, "#475569", "middle"))
    # sensor in 3D-printed case on the motor housing
    o.append('<g filter="url(#sh2)"><rect x="300" y="430" width="54" height="40" rx="7" fill="#1e293b"/><rect x="306" y="436" width="42" height="28" rx="4" fill="#334155"/><circle cx="318" cy="450" r="4" fill="#22c55e"/></g>')
    # vibration rings
    for r, op in [(28, .5), (44, .32), (60, .18)]:
        o.append(f'<path d="M{327-r} {450-r*0.2} A{r} {r} 0 0 1 {327+r} {450-r*0.2}" fill="none" stroke="#22c55e" stroke-width="3" stroke-opacity="{op}"/>')
    o.append(card(150, 120, 330, 110, "#ffffff"))
    o.append(T(170, 156, "MEMS accelerometer", 19, 700, "#0f172a") + T(170, 182, "3-axis · flat to ~6 kHz", 16, 500, "#475569") + T(170, 206, "3D-printed case on the motor", 16, 500, "#475569"))
    o.append(arrow("M300 230 C 300 300 320 380 325 424", dash="6 6"))
    o.append(T(330, 760, "Helium pump (BLS) and storage-ring cooling-water pumps", 17, 600, "#334155", "middle"))

    # cable to edge node
    o.append('<path d="M354 450 C 420 420 640 640 720 640" fill="none" stroke="#0f172a" stroke-width="5"/>')
    # --- edge node
    o.append(card(720, 560, 210, 160, "#ffffff"))
    o.append('<rect x="745" y="585" width="160" height="60" rx="8" fill="#16a34a"/><rect x="757" y="597" width="40" height="36" rx="3" fill="#0f172a"/>' + "".join(f'<rect x="{807+i*14}" y="597" width="8" height="36" rx="2" fill="#bbf7d0"/>' for i in range(6)))
    o.append(T(825, 672, "Linux edge node", 18, 700, "#0f172a", "middle") + T(825, 696, "30-s segments · hourly features", 14.5, 500, "#475569", "middle"))
    o.append(arrow("M930 640 C 950 640 950 600 965 600"))
    # --- GPU + autoencoder
    o.append(card(965, 480, 250, 230, "#0f172a", "#0f172a"))
    o.append(T(1090, 516, "Autoencoder inference", 18, 700, "#f8fafc", "middle") + T(1090, 540, "GPU workstation · hourly", 14.5, 500, "#94a3b8", "middle"))
    layers = [5, 4, 2, 4, 5]
    pts = []
    for li, n in enumerate(layers):
        x = 1005 + li * 42
        col = []
        for k in range(n):
            y = 620 - (n - 1) * 15 + k * 30
            col.append((x, y))
        pts.append(col)
    for a, b in zip(pts, pts[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#38bdf8" stroke-opacity=".25" stroke-width="1.5"/>')
    for li, col in enumerate(pts):
        c = "#f472b6" if li == 2 else "#38bdf8"
        for (x, y) in col: o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}"/>')
    o.append(T(1090, 694, "learns normal vibration", 14, 500, "#cbd5e1", "middle"))
    o.append(arrow("M1150 480 C 1150 455 1190 430 1210 418"))

    # --- dashboard monitor
    o.append('<g filter="url(#sh)"><rect x="1150" y="105" width="420" height="300" rx="14" fill="#334155"/>'
             '<rect x="1164" y="119" width="392" height="262" rx="6" fill="url(#screen)"/>'
             '<rect x="1330" y="405" width="60" height="40" fill="#475569"/><rect x="1290" y="440" width="140" height="12" rx="6" fill="#475569"/></g>')
    # widgets on the screen
    o.append(T(1176, 142, "Pump health dashboard", 14, 700, "#e2e8f0"))
    # trend with anomaly
    rnd = random.Random(7); path = "M1176 210"
    for i in range(1, 46):
        x = 1176 + i * 4.2; y = 205 + rnd.gauss(0, 3) - (32 if i in (38, 39, 40) else 0)
        path += f" L{x:.1f} {y:.1f}"
    o.append('<rect x="1176" y="160" width="190" height="70" rx="4" fill="#0b1220"/>')
    o.append(f'<path d="{path}" fill="none" stroke="#38bdf8" stroke-width="2"/>')
    o.append('<rect x="1330" y="163" width="24" height="64" rx="3" fill="#ef4444" opacity=".22"/>')
    o.append(T(1180, 176, "RMS trend", 10, 600, "#94a3b8"))
    # spectrogram
    o.append('<rect x="1376" y="160" width="168" height="70" rx="4" fill="#0b1220"/>')
    vir = ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"]
    for i in range(28):
        for j in range(10):
            v = 0.15 + 0.25 * math.exp(-((j - 3) ** 2) / 2) + (0.6 if (i > 21 and j in (6, 7)) else 0) + rnd.uniform(0, .15)
            c = vir[min(4, int(v * 5))]
            o.append(f'<rect x="{1378+i*5.9:.1f}" y="{162+j*6.6:.1f}" width="5.9" height="6.6" fill="{c}"/>')
    o.append(T(1380, 176, "spectrogram", 10, 600, "#e2e8f0"))
    # PSD with baseline band
    o.append('<rect x="1176" y="242" width="368" height="124" rx="4" fill="#0b1220"/>')
    base = "M1186 350"; live = "M1186 350"
    for i in range(1, 70):
        x = 1186 + i * 5
        f = i / 69
        peak = 60 * math.exp(-((f - .2) ** 2) / .0012) + 34 * math.exp(-((f - .4) ** 2) / .0008)
        y = 345 - 12 * f - peak + rnd.gauss(0, 1.2)
        base += f" L{x} {y:.1f}"
        extra = 40 * math.exp(-((f - .6) ** 2) / .0007)
        live += f" L{x} {y - extra:.1f}"
    o.append(f'<path d="{base}" fill="none" stroke="#94a3b8" stroke-width="9" stroke-opacity=".55" stroke-linejoin="round"/>')
    o.append(f'<path d="{live}" fill="none" stroke="#f59e0b" stroke-width="2.2"/>')
    o.append('<circle cx="1394" cy="268" r="12" fill="none" stroke="#ef4444" stroke-width="2.5"/>')
    o.append(T(1186, 258, "PSD  ·  live vs rolling weekly baseline", 10.5, 600, "#94a3b8"))
    # anomaly score gauge under monitor
    o.append(card(1240, 500, 330, 120, "#ffffff"))
    o.append(T(1262, 534, "Anomaly score", 17, 700, "#0f172a"))
    o.append('<rect x="1262" y="555" width="286" height="18" rx="9" fill="#e2e8f0"/>'
             '<rect x="1262" y="555" width="150" height="18" rx="9" fill="#22c55e"/><rect x="1412" y="555" width="76" height="18" fill="#f59e0b"/><rect x="1488" y="555" width="60" height="18" rx="9" fill="#ef4444"/>')
    o.append('<path d="M1450 550 l-9 -14 h18 z" fill="#0f172a"/>' + T(1262, 600, "normal", 13, 600, "#16a34a") + T(1420, 600, "warning", 13, 600, "#d97706") + T(1500, 600, "alarm", 13, 600, "#dc2626"))
    o.append(arrow("M1420 452 C 1420 470 1420 480 1420 496", dash="5 6"))
    o.append(T(1405, 680, "Early warning →", 19, 700, "#1d4ed8", "middle") + T(1405, 706, "predictive maintenance", 19, 700, "#1d4ed8", "middle"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{"".join(o)}</svg>'


# ------------------------------------------------------------------ NAPAC 2025: transformer autoencoder
def napac():
    o = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    o.append(T(60, 70, "Water-pump vibration monitoring", 34, 800, "#0f172a") + T(612, 70, "low-cost sensors + transformer autoencoder", 22, 400, "#475569"))
    # --- pump (smaller), sensor on the coupler end
    g = []
    g.append('<path d="M20 600 L 520 600 L 490 650 L 0 650 Z" fill="#cbd5e1"/>')
    g.append('<g filter="url(#sh)">')
    g.append('<rect x="60" y="560" width="440" height="34" rx="6" fill="#64748b"/>')
    g.append('<rect x="78" y="380" width="210" height="170" rx="24" fill="url(#motor)"/>')
    g.extend(f'<rect x="{90+i*24}" y="388" width="9" height="154" rx="4" fill="#1e40af" opacity=".35"/>' for i in range(8))
    g.append('<rect x="60" y="410" width="26" height="110" rx="9" fill="#1e3a8a"/>')
    g.append('<rect x="286" y="440" width="66" height="50" rx="8" fill="url(#steel)"/>')
    g.append('<circle cx="420" cy="465" r="76" fill="url(#volute)"/><circle cx="420" cy="465" r="34" fill="#ea580c" opacity=".5"/>')
    g.append('<rect x="394" y="335" width="52" height="60" rx="6" fill="url(#steel)"/><rect x="380" y="325" width="80" height="18" rx="5" fill="#94a3b8"/>')
    g.append('</g>')
    o.extend(g)
    # sensor on coupler end + vibration arcs
    o.append('<g filter="url(#sh2)"><rect x="296" y="404" width="46" height="34" rx="6" fill="#1e293b"/><circle cx="309" cy="421" r="4" fill="#22c55e"/></g>')
    for r, op in [(24, .5), (38, .3), (52, .16)]:
        o.append(f'<path d="M{319-r} {421-r*0.2} A{r} {r} 0 0 1 {319+r} {421-r*0.2}" fill="none" stroke="#22c55e" stroke-width="3" stroke-opacity="{op}"/>')
    o.append(card(70, 125, 300, 92, "#ffffff"))
    o.append(T(90, 160, "Triaxial MEMS sensor", 19, 700, "#0f172a") + T(90, 188, "on the pump coupler end", 16, 500, "#475569"))
    o.append(arrow("M260 217 C 280 290 300 350 312 398", dash="6 6"))
    # Raspberry Pi + cloud
    o.append('<path d="M342 421 C 380 400 340 700 250 720" fill="none" stroke="#0f172a" stroke-width="4"/>')
    o.append(card(110, 690, 210, 110, "#ffffff"))
    o.append('<rect x="130" y="708" width="96" height="62" rx="6" fill="#16a34a"/><rect x="140" y="718" width="30" height="24" rx="3" fill="#0f172a"/>' + "".join(f'<circle cx="{182+i*9}" cy="{722}" r="3" fill="#fde68a"/>' for i in range(5)))
    o.append(T(236, 735, "Raspberry Pi", 15, 700, "#0f172a") + T(236, 756, "edge node", 14, 500, "#475569"))
    o.append(T(215, 788, "streams vibration data", 13.5, 500, "#475569", "middle"))
    o.append('<g transform="translate(400 740)"><circle cx="0" cy="0" r="26" fill="#bae6fd"/><circle cx="28" cy="-10" r="32" fill="#bae6fd"/><circle cx="60" cy="2" r="24" fill="#bae6fd"/><rect x="-4" y="0" width="68" height="26" fill="#bae6fd"/></g>')
    o.append(T(430, 752, "PC / cloud", 14, 700, "#0f172a", "middle"))
    o.append(arrow("M320 745 L 372 745"))
    o.append(arrow("M488 735 C 540 735 560 690 600 680"))

    # --- synthetic faults (top middle)
    o.append(card(600, 110, 420, 230, "#ffffff"))
    o.append(T(622, 146, "Physics-based synthetic faults", 19, 700, "#0f172a"))
    rnd = random.Random(11)
    rows = [("baseline", "#38bdf8", lambda t: math.sin(t) * 9), ("fault: added 0.5x", "#fb923c", lambda t: math.sin(t) * 9 + math.sin(t / 2) * 9),
            ("fault: growing 1x", "#ef4444", lambda t: math.sin(t) * (9 + t * 0.35))]
    for k, (lab, col, fn) in enumerate(rows):
        y0 = 192 + k * 52
        d = f"M760 {y0}"
        for i in range(1, 120):
            t = i * 0.5
            d += f" L{760 + i * 2.1:.1f} {y0 - fn(t) - rnd.gauss(0, 1.1):.1f}"
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.2"/>' + T(622, y0 + 5, lab, 14.5, 600, "#334155"))

    # --- transformer autoencoder (bottom middle)
    o.append(arrow("M810 340 L 810 386"))
    o.append(card(600, 388, 420, 330, "#0f172a", "#0f172a"))
    o.append(T(810, 424, "Transformer autoencoder", 19, 700, "#f8fafc", "middle") + T(810, 448, "self-attention · sinusoidal position encoding", 14, 500, "#94a3b8", "middle"))
    def stack(x, title, blocks, col):
        out = T(x + 70, 486, title, 15, 700, "#e2e8f0", "middle")
        for i, (b, c) in enumerate(blocks):
            out += f'<rect x="{x}" y="{500+i*38}" width="140" height="30" rx="7" fill="{c}"/>' + T(x + 70, 520 + i * 38, b, 13, 700, "#0f172a", "middle")
        return out
    o.append(stack(628, "Encoder", [("Add & Norm", "#bbf7d0"), ("Feed forward", "#bfdbfe"), ("Add & Norm", "#bbf7d0"), ("Self-attention", "#fed7aa")], "#38bdf8"))
    o.append(stack(852, "Decoder", [("Add & Norm", "#bbf7d0"), ("Feed forward", "#bfdbfe"), ("Enc-dec attention", "#fed7aa"), ("Self-attention", "#fed7aa")], "#38bdf8"))
    o.append(arrow("M770 580 L 848 580", col="#94a3b8"))
    # input window and reconstruction strip
    d1, d2 = "M630 690", "M818 690"
    for i in range(1, 80):
        y = 690 - math.sin(i * 0.45) * 8 - rnd.gauss(0, 1.5)
        if i < 50: d1 += f" L{630 + i * 3.6:.1f} {y:.1f}"
        else: d2 += f" L{818 + (i - 50) * 5.6:.1f} {y:.1f}"
    o.append('<rect x="626" y="672" width="186" height="36" rx="6" fill="#0b1220" stroke="#94a3b8" stroke-dasharray="4 4"/>' + f'<path d="{d1}" fill="none" stroke="#38bdf8" stroke-width="2"/>')
    o.append('<rect x="814" y="672" width="180" height="36" rx="6" fill="#0b1220" stroke="#22c55e"/>' + f'<path d="{d2}" fill="none" stroke="#22c55e" stroke-width="2"/>')
    o.append(T(719, 666, "input window", 12, 600, "#94a3b8", "middle") + T(904, 666, "predicted next steps", 12, 600, "#94a3b8", "middle"))

    # --- order spectrum (top right)
    o.append(arrow("M1020 550 C 1050 550 1050 300 1078 290"))
    o.append(card(1080, 110, 490, 330, "#ffffff"))
    o.append(T(1102, 146, "Order spectrum (vdB)", 19, 700, "#0f172a") + T(1548, 146, "1x = 44.4 Hz", 15, 700, "#1d4ed8", "end"))
    orders = ["0.5x", "1x", "1.5x", "2x", "3x", "4x", "5x"]
    base = [22, 130, 30, 62, 38, 26, 18]
    live = [92, 186, 96, 70, 44, 30, 20]
    for i, (lab, b, l) in enumerate(zip(orders, base, live)):
        x = 1112 + i * 64
        o.append(f'<rect x="{x}" y="{400-b}" width="22" height="{b}" rx="4" fill="#94a3b8"/>')
        o.append(f'<rect x="{x+26}" y="{400-l}" width="22" height="{l}" rx="4" fill="{"#ef4444" if l - b > 30 else "#fb923c"}"/>')
        o.append(T(x + 24, 424, lab, 13.5, 700, "#334155", "middle"))
    o.append('<rect x="1340" y="170" width="14" height="14" rx="3" fill="#94a3b8"/>' + T(1360, 182, "baseline", 13.5, 600, "#475569"))
    o.append('<rect x="1440" y="170" width="14" height="14" rx="3" fill="#ef4444"/>' + T(1460, 182, "live", 13.5, 600, "#475569"))
    # --- weighted anomaly score (bottom right)
    o.append(card(1080, 470, 490, 248, "#ffffff"))
    o.append(T(1102, 506, "Weighted anomaly score", 19, 700, "#0f172a") + T(1548, 506, "wear progression", 14, 500, "#64748b", "end"))
    o.append('<rect x="1104" y="526" width="442" height="54" fill="#fecaca" opacity=".55"/><rect x="1104" y="580" width="442" height="44" fill="#fde68a" opacity=".55"/><rect x="1104" y="624" width="442" height="66" fill="#bbf7d0" opacity=".55"/>')
    o.append(T(1112, 545, "alarm", 12.5, 700, "#dc2626") + T(1112, 597, "warning", 12.5, 700, "#d97706") + T(1112, 682, "normal", 12.5, 700, "#16a34a"))
    d = "M1160 676"
    for i in range(1, 76):
        x = 1160 + i * 5
        y = 676 - 3 * math.exp(i / 17.5) + rnd.gauss(0, 2.2)
        d += f" L{x} {max(532, y):.1f}"
    o.append(f'<path d="{d}" fill="none" stroke="#1d4ed8" stroke-width="3" stroke-linejoin="round"/>')
    o.append(T(1325, 790, "Early fault detection → less downtime", 19, 700, "#1d4ed8", "middle"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{"".join(o)}</svg>'

# Warm editorial palette (ink navy, deep teal, terracotta, mustard, sage, plum on ivory),
# chosen to sit on the site's cream background. Every colour above is remapped here.
PALETTE = {
 "#0f172a": "#2b2d42", "#1e293b": "#2b2d42", "#334155": "#3d405b", "#475569": "#5c5f6b",
 "#64748b": "#7a7468", "#94a3b8": "#a39d91", "#cbd5e1": "#ddd5c4", "#e2e8f0": "#e4dccd",
 "#f1f5f9": "#f1ebdf", "#f8fafc": "#fbf8f1", "#eef2f7": "#efe8da", "#ffffff": "#fffdf8",
 "#0b1220": "#23253a",
 "#2563eb": "#2a6f73", "#1d4ed8": "#2a6f73", "#60a5fa": "#5a9ea1", "#3b82f6": "#3d8b8f",
 "#1e3a8a": "#1f4f52", "#1e40af": "#1f4f52", "#0284c7": "#3d8b8f", "#bae6fd": "#a8cfc9",
 "#bfdbfe": "#b9d8d2", "#eff6ff": "#e9f2f0", "#38bdf8": "#7fc4b2", "#7dd3fc": "#9fd3c4",
 "#22c55e": "#81b29a", "#16a34a": "#4f8a6e", "#15803d": "#4f8a6e", "#166534": "#3f6f57",
 "#bbf7d0": "#c9dfd2", "#f0fdf4": "#eef5ef",
 "#fb923c": "#e07a5f", "#fdba74": "#f2a48a", "#ea580c": "#c8553d", "#c2410c": "#a8432f",
 "#fff7ed": "#fbeee6", "#fed7aa": "#efc3b3", "#ef4444": "#c8553d", "#dc2626": "#c8553d",
 "#f87171": "#e07a5f", "#fecaca": "#f2b8a2",
 "#f59e0b": "#e0a458", "#fde68a": "#f2cc8f", "#d97706": "#b7832f", "#f472b6": "#e0a458",
 "#a21caf": "#6d597a", "#86198f": "#5b4766", "#d946ef": "#8f6f9e", "#fdf4ff": "#f3eef5",
 "#f5d0fe": "#d9cbe0", "#6366f1": "#6d597a", "#818cf8": "#a58bb0", "#c7d2fe": "#c9bcd1",
 # spectrogram colormap (was viridis)
 "#440154": "#2b2d42", "#3b528b": "#6d597a", "#21918c": "#b56576", "#5ec962": "#e07a5f", "#fde725": "#f2cc8f",
}

def recolor(svg):
    import re
    return re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: PALETTE.get(m.group(0).lower(), m.group(0)), svg)

if __name__ == "__main__":
    import sys
    from playwright.sync_api import sync_playwright
    out = sys.argv[1]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for name, svg in [("ipac26_apsrag", recolor(aps_rag())), ("ipac26_pumps", recolor(pump())), ("napac2025_art", recolor(napac()))]:
            pg.set_content(f'<html><body style="margin:0">{svg}</body></html>'); pg.wait_for_timeout(200)
            pg.screenshot(path=f"{out}/{name}.png", clip={"x": 0, "y": 0, "width": W, "height": H}); print("rendered", name)
