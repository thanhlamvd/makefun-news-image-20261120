#!/usr/bin/env python3
"""Render the 20 November 2026 front page as a 1024x1024 PNG.

Pure Python 3.13 standard library: an RGB framebuffer, a hand-made
5x7 bitmap font and a tiny PNG encoder on top of zlib. No network, no
clock, no randomness, so every run writes identical bytes.

    python3 generate_image.py [output.png]

With no argument the image goes to entry.png next to this file.
This is a build-time tool only; the entry itself is main.py, which
copies the committed entry.png into the output directory.
"""

import binascii
import os
import struct
import sys
import zlib

W = 1024
H = 1024

# 5x7 bitmap font, capital letters and digits only. A glyph is seven
# rows of five cells; '#' is ink, '.' is paper. All front-page text
# is set in capitals, so no lowercase shapes are needed.
GLYPHS = {
    "A": (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    "C": (" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"),
    "D": ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    "E": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    "F": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    "G": (" ####", "#    ", "#    ", "#  ##", "#   #", "#   #", " ### "),
    "H": ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "I": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"),
    "J": ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    "K": ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    "R": ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    "S": (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    "X": ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    "Y": ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    "0": (" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "# #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "2": (" ### ", "#   #", "    #", "  ## ", " #   ", "#    ", "#####"),
    "3": ("#### ", "    #", "    #", " ### ", "    #", "    #", "#### "),
    "4": ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    "6": (" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "),
    "7": ("#####", "    #", "   # ", "  #  ", "  #  ", " #   ", " #   "),
    "8": (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    "9": (" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "),
    " ": ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    ",": ("     ", "     ", "     ", "     ", "  ## ", "  ## ", " #   "),
    ".": ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ":": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    ";": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", " #   "),
    "'": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
    "-": ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
    "/": ("    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "),
    "&": (" ##  ", "#  # ", "#  # ", " #   ", "# # #", "#  # ", " ## #"),
    "(": ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
    ")": (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
    "%": ("##  #", "## # ", "   # ", "  #  ", " #   ", "# # #", "#  ##"),
    "$": ("  #  ", " ####", "# #  ", " ### ", "  # #", "#### ", "  #  "),
    "?": (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    "!": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
}


def canvas(width, height, colour):
    return bytearray(bytes(colour) * (width * height))


def paint(buf, x, y, w, h, colour):
    r, g, b = colour
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            o = base + (xx - x0) * 3
            buf[o] = r
            buf[o + 1] = g
            buf[o + 2] = b


def frame(buf, x, y, w, h, colour, thick=2):
    paint(buf, x, y, w, thick, colour)
    paint(buf, x, y + h - thick, w, thick, colour)
    paint(buf, x, y, thick, h, colour)
    paint(buf, x + w - thick, y, thick, h, colour)


def glyph(buf, x, y, ch, colour, scale):
    shape = GLYPHS.get(ch, GLYPHS["?"])
    for row in range(7):
        for col in range(5):
            if shape[row][col] == "#":
                paint(buf, x + col * scale, y + row * scale,
                      scale, scale, colour)


def text_w(text, scale):
    return len(text) * 6 * scale


def put_text(buf, x, y, text, colour, scale):
    cx = x
    for ch in text:
        glyph(buf, cx, y, ch, colour, scale)
        cx += 6 * scale


def put_centred(buf, y, text, colour, scale):
    put_text(buf, (W - text_w(text, scale)) // 2, y, text, colour, scale)


def fit_scale(text, max_w, start):
    """Largest scale at or below `start` that fits `text` in `max_w`."""
    scale = start
    while scale > 1 and text_w(text, scale) > max_w:
        scale -= 1
    return scale


def wrap_words(text, limit):
    lines = []
    cur = ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if len(trial) <= limit:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def put_wrapped(buf, x, y, text, colour, scale, limit, line_h):
    lines = wrap_words(text, limit)
    for i, line in enumerate(lines):
        put_text(buf, x, y + i * line_h, line, colour, scale)
    return y + len(lines) * line_h


def png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    return out + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)


def save_png(path, width, height, buf):
    raw = b"".join(
        b"\x00" + bytes(buf[y * width * 3:(y + 1) * width * 3])
        for y in range(height)
    )
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", ihdr)
    png += png_chunk(b"IDAT", zlib.compress(raw, 9))
    png += png_chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


PAPER = (250, 247, 240)
CARD = (255, 255, 255)
INK = (22, 22, 30)
NAVY = (15, 23, 42)
GOLD = (198, 160, 38)
GREY = (98, 114, 138)
LINE = (201, 211, 224)
WHITE = (255, 255, 255)

# Six stories, each verified against reporting dated 20 November 2026.
STORIES = [
    {
        "kicker": "EUROPE",
        "accent": (37, 99, 235),
        "headline": "RUSSIAN MISSILES LAND IN POLAND",
        "body": "THREE OBJECTS, TWO MISSILES AND A DRONE, CROSS "
                "INTO POLAND DURING ALLIED DRILLS. NATO CALLS IT "
                "A VIOLATION OF POLISH AIRSPACE.",
        "source": "AP - REUTERS",
    },
    {
        "kicker": "WAR IN UKRAINE",
        "accent": (217, 119, 6),
        "headline": "KYIV BRIDGES HIT, EIGHT KILLED",
        "body": "OVERNIGHT STRIKES TARGET BRIDGES IN KYIV. 28 "
                "PEOPLE INJURED ACROSS NINE REGIONS, OFFICIALS SAY.",
        "source": "REUTERS",
    },
    {
        "kicker": "MIDDLE EAST",
        "accent": (220, 38, 38),
        "headline": "SAUDI SHOOTS DOWN HOUTHI MISSILE",
        "body": "AIR DEFENCES INTERCEPT A BALLISTIC MISSILE AND "
                "TWO DRONES AIMED AT THE SOUTH. RIYADH WAS AMONG "
                "THE TARGETS.",
        "source": "REUTERS - AP",
    },
    {
        "kicker": "IRAQ",
        "accent": (124, 58, 237),
        "headline": "IRAQ MOVES ON MILITIA STRONGHOLD",
        "body": "FEDERAL FORCES DEPLOY AT JURF AL-SAKHAR, BASE "
                "OF IRAN-BACKED KATAIB HEZBOLLAH, ACCUSED OF "
                "RUNNING AN OIL-SMUGGLING NETWORK.",
        "source": "REUTERS - AP",
    },
    {
        "kicker": "MARKETS",
        "accent": (5, 150, 105),
        "headline": "STOCKS SLIDE AS AI SELL-OFF DEEPENS",
        "body": "S AND P 500 NEARS CORRECTION, DOWN 2 PERCENT "
                "FOR A FIFTH STRAIGHT DAY. ASIAN MARKETS FALL "
                "SHARPLY, WITH THE NIKKEI DOWN 4.8 PERCENT.",
        "source": "REUTERS - AP",
    },
    {
        "kicker": "CLIMATE",
        "accent": (13, 148, 136),
        "headline": "COP31 DRAFT DROPS FOSSIL FUEL EXIT",
        "body": "NEGOTIATORS REMOVE ANY CALL TO PHASE OUT FOSSIL "
                "FUELS FROM THE DRAFT DEAL. PACIFIC NATIONS "
                "DEMAND A PHASE-OUT.",
        "source": "THE HINDU - CBC NEWS",
    },
]


def render():
    buf = canvas(W, H, PAPER)
    # Masthead: navy band, title, date, gold rule.
    paint(buf, 0, 0, W, 150, NAVY)
    put_centred(buf, 24, "THE WORLD IN ONE DAY", WHITE, 4)
    date = "FRIDAY, 20 NOVEMBER 2026"
    date_scale = fit_scale(date, W - 80, 3)
    put_centred(buf, 92, date, GOLD, date_scale)
    paint(buf, 0, 150, W, 4, GOLD)

    # Six cards: three columns, two rows.
    margin = 24
    gap = 16
    top = 172
    bottom = 896
    cols = 3
    rows = 2
    card_w = (W - 2 * margin - (cols - 1) * gap) // cols
    card_h = (bottom - top - (rows - 1) * gap) // rows
    for i, story in enumerate(STORIES):
        col = i % cols
        row = i // cols
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        paint(buf, x, y, card_w, card_h, CARD)
        frame(buf, x, y, card_w, card_h, LINE, 2)
        paint(buf, x, y, card_w, 9, story["accent"])
        put_text(buf, x + 16, y + 26, story["kicker"],
                 story["accent"], 1)
        put_text(buf, x + 16 + text_w(story["kicker"], 1) + 12,
                 y + 26, str(i + 1), GREY, 1)
        after = put_wrapped(buf, x + 16, y + 54, story["headline"],
                            INK, 2, (card_w - 32) // 12, 30)
        paint(buf, x + 16, after + 10, card_w - 32, 2, LINE)
        put_wrapped(buf, x + 16, after + 26, story["body"],
                    INK, 1, (card_w - 32) // 6, 15)
        put_text(buf, x + 16, y + card_h - 28, story["source"],
                 GREY, 1)
    # The day in numbers: one verified figure from four of the stories.
    paint(buf, margin, 912, W - 2 * margin, 52, NAVY)
    numbers = ("8 KILLED IN KYIV  -  3 OBJECTS OVER POLAND  -  "
               "S AND P 500 DOWN 2%  -  NIKKEI DOWN 4.8%")
    put_centred(buf, 930, numbers, WHITE, 1)
    put_centred(buf, 982,
                "SOURCES: REUTERS - AP - BBC - THE HINDU - CBC NEWS",
                GREY, 1)
    return buf


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "entry.png")
    buf = render()
    save_png(out, W, H, buf)
    print("wrote %s (%dx%d)" % (out, W, H))


if __name__ == "__main__":
    main()
