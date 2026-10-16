"""Experience timeline + LLM system blueprint SVGs."""
from lib import *

ROLES = [
    dict(co="Ripik.ai", role="Engineering Intern", sub="ML / Backend · Production Systems", when="JAN – APR 2025", where="NOIDA",
         acc=P["pink"], head="3 months, 3 production systems shipped",
         bullets=["Parallel Boto3 + PIL compression pipeline (150 workers) over 10K+ files: S3 cost −60%, full audit logging",
                  "Fine-tuned ResNet18 on a custom 3-class kiln dataset: 98% val accuracy + confusion-matrix tooling",
                  "Gemini image-analysis pipeline (150 threads): 100+ images/day to JSON reports, manual review −80%"],
         chips=["PyTorch", "AWS S3", "Boto3", "Gemini API"]),
    dict(co="Renan", role="AI Engineer", sub="AI Product Engineer · Analytics Platform", when="MAY 2025 – MAR 2026", where="PROJECT FRIDAY",
         acc=P["cyan"], head="Owned the AI roadmap solo, architecture to production",
         bullets=["LLM auto-labeling for RAG metadata lifted column recall 0.48 → 0.81 (+69%) with zero manual annotation",
                  "4-stage SQL validation (syntax → semantic → intent → execution) with SQLGlot, auto-fix and destructive-op guardrails",
                  "Clarification agent + Document Q&A agent with metadata-filtered grounding to cut hallucinations and tokens"],
         chips=["LangChain", "LangGraph", "Azure OpenAI", "SQLGlot"]),
    dict(co="Alphabetum Technology", role="AI Engineer", sub="AI-Powered HRMS · Multi-Agent Platform", when="APR 2026 – PRESENT", where="CURRENT",
         acc=P["purple"], head="Building a multi-agent HR platform from scratch",
         bullets=["LangGraph state machine modelling 4 HR workflows as DAGs with conditional routing",
                  "Schema-aware NL → SQL: optimized read-only PostgreSQL with automatic multi-tenant isolation",
                  "RBAC + prompt-injection detection for PII; attrition-risk model, DistilBERT sentiment, doc generation"],
         chips=["LangGraph", "FastAPI", "PostgreSQL", "DistilBERT"]),
]


