---
name: seven-criteria-assessment
description: Evaluar una propuesta UFT mediante siete criterios con evidencia y límites, sin convertir puntuaciones o argumentos no empíricos en confirmación experimental.
---

# Evaluación científica con alcance declarado

## Propósito y uso
Usa esta habilidad para evaluar candidatos o resultados parciales del programa,
conforme al [protocolo](../../../docs/research_protocol.md). Evalúa el dominio
declarado: una comprobación finita no satisface un requisito de RG completa.

## Entradas
Pregunta y dominio, formulación vigente, hipótesis independientes, resultados,
fuentes examinadas, auditorías, alternativas y comprobaciones ejecutadas.
Recupera la entidad mediante `python3 -m uft show ID` cuando exista.

## Procedimiento
Construye una fila para cada criterio del esquema `uft.schema.CRITERIA`:

1. **Coherencia matemática:** separa ausencia de fallos detectados, identidad
   algebraica, ejemplo, existencia, consistencia relativa y verificación formal.
2. **Contrastabilidad:** precisa predicción, auxiliares, régimen, incertidumbre,
   medición incompatible y qué parte quedaría cuestionada. En pruebas aleatorias
   especifica modelo estadístico y regla de decisión; un suceso raro no basta.
3. **Correspondencia:** exige variables, límite, cálculo, observables, grados de
   libertad y error retenido; no basta una ecuación visualmente semejante.
4. **Definiciones operacionales:** relaciona magnitudes físicas con unidades,
   medición o inferencia y gauge. No exijas medir cada símbolo auxiliar.
5. **Explicación y unificación:** diferencia lenguaje común, analogía,
   correspondencia, reformulación, unificación dinámica y equivalencia física.
6. **Parsimonia:** identifica postulados, parámetros, funciones arbitrarias y
   ajustes posteriores; compara alternativas de alcance semejante.
7. **Evaluación no empírica:** documenta búsqueda de alternativas, conexiones
   inesperadas y antecedentes metainductivos, con objeciones y límites propios.

Asigna «Cumplido en el alcance declarado», «Parcial», «Pendiente», «Incumplido»
o «No aplicable, con justificación». Cada fila incluye evidencia concreta,
limitaciones y la siguiente comprobación. La falta de evaluación es pendiente.

## Herramientas
`ResearchStore.set_assessment` conserva las siete filas y su revisión. Para un
informe usa `python3 -m uft report informe.json --output informe.md`; el esquema
de sus once secciones está en `uft.reporting.REPORT_SECTIONS`. Exporta con
`python3 -m uft export` para conservar la evaluación junto al mapa.

## Entregables
Tabla de siete criterios, referencias a pruebas y auditorías, incertidumbres
localizadas y hasta cinco pruebas discriminantes; si no hay predicciones,
declara el puente físico que falta construir.

## Aceptación
Ningún criterio cumplido carece de evidencia. No hay probabilidades inventadas
de verdad ni una puntuación agregada que oculte un fallo esencial. La evidencia
no empírica no se denomina confirmación experimental.

## Errores frecuentes
Declarar consistencia absoluta tras pruebas automáticas, equiparar elegancia con
observación, contar hipótesis por longitud del texto o llamar unificación a una
suma de acciones sin analizar materia, interacciones y observables.

## Colaboración
Solicita análisis funcional para dominios, revisión física para espectros y
contrastes, o metodología estadística cuando las predicciones sean probabilísticas.

## Ejemplo
En un reloj de dimensión finita, la conservación de norma puede cumplir un
control acotado de dinámica. La recuperación de Einstein sigue pendiente hasta
mostrar variables, restricciones, límite y observables pertinentes.
