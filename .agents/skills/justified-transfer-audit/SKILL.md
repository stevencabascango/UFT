---
name: justified-transfer-audit
description: Auditar conexiones y transferencias entre objetivos UFT mediante mapas, hipótesis y procedencia, conservando condiciones e invalidaciones.
---

# Conexiones justificadas entre programas

## Propósito y uso
Úsala cuando se proponga trasladar un resultado o hipótesis entre Googly,
unificación y gravedad cuántica, o cuando cambie una conexión existente. Sigue
el [protocolo](../../../docs/research_protocol.md) y el
[contrato de enlaces](../../../docs/data_model.md). La conectividad se investiga.

## Entradas
IDs y revisiones de origen y destino, enunciados y dominio, fuentes, auditorías,
mapa concreto, convenciones y fronteras refutadas pertinentes. Registra una
conexión desconocida como pregunta, sin imponer conexiones mínimas por nodo.

## Procedimiento
1. Elige dependencia, implicación, equivalencia, correspondencia, compatibilidad,
   incompatibilidad, analogía o conexión propuesta según lo realmente justificado.
2. Para una transferencia A/B documenta los seis controles: `map`, `hypotheses`,
   `conventions`, `category`, `frontiers`, `registration`. Cada control necesita
   una justificación específica, además de `passed`.
3. Explicita objetos, mapas, estructura preservada y, si se afirma equivalencia,
   reconstrucción y sentido de inversa o cociente gauge. Comprueba hipótesis,
   pesos, unidades, firma, orientación, grupos y representaciones compatibles.
4. A requiere fuente establecida consultada o resultado auditado vigente. B usa
   una hipótesis de trabajo identificada y obliga a `conditional_on` en el
   destino; sus conclusiones permanecen condicionadas. Un origen refutado,
   vetado o invalidado no es una premisa transferible.
5. Registra revisión, fuentes y propagación de cambios. La dirección propagante
   es origen → dependiente. Rechazar una dependencia o cambiar su fundamento
   obliga a revisar el destino y sus resultados dependientes.

## Herramientas
`python3 -m uft show ID` para inspección; `ResearchStore.add_link` o
`python3 -m uft ingest evento.json` para el registro; `python3 -m uft export`
para grafo tipado y evidencia. Estos comandos no prueban la correspondencia.

## Entregables
Enlace con mapa, fundamento, hipótesis, fuentes, nivel cuando proceda y revisión;
condiciones heredadas, incompatibilidades y comprobación capaz de descartar el mapa.

## Aceptación
No se presenta analogía como equivalencia, fuente como segunda helicidad ni
estructura algebraica como dinámica física. La conclusión B conserva el ID de
su hipótesis y las condiciones de origen no desaparecen tras la transferencia.

## Errores frecuentes
Inferir equivalencia por un camino indirecto, trasladar un teorema sin sus
hipótesis, marcar seis casillas sin argumentos o borrar una condición para
presentar la conclusión como resultado incondicional.

## Colaboración
Pide revisión en ambas especialidades cuando el diccionario cambie de categoría
matemática o régimen físico. Conserva desacuerdos si la reconstrucción no cierra.

## Ejemplo
Una obstrucción cohomológica de un modelo DGLA puede orientar Googly como ruta
condicionada. El diccionario entre clases, helicidades y Einstein debe quedar
pendiente hasta proporcionar mapas, pesos, realidad e integrabilidad concretos.
