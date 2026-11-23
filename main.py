#!/usr/bin/env python3
"""Draw the world news of Monday 23 November 2026 as one front page.

Writes a deterministic 1024x1024 PNG to $MAKEFUN_OUTPUT_DIR/entry.png
(or /output/entry.png when the variable is unset). Standard library
plus Pillow only; no network, no clock, no randomness, so repeated
runs produce byte-identical output.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

INK = (18, 18, 18)
RED = (178, 28, 28)
PAPER = (255, 255, 255)
PANEL = (246, 243, 236)
RULE = (150, 150, 150)
FAINT = (110, 110, 110)

# Region tag colours: 9 regions.
REGION_COLORS = {
    "NORTH AMERICA": (31, 78, 121),
    "LATIN AMERICA": (46, 125, 50),
    "EUROPE": (106, 27, 154),
    "MIDDLE EAST": (183, 28, 28),
    "AFRICA": (230, 81, 0),
    "SOUTH ASIA": (0, 105, 92),
    "EAST ASIA": (194, 24, 91),
    "SOUTHEAST ASIA": (2, 119, 189),
    "OCEANIA": (93, 64, 55),
    "GLOBAL": (178, 28, 28),
}

LEAD = (
    "GLOBAL",
    "COP31 COLLAPSES WITH NO DEAL",
    "Climate talks in Türkiye end with no agreement - the first failure since "
    "Copenhagen 2009 - after the EU rejects a final text with no fossil-fuel pledge.",
)

# (region, headline, one-line summary) - 36 stories, 9 regions.
STORIES = [
    ("NORTH AMERICA", "Democrats clinch historic House majority",
     "At least 258 seats - the largest since 1992."),
    ("NORTH AMERICA", "Trump blames Democrats for Iran escalation",
     "Blames the opposition for the stock market slide."),
    ("NORTH AMERICA", "Delta glitch delays 1,000+ flights",
     "Automation failure hits Atlanta hub before Thanksgiving."),
    ("NORTH AMERICA", "Intel chief backs Trump on Putin 'friend'",
     "Calls the description 'entirely appropriate'."),
    ("NORTH AMERICA", "Nine shot at California concert",
     "One victim in critical condition after the gunfire."),
    ("NORTH AMERICA", "Nvidia spy affair deepens",
     "Trump backs ex-CEO's return amid the spy probe."),
    ("LATIN AMERICA", "Paraguay bank collapse ousts president",
     "Bank holding half the nation's accounts fails."),
    ("LATIN AMERICA", "Chile's Kast approval falls to 20%",
     "Far-right president's ratings slide after a year."),
    ("LATIN AMERICA", "Boca win Sudamericana; Paredes collapses",
     "Midfielder faints live on TV after the 2-0 final win."),
    ("EUROPE", "Russian strikes kill at least 15 in Kyiv region",
     "Fresh deaths as missile and drone attacks continue."),
    ("EUROPE", "Ukraine says it sank a Russian warship off Libya",
     "Sea drones hit the MV Angara and a Ka-27 helicopter."),
    ("EUROPE", "Russia tows Baltic ship hit by drones",
     "Finland says the damaged freighter is under tow."),
    ("EUROPE", "Poland: Russia twice tried to kill US rapper",
     "Warsaw alleges two attempts on a US artist."),
    ("EUROPE", "UK to dig £800m reservoir as droughts persist",
     "Havant Thicket scheme to secure water for the south-east."),
    ("EUROPE", "Alcaraz wins first ATP Finals title",
     "Spaniard beats world No. 1 Zverev in Turin."),
    ("MIDDLE EAST", "Trump 'inclined' to resume war on Tehran",
     "Warns of renewed conflict if no deal by New Year."),
    ("MIDDLE EAST", "Iran seeks 'clear' end to limbo with US",
     "Speaker demands a plan to end 'neither war nor peace'."),
    ("MIDDLE EAST", "Netanyahu-Eisenkot talks fail",
     "No deal on forming an Israeli government."),
    ("MIDDLE EAST", "Israel probes West Bank fires",
     "Authorities investigate blazes blamed on settlers."),
    ("AFRICA", "Sudan drone strikes hit UN building",
     "Homes also hit in the capital as the war grinds on."),
    ("AFRICA", "24 civilians killed in South Sudan attack",
     "SPLA-IO forces blamed for the assault on a village."),
    ("AFRICA", "Ebola deaths pass 5,700 in DR Congo",
     "Cases reach 11,680; Uganda tightens border controls."),
    ("AFRICA", "Somalia flags climate finance gap",
     "Pledges not reaching frontline communities, it warns."),
    ("AFRICA", "Ghana win amputee football World Cup",
     "Black Challenge beat Morocco 1-0 to take the title."),
    ("SOUTH ASIA", "400 tonnes of missile chemical seized",
     "Indonesia stops a China-to-Bangladesh shipment."),
    ("SOUTH ASIA", "2,300 Sikh pilgrims cross into Pakistan",
     "Worshippers arrive for Guru Nanak's birthday."),
    ("SOUTH ASIA", "Pakistan: India talks must be 'evidence-based'",
     "Islamabad sets its terms for dialogue on terrorism."),
    ("SOUTH ASIA", "Bangladesh unrest spreads to 28 districts",
     "About 600 arrested as protests and arson spread."),
    ("EAST ASIA", "Xi, Trump and Putin hold first trilateral talks",
     "First three-way summit; critics question the format."),
    ("EAST ASIA", "China sets 2030 elderly and childcare targets",
     "More support promised for older people and families."),
    ("EAST ASIA", "South Korea minister quits over exam chaos",
     "Education chief resigns over CSAT cheating confusion."),
    ("EAST ASIA", "Kim: North Korea seeks security, not supremacy",
     "Leader frames the nuclear-armed state's aims."),
    ("EAST ASIA", "Japan-Europe Mercury probes enter orbit",
     "BepiColombo craft reach the innermost planet."),
    ("SOUTHEAST ASIA", "Indonesia factory fire: 24 bodies found",
     "Search resumes for 34 workers still missing."),
    ("SOUTHEAST ASIA", "Thailand to ban chemical exports",
     "Bangkok acts on pollution from hazardous shipments."),
    ("OCEANIA", "COP backlash hits Australia; Pacific despairs",
     "Bowen faces calls to quit; Pacific islands despair."),
]

SOURCES = ("Sources: Reuters - AP - AFP - BBC - The Japan Times - SCMP - "
           "Xinhua - Dawn - Arab News - ABP Live - RNZ - AfricaFrontPage")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def ellipsize(draw, text, fnt, width):
    """Shorten text with an ellipsis so it fits width."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "...", font=fnt) > width:
        text = text[:-1].rstrip()
    return text + "..."


