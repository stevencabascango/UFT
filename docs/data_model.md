# Modelo de datos y contratos del motor UFT

El motor `uft.store.ResearchStore` mantiene un índice SQLite local y exportaciones
JSON legibles en Git. Trabaja con Python 3.11 o posterior y su biblioteca estándar.
Crear el índice no activa servicios, modelos, tareas programadas ni conexiones de red.

Las validaciones comprueban estructura, procedencia y condiciones del flujo de
trabajo. No deciden la verdad de una teoría, la validez de una demostración ni
la consistencia absoluta de un sistema formal. Una revisión interna conserva
ese alcance; varias ejecuciones del mismo modelo pueden compartir errores.

## Entidades y estados

Cada entidad requiere `id`, `kind`, `objectives`, `statement`, `hypotheses`,
`evidence`, `dependencies`, `status` y `review`. Se admiten `sources`, `domain`,
`conditional_on`, `contradicts` y otros metadatos documentados por el productor.
Los campos de almacenamiento `revision`, `updated` y `content_sha256` se generan
localmente y no pueden reemplazarse mediante datos de entrada.

Los tres identificadores de objetivos son `googly`, `unification` y
`quantum_gravity`. Un objetivo organiza una investigación. Pertenecer a él no
equivale a utilizarlo como premisa: use `objectives` para clasificación y
`dependencies` solamente para dependencias que deban provocar revalidación.

`kind` puede ser `goal`, `objective`, `definition`, `axiom`, `postulate`,
`hypothesis`, `approximation`, `result`, `prediction`, `counterexample`,
`reference`, `obstruction`, `question`, `open_problem`, `convention`,
`candidate`, `observable`, `calculation`, `audit`, `disagreement`, `equation`
o `document`. Definiciones, axiomas matemáticos y postulados físicos no se
confunden mediante una única categoría de «principios».

Los estados científicos reutilizan `genius.memory.STATES`:

| Clave | Estado |
|---|---|
| `established` | Resultado establecido en una fuente verificada |
| `proposal` | Propuesta |
| `conjecture` | Conjetura |
| `evidence` | Evidencia simbólica o numérica de alcance declarado |
| `pending_audit` | Derivación pendiente de auditoría |
| `proven` | Demostrado bajo hipótesis explícitas, tras el flujo de auditoría |
| `formal` | Verificado formalmente, con herramienta y archivos identificados |
| `refuted` | Refutado, con evidencia documentada |
| `review` | En revisión por cambio u objeción |

Una fuente para `established` debe identificar `url`, `path` o `id`, declarar
`verified: true` y precisar `result_used`. Esa declaración es una atribución
auditable del productor, no una verificación bibliográfica automática. Las
referencias pendientes pueden registrarse con estado `proposal` y conservar
su clasificación original en `reported_status`.

La evidencia admite descripciones identificadas y objetos. Si un objeto contiene
`path`, el archivo debe existir; se calcula su SHA-256 y, si se proporcionó uno,
debe coincidir. Una comprobación de archivo no convierte su contenido en prueba.
Las rutas relativas se resuelven respecto del directorio de ejecución; los
servicios del proyecto deben usar rutas absolutas o ejecutar desde su raíz.

`upsert_entity` rechaza la creación o promoción directa a `proven` y `formal`.
Para esos estados se usa el núcleo ya existente `genius.memory.ScientificMemory`:
ejecuciones distintas y terminadas, artefactos, revisión separada de todos los
aspectos requeridos, ausencia de objeciones abiertas y promoción explícita.
Después `import_claim` revalida la revisión exacta, los registros de ejecución,
las huellas de auditoría y el estado de sus dependencias. Las dependencias que
se importen deben existir también en el índice UFT. El registro conserva la
ruta, el ID y la revisión del núcleo. No sustituye el control formal de Lean.

