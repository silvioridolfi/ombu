#!/usr/bin/env python3
"""Genera el tema de íconos "Ombu" (SVG): cuadrados redondeados de colores con glifos Tabler (MIT).

Uso:  python3 tools/gen-icon-theme.py
Salida: config/includes.chroot/usr/share/icons/Ombu/
Hereda de Papirus: lo que no está acá se ve con Papirus.
"""
import os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "config", "includes.chroot", "usr", "share", "icons", "Ombu")
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "ombu-tabler")
TABLER = "https://cdn.jsdelivr.net/npm/@tabler/icons@3.34.0/icons/outline/%s.svg"

TURQUESA, MAGENTA, NARANJA, AZUL, VERDE, VIOLETA, AMBAR, ROJO, GRIS = (
    "#10a8c0", "#d6358a", "#e0852b", "#2d7fd1", "#2fa36b", "#7b5bd6", "#e8a321", "#e5484d", "#4b5568")

# nombre de ícono -> (glifo Tabler, color)
APPS = {
    "firefox-esr": ("world", NARANJA),
    "libreoffice-writer": ("file-text", AZUL),
    "libreoffice-calc": ("table", VERDE),
    "libreoffice-impress": ("presentation", MAGENTA),
    "libreoffice-draw": ("vector-triangle", AMBAR),
    "libreoffice-math": ("math-function", VIOLETA),
    "turbowarp-desktop": ("rocket", ROJO),
    "ombu-scratch": ("puzzle", VIOLETA),
    "ombu-pilas": ("robot", TURQUESA),
    "gcompris-qt": ("school", AMBAR),
    "tuxpaint": ("palette", TURQUESA),
    "tuxmath": ("calculator", AZUL),
    "tuxtype": ("typography", MAGENTA),
    "ktouch": ("keyboard", VIOLETA),
    "kturtle": ("route", VERDE),
    "kolourpaint": ("brush", MAGENTA),
    "audacity": ("wave-sine", NARANJA),
    "org.xfce.filemanager": ("folder", TURQUESA),
    "org.xfce.thunar": ("folder", TURQUESA),
    "org.xfce.terminal": ("terminal-2", GRIS),
    "org.xfce.parole": ("player-play", VIOLETA),
    "org.gnome.SimpleScan": ("scan", AZUL),
    "org.xfce.mousepad": ("notes", GRIS),
    "org.xfce.ristretto": ("photo", MAGENTA),
    "gparted": ("chart-pie", GRIS),
    "ombu-install": ("download", TURQUESA),
}
PLACES = {
    "user-home": ("home", TURQUESA),
    "user-trash": ("trash", NARANJA),
    "user-trash-full": ("trash-x", NARANJA),
    "user-desktop": ("device-desktop", AZUL),
}
DEVICES = {
    "computer": ("device-laptop", MAGENTA),
    "drive-harddisk": ("database", GRIS),
    "drive-removable-media": ("usb", TURQUESA),
    "drive-removable-media-usb": ("usb", TURQUESA),
}
# carpetas: forma propia + glifo pequeño (None = solo carpeta)
FOLDERS = {
    "folder": None, "inode-directory": None, "folder-templates": None, "folder-publicshare": None,
    "folder-documents": "file-text", "folder-download": "download", "folder-music": "music",
    "folder-pictures": "photo", "folder-videos": "movie", "folder-open": None,
}


def glifo(nombre):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, nombre + ".svg")
    if not os.path.exists(p):
        with urllib.request.urlopen(TABLER % nombre, timeout=30) as r:
            open(p, "wb").write(r.read())
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"<svg[^>]*>(.*)</svg>", txt, re.S)
    inner = m.group(1)
    inner = re.sub(r'<path stroke="none"[^>]*/>', "", inner)     # recuadro vacío de Tabler
    return inner.strip()


def cuadrado(color, nombre, escala=1.9):
    t = (64 - 24 * escala) / 2
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
            '<rect x="2" y="2" width="60" height="60" rx="16" fill="%s"/>'
            '<g transform="translate(%.2f %.2f) scale(%.2f)" fill="none" stroke="#ffffff" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">%s</g></svg>'
            % (color, t, t, escala, glifo(nombre)))


def carpeta(glifo_chico=None):
    g = ""
    if glifo_chico:
        g = ('<g transform="translate(22 27) scale(0.8)" fill="none" stroke="#ffffff" stroke-width="2.2" '
             'stroke-linecap="round" stroke-linejoin="round">%s</g>' % glifo(glifo_chico))
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
            '<path d="M6 14a4 4 0 0 1 4-4h14l6 7h24a4 4 0 0 1 4 4v31a4 4 0 0 1-4 4H10a4 4 0 0 1-4-4z" fill="#0b7f93"/>'
            '<rect x="6" y="22" width="52" height="32" rx="4" fill="#10a8c0"/>' + g + '</svg>')


def guardar(sub, nombre, svg):
    d = os.path.join(OUT, "scalable", sub)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, nombre + ".svg"), "w", encoding="utf-8").write(svg)


def main():
    for tabla, sub in ((APPS, "apps"), (PLACES, "places"), (DEVICES, "devices")):
        for nombre, (g, color) in tabla.items():
            guardar(sub, nombre, cuadrado(color, g))
    for nombre, g in FOLDERS.items():
        guardar("places", nombre, carpeta(g))
    open(os.path.join(OUT, "index.theme"), "w", encoding="utf-8").write(
        "[Icon Theme]\nName=Ombú\nComment=Íconos de Ombú (cuadrados redondeados)\nInherits=Papirus,hicolor\n"
        "Directories=scalable/apps,scalable/places,scalable/devices\n\n"
        "[scalable/apps]\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\nContext=Applications\n\n"
        "[scalable/places]\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\nContext=Places\n\n"
        "[scalable/devices]\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\nContext=Devices\n")
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print("Tema Ombu: %d archivos en %s" % (n, os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    sys.exit(main())
