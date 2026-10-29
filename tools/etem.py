"""Simulated in-situ ETEM frames of Ni nanoparticles oxidizing at 600 °C.

    python tools/etem.py OUT_DIR

Writes, for every time step (0.5 s apart), a bright-field frame (grey PNG), a
segmentation mask (RGBA PNG: metal green, oxide red, void turquoise, the
paper's colours), the outline of each phase and each particle's normalized NiO
volume fraction alpha (JSON), for the "by hand vs. by model" animations.

The geometry follows Sainju et al., ACS Nano 2022: a large particle
(Ø 43.8 nm) whose primary void appears at t = 3.5 s and which is fully
oxidized at t = 59.5 s (Fig. 2a), a medium one (Ø 14.3 nm) that ends with a
centred void, and a small one (Ø 8.6 nm) that becomes solid oxide. Stage 1
oxide eats inward by the critical thickness of 5.52 nm; stage 2 follows a
parabolic (Wagner) law. The frames are an illustration, not data.
"""
import json
import math
import os
import sys

import cv2
import numpy as np

W, H = 800, 450
PX = 4.0                    # pixels per nm
H_CRIT = 5.52               # critical thickness, nm
PBR = 1.65                  # NiO / Ni volume ratio
MU_METAL, MU_OXIDE = 0.0080, 0.0040   # attenuation per pixel of thickness
KEY_TIMES = [0.0, 3.5, 59.5]

PARTICLES = [
    # centre (px), starting radius (nm), facet phase, void direction (radians, image coords)
    dict(name="large", c=(300, 232), r0=43.8 / 2, t_void=3.0, t_end=59.5, phase=0.4, fast=math.radians(225)),
    dict(name="medium", c=(574, 148), r0=14.3 / 2, t_void=1.5, t_end=2.5, phase=1.3, fast=math.radians(200)),
    dict(name="small", c=(662, 322), r0=8.6 / 2, t_void=None, t_end=1.0, phase=2.1, fast=0.0),
    dict(name="small2", c=(118, 96), r0=6.4 / 2, t_void=None, t_end=0.8, phase=0.7, fast=0.0),
]


