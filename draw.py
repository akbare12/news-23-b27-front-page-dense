#!/usr/bin/env python3
"""news-23 b27 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
Deterministic: no randomness, no timestamps. Output: entry.png 1024x1024.
Scenes are drawn illustrations, not photographs.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """fnt is an ImageFont object."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def chip(draw, x, y, label, fill):
    f = font(SANS_B, 10)
    w = int(draw.textlength(label, font=f)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    draw.text((x + 6, y + 2), label, font=f, fill="white")
    return w


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 56], fill="#111111")
    text(d, (14, 8), "THE WORLD TODAY", font(SERIF_B, 40), "#f5f0e6")
    text(d, (1010, 20), "MONDAY  23 NOVEMBER 2026", font(SANS_B, 17), "#f2c14e", anchor="ra")

    # ---------- kicker ----------
    text(d, (14, 60), "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
         font(SANS_B, 13), "#b3001b")

    # ---------- number strip (2 rows x 5) ----------
    nums = [
        ("-3.3%", "KOSPI", "#b3001b"), ("5.3", "US-CHINA POWER GAP", "#1a3a6b"),
        ("11,762", "EBOLA CASES, DRC", "#5a6b00"), ("10T won", "SEOUL STABILISATION FUND", "#7a4a00"),
        ("2%", "BILLIONAIRE TAX IN PARIS", "#7a007a"),
        ("$450M", "SKUBAL DEAL", "#7a007a"), ("165", "RUSSIAN MISSILES IN A WEEK", "#b3001b"),
        ("12,000", "CLEARED IN MANCHESTER", "#0057a8"), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", "#7a4a00"),
        ("$107.3B", "ANTHROPIC IPO — LARGEST EVER", "#b3001b"),
    ]
    for i, (num, lab, col) in enumerate(nums):
        row, c = divmod(i, 5)
        x = 14 + c * 202
        y = 76 + row * 31
        text(d, (x, y), num, font(SANS_B, 20), col)
        text(d, (x, y + 20), lab, font(SANS_B, 9), "#333333")

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", 7, "#0f766e"), ("AMERICAS 8", 8, "#1a3a6b"),
               ("MIDDLE EAST 6", 6, "#8a6d00"), ("EUROPE 5", 5, "#6b4fa1"),
               ("AFRICA 3", 3, "#7a4a00"), ("WORLD 2", 2, "#555555")]
    total = 31
    x = 8
    bar_w = 1008
    for name, n, col in regions:
        w = int(bar_w * n / total)
        d.rectangle([x, 142, x + w - 1, 162], fill=col)
        text(d, (x + 6, 146), name, font(SANS_B, 11), "white")
        x += w

    # ---------- UTC strip ----------
    d.rectangle([0, 164, W, 178], fill="#0b1e3a")
    text(d, (10, 167), "THE DAY IN UTC", font(SANS_B, 10), "#f2c14e")
    text(d, (120, 167), "~00:00 Kospi dives   ·   ~06:30 Guterres opens   ·   ~09:00 Power Index   ·   ~12:00 Paris 2% tax   ·   ~15:00 Kyiv missiles   ·   ~18:00 Anthropic $97.17",
         font(SANS, 10), "#dfe6f2")
    text(d, (1014, 167), "~ APPROX", font(SANS, 9), "#9fb2cc", anchor="ra")

    # ---------- hero panels ----------
    HX, HY, HW, HH = 8, 180, 330, 122
    # --- hero 1: Kospi skyline + chart ---
    x0 = HX
    d.rectangle([x0, HY, x0 + HW, HY + HH], fill="#0b1e3a")
    # skyline: buildings rise from a fixed base (just above the black bar)
    base_y = HY + HH - 20
    blds = [(0, 58, 26), (28, 44, 24), (54, 66, 30), (86, 38, 22),
            (110, 60, 28), (140, 48, 24), (166, 70, 30), (192, 42, 22),
            (216, 62, 28), (246, 50, 24), (272, 68, 30), (304, 56, 26)]
    for bx, by, bw in blds:
        d.rectangle([x0 + bx, HY + by, x0 + bx + bw, base_y], fill="#16345c")
        for wy in range(HY + by + 6, base_y - 4, 10):
            for wx in range(x0 + bx + 4, x0 + bx + bw - 3, 9):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill="#f2c14e")
    # big -3.3% top-left, chart line BELOW it
    text(d, (x0 + 8, HY + 6), "-3.3%", font(SANS_B, 30), "#ff5a4e")
    pts = [(x0 + 14 + i * 30, HY + 52 + i * 4) for i in range(11)]
    d.line(pts, fill="#ff5a4e", width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill="#ffd23e")
    d.rectangle([x0, HY + HH - 20, x0 + HW, HY + HH], fill="black")
    text(d, (x0 + 8, HY + HH - 17), "KOSPI  4,708.54   ·   -161 PTS", font(SANS_B, 12), "white")

    # --- hero 2: Guterres ---
    x0 = HX + 336
    d.rectangle([x0, HY, x0 + HW, HY + HH], fill="#0f766e")
    text(d, (x0 + 10, HY + 6), "150 DELEGATES", font(SANS_B, 27), "#ffd23e")
    text(d, (x0 + 10, HY + 36), "BACK A RISK", font(SANS_B, 27), "white")
    text(d, (x0 + 10, HY + 66), "FRAMEWORK", font(SANS_B, 27), "white")
    # small globe bottom-right, clear of text
    gx, gy, gr = x0 + HW - 34, HY + HH - 42, 17
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill="#bfe3dd", outline="#0b4f49", width=2)
    d.ellipse([gx - 6, gy - 9, gx + 2, gy - 1], fill="#2e9e8f")
    d.ellipse([gx - 2, gy + 3, gx + 8, gy + 10], fill="#2e9e8f")
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill="#0b4f49", width=2)
    # flags row bottom-right, below globe
    for i, col in enumerate(["#1a3a6b", "#b3001b", "#f2c14e", "#0f766e"]):
        fx = x0 + HW - 92 + i * 22
        d.rectangle([fx, HY + HH - 14, fx + 16, HY + HH - 4], fill=col, outline="white")
    d.rectangle([x0, HY + HH - 20, x0 + HW, HY + HH], fill="black")
    text(d, (x0 + 8, HY + HH - 17), "UN  ·  BRIDGETOWN", font(SANS_B, 12), "white")

    # --- hero 3: Asia Power Index bars ---
    x0 = HX + 672
    d.rectangle([x0, HY, x0 + HW, HY + HH], fill="#f4f1e8")
    text(d, (x0 + 10, HY + 6), "NARROWEST SINCE 2018", font(SANS_B, 12), "#333333")
    text(d, (x0 + HW - 10, HY + 6), "GAP 5.3", font(SANS_B, 12), "#8a6d00", anchor="ra")
    bars = [("78.9", 78.9, "#1a3a6b", "US"), ("73.6", 73.6, "#b3001b", "CHINA"), ("40.5", 40.5, "#c9930a", "INDIA")]
    base = HY + HH - 40
    for i, (val, v, col, lab) in enumerate(bars):
        bx = x0 + 30 + i * 104
        bh = int(v * 0.55)
        d.rectangle([bx, base - bh, bx + 64, base], fill=col)
        text(d, (bx + 32, base - bh - 17), val, font(SANS_B, 15), "#111111", anchor="ma")
        text(d, (bx + 32, base + 3), lab, font(SANS_B, 11), "#111111", anchor="ma")
    d.rectangle([x0, HY + HH - 20, x0 + HW, HY + HH], fill="black")
    text(d, (x0 + 8, HY + HH - 17), "ASIA POWER INDEX 2026", font(SANS_B, 12), "white")

    # ---------- hero headlines ----------
    heroes = [
        ("1", "AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.",
         "KOREA EXCHANGE"),
        ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
         "UNITED NATIONS"),
        ("3", "US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE"),
    ]
    for i, (num, head, body, src) in enumerate(heroes):
        x0 = HX + i * 336
        y = 306
        d.ellipse([x0, y, x0 + 18, y + 18], fill="#b3001b")
        text(d, (x0 + 9, y + 2), num, font(SANS_B, 12), "white", anchor="ma")
        lines = wrap(d, head, font(SANS_B, 15), 300)
        yy = y
        for ln in lines[:2]:
            text(d, (x0 + 24, yy), ln, font(SANS_B, 15), "#111111")
            yy += 18
        blines = wrap(d, body, font(SANS, 11), 318)
        yy += 2
        for ln in blines[:3]:
            text(d, (x0, yy), ln, font(SANS, 11), "#333333")
            yy += 14
        text(d, (x0, 386), src, font(SANS, 9), "#777777")
        chip(d, x0 + 252, 382, "REPORTED", "#1a3a6b")

    # ---------- MORE OF THE DAY header ----------
    text(d, (8, 398), "MORE OF THE DAY  —  10 STORIES", font(SANS_B, 14), "#111111")
    d.line([8, 416, 1016, 416], fill="#111111", width=2)

    # ---------- 10 cards ----------
    cards = [
        ("AMERICAS", "#1a3a6b", "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED", "#1a3a6b"),
        ("FBI", "#6b4fa1", "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED", "#1a3a6b"),
        ("WHITE HOUSE", "#8a6d00", "TRUMP: IRAN STRIKES MAY RESUME", "Strikes could resume in the New Year.", "Reuters", "REPORTED", "#1a3a6b"),
        ("MARKETS", "#0f766e", "US FUTURES JUMP 3%", "Holiday rally lifts Nasdaq futures 3%.", "Bloomberg", "REPORTED", "#1a3a6b"),
        ("SPORT", "#b3001b", "SKUBAL'S $450M METS DEAL", "Largest ever for a pitcher.", "AP", "REPORTED", "#1a3a6b"),
        ("SPORT", "#0f766e", "TOM JACKSON DIES AT 75", "Broncos LB turned ESPN voice dies.", "ESPN", "REPORTED", "#1a3a6b"),
        ("LEGAL", "#6b4fa1", "STATES SUE SPACEX", "Ten states challenge AI safety claims.", "AP", "REPORTED", "#1a3a6b"),
        ("TECH", "#1a3a6b", "ANTHROPIC IPO: $107.3B", "Raised at $83; debut closes $97.17.", "WSJ", "REPORTED", "#1a3a6b"),
        ("EUROPE", "#6b4fa1", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed airspace.", "AP", "CLAIM", "#b3001b"),
        ("SPACE", "#555555", "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite built to carry a nuke.", "Reuters", "CLAIM", "#b3001b"),
    ]
    for i, (cat, ccol, head, body, src, tag, tcol) in enumerate(cards):
        row, c = divmod(i, 5)
        x0 = 8 + c * 202
        y0 = 422 + row * 92
        d.rectangle([x0, y0, x0 + 198, y0 + 88], outline="#bbbbbb")
        d.rectangle([x0, y0, x0 + 198, y0 + 16], fill=ccol)
        text(d, (x0 + 6, y0 + 2), cat, font(SANS_B, 10), "white")
        text(d, (x0 + 192, y0 + 2), str(4 + i), font(SANS_B, 10), "white", anchor="ra")
        hlines = wrap(d, head, font(SANS_B, 12), 186)
        yy = y0 + 20
        for ln in hlines[:2]:
            text(d, (x0 + 6, yy), ln, font(SANS_B, 12), "#111111")
            yy += 15
        blines = wrap(d, body, font(SANS, 10), 186)
        for ln in blines[:1]:
            text(d, (x0 + 6, yy), ln, font(SANS, 10), "#444444")
            yy += 13
        text(d, (x0 + 6, y0 + 72), src, font(SANS, 9), "#777777")
        chip(d, x0 + 198 - 62, y0 + 69, tag, tcol)

    # ---------- map + ALSO header ----------
    text(d, (8, 612), "WHERE IT HAPPENED", font(SANS_B, 14), "#111111")
    text(d, (420, 612), "ALSO ON MONDAY", font(SANS_B, 14), "#111111")
    d.line([8, 630, 1016, 630], fill="#111111", width=2)

    # ---------- map ----------
    mx, my, mw, mh = 8, 636, 396, 178
    d.rectangle([mx, my, mx + mw, my + mh], fill="#dcebf5")
    for gx in range(mx, mx + mw, 22):
        d.line([gx, my, gx, my + mh], fill="#c2d8e8")
    for gy in range(my, my + mh, 22):
        d.line([mx, gy, mx + mw, gy], fill="#c2d8e8")
    # stylised continents (green blobs)
    d.polygon([(mx + 18, my + 30), (mx + 130, my + 18), (mx + 165, my + 52), (mx + 150, my + 96),
               (mx + 105, my + 118), (mx + 60, my + 108), (mx + 22, my + 78)], fill="#8fbf6f")  # N America
    d.polygon([(mx + 78, my + 122), (mx + 128, my + 118), (mx + 138, my + 152), (mx + 108, my + 172),
               (mx + 82, my + 158)], fill="#8fbf6f")  # S America
    d.polygon([(mx + 185, my + 28), (mx + 235, my + 18), (mx + 252, my + 42), (mx + 228, my + 66),
               (mx + 192, my + 60)], fill="#8fbf6f")  # Europe
    d.polygon([(mx + 200, my + 74), (mx + 252, my + 70), (mx + 262, my + 112), (mx + 232, my + 140),
               (mx + 204, my + 118)], fill="#8fbf6f")  # Africa
    d.polygon([(mx + 258, my + 22), (mx + 380, my + 14), (mx + 390, my + 60), (mx + 350, my + 96),
               (mx + 292, my + 88), (mx + 262, my + 52)], fill="#8fbf6f")  # Asia
    d.polygon([(mx + 330, my + 138), (mx + 372, my + 132), (mx + 380, my + 156), (mx + 344, my + 164)],
              fill="#8fbf6f")  # Australia
    # pins 1-13, spread to avoid overlap (stylised positions)
    pins = [(330, 34), (112, 148), (300, 30), (128, 66), (150, 58), (238, 58),
            (96, 74), (44, 82), (78, 96), (104, 92), (222, 36), (240, 34), (268, 26)]
    for i, (px, py) in enumerate(pins, start=1):
        d.ellipse([mx + px - 8, my + py - 8, mx + px + 8, my + py + 8], fill="#b3001b", outline="white", width=1)
        text(d, (mx + px, my + py - 6), str(i), font(SANS_B, 10), "white", anchor="ma")
    text(d, (8, 818), "Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing · 4 Washington · 5 New York · 6 Tehran · 7 Chicago · 8 San Francisco",
         font(SANS, 9), "#555555")
    text(d, (8, 831), "9 Denver · 10 Austin · 11 Warsaw · 12 Kyiv · 13 Moscow", font(SANS, 9), "#555555")

    # ---------- ALSO list ----------
    also = [
        "Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
        "Zelenskyy: 165 missiles in a week", "COP31: the day after pact rejected",
        "Benghazi: UN demands port probe", "Israel unity talks resume",
        "Gaza: two killed in Israeli strike", "West Bank settler attacks",
        "Iran war: no deal in sight",
        "Lebanon seizes 264 kg explosives", "Bahrain: strike hits plant, 2 hurt",
        "Sudan: defences down drones", "DRC: fighting traps Ebola teams",
        "Bangladesh: Hasina jailed if she returns", "Seoul minister quits in exam row",
        "SK Telecom -7.3% as hype cools", "China eases margin rules",
        "Seoul readies 10T-won fund",
    ]
    for i, item in enumerate(also):
        col, row = divmod(i, 9)
        x0 = 420 + col * 300
        y0 = 638 + row * 20
        text(d, (x0, y0), f"{14 + i}.  {item}", font(SANS, 11), "#222222")

    # ---------- DATE CHECK ----------
    d.rectangle([8, 850, 1016, 928], outline="#b3001b", width=2)
    text(d, (16, 856), "DATE CHECK", font(SANS_B, 14), "#b3001b")
    text(d, (1008, 856), "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY",
         font(SANS_B, 10), "#111111", anchor="ra")
    text(d, (16, 878), "LEFT OUT — NOT 23 NOV: Democrats reach 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) ·",
         font(SANS, 11), "#111111")
    text(d, (16, 893), "EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)",
         font(SANS, 11), "#111111")
    text(d, (16, 910), "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
         font(SANS, 11), "#111111")

    # ---------- sources / legend ----------
    text(d, (8, 936), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
         font(SANS, 10), "#555555")
    text(d, (8, 952), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing",
         font(SANS, 10), "#555555")

    # ---------- bottom bar ----------
    d.rectangle([0, 968, W, H], fill="#111111")
    text(d, (512, 982), "Scenes are drawn illustrations, not photographs.   ·   THE WORLD TODAY — Monday 23 November 2026   ·   31 stories   ·   6 regions",
         font(SANS_B, 12), "#f2c14e", anchor="ma")

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
