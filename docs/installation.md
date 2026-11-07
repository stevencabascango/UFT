# Instalación local y conservación de configuraciones

Requisitos del núcleo: Git y Python **3.11 o posterior**. No usa claves API,
servicios externos, privilegios de administrador ni paquetes científicos para el
inventario, el motor, las pruebas y los ejemplos exactos de referencia.

```bash
git clone https://github.com/stevencabascango/UFT.git
cd UFT
python3 -m uft validate
python3 -m uft init
python3 scripts/seed_research.py
python3 -m uft export
python3 -m uft cycle --output .uft/my-first-cycle
python3 scripts/check.py --output .uft/checks.json
```

Abre `exports/dashboard.html` directamente en el navegador; no necesita servidor.
El JSON exportado contiene el alcance y los estados científicos. `cycle` lanza
dos programas deterministas distintos; los informes de revisión científica están
en `research/audits/`. Reejecutar programas no crea por sí solo un nuevo arbitraje.

## Entorno opcional

Puedes usar `python3 -m venv .venv --without-pip` y `.venv/bin/python -m uft ...`
desde el directorio del repositorio. Para instalar el CLI editable con `uv`:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e .
```

La instalación editable conserva el acceso a los datos versionados del checkout.
Si un ejecutable se usa fuera de él, indica `uft --root /ruta/UFT ...`.
El caso SymPy es opcional; en la máquina de origen se ejecutó con `scipython`:

```bash
scipython scripts/science_examples.py --sympy --output .uft/sympy.json
scipython scripts/independent_science_audit.py --output .uft/independent.json
```

## Adaptadores Claude y Codex

`.agents/skills/` contiene las 22 habilidades compartidas del instituto. Las
entradas `.claude/skills/` enlazan al mismo núcleo. `.claude/agents/` y
`.codex/agents/` contienen siete funciones nativas. No se fija un modelo que el
usuario no tenga. Revisa las capacidades detectadas con `python3 -m genius doctor`.

Para instalar los adaptadores **en otro proyecto**, inspecciona primero el plan:

```bash
python3 -m genius install --target /ruta/proyecto --dry-run
python3 -m genius install --target /ruta/proyecto
```

El instalador conserva configuraciones existentes, rechaza destinos de
configuración que redirigen por symlink y comunica cada conflicto. No sobrescribe
`AGENTS.md`, `CLAUDE.md`, skills ni configuraciones personales. Un conflicto deja
la instalación incompleta y explícita; no se presenta como éxito silencioso.

## Fuentes canónicas opcionales

La instantánea portable de `data/` funciona sin la computadora del autor. Para
refrescar objetivos y procedencia desde tus directorios científicos compartidos:

```bash
python3 -m uft inventory --refresh --brain /ruta/brain_uft --master /ruta/TWISTOR_TOPOLOGY_RESEARCH
python3 -m uft watch --brain /ruta/brain_uft --master /ruta/TWISTOR_TOPOLOGY_RESEARCH --max-cycles 1 --max-seconds 30
python3 -m uft export
```

Se leen catorce archivos permitidos; no se recorre todo el home ni OneDrive.
La actualización de procedencia no audita de nuevo cada afirmación de la fuente.
Una fuente inaccesible se registra como tal, sin inventar su contenido.

## Recuperación

La base de trabajo está en `.uft/research.sqlite` y se excluye de Git. Exporta
JSON/CSV después de cambios significativos y conserva evidencia antes de migrar.
Los eventos fallidos permanecen registrados; `ResearchStore.recover(event_id)`
reintenta su contenido original con el límite guardado. Un cambio de entrada usa
un ID o versión nuevos. No cambies un evento ya cerrado para ocultar un fallo.

La suite incluye transacciones revertidas, fallos recuperables, reanudación del
orquestador, agotamiento de presupuesto, comparación incompleta y preservación de
configuraciones. La plataforma puede impedir un planificador de fondo; véase
[`automation.md`](automation.md) y la evidencia real de esta entrega.
