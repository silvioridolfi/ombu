#!/usr/bin/env python3
"""Genera el tema de ventanas "Ombu" para xfwm4: barra clara, esquinas superiores redondeadas y
botones planos de 46 px (minimizar, maximizar/restaurar, cerrar; el cerrar se pone rojo al pasar el mouse).

Uso:  python3 tools/gen-xfwm4-theme.py
Salida: config/includes.chroot/usr/share/themes/Ombu/xfwm4/
"""
import os, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "config", "includes.chroot", "usr", "share", "themes", "Ombu", "xfwm4")
SS = 8                     # supersampling para suavizar bordes y trazos
H = 30                     # alto de la barra de título
BW = 4                     # grosor de los bordes laterales e inferior
BTN_W = 34                 # ancho de cada botón
BTN_H = 22                 # alto del botón (la barra mide 30: queda un margen que no reacciona al mouse)
R = 9                      # radio de las esquinas superiores

ACTIVO = dict(bg="#f4f6fa", borde="#c3c9d6", glifo="#1b1f2a", texto="#1b1f2a")
INACTIVO = dict(bg="#eceef3", borde="#d2d6e0", glifo="#9097a8", texto="#8d93a3")
PRELIGHT_BG, PRESSED_BG = "#dde1ea", "#c9cfdb"
CERRAR_PRELIGHT, CERRAR_PRESSED = "#e81123", "#f1707a"


def rgba(hexcolor, a=255):
    h = hexcolor.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def guardar(img, nombre):
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, nombre + ".png"), optimize=True)


def barra(p):
    """Mosaico de 2 px de ancho para la barra de título (línea superior del borde incluida)."""
    im = Image.new("RGBA", (2, H), rgba(p["bg"]))
    ImageDraw.Draw(im).line([(0, 0), (1, 0)], fill=rgba(p["borde"]))
    return im


