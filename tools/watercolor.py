"""Turn any image into a watercolor painting with OpenCV.

    python tools/watercolor.py in.jpg out.jpg [--seed 3] [--colors 14] [--no-border]

The filter imitates what pigment does on wet paper:

1. Simplify      edge-preserving smoothing and colour quantization give flat washes.
2. Wobble        a smooth noise field displaces shapes, so edges are hand-drawn.
3. Wet edges     pigment pools at the rim of each wash, so edges darken.
4. Density       low-frequency noise makes washes uneven; high-frequency noise
                 adds granulation, mostly in dark passages.
5. Glaze         colour is applied subtractively (Beer-Lambert) on warm paper,
                 so overlapping washes darken the way real glazes do.
6. Pencil        faint graphite under-drawing from the source edges.
7. Paper         fibre grain and a deckled, unpainted border.
"""
import argparse

import cv2
import numpy as np

PAPER = np.array([0.965, 0.948, 0.915], np.float32)  # warm cold-press paper, RGB


def fbm(h, w, scale, octaves, rng):
    """Fractal value noise in [0, 1]."""
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        s = max(2, int(scale / 2 ** o))
        gh, gw = h // s + 2, w // s + 2
        grid = rng.random((gh, gw)).astype(np.float32)
        up = cv2.resize(grid, (gw * s, gh * s), interpolation=cv2.INTER_CUBIC)[:h, :w]
        out += amp * up
        total += amp
        amp *= 0.5
    out /= total
    return (out - out.min()) / (np.ptp(out) + 1e-6)


def quantize(img, k, rng):
    """k-means in Lab; returns the label map and the quantized RGB image."""
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5)
    cv2.setRNGSeed(int(rng.integers(1 << 30)))
    _, labels, centers = cv2.kmeans(lab, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    q = centers[labels.ravel()].reshape(img.shape).astype(np.uint8)
    return labels.reshape(img.shape[:2]).astype(np.int32), cv2.cvtColor(q, cv2.COLOR_LAB2RGB)


def deckle_mask(h, w, rng, margin):
    """1 inside the painted area, 0 on the bare border, with a ragged edge."""
    m = np.zeros((h, w), np.float32)
    cv2.rectangle(m, (margin, margin), (w - margin, h - margin), 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), margin * 0.45)
    n = fbm(h, w, margin * 1.6, 4, rng)
    m = np.clip((m + (n - 0.5) * 0.55 - 0.5) * 9 + 0.5, 0, 1)
    return cv2.GaussianBlur(m, (0, 0), 1.2)


