"""Six animated project cards (each its own SVG so each can link somewhere)."""
import math, random
from lib import *

CW, CH = 490, 280

PROJECTS = [
    dict(file="proj-hrms.svg", tag="PRODUCTION · ALPHABETUM", title="Multi-Agent HRMS Platform", acc=P["purple"],
         desc="Multi-agent platform automating recruitment, compensation analytics, an employee co-pilot and workforce simulation.",
         metric="4 HR workflows → LangGraph DAGs", chips=["LangGraph", "FastAPI", "PostgreSQL", "RBAC"], art="agents"),
    dict(file="proj-friday.svg", tag="PRODUCTION · RENAN", title="Project Friday · Analytics AI", acc=P["cyan"],
         desc="Conversational analytics: clarification agent, schema-aware NL → SQL with 4-stage validation, document Q&A agent.",
         metric="column recall 0.48 → 0.81", chips=["LangChain", "Azure OpenAI", "SQLGlot", "RAG"], art="sql"),
    dict(file="proj-image-search.svg", tag="LIVE DEMO", title="Semantic Image Search", acc=P["sky"],
         desc="CLIP embeddings + FAISS similarity search across 1000+ images, hybrid text-image scoring and K-means clustering.",
         metric="sub-second queries · Flask API", chips=["CLIP", "FAISS", "Flask", "React"], art="embed"),
    dict(file="proj-knowledge.svg", tag="OPEN SOURCE · LIVE", title="Personal Knowledge Assistant", acc=P["mint"],
         desc="RAG chatbot over your own documents: BGE embeddings, Pinecone retrieval, configurable chunking and prompts.",
         metric="Gemini + LangChain + Pinecone", chips=["Gemini", "LangChain", "Pinecone", "Streamlit"], art="chat"),
    dict(file="proj-talentscout.svg", tag="OPEN SOURCE", title="TalentScout Hiring Assistant", acc=P["pink"],
         desc="AI screening assistant: collects candidate details, generates tech-stack-specific questions, anonymizes PII.",
         metric="Gemini 2.0 Flash · Streamlit", chips=["Python", "Gemini", "Streamlit", "SHA-256"], art="hire"),
    dict(file="proj-yolo.svg", tag="OPEN SOURCE · LIVE", title="YOLO Vision Pro", acc=P["amber"],
         desc="Real-time object detection in the browser: YOLOv8 on ONNX Runtime for uploads or live webcam, tunable confidence and IoU.",
         metric="Nano → Large model variants", chips=["YOLOv8", "ONNX", "OpenCV", "WebRTC"], art="yolo"),
]


def art_agents(acc, ox, oy):
    hub = (ox + 70, oy + 70)
    sats = [(ox + 70 + 58 * math.cos(a), oy + 70 + 58 * math.sin(a)) for a in [math.radians(d) for d in (-90, 0, 90, 180)]]
    labels = ["HIRE", "PAY", "COPILOT", "SIM"]
    o = [f'<circle cx="{hub[0]}" cy="{hub[1]}" r="58" fill="none" stroke="{acc}" stroke-opacity=".2" stroke-dasharray="2 5">'
         f'<animateTransform attributeName="transform" type="rotate" from="0 {hub[0]} {hub[1]}" to="360 {hub[0]} {hub[1]}" dur="30s" repeatCount="indefinite"/></circle>']
    for i, (sx, sy) in enumerate(sats):
        pid = f"ag{i}"
        o.append(f'<path id="{pid}" d="M{hub[0]} {hub[1]} L{sx:.1f} {sy:.1f}" stroke="{acc}" stroke-opacity=".45" stroke-width="1.3"/>')
        o.append(f'<circle r="2.6" fill="{acc}"><animateMotion dur="1.8s" begin="{i*0.45:.2f}s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear"><mpath xlink:href="#{pid}"/></animateMotion></circle>')
    o.append(f'<circle cx="{hub[0]}" cy="{hub[1]}" r="20" fill="{P["bg1"]}" stroke="{acc}" stroke-width="1.6"/>'
             f'<circle cx="{hub[0]}" cy="{hub[1]}" r="20" fill="{acc}" opacity=".15"><animate attributeName="r" values="20;27;20" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".25;0;.25" dur="2.4s" repeatCount="indefinite"/></circle>')
    o.append(T(hub[0], hub[1] + 3.5, "LG", 10, "JB", 700, acc, "middle"))
    for i, ((sx, sy), lab) in enumerate(zip(sats, labels)):
        o.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="13" fill="{P["bg1"]}" stroke="{acc}" stroke-opacity=".8"/>')
        o.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4" fill="{acc}"><animate attributeName="opacity" values=".3;1;.3" dur="1.8s" begin="{i*0.45:.2f}s" repeatCount="indefinite"/></circle>')
        if i in (0, 2):
            o.append(T(sx, sy + (-19 if i == 0 else 27), lab, 8, "JB", 700, P["muted"], "middle"))
        else:
            o.append(T(sx + (17 if i == 1 else -17), sy + 3, lab, 8, "JB", 700, P["muted"], "start" if i == 1 else "end"))
    return "".join(o)


