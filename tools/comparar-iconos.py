import gi, os, sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from PIL import Image, ImageDraw, ImageFont

TEMAS = [("Ombu", "Ombú (actual, sobre Papirus)"), ("Papirus", "Papirus"), ("Numix-Circle", "Numix Circle"),
         ("elementary-xfce", "elementary-xfce"), ("breeze", "Breeze (KDE)"), ("Moka", "Moka"),
         ("Yaru", "Yaru (Ubuntu)"), ("Adwaita", "Adwaita (GNOME)")]
ICONOS = [("firefox-esr","Firefox"),("libreoffice-writer","Writer"),("libreoffice-calc","Calc"),("libreoffice-impress","Impress"),
          ("turbowarp-desktop","TurboWarp"),("ombu-scratch","Scratch"),("ombu-pilas","Pilas Bloques"),("gcompris-qt","GCompris"),
          ("tuxpaint","Tux Paint"),("tuxmath","Tux Math"),("ktouch","KTouch"),("audacity","Audacity"),
          ("org.xfce.thunar","Archivos"),("folder","Carpeta"),("user-home","Personal"),("user-trash","Papelera"),
          ("drive-harddisk","Disco"),("utilities-terminal","Terminal"),("preferences-system","Config."),("system-shutdown","Apagar")]
COLS, TAM, CELDA_W, CELDA_H, IZQ = 10, 56, 104, 92, 190
FUENTE = ImageFont.truetype(sys.argv[2], 14) if os.path.exists(sys.argv[2]) else ImageFont.load_default()
FUENTE_T = ImageFont.truetype(sys.argv[2], 20) if os.path.exists(sys.argv[2]) else ImageFont.load_default()
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
it = Gtk.IconTheme.new()
ombu = Gtk.IconTheme.new(); ombu.set_custom_theme("Ombu")

def icono(tema, nombre):
    info = tema.lookup_icon(nombre, TAM, Gtk.IconLookupFlags.FORCE_SIZE)
    if info is None and nombre.startswith("ombu-"):
        info = ombu.lookup_icon(nombre, TAM, Gtk.IconLookupFlags.FORCE_SIZE)   # apps propias de Ombu
    if info is None:
        info = tema.lookup_icon("application-x-executable", TAM, Gtk.IconLookupFlags.FORCE_SIZE)
    pb = info.load_icon()
    ruta = "/tmp/ic.png"; pb.savev(ruta, "png", [], [])
    return Image.open(ruta).convert("RGBA").resize((TAM, TAM))

def hoja(temas, destino):
    filas = (len(ICONOS) + COLS - 1) // COLS
    alto_t = filas * CELDA_H + 36
    img = Image.new("RGB", (IZQ + COLS * CELDA_W + 10, len(temas) * alto_t + 10), (20, 18, 47))
    d = ImageDraw.Draw(img)
    for n, (tid, etiqueta) in enumerate(temas):
        it.set_custom_theme(tid)
        y0 = 10 + n * alto_t
        d.text((14, y0 + alto_t // 2 - 30), etiqueta, font=FUENTE_T, fill=(16, 168, 192))
        d.line([(10, y0 + alto_t - 8), (img.width - 10, y0 + alto_t - 8)], fill=(60, 58, 90))
        for i, (nom, rot) in enumerate(ICONOS):
            x = IZQ + (i % COLS) * CELDA_W + (CELDA_W - TAM) // 2
            y = y0 + (i // COLS) * CELDA_H + 6
            ic = icono(it, nom)
            img.paste(ic, (x, y), ic)
            w = d.textlength(rot, font=FUENTE)
            d.text((IZQ + (i % COLS) * CELDA_W + (CELDA_W - w) / 2, y + TAM + 6), rot, font=FUENTE, fill=(232, 237, 242))
    img.save(destino)

# Candidatos propios: carpeta (3er argumento) con un juego de iconos por subcarpeta (cada una con index.theme)
EXTRA = []
if len(sys.argv) > 3 and os.path.isdir(sys.argv[3]):
    home_icons = os.path.expanduser("~/.icons"); os.makedirs(home_icons, exist_ok=True)
    for nombre in sorted(os.listdir(sys.argv[3])):
        ruta = os.path.join(sys.argv[3], nombre)
        if os.path.isfile(os.path.join(ruta, "index.theme")):
            destino = os.path.join(home_icons, nombre)
            if not os.path.exists(destino): os.symlink(ruta, destino)
            EXTRA.append((nombre, nombre + " (candidato)"))
    it = Gtk.IconTheme.new()
hoja(TEMAS[:4], os.path.join(OUT, "comparativa-1.png"))
hoja(TEMAS[4:], os.path.join(OUT, "comparativa-2.png"))
for k in range(0, len(EXTRA), 4):
    hoja(EXTRA[k:k+4], os.path.join(OUT, "comparativa-candidatos-%d.png" % (k // 4 + 1)))
print("listo")