def experience():
    W, cw, gap, top = 1000, 310, 35, 78
    pad, bw = 22, 310 - 44 - 16
    # measure
    laid = []
    for r in ROLES:
        y = 34
        items = [("co", y)]
        y += 23; items.append(("role", y)); y += 18; items.append(("sub", y)); y += 20; items.append(("meta", y)); y += 16; items.append(("div", y)); y += 24
        hl = wrap(r["head"], cw - 2 * pad, "SG", 700, 14)
        items.append(("head", y, hl)); y += 19 * len(hl) + 8
        bl = []
        for bt in r["bullets"]:
            ls = wrap(bt, bw, "SG", 400, 12.8)
            bl.append((y, ls)); y += 18.5 * len(ls) + 8
        items.append(("bul", bl))
        laid.append((items, y))
    ch = max(y for _, y in laid) + 74
    H = top + ch + 4
    defs = [f'<linearGradient id="tl" x1="0" x2="1"><stop offset="0" stop-color="{P["pink"]}"/><stop offset=".5" stop-color="{P["cyan"]}"/><stop offset="1" stop-color="{P["purple"]}"/></linearGradient>']
    css = (".cin{animation:cin .9s cubic-bezier(.2,.8,.2,1) both}@keyframes cin{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}"
           ".halo{animation:halo 2s ease-out infinite;transform-box:fill-box;transform-origin:center}@keyframes halo{0%{opacity:.8;transform:scale(1)}100%{opacity:0;transform:scale(3)}}")
    b = []
    ty, x1, x2 = 46, 40, 960
    b.append(f'<line x1="{x1}" y1="{ty}" x2="{x2}" y2="{ty}" stroke="{P["line2"]}" stroke-width="2" stroke-linecap="round"/>')
    b.append(f'<line x1="{x1}" y1="{ty}" x2="{x1}" y2="{ty}" stroke="url(#tl)" stroke-width="3" stroke-linecap="round">'
             f'<animate attributeName="x2" from="{x1}" to="{x2}" begin=".2s" dur="2.6s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/></line>')
    for i, (r, (items, _)) in enumerate(zip(ROLES, laid)):
        x = i * (cw + gap)
        cx = x + cw / 2
        acc = r["acc"]
        frac = (cx - x1) / (x2 - x1)
        tnode = 0.2 + 2.6 * (0.15 + 0.85 * frac) * 0.85
        b.append(f'<circle cx="{cx}" cy="{ty}" r="8" fill="{P["bg1"]}" stroke="{P["line2"]}" stroke-width="2"/>'
                 f'<circle cx="{cx}" cy="{ty}" r="5" fill="{acc}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{tnode:.2f}s" dur=".3s" fill="freeze"/></circle>')
        if i == 2:
            b.append(f'<circle class="halo" cx="{cx}" cy="{ty}" r="6" fill="none" stroke="{acc}" stroke-width="2"/>')
        b.append(T(cx, ty - 20, r["when"], 11, "JB", 700, acc, "middle", ls=1.2))
        defs.append(frame_grad(f"cg{i}", 10 + i * 2, acc, P["line"], acc, 0.9))
        defs.append(f'<radialGradient id="cr{i}" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="{acc}" stop-opacity=".14"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></radialGradient>')
        g = [f'<g class="cin" style="animation-delay:{tnode-0.2:.2f}s"><g transform="translate({x} {top})">',
             f'<rect x=".7" y=".7" width="{cw-1.4}" height="{ch-1.4}" rx="16" fill="{P["card"]}"/>',
             f'<rect x=".7" y=".7" width="{cw-1.4}" height="{ch-1.4}" rx="16" fill="url(#cr{i})"/>',
             f'<rect x=".7" y=".7" width="{cw-1.4}" height="{ch-1.4}" rx="16" fill="none" stroke="url(#cg{i})" stroke-width="1.2"/>',
             f'<line x1="{cx-x}" y1="-{top-ty-8}" x2="{cx-x}" y2="0" stroke="{acc}" stroke-opacity=".35" stroke-dasharray="2 4"/>']
        for it in items:
            k = it[0]
            if k == "co":
                fs = 21 if text_width(r["co"], "SG", 700, 21) < cw - 2 * pad else 19
                g.append(T(pad, it[1], r["co"], fs, "SG", 700, P["text"]))
            elif k == "role":
                g.append(T(pad, it[1], r["role"], 14.5, "SG", 700, acc))
            elif k == "sub":
                g.append(T(pad, it[1], r["sub"], 12, "SG", 500, P["muted"]))
            elif k == "meta":
                tag = r["where"]
                g.append(T(pad, it[1], tag, 10, "JB", 700, P["dim"], ls=1.4))
                if i == 2:
                    s, _ = pill(cw - pad - 52, it[1] - 14, "NOW", "JB", 10, 700, P["mint"], "rgba(52,211,153,.1)", P["mint"], 10, 19, 1.2)
                    g.append(s)
            elif k == "div":
                g.append(f'<line x1="{pad}" x2="{cw-pad}" y1="{it[1]}" y2="{it[1]}" stroke="{P["line2"]}"/>')
            elif k == "head":
                for j, ln in enumerate(it[2]):
                    g.append(T(pad, it[1] + j * 19, ln, 14, "SG", 700, P["text"]))
            elif k == "bul":
                for (by, ls) in it[1]:
                    g.append(T(pad, by, "▸", 11, "JB", 700, acc))
                    for j, ln in enumerate(ls):
                        g.append(T(pad + 16, by + j * 18.5, ln, 12.8, "SG", 400, "#C9D4E8"))
        cxp, row = pad, 0
        for c in r["chips"]:
            w = text_width(c, "JB", 700, 10, 0.3) + 18
            if cxp + w > cw - pad:
                cxp, row = pad, row + 1
            s, w = pill(cxp, ch - 64 + row * 27, c, "JB", 10, 700, acc, "rgba(255,255,255,.03)", acc, 9, 21, 0.3, 6)
            g.append(s); cxp += w + 6
        g.append("</g></g>")
        b += g
    write("experience.svg", svg_doc(W, H, "".join(b), css, "Experience timeline",
                                    "Ripik.ai (Jan-Apr 2025) Engineering Intern; Renan (May 2025-Mar 2026) AI Engineer; Alphabetum Technology (Apr 2026-present) AI Engineer.",
                                    "".join(defs)))


# ------------------------------------------------------------------ blueprint
def node_h(w, title, sub):
    tl = wrap(title, w - 22, "SG", 700, 14)
    sl = wrap(sub, w - 22, "JB", 400, 9.6)
    return 42 + 17 * len(tl) + 2 + 13.5 * len(sl) + 4


def node(x, y, w, h, title, sub, acc, idx, big=False):
    out = [f'<g transform="translate({x} {y})">',
           f'<rect width="{w}" height="{h}" rx="13" fill="{P["card2"]}"/>',
           f'<rect width="{w}" height="{h}" rx="13" fill="url(#nodeSheen)"/>',
           f'<rect x=".6" y=".6" width="{w-1.2}" height="{h-1.2}" rx="12.5" fill="none" stroke="{acc}" stroke-opacity=".75" stroke-width="1.2"/>',
           f'<rect x="12" y="0" width="{min(40, w-24)}" height="2.5" rx="1.25" fill="{acc}"/>',
           T(12, 22, idx, 9.5, "JB", 700, acc, ls=1.2)]
    tl = wrap(title, w - 22, "SG", 700, 14)
    yy = 42
    for ln in tl:
        out.append(T(12, yy, ln, 14, "SG", 700, P["text"])); yy += 17
    yy += 2
    for ln in wrap(sub, w - 22, "JB", 400, 9.6):
        out.append(T(12, yy, ln, 9.6, "JB", 400, P["muted"])); yy += 13.5
    out.append("</g>")
    return "".join(out), yy


