#!/usr/bin/env python3
"""
Genera TODA la identidad visual de Ombú (fondos, login, arranque, GRUB,
instalador, logo) usando la paleta de la DTE y la tipografía Encode Sans.

No hace falta correrlo para construir la ISO: los PNG ya vienen generados en
assets/generated/. Sirve para regenerarlos si cambian la paleta o los textos.

Requisitos: python3, Pillow, numpy y rsvg-convert (paquete librsvg2-bin).
Uso:  python3 tools/gen-assets.py
"""
import os
import shutil
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "assets", "fonts", "EncodeSans[wdth,wght].ttf")
BRAND = os.path.join(ROOT, "assets", "brand")
OUT = os.path.join(ROOT, "assets", "generated")
os.makedirs(OUT, exist_ok=True)

# --- Paleta tomada de los archivos de la DTE (logo color, DTE 1, plantilla) ---
PINK = (229, 34, 119)      # #E52277
MAGENTA = (170, 49, 122)   # #AA317A
STEEL = (58, 118, 155)     # #3A769B
TEAL = (16, 168, 192)      # #10A8C0
TEAL2 = (0, 172, 194)      # #00ACC2
NAVY = (4, 70, 110)        # #04466E
WHITE = (255, 255, 255)


def font(size, weight=700, width=100):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight, width])
    return f


def gradient(w, h, stops=((0.0, PINK), (0.5, STEEL), (1.0, TEAL2))):
    """Degradé diagonal (arriba-izquierda -> abajo-derecha) como el de DTE 1."""
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    t = (xs / max(w - 1, 1)) * 0.62 + (ys / max(h - 1, 1)) * 0.38
    t = np.clip(t, 0, 1)
    out = np.zeros((h, w, 3), np.float32)
    for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
        m = (t >= t0) & (t <= t1)
        k = ((t - t0) / (t1 - t0))[m][:, None]
        out[m] = np.array(c0) * (1 - k) + np.array(c1) * k
    return Image.fromarray(out.astype(np.uint8), "RGB").convert("RGBA")


def vgradient(w, h, top, bottom):
    ys = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    arr = np.array(top, np.float32) * (1 - ys) + np.array(bottom, np.float32) * ys
    arr = np.broadcast_to(arr, (h, w, 3))
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")


# --- Ícono del ombú (SVG propio, original de Ombú) ---------------------------
def tree_svg(canopy, trunk, highlight):
    """Ombú: copa ancha en forma de sombrilla, tronco grueso y raíces tabulares."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <path fill="{trunk}" d="M96 112 C100 140 94 164 82 184 C72 198 56 207 32 210
    L86 210 C90 210 94 192 100 192 C106 192 108 210 112 210
    L128 210 C132 210 134 192 140 192 C146 192 150 210 154 210
    L208 210 C184 207 168 198 158 184 C146 164 140 140 144 112 Z"/>
  <g fill="{canopy}">
    <circle cx="52" cy="108" r="30"/>
    <circle cx="82" cy="80" r="38"/>
    <circle cx="120" cy="66" r="46"/>
    <circle cx="160" cy="80" r="38"/>
    <circle cx="190" cy="108" r="30"/>
    <ellipse cx="120" cy="106" rx="100" ry="30"/>
  </g>
  <g fill="{highlight}" opacity="0.22">
    <circle cx="96" cy="60" r="22"/>
    <circle cx="150" cy="86" r="18"/>
    <circle cx="62" cy="100" r="16"/>
  </g>
</svg>"""


def render_svg(svg, size):
    with tempfile.TemporaryDirectory() as td:
        sp = os.path.join(td, "t.svg")
        pp = os.path.join(td, "t.png")
        with open(sp, "w") as fh:
            fh.write(svg)
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), sp, "-o", pp], check=True)
        return Image.open(pp).convert("RGBA")


def icon_white(size):
    return render_svg(tree_svg("#FFFFFF", "#FFFFFF", "#FFFFFF"), size)


def icon_color(size):
    return render_svg(tree_svg("#10A8C0", "#04466E", "#FFFFFF"), size)


def text_size(draw, txt, f):
    l, t, r, b = draw.textbbox((0, 0), txt, font=f)
    return r - l, b - t, l, t


def draw_text(img, xy, txt, f, fill=WHITE, anchor="la"):
    ImageDraw.Draw(img).text(xy, txt, font=f, fill=fill, anchor=anchor)


