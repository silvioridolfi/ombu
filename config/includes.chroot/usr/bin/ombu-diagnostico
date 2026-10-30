#!/usr/bin/env bash
# Ombú — informe de diagnóstico de hardware para pruebas por modelo.
# Uso:  ombu-diagnostico [carpeta_de_salida]
# No necesita permisos de administrador. Genera un .txt con los datos del
# equipo y una lista para completar a mano (Wi-Fi, audio, cámara, etc.).
set -u

DEST="${1:-}"
if [ -z "$DEST" ]; then
    case "$(dirname "$(readlink -f "$0")")" in
        /usr/*) DEST="$HOME" ;;
        *)      DEST="$(dirname "$(readlink -f "$0")")" ;;
    esac
fi
[ -w "$DEST" ] || DEST="$HOME"

dmi() { cat "/sys/class/dmi/id/$1" 2>/dev/null || echo "?"; }
tiene() { command -v "$1" >/dev/null 2>&1; }

MODELO="$(dmi product_name | tr ' /' '__')"
FECHA="$(date +%Y%m%d-%H%M)"
OUT="$DEST/ombu-diagnostico-${MODELO}-${FECHA}.txt"

sec() { printf '\n===== %s =====\n' "$*"; }

{
echo "INFORME DE DIAGNÓSTICO — Ombú"
echo "Fecha: $(date '+%d/%m/%Y %H:%M')"

sec "SISTEMA"
grep PRETTY_NAME /etc/os-release 2>/dev/null
echo "Kernel: $(uname -r)"
if grep -qw 'boot=live' /proc/cmdline; then echo "Modo: sesión en vivo (pendrive)"; else echo "Modo: sistema instalado"; fi
[ -r /etc/ombu/installed ] && echo "Instalado el: $(cat /etc/ombu/installed)"

sec "EQUIPO"
echo "Fabricante : $(dmi sys_vendor)"
echo "Modelo     : $(dmi product_name)"
echo "Versión    : $(dmi product_version)"
echo "BIOS       : $(dmi bios_vendor) $(dmi bios_version) ($(dmi bios_date))"
if [ -d /sys/firmware/efi ]; then
    echo "Arranque   : UEFI ($(cat /sys/firmware/efi/fw_platform_size 2>/dev/null || echo '?') bits)"
else
    echo "Arranque   : BIOS tradicional (legacy)"
fi

sec "PROCESADOR Y MEMORIA"
tiene lscpu && lscpu | grep -E 'Model name|^CPU\(s\)|Architecture'
free -m
echo; swapon --show 2>/dev/null

sec "DISCO"
tiene lsblk && lsblk -o NAME,SIZE,TYPE,ROTA,MOUNTPOINT 2>/dev/null
echo; df -h / 2>/dev/null

sec "TIEMPO DE ARRANQUE"
if tiene systemd-analyze; then systemd-analyze 2>/dev/null; else echo "(no disponible)"; fi

sec "WI-FI Y RED"
tiene rfkill && rfkill list 2>/dev/null
tiene nmcli && nmcli -t -f DEVICE,TYPE,STATE device 2>/dev/null
echo; (lspci -nn 2>/dev/null | grep -iE 'network|ethernet|wireless'); (lsusb 2>/dev/null | grep -iE 'wireless|wlan|802.11|wi-?fi')
echo; lsmod 2>/dev/null | grep -iE 'rtl|ath|iwl|brcm|b43|wl|8188|8723|r8169' | awk '{print $1}'

sec "BLUETOOTH"
tiene bluetoothctl && bluetoothctl list 2>/dev/null || echo "(sin controlador detectado)"

sec "AUDIO"
tiene aplay && aplay -l 2>/dev/null || echo "(sin placas de sonido detectadas)"

sec "CÁMARA"
ls /dev/video* 2>/dev/null || echo "(no se detectó cámara)"

sec "TECLADO Y PANEL TÁCTIL"
grep -iE 'N: Name=.*(keyboard|touchpad|mouse|elan|synaptics)' /proc/bus/input/devices 2>/dev/null

sec "BATERÍA"
for b in /sys/class/power_supply/BAT*; do
    [ -d "$b" ] || continue
    echo "$(basename "$b"): $(cat "$b/status" 2>/dev/null), carga $(cat "$b/capacity" 2>/dev/null)%"
    full="$(cat "$b/energy_full" "$b/charge_full" 2>/dev/null | head -1)"
    design="$(cat "$b/energy_full_design" "$b/charge_full_design" 2>/dev/null | head -1)"
    if [ -n "$full" ] && [ -n "$design" ] && [ "$design" -gt 0 ] 2>/dev/null; then
        echo "Salud estimada: $(( full * 100 / design ))% de la capacidad original"
    fi
done
ls /sys/class/power_supply/BAT* >/dev/null 2>&1 || echo "(sin batería detectada)"

sec "PANTALLA"
if [ -n "${DISPLAY:-}" ] && tiene xrandr; then xrandr --query 2>/dev/null | grep -E ' connected|^Screen'; else echo "(sin sesión gráfica)"; fi

sec "FIRMWARE FALTANTE Y ERRORES DEL NÚCLEO"
{ dmesg 2>/dev/null || journalctl -k --no-pager 2>/dev/null; } | grep -iE 'firmware.*(fail|missing|not found)|direct firmware load' | head -20
echo "(si no aparece nada arriba, no hay firmware faltante registrado)"

sec "SERVICIOS CON FALLAS"
systemctl --failed --no-legend 2>/dev/null
echo "(vacío = sin fallas)"

cat <<'LISTA'

===== PRUEBA MANUAL (completar a mano: OK / FALLA / NO TIENE) =====
Wi-Fi conecta a una red y navega ............ [   ]
Wi-Fi: el equipo recuerda la red al reiniciar  [   ]
Audio: se escucha por parlantes ............. [   ]
Audio: se escucha por auriculares ........... [   ]
Micrófono ................................... [   ]
Cámara ...................................... [   ]
Teclado: todas las teclas y tildes (ñ, á, @)  [   ]
Panel táctil: movimiento, clic y desplazar .. [   ]
Pantalla: brillo y resolución correctos ..... [   ]
Batería: carga y dura lo esperado ........... [   ]
Puertos USB (pendrive, mouse) ............... [   ]
Lector de tarjeta / HDMI .................... [   ]
Aplicaciones: TurboWarp, GCompris, Tux Paint, LibreOffice, Firefox abren [   ]
Suspender y reanudar (cerrar la tapa) ....... [   ]
Apagado y reinicio sin colgarse ............. [   ]
Observaciones:

LISTA
} > "$OUT" 2>&1

echo "Informe guardado en: $OUT"