def blueprint():
    W, H = 1000, 480
    defs = [frame_grad("bf", 14), grid_pattern("dots", 22, P["line2"], 0.55),
            '<filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
            '<linearGradient id="nodeSheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>']
    css = (".flow{animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}"
           ".fb{animation:flow 2.4s linear infinite reverse}"
           ".nin{animation:nin .8s cubic-bezier(.2,.8,.2,1) both}@keyframes nin{from{opacity:0;transform:scale(.96)}to{opacity:1;transform:none}}")
    b = [f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="18" fill="#080C1A"/>',
         f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="18" fill="url(#dots)"/>',
         f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="18" fill="none" stroke="url(#bf)" stroke-width="1.3"/>',
         T(26, 36, "SYSTEM BLUEPRINT", 11, "JB", 700, P["cyan"], ls=2),
         T(26 + text_width("SYSTEM BLUEPRINT", "JB", 700, 11, 2) + 12, 36, "the shape of the LLM systems I ship to production", 12, "SG", 500, P["muted"]),
         f'<circle cx="{W-232}" cy="32" r="4" fill="{P["cyan"]}" filter="url(#glow)"/>', T(W - 222, 36, "request flow", 10.5, "JB", 400, P["muted"]),
         f'<line x1="{W-124}" x2="{W-104}" y1="32" y2="32" stroke="{P["amber"]}" stroke-width="1.6" stroke-dasharray="3 3"/>', T(W - 98, 36, "eval loop", 10.5, "JB", 400, P["muted"])]
    N = {
        "Q": (22, 196, 112, 84, "Query", "analyst · HR user · employee", P["sky"], "01"),
        "C": (156, 186, 132, 104, "Clarification Agent", "detects vague asks · smart follow-ups · session cache", P["cyan"], "02"),
        "O": (312, 150, 166, 176, "LangGraph Orchestrator", "state machine · conditional DAG routing · semantic router", P["violet"], "03"),
        "T1": (510, 68, 184, 96, "Agentic RAG", "metadata-filtered retrieval · hybrid search · recall 0.81", P["cyan"], "04a"),
        "T2": (510, 190, 184, 96, "NL → SQL Engine", "schema-aware · 4-stage validation · SQLGlot auto-fix", P["purple"], "04b"),
        "T3": (510, 312, 184, 96, "Document Q&A Agent", "PDF/XLSX/DOCX → markdown → S3 · Gemini metadata tags", P["pink"], "04c"),
        "G": (724, 112, 146, 112, "Guardrails", "RBAC · tenant isolation · prompt-injection · PII safety", P["mint"], "05"),
        "E": (724, 262, 146, 112, "Eval Harness", "recall/precision · groundedness · hallucination rate", P["amber"], "06"),
        "R": (890, 196, 88, 84, "Answer", "grounded · cached · schema-safe", P["sky"], "07"),
    }

    for k, v in list(N.items()):
        x, y, w, h = v[:4]
        need = node_h(w, v[4], v[5]) + (62 if k == "O" else 0)
        if need > h:
            cyy = y + h / 2
            N[k] = (x, cyy - need / 2, w, need) + v[4:]

    def port(k, side):
        x, y, w, h = N[k][:4]
        return {"r": (x + w, y + h / 2), "l": (x, y + h / 2), "b": (x + w / 2, y + h), "t": (x + w / 2, y)}[side]

    def curve(a, b_, bend=0.5):
        (x1, y1), (x2, y2) = a, b_
        dx = (x2 - x1) * bend
        return f"M{x1:.1f} {y1:.1f} C{x1+dx:.1f} {y1:.1f} {x2-dx:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"

    edges = [("Q", "C", P["sky"]), ("C", "O", P["cyan"]), ("O", "T1", P["cyan"]), ("O", "T2", P["purple"]), ("O", "T3", P["pink"]),
             ("T1", "G", P["cyan"]), ("T2", "G", P["purple"]), ("T3", "G", P["pink"]), ("G", "R", P["mint"])]
    eb = []
    for i, (a, c, col) in enumerate(edges):
        d = curve(port(a, "r"), port(c, "l"))
        pid = f"e{i}"
        eb.append(f'<path id="{pid}" d="{d}" fill="none" stroke="{P["line2"]}" stroke-width="1.6"/>')
        eb.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6" stroke-opacity=".75" stroke-dasharray="4 8" class="flow"/>')
        stage = {"Q": 0, "C": 1, "O": 2, "T1": 3, "T2": 3, "T3": 3, "G": 4}[a]
        dur = 1.6
        eb.append(f'<circle r="3.6" fill="{col}" filter="url(#glow)"><animateMotion dur="{dur}s" begin="{stage*0.55:.2f}s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".45 0 .55 1"><mpath xlink:href="#{pid}"/></animateMotion></circle>')
    # answer -> eval (logging) and eval -> orchestrator (feedback)
    rx, ry = port("R", "b"); ex, ey = port("E", "r")
    d1 = f"M{rx:.1f} {ry:.1f} C{rx:.1f} {ey:.1f} {ex+40:.1f} {ey:.1f} {ex:.1f} {ey:.1f}"
    eb.append(f'<path id="lg" d="{d1}" fill="none" stroke="{P["amber"]}" stroke-width="1.5" stroke-dasharray="3 4" class="fb" stroke-opacity=".85"/>')
    eb.append(f'<circle r="3" fill="{P["amber"]}" filter="url(#glow)"><animateMotion dur="2.4s" repeatCount="indefinite"><mpath xlink:href="#lg"/></animateMotion></circle>')
    bx, by = port("E", "b"); ox, oy = port("O", "b")
    d2 = f"M{bx:.1f} {by:.1f} C{bx:.1f} {by+70:.1f} {ox:.1f} {oy+120:.1f} {ox:.1f} {oy:.1f}"
    eb.append(f'<path id="fbk" d="{d2}" fill="none" stroke="{P["amber"]}" stroke-width="1.5" stroke-dasharray="3 4" class="fb" stroke-opacity=".85"/>')
    eb.append(f'<circle r="3.4" fill="{P["amber"]}" filter="url(#glow)"><animateMotion dur="3.6s" repeatCount="indefinite"><mpath xlink:href="#fbk"/></animateMotion></circle>')
    lbl = "eval feedback → prompt, routing & retrieval tuning"
    lw = text_width(lbl, "JB", 400, 10.5) + 20
    lx, ly = (bx + ox) / 2 - lw / 2 - 10, 436
    eb.append(f'<rect x="{lx:.1f}" y="{ly-15}" width="{lw:.1f}" height="22" rx="11" fill="#0B1226" stroke="{P["amber"]}" stroke-opacity=".5"/>'
              + T(lx + lw / 2, ly, lbl, 10.5, "JB", 400, P["amber"], "middle"))
    b += eb
    for j, (k, v) in enumerate(N.items()):
        s, endy = node(*v)
        b.append(f'<g class="nin" style="animation-delay:{j*0.09:.2f}s">{s}</g>')
    # mini DAG inside orchestrator
    ox0, oy0 = N["O"][0], N["O"][1]
    dy = N["O"][3] - 62
    pts = [(28, dy + 18), (70, dy + 4), (70, dy + 32), (112, dy + 18), (146, dy + 18)]
    dag = [f'<g transform="translate({ox0} {oy0})">']
    for a_, c_ in [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]:
        dag.append(f'<line x1="{pts[a_][0]}" y1="{pts[a_][1]}" x2="{pts[c_][0]}" y2="{pts[c_][1]}" stroke="{P["violet"]}" stroke-opacity=".6" stroke-width="1.2"/>')
    order = [0, 1, 2, 3, 4]
    for q, (px, py) in enumerate(pts):
        kt = q / len(pts)
        vals = ";".join("1" if k == order[q] else ".25" for k in range(len(pts))) + ";.25"
        dag.append(f'<circle cx="{px}" cy="{py}" r="6" fill="{P["bg1"]}" stroke="{P["purple"]}" stroke-width="1.4"/>'
                   f'<circle cx="{px}" cy="{py}" r="3.2" fill="{P["purple"]}" opacity=".25"><animate attributeName="opacity" values="{vals}" dur="2.5s" calcMode="discrete" repeatCount="indefinite"/></circle>')
    dag.append(T(12, dy + 52, "state: route → act → verify", 9, "JB", 400, P["dim"]))
    dag.append("</g>")
    b += dag
    write("blueprint.svg", svg_doc(W, H, "".join(b), css, "LLM system blueprint",
                                   "Pipeline: query, clarification agent, LangGraph orchestrator routing to agentic RAG, NL-to-SQL engine and document Q&A agent; guardrails (RBAC, tenant isolation, prompt-injection, PII); answer; eval harness feeding back into routing and retrieval.",
                                   "".join(defs)))


if __name__ == "__main__":
    experience(); blueprint()
