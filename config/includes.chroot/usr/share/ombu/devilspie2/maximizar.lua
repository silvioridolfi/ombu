-- Ombú — las ventanas normales se abren maximizadas (útil en pantallas chicas de las netbooks).
-- Se excluyen utilidades pequeñas, que quedan con su tamaño y centradas.
local clase = string.lower(get_class_instance_name() or "")
local excluidas = {
    "galculator", "xfce4-appfinder", "pavucontrol", "blueman-manager", "nm-connection-editor",
    "xfce4-taskmanager", "xfce4-screenshooter", "calamares", "yad", "zenity", "ristretto",
    "xfce4-notifyd", "gcr-prompter", "polkit-gnome-authentication-agent-1"
}
if get_window_type() == "WINDOW_TYPE_NORMAL" then
    for _, c in ipairs(excluidas) do
        if clase == c then return end
    end
    maximize()
end