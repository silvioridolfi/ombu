# Ombú 1.6 — Libre, simple y nuestro

Sistema operativo libre pensado para las netbooks de las escuelas de Región 1. Es una iniciativa del equipo territorial de la DTE Región 1: una propuesta de tecnología educativa para enseñar, aprender y crear con lo que ya tenemos.

Base: Debian 13 "trixie" · Escritorio: XFCE · Instalador: Calamares · Sin telemetría.

- Sitio: <https://v0-ombudte.vercel.app>
- Guía de instalación: <https://v0-ombudte.vercel.app/guia>
- Descarga (ISO 1.6, versión de prueba): <https://github.com/silvioridolfi/ombu/releases/tag/v1.6>

> Es una versión de prueba. Seguimos haciendo pruebas de compatibilidad en distintos modelos de netbooks escolares para llegar a la mayor cantidad posible.

## Qué incluye

| Área | Software |
|---|---|
| Producción digital | LibreOffice (Writer, Calc, Impress) en español, con corrector ortográfico · Firefox ESR |
| Pensamiento computacional y programación | TurboWarp (sin conexión) · KTurtle (sin conexión) · Scratch y Pilas Bloques (requieren Internet) |
| Creatividad y producción multimedia | Tux Paint · KolourPaint · Audacity · Reproductor (Parole) · visor de imágenes |
| Matemática y aprendizajes fundamentales | GCompris · Tux Math · KTouch · Tux Typing · KLettres · KHangMan · KGeography |
| Sistema | NetworkManager, Bluetooth, impresión y escáner, zram, firmware Realtek / Atheros / Intel |

La mayoría de los programas funcionan sin conexión. Scratch, Pilas Bloques y Firefox requieren Internet.

## Usuarios

La netbook instalada queda con dos usuarios:

| Usuario | Clave | Uso |
|---|---|---|
| `estudiante` | `estudiante` | Inicia sola al encender. Sin permisos de administrador. |
| el que se crea en el instalador (sugerido: `soporte`) | la que se elija en el instalador | Cuenta técnica con permisos de administrador. Para usarla, cerrar la sesión de `estudiante`. |

En la sesión de prueba (live, sin instalar) el usuario es `user` (clave `live`) con permisos de administrador; ahí `estudiante` todavía no existe: se crea durante la instalación.

Una edición Personal, en la que cada persona elige su propio usuario y contraseña, está prevista para más adelante.

## Probar e instalar

