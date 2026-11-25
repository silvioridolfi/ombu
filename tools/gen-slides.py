#!/usr/bin/env python3
"""
Diapositivas del instalador de Ombú (Calamares): 13 diapositivas con la identidad visual de la DTE y datos de la provincia de Buenos Aires.

Usa los mismos recursos que tools/gen-assets.py (degradé, silueta del ombú, logo DTE, Encode Sans).
Uso:  python3 tools/gen-slides.py [carpeta_de_salida]
Por defecto escribe slide1.png ... slide13.png en config/includes.chroot/etc/calamares/branding/ombu/
y regenera show.qml con la cantidad de diapositivas.

Los datos curiosos fueron verificados: 135 municipios y 25 regiones educativas (Documento marco DTE 2025-2027), La Plata fundada el
19/11/1882 por Dardo Rocha (planificada, con diagonales), Censo 2022 (17,5 millones), Cerro Tres Picos 1.239 m (punto más alto de la
provincia), Juan Vucetich (policía bonaerense) y el caso de Necochea de 1892.
"""
import importlib.util
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ga", os.path.join(AQUI, "gen-assets.py"))
ga = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ga)

ROOT = ga.ROOT
SW, SH, MX = ga.SW, ga.SH, ga.MX
WHITE, PINK = ga.WHITE, ga.PINK
DESTINO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "config", "includes.chroot", "etc", "calamares", "branding", "ombu")
os.makedirs(DESTINO, exist_ok=True)

BLANCO_SUAVE = (255, 255, 255, 242)


def lineas(d, x, y, textos, tam=25, paso=40, peso=500):
    for t in textos:
        d.text((x, y), t, font=ga.font(tam, peso), fill=BLANCO_SUAVE)
        y += paso
    return y


def logo_dte(im):
    dl = ga.dte_white(380)
    im.alpha_composite(dl, (SW - dl.width - 36, SH - dl.height - 18))


def guardar(im, n):
    p = os.path.join(DESTINO, "slide%d.png" % n)
    im.convert("RGB").save(p, optimize=True)
    print("  ->", p)


def base():
    return ga.slide_fondo()


# ---- Diseño A: ícono del ombú + título + texto (el original) ----
def diseno_a(n, titulo, texto):
    im = base(); d = ImageDraw.Draw(im)
    im.alpha_composite(ga.icon_white(112), (MX, 44))
    tx = MX + 142
    d.text((tx, 46), titulo[0], font=ga.font(42, 800), fill=WHITE)
    if len(titulo) > 1:
        d.text((tx, 98), titulo[1], font=ga.font(42, 800), fill=WHITE)
    lineas(d, MX, 184, texto)
    logo_dte(im); guardar(im, n)


# ---- Diseño B: número grande ----
def diseno_b(n, numero, unidad, titulo, texto):
    im = base(); d = ImageDraw.Draw(im)
    d.text((MX - 6, 18), numero, font=ga.font(200, 800), fill=WHITE)
    ancho = d.textbbox((0, 0), numero, font=ga.font(200, 800))[2]
    d.text((MX + 2, 232), unidad, font=ga.font(34, 700), fill=(255, 255, 255, 235))
    x = max(MX + ancho + 40, 470)
    d.text((x, 44), titulo[0], font=ga.font(38, 800), fill=WHITE)
    if len(titulo) > 1:
        d.text((x, 90), titulo[1], font=ga.font(38, 800), fill=WHITE)
    lineas(d, x, 160, texto, tam=23, paso=36)
    logo_dte(im); guardar(im, n)