def art_sql(acc, ox, oy):
    stages = ["syntax", "semantic", "intent", "execute"]
    o = [f'<rect x="{ox}" y="{oy+4}" width="140" height="44" rx="8" fill="#070B18" stroke="{P["line2"]}"/>',
         T(ox + 10, oy + 22, "SELECT dept,", 9, "JB", 700, acc), T(ox + 10, oy + 37, "  AVG(ctc) ...", 9, "JB", 400, P["muted"])]
    for i, s in enumerate(stages):
        y = oy + 66 + i * 22
        b = 0.4 + i * 0.6
        o.append(f'<rect x="{ox}" y="{y}" width="140" height="17" rx="8.5" fill="{P["line"]}"/>')
        o.append(f'<rect x="{ox}" y="{y}" width="0" height="17" rx="8.5" fill="{acc}" fill-opacity=".25"><animate attributeName="width" values="0;140;140" keyTimes="0;.18;1" dur="4s" begin="{b:.1f}s" repeatCount="indefinite"/></rect>')
        o.append(T(ox + 10, y + 12, f"{i+1} {s}", 9, "JB", 400, P["text"]))
        o.append(f'<g opacity="0">' + T(ox + 128, y + 12.5, "✓", 10, "JB", 700, P["mint"], "middle") +
                 f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;.17;.2;1" dur="4s" begin="{b:.1f}s" repeatCount="indefinite"/></g>')
    return "".join(o)


def art_embed(acc, ox, oy):
    random.seed(3)
    centers = [(ox + 35, oy + 40, P["sky"]), (ox + 105, oy + 50, P["violet"]), (ox + 65, oy + 115, P["pink"])]
    o = [f'<rect x="{ox-6}" y="{oy}" width="152" height="150" rx="10" fill="#070B18" stroke="{P["line2"]}"/>']
    for k in range(30):
        cx, cy, col = centers[k % 3]
        tx, ty = cx + random.gauss(0, 9), cy + random.gauss(0, 9)
        sx, sy = ox + random.uniform(5, 135), oy + random.uniform(8, 142)
        o.append(f'<circle r="2.6" fill="{col}" cx="{sx:.1f}" cy="{sy:.1f}">'
                 f'<animate attributeName="cx" values="{sx:.1f};{tx:.1f};{tx:.1f};{sx:.1f}" keyTimes="0;.35;.85;1" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;0 0 1 1;.4 0 .2 1"/>'
                 f'<animate attributeName="cy" values="{sy:.1f};{ty:.1f};{ty:.1f};{sy:.1f}" keyTimes="0;.35;.85;1" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;0 0 1 1;.4 0 .2 1"/></circle>')
    qx, qy = ox + 98, oy + 92
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.38;.45;.85;.9" dur="6s" repeatCount="indefinite"/>'
             f'<circle cx="{qx}" cy="{qy}" r="22" fill="none" stroke="{acc}" stroke-dasharray="3 3"/>'
             f'<line x1="{qx}" y1="{qy}" x2="{centers[1][0]}" y2="{centers[1][1]}" stroke="{acc}" stroke-opacity=".7"/>'
             f'<circle cx="{qx}" cy="{qy}" r="5" fill="#fff"/>' + T(qx + 8, qy + 30, "query", 8.5, "JB", 700, acc) + "</g>")
    return "".join(o)


