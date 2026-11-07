# Requisitos y evidencia de aceptación

El encargo completo se traduce en mecanismos y evidencias observables. La columna
«estado» describe la implementación; no acredita la solución de las tres metas.

| Requisito | Implementación y evidencia | Estado |
|---|---|---|
| Localizar metas actuales y antecedentes | `data/goals.json`, `data/source_inventory.json`, hashes de14 fuentes compartidas y conflicto de precedencia documentado. | Implementado y ejecutado |
| Inventario matemático, físico, documental y operativo | `uft/workflow.py`,108 celdas iniciales, `exports/coverage.csv`. | Implementado; revisión sustantiva delimitada |
| Siete criterios | Esquema,21 evaluaciones de metas y tablas de informes; carencias explícitas. | Implementado; metas pendientes |
| Tres programas y tiempo/LQG | `research/*/proposal.md`, A–O y seis entradas de fundamentos por banco. | Programas condicionados |
| 5.000 perfiles únicos y distribución exacta | `institute/registry/profiles.jsonl`, catálogo, SHA y pruebas. | Verificado estructuralmente |
| Diferencias metodológicas reales de fichas | Huellas semánticas, objetos, métodos, tareas y cobertura; `tests/test_catalogue.py`. | Validado por diseño, no competencia individual |
| Equipos y funciones | Selección específica por programa; roles conceptuales, matemáticos, físicos, cómputo, contraejemplo, auditoría e integración. | Implementado y seleccionado |
| Concurrencia, consumo, fallos y recuperación | `genius/orchestration.py`, presupuestos y pruebas adversariales. | Verificado localmente |
| Conexiones justificadas | Ocho tipos, mapas y testA/B; pruebas de hipótesis inseparables y ciclos. | Implementado; relaciones físicas pendientes |
| Memoria e invalidación | SQLite transaccional, historial, hashes, impacto transitivo y revisión de criterios/cobertura/enlaces. | Verificado, incluidos cambios y rechazo de aristas |
| Refutados protegidos | Tres controles falsos científicos y pruebas de no promoción incluso pasando por revisión. | Verificado |
| Primer ciclo real | Productor, checker independiente, comparación exacta+hash y revisores en otros procesos. | Ejecutado y auditado internamente |
| Informes obligatorios | Once secciones, siete criterios, cinco tests y ausencia de predicción observacional declarada. | Revisado |
| Habilidades localizables y utilizables |22 canónicas+5 integradas; validación de adapters, rutas y secciones; ciclo ingest de prueba. | Verificado |
| Claude–Codex | Cierre de informes y pendiente por informe ausente; intentoClaude con timeout. | Infraestructura lista; comparación pendiente |
| Alertas significativas | Fuentes, objetivos, dependientes, consecuencias y acciones; deduplicación, silencio sin cambios. | Verificado localmente |
| Seguimiento continuo | Observador finito por eventos y plantillas systemd; dos pasadas reales sin cambios. | Manual comprobado; planificador no activo |
| Conservación de configuraciones | Instalador conservador, dry-run y pruebas contra sobreescritura/symlinks. | Verificado |
| Publicación y paquete | Commit, ZIP, bundle, SHA-256 y script que comprueba cuenta, destino y SHA remoto. | Consultar recibo real, no inferir del README |

La salida completa de la suite está en `evidence/checks.json` cuando se cierra la
entrega. Los tests usan fixtures identificadas y no hacen llamadas de pago. Las
ejecuciones de software no se cuentan como científicos ni como descubrimientos.
