#!/usr/bin/env python3
"""Render the news-image-20261119 entry: one 1024x1024 front page summing
up Thursday 19 November 2026's world news.

Six verified stories, drawn with Pillow only (no network, no external
assets): a masthead, one hero panel, two mid panels, three lower panels,
and a footer ticker. Every string, colour and coordinate is fixed in
this file, so the output is byte-identical on every run.

Usage:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
PAPER = (247, 242, 231)
INK = (20, 24, 33)
NAVY = (18, 33, 61)
GOLD = (197, 148, 44)
WHITE = (255, 255, 255)
MUTED = (92, 96, 104)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)          # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


# (kicker, headline, body, accent, icon)
STORIES = [
    ("SHENZHEN · APEC SUMMIT",
     "Three nuclear powers, one table",
     "Trump, Xi and Putin meet for the first-ever US\u2013China\u2013Russia "
     "trilateral summit, with Ukraine, Iran and nuclear arms control on "
     "the agenda.",
     (178, 34, 34), "globe"),
    ("GAMING · VICE CITY RETURNS",
     "GTA VI is out",
     "After 13 years, Rockstar's blockbuster launches on PS5 and Xbox. "
     "$1.65B in presales, 17M copies pre-ordered, Metacritic 99.",
     (124, 58, 168), "pad"),
    ("GULF · STRAIT OF HORMUZ",
     "Iran widens the war",
     "Tehran hits Kuwait and Bahrain after US strikes on Qeshm Island. "
     "Tankers burn in the Strait; the IEA warns of the gravest threat "
     "ever to energy security.",
     (176, 92, 8), "flame"),
    ("UKRAINE · KERCH STRAIT",
     "Bridge struck a third time",
     "A third Ukrainian strike in four days halts traffic on the Crimean "
     "Bridge, collapsing a road span over the Kerch Strait.",
     (31, 94, 124), "bridge"),
    ("THE HAGUE · ICJ",
     "Myanmar guilty of genocide",
     "The ICJ rules Myanmar committed genocide against the Rohingya in "
     "2017 \u2014 the first time the court has held a state responsible.",
     (43, 110, 71), "scales"),
    ("TECH · AI BOOM",
     "Anthropic's record $81.3B IPO",
     "The Claude maker's market debut is the biggest AI listing yet, "
     "valuing the company at about $1.5 trillion.",
     (30, 80, 160), "chip"),
]

TICKER = ("ALSO: Van Gogh sells for $190.4M, an artist record  \u00b7  "
          "COP31 ministers race for a final text")
SOURCES = ("Sources: Reuters, AP, The Wall Street Journal, USA Today, "
           "Le Monde, Inshorts \u2014 19 Nov 2026")


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r, colour):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=colour,
              width=3)
    d.line([cx - r, cy, cx + r, cy], fill=colour, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=colour,
          width=3)


def draw_pad(d, cx, cy, r, colour):
    d.rounded_rectangle([cx - r, cy - r // 2, cx + r, cy + r // 2],
                        radius=r // 2, outline=colour, width=4)
    d.line([cx - r // 3, cy, cx + r // 3, cy], fill=colour, width=4)
    d.line([cx - r // 6, cy - r // 6, cx - r // 6, cy + r // 6],
           fill=colour, width=4)
    for dx, dy in ((r // 2, -r // 6), (r // 2 + 12, r // 6)):
        d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5],
                  fill=colour)


def draw_flame(d, cx, cy, r, colour):
    pts = [(cx, cy - r), (cx + r * 0.6, cy + r * 0.1), (cx + r * 0.3, cy + r),
           (cx - r * 0.3, cy + r), (cx - r * 0.6, cy + r * 0.1)]
    d.polygon(pts, fill=colour)
    d.ellipse([cx - r * 0.25, cy + r * 0.1, cx + r * 0.25, cy + r * 0.6],
              fill=(255, 214, 130))


def draw_bridge(d, cx, cy, r, colour):
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=colour, width=4)
    d.line([cx - r, cy + r // 3, cx + r, cy + r // 3], fill=colour, width=4)
    for x in (-r // 2, 0, r // 2):
        d.line([cx + x, cy - r // 2, cx + x, cy + r // 3], fill=colour,
               width=3)


def draw_scales(d, cx, cy, r, colour):
    d.line([cx, cy - r, cx, cy + r], fill=colour, width=4)
    d.line([cx - r, cy - r // 2, cx + r, cy - r // 2], fill=colour, width=4)
    for sx in (-r, r):
        d.polygon([(cx + sx - r // 3, cy - r // 2), (cx + sx + r // 3,
                    cy - r // 2), (cx + sx, cy + r // 4)], outline=colour,
                  width=3)
    d.line([cx - r // 4, cy - r, cx + r // 4, cy - r], fill=colour, width=4)


def draw_chip(d, cx, cy, r, colour):
    d.rectangle([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                outline=colour, width=4)
    d.rectangle([cx - r // 4, cy - r // 4, cx + r // 4, cy + r // 4],
                fill=colour)
    for i in (-1, 0, 1):
        d.line([cx + i * r // 3, cy - r // 2 - 10, cx + i * r // 3,
                cy - r // 2], fill=colour, width=3)
        d.line([cx + i * r // 3, cy + r // 2, cx + i * r // 3,
                cy + r // 2 + 10], fill=colour, width=3)
        d.line([cx - r // 2 - 10, cy + i * r // 3, cx - r // 2,
                cy + i * r // 3], fill=colour, width=3)
        d.line([cx + r // 2, cy + i * r // 3, cx + r // 2 + 10,
                cy + i * r // 3], fill=colour, width=3)


ICONS = {"globe": draw_globe, "pad": draw_pad, "flame": draw_flame,
         "bridge": draw_bridge, "scales": draw_scales, "chip": draw_chip}


def panel(d, box, story, headline_size, body_size, icon_r):
    x0, y0, x1, y1 = box
    kicker, headline, body, accent, icon = story
    d.rounded_rectangle(box, radius=10, fill=WHITE, outline=(210, 204, 188),
                        width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=accent)
    pad = 20
    cx, cy = x1 - pad - icon_r, y0 + pad + icon_r
    ICONS[icon](d, cx, cy, icon_r, accent)
    # Text never runs under the icon: reserve its column for every line.
    text_w = (x1 - x0) - 2 * pad - (2 * icon_r + 12)
    y = y0 + 22
    d.text((x0 + pad, y), kicker, font=SANS_B(15), fill=accent)
    y += 26
    for line in wrap(d, headline, SERIF_B(headline_size), text_w):
        d.text((x0 + pad, y), line, font=SERIF_B(headline_size), fill=INK)
        y += headline_size + 8
    y += 6
    for line in wrap(d, body, SANS(body_size), text_w):
        d.text((x0 + pad, y), line, font=SANS(body_size), fill=(52, 56, 66))
        y += body_size + 7


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 116, W, 120], fill=GOLD)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=SERIF_B(52))) / 2, 14), title,
           font=SERIF_B(52), fill=WHITE)
    sub = "THURSDAY 19 NOVEMBER 2026  \u00b7  SIX STORIES, ONE IMAGE"
    d.text(((W - d.textlength(sub, font=SANS_B(17))) / 2, 82), sub,
           font=SANS_B(17), fill=(212, 178, 94))

    # Hero: Shenzhen summit
    panel(d, (MARGIN, 134, W - MARGIN, 380), STORIES[0], 40, 20, 52)

    # Mid row: GTA VI + Iran/Hormuz
    panel(d, (MARGIN, 394, 505, 656), STORIES[1], 27, 18, 34)
    panel(d, (519, 394, W - MARGIN, 656), STORIES[2], 27, 18, 34)

    # Bottom row: Crimea Bridge, ICJ Rohingya, Anthropic IPO
    panel(d, (MARGIN, 670, 335, 938), STORIES[3], 22, 16, 22)
    panel(d, (356, 670, 668, 938), STORIES[4], 22, 16, 22)
    panel(d, (688, 670, W - MARGIN, 938), STORIES[5], 22, 16, 22)

    # Footer ticker + sources
    d.text((MARGIN, 954), TICKER, font=SANS_B(15), fill=INK)
    d.text((MARGIN, 982), SOURCES, font=SANS(13), fill=MUTED)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG",
             compress_level=9)
    return 0


if __name__ == "__main__":
    sys.exit(main())
