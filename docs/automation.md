# Actividad real y análisis continuo

El mecanismo implementado es incremental: archivos nuevos o modificados producen
eventos versionados; estos registran el impacto transitivo y las revisiones
pendientes. Cada proceso tiene límites de archivos, bytes, ciclos y tiempo.
No realiza llamadas a modelos ni publica conclusiones sin revisión.

```bash
python3 -m uft watch --brain /ruta/brain_uft --master /ruta/TWISTOR_TOPOLOGY_RESEARCH --interval 60 --max-cycles 60 --max-seconds 3600 --quiet
```

`--quiet` no imprime nada cuando no hay cambios ni fallos; el estado de ejecución
queda en `.uft/watch-last.json`. Un archivo sin cambios no genera un nuevo evento.
Las incidencias documentales no se convierten en alertas de descubrimiento físico.

## Planificadores

Se incluyen plantillas systemd de usuario en `automation/`. Configuran una pasada
cada hora, con timeout externo y bloqueo entre ejecuciones. Edita rutas antes de
instalarlas. El archivo de unidad no activa ningún servicio por sí mismo.

La sesión de construcción no tiene acceso al bus systemd de usuario ni permiso
para leer crontab. Por ello se comprobó el observador mediante ejecución manual,
sin afirmar que existe un planificador activo. Los resultados y fechas reales
están en [`evidence/automation.json`](../evidence/automation.json).

En un terminal con systemd de usuario operativo, después de revisar las rutas:

```bash
mkdir -p ~/.config/systemd/user
cp automation/uft-observer.service automation/uft-observer.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now uft-observer.timer
systemctl --user list-timers uft-observer.timer
journalctl --user -u uft-observer.service -n 30
```

Esta operación añade unidades con namespace propio. No reemplaza tareas del BRAIN
ni sincroniza directorios privados con GitHub. Marca «automatización comprobada»
solo tras una ejecución satisfactoria del servicio y conserva su log. Repetir una
investigación requiere información nueva, un error o una pregunta abierta concreta.

## Alertas y Descargas

Cada alerta incluye ID/fecha, objetivos afectados, cambio y fuente, estado
científico, dependientes, consecuencia, acción y análisis enlazado. El almacén
deduplica por cambio significativo. Mantiene separados los namespaces científico
y operativo. Las exportaciones UFT no alteran la política de Alertas del BRAIN.

`exports/` contiene el panel y datos portables. `Descargas/` enlaza informes,
cálculos y material reproducible. La web externa de OneDrive puede estar fuera
de los permisos del proceso: una regeneración fallida no se declara publicada.