Un resultado refutado conserva su estado negativo al cambiar una dependencia.
No puede volver a `proposal`, `review`, `pending_audit`, `proven` o `formal` bajo
el mismo ID. Una construcción distinta necesita otro identificador y una
explicación de qué se corrigió. Los supuestos `conditional_on` de un resultado
tampoco pueden borrarse para presentar la conclusión como incondicional.

## Relaciones y transferencia

Cada enlace incluye `id`, `source`, `target`, `relation`, `map`, `foundation`,
`hypotheses`, `sources`, `review` y `status`. `map` expresa el mapa concreto entre
objetos; `foundation` explica qué lo respalda. Los tipos son `dependency`,
`implication`, `equivalence`, `correspondence`, `compatibility`,
`incompatibility`, `analogy` y `proposed_connection`. Los estados del enlace son
`proposed`, `reviewed`, `rejected` y `review`.

La dirección de un enlace propagador es **premisa/origen → resultado/destino**.
En cambio, `entity.dependencies` enumera los prerrequisitos de esa entidad.
Solamente `dependency` propaga por defecto; otras conexiones requieren
`propagates: true` cuando sus cambios deban afectar la conclusión. Los ciclos de
dependencia propagadora se rechazan; los ciclos de analogía no se prohíben por
su mera forma gráfica. Los extremos de un ID de enlace son inmutables.

Una transferencia usa `transfer_level: "A"` o `"B"`, `propagates: true` y los
seis campos `coherence` siguientes. Cada uno contiene `passed: true` y una
`justification` específica:

1. `map`: correspondencia de objetos y estructura preservada.
2. `hypotheses`: compatibilidad de hipótesis y condiciones heredadas.
3. `conventions`: dimensiones, pesos, signatura, grupos y representaciones.
4. `category`: nivel científico de origen y conclusión permitido.
5. `frontiers`: ausencia de contradicción con resultados refutados o vetados.
6. `registration`: trazabilidad y registro de la transferencia.

El nivel A exige un origen `established`, `proven` o `formal`. El nivel B exige
que el destino incluya el origen en `conditional_on`; no puede producir un
resultado incondicional establecido o demostrado. Un origen refutado o
invalidado no puede transferirse. Una analogía, incompatibilidad o conexión
todavía no demostrada no se registra como una transferencia de resultados.
Las justificaciones siguen siendo afirmaciones revisables: seis booleanos
marcados no prueban una equivalencia física.

## Versiones, impacto y alertas

Una entidad sin cambios conserva su revisión y no produce alertas. Si cambia
su contenido científico, se conserva el estado recibido en `reported_status`
y se marca `review`, salvo la persistencia de una refutación. Los cambios de
contenido o estado invalidan transitivamente las entidades que dependan de ella,
sus enlaces, cobertura y evaluaciones. La revisión anterior queda en el historial.

Los duplicados evidentes se detectan por texto normalizado, sin resolver
equivalencia matemática. No se fusionan automáticamente. `contradicts` permite
señalar una contradicción explícita y generar una alerta de revisión; el motor
no inventa una refutación a partir de dos frases contrarias.

Las alertas registran ID y fecha, tipo científico u operativo, prioridad,
objetivos, cambio, fuente, estado, dependientes, consecuencia, acción recomendada
y enlace al análisis (`analysis`, que puede ser un ID resoluble). Se deduplican
por significado y revisión. Un fallo repetido con idéntica causa conserva los
intentos sin repetir la misma alerta. Registrar nuevas hipótesis por sí solo
no activa una alarma científica. El mecanismo no envía mensajes externos.

## Cobertura y siete criterios

`set_coverage` admite dimensiones `mathematical`, `physical`, `documentary` y
`operational`. Cada fila identifica elemento, justificación, evidencia y revisión
de entidad. Los estados guardados son «Revisado», «Parcialmente revisado»,
«Pendiente», «Bloqueado» y «No aplicable, con justificación». Se aceptan como
entrada los alias `reviewed`, `partial`, `pending`, `blocked`, `not_applicable`.
«Revisado» exige evidencia; toda fila exige justificación, también la no aplicable.

