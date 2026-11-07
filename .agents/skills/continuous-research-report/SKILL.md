---
name: continuous-research-report
description: Elaborar informes UFT trazables de ciclos por eventos, distinguiendo análisis realizado, automatización comprobada y pendientes científicos.
---

# Informes de investigación incremental

## Propósito y uso
Usa esta habilidad al cerrar un ciclo de investigación o comunicar un cambio
significativo. Sigue el [protocolo](../../../docs/research_protocol.md) y utiliza
el esquema de `uft.reporting`; la palabra «continuo» debe corresponder a un
mecanismo real y delimitado de eventos o programación.

## Entradas
Pregunta y alcance, fuentes accesibles e inaccesibles, estado previo, resultados,
ejecuciones y presupuestos reales, revisión separada, desacuerdos, cobertura,
siete criterios, impactos y estado efectivo del observador o planificador.

## Procedimiento
1. Cubre las once secciones: pregunta y alcance; fuentes; estado previo; análisis
   matemático; análisis físico; conexiones; resultados y evidencia; objeciones;
   impacto sobre los tres objetivos; memoria y alertas; próxima comprobación.
2. Añade las siete filas de evaluación con estado, evidencia, limitaciones y
   siguiente comprobación. Conserva afirmaciones condicionadas y resultados
   negativos; no conviertas el formato editorial en acreditación científica.
3. Diferencia perfiles registrados y seleccionados, agentes ejecutados,
   ejecuciones terminadas y resultados revisados. Identifica modelo y herramientas
   solo cuando se conocen, junto con los límites de independencia de la revisión.
4. Distingue protocolo diseñado, ejecución manual disponible, automatización
   configurada, comprobada, última ejecución satisfactoria y fallos. Un observador
   de archivos no ejecuta una investigación física por sí mismo.
5. Genera alertas solamente por cambios significativos y exporta los archivos
   pertinentes a Descargas mediante los mecanismos existentes. Finaliza con
   hasta cinco pruebas discriminantes y qué cuestionaría cada fallo. Si no hay
   predicciones, identifica qué derivación física falta.

## Herramientas
`python3 -m uft report informe.json --output informes/ciclo.md` valida el esquema;
`python3 -m uft export` conserva memoria y mapa. El observador acotado se ejecuta
con `python3 -m uft watch --max-cycles 1 --max-seconds 60 --quiet`. No actives un
planificador ni repitas llamadas a modelos para generar novedades artificiales.

## Entregables
Informe completo, evidencia enlazada, cambios de memoria y alertas pertinentes,
estado de automatización y siguiente comprobación. Si falta un entorno, conserva
la comparación Claude–Codex como pendiente.

## Aceptación
El informe permite localizar enunciado, hipótesis, archivos, revisión y estado.
Las once secciones y siete criterios tienen contenido acorde a la evidencia.
Sin cambios relevantes, el observador permanece en silencio cuando se solicita.

## Errores frecuentes
Llamar seguimiento 24/7 a un comando manual, contar selección como ejecución,
declarar revisión externa sin evidencia o ocultar una predicción ausente detrás
de una lista de comprobaciones puramente matemáticas.

## Colaboración
Consulta al productor y al auditor para resolver discrepancias de alcance.
Mantén abiertos los desacuerdos que requieran cálculos nuevos o fuentes inaccesibles.

## Ejemplo
Una corrección de firma invalida dos derivaciones: informa el impacto, registra
la alerta y propone reconstruir la primera identidad afectada. Una segunda
observación del mismo archivo no justifica otro ciclo científico.
