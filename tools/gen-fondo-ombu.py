#!/usr/bin/env python3
"""Fondo de escritorio de Ombú (poliedros oscuro) como archivo VECTORIAL editable.

Genera el SVG maestro con capas (grupos con nombre) y, a partir de él, el PNG que usa el sistema y un PDF.
El mismo SVG se puede abrir en Adobe Illustrator y guardar como .ai.

Uso:  python3 tools/gen-fondo-ombu.py
Salida (assets/wallpapers/):
    ombu-fondo.svg                  maestro editable (capas: fondo, red-de-nodos, poliedros, vineta, velo-inferior, logo-ombu, logo-dte)
    ombu-poliedros-oscuro.png       1920x1080 (escritorio e inicio de sesión)
    ombu-fondo.pdf                  mismo diseño en PDF
    _base-oscuro-limpio.png         fondo sin logos (lo usa el tema de GRUB)
Requiere: numpy, fonttools y rsvg-convert (librsvg2-bin).
"""
import math, os, random, re, subprocess, sys, tempfile
import numpy as np
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "wallpapers")
FONT = os.path.join(ROOT, "assets", "fonts", "EncodeSans[wdth,wght].ttf")
DTE_SVG = os.path.join(ROOT, "assets", "brand", "logo-dte-2026-v2-blanco.svg")

W, H, SS = 1920, 1080, 2            # lienzo; SS: las posiciones aleatorias se calculan al doble (igual que el diseño original)
INDIGO = (40, 30, 110)
DOTS = [(230, 190, 30), (255, 100, 50), (50, 170, 100), (30, 150, 210), (205, 205, 215), (230, 120, 190)]
COLORES_NODOS = DOTS[:4] + [(16, 168, 192)]

# --- Distribución de los logos (se puede ajustar acá o editando el SVG) -----------------------------------------
XMIN_POLIEDROS = 560                # los poliedros no entran en la franja izquierda (íconos del escritorio)
Y_CENTRO_LOGOS = H - 165            # línea central de los logos: queda libre de la barra de tareas
DTE_ANCHO = 700
DTE_MARGEN_DER = 160                # margen de seguridad (en pantallas 16:10 se recortan los costados)
SEPARACION_LOGOS = 190              # espacio entre el logo de Ombú y el de la DTE
OMBU_ESCALA = 0.526                 # tamaño del logo de Ombú (el árbol mide ~100 px de alto)


def rgb(c):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)


def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


# --- Red de nodos -------------------------------------------------------------------------------------------------
def poisson(n, mind, rng, margin):
    pts, tries = [], 0
    while len(pts) < n and tries < n * 400:
        tries += 1
        x, y = rng.uniform(-margin, W * SS + margin), rng.uniform(-margin, H * SS + margin)
        if all((x - a) ** 2 + (y - b) ** 2 >= mind ** 2 for a, b in pts):
            pts.append((x, y))
    return pts


def red_de_nodos(rng, n=90, mind=140, k=3, line_a=42):
    pts = poisson(n, mind * SS, rng, margin=60 * SS)
    lineas, hechos = [], set()
    for i, (x, y) in enumerate(pts):
        cercanos = sorted(range(len(pts)), key=lambda j: (pts[j][0] - x) ** 2 + (pts[j][1] - y) ** 2)[1:k + 1]
        for j in cercanos:
            if (min(i, j), max(i, j)) in hechos:
                continue
            hechos.add((min(i, j), max(i, j)))
            lineas.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (f(x / SS), f(y / SS), f(pts[j][0] / SS), f(pts[j][1] / SS)))
    nodos = []
    for (x, y) in pts:
        r = rng.choice([3, 3, 4, 5, 7])
        c = rng.choice(COLORES_NODOS)
        a = rng.choice([150, 200, 235])
        nodos.append('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s"/>' % (f(x / SS), f(y / SS), r, rgb(c), f(a / 255)))
    return (
        '<g id="red-de-nodos">\n'
        '  <g id="lineas" stroke="#ffffff" stroke-opacity="%s" stroke-width="1" fill="none">\n    %s\n  </g>\n'
        '  <g id="nodos">\n    %s\n  </g>\n</g>' % (f(line_a / 255), "\n    ".join(lineas), "\n    ".join(nodos)))


# --- Poliedros (tetraedros con tres tonos) -------------------------------------------------------------------------
def rot_matrix(rng):
    a, b, c = (rng.uniform(0, 2 * math.pi) for _ in range(3))
    ca, sa, cb, sb, cc, sc = math.cos(a), math.sin(a), math.cos(b), math.sin(b), math.cos(c), math.sin(c)
    rx = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]])
    ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
    rz = np.array([[cc, -sc, 0], [sc, cc, 0], [0, 0, 1]])
    return rz @ ry @ rx


TETRA = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float)
CARAS = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
LUZ = np.array([-0.45, -0.55, 0.7])
LUZ /= np.linalg.norm(LUZ)


