# Ombú — registro de mejoras, pendientes y lecciones

Este archivo es la memoria del proyecto. Se actualiza **cada vez que se pide una mejora, se corrige algo o se decide algo**, para que no dependa de ningún chat.
El historial de lo ya entregado por versión está en `CHANGELOG.md`. Acá va lo que falta, lo que se pidió y lo que se aprendió.

Última actualización: 20 de noviembre de 2026 (versión de trabajo: 1.6).

## 1. Cómo retomar el proyecto (desde cero)

1. Leer `CHANGELOG.md` (qué trae cada versión) y este archivo (qué falta).
2. `../TRASPASO_Ombu_DTE.md` tiene el contexto original (30/10): decisiones, hardware probado, preferencias. Está en parte desactualizado; manda el CHANGELOG.
3. Carpeta del proyecto: `E:\DTE\SOFTWARE\Ombú DTE`. El código del sistema está en `ombu/`; las ISO y capturas en `salida/`; el material del sitio en `sitio-web/`; los scripts para netbooks ya instaladas en `ombu-update/`.
4. Repositorio del sistema en GitHub: `silvioridolfi/ombu` (releases y CHANGELOG). Sitio publicado: https://v0-ombudte.vercel.app (el código del sitio **no** está en esta carpeta; el historial se edita en `lib/novedades.ts` de ese repositorio).

## 2. Decisiones que no se tocan sin consultar

- Nombre «Ombú»: provisorio hasta que lo elijan estudiantes en un evento.
- Crédito visible: «Silvio Ridolfi y el equipo territorial de Región 1».
- Lenguaje neutro: «estudiantes». Usuarios: `estudiante` (diario, sin sudo) y `soporte` (administración).
- Sin telemetría. Sin control remoto de aula. Licencias libres.
- Base: Debian 13 + XFCE + live-build + Calamares. Netbooks G4, G5 y G6 con 2 a 4 GB de RAM.
- Consultar antes de cambiar: alcance, nombre, fondos, usuarios y permisos, textos institucionales.
- Se puede corregir sin consultar (informando): bugs y mejoras técnicas pequeñas.

## 3. Pendientes (ordenados)

### Pruebas en hardware real (lo más urgente)
- [ ] **G4 Positivo BGH Schoolmate 15 con la ISO 1.6:** arranque normal sin pantalla negra; `nomodeset` aplicado en el sistema instalado (`cat /proc/cmdline`); puntero visible después de suspender; colores correctos al reanudar; Wi-Fi, audio, cámara, touchpad, lector; que Calamares entre en 1024x600; que TurboWarp abra.
- [ ] **G5 Bangho Suma 1025 con la ISO 1.6:** que no haya cambios respecto de la 1.5 y que el touchpad se comporte.
- [ ] **Touchpad Elantech de la G5:** el núcleo informa `elantech: absolute mode broken, forcing standard PS/2 protocol`, así que el sistema lo toma como mouse. Probar las entradas de arranque «prueba touchpad: i8042.reset» y «i8042.nomux» sin mouse USB conectado, y decidir cuál queda como ajuste para ese modelo.
- [ ] **G6:** no probada.

### Mejoras propuestas, sin decisión
- [ ] Quitar la terminal del dock para primaria.
- [ ] Suspensión al cerrar la tapa (con o sin bloqueo).
- [ ] Desactivar el aviso de actualización de TurboWarp.
- [ ] Accesibilidad: Orca, teclado en pantalla.
- [ ] Reloj/RTC con fecha errónea: sincronizar por internet.
- [ ] «Bienvenido/a» de Calamares no es neutro (usar texto neutro).
- [ ] Usuario del live aparece como «Debian Live user»; íconos de particiones de Windows en el escritorio del live.
- [ ] Archivo único de variables (nombre, versión, créditos), hoy repartido en varios archivos (ver sección 5).
- [ ] Verificar la URL de Continuemos Estudiando y la leyenda 2026.

### Prometido en la propuesta a la DTE y no hecho
- [ ] Piloto, lista de compatibilidad por modelo (hay registros de G5 y G4), indicadores.
- [ ] Ciclo de actualizaciones de seguridad con responsables.
- [ ] Verificación de integridad de imágenes (sumas y firmas).
- [ ] Accesibilidad, licencias, uso de identidad institucional.
- [ ] Actualizar el anexo técnico (G4, panel, etiquetas, diagnóstico, capturas nuevas) y la propuesta.

### Publicación de la 1.6
- [x] Estado de la 1.6: pre-release publicada el 20/11/2026 (CHANGELOG actualizado).
- [x] Release v1.6 publicada en GitHub con ISO y .sha256 (20/11/2026).
- [x] Entrada 1.6 en `lib/novedades.ts` del sitio, publicada (20/11/2026).
- [x] CHANGELOG.md y este archivo subidos a `silvioridolfi/ombu` (20/11/2026).
- [ ] Subir al repositorio las fuentes de la 1.6 (post-install.sh, versión en 6 archivos, branding.desc): hoy el repo tiene las fuentes de la 1.5.
- [x] URL de descarga en `constants.ts` actualizada (20/11/2026).