def watercolor(bgr, seed=0, colors=14, border=True, pencil=0.22, wobble=7.0):
    rng = np.random.default_rng(seed)
    h, w = bgr.shape[:2]
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # 1. Simplify into washes.
    smooth = rgb
    for _ in range(3):
        smooth = cv2.bilateralFilter(smooth, 9, 40, 7)
    smooth = cv2.pyrMeanShiftFiltering(smooth, 9, 22)
    labels, q = quantize(smooth, colors, rng)
    # Keep some of the smooth gradients so skies don't band too hard.
    base = cv2.addWeighted(q, 0.5, cv2.GaussianBlur(smooth, (0, 0), 3), 0.5, 0)

    # 2. Wobble: displace everything by a smooth noise field.
    sc = max(h, w) / 14
    dx = (fbm(h, w, sc, 3, rng) - 0.5) * 2 * wobble
    dy = (fbm(h, w, sc, 3, rng) - 0.5) * 2 * wobble
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    mx, my = gx + dx, gy + dy
    base = cv2.remap(base, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    labels = cv2.remap(labels.astype(np.float32), mx, my, cv2.INTER_NEAREST,
                       borderMode=cv2.BORDER_REFLECT).astype(np.int32)

    # 3. Wet edges: distance to the nearest wash boundary.
    edge = np.zeros((h, w), np.uint8)
    edge[:, 1:] |= (labels[:, 1:] != labels[:, :-1]).astype(np.uint8)
    edge[1:, :] |= (labels[1:, :] != labels[:-1, :]).astype(np.uint8)
    dist = cv2.distanceTransform(1 - edge, cv2.DIST_L2, 3)
    rim = np.exp(-dist / 2.2)

    # 4. Uneven density, colour drift, granulation and blooms.
    big = max(h, w)
    blotch = fbm(h, w, big / 5, 4, rng)
    flow = fbm(h, w, big / 18, 3, rng)
    grain = fbm(h, w, 2.5, 2, rng) * 0.6 + fbm(h, w, 7, 2, rng) * 0.4
    c = base.astype(np.float32) / 255.0
    lum = c.mean(axis=2)
    density = (0.62 + 0.55 * blotch * 0.6 + 0.4 * flow * 0.4) * (1 + 0.55 * rim)
    density *= 1 + (grain - 0.5) * (0.25 + 0.6 * (1 - lum))
    for _ in range(int(rng.integers(3, 7))):  # blooms: pale patches with a dark tide line
        bx, by = rng.uniform(0, w), rng.uniform(0, h)
        br = rng.uniform(0.04, 0.10) * big
        r = np.hypot(gx - bx, gy - by) / br + (fbm(h, w, big / 30, 2, rng) - 0.5) * 0.6
        inside = np.clip(1 - r, 0, 1) ** 0.5
        tide = np.exp(-((r - 1) / 0.06) ** 2)
        density *= 1 - 0.35 * inside + 0.35 * tide
    drift = np.stack([fbm(h, w, big / 7, 2, rng) for _ in range(3)], axis=2) - 0.5
    c = np.clip(c * (1 + 0.11 * drift), 0, 1)

    # 5. Glaze subtractively onto paper; leave hairlines of bare paper between some washes.
    absorb = -np.log(np.clip(c, 0.02, 1.0)) * density[..., None] * 0.95
    contrast = cv2.morphologyEx(cv2.cvtColor(base, cv2.COLOR_RGB2GRAY), cv2.MORPH_GRADIENT,
                                np.ones((3, 3), np.uint8)).astype(np.float32) / 255
    gap = ((dist < 1.0) & (contrast > 0.18) & (fbm(h, w, 90, 2, rng) > 0.68)).astype(np.float32)
    gap = cv2.GaussianBlur(gap, (0, 0), 0.9)
    absorb *= (1 - 0.6 * np.clip(gap * 1.5, 0, 1))[..., None]
    out = PAPER * np.exp(-absorb)

    # 6. Pencil under-drawing.
    if pencil > 0:
        g = cv2.GaussianBlur(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY), (0, 0), 1.4)
        lines = cv2.Canny(g, 40, 110)
        lines = cv2.remap(lines, mx + dx * 0.6, my + dy * 0.6, cv2.INTER_LINEAR)
        lines = cv2.GaussianBlur(lines.astype(np.float32) / 255, (0, 0), 0.7)
        broken = fbm(h, w, 18, 2, rng) > 0.35
        out *= 1 - (pencil * lines * broken)[..., None] * np.array([0.75, 0.78, 0.85], np.float32)

    # 7. Paper grain and deckled border.
    fibre = fbm(h, w, 2, 2, rng) * 0.6 + fbm(h, w, 24, 3, rng) * 0.4
    paper = PAPER * (0.975 + 0.05 * fibre[..., None])
    out *= 0.975 + 0.05 * fibre[..., None]
    if border:
        mask = deckle_mask(h, w, rng, int(min(h, w) * 0.045))
        # Pigment pools where the wash stops at the border.
        pool = np.exp(-np.abs(mask - 0.5) * 9) * 0.10
        out *= 1 - pool[..., None]
        out = out * mask[..., None] + paper * (1 - mask[..., None])

    out = np.clip(out * 255, 0, 255).astype(np.uint8)
    return cv2.cvtColor(out, cv2.COLOR_RGB2BGR)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--colors", type=int, default=14)
    ap.add_argument("--width", type=int, default=0, help="resize to this width first")
    ap.add_argument("--no-border", action="store_true")
    a = ap.parse_args()
    img = cv2.imread(a.src)
    if a.width:
        img = cv2.resize(img, (a.width, round(img.shape[0] * a.width / img.shape[1])),
                         interpolation=cv2.INTER_AREA)
    cv2.imwrite(a.dst, watercolor(img, a.seed, a.colors, not a.no_border),
                [cv2.IMWRITE_JPEG_QUALITY, 86])


if __name__ == "__main__":
    main()
