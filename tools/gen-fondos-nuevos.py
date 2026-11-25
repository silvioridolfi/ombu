#!/usr/bin/env python3
"""Cuatro fondos de escritorio nuevos para Ombú (propuesta), inspirados en las referencias que pasó Silvio pero con diseño propio.

  ombu-7-burbujas.png        esfera de red y burbujas con los dibujos de los programas (violeta a magenta)
  ombu-8-mosaico.png         mosaico de chips de Ombú sobre degradé turquesa
  ombu-9-arbol-de-puntos.png el ombú dibujado con puntos de trama (semitono) sobre azul noche
  ombu-10-red-de-colores.png red de nodos de colores sobre índigo, con el ombú de fondo

Sin logos de ninguna institución. Los íconos del escritorio tienen letras blancas: por eso los fondos son de tonos medios u
oscuros (un fondo blanco como el de las referencias dejaría los nombres ilegibles) y la franja izquierda queda calma.

Uso:  python3 tools/gen-fondos-nuevos.py          Salida: assets/wallpapers/nuevos-propuesta/
Requiere: numpy, Pillow y rsvg-convert (librsvg2-bin).
"""
import importlib.util, math, os, random, subprocess, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "wallpapers", "nuevos-propuesta")
W, H = 1920, 1080


def cargar(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(ROOT, "tools", archivo))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


fondo = cargar("gf", "gen-fondo-ombu.py")          # ARBOL, poliedros, rgb
iconos = cargar("gi", "gen-icon-theme.py")         # los dibujos (glifos 24x24) de los programas

TURQUESA = (16, 168, 192)
MAGENTA = (229, 60, 140)
AMBAR = (245, 166, 35)
VIOLETA = (124, 64, 184)
AZUL = (30, 110, 190)
NARANJA = (240, 96, 60)
VERDE = (50, 170, 100)
PALETA = [TURQUESA, MAGENTA, AMBAR, VIOLETA, AZUL, NARANJA, VERDE]
GLIFOS = ["BIRRETE", "CODIGO", "NOTA_MUSICAL", "MATRAZ", "LIBRO", "PALETA", "GLOBO", "ATOMO", "ESTRELLA", "CALCULADORA",
          "ROBOT", "COHETE", "LAPIZ", "CAMARA", "ABACO", "TEXTO"]
rgb = fondo.rgb


def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def glifo(nombre, cx, cy, tam, color="#ffffff", grosor=1.6, relleno_bg="#000000"):
    g = getattr(iconos, nombre).replace("{c}", color).replace("{bg}", relleno_bg)
    k = tam / 24.0
    return ('<g transform="translate(%s %s) scale(%s)" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round">%s</g>' % (f(cx - tam / 2), f(cy - tam / 2), "%.4f" % k, color, grosor, g))


def svg(titulo, defs, cuerpo):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n'
            '<title>%s</title>\n<defs>\n%s\n</defs>\n%s\n</svg>\n' % (W, H, W, H, titulo, defs, cuerpo))


def degradado(id_, c0, c1, c2=None, x2=1, y2=1):
    paradas = '<stop offset="0" stop-color="%s"/>' % rgb(c0)
    if c2:
        paradas += '<stop offset="0.5" stop-color="%s"/>' % rgb(c1)
        paradas += '<stop offset="1" stop-color="%s"/>' % rgb(c2)
    else:
        paradas += '<stop offset="1" stop-color="%s"/>' % rgb(c1)
    return '<linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s">%s</linearGradient>' % (id_, x2, y2, paradas)


def vineta():
    return ('<radialGradient id="vineta" cx="0.5" cy="0.5" r="0.72"><stop offset="0.45" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.28"/></radialGradient>')


