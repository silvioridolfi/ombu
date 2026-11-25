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

# ---------- GRUB limpio ----------
# Se quita la entrada «UEFI Firmware Settings» (en inglés y no hace falta: la BIOS se abre con su tecla) y el submenú «Opciones avanzadas»:
# queda una sola entrada, «Ombú GNU/Linux». grub-limpio se vuelve a llamar después de cada update-grub (también al actualizar el núcleo).
chmod -x /etc/grub.d/30_uefi-firmware 2>/dev/null || true
chmod +x /usr/lib/ombu/grub-limpio /etc/kernel/postinst.d/zzz-ombu-grub-limpio /etc/kernel/postrm.d/zzz-ombu-grub-limpio 2>/dev/null || true
update-grub >/dev/null 2>&1 || true
/usr/lib/ombu/grub-limpio || true

# ---------- Inicio de sesión automático ----------
mkdir -p /etc/lightdm/lightdm.conf.d
cat > /etc/lightdm/lightdm.conf.d/50-ombu-autologin.conf <<EOT
[Seat:*]
autologin-user=estudiante
autologin-user-timeout=0
EOT
# ---------- Video Intel GMA 3600/3650 (Atom N2xxx, netbooks G4) ----------
# Estos chips (Cedarview/Poulsbo) con el controlador del núcleo (gma500) dejan la pantalla
# negra en casi todos los arranques; se reactiva con una suspensión corta automática (ver abajo).
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
    # 1.7: se usa el controlador del núcleo (gma500) SIN nomodeset (con nomodeset la imagen sale estirada y la suspensión
    # no despierta). El menú de GRUB va en modo texto porque el gráfico se cuelga en estos equipos.
    cat > /etc/default/grub.d/zz-ombu-g4.cfg <<'EOT'
# Ombú: video Intel GMA 3600/3650 (netbooks G4).
GRUB_TERMINAL=console
GRUB_GFXPAYLOAD_LINUX=text
# El menú en modo texto no dibuja la «ú» (se ve «Omb?»): se usa el nombre sin tilde solo en este modo.
GRUB_DISTRIBUTOR="Ombu"
GRUB_CMDLINE_LINUX_DEFAULT="quiet loglevel=3"
EOT
    update-grub >/dev/null 2>&1 || true
    /usr/lib/ombu/grub-limpio || true

    # Con gma500 la pantalla puede quedar negra al iniciar el escritorio; una suspensión corta con despertar automático
    # la reactiva (igual que cerrar y abrir la tapa). Probado en una G4 real: 3 de 3 arranques.
    mkdir -p /usr/lib/ombu
    cat > /usr/lib/ombu/revivir-pantalla-g4 <<'EOT'
#!/bin/sh
# Ombú (G4): reactiva la pantalla con una suspensión de 4 s con despertar automático. Una vez por arranque.
LOG=/var/log/ombu-revivir.log
exec >>"$LOG" 2>&1
echo "=== $(date '+%F %T') inicio"
export DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0
i=0
while [ "$i" -lt 120 ]; do
    pgrep -x xfdesktop >/dev/null 2>&1 && pgrep -x xfce4-panel >/dev/null 2>&1 && break
    i=$((i+1)); sleep 1
done
echo "escritorio listo tras ${i}s"
sleep 3
if rtcwake -m mem -s 4; then
    echo "$(date '+%F %T') despertó de la suspensión"
else
    echo "rtcwake falló (código $?)"
fi
sleep 2
xrandr --output LVDS-1 --off >/dev/null 2>&1; sleep 1
xrandr --output LVDS-1 --auto --gamma 1:1:1 >/dev/null 2>&1
xset dpms force on >/dev/null 2>&1
echo "=== $(date '+%F %T') fin"
exit 0
EOT
    chmod 755 /usr/lib/ombu/revivir-pantalla-g4
    cat > /etc/systemd/system/ombu-revivir-pantalla.service <<'EOT'
[Unit]
Description=Ombú: reactivar la pantalla de las G4 (gma500)
After=graphical.target
ConditionPathExists=/sys/bus/pci/drivers/gma500

[Service]
Type=oneshot
ExecStart=/usr/lib/ombu/revivir-pantalla-g4
TimeoutStartSec=300

[Install]
WantedBy=graphical.target
EOT
    chmod 644 /etc/systemd/system/ombu-revivir-pantalla.service
    systemctl enable ombu-revivir-pantalla.service >/dev/null 2>&1 || \
        { mkdir -p /etc/systemd/system/graphical.target.wants; ln -sf /etc/systemd/system/ombu-revivir-pantalla.service /etc/systemd/system/graphical.target.wants/ombu-revivir-pantalla.service; }

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
