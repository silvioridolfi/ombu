#!/usr/bin/env bash
# =============================================================================
#  Ombú — actualizador por pendrive
#  Uso en la netbook (abrir una terminal en la carpeta del pendrive):
#      sudo bash actualizar.sh            # aplica lo que haya en esta carpeta
#      sudo bash actualizar.sh --online   # además baja actualizaciones de Debian
#
#  Qué aplica (todo es opcional, se usa lo que encuentre):
#      fondo.png         -> fondo de escritorio
#      fondo-login.png   -> fondo de la pantalla de inicio de sesión
#      paquetes/*.deb    -> programas nuevos (se instalan sin internet)
#      extra.sh          -> script propio que se ejecuta como administrador
# =============================================================================
set -u

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIJO="${OMBU_PREFIX:-}"          # solo para pruebas; en la netbook queda vacío
LOG="$PREFIJO/var/log/ombu-update.log"
ONLINE=0
[ "${1:-}" = "--online" ] && ONLINE=1

if [ "$(id -u)" -ne 0 ]; then
    echo "Ejecutá con sudo:  sudo bash actualizar.sh"
    exit 1
fi

mkdir -p "$(dirname "$LOG")" "$PREFIJO/etc/ombu"
log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG"; }
HECHO=0

log "=== Actualización de Ombú desde $AQUI ==="

# ---- Fondo de escritorio ----------------------------------------------------
if [ -f "$AQUI/fondo.png" ]; then
    install -D -m 644 "$AQUI/fondo.png" "$PREFIJO/usr/share/ombu/wallpapers/ombu.png"
    log "OK  fondo de escritorio reemplazado"
    HECHO=1
fi

# ---- Fondo de inicio de sesión ----------------------------------------------
if [ -f "$AQUI/fondo-login.png" ]; then
    install -D -m 644 "$AQUI/fondo-login.png" "$PREFIJO/usr/share/ombu/wallpapers/login.png"
    log "OK  fondo de login reemplazado"
    HECHO=1
fi

# ---- Paquetes .deb (sin internet) ------------------------------------------
shopt -s nullglob
DEBS=("$AQUI"/paquetes/*.deb)
if [ "${#DEBS[@]}" -gt 0 ]; then
    log "Instalando ${#DEBS[@]} paquete(s) .deb..."
    if [ -z "$PREFIJO" ]; then
        if dpkg -i "${DEBS[@]}" >>"$LOG" 2>&1; then
            log "OK  paquetes instalados"
        else
            log "..  faltan dependencias, intentando resolverlas"
            if apt-get -f install -y >>"$LOG" 2>&1; then
                log "OK  paquetes instalados (dependencias resueltas; puede haber usado internet)"
            else
                log "ERR no se pudieron instalar los paquetes. Revisá $LOG"
            fi
        fi
    else
        log "(modo prueba: no se instalan .deb)"
    fi
    HECHO=1
fi

# ---- Actualizaciones de Debian (solo si se pide) ---------------------------
if [ "$ONLINE" -eq 1 ] && [ -z "$PREFIJO" ]; then
    log "Buscando actualizaciones de Debian..."
    if apt-get update >>"$LOG" 2>&1 && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade >>"$LOG" 2>&1; then
        log "OK  sistema actualizado"
    else
        log "ERR no se pudo actualizar (¿hay internet?). Revisá $LOG"
    fi
    HECHO=1
fi

# ---- Script propio ----------------------------------------------------------
if [ -f "$AQUI/extra.sh" ]; then
    log "Ejecutando extra.sh..."
    if bash "$AQUI/extra.sh" >>"$LOG" 2>&1; then log "OK  extra.sh terminó bien"; else log "ERR extra.sh falló. Revisá $LOG"; fi
    HECHO=1
fi

# ---- Registro ---------------------------------------------------------------
if [ "$HECHO" -eq 1 ]; then
    date '+%Y-%m-%d %H:%M:%S' > "$PREFIJO/etc/ombu/ultima-actualizacion"
    log "Listo. Para ver el fondo nuevo, cerrá sesión y volvé a entrar."
else
    log "No había nada para aplicar en esta carpeta (fondo.png, fondo-login.png, paquetes/, extra.sh)."
fi