def fbm(h, w, scale, octaves, rng):
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        s = max(2, int(scale / 2 ** o))
        g = rng.random((h // s + 2, w // s + 2)).astype(np.float32)
        out += amp * cv2.resize(g, (g.shape[1] * s, g.shape[0] * s), interpolation=cv2.INTER_CUBIC)[:h, :w]
        total += amp
        amp *= 0.5
    out /= total
    return (out - out.min()) / (np.ptp(out) + 1e-6)


def state(p, t):
    """Radii (nm) and centre offsets (nm) of outer surface, cavity and metal core."""
    r0 = p["r0"]
    hollow = r0 > H_CRIT
    t1 = p["t_void"] if hollow else p["t_end"]
    s1 = min(1.0, t / t1)
    s1 = (1 - math.exp(-(s1 * 2.2) ** 2)) / (1 - math.exp(-2.2 ** 2))   # Avrami-Erofeev-like
    if not hollow or t <= t1:
        core = r0 - min(H_CRIT, r0) * s1
        cav, off_cav, off_core = core, 0.0, 0.0
        outer = (core ** 3 + PBR * (r0 ** 3 - core ** 3)) ** (1 / 3)
        return outer, cav, core, off_cav, off_core
    s2 = min(1.0, math.sqrt((t - t1) / (p["t_end"] - t1)))              # Wagner, parabolic
    cav = r0 - H_CRIT
    core = cav * (1 - s2) ** (1 / 3)
    outer = (cav ** 3 + PBR * (r0 ** 3 - core ** 3)) ** (1 / 3)
    off_cav = (outer - cav) * (0.42 if p["name"] == "large" else 0.0) * s2   # shell thickens on one side
    off_core = cav - core                                                    # core rests on the slow side
    return outer, cav, core, off_cav, off_core


def render(t, bg, grain, grains_id, grain_gain, yy, xx):
    atten = np.zeros((H, W), np.float32)
    fringe = np.zeros((H, W), np.float32)
    labels = np.zeros((H, W), np.uint8)        # 0 none, 1 metal, 2 oxide, 3 void
    outlines = {}
    for p in PARTICLES:
        outer, cav, core, off_cav, off_core = state(p, t)
        cx, cy = p["c"]
        ux, uy = math.cos(p["fast"]), math.sin(p["fast"])
        ccx, ccy = cx + ux * off_cav * PX, cy + uy * off_cav * PX            # cavity centre
        kx, ky = ccx - ux * off_core * PX, ccy - uy * off_core * PX          # core centre
        def shape(x0, y0):
            """Irregular, slightly faceted outline, the same for every surface of a particle."""
            th = np.arctan2(yy - y0, xx - x0)
            ph = p["phase"]
            return (1 + 0.045 * np.cos(2 * th + ph) + 0.03 * np.cos(3 * th + 2.1 * ph)
                    + 0.012 * np.cos(6 * th + ph)), np.hypot(xx - x0, yy - y0)
        f_o, rho_o = shape(cx, cy)
        f_a, rho_a = shape(ccx, ccy)
        f_c, rho_c = shape(kx, ky)
        R = outer * PX * f_o
        T_out = 2 * np.sqrt(np.clip(R ** 2 - rho_o ** 2, 0, None))
        T_cav = 2 * np.sqrt(np.clip((cav * PX * f_a) ** 2 - rho_a ** 2, 0, None))
        T_core = 2 * np.sqrt(np.clip((core * PX * f_c) ** 2 - rho_c ** 2, 0, None))
        oxide_T = np.clip(T_out - T_cav, 0, None)
        atten += MU_OXIDE * oxide_T * grain_gain[grains_id] + MU_METAL * T_core * (1 + 0.12 * np.sin(0.06 * (xx * 0.8 + yy * 0.6)))
        o_mask = rho_o < R
        a_mask = rho_a < cav * PX * f_a
        c_mask = rho_c < core * PX * f_c
        labels[o_mask] = 2
        labels[a_mask & o_mask] = 3
        labels[c_mask] = 1
        # Fresnel fringes: bright just outside the particle, darker just inside; faint at the void.
        m = o_mask.astype(np.uint8)
        d_out = cv2.distanceTransform(1 - m, cv2.DIST_L2, 3)
        d_in = cv2.distanceTransform(m, cv2.DIST_L2, 3)
        fringe += 16 * np.exp(-(d_out / 1.4) ** 2) * (d_out > 0) - 9 * np.exp(-(d_in / 1.6) ** 2) * (d_in > 0)
        v = (a_mask & ~c_mask & o_mask).astype(np.uint8)
        if v.any():
            dv = cv2.distanceTransform(v, cv2.DIST_L2, 3)
            fringe += 7 * np.exp(-(dv / 1.5) ** 2) * (dv > 0)
        outlines[p["name"]] = {k: contour(mk) for k, mk in
                               [("oxide", o_mask), ("metal", c_mask), ("void", a_mask & ~c_mask & o_mask)]}
        if t == 0:
            outlines[p["name"]]["oxide"] = []           # nothing has oxidized yet
    img = bg * np.exp(-atten) + fringe
    img = cv2.GaussianBlur(img, (0, 0), 0.75) + grain
    return np.clip(img, 0, 255).astype(np.uint8), labels, outlines


def contour(mask):
    m = mask.astype(np.uint8)
    if m.sum() < 6:
        return []
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)[:, 0, :].astype(float)
    step = max(1, len(c) // 120)
    return [[round(x, 1), round(y, 1)] for x, y in c[::step]]


def colour_mask(labels):
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[labels == 1] = (60, 170, 92, 228)     # metal, green
    rgba[labels == 2] = (226, 72, 58, 214)     # oxide, red
    rgba[labels == 3] = (44, 197, 204, 236)    # void, turquoise
    return rgba


def times():
    """Evenly spaced, like a real video: 0 to 59.5 s, one frame every 0.5 s."""
    return [round(0.5 * i, 2) for i in range(120)]


def main(out):
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(11)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    bg = 152 + 30 * (fbm(H, W, 110, 4, rng) - 0.5) + 16 * (fbm(H, W, 7, 2, rng) - 0.5)
    edge = np.hypot((xx - 40) / 300, (yy - 560) / 230) + 0.12 * (fbm(H, W, 40, 3, rng) - 0.5)
    bg -= 62 * np.clip((1.0 - edge) * 9, 0, 1)                 # thick support film, lower left
    grain = cv2.GaussianBlur(rng.normal(0, 17, (H, W)).astype(np.float32), (0, 0), 0.6)
    seeds = np.ones((H, W), np.uint8)
    for _ in range(900):
        seeds[rng.integers(0, H), rng.integers(0, W)] = 0
    _, grains_id = cv2.distanceTransformWithLabels(seeds, cv2.DIST_L2, 3, labelType=cv2.DIST_LABEL_PIXEL)
    grain_gain = rng.uniform(0.6, 1.45, grains_id.max() + 1).astype(np.float32)
    index = []
    for i, t in enumerate(times()):
        img, labels, outlines = render(t, bg, grain, grains_id, grain_gain, yy, xx)
        cv2.imwrite(os.path.join(out, f"tem_{i:03d}.png"), img)
        cv2.imwrite(os.path.join(out, f"mask_{i:03d}.png"), cv2.cvtColor(colour_mask(labels), cv2.COLOR_RGBA2BGRA))
        frac = {k: int((labels == v).sum()) for k, v in [("metal", 1), ("oxide", 2), ("void", 3)]}
        # Normalized NiO volume fraction, as in the paper's Fig. 6c: the share of the nickel turned to NiO.
        alpha = {p["name"]: round(1 - (state(p, t)[2] / p["r0"]) ** 3, 4) for p in PARTICLES}
        index.append(dict(i=i, t=t, outlines=outlines, area=frac, alpha=alpha))
    with open(os.path.join(out, "index.json"), "w") as f:
        json.dump(dict(W=W, H=H, px_per_nm=PX, key_times=KEY_TIMES, frames=index), f)
    print(len(index), "frames")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "etem_frames")