def art_chat(acc, ox, oy):
    msgs = [(0, 18, 96, "user", P["line2"]), (34, 52, 106, "ai", acc), (10, 92, 80, "user", P["line2"]), (28, 124, 112, "ai", acc)]
    o = []
    for i, (dx, y, w, who, col) in enumerate(msgs):
        x = ox + (140 - w if who == "user" else 0)
        b = i * 0.9
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.06;.9;1" dur="6s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                 f'<rect x="{x}" y="{oy+y}" width="{w}" height="24" rx="10" fill="{col}" fill-opacity="{0.22 if who=="ai" else 1}" stroke="{col}" stroke-opacity=".6"/>'
                 f'<rect x="{x+10}" y="{oy+y+8}" width="{w*0.62:.0f}" height="3" rx="1.5" fill="{P["text"]}" opacity=".7"/>'
                 f'<rect x="{x+10}" y="{oy+y+14}" width="{w*0.4:.0f}" height="3" rx="1.5" fill="{P["text"]}" opacity=".4"/>'
                 + (T(x + w - 8, oy + y - 4, "src: notes.pdf p.3", 7.5, "JB", 400, acc, "end") if i == 3 else "") + "</g>")
    return "".join(o)


def art_hire(acc, ox, oy):
    o = [f'<rect x="{ox}" y="{oy+6}" width="140" height="140" rx="12" fill="#070B18" stroke="{P["line2"]}"/>',
         f'<circle cx="{ox+30}" cy="{oy+36}" r="14" fill="{acc}" fill-opacity=".2" stroke="{acc}"/>',
         f'<circle cx="{ox+30}" cy="{oy+32}" r="5" fill="{acc}"/><path d="M{ox+21} {oy+45} q9 -9 18 0" stroke="{acc}" fill="none" stroke-width="2"/>',
         T(ox + 52, oy + 33, "candidate", 9, "JB", 700, P["text"]), T(ox + 52, oy + 46, "#a3f9…e1", 8.5, "JB", 400, P["muted"])]
    rows = ["Python", "FastAPI", "SQL", "LLMs"]
    for i, r in enumerate(rows):
        y = oy + 68 + i * 19
        o.append(T(ox + 12, y + 8, r, 8.5, "JB", 400, P["muted"]))
        o.append(f'<rect x="{ox+62}" y="{y+1}" width="66" height="8" rx="4" fill="{P["line"]}"/>')
        w = [58, 46, 52, 62][i]
        o.append(f'<rect x="{ox+62}" y="{y+1}" width="0" height="8" rx="4" fill="{acc}"><animate attributeName="width" values="0;{w};{w};0" keyTimes="0;.25;.9;1" dur="5s" begin="{i*0.25:.2f}s" repeatCount="indefinite"/></rect>')
    return "".join(o)