# ---------------------------------------------------------------------------------------------------- 7. Burbujas
def esfera(rng, cx, cy, r):
    """Esfera de red (meridianos y paralelos) con nodos."""
    lin = []
    lin.append('<circle cx="%s" cy="%s" r="%s"/>' % (f(cx), f(cy), f(r)))
    for lon in range(0, 180, 22):
        rx = abs(r * math.cos(math.radians(lon)))
        if rx > 1:
            lin.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s"/>' % (f(cx), f(cy), f(rx), f(r)))
    for lat in range(-72, 90, 24):
        rr = r * math.cos(math.radians(lat))
        y = cy + r * math.sin(math.radians(lat))
        lin.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s"/>' % (f(cx), f(y), f(rr), f(rr * 0.18)))
    nodos = []
    for _ in range(70):
        a, b = rng.uniform(0, 2 * math.pi), rng.uniform(-1.2, 1.2)
        x, y = cx + r * math.cos(b) * math.sin(a), cy + r * math.sin(b)
        if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
            nodos.append('<circle cx="%s" cy="%s" r="%s" fill="#fff" fill-opacity="%s"/>' % (f(x), f(y), rng.choice([2, 3, 4]), f(rng.uniform(.25, .6))))
    return ('<g id="esfera" stroke="#fff" stroke-opacity=".17" stroke-width="1.4" fill="none">%s</g><g id="nodos">%s</g>'
            % ("".join(lin), "".join(nodos)))


def fondo_burbujas():
    rng = random.Random(7)
    defs = [degradado("fondo", (58, 24, 118), (118, 40, 140), (160, 38, 128), 1, 0.8), vineta(),
            '<radialGradient id="brillo" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#fff" stop-opacity="0.38"/>'
            '<stop offset="0.6" stop-color="#fff" stop-opacity="0"/></radialGradient>',
            '<radialGradient id="halo" cx="0.62" cy="0.5" r="0.55"><stop offset="0" stop-color="#ff7ac6" stop-opacity="0.35"/>'
            '<stop offset="1" stop-color="#ff7ac6" stop-opacity="0"/></radialGradient>']
    capas = ['<rect width="%d" height="%d" fill="url(#fondo)"/>' % (W, H),
             '<rect width="%d" height="%d" fill="url(#halo)"/>' % (W, H),
             esfera(rng, 1170, 520, 470)]
    # (x, y, radio) de las burbujas: concentradas a la derecha del centro; la franja izquierda queda libre
    puestos = [(1010, 330, 92), (1380, 215, 84), (1520, 560, 76), (1180, 700, 98), (860, 560, 70), (1290, 450, 44), (1010, 520, 34),
               (1640, 330, 38), (780, 330, 32), (1460, 800, 36), (940, 790, 30), (1700, 690, 30), (1120, 190, 28), (1380, 640, 28)]
    ids = rng.sample(GLIFOS, len(puestos))
    for i, ((x, y, r), nombre) in enumerate(zip(puestos, ids)):
        col = PALETA[i % len(PALETA)]
        capas.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/><circle cx="%d" cy="%d" r="%d" fill="url(#brillo)"/>'
                     % (x, y, r, rgb(col), x, y, r))
        capas.append(glifo(ids[i], x, y, r * 1.05, grosor=1.5 if r > 60 else 1.8))
    capas.append('<rect width="%d" height="%d" fill="url(#vineta)"/>' % (W, H))
    return svg("Ombú — burbujas", "\n".join(defs), "\n".join(capas))


# ---------------------------------------------------------------------------------------------------- 8. Mosaico
CHIP = "M10 4h38l12 12v38a6 6 0 0 1-6 6H16L4 48V10a6 6 0 0 1 6-6z"          # la forma del chip de los íconos de Ombú


def chip(x, y, lado, relleno, op=1.0, borde=None):
    k = lado / 64.0
    ex = ' stroke="%s" stroke-width="%s"' % (borde, f(2 / k)) if borde else ""
    return '<path transform="translate(%s %s) scale(%s)" d="%s" fill="%s" fill-opacity="%s"%s/>' % (f(x), f(y), "%.4f" % k, CHIP, relleno, f(op), ex)


