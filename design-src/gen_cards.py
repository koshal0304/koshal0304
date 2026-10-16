"""Buttons, terminal ("whoami") and impact-metrics SVGs."""
import math
from lib import *


# ---------------------------------------------------------------- buttons
def button(name, label, icon_svg, accent):
    tw = text_width(label, "SG", 700, 16)
    w, h = int(58 + tw + 10 + 14 + 24), 50
    defs = frame_grad("bg1", 6, accent, P["violet"], accent, 1)
    css = ".sh{animation:sh 3.6s ease-in-out infinite}@keyframes sh{0%{transform:translateX(-120px)}60%,100%{transform:translateX(330px)}}"
    defs += (f'<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<clipPath id="c"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14"/></clipPath>')
    b = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="#0B1124"/>'
         f'<g clip-path="url(#c)"><rect class="sh" x="0" y="0" width="70" height="{h}" fill="url(#shine)" transform="skewX(-20)"/></g>'
         f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="none" stroke="url(#bg1)" stroke-width="1.6"/>'
         f'<g transform="translate(22 13)">{icon_svg}</g>'
         + T(58, 31, label, 16, "SG", 700, P["text"])
         + T(58 + tw + 10, 31, "↗", 15, "JB", 700, accent))
    write(name, svg_doc(w, h, b, css, label, f"Button: {label}", defs))


def buttons():
    globe = (f'<g fill="none" stroke="{P["cyan"]}" stroke-width="1.8"><circle cx="12" cy="12" r="11"/>'
             f'<ellipse cx="12" cy="12" rx="5" ry="11"/><path d="M1 12h22M3.5 6h17M3.5 18h17"/></g>')
    lin = (f'<rect x="0" y="0" width="24" height="24" rx="5" fill="{P["sky"]}"/>'
           f'<rect x="5" y="9.5" width="3" height="9.5" fill="#0B1124"/><circle cx="6.5" cy="6" r="1.8" fill="#0B1124"/>'
           f'<path d="M10.5 9.5h2.9v1.4c.5-.9 1.6-1.6 3.1-1.6 2.6 0 3.3 1.6 3.3 4V19h-3v-5.1c0-1.2-.3-2.1-1.5-2.1s-1.8.9-1.8 2.1V19h-3z" fill="#0B1124"/>')
    mail = (f'<g fill="none" stroke="{P["pink"]}" stroke-width="1.8" stroke-linejoin="round">'
            f'<rect x="1" y="3.5" width="22" height="17" rx="3"/><path d="M2 5.5l10 8 10-8"/></g>')
    button("btn-portfolio.svg", "Portfolio", globe, P["cyan"])
    button("btn-linkedin.svg", "LinkedIn", lin, P["sky"])
    button("btn-email.svg", "Email me", mail, P["pink"])