# ---- Diseño C: trazado de La Plata (cuadrícula con diagonales) ----
def diseno_c(n, titulo, texto):
    im = base()
    arte = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); a = ImageDraw.Draw(arte)
    x0, y0, lado = 660, 16, 252
    paso = lado // 8
    for i in range(9):
        a.line((x0 + i * paso, y0, x0 + i * paso, y0 + lado), fill=(255, 255, 255, 120), width=2)
        a.line((x0, y0 + i * paso, x0 + lado, y0 + i * paso), fill=(255, 255, 255, 120), width=2)
    for (p, q) in (((0, 0), (8, 8)), ((8, 0), (0, 8)), ((0, 4), (4, 0)), ((4, 8), (8, 4)), ((0, 4), (4, 8)), ((4, 0), (8, 4))):
        a.line((x0 + p[0] * paso, y0 + p[1] * paso, x0 + q[0] * paso, y0 + q[1] * paso), fill=(255, 255, 255, 235), width=4)
    for (px, py) in ((4, 4), (2, 2), (6, 2), (2, 6), (6, 6)):
        r = 9 if (px, py) == (4, 4) else 6
        cx, cy = x0 + px * paso, y0 + py * paso
        a.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))
    im.alpha_composite(arte)
    d = ImageDraw.Draw(im)
    d.text((MX, 40), titulo[0], font=ga.font(42, 800), fill=WHITE)
    if len(titulo) > 1:
        d.text((MX, 92), titulo[1], font=ga.font(42, 800), fill=WHITE)
    lineas(d, MX, 170, texto, tam=24, paso=38)
    logo_dte(im); guardar(im, n)


# ---- Diseño D: sierra con la altura marcada (Tres Picos) ----
def diseno_d(n, titulo, texto, altura):
    im = base()
    arte = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); a = ImageDraw.Draw(arte)
    base_y = SH - 112
    cumbres = [(560, base_y), (640, 214), (700, 250), (790, 110), (860, 226), (905, 190), (1000, base_y)]
    a.polygon(cumbres, fill=(255, 255, 255, 70))
    a.line(cumbres, fill=(255, 255, 255, 235), width=4, joint="curve")
    a.line((790, 70, 790, 110), fill=(255, 255, 255, 235), width=3)
    a.ellipse((783, 103, 797, 117), fill=(255, 255, 255, 255))
    a.line((560, base_y, 1000, base_y), fill=(255, 255, 255, 160), width=2)
    im.alpha_composite(arte)
    d = ImageDraw.Draw(im)
    d.text((790, 36), altura, font=ga.font(34, 800), fill=WHITE, anchor="ma")
    d.text((MX, 40), titulo[0], font=ga.font(42, 800), fill=WHITE)
    if len(titulo) > 1:
        d.text((MX, 92), titulo[1], font=ga.font(42, 800), fill=WHITE)
    lineas(d, MX, 170, texto, tam=24, paso=38)
    logo_dte(im); guardar(im, n)


# ---- Diseño E: huella dactilar (curvas concéntricas) ----
def diseno_e(n, titulo, texto):
    im = base()
    arte = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); a = ImageDraw.Draw(arte)
    cx, cy = 810, 132
    for i, r in enumerate(range(14, 122, 12)):
        caja = (cx - r * 0.78, cy - r, cx + r * 0.78, cy + r)
        a.arc(caja, start=200 + (i % 3) * 6, end=340 - (i % 2) * 14, fill=(255, 255, 255, 215), width=4)
        a.arc(caja, start=18 + (i % 2) * 8, end=165 - (i % 3) * 8, fill=(255, 255, 255, 215), width=4)
    im.alpha_composite(arte)
    d = ImageDraw.Draw(im)
    d.text((MX, 34), titulo[0], font=ga.font(42, 800), fill=WHITE)
    if len(titulo) > 1:
        d.text((MX, 86), titulo[1], font=ga.font(42, 800), fill=WHITE)
    lineas(d, MX, 160, texto, tam=24, paso=38)
    logo_dte(im); guardar(im, n)


# ---- Diseño F: una línea de trabajo de la DTE ----
def diseno_f(n, titulo, texto, en_ombu):
    im = base(); d = ImageDraw.Draw(im)
    etiqueta = "Línea de trabajo de la DTE"
    f = ga.font(20, 700)
    w = d.textbbox((0, 0), etiqueta, font=f)[2]
    d.rounded_rectangle((MX, 30, MX + w + 36, 66), radius=18, fill=PINK)
    d.text((MX + 18, 48), etiqueta, font=f, fill=WHITE, anchor="lm")
    d.text((MX, 86), titulo, font=ga.font(42, 800), fill=WHITE)
    y = lineas(d, MX, 156, texto, tam=24, paso=36)
    d.rounded_rectangle((MX, y + 10, MX + 6, y + 10 + 38 * len(en_ombu) - 4), radius=3, fill=WHITE)
    lineas(d, MX + 22, y + 8, en_ombu, tam=23, paso=36, peso=700)
    logo_dte(im); guardar(im, n)


