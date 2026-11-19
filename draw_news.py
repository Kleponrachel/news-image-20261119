#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a dense newspaper front page that
sums up world news of Thursday 19 November 2026.

Run:  python3 draw_news.py
Out:  entry.png  (1024x1024, well under the 1 MiB gate)

Layout: masthead + big date, 3 lead stories, a world map with 16 hotspots,
a count bar (stories by region, seven regions), a "day in numbers" strip,
and 45 more stories in brief -- 48 stories from seven regions.

The coastline data (coast.txt) is a simplified public-domain world outline
(Natural Earth data, decimated to 88 polygons / 649 points); this script
renders it. The map is drawn by this code, not copied as artwork.

Every story was checked against live news on 19 Nov 2026 (NDTV world
live blog, Horizon daily brief, One Turn daily edition, FeedCast daily
brief, Japan Times, Manila Times, Le Monde, BusinessWorld, Nikkei Asia,
PYMNTS, Moneyta). Leads:
  1. Trump, Xi and Putin hold the first-ever trilateral summit in
     Shenzhen; Ukraine dominates the talks.
  2. Anthropic debuts on Nasdaq as ANT at $83 a share; $81.3B raised,
     the largest IPO ever, topping SpaceX's $75B.
  3. Grand Theft Auto VI launches worldwide to a 99 on Metacritic;
     2.3 million watch on Twitch.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
OUT = os.path.join(HERE, "entry.png")

PAPER = (250, 247, 240)
INK = (20, 33, 61)
RED = (169, 22, 33)
GREY = (90, 92, 96)
LIGHT = (214, 210, 200)
WHITE = (255, 255, 255)
LAND = (196, 198, 190)
LAND_EDGE = (150, 152, 144)
SEA = (233, 236, 232)
CHIP = (238, 235, 228)
CHIP_EDGE = (200, 196, 186)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_NAME = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)

LEADS = [
    {
        "kicker": "SUMMIT IN SHENZHEN",
        "head": "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
        "body": "First-ever trilateral summit on the APEC sidelines; "
                "Ukraine tops the agenda.",
        "color": (27, 58, 92),
    },
    {
        "kicker": "RECORD IPO",
        "head": "ANTHROPIC DEBUTS AT $83 IN RECORD $81.3B IPO",
        "body": "Nasdaq listing as ANT values the AI firm near $1.5T; "
                "tops SpaceX's $75B record.",
        "color": (163, 22, 33),
    },
    {
        "kicker": "GTA VI DAY",
        "head": "GTA VI LAUNCHES TO A 99 ON METACRITIC",
        "body": "Vice City opens worldwide at midnight; 2.3M watch "
                "on Twitch as Take-Two jumps.",
        "color": (15, 82, 87),
    },
]

# (lon, lat, label, dx, dy, big) -- hotspots marked on the map.
DOTS = [
    (114.1, 22.5, "Shenzhen", 8, -8, True),
    (-74.0, 40.7, "New York", 8, -8, True),
    (-80.2, 25.8, "Miami", 8, -8, True),
    (36.5, 45.3, "Kerch", 8, -20, True),
    (56.3, 26.9, "Hormuz", 8, -8, False),
    (47.5, 29.4, "Kuwait", 8, 14, False),
    (34.5, 31.5, "Gaza", 8, -4, False),
    (4.3, 52.1, "The Hague", 8, -8, False),
    (90.4, 23.8, "Dhaka", 8, -4, False),
    (30.7, 36.9, "Antalya", 8, -12, False),
    (130.7, 32.8, "Kumamoto", 8, -4, False),
    (127.0, 37.5, "Seoul", 8, -8, False),
    (121.0, 14.6, "Manila", 8, -4, False),
    (39.0, 14.0, "Eritrea", -58, 6, False),
    (-17.4, 14.7, "Dakar", 8, -4, False),
    (147.3, -42.9, "Hobart", 8, -4, False),
]

# stories by region (7 regions) -- must sum to 48 (3 leads + 45 briefs).
# North America 9, South America 2, Europe 14, Africa 3,
# Middle East 7, Asia 10, Oceania 3.
REGION_COUNTS = [
    ("N. AMERICA", 9),
    ("S. AMERICA", 2),
    ("EUROPE", 14),
    ("AFRICA", 3),
    ("M. EAST", 7),
    ("ASIA", 10),
    ("OCEANIA", 3),
]