# ---------------------------------------------------------------- terminal
def terminal():
    W, size, lh, x0, y0 = 1000, 15, 25, 34, 84
    cw = text_width("M", "JB", 400, size)
    K, V, D, S, N, G = P["purple"], P["text"], P["dim"], P["mint"], P["cyan"], P["muted"]
    script = [
        ("cmd", "whoami"),
        ("out", [("Koshal Kumar", V), (" — ", D), ("AI Engineer", N), (" @ Alphabetum Technology", V), (" · Bengaluru, IN", G)]),
        ("cmd", "cat focus.yaml"),
        ("out", [("builds:   ", K), ("production LLM systems — RAG, LangGraph multi-agents, NL→SQL, doc Q&A", V)]),
        ("out", [("owns:     ", K), ("end-to-end", N), (" · architecture → deployment · comfortable with ambiguity", V)]),
        ("out", [("obsessed: ", K), ("eval rigor", N), (" — recall/precision, groundedness, hallucination-rate tracking", V)]),
        ("out", [("stack:    ", K), ("[", D), ("LangChain, LangGraph, Azure OpenAI, Gemini, FastAPI, PostgreSQL, AWS", S), ("]", D)]),
        ("out", [("shipped:  ", K), ("recall 0.48→0.81", N), (" · ", D), ("S3 cost −60%", N), (" · ", D), ("review time −80%", N), (" · ", D), ("98% val acc", N)]),
        ("out", [("open_to:  ", K), ("AI / LLM Engineer roles ", V), ("✔", S)]),
        ("cmd", "echo $MOTTO"),
        ("out", [('"Separate the demo from a system people can trust."', S)]),
        ("prompt", None),
    ]
    H = y0 + lh * len(script) + 24
    defs = [frame_grad("fg", 12), f'<clipPath id="win"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
            f'<linearGradient id="tb" x1="0" x2="1"><stop offset="0" stop-color="#111a33"/><stop offset="1" stop-color="#0c1328"/></linearGradient>',
            grid_pattern("dots", 20, P["line2"], 0.35)]
    b = [f'<g clip-path="url(#win)"><rect width="{W}" height="{H}" fill="#080C1A"/><rect width="{W}" height="{H}" fill="url(#dots)"/>',
         f'<rect width="{W}" height="40" fill="url(#tb)"/><line x1="0" y1="40" x2="{W}" y2="40" stroke="{P["line"]}"/>',
         '<circle cx="24" cy="20" r="6" fill="#FF5F57"/><circle cx="44" cy="20" r="6" fill="#FEBC2E"/><circle cx="64" cy="20" r="6" fill="#28C840"/>',
         T(W / 2, 25, "koshal@neural-lab: ~/profile — zsh", 12, "JB", 400, P["dim"], "middle"),
         T(W - 24, 25, "● live", 11, "JB", 700, P["mint"], "end")]
    t, cur = 0.5, []   # cursor events (time, x, y)
    for i, (kind, data) in enumerate(script):
        y = y0 + i * lh
        if kind in ("cmd", "prompt"):
            b.append(T(x0, y, "❯", size, "JB", 700, P["pink"]))
            b.append(T(x0 + 2 * cw - 6, y, "~", size, "JB", 700, P["cyan"]))
            px = x0 + 4 * cw - 6
            cur.append((t, px, y))
            if kind == "cmd":
                n = len(data)
                ev = [(0, 0)] + [(k * 0.065, k * cw) for k in range(1, n + 1)]
                kt = ";".join(f"{e[0]/(n*0.065):.4f}" for e in ev)
                vals = ";".join(f"{e[1]:.1f}" for e in ev)
                defs.append(f'<clipPath id="c{i}"><rect x="{px}" y="{y-size}" height="{size*1.6}" width="0">'
                            f'<animate attributeName="width" begin="{t:.2f}s" dur="{n*0.065+0.001:.3f}s" fill="freeze" calcMode="discrete" keyTimes="{kt}" values="{vals}"/></rect></clipPath>')
                b.append(f'<g clip-path="url(#c{i})">' + T(px, y, data, size, "JB", 700, V) + "</g>")
                for k in range(1, n + 1):
                    cur.append((t + k * 0.065, px + k * cw, y))
                t += n * 0.065 + 0.28
        else:
            x = x0 + 2 * cw
            parts = []
            for s, col in data:
                parts.append(T(x, y, s, size, "JB", 400, col))
                x += text_width(s, "JB", 400, size)
            b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".25s" fill="freeze"/>' + "".join(parts) + "</g>")
            t += 0.16
            if i + 1 < len(script) and script[i + 1][0] != "out":
                t += 0.35
    # cursor path
    cur.sort()
    total = cur[-1][0] + 0.01
    kt = ";".join(["0"] + [f"{c[0]/total:.4f}" for c in cur])
    xs = ";".join([f"{cur[0][1]:.1f}"] + [f"{c[1]+1:.1f}" for c in cur])
    ys = ";".join([f"{cur[0][2]-size*0.8:.1f}"] + [f"{c[2]-size*0.8:.1f}" for c in cur])
    b.append(f'<rect width="{cw:.1f}" height="{size*1.1:.1f}" rx="1.5" fill="{P["cyan"]}" x="{cur[0][1]:.1f}" y="{cur[0][2]-size*0.8:.1f}">'
             f'<animate attributeName="x" dur="{total:.2f}s" fill="freeze" calcMode="discrete" keyTimes="{kt}" values="{xs}"/>'
             f'<animate attributeName="y" dur="{total:.2f}s" fill="freeze" calcMode="discrete" keyTimes="{kt}" values="{ys}"/>'
             f'<animate attributeName="opacity" values="1;.1;1" dur="1.05s" repeatCount="indefinite"/></rect>')
    b.append("</g>")
    b.append(f'<rect x=".7" y=".7" width="{W-1.4}" height="{H-1.4}" rx="16" fill="none" stroke="url(#fg)" stroke-width="1.3"/>')
    write("terminal.svg", svg_doc(W, H, "".join(b), "", "whoami — Koshal Kumar",
                                  "Terminal: Koshal Kumar, AI Engineer at Alphabetum Technology, Bengaluru. Builds production LLM systems (RAG, LangGraph multi-agents, NL-to-SQL, document Q&A); end-to-end ownership; focused on evaluation rigor. Open to AI/LLM Engineer roles.",
                                  "".join(defs)))


