#!/usr/bin/env python3
"""Ícono genérico de 'programación por bloques' para Scratch y Pilas Bloques (diseño propio de Ombú)."""
from PIL import Image, ImageDraw
import sys

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

def block(x, y, w, h, color, notch=True):
    r = 56
    d.rounded_rectangle((x, y, x + w, y + h), r, fill=color)
    if notch:
        d.rounded_rectangle((x + 90, y - 36, x + 250, y + 10), 20, fill=color)

# fondo redondeado
d.rounded_rectangle((40, 40, S - 40, S - 40), 200, fill=(4, 70, 110, 255))
block(170, 220, 620, 190, (229, 34, 119, 255), notch=False)
block(250, 450, 620, 190, (16, 168, 192, 255))
block(170, 680, 620, 190, (170, 49, 122, 255))
# detalle blanco (círculos)
for cx, cy in ((290, 315), (370, 545), (290, 775)):
    d.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=(255, 255, 255, 230))
out = sys.argv[1] if len(sys.argv) > 1 else "ombu-bloques.png"
img.resize((256, 256), Image.LANCZOS).save(out)
print("ok", out)