def fondo_mosaico():
    rng = random.Random(8)
    defs = [degradado("fondo", (0, 82, 120), (10, 140, 168), (60, 190, 196), 1, 0.9), vineta(),
            '<radialGradient id="brillo" cx="0.4" cy="0.3" r="0.9"><stop offset="0" stop-color="#fff" stop-opacity="0.32"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>']
    capas = ['<rect width="%d" height="%d" fill="url(#fondo)"/>' % (W, H)]
    celda, sep = 124, 16
    x0, y0 = 640, 52
    cols, filas = 10, 8
    ocupado = set()
    destacados = []                                   # (col, fila, tamaño en celdas, color, glifo)
    nombres = rng.sample(GLIFOS, 9)
    base = [(2, 0, 2), (6, 1, 1), (4, 2, 2), (7, 3, 2), (1, 4, 1), (3, 5, 2), (6, 5, 1), (8, 6, 1), (0, 6, 1)]
    for i, (c, r, t) in enumerate(base):
        destacados.append((c, r, t, PALETA[(i * 3) % len(PALETA)], nombres[i]))
        for dc in range(t):
            for dr in range(t):
                ocupado.add((c + dc, r + dr))
    for r in range(filas):
        for c in range(cols):
            if (c, r) in ocupado:
                continue
            a = rng.choice([0.05, 0.07, 0.1, 0.13, 0.0, 0.0])
            if a > 0:
                capas.append(chip(x0 + c * (celda + sep), y0 + r * (celda + sep), celda, "#ffffff", a))
    for c, r, t, col, nombre in destacados:
        lado = celda * t + sep * (t - 1)
        x, y = x0 + c * (celda + sep), y0 + r * (celda + sep)
        capas.append(chip(x, y, lado, rgb(col)))
        capas.append(chip(x, y, lado, "url(#brillo)"))
        capas.append(glifo(nombre, x + lado / 2, y + lado / 2, lado * 0.52, grosor=1.7))
    capas.append('<rect width="%d" height="%d" fill="url(#vineta)"/>' % (W, H))
    return svg("Ombú — mosaico", "\n".join(defs), "\n".join(capas))


# ---------------------------------------------------------------------------------------------------- 9. Árbol de puntos
def mascara_arbol(alto):
    """Silueta del ombú (la del logo) rasterizada: devuelve una matriz con la cobertura de 0 a 1."""
    ancho = int(alto * 240 / 230)
    s = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 240 230">'
         '<g transform="translate(0 -14)">%s</g></svg>' % (ancho, alto, fondo.ARBOL))
    ruta = os.path.join(OUT, "_arbol.svg")
    open(ruta, "w").write(s)
    png = os.path.join(OUT, "_arbol.png")
    subprocess.run(["rsvg-convert", "-w", str(ancho), "-h", str(alto), ruta, "-o", png], check=True)
    a = np.array(Image.open(png).convert("RGBA"))[:, :, 3] / 255.0
    os.remove(ruta)
    os.remove(png)
    return a