### Datos de documentación incompletos
- [ ] CHANGELOG, versión 1.0: casi sin datos.
- [ ] CHANGELOG, versiones 1.2 a 1.4: revisar que no falte nada importante.

## 4. Registro de pedidos y cambios (más reciente arriba)

Formato: fecha — qué se pidió o decidió — qué se hizo — estado.

- 20/11/2026 — Pedido: actualizar el sitio https://v0-ombudte.vercel.app para que muestre la versión 1.6. — El sitio es el repositorio `silvioridolfi/ombu-m2` (público; Vercel despliega al subir a `main`; proyecto `ombu`, dominio v0-ombudte.vercel.app). Se preparó una rama local `version-1.6` con: `lib/constants.ts` (versión, URL de descarga a la release v1.6, SHA-256), `lib/novedades.ts` (entrada 1.6) y 3 capturas nuevas. Parche guardado en `sitio-web/version-1.6.patch`. La rama `version-1.6` se subió a GitHub el 20/11 (solo vista previa de Vercel, no producción; `main` sin tocar). Esta PC no tiene `gh`: para subir la ISO como release hace falta instalar GitHub CLI e iniciar sesión, o subirla a mano desde la web de GitHub. **No fusionado a `main`**: falta que exista la release v1.6 en GitHub (si no, el botón de descarga da 404) y decidir el estado de la versión. — Hecho el 20/11/2026: release `v1.6` (pre-release) publicada en `silvioridolfi/ombu` con la ISO y el `.sha256`; sitio fusionado a `main` y desplegado. GitHub CLI instalado en esta PC (`C:\Program Files\GitHub CLI\gh.exe`, sesión de `silvioridolfi`). Pendiente: prueba en G4/G5 reales, pasar el estado del CHANGELOG de «En preparación» a «Pre-release publicada» y subir CHANGELOG/MEJORAS al repo del sistema.
- 15/11/2026 — Pedido: llevar un registro de todas las mejoras y correcciones para no perderlas. — Se creó este archivo. — Hecho.
- 15/11/2026 — Se detectó que el instalador decía «Ombú 1.5» en una ISO marcada 1.6. — Se corrigió `branding.desc` y `ombu.conf`; se reconstruyó la ISO y se verificó en QEMU. — Hecho. (Ver lección 6.1.)
- 15/11/2026 — Pedido: versión 1.6. — Se integraron los arreglos de G4 a la ISO (ver CHANGELOG), se corrigió que `nomodeset` no se aplicaba, se construyó la ISO en WSL, se probó en QEMU, se actualizaron capturas y datos del sitio. — Hecho; falta prueba en hardware real.
- 15/11/2026 — Se consultó si había cambios de diseño (botones, carpetas) pendientes para la 1.6. — No hay constancia en la carpeta ni en sesiones accesibles. Lo existente (botones de ventana, carpetas turquesa, menú) ya está desde la 1.3 y la 1.4. — Sin acción; si hay algo concreto, se anota acá y entra en la 1.7.
- 02/11/2026 y días siguientes — Scripts de diagnóstico y arreglos para G4 en `ombu-update/` (arreglos.sh, ombu-g4-arreglos.sh, ombu-reparar-arranque.sh, ombu-g4-pruebas.sh, ombu-prueba-completa.sh, ombu-diagnostico-instalado.sh). — Los arreglos de G4 pasaron a la ISO en la 1.6. — Hecho.

> Cada pedido nuevo se agrega acá **antes** de hacerlo, y se marca el estado al terminar.

## 5. Dónde está cada cosa (para no olvidar nada al cambiar la versión)

El número de versión está escrito en **estos lugares**; hay que cambiarlos todos:
- `build-ombu.sh` (nombre de la ISO, 3 líneas)
- `README.md` (título y nombre de la ISO)
- `config/hooks/live/0010-sistema.hook.chroot` (`os-release`, `issue`)
- `config/includes.chroot/etc/calamares/branding/ombu/branding.desc` (4 líneas) ← el instalador
- `config/includes.chroot/etc/ombu/ombu.conf` (`OMBU_VERSION`) ← «Acerca de Ombú»
- `CHANGELOG.md`
- Fuera de `ombu/`: `sitio-web/LEEME-sitio.txt`, `lib/novedades.ts` del sitio.
Mejora pendiente: un solo archivo de variables que alimente todo lo anterior.