# ---------------------------------------------------------------- impact
def odometer(x, y, prefix, digits, suffix, size, fill, begin=0.3, uid="o"):
    """Rolling-digit counter. Returns (svg, defs)."""
    dw = max(text_width(str(d), "SG", 700, size) for d in range(10))
    lh = size * 1.0
    out, defs = [], []
    cx = x
    if prefix:
        out.append(T(cx, y, prefix, size, "SG", 700, fill))
        cx += text_width(prefix, "SG", 700, size) + 2
    for j, ch in enumerate(digits):
        target = int(ch)
        spins = 10 + target if j == 0 else 20 + target  # extra turns -> a satisfying roll
        cid = f"{uid}{j}"
        defs.append(f'<clipPath id="{cid}"><rect x="{cx-2}" y="{y-size*0.86}" width="{dw+4}" height="{size*1.02}"/></clipPath>')
        col = "".join(T(cx + dw / 2, y + k * lh, str(k % 10), size, "SG", 700, fill, "middle") for k in range(spins + 1))
        out.append(f'<g clip-path="url(#{cid})"><g transform="translate(0 {-spins*lh:.1f})">'
                   f'<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {-spins*lh:.1f}" begin="{begin+j*0.12:.2f}s" dur="{1.9+j*0.25:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".15 .7 .2 1"/>'
                   f'{col}</g></g>')
        cx += dw
    if suffix:
        out.append(T(cx + 2, y, suffix, size * 0.62, "SG", 700, fill))
    return "".join(out), "".join(defs)