# (big number, label) -- the day in numbers.
NUMBERS = [
    ("$81.3B", "Anthropic IPO record"),
    ("99", "GTA VI Metacritic"),
    ("$190.4M", "Van Gogh record"),
    ("4.7%", "global inflation"),
    ("28", "Bangladesh districts"),
    ("$89.59", "Brent crude"),
]

BRIEF = [
    # column 1 -- conflict, disaster, security
    "Ukraine hits Kerch Bridge a third time",
    "Iran attacks Gulf states after Qeshm",
    "Three tankers burn after Hormuz mines",
    "Israel ground op in central Gaza",
    "Netanyahu urges Trump to strike Iran",
    "Kuwait repels first Iran attack in 2 mo",
    "Ethiopia, Eritrea mass troops at border",
    "M5.7 quake jolts Kumamoto, Japan",
    "N. Korea expands uranium enrichment",
    "Russian arrested for spying on Palantir",
    "Houthi rocket debris hits Riyadh tower",
    "Fiji declares disaster over drought",
    "Indonesia fires burn 3M hectares",
    "Haiti pastor guilty in Moise murder",
    "IEA: Hormuz crisis tops energy threats",
    # column 2 -- politics, diplomacy, economy
    "Trump meets Putin 40 min; Ukraine leads",
    "EU proposes 45bn euro Ukraine loan",
    "US, Venezuela sign defense pact",
    "Hegseth lands in Colombia after Caracas",
    "Jeffries to be first Black House Speaker",
    "Trump floats selling Blackwell to China",
    "COP31 ministers try to unblock talks",
    "IMF: global debt nears 100% of GDP",
    "UK energy bills up 443 pounds a year",
    "Senegal ruling party splits from Faye",
    "Myanmar leader reconsiders ASEAN ties",
    "Trump, Marcos hail alliance, trade ties",
    "Spain snap vote may stifle economy",
    "MEPs accuse China over Taiwan threats",
    "Peltola: Alaska voters want price relief",
    # column 3 -- tech, economy, culture, sport, health
    "Illinois man indicted over temple attack",
    "France jails 3 women for joining ISIS",
    "Chelsea beat PSG 1-0 in women's UCL",
    "Man City beat Hacken 2-0 in women's UCL",
    "Alcaraz beats Medvedev at ATP Finals",
    "Wattimena beats Littler in darts",
    "Pochettino starts as Man Utd manager",
    "Leicester City ends BC Game sponsorship",
    "Van Gogh sells for $190.4M, a record",
    "Kenya milk shortage amid drought",
    "S. Korea exports pass $1 trillion",
    "S. Korea exam under strict cheating curbs",
    "India police kill rebel leader in Kashmir",
    "England win ODI series in Australia",
    "Bancroft: whole team knew sandpaper plot",
]


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def load_coast():
    polys = []
    with open(os.path.join(HERE, "coast.txt")) as fh:
        for line in fh:
            pts = []
            for tok in line.split():
                lon, lat = tok.split(",")
                pts.append((float(lon), float(lat)))
            if len(pts) >= 4:
                polys.append(pts)
    return polys


def project(lon, lat, box):
    """Equirectangular projection into box (x0, y0, x1, y1).
    Longitude -170..190, latitude -56..84 (Antarctica cut)."""
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (84.0 - lat) / 140.0 * (y1 - y0)
    return (x, y)