def tag(draw, x, y, label):
    """Draw a coloured region tag; returns its width."""
    fnt = font(SANS_B, 10)
    tw = draw.textlength(label, font=fnt)
    w = int(tw) + 10
    h = 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=2,
                           fill=REGION_COLORS[label])
    draw.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def draw_masthead(draw):
    draw.rectangle([MARGIN, 8, W - MARGIN, 11], fill=INK)
    title = "THE WORLD IN ONE PAGE"
    tf = font(SERIF_B, 42)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    sub = "MONDAY, 23 NOVEMBER 2026   -   37 STORIES   -   9 REGIONS"
    sf = font(SANS_B, 14)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 64), sub, font=sf, fill=RED)
    draw.rectangle([MARGIN, 84, W - MARGIN, 87], fill=INK)
    draw.rectangle([MARGIN, 89, W - MARGIN, 90], fill=INK)


def draw_lead(draw):
    x0, y0 = MARGIN, 96
    x1, y1 = W - MARGIN, 190
    draw.rectangle([x0, y0, x1, y1], fill=PANEL)
    draw.rectangle([x0, y0, x0 + 6, y1], fill=RED)
    region, headline, summary = LEAD
    tag(draw, x0 + 16, y0 + 8, region)
    hf = font(SERIF_B, 28)
    lines = wrap(draw, headline, hf, x1 - x0 - 32)[:2]
    y = y0 + 26
    for line in lines:
        draw.text((x0 + 16, y), line, font=hf, fill=INK)
        y += 32
    sf = font(SANS, 13)
    slines = wrap(draw, summary, sf, x1 - x0 - 32)[:2]
    for line in slines:
        draw.text((x0 + 16, y), line, font=sf, fill=(40, 40, 40))
        y += 17


def draw_grid(draw):
    gx0, gy0 = MARGIN, 220
    cols, rows = 3, 12
    cw = (W - 2 * MARGIN - (cols - 1) * 8) // cols
    ch = 64
    # Section header.
    hf = font(SANS_B, 12)
    draw.text((gx0, 198), "THE DAY IN BRIEF", font=hf, fill=INK)
    right = "36 MORE STORIES FROM 9 REGIONS"
    rw = draw.textlength(right, font=hf)
    draw.text((W - MARGIN - rw, 198), right, font=hf, fill=RED)
    draw.rectangle([gx0, 214, W - MARGIN, 215], fill=INK)
    # Grid lines.
    for r in range(rows + 1):
        y = gy0 + r * ch
        draw.line([(gx0, y), (W - MARGIN, y)], fill=(205, 205, 205), width=1)
    for c in range(1, cols):
        x = gx0 + c * cw + (c - 1) * 8 + 4
        draw.line([(x, gy0), (x, gy0 + rows * ch)], fill=(205, 205, 205), width=1)
    # Cells: tag, up to 2 headline lines, exactly 1 summary line.
    hfont = font(SANS_B, 13)
    sfont = font(SANS, 10)
    for i, (region, headline, summary) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x = gx0 + c * (cw + 8)
        y = gy0 + r * ch
        tag(draw, x + 4, y + 4, region)
        hlines = wrap(draw, headline, hfont, cw - 8)[:2]
        hy = y + 20
        for line in hlines:
            draw.text((x + 4, hy), line, font=hfont, fill=INK)
            hy += 15
        sline = ellipsize(draw, summary, sfont, cw - 8)
        draw.text((x + 4, hy), sline, font=sfont, fill=(60, 60, 60))


def draw_footer(draw):
    ff = font(SANS, 10)
    fw = draw.textlength(SOURCES, font=ff)
    draw.text(((W - fw) / 2, 1002), SOURCES, font=ff, fill=FAINT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_grid(draw)
    draw_footer(draw)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    img.save(os.path.join(outdir, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    main()
