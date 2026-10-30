# Ombú 1.1

Sistema operativo libre para las escuelas bonaerenses — DTE Región 1.
Base: Debian 13 "trixie" · Escritorio: XFCE · Instalador: Calamares · Sin telemetría.

> Primera versión pensada para las netbooks **G5/G6** (Coradir EF10MI2 / EF10MIX). Las G4 quedan para más adelante.

## Qué incluye

| Área | Software |
|---|---|
| Programación | TurboWarp Desktop (compatible con Scratch 3, funciona sin internet), Scratch y Pilas Bloques en línea, KTurtle |
| Primaria | GCompris, Tux Paint, Tux Math, Tux Typing, KTouch, KLettres, KHangMan, KGeography, KolourPaint |
| Ofimática | LibreOffice (Writer, Calc, Impress, Draw, Math) en español, corrector ortográfico |
| Audio / video | Audacity, Parole |
| Internet | Firefox ESR con políticas del sistema (sin telemetría, marcadores educativos) |
| Sistema | NetworkManager, Bluetooth, impresión y escáner, zram, firmware Realtek / Atheros / Intel |

## Usuarios

| Usuario | Clave | Uso |
|---|---|---|
| `estudiante` | `estudiante` | Sesión automática. Sin permisos de administrador. |
| el que se crea en el instalador (sugerido: `soporte`) | la que elija el instalador | Administrador (sudo). Para entrar, cerrar la sesión de `estudiante`. |

En la sesión de prueba (live, sin instalar) el usuario es `user` (clave `live`) con permisos de administrador; ahí `estudiante` todavía no existe: se crea durante la instalación.

## Cómo construir la ISO (Windows 11 + WSL2)

1. En PowerShell (administrador), una sola vez:
   ```powershell
   wsl --install -d Debian
   ```
   Reiniciar si lo pide y crear usuario y clave de Debian.
2. Descomprimir este proyecto en `C:\ombu` (o donde quieras).
3. En la terminal de Debian:
   ```bash
   cd /mnt/c/ombu
   bash build-ombu.sh
   ```
   Hace todo solo: instala herramientas, baja TurboWarp, construye la ISO y la copia a la carpeta **Descargas** de Windows como `ombu-1.1-amd64.iso`.
   Tarda entre 30 y 90 minutos y necesita unos 20 GB libres.

Si la descarga de TurboWarp falla, bajar a mano `TurboWarp-linux-amd64-X.Y.Z.deb` desde
<https://github.com/TurboWarp/desktop/releases> y ejecutar:

```bash
OMBU_TW_DEB=/ruta/al/archivo.deb bash build-ombu.sh
```

## Probar y instalar

1. Grabar la ISO en un pendrive con Rufus o balenaEtcher.
2. En la netbook, arrancar desde USB (en las netbooks G4 y G5 se abre el menú de arranque con `F11`; las G5 usan UEFI con Secure Boot desactivado, las G4 arrancan en modo BIOS clásico / Legacy).
3. Probar la sesión live. Para instalar: ícono **Instalar Ombú** del escritorio.
4. El instalador borra el disco elegido (instalación solo Ombú, sin doble arranque).
5. En la pantalla **Teclado** verificar el layout (en las netbooks suele ser *Spanish (Latin American)*). Lo que se elija ahí queda en el sistema instalado.

## Pruebas por modelo

En cada netbook (sesión en vivo o instalada) abrir una terminal y ejecutar:

```bash
ombu-diagnostico
```

Genera un informe `.txt` en la carpeta personal con los datos del equipo (modelo, BIOS/UEFI, CPU, memoria, Wi-Fi, audio, cámara, batería, firmware faltante) y una lista para completar a mano. Un informe por modelo arma la lista de compatibilidad.

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
```

## Identidad visual

Paleta DTE: rosa `#E52277`, magenta `#AA317A`, azul acero `#3A769B`, turquesa `#10A8C0`, azul oscuro `#04466E`.
Tipografía: Encode Sans (licencia OFL, incluida en `assets/fonts`).
Para regenerar las imágenes: `python3 tools/gen-assets.py` (requiere Pillow, numpy y rsvg-convert).

## Créditos

Creado por **Silvio Ridolfi** y el **equipo territorial de Región 1** — DTE | Dirección de Tecnología Educativa, Provincia de Buenos Aires.
Se muestra en el instalador (última diapositiva), en *Acerca de Ombú* (menú de aplicaciones) y en `/usr/share/ombu/CREDITOS.txt`.

## Privacidad

- Sin `popularity-contest`, sin reportes automáticos, sin actualizaciones automáticas.
- Firefox: telemetría, estudios, Pocket y sugerencias patrocinadas desactivados por política.
- NetworkManager: sin verificación de conectividad contra servidores externos.
- El instalador no consulta geolocalización por IP.

## Limitaciones conocidas

- Probar siempre en una G5 real antes de distribuir: hay modelos con Wi-Fi o audio que pueden necesitar firmware adicional.
- Scratch oficial no tiene versión de escritorio para Linux: se usa TurboWarp (offline) y Scratch en línea.
- Si alguna netbook tiene firmware UEFI de 32 bits, esta ISO no arranca en ella (hay que generar una variante `ia32`).

## Licencias

Código y configuración: GPL-3.0-or-later. Arte propio y documentación: CC BY-SA 4.0. Los logos e identidad institucional de la DTE, la Dirección General de Cultura y Educación y el Gobierno de la Provincia de Buenos Aires son de sus titulares, con todos los derechos reservados. Detalle en [`LICENSES/README.md`](LICENSES/README.md).

## Descargar y probar

La ISO se publica en [Releases](../../releases). Verificá la descarga con el archivo `.sha256`:

```bash
sha256sum -c ombu-1.1-amd64.iso.sha256
```

Para reportar problemas, abrí un *Issue* e incluí el informe de `ombu-diagnostico`.
