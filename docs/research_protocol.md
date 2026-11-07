# Investigación integrada y análisis incremental

Este documento complementa el [protocolo científico](scientific_protocol.md).
La meta es generar trabajo técnico revisable para **tres problemas físicos**:
Googly, unificación de campos y cuantización de RG, incorporando tiempo y LQG.
Las hojas originales G1–G5, U1–U5 y GQ1–GQ5 se conservan en
[`data/goals.json`](../data/goals.json). El modelo de reloj es una calibración
adicional del programa QG: no satisface por sí solo ninguno de esos hitos.

## Qué constituye un avance

Un ciclo puede producir una construcción, un teorema parcial, una correspondencia
restringida, una obstrucción, un contraejemplo o una pregunta precisa. La selección
de una teoría final única se mantiene abierta. Nunca se infiere una equivalencia
de una semejanza de acciones, de un grafo conectado o de una votación de agentes.

Cada propuesta usa A–O en `research/*/proposal.md`. Cada informe científico usa
las once secciones y los siete criterios del esquema de `uft.reporting`. Las
definiciones, axiomas matemáticos, postulados físicos, hipótesis auxiliares,
aproximaciones y consecuencias derivadas tienen funciones distintas. Axiomas
consistentes, ejemplos finitos y ausencia de contradicciones detectadas son
afirmaciones distintas de una consistencia relativa o absoluta.

## Ciclo por nueva información

1. Registrar procedencia, versión y huella de la entrada.
2. Clasificar su naturaleza y su estado científico, conservando el original.
3. Detectar duplicados textuales y contradicciones explícitamente identificadas.
4. Recorrer dependencias y conexiones propagantes para determinar el impacto.
5. Formular una pregunta acotada y seleccionar especialistas y presupuesto.
6. Ejecutar derivaciones o cálculos reproducibles y buscar contraejemplos.
7. Obtener una revisión en otra ejecución y registrar las objeciones.
8. Actualizar evidencia y marcar resultados y evaluaciones que requieren revisión.
9. Exportar memoria, documentos, alertas significativas y materiales reproducibles.
10. Parar al resolver el impacto o registrar el siguiente paso pendiente.

Un archivo sin cambios no inicia otra investigación ni dispara una alerta. Un
fallo de evento conserva su entrada; los reintentos son limitados. Cambiar un
enunciado después de un resultado desfavorable exige una versión nueva.

## Mapa de conocimiento y transferencias

Los nodos representan objetos identificados, no solo etiquetas temáticas. Las
aristas tienen uno de ocho tipos: dependencia, implicación, equivalencia,
correspondencia, compatibilidad, incompatibilidad, analogía y conexión propuesta.
Cada enlace conserva mapa, fundamento, hipótesis, fuentes y revisión. La dirección
de una arista propagante es **premisa → dependiente**. En una entidad, en cambio,
`dependencies` enumera sus premisas. No se exige un número de conexiones por nodo.

Antes de una transferencia A o B se comprueban y justifican por separado:

- Mapa explícito y estructura preservada.
- Compatibilidad de hipótesis.
- Dimensiones, unidades, pesos, firma, grupos y representaciones.
- Categoría científica adecuada y condiciones heredadas.
- Ausencia de contradicción con fronteras refutadas o resultados vetados.
- Registro de origen, destino, mapa y estado.

A usa una fuente establecida o un resultado con auditoría vigente. B usa una
hipótesis de trabajo y obliga a `conditional_on` en el destino. Las conclusiones
quedan condicionadas. Una analogía no cuenta como transferencia A. Los ejemplos
DGLA y Yang–Mills proporcionan herramientas de obstrucción; no son un diccionario
entre twistores, Einstein y materia. La correspondencia física sigue pendiente.

## Los siete criterios

| Criterio | Evidencia requerida |
|---|---|
| Coherencia matemática | Objetos, hipótesis, argumentos y alcance exacto de cada verificador. |
| Contrastabilidad | Predicción, auxiliares, régimen, incertidumbre y observación incompatible. |
| Correspondencia | Variables, límite, cálculo, observables, grados de libertad y correcciones. |
| Definiciones operacionales | Magnitud, unidades, medición/inferencia, gauge y límites de acceso. |
| Explicación y unificación | Qué aporta frente a alternativas y qué estructura física relaciona. |
| Parsimonia | Postulados independientes, parámetros, funciones libres y ajustes posteriores. |
| Evaluación no empírica | Premisas, búsqueda de alternativas, conexiones inesperadas y objeciones. |

Estados: «Cumplido en el alcance declarado», «Parcial», «Pendiente», «Incumplido»
y «No aplicable, con justificación». Cumplir un criterio en un modelo finito no lo
cumple en RG completa. No se asignan probabilidades inventadas de verdad.

La discusión de [Dawid](https://arxiv.org/abs/1702.01133) se usa para registrar
argumentos sobre alternativas, conexiones explicativas y antecedentes de éxito;
sus premisas se examinan y no se convierten en datos experimentales. La posición
crítica de [Rovelli](https://arxiv.org/abs/1609.01966) se conserva como desacuerdo
metodológico. [Ellis y Silk](https://www.nature.com/articles/516321a) motivan la
exigencia de explicitar el contraste físico. Acceso y metadatos verificados se
documentan en [`references/epistemology.json`](../references/epistemology.json).

En predicciones probabilísticas se prerregistran población, distribución bajo la
hipótesis, estadístico, regla de decisión, potencia y tratamiento de múltiples
pruebas cuando corresponda. Un resultado improbable aislado no refuta por sí solo
una teoría ni distingue un fallo del modelo de uno de sus auxiliares.

## Convenciones por programa

Googly declara espacios twistoriales, firma, realidad, orientación, dualidad,
pesos, cohomología, gauge, regularidad, integrabilidad, reconstrucción, helicidades
y relación con Einstein. Un (L_\infty\) o una fuente no recupera automáticamente
la segunda helicidad. Lo local y perturbativo conserva esos límites.

Unificación declara sectores, materia, interacciones, representaciones, anomalías,
parámetros, espectro y correspondencias. Lenguaje común, reformulación y unificación
dinámica son categorías distintas. Las candidatas previas no se reinician ni se
promueven automáticamente por haber sido importadas.

Gravedad cuántica declara qué se cuantiza, dominio y producto interno de estados,
observables, restricciones, dinámica, regularización, UV y límite clásico. En el
reloj ideal se diferencia el espacio cinemático del espacio de soluciones
generalizadas; la discreción de un operador cinemático de área no implica tiempo
discreto. El Hamiltoniano de prueba no es el Hamiltoniano completo de LQG.

## Independencia y límites de automatización

Claude y Codex reciben el mismo brief, convenciones, fuentes y presupuesto. Sus
espacios separados se cierran con hashes antes del intercambio. La revisión
cruzada conserva desacuerdos; si falta un informe permanece pendiente. Los
subagentes actuales son ejecuciones diferentes y pueden compartir errores del
mismo modelo. No son arbitraje externo ni confirmación observacional.

El observador automatiza procedencia e impacto. La investigación científica y las
promociones requieren evidencia y revisión registrada. `evidence/automation.json`
distingue mecanismo diseñado, ejecución disponible, configuración de planificador,
prueba realizada, última ejecución y fallos. No se promete vigilancia permanente
cuando solo existe ejecución a demanda.