def art_yolo(acc, ox, oy):
    o = [f'<rect x="{ox}" y="{oy}" width="140" height="150" rx="10" fill="#070B18" stroke="{P["line2"]}"/>',
         f'<path d="M{ox+18} {oy+120} q22 -60 44 -20 q16 -36 40 -4 q12 -20 22 10 v24 h-106z" fill="{P["line"]}"/>',
         f'<circle cx="{ox+104}" cy="{oy+38}" r="12" fill="{P["line2"]}"/>']
    boxes = [(ox + 14, oy + 58, 54, 68, "person 0.94"), (ox + 72, oy + 22, 54, 42, "sun 0.71"), (ox + 66, oy + 80, 62, 50, "dog 0.88")]
    for i, (x, y, w, h, lab) in enumerate(boxes):
        b = i * 0.7
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.85;1" dur="4.2s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{acc}" fill-opacity=".08" stroke="{acc}" stroke-width="1.6"/>'
                 f'<rect x="{x}" y="{y-12}" width="{text_width(lab,"JB",700,7.5)+8:.1f}" height="12" fill="{acc}"/>'
                 + T(x + 4, y - 3, lab, 7.5, "JB", 700, "#0B1124") + "</g>")
    o.append(f'<rect x="{ox}" y="{oy}" width="140" height="2" fill="{acc}" opacity=".8"><animate attributeName="y" values="{oy};{oy+148};{oy}" dur="3s" repeatCount="indefinite"/></rect>')
    return "".join(o)


ARTS = dict(agents=art_agents, sql=art_sql, embed=art_embed, chat=art_chat, hire=art_hire, yolo=art_yolo)


def card(p):
    acc = p["acc"]
    defs = [frame_grad("fg", 9, acc, P["line"], acc, 1),
            f'<radialGradient id="rg" cx=".9" cy=".1" r=".9"><stop offset="0" stop-color="{acc}" stop-opacity=".2"/><stop offset=".7" stop-color="{acc}" stop-opacity="0"/></radialGradient>',
            grid_pattern("dots", 18, P["line2"], 0.4)]
    pad = 24
    b = [f'<rect x=".7" y=".7" width="{CW-1.4}" height="{CH-1.4}" rx="18" fill="{P["card"]}"/>',
         f'<rect x=".7" y=".7" width="{CW-1.4}" height="{CH-1.4}" rx="18" fill="url(#dots)" opacity=".6"/>',
         f'<rect x=".7" y=".7" width="{CW-1.4}" height="{CH-1.4}" rx="18" fill="url(#rg)"/>',
         f'<rect x=".7" y=".7" width="{CW-1.4}" height="{CH-1.4}" rx="18" fill="none" stroke="url(#fg)" stroke-width="1.4"/>']
    s, _ = pill(pad, 22, p["tag"], "JB", 10, 700, acc, "rgba(255,255,255,.03)", acc, 10, 22, 1.2)
    b.append(s)
    b.append(f'<circle cx="{CW-34}" cy="33" r="14" fill="none" stroke="{acc}" stroke-opacity=".6"/>' + T(CW - 34, 38, "↗", 13, "JB", 700, acc, "middle"))
    b.append(T(pad, 84, p["title"], 23, "SG", 700, P["text"], ls=-0.3))
    y, fs = 114, 14
    lines = wrap(p["desc"], 300, "SG", 400, fs)
    if len(lines) > 4:
        fs = 13; lines = wrap(p["desc"], 300, "SG", 400, fs)
    assert len(lines) <= 4, p["title"]
    for ln in lines:
        b.append(T(pad, y, ln, fs, "SG", 400, "#C3CEE3")); y += 19.5
    b.append(T(pad, CH - 66, "▸ " + p["metric"], 12, "JB", 700, acc))
    x = pad
    for c in p["chips"]:
        s, w = pill(x, CH - 46, c, "JB", 10.5, 700, P["text"], "rgba(255,255,255,.04)", P["line2"], 9, 22, 0.2, 6)
        b.append(s); x += w + 6
    b.append(f'<g transform="translate({CW-24-118} 92) scale(.82)">' + ARTS[p["art"]](acc, 0, 0) + "</g>")
    write(p["file"], svg_doc(CW, CH, "".join(b), "", p["title"], f'{p["title"]}: {p["desc"]} ({p["metric"]})', "".join(defs)))


if __name__ == "__main__":
    for p in PROJECTS:
        card(p)
