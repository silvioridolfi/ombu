# Historial de versiones de Ombú

Registro de lo que se fue mejorando en cada versión, incluidas las de prueba interna que no se publicaron.
La versión más nueva va arriba. La versión en lenguaje simple está en la página «Novedades» del sitio.

| Versión | Fecha | Estado |
|---|---|---|
| 1.10 | 25 de noviembre de 2026 | Pre-release publicada |
| 1.9 | 22 de noviembre de 2026 | Prueba interna |
| 1.8 | 22 de noviembre de 2026 | Prueba interna |
| 1.7 | 21 de noviembre de 2026 | Prueba interna |
| 1.6 | 15 de noviembre de 2026 | Pre-release publicada |
| 1.5 | 1 de noviembre de 2026 | Pre-release publicada |
| 1.4 | 31 de octubre de 2026 | Prueba interna |
| 1.3 | 31 de octubre de 2026 | Prueba interna |
| 1.2 | 30 de octubre de 2026 | Prueba interna |
| 1.1 | 30 de octubre de 2026 | Pre-release publicada |
| 1.0 | octubre de 2026 | Prueba interna |

## 1.10 — 25 de noviembre de 2026 (pre-release)
Reúne todo lo de las versiones 1.7 a 1.9, que no se publicaron. Compilación 20261124-2131. Es la versión más completa para probar en distintos equipos.
- Instalador: 13 diapositivas con datos de la provincia de Buenos Aires y las líneas de trabajo de la DTE; logo de la DTE más grande.
- Atajos tipo Windows (Win+D, Win+M, Win+flechas, Win+E, S, I, R, P, Win+Mayús+S); Win+L y Ctrl+Alt+L cierran la sesión; lista «Atajos de teclado» en el menú.
- El botón de encendido y Alt+F4 en el escritorio abren el menú de Ombú.
- Pendrives y discos USB: se abren solos al conectarlos (sin ejecutar nada del pendrive), con el símbolo USB; «Mi Equipo» y la barra lateral con íconos de Ombú.
- Íconos de la bandeja (Wi-Fi, Bluetooth, volumen, batería) con el diseño de Ombú, más grandes; Continuemos, Chromium y Cámara en estilo Ombú; nombres cortos en el escritorio.
- Protector de pantalla con cuatro estilos (Reloj Ombú, Poliedros, ¿Sabías que…? y Descanso): entra a los 10 minutos, no pide contraseña y se elige en «Protector de pantalla».
- Diez fondos de escritorio para elegir (cuatro nuevos: burbujas, mosaico, árbol de puntos y red de colores).
- Sonidos: inicio propio, conexión y desconexión de USB, papelera; aviso de volumen con barra; aviso de batería nuevo; volumen y micrófono ajustados.
- GRUB con una sola entrada («Ombú GNU/Linux») y el menú de la ISO ordenado; la G4 sin avisos del núcleo al apagar.
- Apagado más rápido: los servicios de Bluetooth no arrancan en equipos sin Bluetooth y ningún servicio de la sesión retrasa el apagado más de unos segundos.
- Se agregó un agente de contraseñas (`lxpolkit`): sin él, el Centro de software y «Restaurar Ombú» no podían pedir la clave de administrador.
- Escritorio sin lugar ocupado por los pendrives y herramientas del sistema con tamaño normal.
- Instalación: `hwclock` (util-linux-extra), instantánea inicial con la hora de internet, arreglos de G4 y G5.
- Centro de software: «Protección antirrobo (Theft Deterrent)», solo para administración, con descarga desde el repositorio de Ombú y verificación de la huella antes de instalar.

## 1.6 — 15 de noviembre de 2026 (pre-release)
- G4: `nomodeset` ahora sí queda aplicado en el sistema instalado (antes lo pisaba `grub.d/ombu.cfg`).
- G4: puntero visible después de suspender (cursor por software), redibujado de pantalla al reanudar y bloqueo del sintonizador de TV USB que rompía la suspensión. Antes solo existía como script aparte (`ombu-g4-arreglos.sh`).

## 1.5 — 1 de noviembre de 2026 (pre-release)
- Fondo definitivo del escritorio y del inicio de sesión (`ombu-fondo-2026.png`).
- GRUB del sistema instalado: resolución automática, título simple «Ombú GNU/Linux» y tipografías de tamaño 17 y 24.
- Se quitó la carpeta `Desktop` vacía del esqueleto de usuario, para que no reaparezca en inglés.
- Menú de la ISO de 10 segundos con 5 entradas, más la del firmware.
- Reúne todo lo de las versiones 1.2 a 1.4, que no se habían publicado.

## 1.4 — 31 de octubre de 2026 (prueba interna)
- Tema de GRUB en el sistema instalado.
- Ventanas centradas con maximizado automático (devilspie2).
- Menú que se abre con un clic; panel con separador a la derecha y estilo propio del botón «Ombú».
- Carpeta «Escritorio» en español; accesos «Writer» y «Calc».
- «Instalar Ombú» oculto en el sistema instalado.
- «Acerca de» con la lista del equipo y el número de compilación.

## 1.3 — 31 de octubre de 2026 (prueba interna)
- Fondo oscuro nuevo con los logos de Ombú y la DTE.
- Menú Whisker con íconos grandes (Alt+F1 y tecla Windows).
- Juego de íconos nuevo (cuadrados redondeados de colores, carpetas turquesa).
- Ventanas con los tres botones: minimizar, maximizar y cerrar.
- Perfil visual automático «base» o «completo» según la memoria del equipo.
- Carpeta personal y papelera en el escritorio.

## 1.2 — 30 de octubre de 2026 (prueba interna)
- Teclado latinoamericano, también en el instalador.
- Wi-Fi «Estudiantes» preconfigurada.
- Botón de encendido con cartel para elegir (apagar o reiniciar); tecla Windows.
- Logos grandes en el arranque.
- uBlock Origin en Firefox.
- Dos entradas de prueba del touchpad en el menú de arranque (`i8042.nomux` e `i8042.reset`), `xinput` y `libinput-tools` para los informes.

## 1.1 — 30 de octubre de 2026 (pre-release)
- Usuario diario `estudiante` y administración `soporte`.
- Panel con volumen, batería y reloj; Bloq Num apagado al iniciar; íconos del escritorio sin cajas blancas; lanzadores sin cartel de «no confiable».
- Netbooks G4 (Intel GMA 3600): entrada de arranque «video compatible - G4» y `nomodeset` automático al instalar; TurboWarp con WebGL por software.
- Touchpad: tocar para hacer clic.

## 1.0 — octubre de 2026 (prueba interna)
- Primera compilación de prueba: Debian 13 con escritorio XFCE. No se publicó.
