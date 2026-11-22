#!/usr/bin/env python3
"""Draw entry.png for the make.fun "News image 22 Nov" bounty.

One 1024x1024 newspaper front page summing up 22 November 2026:
a navy masthead, one lead story (Trump-Xi-Putin trilateral summit),
two medium stories (Mexico captures 'El Chapo Isidro'; COP31 overtime),
three small stories (US stocks correction; Kryvyi Rih strike;
Iran strikes Bahrain), plus an ALSO ticker and a sources footer.

Layout mirrors the proven 19 November entry: masthead, lead panel,
2 medium panels, 3 small panels, ticker, sources line.

Run: python3 draw_entry.py  -> writes entry.png next to this script.
Stdlib + Pillow only. No network.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (246, 241, 229)        # cream paper
NAVY = (16, 30, 60)
GOLD = (217, 164, 65)
RED = (180, 35, 24)
PURPLE = (107, 33, 168)
AMBER = (154, 91, 0)
BLUE = (20, 71, 166)
TEAL = (14, 107, 122)
GREEN = (30, 107, 52)
INK = (17, 17, 17)
GRAY = (90, 90, 90)
PANEL = (255, 255, 255)
BORDER = (216, 210, 192)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_headline(draw, text, fnt_path, size, max_w, max_lines, x, y, fill):
    """Shrink headline size until it wraps into max_lines; draw it."""
    while size >= 20:
        fnt = font(fnt_path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            leading = int(size * 1.12)
            return draw_lines(draw, lines, x, y, fnt, fill, leading)
        size -= 2
    fnt = font(fnt_path, 20)
    lines = wrap(draw, text, fnt, max_w)[:max_lines]
    return draw_lines(draw, lines, x, y, fnt, fill, int(20 * 1.12))


def panel(draw, x0, y0, x1, y1, accent, radius=10):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=PANEL,
                           outline=BORDER, width=2)
    # top accent bar: rounded top, square bottom
    draw.rounded_rectangle([x0, y0, x1, y0 + 18], radius=radius, fill=accent)
    draw.rectangle([x0, y0 + 9, x1, y0 + 18], fill=accent)


def globe(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r],
                 outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
             fill=color, width=3)


def star(draw, cx, cy, r, color):
    import math
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    draw.polygon(pts, outline=color, width=4)


def leaf(draw, cx, cy, r, color):
    import math
    # diagonal leaf: pointed at both ends, wide in the middle
    ux, uy = 0.7071, -0.7071   # along the leaf
    vx, vy = 0.7071, 0.7071    # across the leaf
    pts = []
    for i in range(13):
        t = i / 12
        along = (t - 0.5) * 2 * r
        wide = math.sin(math.pi * t) * r * 0.55
        pts.append((cx + ux * along + vx * wide,
                    cy + uy * along + vy * wide))
    for i in range(12, -1, -1):
        t = i / 12
        along = (t - 0.5) * 2 * r
        wide = -math.sin(math.pi * t) * r * 0.55
        pts.append((cx + ux * along + vx * wide,
                    cy + uy * along + vy * wide))
    draw.polygon(pts, outline=color, width=4)
    draw.line([cx - ux * r * 0.8, cy - uy * r * 0.8,
               cx + ux * r * 0.8, cy + uy * r * 0.8], fill=color, width=3)


def chart(draw, cx, cy, r, color):
    bw = r // 2
    base = cy + r
    heights = [r * 0.5, r * 0.9, r * 1.3]
    xs = [cx - r - bw // 2, cx - bw // 2, cx + r - bw // 2]
    for x, h in zip(xs, heights):
        draw.rectangle([x, base - h, x + bw, base], fill=color)


def burst(draw, cx, cy, r, color):
    import math
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, outline=color, width=3)


def flame(draw, cx, cy, r, color):
    draw.ellipse([cx - r * 0.7, cy - r * 0.2, cx + r * 0.7, cy + r],
                 fill=color)
    draw.polygon([(cx, cy - r * 1.2), (cx - r * 0.55, cy + r * 0.2),
                  (cx + r * 0.55, cy + r * 0.2)], fill=color)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ---------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    mast = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 18), title, font=mast, fill=(255, 255, 255))
    sub = font(SANS_B, 21)
    subline = "SUNDAY 22 NOVEMBER 2026  ·  SIX STORIES, ONE IMAGE"
    sw = d.textlength(subline, font=sub)
    d.text(((W - sw) / 2, 82), subline, font=sub, fill=GOLD)

    mx = 28            # outer margin
    gap = 16
    col_w = (W - 2 * mx - 2 * gap) // 3   # 309

    # ---- lead panel -------------------------------------------------
    ly0, ly1 = 140, 396
    panel(d, mx, ly0, W - mx, ly1, RED)
    kx, ky = mx + 24, ly0 + 34
    kick = font(SANS_B, 20)
    d.text((kx, ky), "SHENZHEN  ·  TRILATERAL SUMMIT", font=kick, fill=RED)
    globe(d, W - mx - 62, ly0 + 66, 34, RED)
    hy = fit_headline(d, "Three powers agree to talk nuclear risks",
                      SERIF_B, 50, W - 2 * mx - 48 - 96, 2, kx, ky + 34, INK)
    summ = font(SANS, 25)
    lead_text = ("Trump, Xi and Putin close their first trilateral summit "
                 "with a deal to open nuclear-risk dialogue. US envoys now "
                 "head to Moscow and Dublin.")
    lines = wrap(d, lead_text, summ, W - 2 * mx - 48)
    draw_lines(d, lines, kx, hy + 6, summ, (40, 40, 40), 34)

    # ---- row 2: two medium panels -----------------------------------
    ry0, ry1 = 412, 648
    mid_w = (W - 2 * mx - gap) // 2   # 470
    # left: Mexico
    panel(d, mx, ry0, mx + mid_w, ry1, PURPLE)
    px, py = mx + 20, ry0 + 32
    d.text((px, py), "MEXICO  ·  SINALOA", font=kick, fill=PURPLE)
    star(d, mx + mid_w - 52, ry0 + 46, 26, PURPLE)
    hy = fit_headline(d, "'El Chapo Isidro' captured", SERIF_B, 38,
                      mid_w - 40 - 72, 2, px, py + 32, INK)
    med = font(SANS, 22)
    t = ("Special forces seize FBI Top 10 fugitive Fausto Isidro Meza "
         "Flores in Guasave. Eleven dead as cartel violence flares.")
    lines = wrap(d, t, med, mid_w - 40)
    draw_lines(d, lines, px, hy + 4, med, (40, 40, 40), 29)
    # right: COP31
    rx0 = mx + mid_w + gap
    panel(d, rx0, ry0, W - mx, ry1, AMBER)
    px, py = rx0 + 20, ry0 + 32
    d.text((px, py), "ANTALYA  ·  COP31", font=kick, fill=AMBER)
    leaf(d, rx0 + mid_w - 52, ry0 + 46, 26, AMBER)
    hy = fit_headline(d, "Climate talks into day two of overtime", SERIF_B,
                      38, mid_w - 40 - 72, 2, px, py + 32, INK)
    t = ("A fossil-fuel deadlock drags COP31 past its Friday deadline. "
         "President Kurum offers a last-minute text.")
    lines = wrap(d, t, med, mid_w - 40)
    draw_lines(d, lines, px, hy + 4, med, (40, 40, 40), 29)

    # ---- row 3: three small panels ----------------------------------
    sy0, sy1 = 664, 912
    icons = [chart, burst, flame]
    colors = [BLUE, TEAL, GREEN]
    kickers = ["NEW YORK  ·  MARKETS", "UKRAINE  ·  KRYVYI RIH",
               "GULF  ·  HORMUZ"]
    heads = ["Stocks slide into correction",
             "Kryvyi Rih hit by missile",
             "Iran strikes Bahrain"]
    texts = [
        "An AI and chip sell-off drags the Dow and the S&P 500 into "
        "correction.",
        "A Russian strike kills two in Zelensky's hometown; Ukraine hit "
        "a Russian ship in reply.",
        "Tehran hits an industrial site in Bahrain; a tanker burns in "
        "the Strait as oil holds near $90.",
    ]
    small = font(SANS, 19)
    for i in range(3):
        x0 = mx + i * (col_w + gap)
        x1 = x0 + col_w
        panel(d, x0, sy0, x1, sy1, colors[i])
        px, py = x0 + 18, sy0 + 30
        d.text((px, py), kickers[i], font=font(SANS_B, 17), fill=colors[i])
        icons[i](d, x1 - 44, sy0 + 44, 20, colors[i])
        hy = fit_headline(d, heads[i], SERIF_B, 32, col_w - 36, 2,
                          px, py + 28, INK)
        lines = wrap(d, texts[i], small, col_w - 36)
        draw_lines(d, lines, px, hy + 2, small, (40, 40, 40), 26)

    # ---- ALSO ticker ------------------------------------------------
    ay = 928
    also = font(SANS_B, 20)
    also_text = ("ALSO:  AI “helps prove” the Riemann hypothesis, Anthropic "
                 "researcher says  ·  151 robots dance into the Guinness "
                 "record in Shenzhen")
    lines = wrap(d, also_text, also, W - 2 * mx)
    draw_lines(d, lines, mx, ay, also, INK, 26)

    # ---- sources footer ---------------------------------------------
    src = font(SANS, 17)
    src_text = "Sources: CNN, AP, Reuters, One Turn, Inshorts — 22 Nov 2026"
    d.text((mx, 992), src_text, font=src, fill=GRAY)

    img.save("entry.png", "PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
