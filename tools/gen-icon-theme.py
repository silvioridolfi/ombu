#!/usr/bin/env python3
"""Generador oficial del tema de íconos "Ombu" de Ombú: estilo Chip con dibujos propios.

Estilo: placa oscura con dos esquinas cortadas, borde de color y tres "pines" de circuito, con un dibujo de línea
(grilla de 24 x 24, trazo redondeado, relleno suave de acento). Todo plano, sin degradados ni sombras.
- apps, lugares, dispositivos y tipos de archivo: placa + dibujo
- carpetas: forma de carpeta propia con el mismo borde de color
- categorías del menú y acciones (apagar, reiniciar...): solo el dibujo, sin placa, para que se lea a 16-24 px

No necesita internet ni otros archivos: los colores y los dibujos están acá. Lo que no se define acá se ve con Papirus.

Uso:  python3 tools/gen-icon-theme.py [carpeta_de_salida] [grosor_del_trazo]
Por defecto escribe en config/includes.chroot/usr/share/icons/Ombu con trazo fino (1.7).
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "config", "includes.chroot", "usr", "share", "icons", "Ombu")
TRAZO = float(sys.argv[2]) if len(sys.argv) > 2 else 1.7

NAVY = "#1b1843"
TURQUESA, AZUL, VIOLETA, MAGENTA, VERDE, NARANJA = "#10a8c0", "#2d7fd1", "#7b5bd6", "#d6358a", "#2fa36b", "#e0852b"
AMBAR, ROJO, GRIS = "#e8a321", "#e5484d", "#a9b6cc"          # GRIS ya es el claro que se ve sobre la placa oscura
# {c} = color de acento (relleno suave o puntos). {bg} = color de la placa. Trazo y color de línea los pone el contenedor.
F = 'fill="{c}" fill-opacity=".22"'          # relleno suave
S = 'fill="{c}" stroke="none"'               # relleno sólido de acento, sin borde

NAVEGADOR = f'''<path d="M3.2 3.8L8.9 7.6C10.9 7 13.1 7 15.1 7.6L20.8 3.8L21.2 11.5L12 21L2.8 11.5Z" {F}/>
<path d="M7 12.4l2.8 1.4M17 12.4l-2.8 1.4"/><path d="M10.4 17.4h3.2l-1.6 1.8z" {S}/><path d="M12 7.4v3"/>'''
TEXTO = f'''<path d="M7 3h7l4.5 4.5V19a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/>
<path d="M14 3v4.5h4.5" {F}/><path d="M8.5 12h7M8.5 15h7M8.5 18h4"/>'''
PLANILLA = f'''<rect x="3.5" y="3.5" width="17" height="17" rx="2.5"/><rect x="10" y="9" width="10.5" height="5.5" {S} fill-opacity=".3"/>
<path d="M3.5 9h17M3.5 14.5h17M10 3.5v17"/>'''
PRESENTACION = f'''<rect x="3" y="4" width="18" height="11.5" rx="2"/><path d="M12 15.5V20M8 20.5h8"/>
<path d="M6.5 12.5l3.2-3.4 2.8 2.2 4.8-4.4"/><circle cx="17.3" cy="6.9" r="1.3" {S}/>'''
COHETE = f'''<path d="M12 2.8c3 2.1 4.4 5.2 4.2 9l-1.7 2.4h-5l-1.7-2.4c-.2-3.8 1.2-6.9 4.2-9z" {F}/><circle cx="12" cy="9.3" r="1.7"/>
<path d="M7.6 12.3L5 15.3l2.6.9M16.4 12.3l2.6 3-2.6.9"/><path d="M10 18c.1 1.5.8 2.6 2 3.4 1.2-.8 1.9-1.9 2-3.4"/>'''
BLOQUES = f'''<path d="M5.2 9.6L5.4 3.8L10 6.4C11.3 6.1 12.7 6.1 14 6.4L18.6 3.8L18.8 9.6C20 10.8 20.5 12.1 20.5 13.6C20.5 17.7 16.8 20.7 12 20.7C7.2 20.7 3.5 17.7 3.5 13.6C3.5 12.1 4 10.8 5.2 9.6Z" {F}/>
<circle cx="9" cy="12.6" r="1.1" {S}/><circle cx="15" cy="12.6" r="1.1" {S}/><path d="M11 15h2l-1 1.2z" {S}/>
<path d="M9.4 17.4c1.5 1.1 3.7 1.1 5.2 0"/>'''
ROBOT = f'''<rect x="5" y="8" width="14" height="11.5" rx="3.2" {F}/><path d="M12 8V5.2"/><circle cx="12" cy="3.9" r="1.1"/>
<circle cx="9.4" cy="13" r="1.2" {S}/><circle cx="14.6" cy="13" r="1.2" {S}/><path d="M9.5 16.6h5M3 12v3.5M21 12v3.5"/>'''
ABACO = f'''<path d="M5 4.5h14M5 19.5h14M5 4.5v15M19 4.5v15"/><path d="M8.7 4.5v15M12.2 4.5v15M15.7 4.5v15"/>
<circle cx="8.7" cy="8" r="1.7" {S}/><circle cx="8.7" cy="11.6" r="1.7" {S}/><circle cx="12.2" cy="10" r="1.7" {S}/>
<circle cx="15.7" cy="14" r="1.7" {S}/><circle cx="15.7" cy="17" r="1.7" {S}/><circle cx="12.2" cy="16" r="1.7" {S}/>'''
PALETA = f'''<path d="M12 3.5a8.5 8.5 0 1 0 0 17c1.3 0 2-.9 2-1.9 0-1.4-1.3-1.6-1.3-2.7 0-.9.7-1.5 1.6-1.5H17a3.5 3.5 0 0 0 3.5-3.5C20.5 7 16.8 3.5 12 3.5z" {F}/>
<circle cx="7.8" cy="11" r="1.1" {S}/><circle cx="10.6" cy="7.3" r="1.1" {S}/><circle cx="15" cy="7.8" r="1.1" {S}/>'''
CALCULADORA = f'''<rect x="5" y="3" width="14" height="18" rx="2.5"/><rect x="8" y="6" width="8" height="3.5" rx=".8" {F}/>
<path d="M8.5 13h2M9.5 12v2M13.5 13h2M8.7 16.7l1.6 1.6M10.3 16.7l-1.6 1.6M13.5 17.5h2"/>
<circle cx="14.5" cy="16.2" r=".4" {S}/><circle cx="14.5" cy="18.8" r=".4" {S}/>'''
TECLADO = f'''<rect x="2.5" y="6" width="19" height="12" rx="2.5"/>
<path d="M6 12.9h.01M9 12.9h.01M12 12.9h.01M15 12.9h.01M18 12.9h.01M6 9.9h.01M9 9.9h.01M15 9.9h.01M18 9.9h.01" stroke-width="2.2"/>
<path d="M8 15.8h8"/><rect x="10.3" y="8.3" width="3.4" height="3" rx=".8" {S}/>'''
AUDIO = f'''<path d="M4 14.5V12a8 8 0 0 1 16 0v2.5"/><rect x="3" y="13.5" width="4" height="6.5" rx="1.6" {F}/>
<rect x="17" y="13.5" width="4" height="6.5" rx="1.6" {F}/><path d="M10 11v6M12 8.5v11M14 11.5v5"/>'''
CARPETA_G = f'''<path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2.5h7a2 2 0 0 1 2 2V17.5a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z" {F}/><path d="M3.5 11.5h17"/>'''
TERMINAL = f'''<rect x="3" y="4.5" width="18" height="15" rx="2.5" {F}/><path d="M7 9.5l3 2.5-3 2.5M12.5 15h4.5"/>'''
IMAGEN = f'''<rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><circle cx="8.6" cy="9.5" r="1.6" {S}/>
<path d="M4 17l4.8-4.6 3.6 3.4 3-3 4.6 4.6"/>'''
INSTALAR = f'''<path d="M4.5 15v2.5a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V15" {F}/><path d="M12 4v10M8 10.5l4 4 4-4"/>'''
CASA = f'''<path d="M4 11.5l8-7 8 7"/><path d="M6 10v8.5a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V10" {F}/><path d="M10 19.5v-5h4v5"/>'''
PAPELERA = f'''<path d="M5 7h14M10 4h4M7 7l.8 12a1.5 1.5 0 0 0 1.5 1.4h5.4a1.5 1.5 0 0 0 1.5-1.4L17 7" {F}/><path d="M10 11v6M14 11v6"/>'''
PAPELERA_LLENA = f'''<path d="M7 7l1-2.5h8L17 7"/><path d="M4.5 7h15M7 7l.8 12a1.5 1.5 0 0 0 1.5 1.4h5.4a1.5 1.5 0 0 0 1.5-1.4L17 7" {F}/>
<path d="M9 11.5l1.5 2M15 11l-1.5 3M12 10.5v6"/>'''
DISCO = f'''<rect x="3.5" y="7" width="17" height="10" rx="2.5" {F}/><path d="M7 12h6"/><circle cx="17" cy="12" r=".9" {S}/>'''
PORTATIL = f'''<rect x="5" y="5" width="14" height="10" rx="2" {F}/><path d="M3 19h18"/>'''
ESCRITORIO = f'''<rect x="3" y="4.5" width="18" height="12" rx="2" {F}/><path d="M9 20.5h6M12 16.5v4"/>'''
PENDRIVE = f'''<rect x="8" y="2.5" width="8" height="5" rx="1"/><rect x="6.5" y="7.5" width="11" height="14" rx="2.5" {F}/>
<path d="M10.5 11.5v2M13.5 11.5v2"/>'''
USB = f'''<path d="M12 18V4.2"/><circle cx="12" cy="19.2" r="2" {F}/><path d="M9.6 7.2L12 3.6l2.4 3.6z" {S}/><path d="M12 14.5L7.2 11.8V9.4M12 12L16.8 9.4V8"/><circle cx="7.2" cy="8" r="1.4" {S}/><rect x="15.5" y="5.2" width="2.6" height="2.6" rx=".3" {S}/>'''
FORMAS = f'''<path d="M8.5 4.5l5 8.5h-10z" {F}/><circle cx="16.5" cy="8.5" r="3.5"/><rect x="10.5" y="14" width="9" height="6.5" rx="1.5"/>'''
RAIZ = f'''<path d="M3.5 13h3l2.8 6.5L14.6 4.5h6.9"/><path d="M15.6 9.2l3.8 3.8M19.4 9.2l-3.8 3.8"/>'''
TECLA_T = f'''<rect x="3.5" y="3.5" width="17" height="17" rx="3.5" {F}/><path d="M8 9h8M12 9v7.5"/>'''
TORTUGA = f'''<ellipse cx="12" cy="13" rx="5.6" ry="6.8" {F}/>
<path d="M7.5 9L4.6 7.2M16.5 9l2.9-1.8M7.5 17l-2.9 1.8M16.5 17l2.9 1.8M12 19.8v2"/>
<circle cx="12" cy="4.7" r="1.9" fill="{{bg}}"/><path d="M12 9.6l2.6 1.6v3.6L12 16.4l-2.6-1.6v-3.6z"/>'''
PINCEL = f'''<path d="M19.5 4.5l-8 8"/><path d="M9 13.5c-2 0-3.5 1.5-3.5 3.5 0 1.5-.8 2.3-1.5 2.8 2.5 1 6.5.5 7.5-2.3.5-1.4-.3-3.6-2.5-4z" {F}/>'''
REPRODUCTOR = f'''<circle cx="12" cy="12" r="8.5"/><path d="M10 8.6l5.4 3.4-5.4 3.4z" {F}/>'''
ESCANER = f'''<path d="M4.5 11l2-5h11l2 5"/><rect x="3" y="11" width="18" height="8" rx="2" {F}/><path d="M6 14.8h12"/>'''
NOTAS = f'''<rect x="5" y="4" width="14" height="17" rx="2.2"/><path d="M8.5 3v3M12 3v3M15.5 3v3"/><path d="M8.5 11h7M8.5 14.5h7M8.5 18h4"/>'''
PARTICIONES = f'''<path d="M12 13V4.5A8.5 8.5 0 1 0 20.5 13z" {F}/><path d="M14.5 10.5V2.5a8.5 8.5 0 0 1 8 8z"/>'''
APAGAR = '''<path d="M12 4v8"/><path d="M7 6.8a7.5 7.5 0 1 0 10 0"/>'''


# ---- dibujos nuevos (resto del sistema) ----
CAJA_HERR = f'''<rect x="3.5" y="8" width="17" height="11.5" rx="2.5" {F}/><path d="M9 8V6.5A1.5 1.5 0 0 1 10.5 5h3A1.5 1.5 0 0 1 15 6.5V8M3.5 13h17M10.5 13v2h3v-2"/>'''
CODIGO = f'''<path d="M8.5 7.5L4 12l4.5 4.5M15.5 7.5L20 12l-4.5 4.5M13.5 5l-3 14"/>'''
BIRRETE = f'''<path d="M2.5 9.5L12 5l9.5 4.5L12 14z" {F}/><path d="M6.5 11.8V16c1.5 1.6 3.4 2.3 5.5 2.3s4-.7 5.5-2.3v-4.2M21.5 9.5V15"/>'''
GLOBO = f'''<circle cx="12" cy="12" r="8.5" {F}/><path d="M3.5 12h17M12 3.5c3 3.2 3 13.8 0 17M12 3.5c-3 3.2-3 13.8 0 17"/>'''
JOYSTICK = f'''<rect x="2.5" y="7" width="19" height="10.5" rx="5" {F}/><path d="M7.5 10.2v4M5.5 12.2h4"/><circle cx="15.6" cy="11.2" r=".9" {S}/><circle cx="18.2" cy="13.4" r=".9" {S}/>'''
NOTA_MUSICAL = f'''<path d="M9.5 17V6.5l9-1.8v10.8"/><circle cx="7.3" cy="17" r="2.2" {F}/><circle cx="16.3" cy="15.5" r="2.2" {F}/>'''
MALETIN = f'''<rect x="3" y="7.5" width="18" height="12" rx="2.5" {F}/><path d="M8.5 7.5V6A1.5 1.5 0 0 1 10 4.5h4A1.5 1.5 0 0 1 15.5 6v1.5M3 13h18M11 13v1.5h2V13"/>'''
ENGRANAJE = f'''<circle cx="12" cy="12" r="3.2" {F}/><path d="M12 3v2.4M12 18.6V21M3 12h2.4M18.6 12H21M5.6 5.6l1.7 1.7M16.7 16.7l1.7 1.7M18.4 5.6l-1.7 1.7M7.3 16.7l-1.7 1.7"/>'''
AJUSTES = f'''<path d="M4 7h16M4 12h16M4 17h16"/><circle cx="9" cy="7" r="2.2" fill="{{bg}}"/><circle cx="15.5" cy="12" r="2.2" fill="{{bg}}"/><circle cx="8" cy="17" r="2.2" fill="{{bg}}"/>'''
AJUSTES_SOLO = f'''<path d="M4 7h2.8M11.2 7H20M4 12h9.3M17.7 12H20M4 17h1.8M10.2 17H20"/><circle cx="9" cy="7" r="2.2" {F}/><circle cx="15.5" cy="12" r="2.2" {F}/><circle cx="8" cy="17" r="2.2" {F}/>'''
REINICIAR = f'''<path d="M19.5 12a7.5 7.5 0 1 1-2.4-5.5"/><path d="M19.5 4.5v4.5h-4.5"/>'''
BOLSA = f'''<path d="M5.5 8.5h13l-1 11.5h-11z" {F}/><path d="M9 8.5V7a3 3 0 0 1 6 0v1.5"/><path d="M9.5 12.5a2.5 2.5 0 0 0 5 0"/>'''
RESTAURAR = f'''<path d="M4.5 12a7.5 7.5 0 1 0 2.4-5.5"/><path d="M4.5 4.5v4.5h4.5"/><path d="M12 8v4.2l2.8 1.6"/>'''
ESCUDO = f'''<path d="M12 3.5l7 2.8v5.4c0 4.2-2.8 7.3-7 8.8-4.2-1.5-7-4.6-7-8.8V6.3z" {F}/><path d="M8.7 12l2.2 2.2 4.4-4.5"/>'''
CANDADO = f'''<rect x="5" y="10.5" width="14" height="10" rx="2.5" {F}/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/><circle cx="12" cy="15.5" r="1.1" {S}/>'''
SALIR = f'''<path d="M10 4.5H6.5a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2H10"/><path d="M14 8l4 4-4 4M18 12H9"/>'''
LUNA = f'''<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10z" {F}/>'''
RED = f'''<circle cx="12" cy="6" r="2.5" {F}/><circle cx="5.5" cy="18" r="2.5" {F}/><circle cx="18.5" cy="18" r="2.5" {F}/><path d="M10.7 8.2L6.8 15.8M13.3 8.2l3.9 7.6M8 18h8"/>'''
OTROS = f'''<rect x="3.5" y="3.5" width="7" height="7" rx="1.8" {F}/><rect x="13.5" y="3.5" width="7" height="7" rx="1.8"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.8"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.8" {F}/>'''
CAMARA = f'''<rect x="3" y="7" width="18" height="12" rx="2.5" {F}/><circle cx="12" cy="13" r="3.3"/><path d="M8 7l1.2-2h5.6L16 7"/>'''
ACTIVIDAD = f'''<rect x="3" y="4.5" width="18" height="12.5" rx="2.5"/><path d="M6 11.5h2.8l1.7-3.8 2.8 6.6 1.6-2.8H18"/><path d="M9 20.5h6M12 17v3.5"/>'''
LUPA = f'''<circle cx="10.5" cy="10.5" r="6" {F}/><path d="M15 15l5 5"/>'''
ARCHIVO_COMP = f'''<rect x="4" y="5" width="16" height="15" rx="2.5" {F}/><path d="M4 9.5h16M12 5v8"/><rect x="10.3" y="13" width="3.4" height="3.4" rx=".8"/>'''
PDF = f'''<path d="M7 3h7l4.5 4.5V19a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M14 3v4.5h4.5"/>
<path d="M5 14.5h13.5V19a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z" {S} fill-opacity=".4"/><path d="M8.5 11h7"/>'''
HTML = f'''<path d="M7 3h7l4.5 4.5V19a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M14 3v4.5h4.5" {F}/><path d="M10 12l-2 2 2 2M14 12l2 2-2 2"/>'''
EJECUTABLE = f'''<rect x="4" y="5" width="16" height="14" rx="2.5" {F}/><path d="M8 10.5l3 2-3 2M13 15h3.5"/>'''
VIDEO_ARCH = f'''<rect x="3.5" y="5" width="17" height="14" rx="2.5" {F}/><path d="M10 9.5v5l4.5-2.5z"/>'''
AUDIO_ARCH = f'''<rect x="3.5" y="5" width="17" height="14" rx="2.5" {F}/><path d="M9 15.5v-6l6.5-1.2v6"/><circle cx="7.8" cy="15.7" r="1.4" {S}/><circle cx="14.3" cy="14.5" r="1.4" {S}/>'''

# apps / lugares / dispositivos / tipos de archivo -> (dibujo, color)
APPS = {
    "firefox-esr": (NAVEGADOR, NARANJA), "libreoffice-writer": (TEXTO, AZUL), "libreoffice-calc": (PLANILLA, VERDE),
    "libreoffice-impress": (PRESENTACION, MAGENTA), "libreoffice-draw": (FORMAS, AMBAR), "libreoffice-math": (RAIZ, VIOLETA),
    "turbowarp-desktop": (COHETE, ROJO), "ombu-scratch": (BLOQUES, VIOLETA), "ombu-pilas": (ROBOT, TURQUESA),
    "gcompris-qt": (ABACO, AMBAR), "tuxpaint": (PALETA, TURQUESA), "tuxmath": (CALCULADORA, AZUL), "tuxtype": (TECLA_T, MAGENTA),
    "ktouch": (TECLADO, VIOLETA), "kturtle": (TORTUGA, VERDE), "kolourpaint": (PINCEL, MAGENTA), "audacity": (AUDIO, NARANJA),
    "org.xfce.filemanager": (CARPETA_G, TURQUESA), "org.xfce.thunar": (CARPETA_G, TURQUESA), "org.xfce.terminal": (TERMINAL, GRIS),
    "org.xfce.parole": (REPRODUCTOR, VIOLETA), "org.gnome.SimpleScan": (ESCANER, AZUL), "org.xfce.mousepad": (NOTAS, GRIS),
    "org.xfce.ristretto": (IMAGEN, MAGENTA), "gparted": (PARTICIONES, GRIS), "ombu-install": (INSTALAR, TURQUESA), "ombu-restaurar": (RESTAURAR, VERDE), "ombu-antirrobo": (ESCUDO, AZUL), "ombu-centro": (BOLSA, AMBAR),
    "org.xfce.screenshooter": (CAMARA, AZUL), "org.xfce.taskmanager": (ACTIVIDAD, VERDE), "xarchiver": (ARCHIVO_COMP, AMBAR),
    "org.xfce.appfinder": (LUPA, TURQUESA), "org.xfce.settings.manager": (AJUSTES, GRIS),
}
# ---- ¡Todos los programas con el mismo diseño! (los que antes se veían con Papirus) ----
MOUSE = f'''<rect x="6.5" y="3" width="11" height="18" rx="5.5" {F}/><path d="M12 3v7M6.5 10h11"/>'''
ALTAVOZ = f'''<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" {F}/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>'''
IMPRESORA = f'''<path d="M7 9V4h10v5"/><rect x="3.5" y="9" width="17" height="8" rx="2" {F}/><rect x="7" y="14" width="10" height="6" rx="1"/>'''
BLUETOOTH = f'''<path d="M7 7.5l10 9-5 4.5V3l5 4.5-10 9"/>'''
CAMPANA = f'''<path d="M6 17.5V11a6 6 0 0 1 12 0v6.5l1.5 1.5h-15z" {F}/><path d="M10 21h4"/>'''
PERSONA = f'''<circle cx="12" cy="7.5" r="3.5" {F}/><path d="M4.5 20c0-4.2 3.4-7 7.5-7s7.5 2.8 7.5 7"/>'''
SOBRE = f'''<rect x="3" y="5.5" width="18" height="13" rx="2.5" {F}/><path d="M3.5 7l8.5 6.5L20.5 7"/>'''
VENTANA = f'''<rect x="3" y="4.5" width="18" height="15" rx="2.5" {F}/><path d="M3 9h18"/><path d="M6.5 6.8h.01M9 6.8h.01" stroke-width="1.8"/>'''
APPS.update({
    "org.gnome.Cheese": (CAMARA, MAGENTA), "camera-web": (CAMARA, MAGENTA), "camera-photo": (CAMARA, MAGENTA),
    "chromium": (GLOBO, AZUL), "atril": (PDF, ROJO), "galculator": (CALCULADORA, GRIS), "htop": (ACTIVIDAD, VERDE),
    "calamares": (INSTALAR, TURQUESA), "kgeography": (GLOBO, VERDE), "khangman": (JOYSTICK, MAGENTA), "klettres": (BIRRETE, VIOLETA),
    "libreoffice-startcenter": (MALETIN, AZUL), "lightdm-gtk-greeter-settings": (AJUSTES, GRIS),
    "preferences-system-network": (RED, TURQUESA), "system-shutdown": (APAGAR, ROJO), "xfsm-logout": (SALIR, NARANJA),
    "org.xfce.settings.accessibility": (PERSONA, AZUL), "org.xfce.settings.appearance": (PALETA, MAGENTA),
    "org.xfce.settings.color": (PALETA, AMBAR), "org.xfce.settings.default-applications": (AJUSTES, GRIS),
    "org.xfce.xfdesktop": (ESCRITORIO, AZUL), "org.xfce.settings.display": (ESCRITORIO, AZUL), "org.xfce.settings.keyboard": (TECLADO, VIOLETA),
    "org.xfce.mailreader": (SOBRE, AZUL), "org.xfce.settings.mouse": (MOUSE, TURQUESA), "org.xfce.notification": (CAMPANA, AMBAR),
    "org.xfce.panel": (VENTANA, GRIS), "org.xfce.powermanager": (BATERIA if False else ACTIVIDAD, VERDE),
    "printer": (IMPRESORA, AZUL), "org.xfce.volman": (USB, TURQUESA), "org.xfce.session": (ENGRANAJE, GRIS),
    "org.xfce.settings.editor": (AJUSTES, GRIS), "org.xfce.terminalemulator": (TERMINAL, GRIS), "org.xfce.terminal-settings": (TERMINAL, GRIS),
    "tuxpaint-config": (AJUSTES, TURQUESA), "gvim": (CODIGO, VERDE), "multimedia-volume-control": (ALTAVOZ, NARANJA),
    "org.xfce.webbrowser": (GLOBO, AZUL), "org.xfce.xfwm4": (VENTANA, GRIS), "org.xfce.xfwm4-tweaks": (VENTANA, GRIS),
    "org.xfce.workspaces": (VENTANA, TURQUESA), "org.gnome.DiskUtility": (DISCO, GRIS),
    "blueman": (BLUETOOTH, AZUL), "blueman-device": (BLUETOOTH, AZUL), "bluetooth": (BLUETOOTH, AZUL),
    "preferences-desktop-peripherals": (MOUSE, TURQUESA), "input-mouse": (MOUSE, TURQUESA),
})
# ---- Programas del Centro de software Ombú (31): mismo estilo, para que todo el sistema se vea igual ----
FRACCION = f'''<path d="M5 12h14"/><circle cx="12" cy="6.4" r="1.8" {S}/><circle cx="12" cy="17.6" r="1.8" {S}/>'''
TARJETAS = f'''<rect x="3" y="8" width="13.5" height="11" rx="2.2" {F}/><path d="M7 5.5h11.5a2 2 0 0 1 2 2V15"/><path d="M6.5 12h6.5M6.5 15h4"/>'''
GRAFICO = f'''<path d="M3.5 3.5v17h17"/><path d="M6 16c3-9 6.2 1.5 8-4.5 1.3-4.3 3.4-3.6 5-6.5" {F}/>'''
MATRAZ = f'''<path d="M9.5 3.5h5M10.5 3.5v6L5 19a1.5 1.5 0 0 0 1.3 2h11.4a1.5 1.5 0 0 0 1.3-2l-5.5-9.5v-6" {F}/><path d="M7.8 15h8.4"/>'''
ATOMO = f'''<ellipse cx="12" cy="12" rx="9.2" ry="3.7"/><ellipse cx="12" cy="12" rx="9.2" ry="3.7" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9.2" ry="3.7" transform="rotate(120 12 12)"/><circle cx="12" cy="12" r="1.7" {S}/>'''
ESTRELLA = f'''<path d="M12 3l2.7 5.7 6.2.8-4.6 4.3 1.2 6.1L12 16.8 6.5 19.9l1.2-6.1L3.1 9.5l6.2-.8z" {F}/>'''
LIBRO = f'''<path d="M12 6.3C10 4.8 7 4.3 4 4.8v13.4c3-.5 6 0 8 1.5 2-1.5 5-2 8-1.5V4.8c-3-.5-6 0-8 1.5z" {F}/><path d="M12 6.3v13.4"/>'''
DISCO_OPT = f'''<circle cx="12" cy="12" r="8.5" {F}/><circle cx="12" cy="12" r="2.3"/><path d="M12 5.5a6.5 6.5 0 0 1 6.5 6.5" opacity=".6"/>'''
LAPIZ = f'''<path d="M4 20l1-4.5L16.5 4a2 2 0 0 1 2.8 0l.7.7a2 2 0 0 1 0 2.8L8.5 19z" {F}/><path d="M14.5 6l3.5 3.5"/>'''
APPS.update({
    "kanagram": (TECLA_T, AMBAR), "kbruch": (FRACCION, AZUL), "parley": (TARJETAS, MAGENTA), "supertux": (JOYSTICK, VERDE),
    "geogebra": (GRAFICO, TURQUESA), "kmplot": (GRAFICO, AZUL), "accessories-calculator": (CALCULADORA, GRIS), "qalculate-gtk": (CALCULADORA, GRIS),
    "kalzium": (MATRAZ, VERDE), "step": (ATOMO, VIOLETA), "stellarium": (ESTRELLA, AMBAR), "marble": (GLOBO, AZUL),
    "thonny": (CODIGO, AMBAR), "geany": (CODIGO, AZUL), "mypaint": (PALETA, VIOLETA), "pencil2d": (LAPIZ, AMBAR),
    "inkscape": (FORMAS, GRIS), "gimp": (IMAGEN, NARANJA), "krita": (PALETA, TURQUESA), "vlc": (REPRODUCTOR, NARANJA),
    "tuxguitar": (NOTA_MUSICAL, VIOLETA), "xournalpp": (NOTAS, AZUL), "pdfarranger": (PDF, ROJO), "gnumeric": (PLANILLA, VERDE),
    "abiword": (TEXTO, AZUL), "fbreader": (LIBRO, MAGENTA), "bleachbit": (PAPELERA, VERDE), "xfburn": (DISCO_OPT, ROJO),
})
RELOJ = f'''<circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/>'''
LUGARES = {
    "user-home-symbolic": (CASA, TURQUESA), "go-home-symbolic": (CASA, TURQUESA), "folder-home-symbolic": (CASA, TURQUESA), "folder-home": (CASA, TURQUESA), "go-home": (CASA, TURQUESA), "document-open-recent": (RELOJ, AMBAR), "document-open-recent-symbolic": (RELOJ, AMBAR), "folder-recent": (RELOJ, AMBAR),
    "user-home": (CASA, TURQUESA), "user-trash": (PAPELERA, NARANJA), "user-trash-full": (PAPELERA_LLENA, NARANJA),
    "user-desktop": (ESCRITORIO, AZUL), "network-workgroup": (RED, TURQUESA), "network-server": (RED, TURQUESA),
}
DISPOSITIVOS = {
    "computer": (PORTATIL, MAGENTA), "drive-harddisk": (DISCO, GRIS),
    "drive-removable-media": (USB, TURQUESA), "drive-removable-media-usb": (USB, TURQUESA),
    # pendrives que el sistema ve como disco USB (p. ej. Kingston DataTraveler): piden estos nombres
    "drive-harddisk-usb": (USB, TURQUESA), "media-removable": (USB, TURQUESA), "drive-removable-media-flash": (USB, TURQUESA),
    # la memoria interna de la netbook (eMMC) y el sistema de archivos: disco, no pendrive
    "drive-removable-media-flash-mmc": (DISCO, GRIS), "drive-harddisk-system": (DISCO, GRIS), "drive-harddisk-root": (DISCO, GRIS),
}
TIPOS = {
    "text-x-generic": (TEXTO, GRIS), "application-pdf": (PDF, ROJO), "image-x-generic": (IMAGEN, MAGENTA),
    "audio-x-generic": (AUDIO_ARCH, NARANJA), "video-x-generic": (VIDEO_ARCH, VIOLETA), "package-x-generic": (ARCHIVO_COMP, AMBAR),
    "x-office-document": (TEXTO, AZUL), "x-office-spreadsheet": (PLANILLA, VERDE), "x-office-presentation": (PRESENTACION, MAGENTA),
    "application-x-executable": (EJECUTABLE, GRIS), "text-html": (HTML, NARANJA), "text-x-script": (EJECUTABLE, VERDE),
    "application-x-generic": (TEXTO, GRIS),
}
# nombres específicos que piden las aplicaciones -> se muestran con el tipo genérico de arriba
ALIAS = {
    "text-plain": "text-x-generic",
    "application-vnd.oasis.opendocument.text": "x-office-document", "application-msword": "x-office-document",
    "application-vnd.openxmlformats-officedocument.wordprocessingml.document": "x-office-document", "application-rtf": "x-office-document",
    "application-vnd.oasis.opendocument.spreadsheet": "x-office-spreadsheet", "application-vnd.ms-excel": "x-office-spreadsheet",
    "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet": "x-office-spreadsheet", "text-csv": "x-office-spreadsheet",
    "application-vnd.oasis.opendocument.presentation": "x-office-presentation", "application-vnd.ms-powerpoint": "x-office-presentation",
    "application-vnd.openxmlformats-officedocument.presentationml.presentation": "x-office-presentation",
    "image-png": "image-x-generic", "image-jpeg": "image-x-generic", "image-gif": "image-x-generic", "image-bmp": "image-x-generic",
    "image-svg+xml": "image-x-generic", "image-webp": "image-x-generic",
    "audio-mpeg": "audio-x-generic", "audio-x-wav": "audio-x-generic", "audio-ogg": "audio-x-generic", "audio-flac": "audio-x-generic",
    "video-mp4": "video-x-generic", "video-x-matroska": "video-x-generic", "video-webm": "video-x-generic", "video-x-msvideo": "video-x-generic",
    "application-zip": "package-x-generic", "application-x-archive": "package-x-generic", "application-x-compressed-tar": "package-x-generic",
    "application-x-7z-compressed": "package-x-generic", "application-vnd.rar": "package-x-generic", "application-gzip": "package-x-generic",
    "text-x-shellscript": "text-x-script", "application-x-shellscript": "text-x-script", "text-x-python": "text-x-script",
    "application-x-sharedlib": "application-x-executable", "application-x-pie-executable": "application-x-executable",
    "text-xml": "text-html", "application-xhtml+xml": "text-html",
}
# categorías del menú y acciones: solo el dibujo (sin placa)
CATEGORIAS = {
    "applications-accessories": (CAJA_HERR, AMBAR), "applications-utilities": (CAJA_HERR, AMBAR),
    "applications-development": (CODIGO, VIOLETA), "applications-education": (BIRRETE, TURQUESA),
    "applications-science": (BIRRETE, TURQUESA), "applications-graphics": (FORMAS, MAGENTA),
    "applications-internet": (GLOBO, AZUL), "applications-network": (GLOBO, AZUL), "applications-games": (JOYSTICK, VERDE),
    "applications-multimedia": (NOTA_MUSICAL, NARANJA), "applications-office": (MALETIN, AZUL),
    "applications-system": (ENGRANAJE, GRIS), "applications-other": (OTROS, GRIS),
    "preferences-system": (AJUSTES_SOLO, GRIS), "preferences-desktop": (AJUSTES_SOLO, GRIS), "preferences-other": (AJUSTES_SOLO, GRIS),
}
ACCIONES = {
    "system-shutdown": (APAGAR, ROJO), "system-reboot": (REINICIAR, AMBAR), "system-restart": (REINICIAR, AMBAR),
    "system-lock-screen": (CANDADO, AZUL), "system-log-out": (SALIR, NARANJA), "system-suspend": (LUNA, VIOLETA),
    "system-hibernate": (LUNA, VIOLETA), "system-switch-user": (SALIR, NARANJA),
}
CARPETAS = {"folder": TURQUESA, "inode-directory": TURQUESA, "folder-open": TURQUESA, "folder-templates": AZUL,
            "folder-publicshare": VIOLETA, "folder-documents": AZUL, "folder-download": VERDE,
            "folder-music": VIOLETA, "folder-pictures": MAGENTA, "folder-videos": NARANJA}
GLIFOS_CARPETA = {
    "folder-documents": '<path d="M7.5 5.5h9M7.5 10h9M7.5 14.5h5.5"/>',
    "folder-download": '<path d="M12 4.5v10M8 10.5l4 4 4-4"/>',
    "folder-music": '<path d="M10 17V6.5l8-1.5v11"/><circle cx="8.2" cy="17" r="2"/><circle cx="16.2" cy="16" r="2"/>',
    "folder-pictures": '<circle cx="8.6" cy="8.6" r="1.5"/><path d="M4.5 17.5l5-5 3 3 2.5-2.5 4.5 4.5"/>',
    "folder-videos": '<path d="M9 6.5v10l8.5-5z"/>',
}
SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">%s</svg>'
CUERPO = "M6 14a4 4 0 0 1 4-4h14l7 8h23a4 4 0 0 1 4 4v28a4 4 0 0 1-4 4H10a4 4 0 0 1-4-4z"


def g(glifo, tx, ty, esc, trazo, color, bg=NAVY):
    cuerpo = glifo.replace("{c}", color).replace("{bg}", bg)
    return ('<g transform="translate(%s %s) scale(%s)" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round">%s</g>' % (tx, ty, esc, color, trazo, cuerpo))


def placa(color, glifo):
    forma = "M10 4h38l12 12v38a6 6 0 0 1-6 6H16L4 48V10a6 6 0 0 1 6-6z"
    pines = "".join('<rect x="%s" y="52" width="6" height="%s" rx="1.3" fill="%s" fill-opacity=".8"/>' % (x, 2.4 + (TRAZO - 1.7), color) for x in (27, 37, 47))
    return SVG % ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (forma, NAVY, color, TRAZO + 0.2)
                  + g(glifo, 12.2, 9.8, 1.65, TRAZO, color) + pines)


def solo(color, glifo):
    """Solo el dibujo, grande y con trazo algo más firme, para tamaños chicos (menú, acciones)."""
    return SVG % g(glifo, 6, 6, 2.0, TRAZO + 0.6, color, bg="#ffffff00")


def carpeta(color, glifo_chico):
    chico = g(glifo_chico, 22.5, 29.5, 0.8, TRAZO + 0.4, color) if glifo_chico else ""
    return SVG % ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (CUERPO, NAVY, color, TRAZO + 0.2)
                  + '<path d="M7 25h50" stroke="%s" stroke-width="%s" stroke-opacity=".85"/>' % (color, TRAZO + 0.1)
                  + '<rect x="42" y="14" width="10" height="2.4" rx="1.2" fill="%s" fill-opacity=".75"/>' % color + chico)


def _numeros(s):
    import re
    return [float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", s)]


def _arco(p0, rx, ry, rot, grande, barrido, p1, pasos=14):
    """Arco SVG (dado por sus extremos) -> lista de puntos."""
    import math
    (x1, y1), (x2, y2) = p0, p1
    if rx == 0 or ry == 0 or p0 == p1:
        return [p1]
    fi = math.radians(rot); c, s = math.cos(fi), math.sin(fi)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = c * dx + s * dy, -s * dx + c * dy
    rx, ry = abs(rx), abs(ry)
    lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    co = math.sqrt(max(0.0, num / den)) * (-1 if grande == barrido else 1)
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx, cy = c * cxp - s * cyp + (x1 + x2) / 2, s * cxp + c * cyp + (y1 + y2) / 2
    ang = lambda ux, uy, vx, vy: math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not barrido and dt > 0:
        dt -= 2 * math.pi
    elif barrido and dt < 0:
        dt += 2 * math.pi
    return [(cx + rx * math.cos(t1 + dt * i / pasos) * c - ry * math.sin(t1 + dt * i / pasos) * s,
             cy + rx * math.cos(t1 + dt * i / pasos) * s + ry * math.sin(t1 + dt * i / pasos) * c) for i in range(1, pasos + 1)]


def _curva(p0, c1, c2, p1, pasos=12):
    return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
                  for a, b, c, d in zip(p0, c1, c2, p1)) for t in (i / pasos for i in range(1, pasos + 1))]


def _subtrazos(d):
    """Trazo SVG (M L H V C Q A Z, absolutos o relativos) -> [(puntos, cerrado)]."""
    import re
    subs, cur, pos, ini = [], [], (0.0, 0.0), (0.0, 0.0)
    for cmd, args in re.findall(r"([MmLlHhVvCcQqAaZz])([^MmLlHhVvCcQqAaZz]*)", d):
        rel, c, a = cmd.islower(), cmd.upper(), _numeros(args)
        if c == "Z":
            if cur:
                subs.append((cur, True)); cur = []
            pos = ini
            continue
        n = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "Q": 4, "A": 7}[c]
        for i in range(0, len(a), n):
            v = a[i:i + n]
            ox, oy = pos if rel else (0.0, 0.0)
            if c in "ML":
                p = (v[0] + ox, v[1] + oy)
                if c == "M" and i == 0:
                    if cur:
                        subs.append((cur, False))
                    cur, ini = [p], p
                else:
                    cur.append(p)
            elif c == "H":
                p = (v[0] + (pos[0] if rel else 0), pos[1]); cur.append(p)
            elif c == "V":
                p = (pos[0], v[0] + (pos[1] if rel else 0)); cur.append(p)
            elif c == "C":
                p = (v[4] + ox, v[5] + oy)
                cur += _curva(pos, (v[0] + ox, v[1] + oy), (v[2] + ox, v[3] + oy), p)
            elif c == "Q":
                q, p = (v[0] + ox, v[1] + oy), (v[2] + ox, v[3] + oy)
                cur += _curva(pos, (pos[0] + 2 / 3 * (q[0] - pos[0]), pos[1] + 2 / 3 * (q[1] - pos[1])),
                              (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1])), p)
            else:
                p = (v[5] + ox, v[6] + oy)
                cur += _arco(pos, v[0], v[1], v[2], int(v[3]), int(v[4]), p)
            pos = p
    if cur:
        subs.append((cur, False))
    return subs


def seguro_gtk(svg):
    """GTK3 vuelve a pintar los íconos «-symbolic» y RELLENA con el color del texto todo <path>, <rect> y <circle>, aunque
    diga fill="none": los contornos (batería, Wi-Fi, Bluetooth...) quedaban como manchas sólidas. A los <polyline> no los
    toca. Acá se pasan a <polyline> los trazos de línea y los rellenos de color propio (el verde, ámbar o rojo de la
    batería, que si no saldrían del color del tema). Los rellenos claros (el punto del Wi-Fi, el parlante) se dejan tal cual:
    GTK los pinta con el color del texto, que es el mismo."""
    import math
    import xml.etree.ElementTree as ET
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ns = "{http://www.w3.org/2000/svg}"

    def convertir(el):
        t = el.tag.replace(ns, "")
        if t == "path":
            return _subtrazos(el.get("d"))
        if t == "rect":
            x, y, w, h = (float(el.get(k, 0)) for k in ("x", "y", "width", "height"))
            r = float(el.get("rx", 0))
            if not r:
                return [([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], True)]
            esq = lambda cx, cy, a0: [(cx + r * math.cos(math.radians(a0 + k * 15)), cy + r * math.sin(math.radians(a0 + k * 15))) for k in range(7)]
            return [(esq(x + w - r, y + r, -90) + esq(x + w - r, y + h - r, 0) + esq(x + r, y + h - r, 90) + esq(x + r, y + r, 180), True)]
        cx, cy, r = (float(el.get(k)) for k in ("cx", "cy", "r"))
        return [([(cx + r * math.cos(a * math.pi / 8), cy + r * math.sin(a * math.pi / 8)) for a in range(16)], True)]

    def recorrer(padre):
        for el in list(padre):
            recorrer(el)
            t = el.tag.replace(ns, "")
            relleno = el.get("fill", "none")          # el grupo que los contiene declara fill="none"
            claro = relleno.lower().startswith("#e8edf2") or relleno in ("currentColor", "{c}")
            if t not in ("path", "rect", "circle") or claro:
                continue
            i = list(padre).index(el)
            padre.remove(el)
            for j, (pts, cerrado) in enumerate(convertir(el)):
                if cerrado and pts[0] != pts[-1]:
                    pts = pts + [pts[0]]
                pl = ET.Element(ns + "polyline")
                for k, v in el.attrib.items():
                    if k not in ("d", "x", "y", "width", "height", "rx", "ry", "cx", "cy", "r"):
                        pl.set(k, v)
                pl.set("points", " ".join("%.2f,%.2f" % p for p in pts))
                if relleno == "none":
                    pl.set("fill", "none")
                padre.insert(i + j, pl)

    raiz = ET.fromstring(svg)
    recorrer(raiz)
    return ET.tostring(raiz, encoding="unicode")


def guardar(sub, nombre, svg):
    if sub in ("status", "places") and nombre.endswith("-symbolic"):
        svg = seguro_gtk(svg)
    d = os.path.join(OUT, "scalable", sub)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, nombre + ".svg"), "w", encoding="utf-8").write(svg)


# ---- Íconos de la bandeja del panel (estado): PROPUESTA B = monocromo claro; el color aparece solo cuando algo avisa ----
CLARO = "#e8edf2"


def e_wifi(n, off=False):
    arcos = [("M8.6 16a5 5 0 0 1 6.8 0", 1), ("M5.5 12.5a9.5 9.5 0 0 1 13 0", 2), ("M2.5 9a14 14 0 0 1 19 0", 3)]
    s = "".join('<path d="%s" opacity="%s"/>' % (d, "1" if (k <= n and not off) else ".4") for d, k in arcos)
    s += '<circle cx="12" cy="19.3" r="1.3" fill="{c}" stroke="none" opacity="%s"/>' % (".4" if off else "1")
    if off:
        s += '<path d="M4 4l16 16" stroke="%s"/>' % ROJO
    return s


def e_vol(n):
    s = '<path d="M1.5 8.5H6L12 3v18l-6-5.5H1.5z" fill="{c}" fill-opacity=".22"/>'
    if n == 0:
        s += '<path d="M16 9l6 6M22 9l-6 6" stroke="%s"/>' % ROJO
    if n >= 1:
        s += '<path d="M15.5 8.7a4.5 4.5 0 0 1 0 6.6"/>'
    if n >= 2:
        s += '<path d="M19 5.5a9 9 0 0 1 0 13"/>'
    return s


def e_bat(p, carga=False):
    col = VERDE if p >= 45 else (AMBAR if p >= 20 else ROJO)
    w = int(14 * p / 100)
    s = '<rect x="1.5" y="5" width="19" height="14" rx="3"/><path d="M22.5 9.5v5"/>'
    if w > 0:
        s += '<rect x="4" y="7.5" width="%s" height="9" rx="1.5" fill="%s" stroke="none"/>' % (w, col)
    if carga:
        s += '<path d="M12 5.8l-4 6.4h5l-3.6 6" stroke="#ffffff" stroke-width="1.5" fill="none"/>'
    return s


def e_bt(on=True):
    return '<path d="M7 7.5l10 9-5 4.5V3l5 4.5-10 9" opacity="%s"/>' % ("1" if on else ".4")


E_RED = '<rect x="4" y="5" width="16" height="9" rx="2" fill="{c}" fill-opacity=".22"/><path d="M8 14v3M12 14v3M16 14v3M6 20h12"/>'
E_RED_OFF = E_RED + '<path d="M4 4l16 16" stroke="%s"/>' % ROJO
E_MIC = '<rect x="9" y="3" width="6" height="11" rx="3" fill="{c}" fill-opacity=".22"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M9 21h6"/>'
E_MIC_OFF = E_MIC + '<path d="M4 4l16 16" stroke="%s"/>' % ROJO
E_CARGADOR = '<path d="M8 3v5M16 3v5"/><path d="M6 8h12v3a6 6 0 0 1-12 0z" fill="{c}" fill-opacity=".22"/><path d="M12 17v4"/>'


def estado():
    t = {}
    for nom, n in (("excellent", 3), ("good", 2), ("ok", 2), ("weak", 1), ("none", 0)):
        t["network-wireless-signal-%s-symbolic" % nom] = e_wifi(n)
    for nom, n, off in (("connected", 3, False), ("offline", 0, True), ("disabled", 0, True), ("acquiring", 1, False)):
        t["network-wireless-%s-symbolic" % nom] = e_wifi(n, off)
    t["network-wireless-symbolic"] = e_wifi(3)
    for nom, n in (("100", 3), ("75", 3), ("50", 2), ("25", 1), ("00", 0)):
        t["nm-signal-%s" % nom] = e_wifi(n)
    t["network-wired-symbolic"] = E_RED; t["network-wired-disconnected-symbolic"] = E_RED_OFF
    t["network-offline-symbolic"] = e_wifi(0, True); t["network-idle-symbolic"] = E_RED
    for nom, n in (("high", 2), ("overamplified", 2), ("medium", 2), ("low", 1), ("muted", 0)):
        t["audio-volume-%s-symbolic" % nom] = e_vol(n)
    t["audio-input-microphone-symbolic"] = E_MIC; t["microphone-sensitivity-high-symbolic"] = E_MIC
    t["microphone-sensitivity-muted-symbolic"] = E_MIC_OFF; t["audio-input-microphone-muted-symbolic"] = E_MIC_OFF
    for p in range(0, 101, 10):
        t["battery-level-%d-symbolic" % p] = e_bat(p)
        t["battery-level-%d-charging-symbolic" % p] = e_bat(p, True)
    t["battery-level-100-charged-symbolic"] = e_bat(100, True)
    for nom, p in (("full", 100), ("good", 60), ("low", 25), ("caution", 10), ("empty", 0)):
        t["battery-%s-symbolic" % nom] = e_bat(p); t["battery-%s-charging-symbolic" % nom] = e_bat(p, True)
    t["battery-full-charged-symbolic"] = e_bat(100, True); t["battery-missing-symbolic"] = e_bat(0)
    t["ac-adapter-symbolic"] = E_CARGADOR
    for nom, on in (("active", True), ("", True), ("disabled", False), ("paired", True)):
        t["bluetooth%s-symbolic" % (("-" + nom) if nom else "")] = e_bt(on)
    return t


def main():
    import shutil
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)                                 # el tema se regenera completo
    n = 0
    for sub, tabla in (("apps", APPS), ("places", LUGARES), ("devices", DISPOSITIVOS), ("mimetypes", TIPOS)):
        for nombre, (dibujo, color) in tabla.items():
            guardar(sub, nombre, placa(color, dibujo)); n += 1
    for nombre, color in CARPETAS.items():
        guardar("places", nombre, carpeta(color, GLIFOS_CARPETA.get(nombre))); n += 1
    for sub, tabla in (("categories", CATEGORIAS), ("actions", ACCIONES)):
        for nombre, (dibujo, color) in tabla.items():
            guardar(sub, nombre, solo(color, dibujo)); n += 1
    for nombre, dibujo in estado().items():                 # íconos de la bandeja del panel
        guardar("status", nombre, solo(CLARO, dibujo)); n += 1
    extra = os.path.join(ROOT, "tools", "iconos-extra")      # íconos hechos a mano (con imágenes), que el generador conserva
    if os.path.isdir(extra):
        for f in sorted(os.listdir(extra)):
            if f.endswith(".svg"):
                guardar("apps", f[:-4], open(os.path.join(extra, f), encoding="utf-8").read()); n += 1
    for alias, origen in ALIAS.items():                    # mismo dibujo con el nombre específico
        guardar("mimetypes", alias, open(os.path.join(OUT, "scalable", "mimetypes", origen + ".svg"), encoding="utf-8").read()); n += 1
    dirs = ("apps", "places", "devices", "mimetypes", "categories", "actions", "status")
    contexto = {"apps": "Applications", "places": "Places", "devices": "Devices", "mimetypes": "MimeTypes",
                "categories": "Categories", "actions": "Actions", "status": "Status"}
    texto = "[Icon Theme]\nName=Ombú\nComment=Íconos de Ombú: estilo Chip, dibujos propios\nInherits=Papirus,hicolor\n"
    texto += "Directories=" + ",".join("scalable/" + d for d in dirs) + "\n\n"
    for d in dirs:
        texto += "[scalable/%s]\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\nContext=%s\n\n" % (d, contexto[d])
    open(os.path.join(OUT, "index.theme"), "w", encoding="utf-8").write(texto)
    print("Tema Ombu: %d íconos en %s (trazo %s)" % (n, os.path.relpath(OUT, ROOT), TRAZO))


if __name__ == "__main__":
    sys.exit(main())