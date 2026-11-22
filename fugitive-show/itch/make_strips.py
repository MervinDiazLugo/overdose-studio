"""Image strips for The Fugitive Show's itch.io description.

itch.io shows the description in a column about 616 px wide, so every strip is drawn at
twice that (1232 px) and shown at half size. Two kinds:

  strip-*.jpg    a wide picture, 1232x400, cut from the press kit art or built from the
                 game's own icons, with a yellow rule under it
  head-<lang>-*.png   a section title on a red slanted tab, 1232x76, transparent around it

    python fugitive-show/itch/make_strips.py <game Assets/Proto dir>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "presskit", "images")
GAME = sys.argv[1] if len(sys.argv) > 1 else r"D:\EngineSpikes\runner-bounty-unity-batch\Assets\Proto"
ICONS = os.path.join(GAME, "Kit", "combat")
ANTON = os.path.join(GAME, "Resources", "Fonts", "Anton-Regular.ttf")

W, H, RULE = 1232, 400, 8
INK, RED, YEL, BG, TEAL = (14, 16, 20), (229, 36, 33), (255, 194, 26), (27, 30, 38), (16, 40, 46)


def cover(im, w, h, fx=0.5, fy=0.5):
    """Scale to fill w x h, then cut the window whose centre sits at (fx, fy) of the spare room."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = round((im.width - w) * fx), round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def finish(im, name):
    out = Image.new("RGB", (W, H + RULE), YEL)
    out.paste(im.convert("RGB"), (0, 0))
    ImageDraw.Draw(out).rectangle([0, 0, W - 1, H + RULE - 1], outline=INK, width=4)
    out.save(os.path.join(HERE, name), quality=88, optimize=True)


def kit(name):
    return Image.open(os.path.join(KIT, name)).convert("RGB")


def icon(name, tall):
    im = Image.open(os.path.join(ICONS, name + ".png")).convert("RGBA")
    box = im.getbbox()
    im = im.crop(box)
    s = tall / im.height
    return im.resize((max(1, round(im.width * s)), tall), Image.LANCZOS)


def backdrop(a, b):
    """A dark studio backdrop: a soft diagonal blend of two colours with thin light rays."""
    im = Image.new("RGB", (W, H), a)
    px = im.load()
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.7 + y / H * 0.3)
            px[x, y] = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(-6, 18):
        x0 = i * 110
        d.polygon([(x0, H), (x0 + 26, H), (x0 + 330, 0), (x0 + 318, 0)], fill=(255, 255, 255, 10))
    return im


def row(names, tall, base, gap, bg, lift=None):
    im = bg.copy()
    pics = [icon(n, tall) for n in names]
    total = sum(p.width for p in pics) + gap * (len(pics) - 1)
    if total > W - 60:                           # too many for the strip: all a little smaller
        return row(names, int(tall * (W - 60) / total), base, gap, bg, lift)
    x = (W - total) // 2
    for i, p in enumerate(pics):
        y = base - p.height - (lift[i] if lift else 0)
        shadow = Image.new("RGBA", p.size, (0, 0, 0, 0))
        shadow.putalpha(p.split()[3].point(lambda v: v * 0.45))
        im.paste(shadow, (x + 10, y + 10), shadow)
        im.paste(p, (x, y), p)
        x += p.width + gap
    return im


def strips():
    finish(cover(kit("05-sorteo-hunters.png"), W, H, 0.5, 0.86), "strip-cast-on-stage.jpg")
    finish(cover(kit("02-lobby-estudio.png"), W, H, 0.5, 0.06), "strip-studio.jpg")
    finish(cover(kit("06-caceria.png"), W, H, 0.5, 0.42), "strip-hunt.jpg")
    finish(cover(kit("07-combate.png"), W, H, 0.5, 0.45), "strip-combat.jpg")

    gear = ["w_rattler", "w_rivet", "w_lob", "ammo_boom", "vest", "bubble", "portal"]
    finish(row(gear, 190, 300, 30, backdrop((12, 30, 36), (40, 22, 52))), "strip-shop.jpg")

    cast = ["front_convict", "front_biker", "front_punk", "front_luchador", "front_bride", "front_butcher", "front_cowboy", "front_pilot", "front_mercenary"]
    finish(row(cast, 330, H + 40, -150, backdrop((46, 16, 30), (14, 38, 46))), "strip-cast.jpg")

    # Two arenas, from the game's own map cards: the wasteland on the left, the city on the
    # right, cut on a slant.
    left = cover(Image.open(os.path.join(ICONS, "map_wasteland.png")).convert("RGB"), W, H, 0.5, 0.55)
    right = cover(Image.open(os.path.join(ICONS, "map_city.png")).convert("RGB"), W, H, 0.5, 0.5)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(W // 2 + 70, 0), (W, 0), (W, H), (W // 2 - 70, H)], fill=255)
    left.paste(right, (0, 0), mask)
    d = ImageDraw.Draw(left)
    d.line([(W // 2 + 70, 0), (W // 2 - 70, H)], fill=INK, width=14)
    d.line([(W // 2 + 70, 0), (W // 2 - 70, H)], fill=YEL, width=6)
    finish(left, "strip-arenas.jpg")


def head(text, name):
    font = ImageFont.truetype(ANTON, 46)
    hh, pad, slant, drop = 76, 30, 22, 7
    tw = round(font.getlength(text))
    wide = tw + pad * 2 + slant
    im = Image.new("RGBA", (W, hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    top, bot = 4, hh - drop - 4
    tab = [(slant, top), (wide + slant, top), (wide, bot), (0, bot)]
    d.polygon([(x + drop, y + drop) for x, y in tab], fill=INK)
    d.polygon(tab, fill=RED)
    d.line(tab + [tab[0]], fill=INK, width=4)
    ty = top + (bot - top) // 2
    d.text((slant // 2 + pad + 3, ty + 3), text, font=font, fill=INK, anchor="lm")
    d.text((slant // 2 + pad, ty), text, font=font, fill=(255, 255, 255), anchor="lm")
    # A yellow rule runs on to the right edge, with three short dashes like a film leader.
    x = wide + slant + 18
    d.rectangle([x, ty - 4 + drop // 2, W - 120, ty + 4 + drop // 2], fill=YEL)
    for i in range(3):
        d.rectangle([W - 104 + i * 36, ty - 4 + drop // 2, W - 84 + i * 36, ty + 4 + drop // 2], fill=YEL)
    im.save(os.path.join(HERE, name), optimize=True)


HEADS = {
    "en": ["LIVE FROM THE STUDIO", "BUY BEFORE THE DRAW", "ONE RUNS, THE REST HUNT", "2:30 OF COMIC-BOOK CHAOS",
           "A RIDICULOUS CAST", "TWO ARENAS", "MORE TO KNOW"],
    "es": ["EN VIVO DESDE EL ESTUDIO", "COMPRA ANTES DEL SORTEO", "UNO CORRE, EL RESTO CAZA", "2:30 DE CAOS DE HISTORIETA",
           "UN ELENCO RIDÍCULO", "DOS ESCENARIOS", "MÁS DATOS"],
}

if __name__ == "__main__":
    strips()
    for lang, titles in HEADS.items():
        for i, t in enumerate(titles, 1):
            head(t, f"head-{lang}-{i}.png")
    print("done")
