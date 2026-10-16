"""Tech-stack panel with a rotating 3D geodesic 'agentic core' (pure SVG/SMIL, precomputed projection)."""
import math
from lib import *


def icosphere(freq=2):
    t = (1 + 5 ** 0.5) / 2
    v = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
         (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    v = [tuple(c / math.sqrt(sum(x * x for x in p)) for c in p) for p in v]
    f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
         (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    for _ in range(freq - 1):
        cache, nf = {}, []

        def mid(a, b):
            key = tuple(sorted((a, b)))
            if key not in cache:
                p = [(v[a][i] + v[b][i]) / 2 for i in range(3)]
                n = math.sqrt(sum(x * x for x in p))
                v.append(tuple(x / n for x in p)); cache[key] = len(v) - 1
            return cache[key]
        for a, b, c in f:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            nf += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        f = nf
    edges = set()
    for a, b, c in f:
        for e in ((a, b), (b, c), (c, a)):
            edges.add(tuple(sorted(e)))
    return v, sorted(edges)


def core(cx, cy, R, frames=24, dur=26):
    verts, edges = icosphere(2)
    tilt = math.radians(-22)
    proj = []
    for k in range(frames + 1):
        a = 2 * math.pi * k / frames
        fr = []
        for x, y, z in verts:
            x1 = x * math.cos(a) + z * math.sin(a); z1 = -x * math.sin(a) + z * math.cos(a)
            y2 = y * math.cos(tilt) - z1 * math.sin(tilt); z2 = y * math.sin(tilt) + z1 * math.cos(tilt)
            s = 1 / (1 - z2 * 0.18)  # mild perspective
            fr.append((cx + x1 * R * s, cy + y2 * R * s, z2))
        proj.append(fr)
    o = []
    A = f'dur="{dur}s" repeatCount="indefinite"'
    for (i, j) in edges:
        xs1 = ";".join(f"{proj[k][i][0]:.0f}" for k in range(frames + 1))
        ys1 = ";".join(f"{proj[k][i][1]:.0f}" for k in range(frames + 1))
        xs2 = ";".join(f"{proj[k][j][0]:.0f}" for k in range(frames + 1))
        ys2 = ";".join(f"{proj[k][j][1]:.0f}" for k in range(frames + 1))
        op = ";".join(f"{0.12 + 0.75 * ((proj[k][i][2] + proj[k][j][2]) / 2 + 1) / 2:.2f}" for k in range(frames + 1))
        o.append(f'<line stroke="url(#coreG)" stroke-width="1.1"><animate attributeName="x1" values="{xs1}" {A}/><animate attributeName="y1" values="{ys1}" {A}/>'
                 f'<animate attributeName="x2" values="{xs2}" {A}/><animate attributeName="y2" values="{ys2}" {A}/><animate attributeName="stroke-opacity" values="{op}" {A}/></line>')
    for i in range(len(verts)):
        xs = ";".join(f"{proj[k][i][0]:.0f}" for k in range(frames + 1))
        ys = ";".join(f"{proj[k][i][1]:.0f}" for k in range(frames + 1))
        rs = ";".join(f"{1.4 + 1.9 * (proj[k][i][2] + 1) / 2:.1f}" for k in range(frames + 1))
        op = ";".join(f"{0.25 + 0.75 * (proj[k][i][2] + 1) / 2:.2f}" for k in range(frames + 1))
        col = [P["cyan"], P["purple"], P["pink"]][i % 3]
        o.append(f'<circle fill="{col}"><animate attributeName="cx" values="{xs}" {A}/><animate attributeName="cy" values="{ys}" {A}/>'
                 f'<animate attributeName="r" values="{rs}" {A}/><animate attributeName="opacity" values="{op}" {A}/></circle>')
    return "".join(o), len(verts), len(edges)


STACK = [
    ("LLM & AGENTS", P["cyan"], [("langchain", "LangChain"), ("langgraph", "LangGraph"), (None, "OpenAI API"), (None, "Azure OpenAI"),
                                 ("googlegemini", "Gemini"), ("huggingface", "Hugging Face"), (None, "MCP"), (None, "Semantic routing"), (None, "Fine-tuning")]),
    ("RETRIEVAL & EVALS", P["purple"], [(None, "Pinecone"), (None, "FAISS"), (None, "ChromaDB"), (None, "LlamaIndex"), (None, "Sentence Transformers"),
                                        (None, "Hybrid search"), (None, "Evals · recall · groundedness · hallucination rate")]),
    ("BACKEND & APIs", P["mint"], [("python", "Python"), ("fastapi", "FastAPI"), ("django", "Django"), ("nodedotjs", "Node.js"), ("typescript", "TypeScript"),
                                   ("redis", "Redis"), ("celery", "Celery"), ("sqlalchemy", "SQLAlchemy"), ("prisma", "Prisma"), (None, "WebSockets"), ("jsonwebtokens", "JWT / OAuth2")]),
    ("ML & DATA", P["pink"], [("pytorch", "PyTorch"), ("tensorflow", "TensorFlow"), ("scikitlearn", "scikit-learn"), ("opencv", "OpenCV"), ("yolo", "YOLO"),
                              ("mlflow", "MLflow"), ("weightsandbiases", "W&B"), ("dvc", "DVC"), ("pandas", "Pandas"), ("numpy", "NumPy"), (None, "SQLGlot")]),
    ("CLOUD & DATA STORES", P["amber"], [(None, "AWS · S3 · EC2 · Lambda"), (None, "Azure DevOps"), ("docker", "Docker"), ("githubactions", "GitHub Actions"),
                                          ("postgresql", "PostgreSQL"), ("mongodb", "MongoDB"), ("mysql", "MySQL")]),
]


def hexagon(x, y, r, col):
    pts = " ".join(f"{x + r * math.cos(math.radians(60 * k + 30)):.1f},{y + r * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
    return f'<polygon points="{pts}" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="1.3"/>'


def build():
    W = 1000
    x0, xr, ph, fs = 330, 974, 28, 12.5
    # layout pills
    rows, y = [], 34
    for title, col, items in STACK:
        rows.append(("title", y, title, col)); y += 16
        x = x0
        line = []
        for key, lab in items:
            w = 10 + 16 + 7 + text_width(lab, "SG", 500, fs) + 12
            if x + w > xr:
                y += ph + 8; x = x0
            line.append((x, y, w, key, lab, col)); x += w + 8
        rows.append(("pills", line)); y += ph + 22
    H = int(y + 6)
    defs = [frame_grad("sf", 14), grid_pattern("dots", 22, P["line2"], 0.5),
            f'<linearGradient id="coreG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{P["cyan"]}"/><stop offset=".5" stop-color="{P["violet"]}"/><stop offset="1" stop-color="{P["pink"]}"/></linearGradient>',
            f'<radialGradient id="coreGlow"><stop offset="0" stop-color="{P["violet"]}" stop-opacity=".6"/><stop offset=".45" stop-color="{P["cyan"]}" stop-opacity=".15"/><stop offset="1" stop-color="{P["cyan"]}" stop-opacity="0"/></radialGradient>',
            '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>']
    css = (".pin{animation:pin .7s cubic-bezier(.2,.8,.2,1) both}@keyframes pin{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}"
           ".beat{animation:beat 3s ease-in-out infinite;transform-box:fill-box;transform-origin:center}@keyframes beat{0%,100%{transform:scale(1);opacity:.85}50%{transform:scale(1.18);opacity:1}}")
    b = [f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="18" fill="#080C1A"/>',
         f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="18" fill="url(#dots)"/>',
         f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="18" fill="none" stroke="url(#sf)" stroke-width="1.3"/>',
         f'<line x1="306" y1="24" x2="306" y2="{H-24}" stroke="{P["line"]}"/>']
    cx, cy, R = 156, H / 2 - 6, 104
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R*1.5:.0f}" fill="url(#coreGlow)"/>')
    b.append(f'<g transform="translate({cx} {cy})"><circle r="{R+22}" fill="none" stroke="{P["line2"]}" stroke-dasharray="1 6" stroke-linecap="round">'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="50s" repeatCount="indefinite"/></circle>'
             f'<ellipse rx="{R+30}" ry="{(R+30)*0.26:.0f}" fill="none" stroke="{P["cyan"]}" stroke-opacity=".35" transform="rotate(-14)"/>'
             f'<circle r="5" fill="{P["cyan"]}"><animateMotion dur="7s" repeatCount="indefinite" path="M{-(R+30)*math.cos(math.radians(14)):.1f} {(R+30)*math.sin(math.radians(14)):.1f} A{R+30} {(R+30)*0.26:.0f} -14 1 1 {(R+30)*math.cos(math.radians(14)):.1f} {-(R+30)*math.sin(math.radians(14)):.1f} A{R+30} {(R+30)*0.26:.0f} -14 1 1 {-(R+30)*math.cos(math.radians(14)):.1f} {(R+30)*math.sin(math.radians(14)):.1f}"/></circle></g>')
    b.append(f'<circle class="beat" cx="{cx}" cy="{cy}" r="16" fill="{P["violet"]}" filter="url(#soft)"/>'
             f'<circle cx="{cx}" cy="{cy}" r="7" fill="#fff" opacity=".85"/>')
    sph, nv, ne = core(cx, cy, R)
    b.append(sph)
    b.append(T(cx, H - 58, "AGENTIC CORE", 12, "JB", 700, P["text"], "middle", ls=3))
    b.append(T(cx, H - 38, f"{nv} nodes · {ne} edges · pure SVG, no JS", 10, "JB", 400, P["muted"], "middle"))
    b.append(T(cx, 40, "STACK", 11, "JB", 700, P["cyan"], "middle", ls=3))
    k = 0
    for r in rows:
        if r[0] == "title":
            _, yy, title, col = r
            b.append(f'<rect x="{x0}" y="{yy-9}" width="3" height="11" rx="1.5" fill="{col}"/>' + T(x0 + 10, yy, title, 10.5, "JB", 700, col, ls=1.8))
        else:
            for (x, yy, w, key, lab, col) in r[1]:
                g = [f'<g class="pin" style="animation-delay:{0.15+k*0.035:.2f}s">',
                     f'<rect x="{x:.1f}" y="{yy}" width="{w:.1f}" height="{ph}" rx="8" fill="#0E152B" stroke="{col}" stroke-opacity=".28"/>']
                if key and key in ICONS:
                    g.append(icon(key, x + 10, yy + 6, 16, lift("#" + ICONS[key]["hex"])))
                else:
                    g.append(hexagon(x + 18, yy + ph / 2, 6.5, col))
                g.append(T(x + 33, yy + 18.5, lab, fs, "SG", 500, P["text"]))
                g.append("</g>")
                b += g; k += 1
    write("stack.svg", svg_doc(W, H, "".join(b), css, "Tech stack",
                               "Tech stack: " + "; ".join(t + ": " + ", ".join(l for _, l in it) for t, _, it in STACK),
                               "".join(defs)))


if __name__ == "__main__":
    build()
