# UFT · GENIUS-5000

**Investigación integrada de Googly, unificación de campos y gravedad cuántica,
con tiempo relacional y LQG.** Tres programas independientes que comparten
herramientas cuando existe un mapa matemático y físico justificado.

Este repositorio reúne infraestructura ejecutable, un catálogo de **5.000 perfiles**,
propuestas delimitadas, cálculos reproducibles y revisión separada. Las tres metas
son problemas abiertos. Los resultados iniciales son lemas y modelos finitos;
no constituyen una teoría completa ni evidencia observacional nueva.

## Empezar

```bash
git clone https://github.com/stevencabascango/UFT.git
cd UFT
python3 -m uft validate
python3 -m uft init
python3 scripts/seed_research.py
python3 -m uft export
python3 -m uft cycle --output .uft/cycle-example
python3 scripts/check.py --output .uft/checks.json
```

Python **3.11+**, sin dependencias para el núcleo y los ejemplos exactos. Abre
[`exports/dashboard.html`](exports/dashboard.html) localmente para buscar nodos,
filtrar programas y estados, inspeccionar el grafo y consultar evidencia. GitHub
muestra su código; descarga o clona el proyecto para usarlo en el navegador.

## Qué contiene

| Componente | Contenido y alcance |
|---|---|
| Tres programas | Propuestas A–O con principios, ecuaciones, pruebas delimitadas, límites y objeciones. |
| Objetivos vigentes | Tres metas físicas, quince hitos previos y comparación con resúmenes sustituidos. |
| GENIUS-5000 | Exactamente 5.000 fichas, diez divisiones, referentes, especialidades y evaluación pendiente explícita. |
| Habilidades | 22 del instituto y cinco de análisis integrado; núcleo común Claude–Codex. |
| Equipos | Selección de 3–50 perfiles, siete funciones y cobertura por programa. |
| Orquestador | Concurrencia, tiempo, llamadas, bytes, reintentos, fallos y recuperación acotados. |
| Memoria | Entidades versionadas, hipótesis, evidencias, historial y auditorías internas/externas diferenciadas. |
| Conexiones | Ocho tipos, mapas, condiciones, fuentes, revisiones y transferencias A/B justificadas. |
| Evaluación | 108 celdas iniciales de cobertura y 21 evaluaciones de los siete criterios para las tres metas. |
| Actualización | Eventos idempotentes, impacto transitivo y alertas deduplicadas; observador de archivos ejecutado. |
| Informes | Once secciones, siete criterios y hasta cinco pruebas discriminantes por informe científico. |
| Entrega | Pruebas adversariales, CI, datos exportables, panel local, Descargas y publicación sin force push. |

La distribución completa se conserva: RG500, LQG500, cuerdas450, twistores650,
topología550, geometría algebraica550, QFT500, categorías350, computación500 e
integración450. Una ficha registrada no equivale a un agente ejecutado ni a una
capacidad científica evaluada.

## Primer ciclo: qué se calculó y revisó

- **Gravedad cuántica/tiempo:** dos singletes SU(2) en cuatro espines1/2, operador
  de triple producto y evolución de un reloj ideal con Hamiltoniano finito
  autoadjunto. Se explicita el producto físico y las soluciones generalizadas.
  No se deriva la dinámica completa de LQG ni el límite de Einstein.
- **Googly:** una obstrucción mixta de Maurer–Cartan en dos DGLA finitas, con un
  caso prolongable y otro obstruido. No se identifica esa DGLA con un espacio
  twistorial físico ni se reconstruyen ambas helicidades gravitatorias.
- **Unificación:** un control SU(2) y un tensor antisimétrico de dimensión cinco
  que conserva la métrica interna y falla Jacobi. Es un filtro algebraico para
  acoplamientos, sin gravedad dinámica ni materia del Modelo Estándar.

El productor usa racionales gaussianos; otro programa reconstruye los resultados
mediante permutaciones y álgebra racional, compara signos y salidas y detecta
alteraciones. La comprobación SymPy es adicional y está registrada. Los tres
controles falsos permanecen **REFUTADOS**. Los argumentos y el alcance físico se
revisaron en ejecuciones distintas; esa separación sigue siendo interna y puede
compartir errores del mismo modelo.