QML = """import QtQuick 2.0;
import calamares.slideshow 1.0;

// Las diapositivas (1000x380) llenan todo el espacio de la presentación; si el área tiene otra proporción se recortan
// por los costados (el contenido está dentro de un margen seguro). Generado por tools/gen-slides.py.
Presentation
{
    id: presentation

    Timer {
        interval: 15000
        repeat: true
        running: true
        onTriggered: presentation.goToNextSlide()
    }

%s
}
"""


def escribir_qml(cantidad):
    filas = "\n".join('    Slide { Image { anchors.fill: parent; source: "slide%d.png"; fillMode: Image.PreserveAspectCrop } }' % i
                      for i in range(1, cantidad + 1))
    with open(os.path.join(DESTINO, "show.qml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(QML % filas)
    print("  -> show.qml (%d diapositivas)" % cantidad)


def main():
    print("Diapositivas del instalador")
    diseno_a(1, ("Te damos la", "bienvenida a Ombú"),
             ["El resto de la instalación es automática.", "Tarda unos minutos: es un buen momento", "para tomar unos mates."])
    diseno_a(2, ("Todo para aprender", "ya viene incluido"),
             ["Scratch (TurboWarp), GCompris, Tux Paint,", "LibreOffice, Audacity, Tux Typing,", "Tux Math, Firefox y Chromium."])
    diseno_a(3, ("Software libre y", "soberanía digital"),
             ["Ombú no envía datos de uso a nadie.", "Es software libre pensado desde el", "territorio para las escuelas de la provincia."])
    diseno_b(4, "135", "municipios", ("Una provincia,", "25 regiones educativas"),
             ["La provincia de Buenos Aires se organiza en", "135 municipios, y su educación, en 25", "regiones educativas."])
    diseno_c(5, ("La ciudad de", "las diagonales"),
             ["La Plata, capital bonaerense, se fundó el", "19 de noviembre de 1882 y se planificó", "con calles en cuadrícula y diagonales."])
    diseno_b(6, "17,5", "millones", ("La provincia más", "poblada del país"),
             ["Según el Censo 2022, en la provincia de", "Buenos Aires viven 17,5 millones de personas."])
    diseno_d(7, ("El techo", "bonaerense"),
             ["El cerro Tres Picos, en las sierras de la", "Ventana, es el punto más alto de la provincia:", "1.239 metros sobre el nivel del mar."], "1.239 m")
    diseno_e(8, ("Huellas con", "historia"),
             ["Juan Vucetich, de la policía bonaerense, creó", "un sistema para identificar personas por sus", "huellas dactilares. En 1892, en Necochea, se", "usó por primera vez para resolver un caso."])
    diseno_f(9, "Clubes de Tecnología",
             ["Programación, robótica, pensamiento computacional", "e inteligencia artificial, jugando y en equipo."],
             ["En Ombú: Scratch (TurboWarp),", "Pilas Bloques y KTurtle."])
    diseno_f(10, "Medios Escolares Bonaerenses",
             ["Radios, videos y proyectos de comunicación", "hechos por y para la comunidad educativa."],
             ["En Ombú: Audacity para grabar", "y editar audio."])
    diseno_f(11, "Continuemos Estudiando",
             ["El portal educativo de la provincia: propuestas", "de enseñanza y recursos para toda la comunidad."],
             ["En Ombú: tenés el acceso directo", "en el escritorio."])
    diseno_f(12, "Equipos que vuelven al aula",
             ["La DTE impulsa recuperar el equipamiento", "tecnológico de las escuelas para su uso pedagógico."],
             ["Ombú le da nueva vida a las", "netbooks de la escuela."])
    ga.OUT = DESTINO   # slide_creditos() guarda en OUT/calamares/slide4.png: se redirige y se renombra
    ga.slide_creditos()
    os.replace(os.path.join(DESTINO, "calamares", "slide4.png"), os.path.join(DESTINO, "slide13.png"))
    os.rmdir(os.path.join(DESTINO, "calamares"))
    print("  -> slide13.png (créditos)")
    escribir_qml(13)


if __name__ == "__main__":
    main()
