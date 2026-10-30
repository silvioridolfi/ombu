#!/bin/sh
# Corre dentro del sistema recién instalado (chroot de Calamares).
set -e

# ---------- Usuario estudiante (sin sudo) ----------
# UID/GID 1100: el 1000 queda para el administrador que crea el instalador.
groups=""
for g in audio video cdrom plugdev netdev lpadmin scanner bluetooth; do
    getent group "$g" >/dev/null && groups="$groups,$g"
done
groups="${groups#,}"
getent group estudiante >/dev/null || groupadd -g 1100 estudiante
if ! id estudiante >/dev/null 2>&1; then
    useradd -m -u 1100 -g estudiante -s /bin/bash -c "Estudiante" -G "$groups" estudiante
fi
echo 'estudiante:estudiante' | chpasswd
cp /usr/share/ombu/avatars/estudiante.png /home/estudiante/.face
mkdir -p /var/lib/AccountsService/icons /var/lib/AccountsService/users
cp /usr/share/ombu/avatars/estudiante.png /var/lib/AccountsService/icons/estudiante
cat > /var/lib/AccountsService/users/estudiante <<EOT
[User]
Icon=/var/lib/AccountsService/icons/estudiante
SystemAccount=false
EOT
chown -R estudiante:estudiante /home/estudiante

# ---------- Inicio de sesión automático ----------
mkdir -p /etc/lightdm/lightdm.conf.d
cat > /etc/lightdm/lightdm.conf.d/50-ombu-autologin.conf <<EOT
[Seat:*]
autologin-user=estudiante
autologin-user-timeout=0
EOT
# ---------- Video Intel GMA 3600/3650 (Atom N2xxx, netbooks G4) ----------
# Estos chips (Cedarview/Poulsbo) dejan la pantalla negra con el controlador
# del núcleo: se arranca con "nomodeset" (video genérico, sin aceleración).
gma=0
for d in /sys/bus/pci/devices/*; do
    [ "$(cat "$d/vendor" 2>/dev/null)" = "0x8086" ] || continue
    case "$(cat "$d/device" 2>/dev/null)" in
        0x0be[0-9a-f]|0x8108|0x8109|0x410[0-9a-f]) gma=1 ;;
    esac
done
if [ "$gma" = 1 ] && [ -f /etc/default/grub ]; then
    if ! grep -q 'nomodeset' /etc/default/grub; then
        sed -i 's/^\(GRUB_CMDLINE_LINUX_DEFAULT="[^"]*\)"/\1 nomodeset"/' /etc/default/grub
    fi
    update-grub >/dev/null 2>&1 || true
fi

rm -f /etc/sudoers.d/live /etc/lightdm/lightdm.conf.d/*live* 2>/dev/null || true
mkdir -p /etc/ombu
date -u +%Y-%m-%dT%H:%M:%SZ > /etc/ombu/installed
exit 0