def tono(oscuro, claro, t):
    return tuple(int(oscuro[i] + (claro[i] - oscuro[i]) * t) for i in range(3))


def un_poliedro(size, centro, rng, oscuro, claro, alpha, ident):
    r = rot_matrix(rng)
    v = (TETRA @ r.T) * (size / 1.8)
    cx, cy = centro
    caras = []
    for fc in CARAS:
        p = v[list(fc)]
        n = np.cross(p[1] - p[0], p[2] - p[0])
        n /= np.linalg.norm(n)
        if np.dot(n, p.mean(axis=0)) < 0:
            n = -n
        if n[2] <= 0:
            continue
        t = max(0.0, float(np.dot(n, LUZ)))
        caras.append((p[:, 2].mean(), [(cx + q[0], cy + q[1]) for q in p], t))
    polis = []
    for _, poly, t in sorted(caras, key=lambda x: x[0]):
        pts = " ".join("%s,%s" % (f(x / SS), f(y / SS)) for x, y in poly)
        polis.append('<polygon points="%s" fill="%s"/>' % (pts, rgb(tono(oscuro, claro, 0.12 + 0.88 * t))))
    return '<g id="poliedro-%d" fill-opacity="%s">%s</g>' % (ident, f(alpha / 255), "".join(polis))


def poliedros(rng, n, oscuro, claro, smin=70, smax=230, alpha=255, y_max=None, contador=[0]):
    y_max = y_max if y_max is not None else Y_CENTRO_LOGOS - 110      # los poliedros quedan por encima de los logos
    ubicados = []
    for _ in range(n * 120):
        if len(ubicados) >= n:
            break
        s = rng.uniform(smin, smax)
        x, y = rng.uniform(XMIN_POLIEDROS + s * 0.6, W + 40), rng.uniform(0, y_max)
        if y + s * 0.62 > y_max + 40:
            continue
        if all(math.hypot(x - a, y - b) > (s + s2) * 0.62 for a, b, s2 in ubicados):
            ubicados.append((x, y, s))
    salida = []
    for x, y, s in sorted(ubicados, key=lambda p: p[2]):
        j = rng.uniform(-14, 14)
        dk = tuple(max(0, min(255, c + j)) for c in oscuro)
        lt = tuple(max(0, min(255, c + j)) for c in claro)
        contador[0] += 1
        salida.append(un_poliedro(s * SS, (x * SS, y * SS), rng, dk, lt, alpha, contador[0]))
    return salida


# --- Logos --------------------------------------------------------------------------------------------------------
ARBOL = """<g id="arbol" fill="#ffffff">
      <path d="M96 112 C100 140 94 164 82 184 C72 198 56 207 32 210 L86 210 C90 210 94 192 100 192 C106 192 108 210 112 210 L128 210 C132 210 134 192 140 192 C146 192 150 210 154 210 L208 210 C184 207 168 198 158 184 C146 164 140 140 144 112 Z"/>
      <circle cx="52" cy="108" r="30"/><circle cx="82" cy="80" r="38"/><circle cx="120" cy="66" r="46"/>
      <circle cx="160" cy="80" r="38"/><circle cx="190" cy="108" r="30"/><ellipse cx="120" cy="106" rx="100" ry="30"/>
    </g>"""


def palabra_ombu():
    """'Ombú' (Encode Sans ExtraBold) convertida a curvas, con la altura de la O centrada en la altura del árbol."""
    tmp = tempfile.mkdtemp()
    ttf = os.path.join(tmp, "EncodeSans-ExtraBold.ttf")
    subprocess.run([sys.executable, "-m", "fontTools.varLib.instancer", FONT, "wght=800", "wdth=100", "-o", ttf],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    fuente = TTFont(ttf)
    gs, cmap, upm = fuente.getGlyphSet(), fuente.getBestCmap(), fuente["head"].unitsPerEm
    tam = int(240 * 0.62)
    sc = tam / upm
    x, trazos = 0.0, []
    for ch in "Ombú":
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x, 0)))
        trazos.append(pen.getCommands())
        x += gs[g].width * sc
    bp = BoundsPen(gs)
    gs[cmap[ord("O")]].draw(bp)
    _, ymin, _, ymax = bp.bounds
    linea_base = 115 + (ymax + ymin) / 2 * sc         # 115 = centro vertical del árbol (copa a raíces) en el ícono de 240
    return " ".join(trazos), 240 + 19, linea_base, x


def logo_ombu(x_izq_contenido, y_centro, escala):
    letras, x_texto, base, ancho_texto = palabra_ombu()
    tx = x_izq_contenido - 20 * escala              # el contenido del logo empieza en x=20 (borde izquierdo de la copa)
    ty = y_centro - 115 * escala
    ancho = (x_texto + ancho_texto - 20) * escala
    svg = ('<g id="logo-ombu" transform="translate(%s %s) scale(%s)">\n'
           '    %s\n'
           '    <path id="palabra-ombu" fill="#ffffff" transform="translate(%s %s)" d="%s"/>\n'
           '  </g>' % (f(tx), f(ty), f(escala * 1000) if False else "%.4f" % escala, ARBOL, f(x_texto), f(base), letras))
    return svg, ancho