def impact():
    W, H, cwid, gap = 1000, 250, 238, 16
    cards = [
        dict(kick="RAG · RENAN", pre="+", num="69", suf="%", label="retrieval recall lift", sub="0.48 → 0.81 · zero manual labels",
             acc=P["cyan"], viz="bars", a=0.48, b=0.81, la="before", lb="after"),
        dict(kick="AWS · RIPIK.AI", pre="−", num="60", suf="%", label="S3 storage cost", sub="10K+ files · 150 parallel workers",
             acc=P["mint"], viz="shrink", a=1.0, b=0.40, la="storage spend", lb=""),
        dict(kick="VISION · RIPIK.AI", pre="", num="98", suf="%", label="validation accuracy", sub="ResNet18 fine-tune · 3-class kilns",
             acc=P["purple"], viz="curve"),
        dict(kick="GEN-AI OPS · RIPIK.AI", pre="−", num="80", suf="%", label="manual review time", sub="Gemini vision · 100+ images/day",
             acc=P["pink"], viz="shrink", a=1.0, b=0.20, la="review hours", lb=""),
    ]
    defs, b = [], []
    css = ".cin{animation:cin .9s cubic-bezier(.2,.8,.2,1) both}@keyframes cin{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}"
    for i, c in enumerate(cards):
        x = i * (cwid + gap)
        acc = c["acc"]
        gid = f"g{i}"
        defs.append(frame_grad(gid, 9 + i, acc, P["line2"], acc, 1))
        defs.append(f'<linearGradient id="fill{i}" x1="0" x2="1"><stop offset="0" stop-color="{acc}" stop-opacity=".35"/><stop offset="1" stop-color="{acc}"/></linearGradient>')
        defs.append(f'<radialGradient id="rg{i}" cx=".85" cy="0" r="1"><stop offset="0" stop-color="{acc}" stop-opacity=".18"/><stop offset=".6" stop-color="{acc}" stop-opacity="0"/></radialGradient>')
        g = [f'<g class="cin" style="animation-delay:{i*0.12:.2f}s"><g transform="translate({x} 0)">',
             f'<rect x=".7" y=".7" width="{cwid-1.4}" height="{H-1.4}" rx="16" fill="{P["card"]}"/>',
             f'<rect x=".7" y=".7" width="{cwid-1.4}" height="{H-1.4}" rx="16" fill="url(#rg{i})"/>',
             f'<rect x=".7" y=".7" width="{cwid-1.4}" height="{H-1.4}" rx="16" fill="none" stroke="url(#{gid})" stroke-width="1.2"/>',
             T(20, 32, c["kick"], 10.5, "JB", 700, acc, ls=1.4)]
        od, od_defs = odometer(20, 96, c["pre"], c["num"], c["suf"], 54, P["text"], 0.35 + i * 0.15, f"o{i}_")
        defs.append(od_defs)
        g.append(od)
        g.append(T(20, 126, c["label"], 15, "SG", 500, P["text"]))
        g.append(T(20, 147, c["sub"], 10.5, "JB", 400, P["muted"]))
        vx, vw, vy = 20, cwid - 40, 172
        if c["viz"] == "bars":
            for k, (lab, val, col, dl) in enumerate([(c["la"], c["a"], P["dim"], 0.4), (c["lb"], c["b"], acc, 0.9)]):
                yy = vy + k * 30
                g.append(f'<rect x="{vx}" y="{yy}" width="{vw}" height="10" rx="5" fill="{P["line"]}"/>')
                g.append(f'<rect x="{vx}" y="{yy}" width="0" height="10" rx="5" fill="{"url(#fill%d)" % i if k else col}">'
                         f'<animate attributeName="width" from="0" to="{vw*val:.1f}" begin="{dl+i*0.15:.2f}s" dur="1.4s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect>')
                g.append(T(vx, yy + 24, lab, 10, "JB", 400, P["dim"]))
                g.append(T(vx + vw, yy + 24, f"{val:.2f}", 10, "JB", 700, col if k == 0 else acc, "end"))
        elif c["viz"] == "shrink":
            g.append(f'<rect x="{vx}" y="{vy+6}" width="{vw}" height="14" rx="7" fill="{P["line"]}"/>')
            g.append(f'<rect x="{vx}" y="{vy+6}" width="{vw}" height="14" rx="7" fill="url(#fill{i})">'
                     f'<animate attributeName="width" from="{vw}" to="{vw*c["b"]:.1f}" begin="{0.6+i*0.15:.2f}s" dur="1.6s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect>')
            g.append(f'<line x1="{vx+vw*c["b"]:.1f}" x2="{vx+vw*c["b"]:.1f}" y1="{vy}" y2="{vy+26}" stroke="{acc}" stroke-dasharray="2 3" opacity=".8"/>')
            g.append(T(vx, vy + 46, c["la"], 10, "JB", 400, P["dim"]))
            g.append(T(vx + vw, vy + 46, f"100% → {int(c['b']*100)}%", 10, "JB", 700, acc, "end"))
        else:  # segmented meter: 49 of 50 cells light up (98%)
            nseg, segw = 50, vw / 50
            for k in range(nseg):
                lit = k < 49
                sx = vx + k * segw
                if lit:
                    g.append(f'<rect x="{sx:.1f}" y="{vy+4}" width="{segw-1.2:.1f}" height="18" rx="1.2" fill="{P["line"]}"/>'
                             f'<rect x="{sx:.1f}" y="{vy+4}" width="{segw-1.2:.1f}" height="18" rx="1.2" fill="{acc}" opacity="0">'
                             f'<animate attributeName="opacity" from="0" to="{0.35+0.65*k/49:.2f}" begin="{0.7+i*0.15+k*0.03:.2f}s" dur=".2s" fill="freeze"/></rect>')
                else:
                    g.append(f'<rect x="{sx:.1f}" y="{vy+4}" width="{segw-1.2:.1f}" height="18" rx="1.2" fill="none" stroke="{P["dim"]}" stroke-width=".8"/>')
            g.append(T(vx, vy + 46, "validation accuracy", 10, "JB", 400, P["dim"]))
            g.append(T(vx + vw, vy + 46, "acc 0.98", 10, "JB", 700, acc, "end"))
        g.append("</g></g>")
        b += g
    write("impact.svg", svg_doc(W, H, "".join(b), css, "Impact in numbers",
                                "+69% RAG retrieval recall (0.48 to 0.81) at Renan; -60% AWS S3 storage cost at Ripik.ai; 98% validation accuracy on ResNet18 kiln classifier; -80% manual image review time via Gemini pipeline.",
                                "".join(defs)))


if __name__ == "__main__":
    buttons(); terminal(); impact()
