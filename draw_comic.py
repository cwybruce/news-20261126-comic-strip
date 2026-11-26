#!/usr/bin/env python3
"""news-image-20261126: The day in four frames.

A newspaper comic strip: four flat-colour panels in a 2x2 grid, each
illustrating one of the verified top stories of Thursday 26 November 2026,
under a masthead naming the day. Drawn with Pillow, fully deterministic:
fixed seed, no wall-clock, no network. Writes /output/entry.png (and a
local copy next to this file when the directory is writable).
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def panel_frame(draw, x, y, w, h, bg):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=bg, outline="#1a1a1a", width=3)


def draw_rocket(draw, cx, cy, s):
    """Simple flat rocket pointing up-right."""
    body = [(cx - 14 * s, cy + 30 * s), (cx - 14 * s, cy - 10 * s),
            (cx, cy - 34 * s), (cx + 14 * s, cy - 10 * s),
            (cx + 14 * s, cy + 30 * s)]
    draw.polygon(body, fill="#f2f2f2", outline="#1a1a1a")
    draw.polygon([(cx - 14 * s, cy - 10 * s), (cx, cy - 34 * s),
                  (cx + 14 * s, cy - 10 * s)], fill="#d43d2a")
    draw.ellipse([cx - 8 * s, cy - 14 * s, cx + 8 * s, cy + 2 * s],
                 fill="#7ec8e3", outline="#1a1a1a")
    draw.polygon([(cx - 14 * s, cy + 30 * s), (cx - 26 * s, cy + 44 * s),
                  (cx - 14 * s, cy + 40 * s)], fill="#d43d2a")
    draw.polygon([(cx + 14 * s, cy + 30 * s), (cx + 26 * s, cy + 44 * s),
                  (cx + 14 * s, cy + 40 * s)], fill="#d43d2a")
    draw.polygon([(cx - 9 * s, cy + 32 * s), (cx, cy + 58 * s),
                  (cx + 9 * s, cy + 32 * s)], fill="#f5a623")
    draw.polygon([(cx - 5 * s, cy + 32 * s), (cx, cy + 46 * s),
                  (cx + 5 * s, cy + 32 * s)], fill="#f7d154")


def draw_plane(draw, cx, cy, s, color):
    """Simple side-view jet silhouette."""
    draw.ellipse([cx - 46 * s, cy - 8 * s, cx + 46 * s, cy + 8 * s],
                 fill=color, outline="#1a1a1a")
    draw.polygon([(cx + 20 * s, cy - 6 * s), (cx + 46 * s, cy - 6 * s),
                  (cx + 30 * s, cy + 4 * s)], fill=color, outline="#1a1a1a")
    draw.polygon([(cx - 6 * s, cy - 4 * s), (cx + 6 * s, cy - 26 * s),
                  (cx + 16 * s, cy - 4 * s)], fill=color, outline="#1a1a1a")
    draw.polygon([(cx - 30 * s, cy + 4 * s), (cx - 20 * s, cy + 20 * s),
                  (cx - 10 * s, cy + 4 * s)], fill=color, outline="#1a1a1a")
    draw.ellipse([cx + 28 * s, cy - 4 * s, cx + 38 * s, cy + 4 * s],
                 fill="#bfe3f0", outline="#1a1a1a")


def draw_gavel(draw, cx, cy, s, angle_deg):
    """Gavel drawn with rotated rectangles via a small temp layer."""
    layer = Image.new("RGBA", (220, 160), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([60, 30, 160, 78], radius=12, fill="#8b5a2b",
                         outline="#1a1a1a", width=3)
    ld.rectangle([52, 30, 68, 78], fill="#e8c88a", outline="#1a1a1a", width=2)
    ld.rectangle([144, 30, 160, 78], fill="#e8c88a", outline="#1a1a1a",
                 width=2)
    ld.rounded_rectangle([100, 78, 116, 140], radius=6, fill="#6b4423",
                         outline="#1a1a1a", width=3)
    layer = layer.rotate(angle_deg, resample=Image.BICUBIC, center=(110, 80))
    return layer, (int(cx - 110), int(cy - 80))


def draw_chess_piece(draw, cx, cy, r, letter, fill, text_fill):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                 outline="#1a1a1a", width=2)
    f = font(int(r * 1.1), bold=True)
    draw.text((cx, cy), letter, font=f, fill=text_fill, anchor="mm")


def panel_space(draw, x, y, w, h):
    """Panel 1: rocket + Mercury + space station."""
    rng = random.Random(11)
    draw.rectangle([x, y, x + w, y + 190], fill="#101c3a")
    for _ in range(26):
        sx = x + rng.randint(8, w - 8)
        sy = y + rng.randint(8, 180)
        r = rng.randint(1, 3)
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill="#ffffff")
    # Mercury, top right
    mx, my, mr = x + w - 78, y + 62, 46
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill="#c9a06a",
                 outline="#1a1a1a", width=3)
    for cx, cy, cr in [(mx - 18, my - 8, 9), (mx + 12, my + 14, 7),
                       (mx + 20, my - 20, 5), (mx - 4, my + 22, 6)]:
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill="#a67c4e")
    # Space station, top left
    draw.rectangle([x + 26, y + 44, x + 66, y + 60], fill="#e8e8e8",
                   outline="#1a1a1a", width=2)
    draw.rectangle([x + 8, y + 36, x + 26, y + 68], fill="#3a6ea5",
                   outline="#1a1a1a", width=2)
    draw.rectangle([x + 66, y + 36, x + 84, y + 68], fill="#3a6ea5",
                   outline="#1a1a1a", width=2)
    draw_rocket(draw, x + w // 2 - 10, y + 128, 1.0)


def panel_airbase(draw, x, y, w, h):
    """Panel 2: air base, jets, blast and smoke."""
    draw.rectangle([x, y, x + w, y + 190], fill="#f4d58d")
    draw.ellipse([x + w - 70, y + 22, x + w - 14, y + 78], fill="#f7b733",
                 outline="#1a1a1a", width=2)
    draw.rectangle([x, y + 150, x + w, y + 190], fill="#5b5b5b")
    draw.rectangle([x, y + 150, x + w, y + 158], fill="#e8e8e8")
    for i in range(6):
        draw.rectangle([x + 20 + i * 78, y + 168, x + 52 + i * 78, y + 174],
                       fill="#f2f2f2")
    # Hangar
    draw.rectangle([x + 24, y + 108, x + 104, y + 150], fill="#8a8f98",
                   outline="#1a1a1a", width=3)
    draw.arc([x + 24, y + 66, x + 104, y + 150], 180, 360, fill="#1a1a1a",
             width=3)
    draw_plane(draw, x + 300, y + 92, 1.0, "#3a6ea5")
    draw_plane(draw, x + 330, y + 52, 0.62, "#7a8899")
    # Blast burst
    bx, by = x + 120, y + 60
    pts = []
    for i in range(12):
        ang = i * 30
        rr = 34 if i % 2 == 0 else 16
        import math
        pts.append((bx + rr * math.cos(math.radians(ang)),
                    by + rr * math.sin(math.radians(ang))))
    draw.polygon(pts, fill="#f5761f", outline="#1a1a1a")
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill="#f7d154")
    for cx, cy, cr in [(x + 170, y + 34, 14), (x + 196, y + 26, 10),
                       (x + 150, y + 22, 8)]:
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill="#9a9a9a",
                     outline="#1a1a1a", width=2)


def panel_gavel(draw, img, x, y, w, h):
    """Panel 3: courthouse gavel + factory with chimneys."""
    draw.rectangle([x, y, x + w, y + 190], fill="#eef3f7")
    # Courthouse columns, left
    for i in range(3):
        cx = x + 46 + i * 52
        draw.rectangle([cx - 14, y + 60, cx + 14, y + 150], fill="#f2f2f2",
                       outline="#1a1a1a", width=2)
        draw.rectangle([cx - 20, y + 48, cx + 20, y + 60], fill="#d8dee3",
                       outline="#1a1a1a", width=2)
    draw.polygon([(x + 16, y + 48), (x + 108, y + 14), (x + 200, y + 48)],
                 fill="#c0392b", outline="#1a1a1a")
    draw.rectangle([x + 16, y + 150, x + 200, y + 164], fill="#d8dee3",
                   outline="#1a1a1a", width=2)
    # Factory, right
    draw.rectangle([x + 250, y + 120, x + w - 24, y + 164], fill="#7a8899",
                   outline="#1a1a1a", width=3)
    draw.rectangle([x + 262, y + 66, x + 284, y + 120], fill="#5b6b7c",
                   outline="#1a1a1a", width=3)
    draw.rectangle([x + 296, y + 84, x + 316, y + 120], fill="#5b6b7c",
                   outline="#1a1a1a", width=3)
    for cx, cy, cr in [(x + 273, y + 52, 12), (x + 288, y + 38, 9),
                       (x + 306, y + 66, 10)]:
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill="#cfd8dc",
                     outline="#1a1a1a", width=2)
    draw.rectangle([x + 262, y + 132, x + 286, y + 164], fill="#f7d154",
                   outline="#1a1a1a", width=2)
    draw.rectangle([x + 298, y + 132, x + 322, y + 164], fill="#f7d154",
                   outline="#1a1a1a", width=2)
    # Gavel over the middle
    layer, pos = draw_gavel(draw, x + w // 2 + 6, y + 84, 1.0, -28)
    img.paste(layer, pos, layer)


def panel_chess(draw, x, y, w, h):
    """Panel 4: chess board, Game 2 drawn."""
    draw.rectangle([x, y, x + w, y + 190], fill="#f5efe0")
    bx, by, sq = x + (w - 192) // 2, y + 4, 24
    for r in range(8):
        for c in range(8):
            fill = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
            draw.rectangle([bx + c * sq, by + r * sq,
                            bx + (c + 1) * sq, by + (r + 1) * sq],
                           fill=fill, outline="#1a1a1a", width=1)
    # A few pieces: white king vs black king, queens and pawns
    draw_chess_piece(draw, bx + 4 * sq + 11, by + 7 * sq + 11, 9, "K",
                     "#ffffff", "#1a1a1a")
    draw_chess_piece(draw, bx + 4 * sq + 11, by + 0 * sq + 11, 9, "K",
                     "#1a1a1a", "#ffffff")
    draw_chess_piece(draw, bx + 3 * sq + 11, by + 7 * sq + 11, 9, "Q",
                     "#ffffff", "#1a1a1a")
    draw_chess_piece(draw, bx + 3 * sq + 11, by + 0 * sq + 11, 9, "Q",
                     "#1a1a1a", "#ffffff")
    draw_chess_piece(draw, bx + 2 * sq + 11, by + 6 * sq + 11, 8, "P",
                     "#ffffff", "#1a1a1a")
    draw_chess_piece(draw, bx + 5 * sq + 11, by + 1 * sq + 11, 8, "P",
                     "#1a1a1a", "#ffffff")
    draw_chess_piece(draw, bx + 1 * sq + 11, by + 0 * sq + 11, 9, "R",
                     "#1a1a1a", "#ffffff")
    draw_chess_piece(draw, bx + 6 * sq + 11, by + 7 * sq + 11, 9, "N",
                     "#ffffff", "#1a1a1a")


PANELS = [
    ("1  SPACE", "A FIRST FOR PAKISTAN",
     "Muhammad Zeeshan Ali to fly on Shenzhou-24 to Tiangong. "
     "BepiColombo reaches Mercury after eight years.", panel_space),
    ("2  WAR", "AIR BASE HIT",
     "Ukraine says it struck a Russian air base, damaging five planes. "
     "Kim Jong Un calls for wider tactical nuclear deployment.", panel_airbase),
    ("3  AMERICA", "JUDGE BLOCKS ORDER",
     "A second US judge blocks Trump's newest order curtailing birthright "
     "citizenship. US plans new tariffs on factory overcapacity.",
     None),  # gavel panel needs the image handle
    ("4  SPORT", "CHESS: GAME 2 DRAWN",
     "World Chess Championship 2026: Gukesh vs Sindarov ends in a draw "
     "in Game 2.", panel_chess),
]


def main():
    img = Image.new("RGB", (W, H), "#f7f3e8")
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.rectangle([24, 20, W - 24, 150], fill="#1a1a1a")
    draw.text((W // 2, 50), "THE DAY IN FOUR FRAMES", font=font(46, True),
              fill="#f7f3e8", anchor="mm")
    draw.text((W // 2, 102), "26 NOVEMBER 2026  •  WORLD NEWS AT A GLANCE",
              font=font(24, True), fill="#f7d154", anchor="mm")
    draw.text((W // 2, 136), "Thursday 26 November 2026", font=font(22),
              fill="#f7f3e8", anchor="mm")

    # 2x2 grid of panels
    gx, gy = 24, 164
    pw, ph, gap = 476, 372, 24
    for i, (kicker, headline, body, art) in enumerate(PANELS):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        panel_frame(draw, px, py, pw, ph, "#ffffff")
        if i == 2:
            panel_gavel(draw, img, px + 3, py + 3, pw - 6, ph - 6)
        else:
            art(draw, px + 3, py + 3, pw - 6, ph - 6)
        # Caption strip
        cy = py + 196
        draw.rectangle([px + 3, cy, px + pw - 3, py + ph - 3],
                       fill="#fdfbf4")
        draw.line([px + 3, cy, px + pw - 3, cy], fill="#1a1a1a", width=3)
        draw.text((px + 20, cy + 16), kicker, font=font(20, True),
                  fill="#c0392b")
        draw.text((px + 20, cy + 44), headline, font=font(27, True),
                  fill="#1a1a1a")
        lines = wrap(draw, body, font(21), pw - 40)
        yy = cy + 82
        for line in lines[:3]:
            draw.text((px + 20, yy), line, font=font(21), fill="#333333")
            yy += 28

    # Footer ticker
    fy = gy + 2 * ph + gap + 8
    draw.rectangle([24, fy, W - 24, fy + 44], fill="#1a1a1a")
    ticker = ("ALSO TODAY:  Cairo fire kills 30+  •  Andy Taylor, 65, dies  •  "
              "Bangladesh wage +36%")
    draw.text((W // 2, fy + 22), ticker, font=font(19, True),
              fill="#f7f3e8", anchor="mm")

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "entry.png")
    img.save(out, "PNG")
    try:
        img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "entry.png"), "PNG")
    except OSError:
        pass


if __name__ == "__main__":
    main()
