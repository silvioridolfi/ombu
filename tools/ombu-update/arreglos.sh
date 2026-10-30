#!/usr/bin/env bash
# Arreglos para netbooks instaladas con la primera imagen de Ombú:
#   1. Íconos del escritorio: sin cajas blancas al hacer clic en el reloj.
#   2. Bloq Num apagado al iniciar (las netbooks no tienen teclado numérico).
#   3. Panel superior: volumen + batería + reloj en una línea.
#   4. Panel táctil: tocar para hacer clic.
# Uso:  sudo bash arreglos.sh        (el punto 2 necesita internet una vez)
set -euo pipefail
[ "$(id -u)" -eq 0 ] || { echo "Ejecutar con sudo."; exit 1; }

CSS='/* Ombú — íconos del escritorio: etiquetas siempre transparentes,
   sin cajas blancas al perder el foco (por ejemplo, al hacer clic en el reloj). */
XfdesktopIconView.view .label,
XfdesktopIconView.view .label:backdrop,
XfdesktopIconView.view:backdrop .label {
    background-color: transparent;
    background-image: none;
    color: #ffffff;
    text-shadow: 1px 1px 2px #000000;
}
XfdesktopIconView.view .label:selected,
XfdesktopIconView.view .label:selected:backdrop,
XfdesktopIconView.view:backdrop .label:selected {
    background-color: rgba(16, 168, 192, 0.55);
    color: #ffffff;
    border-radius: 3px;
}'

echo "1/4  Íconos del escritorio"
instalar_css() {   # $1 = carpeta personal  $2 = usuario (o vacío)
    mkdir -p "$1/.config/gtk-3.0"
    printf '%s\n' "$CSS" > "$1/.config/gtk-3.0/gtk.css"
    [ -z "$2" ] || chown -R "$2": "$1/.config"
}
instalar_css /etc/skel ""
while IFS=: read -r usuario _ uid _ _ casa _; do
    if [ "$uid" -ge 1000 ] && [ "$uid" -lt 60000 ] && [ -d "$casa" ]; then
        instalar_css "$casa" "$usuario"
        echo "     aplicado a $usuario"
    fi
done < /etc/passwd

echo "2/4  Bloq Num"
if apt-get install -y numlockx; then
    mkdir -p /etc/xdg/autostart
    cat > /etc/xdg/autostart/ombu-numlock.desktop <<'EOT'
[Desktop Entry]
Type=Application
Name=Bloq Num apagado
Exec=numlockx off
OnlyShowIn=XFCE;
NoDisplay=true
EOT
    mkdir -p /etc/lightdm/lightdm.conf.d
    printf '[Seat:*]\ngreeter-setup-script=/usr/bin/numlockx off\n' > /etc/lightdm/lightdm.conf.d/60-ombu-numlock.conf
else
    echo "     No se pudo instalar numlockx (¿hay internet?). Los íconos sí quedaron arreglados."
fi

AQUI="$(cd "$(dirname "$0")" && pwd)"
echo "3/4  Panel superior (volumen, batería, reloj)"
if [ -f "$AQUI/xfce4-panel.xml" ]; then
    apt-get install -y xfce4-pulseaudio-plugin || echo "     (sin internet: se usa el plugin ya instalado, si existe)"
    X=/etc/xdg/xfce4/xfconf/xfce-perchannel-xml
    mkdir -p "$X"
    install -m 644 "$AQUI/xfce4-panel.xml" "$X/xfce4-panel.xml"
    install -m 644 "$AQUI/xfce4-power-manager.xml" "$X/xfce4-power-manager.xml"
    # La configuración de cada usuario pisa la del sistema: se guarda copia y se descarta.
    while IFS=: read -r usuario _ uid _ _ casa _; do
        if [ "$uid" -ge 1000 ] && [ "$uid" -lt 60000 ] && [ -d "$casa" ]; then
            for f in xfce4-panel.xml xfce4-power-manager.xml; do
                u="$casa/.config/xfce4/xfconf/xfce-perchannel-xml/$f"
                [ -f "$u" ] && mv "$u" "$u.bak-ombu"
            done
            rm -rf "$casa/.config/xfce4/panel"
            echo "     panel restablecido para $usuario"
        fi
    done < /etc/passwd
else
    echo "     Falta xfce4-panel.xml junto a este script; se omite."
fi

echo "4/4  Panel táctil"
if [ -f "$AQUI/40-ombu-touchpad.conf" ]; then
    mkdir -p /etc/X11/xorg.conf.d
    install -m 644 "$AQUI/40-ombu-touchpad.conf" /etc/X11/xorg.conf.d/40-ombu-touchpad.conf
fi

echo "Listo. Reiniciá la netbook para aplicar los cambios."