def draw_map(d, box):
    d.rectangle(box, fill=SEA)
    for poly in load_coast():
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # faint graticule
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 0, box)
        d.line([x, box[1], x, box[3]], fill=(220, 223, 219), width=1)
    for lat in (-30, 0, 30, 60):
        _, y = project(0, lat, box)
        d.line([box[0], y, box[2], y], fill=(220, 223, 219), width=1)
    # ocean labels
    fo = F_REG(13)
    for txt, lon, lat in (("PACIFIC", -150, -32), ("ATLANTIC", -30, -28),
                          ("INDIAN", 85, -38)):
        x, y = project(lon, lat, box)
        d.text((x, y), txt, font=fo, fill=(150, 154, 150))
    # hotspots
    fd = F_BOLD(12)
    for lon, lat, label, dx, dy, big in DOTS:
        x, y = project(lon, lat, box)
        r = 7 if big else 5
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED,
                  outline=WHITE, width=2)
        d.text((x + dx, y + dy), label, font=fd, fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 10], fill=RED)
    name = "THE WORLD IN ONE DAY"
    f = F_NAME(52)
    d.text(((W - d.textlength(name, font=f)) / 2, 20), name, font=f, fill=INK)
    sub = "48 stories from seven regions, in one picture"
    fs = F_REG(18)
    d.text(((W - d.textlength(sub, font=fs)) / 2, 80), sub, font=fs, fill=GREY)
    d.rectangle([0, 104, W, 156], fill=RED)
    date = "THURSDAY  19  NOVEMBER  2026"
    fd = F_BOLD(36)
    d.text(((W - d.textlength(date, font=fd)) / 2, 112), date, font=fd,
           fill=WHITE)
    d.line([0, 162, W, 162], fill=INK, width=2)

    # --- leads ---------------------------------------------------------
    col_w, gap = 304, 32
    x0 = 24
    for i, s in enumerate(LEADS):
        x = x0 + i * (col_w + gap)
        d.rectangle([x, 172, x + col_w, 176], fill=s["color"])
        fk, fh, fb = F_BOLD(14), F_BOLD(19), F_REG(14)
        d.text((x, 180), s["kicker"], font=fk, fill=RED)
        hy = 198
        for line in wrap(d, s["head"], fh, col_w):
            d.text((x, hy), line, font=fh, fill=INK)
            hy += 23
        by = hy + 2
        for line in wrap(d, s["body"], fb, col_w):
            d.text((x, by), line, font=fb, fill=(52, 54, 60))
            by += 18
    d.line([0, 290, W, 290], fill=LIGHT, width=1)

    # --- map -----------------------------------------------------------
    draw_map(d, (24, 298, 1000, 470))

    # --- count bar: stories by region ----------------------------------
    d.text((24, 478), "STORIES BY REGION", font=F_BOLD(13), fill=INK)
    total = sum(n for _, n in REGION_COUNTS)
    d.text((W - 24 - d.textlength("48 IN ALL", font=F_BOLD(13)), 478),
           "48 IN ALL", font=F_BOLD(13), fill=RED)
    chip_w, chip_gap = 132, 8
    cx = 24
    cy = 498
    for name_r, n in REGION_COUNTS:
        d.rectangle([cx, cy, cx + chip_w, cy + 28], fill=CHIP,
                    outline=CHIP_EDGE, width=1)
        d.rectangle([cx, cy, cx + chip_w, cy + 4], fill=RED)
        fr = F_BOLD(11)
        d.text((cx + 8, cy + 8), name_r, font=fr, fill=GREY)
        fn = F_BOLD(16)
        d.text((cx + chip_w - 8 - d.textlength(str(n), font=fn), cy + 7),
               str(n), font=fn, fill=INK)
        cx += chip_w + chip_gap

    # --- the day in numbers --------------------------------------------
    d.text((24, 536), "THE DAY IN NUMBERS", font=F_BOLD(13), fill=INK)
    nw = (W - 48) // len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        x = 24 + i * nw
        fn = F_BOLD(20)
        d.text((x, 554), num, font=fn, fill=RED)
        fl = F_REG(12)
        d.text((x, 578), label, font=fl, fill=(52, 54, 60))

    # --- the day in brief ----------------------------------------------
    d.rectangle([0, 600, W, 626], fill=INK)
    fb2 = F_BOLD(16)
    d.text((24, 606), "THE DAY IN BRIEF  \u2014  45 MORE STORIES",
           font=fb2, fill=WHITE)
    f_item = F_REG(14)
    for col in range(3):
        x = 24 + col * (col_w + gap)
        for row in range(15):
            item = BRIEF[col * 15 + row]
            y = 634 + row * 22
            d.rectangle([x, y + 4, x + 7, y + 11], fill=RED)
            d.text((x + 12, y), item, font=f_item, fill=(32, 34, 40))

    # --- footer --------------------------------------------------------
    d.line([0, 972, W, 972], fill=INK, width=2)
    foot = "Every story above was reported on Thursday 19 November 2026."
    ff = F_REG(16)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 982), foot, font=ff,
           fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {img.size}, {size} bytes ({size / 1048576:.2f} MiB)")
    # sanity: story count
    print(f"stories: {len(LEADS)} leads + {len(BRIEF)} briefs = "
          f"{len(LEADS) + len(BRIEF)}; regions sum to {total}; "
          f"hotspots: {len(DOTS)}")


if __name__ == "__main__":
    main()