def logo_dte(x, y_centro, ancho):
    txt = open(DTE_SVG, encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', txt).group(1).split()
    vw, vh = float(vb[2]), float(vb[3])
    alto = ancho * vh / vw
    interior = re.search(r"<svg[^>]*>(.*)</svg>", txt, re.S).group(1)
    interior = re.sub(r"<!--.*?-->", "", interior, flags=re.S).strip()
    return ('<svg id="logo-dte" x="%s" y="%s" width="%s" height="%s" viewBox="%s">\n%s\n</svg>'
            % (f(x), f(y_centro - alto / 2), f(ancho), f(alto), " ".join(vb), interior)), alto


# --- Documento ----------------------------------------------------------------------------------------------------
def degradado_fondo():
    angulo = 0.55
    a, b = (1 - angulo) / W, angulo / H
    n = a * a + b * b
    return ('<linearGradient id="degradado-fondo" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="%s" y2="%s">'
            '<stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
            '</linearGradient>' % (f(a / n), f(b / n), rgb((3, 38, 70)), rgb(INDIGO), rgb((150, 30, 120))))


def documento(con_logos=True):
    rng = random.Random(22)
    red = red_de_nodos(rng)
    polis = poliedros(rng, 18, (18, 90, 140), (30, 175, 200), alpha=240)
    polis += poliedros(rng, 6, (130, 30, 110), (229, 60, 140), smin=60, smax=140, alpha=235)

    defs = [degradado_fondo(),
            '<radialGradient id="degradado-vineta" cx="0.5" cy="0.5" r="0.7071">'
            '<stop offset="0.389" stop-color="#000" stop-opacity="0"/><stop offset="0.53" stop-color="#000" stop-opacity="0.025"/>'
            '<stop offset="0.707" stop-color="#000" stop-opacity="0.085"/><stop offset="0.849" stop-color="#000" stop-opacity="0.147"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.225"/></radialGradient>',
            '<linearGradient id="degradado-velo" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="0.25" stop-color="#000" stop-opacity="0.065"/>'
            '<stop offset="0.5" stop-color="#000" stop-opacity="0.17"/><stop offset="0.75" stop-color="#000" stop-opacity="0.30"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.45"/></linearGradient>']
    capas = ['<rect id="fondo" width="%d" height="%d" fill="url(#degradado-fondo)"/>' % (W, H),
             red,
             '<g id="poliedros">\n  %s\n</g>' % "\n  ".join(polis),
             '<rect id="vineta" width="%d" height="%d" fill="url(#degradado-vineta)"/>' % (W, H)]
    if con_logos:
        capas.append('<rect id="velo-inferior" x="0" y="%d" width="%d" height="200" fill="url(#degradado-velo)"/>' % (H - 200, W))
        dte_x = W - DTE_MARGEN_DER - DTE_ANCHO
        dte, _ = logo_dte(dte_x, Y_CENTRO_LOGOS, DTE_ANCHO)
        _, ancho_ombu = logo_ombu(0, 0, OMBU_ESCALA)
        x_ombu = dte_x - SEPARACION_LOGOS - ancho_ombu
        ombu, _ = logo_ombu(x_ombu, Y_CENTRO_LOGOS, OMBU_ESCALA)
        capas += [ombu, dte]
        print("Logo de Ombú: x=%d..%d | logo DTE: x=%d..%d | centro y=%d" % (x_ombu, x_ombu + ancho_ombu, dte_x, dte_x + DTE_ANCHO, Y_CENTRO_LOGOS))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n'
            '<title>Fondo de escritorio de Ombú</title>\n<defs>\n%s\n</defs>\n%s\n</svg>\n'
            % (W, H, W, H, "\n".join(defs), "\n".join(capas)))


def rasterizar(svg, png=None, pdf=None):
    if png:
        subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), svg, "-o", png], check=True)
    if pdf:
        subprocess.run(["rsvg-convert", "-f", "pdf", svg, "-o", pdf], check=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    maestro = os.path.join(OUT, "ombu-fondo.svg")
    open(maestro, "w", encoding="utf-8").write(documento(True))
    rasterizar(maestro, os.path.join(OUT, "ombu-poliedros-oscuro.png"), os.path.join(OUT, "ombu-fondo.pdf"))
    limpio = os.path.join(OUT, "_base-oscuro-limpio.svg")
    open(limpio, "w", encoding="utf-8").write(documento(False))
    rasterizar(limpio, os.path.join(OUT, "_base-oscuro-limpio.png"))
    os.remove(limpio)
    for n in ("ombu-fondo.svg", "ombu-poliedros-oscuro.png", "ombu-fondo.pdf", "_base-oscuro-limpio.png"):
        print("  ->", os.path.join("assets", "wallpapers", n), os.path.getsize(os.path.join(OUT, n)), "bytes")


if __name__ == "__main__":
    sys.exit(main())
