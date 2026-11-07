---
name: scientific-intake
description: Incorporar artículos, hipótesis o correcciones al índice UFT con procedencia, versiones y análisis de impacto, conservando su estado científico.
---

# Entrada científica versionada

## Propósito y uso
Usa esta habilidad al registrar información nueva en UFT. Consulta el
[protocolo de investigación](../../../docs/research_protocol.md) y el
[modelo de datos](../../../docs/data_model.md) para distinguir importación,
investigación y promoción científica. Una importación no acredita la afirmación.

## Entradas
Fuente y versión, archivo o URL identificada, alcance examinado, objetivos
afectados y enunciados con hipótesis, evidencia y dependencias. Consulta primero
`data/source_inventory.json`: diferencia la fuente canónica de sus antecedentes
y conserva como pendientes los materiales inaccesibles. No leas fases ajenas
abiertas del Protocolo Maestro ni amplíes el conjunto permitido del observador.

## Procedimiento
1. Comprueba autor, título, fecha e identificador cuando estén disponibles;
   distingue metadatos verificados de resultados efectivamente reconstruidos.
2. Calcula o recupera la huella del archivo. Prepara un evento JSON con `source`,
   `version`, ID estable y `entities` ordenadas por prerrequisitos. Cada entidad
   conserva `statement`, `hypotheses`, `evidence`, `dependencies`, `status` y `review`.
3. Registra fuentes sin consultar como pendientes. No importes etiquetas
   «demostrado» como si fueran una nueva auditoría. Señala contradicciones
   explícitas y posibles duplicados sin fusionar afirmaciones por parecido.
4. Ejecuta `python3 -m uft ingest evento.json`; examina `completed`, `failed` o
   `exhausted`. Un fallo revierte el lote y conserva el intento. Corrige contenido
   mediante un evento nuevo; recuperar una fuente faltante permite reintentar el
   evento original dentro de su presupuesto.
5. Examina los afectados, preguntas pendientes y alertas antes de exportar.
   Un cambio de dependencia exige revalidar sus conclusiones.

## Herramientas
`python3 -m uft init`, `ingest`, `show ID` y `export`; `ResearchStore.recover`
para recuperación acotada. Usa `pdftxt` si está disponible para PDF y conserva
páginas; detecta otras herramientas documentales antes de usarlas. La lectura
de BRAIN UFT es de solo lectura y el observador no consulta modelos.

## Entregables
Evento y fuentes identificados, resultado de entrada, lista de impactos,
materiales inaccesibles y siguiente comprobación con archivos reproducibles.

## Aceptación
Repetir la misma entrada no duplica resultados ni alertas. Una fuente cambiada
invalida las revisiones pertinentes; una refutación conserva su estado negativo.
La evidencia importada conserva su régimen y su alcance.

## Errores frecuentes
Confundir un hash con veracidad, registrar un resumen como demostración general,
considerar toda discrepancia una refutación o afirmar novedad sin delimitar búsqueda.

## Colaboración
Pide revisión documental si la versión vigente es ambigua y especialistas si el
impacto requiere reconstruir argumentos fuera de la competencia seleccionada.

## Ejemplo
Tras corregir una convención de firma, crea una versión nueva de la convención,
registra el documento corregido e inspecciona qué derivaciones pasan a revisión.
Si el PDF no se obtuvo, registra esa carencia sin inventar su contenido.