def lockup_white(height=220):
    """Ícono + 'Ombú' en blanco (transparente)."""
    ic = icon_white(height)
    f = font(int(height * 0.62), 800)
    tmp = Image.new("RGBA", (10, 10))
    w, h, l, t = text_size(ImageDraw.Draw(tmp), "Ombú", f)
    gap = int(height * 0.08)
    out = Image.new("RGBA", (height + gap + w + 8, height), (0, 0, 0, 0))
    out.alpha_composite(ic, (0, 0))
    ImageDraw.Draw(out).text((height + gap, int(height * 0.60)), "Ombú", font=f, fill=WHITE, anchor="ls")
    return out


def lockup_color(height=220):
    ic = icon_color(height)
    f = font(int(height * 0.62), 800)
    tmp = Image.new("RGBA", (10, 10))
    w, h, l, t = text_size(ImageDraw.Draw(tmp), "Ombú", f)
    gap = int(height * 0.08)
    out = Image.new("RGBA", (height + gap + w + 8, height), (0, 0, 0, 0))
    out.alpha_composite(ic, (0, 0))
    ImageDraw.Draw(out).text((height + gap, int(height * 0.60)), "Ombú", font=f, fill=NAVY, anchor="ls")
    return out


def dte_white(width):
    im = Image.open(os.path.join(BRAND, "logo-dte-blanco.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    h = int(im.height * width / im.width)
    return im.resize((width, h), Image.LANCZOS)


def dte_color(width):
    im = Image.open(os.path.join(BRAND, "logo-dte-color.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    h = int(im.height * width / im.width)
    return im.resize((width, h), Image.LANCZOS)


def save(img, *path, mode="RGBA"):
    p = os.path.join(OUT, *path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if mode == "RGB":
        img = img.convert("RGB")
    img.save(p, optimize=True)
    print("  ->", os.path.relpath(p, ROOT), img.size)
    return p


def silhouette(img, size, x, y, alpha=26):
    ic = icon_white(size)
    r, g, b, a = ic.split()
    a = a.point(lambda v: v * alpha // 255)
    ic = Image.merge("RGBA", (r, g, b, a))
    img.alpha_composite(ic, (x, y))


def build_wallpaper(w, h):
    img = gradient(w, h)
    # silueta grande del ombú a la derecha (marca de agua)
    big = int(h * 0.80)
    silhouette(img, big, w - int(big * 0.92), int(h * 0.10), alpha=24)
    # lockup centrado-izquierda: los íconos del escritorio ocupan las primeras columnas
    lh = int(h * 0.19)
    lk = lockup_white(lh)
    x0, y0 = int(w * 0.34), int(h * 0.40)
    img.alpha_composite(lk, (x0, y0))
    d = ImageDraw.Draw(img)
    d.text((x0 + 6, y0 + lh + int(h * 0.025)), "Sistema operativo libre para las escuelas bonaerenses",
           font=font(int(h * 0.030), 500), fill=(255, 255, 255, 235), anchor="la")
    # firma institucional abajo a la derecha
    dl = dte_white(int(w * 0.44))
    img.alpha_composite(dl, (w - dl.width - int(w * 0.035), h - dl.height - int(h * 0.05)))
    return img


def build_login(w, h):
    img = gradient(w, h)
    big = int(h * 1.0)
    silhouette(img, big, int(w * -0.06), int(h * 0.12), alpha=22)
    lk = lockup_white(int(h * 0.12))
    img.alpha_composite(lk, (int(w * 0.04), int(h * 0.06)))
    dl = dte_white(int(w * 0.44))
    img.alpha_composite(dl, (w - dl.width - int(w * 0.035), h - dl.height - int(h * 0.05)))
    return img


def rounded(img, radius):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=radius, fill=255)
    out = img.copy()
    out.putalpha(m)
    return out


def main():
    print("Ícono y logo")
    save(icon_white(512), "ombu-icon-white.png")
    save(icon_color(512), "ombu-icon-color.png")
    save(lockup_white(240), "ombu-logo-white.png")
    save(lockup_color(240), "ombu-logo-color.png")

    print("Escritorio y login")
    save(build_wallpaper(1920, 1080), "wallpaper-1920x1080.png", mode="RGB")
    save(build_login(1920, 1080), "login-1920x1080.png", mode="RGB")

    print("Plymouth (pantalla de arranque)")
    save(gradient(1366, 768), "plymouth", "bg.png", mode="RGB")
    ply = Image.new("RGBA", (560, 300), (0, 0, 0, 0))
    ic = icon_white(210)
    ply.alpha_composite(ic, ((560 - 210) // 2, 0))
    f = font(76, 800)
    ImageDraw.Draw(ply).text((280, 290), "Ombú", font=f, fill=WHITE, anchor="ms")
    save(ply, "plymouth", "logo.png")
    save(dte_white(520), "plymouth", "dte.png")
    bar_bg = Image.new("RGBA", (400, 10), (0, 0, 0, 0))
    ImageDraw.Draw(bar_bg).rounded_rectangle((0, 0, 399, 9), radius=5, fill=(255, 255, 255, 70))
    save(bar_bg, "plymouth", "bar-bg.png")
    bar_fill = Image.new("RGBA", (400, 10), (0, 0, 0, 0))
    ImageDraw.Draw(bar_fill).rounded_rectangle((0, 0, 399, 9), radius=5, fill=(255, 255, 255, 255))
    save(bar_fill, "plymouth", "bar-fill.png")

    print("GRUB (sistema instalado) y menú de arranque de la ISO")
    g = gradient(1366, 768)
    lk = lockup_white(120)
    g.alpha_composite(lk, ((1366 - lk.width) // 2, 70))
    dl = dte_white(520)
    g.alpha_composite(dl, ((1366 - dl.width) // 2, 768 - dl.height - 24))
    save(g, "grub-1366x768.png", mode="RGB")

    s = gradient(640, 480)
    lk = lockup_white(84)
    s.alpha_composite(lk, ((640 - lk.width) // 2, 36))
    ImageDraw.Draw(s).text((320, 150), "Sistema operativo educativo - DTE Región 1",
                           font=font(17, 500), fill=(255, 255, 255, 235), anchor="mm")
    dl = dte_white(420)
    s.alpha_composite(dl, ((640 - dl.width) // 2, 480 - dl.height - 12))
    p = save(s, "splash-640x480.png", mode="RGB")
    import base64
    with open(p, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    svg = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
           '<svg version="1.1" width="640" height="480" xmlns="http://www.w3.org/2000/svg" '
           'xmlns:xlink="http://www.w3.org/1999/xlink">\n'
           f'<image x="0" y="0" width="640" height="480" xlink:href="data:image/png;base64,{b64}"/>\n</svg>\n')
    with open(os.path.join(OUT, "splash.svg"), "w") as fh:
        fh.write(svg)
    print("  -> assets/generated/splash.svg")

    print("Instalador (Calamares)")
    save(icon_white(256), "calamares", "ombu-logo.png")
    wlc = gradient(457, 300)
    lk = lockup_white(104)
    wlc.alpha_composite(lk, ((457 - lk.width) // 2, 52))
    dl = dte_white(400)
    wlc.alpha_composite(dl, ((457 - dl.width) // 2, 300 - dl.height - 22))
    save(wlc, "calamares", "welcome.png", mode="RGB")

    def slide(title, lines, name, show_icon=True):
        im = gradient(560, 300)
        d = ImageDraw.Draw(im)
        if show_icon:
            im.alpha_composite(icon_white(120), (22, 22))
            tx = 160
        else:
            tx = 28
        d.text((tx, 36), title[0], font=font(34, 800), fill=WHITE)
        if len(title) > 1:
            d.text((tx, 78), title[1], font=font(34, 800), fill=WHITE)
        y = 160
        for ln in lines:
            d.text((32, y), ln, font=font(21, 500), fill=(255, 255, 255, 240))
            y += 36
        save(rounded(im, 22), "calamares", name)

    slide(("Te damos la", "bienvenida a Ombú"),
          ["El resto de la instalación es automática.",
           "Tarda unos minutos: es un buen momento",
           "para tomar unos mates."], "slide1.png")
    slide(("Todo para aprender", "ya viene incluido"),
          ["Scratch (TurboWarp), GCompris, Tux Paint,",
           "LibreOffice, Audacity, Tux Typing,",
           "Tux Math y Firefox."], "slide2.png")
    slide(("Software libre,", "sin telemetría"),
          ["Ombú no envía datos de uso a nadie.",
           "Es software libre pensado desde el",
           "territorio para las escuelas de la provincia."], "slide3.png")

    slide(("Hecho en el", "territorio"),
          ["Creado por Silvio Ridolfi y el equipo",
           "territorial de Región 1.",
           "DTE | Dirección de Tecnología Educativa."], "slide4.png", show_icon=False)

    # Ícono del lanzador "Instalar Ombú"
    ins = gradient(256, 256)
    ins.alpha_composite(icon_white(190), (33, 22))
    save(rounded(ins, 48), "install-ombu.png")

    # Avatar para el usuario estudiante (.face)
    av = gradient(256, 256)
    av.alpha_composite(icon_white(200), (28, 18))
    save(rounded(av, 128), "avatar-estudiante.png")

    # Fondo para el GTK greeter / otros: copia con nombre fijo
    shutil.copy(os.path.join(OUT, "login-1920x1080.png"), os.path.join(OUT, "login.png"))


if __name__ == "__main__":
    main()
