#!/bin/bash
# Genera el grub.mo en español de Ombú: el original de Debian + las traducciones de tools/po/grub-es.po
# (Debian no traduce «Advanced options for %s»). Se instala encima del original: usr/share/locale/es/LC_MESSAGES/grub.mo
# Requiere: gettext (msgunfmt, msgcat, msgfmt) y grub-common (el .mo original). Uso: bash tools/gen-grub-mo.sh
set -e
AQUI="$(cd "$(dirname "$0")/.." && pwd)"
ORIG=/usr/share/locale/es/LC_MESSAGES/grub.mo
[ -f "$ORIG" ] || { echo "Falta $ORIG (instalar grub-common)"; exit 1; }
DEST="$AQUI/config/includes.chroot/usr/share/locale/es/LC_MESSAGES"
mkdir -p "$DEST"
TMP="$(mktemp -d)"
msgunfmt "$ORIG" -o "$TMP/base.po"
msgcat --use-first "$AQUI/tools/po/grub-es.po" "$TMP/base.po" -o "$TMP/merged.po"
msgfmt -o "$DEST/grub.mo" "$TMP/merged.po"
rm -rf "$TMP"
echo "-> $DEST/grub.mo"
