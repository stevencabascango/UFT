# Revisión científica crítica del ciclo inicial UFT

ID: UFT-AUD-SCI-001 · Borrador de auditoría interna por ejecución separada.
La versión examinada y sus hashes se conservan en
`evidence/scientific-review.json`. Revisión solicitada por el propietario del
proyecto para estos materiales; no es arbitraje externo, dictamen de revista,
evaluación de 5.000 capacidades individuales ni verificación formal.

## 1. Pregunta y alcance

Se examina si los tres bancos mínimos están bien definidos, si sus argumentos
y cálculos coinciden y si el texto conserva el alcance real de la evidencia.
Los programas pretenden investigar Googly, unificación y gravedad cuántica con
tiempo/LQG; aquí se revisan resultados finitos y lemas condicionados. No se
evalúa una teoría completa de ninguno de esos dominios.

## 2. Fuentes y materiales examinados

Se leyeron las tres propuestas A–O, los scripts productor y auditor independiente,
sus salidas, la auditoría matemática y los contratos de la capa `uft/`. El
registro JSON identifica las versiones exactas; cualquier cambio relevante
requiere revisar su impacto antes de reutilizar el veredicto.

Se consultaron las fichas primarias de [Manetti](https://arxiv.org/abs/math/0507284),
[Barnich–Henneaux](https://arxiv.org/abs/hep-th/9304057),
[Giesel–Thiemann](https://arxiv.org/abs/1206.3807) y
[De Pietri–Rovelli](https://arxiv.org/abs/gr-qc/9602023). Se comprobó en el HTML de
[Mason–Skinner, §3.1](https://arxiv.org/html/0808.3907v2) la convención de pesos
2 y −6 para las helicidades −2 y +2. Se examinó además la expansión de la
ecuación maestra en el HTML de Barnich–Henneaux. Esa consulta limitada no es una
revisión exhaustiva ni acredita prioridad o novedad de los bancos.

## 3. Estado previo

Las demostraciones propuestas estaban pendientes de auditoría; las salidas
computacionales eran evidencia simbólica o numérica. Tres afirmaciones de control
deliberadamente falsas estaban refutadas. Esta revisión preserva su refutación.
Un archivo con `passed: true` no cambia por sí mismo la categoría científica de
un enunciado ni prueba sus extensiones físicas.

## 4. Análisis matemático

Se reconstruyó con SymPy el operador completo sobre
\((\mathbb C^2)^{\otimes4}\), sumando los seis productos de Pauli con el signo
de las permutaciones. En la base no ortonormal escrita por el productor se
obtuvieron exactamente

\[
G=\begin{pmatrix}1&0\\0&3\end{pmatrix},\qquad
Q=\begin{pmatrix}0&-3i/4\\i/4&0\end{pmatrix},\qquad
Q^2=\frac3{16}I,\qquad Q^\dagger G-GQ=0.
\]

También se comprobó que la imagen permanece en el subespacio y que el operador
completo es hermitiano. El cálculo está registrado en el JSON de esta revisión.
El argumento por descomposición de representaciones da dos singletes; el auditor
matemático lo reconstruye además como núcleo de un operador de subida de rango
cuatro sobre el sector de peso cero de dimensión seis.

Para el reloj se revisó el paso decisivo: diagonalizar un (H) finito autoadjunto
reduce la restricción a EDO escalares y da
\(\Psi(T)=\exp[-iH(T-T_0)/\hbar]\psi_0\). La norma constante de una solución
no nula impide que sea (L^2(dT)). El producto por evaluación se define en el
espacio de soluciones generalizadas y no se obtiene restringiendo el producto
cinemático. El dominio (H^1(\mathbb R)\otimes\mathcal H_\gamma\), la
autoadjunción y el carácter ideal del reloj están explicitados.

Se comprobó algebraicamente que el término mixto de Maurer–Cartan es
\(db+[a_+,a_-]\), porque los elementos de grado uno tienen corchete simétrico
y los parámetros son de grado cero. La exactitud de ese cociclo es necesaria y
suficiente sobre el anillo truncado declarado. El argumento no elimina
obstrucciones de otros órdenes ni prueba convergencia.

Para el tensor cúbico malo, ([e_1,e_2]=e_0),
([e_3,e_0]=-e_4) y los otros dos corchetes interiores del triple son cero:
el residuo es (-e_4). La compatibilidad con (delta) solo comprueba una
condición distinta. El control de tres dimensiones es la estructura real
compacta habitual de (mathfrak{su}(2)).

Los argumentos cumplen los pasos pertinentes de los Protocolos A/B dentro de
sus dominios. Los pasos físicos aún ausentes se declaran pendientes. Los
cálculos finitos no sustituyen las demostraciones escritas ni se presentan como
verificación Lean.

## 5. Análisis físico

\(J\) y \(q\) son adimensionales, \([\kappa]\) es energía y
\([\hbar]\) es energía multiplicada por tiempo; el ángulo del propagador es
adimensional. La hipótesis (H=H^\dagger) es esencial: el productor da un
contraejemplo con (i\kappa I), y el auditor matemático otro nilpotente.
La positividad del producto físico elegido y la unitariedad finita no establecen
el cierre de las restricciones gravitatorias completas.

La ley de transición de dos niveles es una consecuencia del banco ideal. No fija
un acoplamiento gravitatorio, un observable de Dirac de RG, el comportamiento UV,
un límite continuo o una medida material del tiempo. El carácter constante de
\(|q|\) en este sector y las limitaciones del volumen están reconocidos.

La propuesta twistorial declara las condiciones físicas que faltan al ejemplo
DGLA. El banco Yang–Mills no contiene gravitones ni materia quiral y no se
atribuye nuevas predicciones de unificación. No se detectó una identificación
indebida de esos ejemplos con Einstein, con una solución de Googly o con una
teoría cuántica completa.

## 6. Conexiones justificadas y propuestas

UFT-X-001 es una correspondencia matemática condicionada: el corrimiento
\(L^n=\mathcal F^{\mathrm{gh}=n-1}\) lleva el antibracket BV de grado
fantasma +1 a un corchete de grado cohomológico cero. Se añadió durante la
revisión la hipótesis de paridad de Grassmann igual a número fantasma módulo
dos, válida en el banco bosónico actual. Con fermiones físicos debe conservarse
la graduación adicional o formularse la estructura supergraduada pertinente.

Este mapa entre complejos y grados no identifica el ejemplo DGLA finito con
twistores gravitatorios. La relación física entre los tres programas sigue
propuesta; sus herramientas comunes no aportan por sí solas una equivalencia.

## 7. Resultados y evidencia

**[REGISTRO DE AUDITORÍA] UFT-AUD-SCI-001.** Ejecución revisora:
`uft_final_review`; ejecuciones anteriores productora `uft_physics` y
matemática `uft_math_audit`. Son procesos diferentes del mismo entorno y pueden
compartir familia de modelo, entrenamiento y errores. No se afirma independencia
estadística ni revisión externa. La versión concreta del modelo no fue expuesta
por el runtime y no se inventa.

| ID | Veredicto interno | Alcance obligatorio |
|---|---|---|
| UFT-QG-001 | CONFIRMADO | Cuatro representaciones spin 1/2, acción diagonal SU(2), base declarada. |
| UFT-QG-002 | CONFIRMADO CON CONDICIONES | Orientación, fases, normalización y Gram; sin dinámica gravitatoria completa. |
| UFT-QG-003 | CONFIRMADO CON CONDICIONES | (H) finito autoadjunto constante, reloj ideal lineal y producto por evaluación. |
| UFT-QG-004 | REFUTADO | La afirmación universal sobre matrices finitas falla por contraejemplos explícitos. |
| UFT-GO-001 | CONFIRMADO CON CONDICIONES | Característica cero, DGLA cohomológica y anillo Artin truncado declarado. |
| UFT-GO-002 | CONFIRMADO | Dos DGLA finitas explícitas con clase mixta exacta o no exacta. |
| UFT-GO-003 | REFUTADO | Resolver sectores por separado no garantiza su combinación. |
| UFT-UF-001 | CONFIRMADO CON CONDICIONES | Obstrucción BV de segundo orden en la categoría de funcionales locales especificada. |
| UFT-UF-002 | CONFIRMADO | La 3-forma de dimensión cinco conserva la métrica y viola Jacobi. |
| UFT-UF-003 | CONFIRMADO | Control (mathfrak{su}(2)) real de dimensión tres. |
| UFT-UF-004 | REFUTADO | La antisimetría total no basta para una extensión gauge de Lie. |
| UFT-X-001 | CONFIRMADO CON CONDICIONES | Grados, paridad, localidad y condiciones de contorno compatibles; sin equivalencia física. |

Se ejecutaron los ocho tests del productor y los diez del auditor independiente;
ambas suites pasaron. Son pruebas de esos programas y contratos, no un recuento
de descubrimientos. El ciclo corregido compara expresamente el JSON productor,
su hash y el dictamen del checker. La revisión no realiza promociones automáticas.

## 8. Objeciones y contraejemplos

No se detectó un **ERROR** central en los resultados finitos y lemas delimitados
tras las correcciones. Se localizaron estos **HUECOS** y se solicitó su remedio:

1. **UFT-X-001, graduación BV:** faltaba explicitar la condición de paridad para
   una DGLA ordinaria. Corregido en la propuesta y ficha; su extensión con materia
   fermiónica sigue requiriendo una formulación adecuada.
2. **`uft/cycles.py`:** dos scripts podían terminar satisfactoriamente sin que el
   comando comparase sus resultados. Corregido: checker con `--producer`, revisión
   de `passed`, comparación y SHA, IDs únicos y protección de artefactos existentes.
3. **`ResearchStore.add_link`:** modificar una premisa almacenada en una arista
   propagante no invalidaba sus resultados. Se añadió invalidación transitiva al
   cambiar sus fundamentos. El registro JSON documenta el estado final de la
   comprobación, incluidas transiciones de rechazo de aristas.

La aclaración «energía multiplicada por tiempo» en el informe matemático es una
corrección **MENOR** que evita una lectura ambigua de las unidades de (hbar).
Los contraejemplos científicos deliberados se conservan como refutaciones y no
se convierten en afirmaciones demostradas por una revisión favorable de su detección.

## 9. Impacto sobre los tres objetivos

El trabajo entrega una infraestructura con evidencia de que puede registrar
problemas, construir modelos mínimos, detectar fallos y conservar objeciones.
En física, el alcance sigue siendo parcial: reloj impuesto a grafo fijo,
obstrucción formal sin reconstrucción twistorial y filtro gauge sin unificación.
No se acredita una teoría original completa, una solución de los tres problemas
ni el cumplimiento de los hitos canónicos por estos ejemplos.

## 10. Actualizaciones de memoria y alertas

Esta ejecución escribe únicamente el presente informe y su JSON de evidencia.
El coordinador integra estados, revisiones y alertas en UFT. BRAIN y la memoria
global permanecen sin cambios por este revisor. Las correcciones de ingeniería
y los controles falsos refutados se distinguen de alertas de descubrimiento.

Skills aplicadas: `metacognicion-operativa` para alcance y evidencias;
`investigador-elite` y `colaborador-cientifico` para operadores, dimensiones y
límites físicos; `colaborador-matematica-pura` para DGLA, graduaciones y signos;
`peer-review` para trazabilidad, hallazgos accionables y límites de revisión.
Se aplicaron A/B al contrastar los argumentos. No se delegaron otros agentes.

El uso de procedimientos de revisión se reconoce con la referencia metodológica
verificada de Kassis, Agarwal, He, Patel y Brueckner (2026),
[*Scientific Agent Skills: A Library of Procedural Knowledge for Research
Agents*](https://arxiv.org/abs/2609.00065). Esa referencia documenta herramientas,
no respalda los enunciados físicos de los bancos.

## 11. Próxima comprobación prioritaria

Sustituir el reloj ideal por un sistema material específico y cuantificar sus
errores antes de interpretar la dinámica como gravitatoria. En paralelo, fijar
el complejo geométrico y el mapa de reconstrucción en Googly y una acción con
contenido de materia en unificación. La prioridad científica no es aumentar
automáticamente el número de perfiles ejecutados.

## Evaluación de los siete criterios

Dominio: los bancos y argumentos acotados de esta revisión. Las metas completas
mantienen sus evaluaciones independientes y pendientes.

| Criterio | Estado | Evidencia concreta | Limitaciones y siguiente comprobación |
|---|---|---|---|
| Coherencia matemática | Cumplido en el alcance declarado | Matrices exactas, argumentos y reconstrucción por algoritmos distintos. | No consistencia absoluta ni formalización; reauditar cualquier ampliación. |
| Contrastabilidad | Parcial | Probabilidad de canal del banco y controles que fallan de manera explícita. | Sin predicciones gravitatorias nuevas; derivar una medición física y sus errores. |
| Correspondencia | Parcial | Mecánica unitaria finita, Maxwell al desacoplar y ejemplos DGLA conocidos. | Sin límite a Einstein; construirlo y comparar observables. |
| Definiciones operacionales | Parcial | Canal, proyector, reloj y unidades declarados en el modelo. | El reloj es ideal; incorporar instrumento material y gauge físico. |
| Explicación y unificación | Parcial | Se localizan condiciones necesarias y obstrucciones concretas. | No hay unificación dinámica nueva; fijar sectores y mapas físicos. |
| Parsimonia | Parcial | Bancos pequeños y elecciones libres documentadas. | No comparación entre teorías de igual cobertura; construir alternativas comparables. |
| Evaluación no empírica | Pendiente | Bibliografía y alcance declarados; sin probabilidades de verdad. | No búsqueda exhaustiva ni argumento metainductivo demostrado. |

## Predicciones o pruebas discriminantes

No hay predicciones observacionales nuevas de gravedad, Googly o unificación.
Las siguientes pruebas discriminan los bancos o su implementación:

1. Cambiar el signo de (Q) conservando su cuadrado: debe detectarse contra
   las convenciones declaradas. Un fallo cuestionaría el checker de UFT-QG-002.
2. Usar (H=ikappa I): una norma constante para datos no nulos y (kappa\ne0)
   cuestionaría el cálculo de UFT-QG-004 o el producto utilizado, no LQG.
3. Poner (dz=0): encontrar un primitivo del cociclo (w) en esa DGLA
   cuestionaría UFT-GO-002 o la especificación del complejo.
4. Recalcular Jacobi en ((e_1,e_2,e_3)): obtener cero para el tensor malo
   cuestionaría UFT-UF-002 o las convenciones implementadas.
5. Rechazar o modificar una arista propagante usada como premisa: sus resultados
   y evaluaciones deben quedar pendientes. Un fallo cuestionaría el mecanismo de
   trazabilidad; no establece ni refuta una teoría física.
