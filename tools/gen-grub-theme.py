#!/usr/bin/env python3
"""Genera el tema gráfico de GRUB de Ombú (fondo, selección redondeada y tipografía Encode Sans).

Uso:  python3 tools/gen-grub-theme.py
Salida:
  config/includes.chroot/boot/grub/themes/ombu/     menú del sistema instalado
  bootloader-overrides/grub-pc/live-theme/          menú de la ISO (UEFI)
Requiere: Pillow, python3-fonttools y grub-mkfont (grub-common).
"""
import os, shutil, subprocess, sys, tempfile
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "assets", "wallpapers", "ombu-poliedros-oscuro.png")      # fondo de escritorio (con logos)
FONT = os.path.join(ROOT, "assets", "fonts", "EncodeSans[wdth,wght].ttf")
LOGO_DTE = os.path.join(ROOT, "assets", "brand", "logo-dte-2026-v2-blanco.svg")
LOGO_OMBU = os.path.join(ROOT, "assets", "generated", "ombu-logo-white.png")
DESTINOS = [
    os.path.join(ROOT, "config", "includes.chroot", "boot", "grub", "themes", "ombu"),
    os.path.join(ROOT, "bootloader-overrides", "grub-pc", "live-theme"),
]
W, H = 1366, 768
TURQUESA = (16, 168, 192, 235)


def fondo():
    """Fondo 1366x768: poliedros del escritorio sin sus logos, más el logo de Ombú arriba y el de la DTE abajo, grandes."""
    fino = os.path.join(ROOT, "assets", "wallpapers", "_base-oscuro-limpio.png")
    if os.path.exists(fino):
        base = Image.open(fino).convert("RGB").resize((W, H), Image.LANCZOS)
    else:
        base = Image.open(BASE).convert("RGB").resize((W, H), Image.LANCZOS)
    img = base.convert("RGBA")
    # velo oscuro suave en el centro para que se lea el menú
    velo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(velo).rounded_rectangle((W * 0.18, H * 0.30, W * 0.82, H * 0.74), radius=24, fill=(6, 8, 24, 120))
    img.alpha_composite(velo)
    # logo de Ombú (arriba, centrado)
    omb = Image.open(LOGO_OMBU).convert("RGBA")
    omb = omb.crop(omb.getbbox())
    h = 104
    omb = omb.resize((int(omb.width * h / omb.height), h), Image.LANCZOS)
    img.alpha_composite(omb, ((W - omb.width) // 2, 62))
    # logos de la DTE (abajo, grandes)
    dte = render_svg(LOGO_DTE, 900)
    dte = dte.crop(dte.getbbox())
    w = 820
    dte = dte.resize((w, int(dte.height * w / dte.width)), Image.LANCZOS)
    img.alpha_composite(dte, ((W - w) // 2, H - dte.height - 44))
    return img.convert("RGB")


def render_svg(svg, ancho):
    tmp = tempfile.mkstemp(suffix=".png")[1]
    subprocess.run(["rsvg-convert", "-w", str(ancho), svg, "-o", tmp], check=True)
    return Image.open(tmp).convert("RGBA")


def seleccion(destino):
    """Nueve imágenes (esquinas, bordes y centro) de un rectángulo turquesa redondeado."""
    r, n = 12, 36
    big = Image.new("RGBA", (n * 8, n * 8), (0, 0, 0, 0))
    ImageDraw.Draw(big).rounded_rectangle((0, 0, n * 8 - 1, n * 8 - 1), radius=r * 8, fill=TURQUESA)
    im = big.resize((n, n), Image.LANCZOS)
    cortes = {"nw": (0, 0, r, r), "n": (r, 0, n - r, r), "ne": (n - r, 0, n, r),
              "w": (0, r, r, n - r), "c": (r, r, n - r, n - r), "e": (n - r, r, n, n - r),
              "sw": (0, n - r, r, n), "s": (r, n - r, n - r, n), "se": (n - r, n - r, n, n)}
    for nombre, caja in cortes.items():
        im.crop(caja).save(os.path.join(destino, "select_%s.png" % nombre))


def fuentes(destino):
    """Encode Sans (instancia Medium, ancho normal) convertida a .pf2 de GRUB."""
    tmp = tempfile.mkdtemp()
    ttf = os.path.join(tmp, "EncodeSans-Medium.ttf")
    subprocess.run([sys.executable, "-m", "fontTools.varLib.instancer", FONT, "wght=500", "wdth=100", "-o", ttf], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for tam in (17, 24):
        subprocess.run(["grub-mkfont", "-s", str(tam), "-n", "Ombu Sans", "-o", os.path.join(destino, "ombu-sans-%d.pf2" % tam), ttf],
                       check=True, stderr=subprocess.DEVNULL)
    shutil.rmtree(tmp, ignore_errors=True)


TEMA = """# Ombú — tema de GRUB (generado por tools/gen-grub-theme.py)
desktop-image: "fondo.png"
desktop-image-scale-method: "crop"
desktop-image-h-align: "center"
desktop-image-v-align: "center"
desktop-color: "#14122f"
title-text: ""
terminal-font: "Ombu Sans Medium 17"
message-font: "Ombu Sans Medium 17"
message-color: "#ffffff"
message-bg-color: "#14122f"

+ label {
    top = 29%
    left = 0
    width = 100%
    align = "center"
    text = "Elegí cómo iniciar"
    font = "Ombu Sans Medium 17"
    color = "#aab3c5"
}

+ boot_menu {
    left = 15%
    width = 70%
    top = 34%
    height = 40%
    item_font = "Ombu Sans Medium 24"
    item_color = "#e8edf2"
    selected_item_font = "Ombu Sans Medium 24"
    selected_item_color = "#04283a"
    selected_item_pixmap_style = "select_*.png"
    item_height = 42
    item_padding = 10
    item_spacing = 6
    icon_width = 0
    icon_height = 0
    item_icon_space = 0
    scrollbar = false
}

+ label {
    id = "__timeout__"
    top = 72%
    left = 0
    width = 100%
    align = "center"
    text = "Iniciando automáticamente en %d s"
    font = "Ombu Sans Medium 17"
    color = "#aab3c5"
}

+ label {
    top = 76%
    left = 0
    width = 100%
    align = "center"
    text = "Flechas para elegir  ·  Enter para iniciar  ·  E para editar"
    font = "Ombu Sans Medium 17"
    color = "#7f8aa3"
}
"""


def main():
    bg = fondo()
    for d in DESTINOS:
        os.makedirs(d, exist_ok=True)
        for viejo in os.listdir(d):                         # limpia restos del tema anterior
            if viejo.endswith((".png", ".pf2", ".txt")):
                os.remove(os.path.join(d, viejo))
        bg.save(os.path.join(d, "fondo.png"), optimize=True)
        seleccion(d)
        fuentes(d)
        open(os.path.join(d, "theme.txt"), "w", encoding="utf-8").write(TEMA)
        print("Tema GRUB ->", os.path.relpath(d, ROOT), len(os.listdir(d)), "archivos")


if __name__ == "__main__":
    sys.exit(main())
