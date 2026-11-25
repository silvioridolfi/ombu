#!/usr/bin/env python3
"""Genera el sonido de inicio propio de Ombú: tres notas ascendentes (do-mi-sol) de campana suave, cálidas y claras.
El de Debian/freedesktop («service-login») es casi inaudible en las netbooks (-22 dB de media, 22 kHz, apenas un «toc»).
Este queda a unos -14 dB de media y -2 dB de pico, 48 kHz estéreo, ~2,2 s, con cola suave.
Uso: python3 tools/gen-sonido-inicio.py [salida.wav]
"""
import os, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "config", "includes.chroot", "usr", "share", "ombu", "sonidos", "inicio.wav")
SR = 48000


def campana(f, dur, t0, total, amp=1.0):
    """Nota de campana: fundamental + armónicos con decaimiento exponencial y ataque corto."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k, (m, a, d) in enumerate([(1, 1.0, 3.2), (2.0, 0.45, 4.5), (3.0, 0.22, 6.0), (4.2, 0.10, 8.0), (5.4, 0.05, 10.0)]):
        y += a * np.sin(2 * np.pi * f * m * t) * np.exp(-d * t)
    ataque = np.minimum(1.0, t / 0.006)
    y *= ataque * amp
    salida = np.zeros(total)
    i0 = int(SR * t0)
    salida[i0:i0 + n] += y[: total - i0]
    return salida


def main():
    total = int(SR * 2.3)
    notas = [(523.25, 0.00), (659.25, 0.20), (783.99, 0.40), (1046.5, 0.62)]   # do5, mi5, sol5, do6
    mono = np.zeros(total)
    for f, t0 in notas:
        mono += campana(f, 1.6, t0, total, amp=1.0 if t0 < 0.6 else 0.8)
    # un poco de eco cálido
    eco = np.zeros(total); eco[int(SR * 0.18):] = mono[: total - int(SR * 0.18)] * 0.25
    mono = mono + eco
    # estéreo con leve apertura
    izq = mono; der = np.roll(mono, int(SR * 0.004))
    est = np.stack([izq, der], axis=1)
    est /= np.max(np.abs(est))
    est *= 10 ** (-2 / 20)
    fade = np.ones(total); nf = int(SR * 0.35); fade[-nf:] = np.linspace(1, 0, nf)
    est *= fade[:, None]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with wave.open(OUT, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((est * 32767).astype("<i2").tobytes())
    rms = 20 * np.log10(np.sqrt(np.mean(est ** 2)))
    print("Sonido de inicio: %s | %.1f s | pico %.1f dB | media (RMS) %.1f dB" % (os.path.relpath(OUT, ROOT), total / SR, 20 * np.log10(np.max(np.abs(est))), rms))


if __name__ == "__main__":
    main()
