"""CTA footer, pre-run placeholders and the interactive 3D STL monogram."""
import math, os, random
from lib import *


def cta():
    W, H = 1000, 230
    defs = [frame_grad("cf", 10), '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>',
            f'<clipPath id="cl"><rect width="{W}" height="{H}" rx="20"/></clipPath>',
            f'<linearGradient id="hg" gradientUnits="userSpaceOnUse" x1="0" x2="640" spreadMethod="repeat"><stop offset="0" stop-color="{P["cyan"]}"/><stop offset=".5" stop-color="{P["pink"]}"/><stop offset="1" stop-color="{P["cyan"]}"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="640 0" dur="8s" repeatCount="indefinite"/></linearGradient>']
    b = [f'<g clip-path="url(#cl)"><rect width="{W}" height="{H}" fill="#070A18"/>',
         f'<g filter="url(#blur)" opacity=".5"><circle cx="160" cy="200" r="130" fill="{P["violet"]}"/><circle cx="860" cy="40" r="130" fill="{P["cyan"]}" opacity=".6"/></g>']
    for k, (amp, wl, y, col, dur, op) in enumerate([(9, 250, 200, P["cyan"], 9, .5), (12, 330, 207, P["violet"], 13, .45), (7, 200, 213, P["pink"], 7, .4)]):
        pts = []
        for x in range(-wl, W + wl * 2, 6):
            pts.append(f"{x} {y + amp * math.sin(2 * math.pi * x / wl):.1f}")
        d = "M" + " L".join(pts)
        b.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.5" stroke-opacity="{op}">'
                 f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-wl} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    b.append(T(W / 2, 52, "// NEXT STEP", 12, "JB", 700, P["cyan"], "middle", ls=2.5))
    b.append(T(W / 2, 100, "Let's build AI that people can trust.", 40, "SG", 700, "url(#hg)", "middle", ls=-0.8))
    b.append(T(W / 2, 134, "Open to AI / LLM Engineer roles  ·  based in Bengaluru, India", 15, "SG", 500, P["text"], "middle"))
    b.append(T(W / 2, 162, "koshalkumar0304@gmail.com", 13, "JB", 400, P["muted"], "middle"))
    b.append("</g>")
    b.append(f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="20" fill="none" stroke="url(#cf)" stroke-width="1.3"/>')
    write("cta.svg", svg_doc(W, H, "".join(b), "", "Let's build AI that people can trust",
                             "Open to AI / LLM Engineer roles, based in Bengaluru, India. Email koshalkumar0304@gmail.com", "".join(defs)))


def placeholder(path, W, H, title, sub):
    random.seed(11)
    defs = [frame_grad("pf", 10)]
    b = [f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="18" fill="#080C1A"/>',
         f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="18" fill="none" stroke="url(#pf)" stroke-width="1.3"/>']
    if H > 200:  # little isometric skyline motif
        ox, oy, s = W / 2 - 150, H - 70, 14
        for i in range(12):
            for j in range(4):
                h = random.choice([4, 8, 14, 22, 30, 40])
                x = ox + (i - j) * s; y = oy + (i + j) * s * 0.5 - 40
                top = f"M{x} {y-h} l{s} {-s*0.5} l{s} {s*0.5} l{-s} {s*0.5}z"
                left = f"M{x} {y-h} l{s} {s*0.5} v{h} l{-s} {-s*0.5}z"
                right = f"M{x+s} {y-h+s*0.5} l{s} {-s*0.5} v{h} l{-s} {s*0.5}z"
                d = 0.2 + (i + j) * 0.05
                b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{d:.2f}s" dur=".4s" fill="freeze"/>'
                         f'<path d="{left}" fill="#3B2C7A"/><path d="{right}" fill="#1E3A6A"/><path d="{top}" fill="{random.choice([P["cyan"], P["purple"], P["pink"], P["violet"]])}"/></g>')
    ty = 70 if H > 200 else H / 2 - 4
    b.append(T(W / 2, ty, title, 22, "SG", 700, P["text"], "middle"))
    b.append(T(W / 2, ty + 28, sub, 12.5, "JB", 400, P["muted"], "middle"))
    svg = svg_doc(W, H, "".join(b), "", title, sub, "".join(defs))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(svg)
    print(os.path.basename(path), f"{len(svg)/1024:.1f} KB")


# ------------------------------------------------------------------ STL monogram
def earclip(poly):
    pts = list(range(len(poly)))
    tris = []

    def area2(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

    def inside(p, a, b, c):
        return area2(a, b, p) >= 0 and area2(b, c, p) >= 0 and area2(c, a, p) >= 0
    guard = 0
    while len(pts) > 3 and guard < 1000:
        guard += 1
        n = len(pts)
        for k in range(n):
            i0, i1, i2 = pts[k - 1], pts[k], pts[(k + 1) % n]
            a, b, c = poly[i0], poly[i1], poly[i2]
            if area2(a, b, c) <= 0:
                continue
            if any(inside(poly[q], a, b, c) for q in pts if q not in (i0, i1, i2)):
                continue
            tris.append((i0, i1, i2)); pts.pop(k); break
    tris.append(tuple(pts))
    return tris


def prism(poly, z0, z1):
    """Closed extrusion of a CCW polygon -> list of triangles (3 xyz tuples)."""
    out = []
    for a, b, c in earclip(poly):
        out.append(((*poly[a], z1), (*poly[b], z1), (*poly[c], z1)))   # top (CCW from +z)
        out.append(((*poly[a], z0), (*poly[c], z0), (*poly[b], z0)))   # bottom
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        out.append(((*p, z0), (*q, z0), (*q, z1)))
        out.append(((*p, z0), (*q, z1), (*p, z1)))
    return out


def normal(t):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = t
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
    return nx / l, ny / l, nz / l


def stl():
    K = [(0, 0), (2, 0), (2, 3.5), (3.2, 4.8), (5.8, 0), (8.2, 0), (4.7, 6.4), (8, 10), (5.4, 10), (2, 6.3), (2, 10), (0, 10)]
    K = [(x - 4.1, y - 5) for x, y in K]  # centre it
    hexa = [(9 * math.cos(math.radians(60 * k + 30)), 9 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    tris = prism(hexa, 0, 1.6) + prism(K, 1.6, 5.2)
    lines = ["solid koshal_monogram"]
    for t in tris:
        n = normal(t)
        lines.append(f"  facet normal {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}")
        lines.append("    outer loop")
        for v in t:
            lines.append(f"      vertex {v[0]:.3f} {v[1]:.3f} {v[2]:.3f}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append("endsolid koshal_monogram")
    txt = "\n".join(lines) + "\n"
    open(os.path.join(ASSETS, "model", "koshal-monogram.stl"), "w").write(txt)
    print("koshal-monogram.stl", len(tris), "facets", len(lines), "lines")
    return txt


if __name__ == "__main__":
    cta()
    placeholder(os.path.join(OUT, "profile-3d-contrib", "profile-night-rainbow.svg"), 1000, 300,
                "3D contribution skyline loading…", "renders after the first run of Actions → Profile visuals")
    placeholder(os.path.join(ASSETS, "generated", "snake-dark.svg"), 1000, 90, "contribution snake arrives after the first workflow run", "")
    placeholder(os.path.join(ASSETS, "generated", "snake-light.svg"), 1000, 90, "contribution snake arrives after the first workflow run", "")
    stl()
