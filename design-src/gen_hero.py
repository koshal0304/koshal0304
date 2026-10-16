import base64, math, random
from lib import *

W, H = 1000, 440
random.seed(7)


def typing_block(x0, y, phrases, size=19, color=None):
    """Type / delete phrases in a loop with SMIL discrete animations (no JS)."""
    color = color or P["text"]
    cw = text_width("M", "JB", 400, size)
    t_char, t_del, hold, gap = 0.055, 0.022, 1.7, 0.35
    slots, t = [], 0.0
    for ph in phrases:
        n = len(ph)
        slots.append((t, n))
        t += n * t_char + hold + n * t_del + gap
    total = t
    defs, body, cursor_ev = [], [], [(0.0, 0.0)]
    for i, (ph, (start, n)) in enumerate(zip(phrases, slots)):
        ev = [(0.0, 0.0)]
        for k in range(1, n + 1):
            ev.append((start + k * t_char, k * cw))
        hold_end = start + n * t_char + hold
        for k in range(1, n + 1):
            ev.append((hold_end + k * t_del, (n - k) * cw))
        cursor_ev += ev[1:]
        kt = ";".join(f"{e[0]/total:.5f}" for e in ev)
        vals = ";".join(f"{e[1]:.1f}" for e in ev)
        defs.append(
            f'<clipPath id="tc{i}"><rect x="{x0}" y="{y-size}" height="{size*1.5}" width="0">'
            f'<animate attributeName="width" dur="{total:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/>'
            f'</rect></clipPath>')
        body.append(f'<g clip-path="url(#tc{i})">' + T(x0, y, ph, size, "JB", 400, color) + "</g>")
    cursor_ev.sort()
    kt = ";".join(f"{e[0]/total:.5f}" for e in cursor_ev)
    vals = ";".join(f"{x0 + e[1] + 2:.1f}" for e in cursor_ev)
    body.append(
        f'<rect x="{x0+2}" y="{y-size*0.82:.1f}" width="{cw*0.9:.1f}" height="{size*1.05:.1f}" rx="2" fill="{P["cyan"]}">'
        f'<animate attributeName="x" dur="{total:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/>'
        f'<animate attributeName="opacity" values="1;0.15;1" dur="1s" repeatCount="indefinite"/></rect>')
    return "".join(defs), "".join(body)


def orbit_paths(cx, cy, rx, ry, deg):
    a = math.radians(deg)
    L = (cx - rx * math.cos(a), cy - rx * math.sin(a))
    R = (cx + rx * math.cos(a), cy + rx * math.sin(a))
    back = f"M{L[0]:.2f} {L[1]:.2f} A{rx} {ry} {deg} 0 1 {R[0]:.2f} {R[1]:.2f}"
    front = f"M{R[0]:.2f} {R[1]:.2f} A{rx} {ry} {deg} 0 1 {L[0]:.2f} {L[1]:.2f}"
    full = back + f" A{rx} {ry} {deg} 0 1 {L[0]:.2f} {L[1]:.2f}"
    return back, front, full


def traveler(label, full, dur, begin, layer, color):
    pw = text_width(label, "JB", 700, 11, 0.4) + 18
    vis = "1;0" if layer == "back" else "0;1"
    op = 0.6 if layer == "back" else 1
    return (
        f'<g opacity="0"><animate attributeName="opacity" values="{vis}" keyTimes="0;0.5" calcMode="discrete" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f'<g opacity="{op}">'
        f'<rect x="{-pw/2-6:.1f}" y="-11" width="{pw+12:.1f}" height="22" rx="11" fill="#0B1226" stroke="{color}" stroke-opacity="0.75"/>'
        f'<circle cx="{-pw/2+5:.1f}" r="3.2" fill="{color}" filter="url(#glow)"/>'
        + T(6, 4, label, 11, "JB", 700, color, "middle", ls=0.4) +
        f'</g><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{full}"/></g>')


