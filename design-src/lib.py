"""Shared helpers for building self-contained animated SVGs for the GitHub profile."""
import base64, html, io, json, math, os, re
from fontTools.ttLib import TTFont
from fontTools import subset as ftsubset

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)          # repo root
ASSETS = os.path.join(OUT, "assets")

FD = os.path.join(HERE, "fonts")
FONT_FILES = {
    ("SG", 400): f"{FD}/space-grotesk-latin-400-normal.woff2",
    ("SG", 500): f"{FD}/space-grotesk-latin-500-normal.woff2",
    ("SG", 700): f"{FD}/space-grotesk-latin-700-normal.woff2",
    ("JB", 400): f"{FD}/jetbrains-mono-latin-400-normal.woff2",
    ("JB", 700): f"{FD}/jetbrains-mono-latin-700-normal.woff2",
    ("SYM", 400): f"{FD}/sym-400.ttf",   # DejaVu Sans Mono symbol subset (arrows, checks, shapes)
    ("SYM", 700): f"{FD}/sym-700.ttf",
}

P = dict(
    bg0="#05070F", bg1="#0A0F1F", card="#0C1224", card2="#101830", line="#1C2541", line2="#26325A",
    text="#E6EDF7", muted="#9AA8C2", dim="#5B6782",
    cyan="#22D3EE", sky="#38BDF8", violet="#8B5CF6", purple="#A78BFA", pink="#E879F9",
    mint="#34D399", amber="#FBBF24", rose="#FB7185",
)

SG = "SG,'Space Grotesk','Segoe UI',Ubuntu,Arial,sans-serif"
JB = "JB,SYM,'JetBrains Mono',Consolas,'Courier New',monospace"
SGS = "SG,SYM,'Space Grotesk','Segoe UI',Ubuntu,Arial,sans-serif"

_font_cache = {}


def _font(key):
    if key not in _font_cache:
        _font_cache[key] = TTFont(FONT_FILES[key])
    return _font_cache[key]


def text_width(s, fam="SG", weight=700, size=16, letter=0.0):
    """Measure rendered width (px) of a string with the embedded font (falls back to SYM)."""
    f = _font((fam, weight))
    cmap = f.getBestCmap(); hmtx = f["hmtx"]; upm = f["head"].unitsPerEm
    sym = _font(("SYM", 400)); scm = sym.getBestCmap(); shm = sym["hmtx"]; supm = sym["head"].unitsPerEm
    w = 0.0
    for ch in s:
        cp = ord(ch)
        if cp in cmap:
            w += hmtx[cmap[cp]][0] / upm * size
        elif cp in scm:
            w += shm[scm[cp]][0] / supm * size
        else:
            w += 0.6 * size
        w += letter
    return w


def esc(s):
    return html.escape(s, quote=True)


def _chars_in(svg):
    chars = set()
    for m in re.finditer(r"<text\b[^>]*>(.*?)</text>", svg, re.S):
        inner = re.sub(r"<[^>]+>", "", m.group(1))
        chars |= set(html.unescape(inner))
    return chars


def font_css(svg, extra=""):
    chars = _chars_in(svg) | set(extra) | {" "}
    css = []
    used = set(re.findall(r"font-family:\s*([A-Z]{2,3})\b", svg)) | set(re.findall(r'font-family="([A-Z]{2,3})\b', svg))
    used |= set(re.findall(r"\b(SG|JB)\b,", svg))
    if "JB" in used or "SG" in used:
        used.add("SYM")
    for (fam, wt), path in FONT_FILES.items():
        if fam not in used:
            continue
        f = TTFont(path)
        cmap = f.getBestCmap()
        need = "".join(c for c in chars if ord(c) in cmap)
        if fam == "SYM":
            # only glyphs the primary fonts lack
            prim = _font(("JB", 400)).getBestCmap()
            prim2 = _font(("SG", 700)).getBestCmap()
            need = "".join(c for c in chars if ord(c) in cmap and ord(c) not in prim and ord(c) not in prim2)
            if not need.strip():
                continue
        if not need:
            continue
        opts = ftsubset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "tnum", "calt", "ccmp", "locl"]
        opts.name_IDs = []
        opts.notdef_outline = False
        opts.hinting = False
        opts.desubroutinize = True
        sub = ftsubset.Subsetter(opts)
        sub.populate(unicodes=[ord(c) for c in need])
        sub.subset(f)
        buf = io.BytesIO()
        f.flavor = "woff2"
        f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{b64}) format('woff2');font-weight:{wt};font-style:normal}}")
    return "\n".join(css)


REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}}"


def svg_doc(w, h, body, css="", title="", desc="", defs=""):
    pre = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
        f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
    )
    draft = pre + "<style>__FONTS__" + css + REDUCED + "</style><defs>" + defs + "</defs>" + body + "</svg>"
    fonts = font_css(draft)
    return draft.replace("__FONTS__", fonts)


def write(name, svg):
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"{name:28s} {len(svg.encode())/1024:7.1f} KB")
    return path


def T(x, y, s, size=14, fam="SG", weight=500, fill=None, anchor="start", cls="", extra="", ls=None):
    fill = fill or P["text"]
    ff = {"SG": SGS, "JB": JB}[fam]
    lsa = f' letter-spacing="{ls}"' if ls is not None else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{ff}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{lsa}{c} xml:space="preserve" {extra}>{esc(s)}</text>')


def wrap(s, maxw, fam="SG", weight=400, size=13):
    s = s.replace(" · ", "\u00a0· ").replace(" → ", "\u00a0→ ")
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_width(t, fam, weight, size) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


ICONS = json.load(open(os.path.join(HERE, "icons.json")))


def icon(key, x, y, size, color=None):
    """Simple-icons brand glyph (24x24 viewbox) placed at x,y with given size."""
    ic = ICONS[key]
    col = color or ("#" + ic["hex"])
    s = size / 24
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" d="{ic["path"]}" fill="{col}"/>'


def lift(hexcol, min_l=0.55):
    """Brighten very dark brand colours so they read on a dark background."""
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if l >= min_l:
        return "#" + h
    k = (min_l - l)
    r, g, b = (min(1, c + k * (1.25)) for c in (r, g, b))
    return "#%02X%02X%02X" % (int(r * 255), int(g * 255), int(b * 255))


def card_frame(w, h, r=18, grad_id="frameGrad", fill=None, stroke_w=1.2):
    fill = fill or P["card"]
    return (f'<rect x="0.6" y="0.6" width="{w-1.2}" height="{h-1.2}" rx="{r}" fill="{fill}"/>'
            f'<rect x="0.6" y="0.6" width="{w-1.2}" height="{h-1.2}" rx="{r}" fill="none" stroke="url(#{grad_id})" stroke-width="{stroke_w}"/>')


def frame_grad(gid="frameGrad", dur=8, a=None, b=None, c=None, opacity=0.9):
    a = a or P["cyan"]; b = b or P["violet"]; c = c or P["pink"]
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{a}" stop-opacity="{opacity}"/>'
            f'<stop offset="0.5" stop-color="{b}" stop-opacity="{opacity*0.35}"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity="{opacity}"/>'
            f'<animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="{dur}s" repeatCount="indefinite"/>'
            f'</linearGradient>')


def grid_pattern(pid="dots", gap=22, col=None, op=0.35):
    col = col or P["line2"]
    return (f'<pattern id="{pid}" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse">'
            f'<circle cx="1" cy="1" r="1" fill="{col}" opacity="{op}"/></pattern>')


def pill(x, y, label, fam="JB", size=11, weight=700, fg=None, bg=None, stroke=None, padx=10, h=22, ls=0.6, rx=None):
    fg = fg or P["cyan"]; bg = bg or "rgba(34,211,238,0.08)"; stroke = stroke or fg
    w = text_width(label, fam, weight, size, ls) + padx * 2
    rx = h / 2 if rx is None else rx
    out = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{rx}" fill="{bg}" stroke="{stroke}" stroke-opacity="0.45"/>'
           + T(x + w / 2, y + h / 2 + size * 0.36, label, size, fam, weight, fg, "middle", ls=ls))
    return out, w