def fondo_puntos():
    rng = random.Random(9)
    defs = [degradado("fondo", (10, 10, 44), (30, 18, 84), (66, 20, 104), 1, 0.9), vineta(),
            '<radialGradient id="luz" cx="0.68" cy="0.5" r="0.5"><stop offset="0" stop-color="#2dd4ee" stop-opacity="0.22"/>'
            '<stop offset="1" stop-color="#2dd4ee" stop-opacity="0"/></radialGradient>']
    capas = ['<rect width="%d" height="%d" fill="url(#fondo)"/>' % (W, H), '<rect width="%d" height="%d" fill="url(#luz)"/>' % (W, H)]
    paso = 17
    alto = 840
    m = mascara_arbol(alto)
    ox, oy = 1340 - m.shape[1] // 2, 540 - alto // 2
    puntos = []
    # trama de fondo: puntos chicos que se desvanecen hacia la izquierda (la franja de íconos queda limpia)
    for y in range(paso // 2, H, paso):
        for x in range(paso // 2, W, paso):
            t = max(0.0, (x - 520) / (W - 520))
            r = 0.9 + 1.7 * t * (0.6 + 0.4 * math.sin(y / 140.0))
            if t > 0.02:
                puntos.append('<circle cx="%d" cy="%d" r="%s" fill="#ffffff" fill-opacity="%s"/>' % (x, y, f(r), f(0.05 + 0.08 * t)))
    capas.append('<g id="trama">%s</g>' % "".join(puntos))
    # el árbol, con puntos más grandes donde hay silueta (semitono) y degradé turquesa a magenta de abajo hacia arriba
    arbol = []
    for y in range(oy, oy + m.shape[0], paso):
        for x in range(ox, ox + m.shape[1], paso):
            yy, xx = y - oy, x - ox
            if yy >= m.shape[0] or xx >= m.shape[1]:
                continue
            cov = float(m[yy:yy + paso, xx:xx + paso].mean())
            if cov < 0.08:
                continue
            r = 1.2 + 6.6 * cov
            u = yy / m.shape[0]
            col = tuple(TURQUESA[i] + (MAGENTA[i] - TURQUESA[i]) * max(0.0, (0.55 - u)) / 0.55 * 0.9 for i in range(3)) if u < 0.55 else TURQUESA
            col = tuple(min(255, c + 30 * cov) for c in col)
            arbol.append('<circle cx="%d" cy="%d" r="%s" fill="%s"/>' % (x + paso // 2, y + paso // 2, f(r), rgb(col)))
    capas.append('<g id="arbol-de-puntos">%s</g>' % "".join(arbol))
    # unos pocos poliedros chicos para atar con el resto de la familia de fondos
    # posiciones elegidas a mano, fuera de la silueta del árbol
    colocados = [(1800, 190, 100, "a"), (1840, 640, 110, "a"), (1700, 900, 70, "m"), (860, 880, 90, "a"), (940, 150, 70, "m"), (1790, 420, 60, "m")]
    polis = []
    for i, (x, y, tam, tipo) in enumerate(colocados):
        osc, cla = ((18, 90, 140), (30, 175, 200)) if tipo == "a" else ((130, 30, 110), (229, 60, 140))
        polis.append(fondo.un_poliedro(tam * fondo.SS, (x * fondo.SS, y * fondo.SS), rng, osc, cla, 230, 200 + i))
    capas.append('<g id="poliedros">%s</g>' % "".join(polis))
    capas.append('<rect width="%d" height="%d" fill="url(#vineta)"/>' % (W, H))
    return svg("Ombú — árbol de puntos", "\n".join(defs), "\n".join(capas))


# ---------------------------------------------------------------------------------------------------- 10. Red de colores
def fondo_red():
    rng = random.Random(10)
    defs = [degradado("fondo", (18, 14, 66), (34, 24, 100), (70, 28, 112), 1, 0.9), vineta(),
            '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff" stop-opacity="0.5"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>']
    capas = ['<rect width="%d" height="%d" fill="url(#fondo)"/>' % (W, H)]
    # el ombú grande y muy suave, de fondo
    capas.append('<g transform="translate(1180 120) scale(3.6)" opacity=".07">%s</g>' % fondo.ARBOL)
    pts = []
    for _ in range(4000):
        if len(pts) >= 120:
            break
        x, y = rng.uniform(560, W + 40), rng.uniform(-30, H + 30)
        if all((x - a) ** 2 + (y - b) ** 2 >= 118 ** 2 for a, b, _ in pts):
            pts.append((x, y, rng.choice([5, 6, 8, 10, 14, 18])))
    lineas, hechos = [], set()
    for i, (x, y, _) in enumerate(pts):
        cerca = sorted(range(len(pts)), key=lambda j: (pts[j][0] - x) ** 2 + (pts[j][1] - y) ** 2)[1:4]
        for j in cerca:
            if (min(i, j), max(i, j)) in hechos:
                continue
            hechos.add((min(i, j), max(i, j)))
            lineas.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (f(x), f(y), f(pts[j][0]), f(pts[j][1])))
    capas.append('<g stroke="#cfd4ff" stroke-opacity=".26" stroke-width="1.6">%s</g>' % "".join(lineas))
    nodos = []
    for x, y, r in pts:
        col = rng.choice(PALETA)
        if r >= 12:
            nodos.append('<circle cx="%s" cy="%s" r="%s" fill="url(#glow)" opacity=".22"/>' % (f(x), f(y), r * 3))
        nodos.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x), f(y), r, rgb(col)))
    capas.append('<g>%s</g>' % "".join(nodos))
    capas.append('<rect width="%d" height="%d" fill="url(#vineta)"/>' % (W, H))
    return svg("Ombú — red de colores", "\n".join(defs), "\n".join(capas))


def main():
    os.makedirs(OUT, exist_ok=True)
    for nombre, fn in (("ombu-7-burbujas", fondo_burbujas), ("ombu-8-mosaico", fondo_mosaico),
                       ("ombu-9-arbol-de-puntos", fondo_puntos), ("ombu-10-red-de-colores", fondo_red)):
        ruta = os.path.join(OUT, nombre + ".svg")
        open(ruta, "w", encoding="utf-8").write(fn())
        subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), ruta, "-o", os.path.join(OUT, nombre + ".png")], check=True)
        print("  ->", os.path.join("assets", "wallpapers", "nuevos-propuesta", nombre + ".png"), os.path.getsize(os.path.join(OUT, nombre + ".png")), "bytes")


if __name__ == "__main__":
    sys.exit(main())
