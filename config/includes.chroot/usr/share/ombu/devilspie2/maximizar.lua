-- Ombú — los PROGRAMAS (navegadores, ofimática, juegos, edición…) se abren maximizados (útil en las pantallas chicas de las netbooks).
-- Las HERRAMIENTAS DEL SISTEMA (terminal, panel de control, explorador de archivos, Centro de software, utilidades…) se abren
-- con su tamaño normal y centradas.
local clase = string.lower(get_class_instance_name() or "")
local nombre = string.lower(get_window_class() or "")

-- Coincidencia exacta
local exactas = {
    "galculator", "pavucontrol", "blueman-manager", "blueman-adapters", "nm-connection-editor", "calamares", "yad", "zenity",
    "gcr-prompter", "polkit-gnome-authentication-agent-1", "thunar", "mousepad", "xarchiver", "gparted", "gnome-disks",
    "timeshift-gtk", "system-config-printer", "lightdm-gtk-greeter-settings", "htop", "simple-scan", "ristretto",
    "atril", "parole", "xfce4-terminal", "xfce4-taskmanager", "xfce4-screenshooter", "xfce4-appfinder", "xfce4-notifyd",
    "xfce4-power-manager-settings", "xfce4-settings-manager", "xfce4-about", "tuxpaint-config", "org.gnome.diskutility"
}
-- Prefijos (cualquier ventana cuya clase empiece así)
local prefijos = { "^xfce", "^ombu", "^org%.xfce", "^thunar", "^xfdesktop", "^panel", "^gcr", "^polkit", "^blueman", "^nm%-" }

if get_window_type() == "WINDOW_TYPE_NORMAL" then
    for _, c in ipairs(exactas) do
        if clase == c or nombre == c then return end
    end
    for _, p in ipairs(prefijos) do
        if string.find(clase, p) or string.find(nombre, p) then return end
    end
    maximize()
end
