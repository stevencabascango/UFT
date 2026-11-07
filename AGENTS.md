# UFT — instrucciones de investigación y desarrollo

Lee `docs/scientific_protocol.md`, `docs/research_protocol.md` y las habilidades
canónicas de `.agents/skills/` antes de una investigación. Este repositorio tiene
tres programas: Googly, unificación y gravedad cuántica con tiempo relacional y
LQG. Pueden avanzar por separado. Una conexión requiere un mapa y sus hipótesis.

- Usa evidencia real, fuentes primarias verificadas y los protocolos A/B.
- Conserva los estados científicos, las objeciones y los resultados negativos.
- No describas un modelo finito, una analogía ni una comprobación simbólica como
  solución de la gravedad cuántica, de la unificación o del problema de Googly.
- Los 5.000 perfiles son fichas de diseño; seleccionados, ejecutados, terminados
  y revisados se contabilizan por separado. No acreditan 5.000 expertos evaluados.
- En trabajos de varias etapas, delega componentes independientes y pide revisión
  separada de los resultados científicos centrales. Registra herramientas,
  modelos realmente conocidos, límites de independencia y presupuesto.
- Las skills locales tienen núcleo común para Claude y Codex. No sustituyas una
  configuración del usuario durante la instalación. Los adaptadores usan las
  capacidades detectadas, sin inventar APIs, permisos ni modelos.
- BRAIN UFT y Protocolo Maestro se leen mediante adaptadores de procedencia.
  No modifiques sus archivos ni leas fases independientes abiertas ajenas.
- Ningún enlace B convierte su hipótesis en resultado demostrado. Un cambio de
  dependencia invalida la revisión afectada. No transfieras resultados refutados.
- `python3 scripts/check.py --output evidence/checks.json` es la comprobación
  principal. Los cálculos científicos se ejecutan con `scipython` si está disponible.
- No ejecutes llamadas de pago ni bucles sin límite sin presupuesto explícito.
  La automatización predeterminada solo observa archivos y registra impactos.
- No publiques datos privados, credenciales, cachés ni bases SQLite de trabajo.
  La publicación a `stevencabascango/UFT` está autorizada por el propietario;
  exige cambios revisados y confirmación del SHA remoto. Nunca uses force push.

Si existe `graphify-out/graph.json`, consulta primero ese grafo. Construir un
grafo Graphify nuevo necesita autorización por su posible consumo de tokens.
El mapa científico tipado del proyecto se genera localmente sin llamadas LLM.