Lee el [primer informe](research/first_cycle.md), la
[revisión matemática](research/audits/mathematical_review.md) y la
[revisión científica](research/audits/scientific_review.md).
Los logs y hashes reales están en [`evidence/`](evidence/); las pruebas no acreditan
excelencia individual de los 5.000 perfiles.

## Programas y antecedentes

| Programa | Propuesta actual | Próximo salto pendiente |
|---|---|---|
| Googly | [Obstrucciones mixtas](research/googly_problem/proposal.md) | Diccionario geométrico, realidad, helicidades y reconstrucción Einstein. |
| Unificación | [Acoplamientos y filtro local](research/unified_field_theory/proposal.md) | Sectores gravitatorio y de materia, espectro, anomalías y predicciones. |
| Gravedad cuántica | [Tiempo relacional y lazos](research/quantum_gravity/proposal.md) | Restricciones completas, reloj físico, UV, continuo y límite semiclásico. |

[`data/goals.json`](data/goals.json) conserva las hojas G1–G5, U1–U5 y GQ1–GQ5
del proyecto previo. El banco de reloj es una calibración adicional; no sustituye
esos hitos. Las candidatas K1–K4, los resultados negativos y los vetos anteriores
se conservan como antecedentes con procedencia, sin importar sus etiquetas como
demostraciones nuevas. Se detectó que un resumen antiguo enumera I–III mientras
que las convenciones y la META vigente incluyen cuantizar RG: prevalecen las
metas actuales y la instrucción explícita del usuario.

## Operación cotidiana

```bash
# Seleccionar especialistas: no ejecuta ningún modelo.
python3 -m uft team 'LQG relational clock intertwiner' --programme quantum_gravity --size 7

# Procesar una entrada versionada y consultar una afirmación.
python3 -m uft ingest examples/new_entry.json
python3 -m uft show EXAMPLE-QUESTION-001

# Una pasada de observación, de solo lectura sobre las fuentes compartidas.
python3 -m uft watch --brain /ruta/brain_uft --master /ruta/TWISTOR_TOPOLOGY_RESEARCH --max-cycles 1 --max-seconds 30 --quiet
python3 -m uft export
```

El análisis continuo funciona mediante eventos y ejecuciones acotadas. Se incluyen
plantillas de planificador; **no se afirma que un servicio de fondo esté activo**.
La sesión de construcción no podía acceder al bus systemd ni a crontab. La
disponibilidad y la última prueba real figuran en
[`evidence/automation.json`](evidence/automation.json). Sin novedades significativas,
el observador permanece silencioso.

La comparación Claude–Codex requiere dos informes cerrados con el mismo brief.
Si falta uno se mantiene pendiente; una prueba del CLI no reemplaza un informe
científico. Véanse [`collaboration/`](collaboration/) y
[`docs/independent_research.md`](docs/independent_research.md).

## Documentación y entrega

- [Instalación y configuraciones existentes](docs/installation.md).
- [Arquitectura](docs/architecture.md), [modelo de datos](docs/data_model.md) y
  [protocolo integrado](docs/research_protocol.md).
- [Estados, rigor y protocolos A/B](docs/scientific_protocol.md).
- [Automatización y Alertas](docs/automation.md), [Descargas](Descargas/README.md).
- [Requisitos y evidencia de aceptación](docs/requirements.md).
- [Limitaciones y hoja de ruta](docs/limitations.md).
- [Publicación en GitHub](docs/publication.md).

El núcleo del instituto procede del repositorio del mismo propietario
[Conf-Claude-Codex](https://github.com/stevencabascango/Conf-Claude-Codex), commit
`85ecc71`. El inventario identifica qué fuentes se consultaron, qué quedó fuera
y el alcance exacto de los resultados importados. La revisión finita no se
presenta como análisis exhaustivo de toda la física y las matemáticas.