Paso a paso en la [guía](https://v0-ombudte.vercel.app/guia). En resumen:

1. Descargar la ISO y verificar su suma SHA-256 (figura en la página del release).
2. Grabarla en un pendrive de 4 GB o más con Rufus (modo **Imagen DD**) o balenaEtcher.
3. Arrancar la netbook desde USB (el menú de arranque suele abrirse con `F12`, `F11`, `F2` o `Esc`; en las G4 y G5 es `F11`).
4. Probar la sesión live. Para instalar: ícono **Instalar Ombú** del escritorio.
5. **El instalador reemplaza todo el contenido del disco elegido** (instalación solo Ombú, sin doble arranque). Guardar antes lo que se quiera conservar.
6. En la pantalla **Teclado** verificar la distribución (en las netbooks suele ser *Spanish (Latin American)*).

Requisitos: equipo de 64 bits (x86-64) con UEFI de 64 bits o BIOS clásico. Algunas netbooks necesitan desactivar Secure Boot desde la configuración del equipo (UEFI).

## Pruebas de compatibilidad

En cada netbook (sesión en vivo o instalada) abrir una terminal y ejecutar:

```bash
ombu-diagnostico
```

Genera un informe `.txt` en la carpeta personal con los datos del equipo (modelo, BIOS/UEFI, CPU, memoria, Wi-Fi, audio, cámara, batería, firmware faltante) y una lista para completar a mano. Un informe por modelo ayuda a armar la lista de compatibilidad.

## Cómo construir la ISO (Windows 11 + WSL2)

1. En PowerShell (administrador), una sola vez:
   ```powershell
   wsl --install -d Debian
   ```
   Reiniciar si lo pide y crear usuario y clave de Debian.
2. Clonar o descomprimir este proyecto en `C:\ombu` (o donde quieras).
3. En la terminal de Debian:
   ```bash
   cd /mnt/c/ombu
   bash build-ombu.sh
   ```
   Hace todo solo: instala herramientas, baja TurboWarp, construye la ISO y la copia a la carpeta **Descargas** de Windows como `ombu-1.6-amd64.iso`.
   Tarda entre 30 y 90 minutos y necesita unos 20 GB libres.

Si la descarga de TurboWarp falla, bajar a mano `TurboWarp-linux-amd64-X.Y.Z.deb` desde
<https://github.com/TurboWarp/desktop/releases> y ejecutar:

```bash
OMBU_TW_DEB=/ruta/al/archivo.deb bash build-ombu.sh
```

### Wi-Fi de las escuelas

La ISO publicada trae configurado el Wi-Fi de las escuelas. Por seguridad, el archivo con la contraseña **no está en este repositorio** (`Estudiantes.nmconnection` figura en `.gitignore`). Para incluirlo al construir, copiar `docs/Estudiantes.nmconnection.example` a
`config/includes.chroot/etc/NetworkManager/system-connections/Estudiantes.nmconnection` y completar la contraseña. Si el archivo no está, la ISO se construye igual, sin esa red.

## Estructura del proyecto

```
build-ombu.sh                   script único de construcción
auto/                           configuración de live-build
config/package-lists/           listas de paquetes
config/hooks/live/              ajustes dentro del sistema (usuario, idioma, Firefox, Plymouth)
config/includes.chroot/         archivos que se copian al sistema (instalador, temas, fuentes, políticas)
bootloader-overrides/           menú de arranque (BIOS y UEFI)
assets/                         logos, tipografía Encode Sans (OFL), imágenes generadas
tools/gen-assets.py             regenera toda la identidad visual
docs/                           plantillas (Wi-Fi)
```

## Identidad visual

Paleta DTE: rosa `#E52277`, magenta `#AA317A`, azul acero `#3A769B`, turquesa `#10A8C0`, azul oscuro `#04466E`.
Tipografía: Encode Sans (licencia OFL, incluida en `assets/fonts`).
Para regenerar las imágenes: `python3 tools/gen-assets.py` (requiere Pillow, numpy y rsvg-convert).

## Privacidad

- Sin `popularity-contest`, sin reportes automáticos, sin actualizaciones automáticas.
- Firefox: telemetría, estudios, Pocket y sugerencias patrocinadas desactivados por política.
- NetworkManager: sin verificación de conectividad contra servidores externos.
- El instalador no consulta geolocalización por IP.

## A tener en cuenta

- Seguimos sumando compatibilidad de Wi-Fi y audio para más modelos; algunos pueden necesitar firmware adicional.
- Scratch oficial no tiene versión de escritorio para Linux: se usa TurboWarp (sin conexión) y Scratch en línea.
- Esta ISO es para equipos de 64 bits; con UEFI de 32 bits haría falta una variante `ia32`.
- La accesibilidad (lector de pantalla, teclado en pantalla) está pendiente de evaluar.

## Contribuir

Probá Ombú en una netbook de tu escuela y contanos cómo te fue: abrí un mensaje en [Issues](https://github.com/silvioridolfi/ombu/issues) o comentáselo a tu referente de tecnología educativa o al equipo territorial de Región 1.

## Créditos

Equipo territorial de la **DTE | Dirección de Tecnología Educativa — Región 1** (Berisso, Brandsen, Ensenada, La Plata, Magdalena y Punta Indio):

Andrés Guzmán (FED) · Carlos Franco (FED) · Daniela Cortés (FED) · Jorge Pérez (FED) · Julio Machado (CED) · Macarena Duarte Buschiazzo (FED) · Marcos Pettiná (FED) · Silvio Ridolfi (FED)

FED: Facilitador/a de Educación Digital · CED: Coordinador de Educación Digital

© 2026 Dirección de Tecnología Educativa (DTE), Región 1 · Desarrollado por Silvio Ridolfi, Facilitador de Educación Digital.

Los créditos se muestran en el instalador (última diapositiva), en *Acerca de Ombú* (menú de aplicaciones) y en `/usr/share/ombu/CREDITOS.txt`. La lista del equipo está en `config/includes.chroot/usr/share/ombu/equipo.txt`.