def build():
    photo = base64.b64encode(open("photo.jpg", "rb").read()).decode()
    defs = []
    css = """
    .blob{animation:drift 18s ease-in-out infinite alternate}
    .b2{animation-duration:23s;animation-direction:alternate-reverse}
    .b3{animation-duration:29s}
    @keyframes drift{0%{transform:translate(0,0) scale(1)}50%{transform:translate(60px,-30px) scale(1.15)}100%{transform:translate(-40px,25px) scale(.95)}}
    .pt{animation:rise linear infinite;opacity:0}
    @keyframes rise{0%{transform:translateY(0);opacity:0}15%{opacity:.9}100%{transform:translateY(-140px);opacity:0}}
    .fade{animation:fin 1.1s cubic-bezier(.2,.8,.2,1) both}
    @keyframes fin{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
    .d1{animation-delay:.15s}.d2{animation-delay:.35s}.d3{animation-delay:.55s}.d4{animation-delay:.75s}.d5{animation-delay:.95s}
    .pulse{animation:pulse 2.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
    @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(1.9)}}
    .halo{animation:halo 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
    @keyframes halo{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:.9;transform:scale(1.07)}}
    """
    defs.append(f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>')
    defs.append('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060914"/><stop offset=".55" stop-color="#090E22"/><stop offset="1" stop-color="#0D0A24"/></linearGradient>')
    defs.append('<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>')
    defs.append('<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    defs.append(grid_pattern("dots", 24, P["line2"], 0.5))
    defs.append(frame_grad("frameGrad", 10))
    # name shimmer gradient (seamless repeat)
    defs.append(
        f'<linearGradient id="nameGrad" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="520" y2="0" spreadMethod="repeat">'
        f'<stop offset="0" stop-color="{P["cyan"]}"/><stop offset=".33" stop-color="{P["purple"]}"/>'
        f'<stop offset=".66" stop-color="{P["pink"]}"/><stop offset="1" stop-color="{P["cyan"]}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="520 0" dur="7s" repeatCount="indefinite"/></linearGradient>')
    defs.append(f'<linearGradient id="floorFade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>')
    defs.append(f'<mask id="floorMask"><rect x="0" y="345" width="{W}" height="{H-345}" fill="url(#floorFade)"/></mask>')
    defs.append(f'<radialGradient id="photoGlow"><stop offset="0" stop-color="{P["violet"]}" stop-opacity=".55"/><stop offset=".6" stop-color="{P["cyan"]}" stop-opacity=".12"/><stop offset="1" stop-color="{P["cyan"]}" stop-opacity="0"/></radialGradient>')
    defs.append(f'<linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{P["cyan"]}"/><stop offset=".5" stop-color="{P["violet"]}"/><stop offset="1" stop-color="{P["pink"]}"/></linearGradient>')
    defs.append(f'<linearGradient id="orbA" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P["cyan"]}" stop-opacity=".9"/><stop offset="1" stop-color="{P["violet"]}" stop-opacity=".9"/></linearGradient>')
    defs.append(f'<linearGradient id="orbB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P["pink"]}" stop-opacity=".9"/><stop offset="1" stop-color="{P["sky"]}" stop-opacity=".9"/></linearGradient>')
    defs.append('<linearGradient id="horizon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22D3EE" stop-opacity="0"/><stop offset=".5" stop-color="#A78BFA" stop-opacity=".95"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></linearGradient>')

    b = [f'<g clip-path="url(#frame)">', f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    # aurora
    b.append(f'<g filter="url(#blur)" opacity=".55">'
             f'<circle class="blob" cx="220" cy="90" r="150" fill="{P["violet"]}" opacity=".55"/>'
             f'<circle class="blob b2" cx="780" cy="140" r="170" fill="{P["cyan"]}" opacity=".35"/>'
             f'<circle class="blob b3" cx="560" cy="380" r="160" fill="{P["pink"]}" opacity=".28"/></g>')
    b.append(f'<rect width="{W}" height="345" fill="url(#dots)"/>')

    # perspective floor (3D grid flying toward the viewer)
    hy, fh, vpx = 345, H - 345, 500
    fl = [f'<g mask="url(#floorMask)">', f'<rect x="0" y="{hy}" width="{W}" height="{fh}" fill="#070A1A"/>']
    for i in range(-14, 15):
        xb = vpx + i * 95
        xt = vpx + i * 95 * 0.10
        fl.append(f'<line x1="{xt:.1f}" y1="{hy}" x2="{xb:.1f}" y2="{H}" stroke="{P["violet"]}" stroke-opacity=".55" stroke-width="1"/>')
    N, step = 8, 0.9
    ys = [hy + fh * (k / N) ** 2.2 for k in range(N + 1)] + [H + 30]
    vals = ";".join(f"{y:.1f}" for y in ys)
    for k in range(N + 1):
        fl.append(f'<line x1="0" x2="{W}" y1="{hy}" y2="{hy}" stroke="{P["cyan"]}" stroke-opacity=".6" stroke-width="1.1">'
                  f'<animate attributeName="y1" values="{vals}" dur="{(N+1)*step:.1f}s" begin="-{k*step:.1f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y2" values="{vals}" dur="{(N+1)*step:.1f}s" begin="-{k*step:.1f}s" repeatCount="indefinite"/></line>')
    fl.append("</g>")
    b += fl
    b.append(f'<rect x="0" y="{hy-1.2}" width="{W}" height="2.4" fill="url(#horizon)" filter="url(#glow)"/>')

    # particles
    for _ in range(26):
        x, y = random.uniform(20, 980), random.uniform(140, 360)
        r = random.choice([1, 1.2, 1.6, 2])
        col = random.choice([P["cyan"], P["purple"], P["pink"], "#ffffff"])
        d, dl = random.uniform(6, 13), random.uniform(0, 12)
        b.append(f'<circle class="pt" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" style="animation-duration:{d:.1f}s;animation-delay:-{dl:.1f}s"/>')

    # --- portrait with 3D orbits ---
    cx, cy, R = 772, 196, 100
    orbits = [(166, 44, -18, "url(#orbA)", P["cyan"], ["LangGraph", "RAG"], 14),
              (158, 38, 22, "url(#orbB)", P["pink"], ["NL→SQL", "Evals"], 17)]
    b.append(f'<circle class="halo" cx="{cx}" cy="{cy}" r="160" fill="url(#photoGlow)"/>')
    backs, fronts = [], []
    for rx, ry, deg, stroke, col, labels, dur in orbits:
        back, front, full = orbit_paths(cx, cy, rx, ry, deg)
        backs.append(f'<path d="{back}" fill="none" stroke="{stroke}" stroke-width="1.4" stroke-opacity=".35" stroke-dasharray="3 5"/>')
        fronts.append(f'<path d="{front}" fill="none" stroke="{stroke}" stroke-width="1.8" stroke-opacity=".9"/>')
        for j, lab in enumerate(labels):
            begin = -j * dur / 2
            backs.append(traveler(lab, full, dur, begin, "back", col))
            fronts.append(traveler(lab, full, dur, begin, "front", col))
    b += backs
    # rings
    b.append(f'<g transform="translate({cx} {cy})">'
             f'<circle r="{R+28}" fill="none" stroke="{P["line2"]}" stroke-width="1" stroke-dasharray="1 7" stroke-linecap="round">'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="40s" repeatCount="indefinite"/></circle>'
             f'<circle r="{R+14}" fill="none" stroke="url(#ringGrad)" stroke-width="3" stroke-linecap="round" stroke-dasharray="210 60 90 50 40 300">'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></circle>'
             f'<circle r="{R+6}" fill="none" stroke="{P["purple"]}" stroke-opacity=".35" stroke-width="1"/></g>')
    defs.append(f'<clipPath id="pc"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>')
    defs.append(f'<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset=".6" stop-color="#0A0F1F" stop-opacity="0"/><stop offset="1" stop-color="#0A0F1F" stop-opacity=".55"/></linearGradient>')
    b.append(f'<g clip-path="url(#pc)"><image x="{cx-R}" y="{cy-R}" width="{2*R}" height="{2*R}" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{photo}"/>'
             f'<rect x="{cx-R}" y="{cy-R}" width="{2*R}" height="{2*R}" fill="url(#shade)"/></g>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#ffffff" stroke-opacity=".15" stroke-width="1.5"/>')
    b += fronts

    # --- text block ---
    x0 = 56
    chip1, w1 = pill(x0 + 16, 46, "OPEN TO AI / LLM ENGINEER ROLES", "JB", 11, 700, P["mint"], "rgba(52,211,153,.08)", P["mint"], 14, 26, 0.8, 13)
    b.append(f'<g class="fade">{chip1}<circle cx="{x0+14}" cy="59" r="4" fill="{P["mint"]}"/><circle class="pulse" cx="{x0+14}" cy="59" r="4" fill="{P["mint"]}"/></g>')
    chip2, w2 = pill(x0 + 16 + w1 + 10, 46, "BENGALURU · IN", "JB", 11, 700, P["muted"], "rgba(154,168,194,.06)", P["muted"], 14, 26, 0.8, 13)
    b.append(f'<g class="fade">{chip2}</g>')
    b.append(f'<g class="fade d1">' + T(x0, 122, "// hello, world — I'm", 15, "JB", 400, P["cyan"]) + "</g>")
    b.append(f'<g class="fade d2">' + T(x0 - 3, 186, "Koshal Kumar", 66, "SG", 700, "url(#nameGrad)", ls=-1.5) + "</g>")
    b.append(f'<g class="fade d3">' + T(x0, 224, "AI ENGINEER", 15, "JB", 700, P["text"], ls=4.5)
             + T(x0 + text_width("AI ENGINEER", "JB", 700, 15, 4.5) + 10, 224, "· LLM SYSTEMS · AGENTS · RAG", 15, "JB", 400, P["muted"], ls=1.2) + "</g>")
    tdefs, tbody = typing_block(x0 + 24, 272, [
        "shipping production LLM systems",
        "orchestrating LangGraph multi-agents",
        "lifting RAG recall 0.48 → 0.81",
        "schema-aware NL → SQL, RBAC-gated",
        "eval harnesses that catch hallucinations",
    ])
    defs.append(tdefs)
    b.append(f'<g class="fade d4">' + T(x0, 272, "❯", 19, "JB", 700, P["pink"]) + tbody + "</g>")
    # stack chips
    x = x0
    chips = [("LangGraph", P["cyan"]), ("LangChain", P["sky"]), ("Azure OpenAI", P["purple"]), ("FastAPI", P["mint"]), ("PostgreSQL", P["pink"]), ("AWS", P["amber"])]
    g = ['<g class="fade d5">']
    for lab, col in chips:
        s, w = pill(x, 300, lab, "JB", 11, 700, col, "rgba(255,255,255,.03)", col, 11, 24, 0.3, 7)
        g.append(s); x += w + 8
    g.append("</g>")
    b += g
    b.append("</g>")
    b.append(card_frame(W, H, 22, "frameGrad", "none", 1.4).split("/>", 1)[1])

    svg = svg_doc(W, H, "".join(b), css, "Koshal Kumar — AI Engineer",
                  "Animated banner: Koshal Kumar, AI Engineer building production LLM systems (LangGraph agents, RAG, NL-to-SQL, evals). Portrait with 3D orbiting skills over a perspective grid.",
                  "".join(defs))
    write("hero.svg", svg)


if __name__ == "__main__":
    build()
