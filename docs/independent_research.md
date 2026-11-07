# Desarrollo separado y revisión cruzada

El instituto puede usar Claude y Codex mediante los adaptadores nativos. Cada
fase independiente recibe un mismo problema, convenciones, criterios, base
documental y presupuesto. Se escriben espacios separados y se cierran informes
con hashes antes del intercambio. Después cada entorno reconstruye el argumento
del otro, busca errores y conserva los desacuerdos que no pueda resolver.

```bash
python3 -m genius prepare-pair examples/comparison_brief.json --output .uft/pair
python3 -m genius seal-report .uft/pair codex /ruta/informe-codex.json
python3 -m genius seal-report .uft/pair claude /ruta/informe-claude.json
python3 -m genius prepare-cross-review .uft/pair
# Tras dos revisiones reales separadas:
python3 -m genius seal-review .uft/pair codex /ruta/revision-codex.json
python3 -m genius seal-review .uft/pair claude /ruta/revision-claude.json
python3 -m genius synthesize .uft/pair
```

Los modelos se registran como realmente informados por el runtime; `null` expresa
versión no expuesta. La disponibilidad de un ejecutable no demuestra acceso al
modelo. Las llamadas de pago necesitan presupuesto y los subprocesos tienen
timeout. La fase no se marca completada con un archivo vacío, un prompt o una
respuesta inventada. Una síntesis no promueve automáticamente afirmaciones.

## Estado de esta entrega

El desarrollo y las dos revisiones científicas se hicieron en ejecuciones
distintas de Codex. Compartir familia de modelo, entrenamiento y herramientas
limita la independencia. La ejecución CLI Claude tuvo un intento con límite de
15 segundos y terminó por timeout: [`evidence/claude-availability.json`](../evidence/claude-availability.json).
No produjo un informe de investigación. La comparación entre proveedores queda
**PENDIENTE**. No se atribuye trabajo científico al Claude ausente.

`collaboration/paired-cycle-001/` conserva un brief común y el informe Codex
cerrado. El brief formaliza retrospectivamente el alcance de este ciclo, por lo
que ese registro no se presenta como experimento prospectivo controlado. Puede
iniciar una repetición futura con ambos entornos sin alterar el historial.

Las revisiones actuales son internas y asistidas por IA; no se atribuyen
afiliaciones, arbitraje de revista, independencia estadística ni consenso externo.
