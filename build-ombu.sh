#!/usr/bin/env bash
# =============================================================================
#  Ombú — script único de construcción de la ISO
#  Sistema operativo libre para las escuelas bonaerenses (DTE Región 1)
#
#  Uso (dentro de Debian 13 en WSL2, o en cualquier Debian 12/13):
#      bash build-ombu.sh
#
#  Variables opcionales:
#      OMBU_OUT=/ruta/destino     carpeta donde queda la ISO (por defecto, Descargas de Windows)
#      OMBU_TW_DEB=/ruta/x.deb    usar un .deb de TurboWarp ya descargado
#      OMBU_WORK=/ruta/trabajo    carpeta de trabajo (debe ser ext4, no /mnt/c)
# =============================================================================
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="${OMBU_WORK:-$HOME/ombu-build}"
SUDO=""
[ "$(id -u)" -eq 0 ] || SUDO="sudo"

say()  { printf '\n\033[1;35m==> %s\033[0m\n' "$*"; }
fail() { printf '\n\033[1;31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- 1. Entorno
say "1/7  Verificando entorno"
[ -r /etc/debian_version ] || fail "Esto tiene que correr en Debian (WSL2 con Debian 13 sirve)."
case "$SRC_DIR" in /mnt/*) echo "El proyecto está en el disco de Windows; se copiará a $WORK (ext4).";; esac
case "$WORK" in /mnt/*) fail "OMBU_WORK no puede estar en /mnt/*: el build falla en sistemas de archivos de Windows.";; esac

AVAIL_GB=$(df -BG --output=avail "$(dirname "$WORK")" | tail -1 | tr -dc '0-9')
[ "${AVAIL_GB:-0}" -ge 20 ] || fail "Hacen falta al menos 20 GB libres (hay ${AVAIL_GB} GB)."

# ------------------------------------------------------------- 2. Dependencias
say "2/7  Instalando herramientas de construcción"
$SUDO apt-get update
$SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    live-build debootstrap squashfs-tools xorriso mtools dosfstools \
    grub-pc-bin grub-efi-amd64-bin grub-common \
    syslinux syslinux-common isolinux \
    librsvg2-bin zstd curl jq rsync ca-certificates gnupg

# ---------------------------------------------------------- 3. Copia de trabajo
say "3/7  Preparando carpeta de trabajo en $WORK"
mkdir -p "$WORK"
rsync -a --delete \
    --exclude 'chroot' --exclude 'binary' --exclude 'cache' --exclude '.build' \
    --exclude 'out' --exclude '*.iso' --exclude 'build.log' --exclude 'local' \
    "$SRC_DIR"/ "$WORK"/
cd "$WORK"
chmod +x auto/* config/hooks/live/*.hook.chroot \
    config/includes.chroot/usr/bin/ombu-acerca \
    config/includes.chroot/usr/bin/ombu-diagnostico \
    config/includes.chroot/usr/bin/ombu-turbowarp \
    config/includes.chroot/usr/bin/ombu-perfil \
    config/includes.chroot/usr/bin/ombu-instalar \
    config/includes.chroot/usr/lib/ombu/* \
    config/includes.chroot/etc/kernel/postinst.d/* config/includes.chroot/etc/kernel/postrm.d/* \
    config/includes.chroot/usr/libexec/xfce4-screensaver/* 2>/dev/null || true
# Identificador de compilación (se muestra en "Acerca de Ombú" y en ombu-diagnostico)
mkdir -p config/includes.chroot/etc/ombu
date '+%Y%m%d-%H%M' > config/includes.chroot/etc/ombu/build
# Limpia restos de un build anterior (solo si existen)
$SUDO lb clean --purge >/dev/null 2>&1 || true

# ------------------------------------------------------------------ 4. TurboWarp
say "4/7  Descargando TurboWarp Desktop (.deb oficial)"
mkdir -p config/packages.chroot
if [ -n "${OMBU_TW_DEB:-}" ]; then
    [ -f "$OMBU_TW_DEB" ] || fail "No existe $OMBU_TW_DEB"
    rm -f config/packages.chroot/*.deb
    cp "$OMBU_TW_DEB" config/packages.chroot/
elif ls config/packages.chroot/*.deb >/dev/null 2>&1; then
    echo "Ya hay un .deb en config/packages.chroot; se usa ese."
else
    API="https://api.github.com/repos/TurboWarp/desktop/releases/latest"
    URL="$(curl -fsSL "$API" | jq -r '.assets[].browser_download_url | select(test("linux-amd64.*\\.deb$"))' | head -n1 || true)"
    if [ -z "$URL" ]; then
        fail "No pude averiguar la URL de TurboWarp. Descargá a mano 'TurboWarp-linux-amd64-*.deb' desde
https://github.com/TurboWarp/desktop/releases y corré de nuevo:
    OMBU_TW_DEB=~/TurboWarp-linux-amd64-X.Y.Z.deb bash build-ombu.sh"
    fi
    echo "Descargando $URL"
    curl -fL --retry 3 -o "config/packages.chroot/$(basename "$URL")" "$URL"
fi
# live-build solo instala paquetes locales llamados <nombre>_<version>_<arq>.deb
for f in config/packages.chroot/*.deb; do
    dpkg-deb -I "$f" >/dev/null 2>&1 || fail "El .deb $f está dañado."
    std="config/packages.chroot/$(dpkg-deb -f "$f" Package)_$(dpkg-deb -f "$f" Version)_$(dpkg-deb -f "$f" Architecture).deb"
    [ "$f" = "$std" ] || mv -f "$f" "$std"
done
ls -lh config/packages.chroot/

# --------------------------------------------------------- 5. Cargador de arranque
say "5/7  Aplicando identidad al menú de arranque"
rm -rf config/bootloaders
cp -a /usr/share/live/build/bootloaders config/bootloaders
cp -a bootloader-overrides/. config/bootloaders/
cp assets/generated/splash.svg config/bootloaders/splash.svg

# ------------------------------------------------------------------ 6. Build
say "6/7  Construyendo la ISO (puede tardar entre 30 y 90 minutos)"
[ -n "$(ls config/packages.chroot/*.deb 2>/dev/null)" ] || fail "Falta el .deb de TurboWarp en config/packages.chroot"

$SUDO ./auto/config
$SUDO lb build 2>&1 | $SUDO tee build.log

ISO="$(ls -1 "$WORK"/*.iso 2>/dev/null | head -n1 || true)"
[ -n "$ISO" ] || fail "El build terminó sin generar ISO. Revisá $WORK/build.log"

# ------------------------------------------------------------------ 7. Entrega
say "7/7  Copiando la ISO"
OUT="${OMBU_OUT:-}"
[ -z "$OUT" ] && [ -d "$SRC_DIR/../salida" ] && OUT="$(cd "$SRC_DIR/../salida" && pwd)"
if [ -z "$OUT" ]; then
    if command -v cmd.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1; then
        WINHOME="$(cmd.exe /c 'echo %USERPROFILE%' 2>/dev/null | tr -d '\r' || true)"
        [ -n "$WINHOME" ] && OUT="$(wslpath "$WINHOME")/Downloads"
    fi
fi
[ -n "$OUT" ] || OUT="$WORK/out"
mkdir -p "$OUT"
cp -f "$ISO" "$OUT/ombu-1.10-amd64.iso"
( cd "$OUT" && sha256sum ombu-1.10-amd64.iso | tee ombu-1.10-amd64.iso.sha256 )

say "Listo. ISO en: $OUT/ombu-1.10-amd64.iso"
echo "Siguiente paso: grabarla en un pendrive con Rufus (modo DD o ISO) o balenaEtcher."