Otros puntos clave:
- Usuarios y primera sesión: `config/includes.chroot/usr/lib/ombu/post-install.sh`.
- Arreglos específicos de la G4 (video GMA): `post-install.sh`, bloque «Video Intel GMA».
- GRUB del sistema instalado: `config/includes.chroot/etc/default/grub.d/ombu.cfg`. **Cualquier ajuste de línea de comandos del núcleo debe ir en un archivo `zz-…` de esa misma carpeta**, porque `ombu.cfg` pisa `/etc/default/grub`.
- Menú de arranque de la ISO: `bootloader-overrides/`.
- Diseño: `tools/gen-*.py` (íconos, tema de ventanas, GRUB, fondos, assets). Las imágenes en `assets/generated/` salen de ahí.
- Panel y atajos: `config/includes.chroot/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/`.

## 6. Lecciones aprendidas (errores que no hay que repetir)

1. **Cambiar la versión en todos los lugares** (sección 5). En la primera ISO 1.6 el instalador seguía diciendo 1.5. Verificar siempre dentro de la ISO, no solo en el código.
2. **Ajustes de GRUB:** el `nomodeset` de la G4 nunca se aplicó en la 1.5 porque `grub.d/ombu.cfg` pisaba el valor. Usar archivos `zz-`.
3. **Si hay que probar en la G4 real, no alcanza QEMU:** no emula el video Intel GMA 3600. QEMU sirve para ver el instalador, la versión, el escritorio y las capturas.
4. Antes de dar una ISO por buena: arrancarla y mirar el instalador y «Acerca de».
5. Las G4 con 2 GB de RAM caen en perfil visual «base»; las capturas hechas con 2 GB muestran ese perfil.

## 7. Cómo construir y probar la ISO (receta usada en la 1.6)

Esta PC tiene WSL2 con Debian 13 instalado (se instaló el 14/11/2026). Todo se hace como root dentro de esa Debian.

**Construir** (30 a 90 minutos; necesita unos 20 GB libres):
```bash
cd /mnt/e/DTE/SOFTWARE/Omb*/ombu
export OMBU_OUT="$(cd .. && pwd)/salida"
bash build-ombu.sh > ../build-X.Y.log 2>&1
```
Consejos:
- Lanzarlo desde PowerShell con `wsl -d Debian -u root -- bash /ruta/script.sh`, **dejando ese comando en segundo plano**. Si WSL se queda sin sesiones abiertas, se apaga y mata el build.
- No pasar rutas con tilde (`Ombú`) directo por PowerShell hacia WSL: se rompe. Usar un comodín (`Omb*`) o un script `.sh` guardado en un archivo.
- El número de compilación se genera solo (`etc/ombu/build`) y aparece en «Acerca de».

**Probar en QEMU** (instalado en la misma Debian; hay KVM):
```bash
qemu-system-x86_64 -accel kvm -m 2048 -smp 2 -cdrom ISO -boot d -vga std \
  -display none -monitor unix:/tmp/qmon,server,nowait -daemonize
```
- Capturas: `echo "screendump /tmp/x.ppm" | socat - UNIX-CONNECT:/tmp/qmon` y convertir con `convert`.
- Teclado: `sendkey ret`, `sendkey meta_l` (abre el menú; escribir y Enter para abrir una app).
- **El mouse por el monitor de QEMU no funciona de forma confiable** (los clics caen en el centro): navegar solo con teclado.
- Para ver los archivos del sistema sin arrancar: extraer `/live/filesystem.squashfs` con `xorriso -osirrox on` y abrirlo con `unsquashfs`.

**Lista de verificación de cada versión nueva**
1. Cambiar la versión en todos los lugares (sección 5).
2. Construir y confirmar `EXIT=0`.
3. Verificar dentro del squashfs: `ombu.conf`, `branding.desc`, `os-release` y que no quede el número viejo.
4. Arrancar en QEMU: menú de arranque, escritorio, menú, Acerca de, instalador.
5. Rehacer capturas en `salida/capturas-X.Y/` y copiarlas a `sitio-web/public/images/`.
6. Actualizar `sitio-web/LEEME-sitio.txt` (versión, compilación, archivo, tamaño, SHA-256).
7. Actualizar `CHANGELOG.md` y este archivo.
8. Probar en G4 y G5 reales.
9. Recién entonces publicar (release, sitio).

## 8. Entorno de la máquina de trabajo

- Windows 11, WSL2 con Debian 13 (instalada 14/11/2026), QEMU, socat, ImageMagick y squashfs-tools instalados en esa Debian.
- VirtualBox **no** está instalado en esta PC (existe el disco `maquinas-virtuales/Ombu 1.5 prueba`, de una instalación anterior).
- Netbooks de prueba: pendrive con Ventoy o ISO grabada; menú de arranque con `F11` en G4 y G5. G5 arranca en UEFI; G4 en BIOS Legacy.