def esquina(p, derecha):
    """Esquina superior redondeada de 8+ px de ancho; fuera del arco queda transparente."""
    w = R
    big = Image.new("RGBA", (w * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    # relleno: rectángulo con la esquina superior izquierda redondeada
    d.rounded_rectangle((0, 0, w * SS * 2, H * SS * 2), radius=R * SS, fill=rgba(p["borde"]))
    d.rounded_rectangle((SS, SS, w * SS * 2, H * SS * 2), radius=(R - 1) * SS, fill=rgba(p["bg"]))
    im = big.resize((w, H), Image.LANCZOS)
    # recorte al lienzo (rounded_rectangle se pasó del borde derecho): la columna x>=R-1 ya es barra
    if derecha:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


def lateral(p, izquierda):
    im = Image.new("RGBA", (BW, 1), rgba(p["bg"]))
    im.putpixel((0 if izquierda else BW - 1, 0), rgba(p["borde"]))
    return im


def inferior(p):
    im = Image.new("RGBA", (1, BW), rgba(p["bg"]))
    im.putpixel((0, BW - 1), rgba(p["borde"]))
    return im


def esquina_inf(p, izquierda):
    """Esquina inferior redondeada (radio = grosor del borde); fuera del arco queda transparente."""
    big = Image.new("RGBA", (BW * SS, BW * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.rounded_rectangle((0, -BW * SS, 2 * BW * SS, BW * SS), radius=BW * SS, fill=rgba(p["borde"]))
    d.rounded_rectangle((SS, -BW * SS, 2 * BW * SS, BW * SS - SS), radius=(BW - 1) * SS, fill=rgba(p["bg"]))
    im = big.resize((BW, BW), Image.LANCZOS)
    return im if izquierda else im.transpose(Image.FLIP_LEFT_RIGHT)


def boton(glifo, fondo, color, ancho=1.15):
    # xfwm4 (sin compositor) descarta los trazos con transparencia parcial: minimizar y maximizar
    # (líneas horizontales y cuadrados) se dibujan pixel-exactos y opacos; solo el cerrar (diagonal) se suaviza.
    if glifo in ("hide", "maximize", "maximize-toggled", "close"):
        im = Image.new("RGBA", (BTN_W, BTN_H), (0, 0, 0, 0))
        dn = ImageDraw.Draw(im)
        if fondo:
            dn.rounded_rectangle((0, 0, BTN_W - 1, BTN_H - 1), radius=5, fill=rgba(fondo))
        c = rgba(color)
        x0, y0 = BTN_W // 2, BTN_H // 2
        if glifo == "hide":
            dn.line([(x0 - 5, y0), (x0 + 5, y0)], fill=c)
        elif glifo == "maximize":
            dn.rectangle([(x0 - 5, y0 - 5), (x0 + 5, y0 + 5)], outline=c)
        elif glifo == "close":
            dn.line([(x0 - 5, y0 - 5), (x0 + 5, y0 + 5)], fill=c)
            dn.line([(x0 + 5, y0 - 5), (x0 - 5, y0 + 5)], fill=c)
        else:
            dn.rectangle([(x0 - 6, y0 - 3), (x0 + 3, y0 + 6)], outline=c)
            dn.line([(x0 - 3, y0 - 3), (x0 - 3, y0 - 6), (x0 + 6, y0 - 6), (x0 + 6, y0 + 3), (x0 + 3, y0 + 3)], fill=c)
        return im
    big = Image.new("RGBA", (BTN_W * SS, BTN_H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    if fondo:
        d.rounded_rectangle((0, 0, BTN_W * SS - 1, BTN_H * SS - 1), radius=5 * SS, fill=rgba(fondo))
    c = rgba(color)
    w = int(ancho * SS)
    cx, cy = BTN_W // 2, BTN_H // 2 + 0

    def p(x, y):
        return (x * SS, y * SS)
    if glifo == "hide":
        d.line([p(cx - 5, cy), p(cx + 5, cy)], fill=c, width=w)
    elif glifo == "maximize":
        d.rectangle([p(cx - 5, cy - 5), p(cx + 5, cy + 5)], outline=c, width=w)
    elif glifo == "maximize-toggled":
        d.rectangle([p(cx - 6, cy - 3), p(cx + 3, cy + 6)], outline=c, width=w)
        d.line([p(cx - 3, cy - 3), p(cx - 3, cy - 6), p(cx + 6, cy - 6), p(cx + 6, cy + 3), p(cx + 3, cy + 3)], fill=c, width=w)
    elif glifo == "close":
        d.line([p(cx - 5, cy - 5), p(cx + 5, cy + 5)], fill=c, width=w)
        d.line([p(cx + 5, cy - 5), p(cx - 5, cy + 5)], fill=c, width=w)
    elif glifo == "menu":
        d.polygon([p(cx - 4, cy - 2), p(cx + 4, cy - 2), p(cx, cy + 3)], fill=c)
    elif glifo == "shade":
        d.line([p(cx - 5, cy - 4), p(cx + 5, cy - 4)], fill=c, width=w * 2)
    elif glifo == "shade-toggled":
        d.line([p(cx - 5, cy + 4), p(cx + 5, cy + 4)], fill=c, width=w * 2)
    elif glifo == "stick":
        d.ellipse([p(cx - 3, cy - 3), p(cx + 3, cy + 3)], outline=c, width=w)
    elif glifo == "stick-toggled":
        d.ellipse([p(cx - 3, cy - 3), p(cx + 3, cy + 3)], fill=c)
    return big.resize((BTN_W, BTN_H), Image.LANCZOS)


def main():
    for estado, p in (("active", ACTIVO), ("inactive", INACTIVO)):
        for n in range(1, 6):
            guardar(barra(p), "title-%d-%s" % (n, estado))
        guardar(esquina(p, False), "top-left-" + estado)
        guardar(esquina(p, True), "top-right-" + estado)
        guardar(lateral(p, True), "left-" + estado)
        guardar(lateral(p, False), "right-" + estado)
        guardar(inferior(p), "bottom-" + estado)
        guardar(esquina_inf(p, True), "bottom-left-" + estado)
        guardar(esquina_inf(p, False), "bottom-right-" + estado)

    glifos = ["hide", "maximize", "maximize-toggled", "close", "menu", "shade", "shade-toggled", "stick", "stick-toggled"]
    for g in glifos:
        cerrar = (g == "close")
        guardar(boton(g, None, ACTIVO["glifo"]), "%s-active" % g)
        guardar(boton(g, None, INACTIVO["glifo"]), "%s-inactive" % g)
        guardar(boton(g, CERRAR_PRELIGHT if cerrar else PRELIGHT_BG, "#ffffff" if cerrar else ACTIVO["glifo"]), "%s-prelight" % g)
        guardar(boton(g, CERRAR_PRESSED if cerrar else PRESSED_BG, "#ffffff" if cerrar else ACTIVO["glifo"]), "%s-pressed" % g)

    open(os.path.join(OUT, "themerc"), "w", encoding="utf-8").write(
        "# Ombú — tema de ventanas para xfwm4 (generado por tools/gen-xfwm4-theme.py)\n"
        "active_text_color=%s\ninactive_text_color=%s\n"
        "active_text_shadow_color=#ffffff\ninactive_text_shadow_color=#ffffff\n"
        "title_shadow_active=false\ntitle_shadow_inactive=false\n"
        "full_width_title=true\ntitle_vertical_offset_active=0\ntitle_vertical_offset_inactive=0\n"
        "title_horizontal_offset=10\nbutton_offset=6\nbutton_spacing=3\n"
        "shadow_delta_height=2\nshadow_delta_width=0\nshadow_delta_x=0\nshadow_delta_y=-10\nshadow_opacity=40\n"
        "frame_border_top=0\n" % (ACTIVO["texto"], INACTIVO["texto"]))
    n = len(os.listdir(OUT))
    print("Tema xfwm4 Ombu: %d archivos en %s" % (n, os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    sys.exit(main())
