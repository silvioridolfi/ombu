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
if [ "$gma" = 1 ]; then
    # /etc/default/grub.d/ombu.cfg se lee después de /etc/default/grub y pisa el valor:
    # por eso el ajuste va en un archivo que se lee al final (zz-).
    mkdir -p /etc/default/grub.d
    cat > /etc/default/grub.d/zz-ombu-g4.cfg <<'EOT'
# Ombú: video Intel GMA 3600/3650 (netbooks G4). Sin esto la pantalla queda negra.
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nomodeset"
EOT
    update-grub >/dev/null 2>&1 || true

    # Puntero invisible después de suspender: cursor por software.
    mkdir -p /etc/X11/xorg.conf.d
    cat > /etc/X11/xorg.conf.d/20-ombu-gma500.conf <<'EOT'
# Ombú: el puntero de hardware del chip Intel GMA 3600 desaparece después de suspender.
Section "Device"
    Identifier "Ombu-GMA"
    Driver "modesetting"
    Option "SWcursor" "true"
EndSection
EOT

    # Colores raros al reanudar: redibujar la pantalla al despertar.
    mkdir -p /usr/lib/systemd/system-sleep /usr/lib/ombu
    cat > /usr/lib/systemd/system-sleep/ombu-reanudar <<'EOT'
#!/bin/sh
[ "$1" = "post" ] || exit 0
systemd-run --no-block --collect --quiet --unit=ombu-reanudar-pantalla /usr/lib/ombu/reanudar-pantalla "$1" "$2" >/dev/null 2>&1
exit 0
EOT
    cat > /usr/lib/ombu/reanudar-pantalla <<'EOT'
#!/bin/sh
LOG=/var/log/ombu-reanudar.log
(
    echo "=== $(date '+%F %T') reanudó ($1 $2)"
    sleep 2
    export DISPLAY=:0
    for xa in /var/run/lightdm/root/:0 /run/lightdm/root/:0; do
        [ -r "$xa" ] && export XAUTHORITY="$xa" && break
    done
    out="$(xrandr --query 2>/dev/null | awk '/ connected/ {print $1; exit}')"
    if command -v chvt >/dev/null 2>&1; then
        cur="$(fgconsole 2>/dev/null || echo 7)"
        chvt 2; sleep 1; chvt "$cur"; sleep 1
    fi
    [ -n "$out" ] && { xrandr --output "$out" --off; sleep 1; xrandr --output "$out" --auto; }
    xset dpms force on 2>/dev/null
    command -v xrefresh >/dev/null 2>&1 && xrefresh
    echo "fin"
) >>"$LOG" 2>&1
exit 0
EOT
    chmod 755 /usr/lib/systemd/system-sleep/ombu-reanudar /usr/lib/ombu/reanudar-pantalla

    # Sintonizador de TV USB Siano sin firmware: rompe la reanudación.
    cat > /etc/modprobe.d/ombu-sin-tv-usb.conf <<'EOT'
blacklist smsusb
blacklist smsdvb
blacklist smsmdtv
install smsusb /bin/false
install smsdvb /bin/false
install smsmdtv /bin/false
EOT
fi

# El instalador no hace falta en el sistema instalado
rm -f /usr/share/applications/ombu-instalar.desktop
rm -f /etc/sudoers.d/live /etc/lightdm/lightdm.conf.d/*live* 2>/dev/null || true
mkdir -p /etc/ombu
date -u +%Y-%m-%dT%H:%M:%SZ > /etc/ombu/installed
exit 0