`set_assessment` usa exactamente siete claves:

| Clave | Criterio |
|---|---|
| `mathematical_coherence` | Coherencia matemática |
| `testability` | Contrastabilidad |
| `correspondence` | Correspondencia |
| `operational_definitions` | Definiciones operacionales |
| `explanation_unification` | Explicación y unificación |
| `parsimony` | Parsimonia |
| `non_empirical` | Evaluación no empírica |

Los estados son «Cumplido en el alcance declarado», «Parcial», «Pendiente»,
«Incumplido» y «No aplicable, con justificación». Sus alias de entrada son
`fulfilled`, `partial`, `pending`, `failed` y `not_applicable`. Cada fila conserva
evidencia, limitaciones, siguiente comprobación y revisión. No se calcula una
probabilidad de verdad ni se equipara evaluación no empírica con experimento.

## Entrada incremental y recuperación

```python
from uft.store import ResearchStore

with ResearchStore("memory/research.sqlite") as store:
    result = store.ingest({
        "id": "IMPORT-001",
        "source": "data/goals.json",
        "version": "sha256:actual-del-archivo",
        "entities": [{
            "id": "GOAL-QG", "kind": "goal",
            "objectives": ["quantum_gravity"],
            "statement": "Investigar una dinámica cuántica de RG con límite semiclásico",
            "hypotheses": [], "evidence": [], "dependencies": [],
            "status": "proposal", "review": None,
        }],
        "links": [],
    }, max_attempts=3)
    snapshot = store.export("memory/research.json")
```

También se admite `entity` para una sola entidad. El lote se entrega con
prerrequisitos antes que dependientes. ID y contenido de evento no pueden
discrepar; la huella también deduplica un evento idéntico con otro ID. Una
observación nueva sin cambios puede registrarse sin producir una alerta.

Las mutaciones de un intento son atómicas. Ante un elemento inválido, se revierte
todo el lote y se conserva evento, error e intento. `recover(event_id)` reintenta
el mismo contenido, por ejemplo después de recuperar una dependencia faltante.
El límite, de 1 a 10 intentos y 3 por defecto, queda fijado al registrar el
evento. No se permite alargarlo mediante cada reintento. Una corrección del
contenido requiere un evento nuevo con versión distinta.

Las excepciones de validación de contenido se reflejan como `failed` o
`exhausted`; las de metadatos inválidos previas al registro se lanzan. Un proceso
interrumpido antes del commit deja el evento pendiente y las mutaciones sin
publicar. SQLite serializa las escrituras locales; los guardados anidados usan
transacciones y savepoints. La herramienta no ejecuta investigación costosa ni
reintentos infinitos por sí misma.

`record_comparison` acepta rutas reales de informes de Claude y Codex. Con un
informe ausente devuelve `pending`; con ambos devuelve `ready_for_cross_review`.
Nunca declara realizada una revisión por la mera existencia de dos archivos.
Conserva desacuerdos y recuerda que archivos distintos no acreditan contextos ni
errores independientes. La revisión cruzada efectiva utiliza el protocolo y los
artefactos separados del núcleo GENIUS.

## Comprobación y límites

`python3 -m unittest discover -s tests -p test_uft_store.py -v` comprueba
idempotencia, rollback y recuperación, límite de reintentos, invalidez transitiva,
cobertura, criterios, estados protegidos, refutaciones, duplicados, transferencia
condicionada, ciclos, evidencia modificada y comparación incompleta.

Las pruebas son del software y de sus barreras documentales. No evalúan la
excelencia individual de los 5.000 perfiles ni resuelven gravedad cuántica,
unificación o el problema de Googly. El historial del índice es append-only
mediante esta API; un propietario que edite directamente la base de datos queda
fuera del modelo de integridad. Los JSON exportados y sus commits proporcionan
la pista de revisión externa al índice de trabajo.
