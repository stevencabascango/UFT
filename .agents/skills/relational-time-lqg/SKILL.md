---
name: relational-time-lqg
description: Estudiar relojes relacionales en modelos LQG delimitados y auditar sus estados, restricciones y unidades sin atribuirles dinámica completa de relatividad general.
---

# Tiempo relacional en modelos de bucles

## Propósito y uso
Úsala al construir o revisar un reloj interno, su evolución y su relación con
variables geométricas. Consulta el [protocolo](../../../docs/research_protocol.md)
y `research/quantum_gravity/proposal.md`. Distingue reloj ideal, sistema reducido,
modelo a grafo fijo y una cuantización completa de RG.

## Entradas
Grafo y representaciones, espacio cinemático, variable de reloj, producto interno,
operadores y dominios, restricciones, Hamiltoniano propuesto y justificación,
unidades, régimen y observables relacionales que se compararán.

## Procedimiento
1. Explicita qué se cuantiza y qué restricciones se resolvieron. Un intertwiner
   SU(2) satisface Gauss en el nodo; eso no resuelve las restricciones de
   difeomorfismos ni el Hamiltoniano de RG.
2. Para el reloj ideal `C = p_T + H`, especifica la medida de
   `L²(R,dT) ⊗ H_s`, autoadjunción y dominio. Las soluciones de evolución pueden
   ser generalizadas: no las presentes como estados normalizables en todo T.
   Define por separado el producto interno físico y sus hipótesis.
3. Verifica evolución, norma y observables dentro del sector declarado. Si
   `H = κ Q` y Q es adimensional, conserva `[κ] = energía` y el cociente
   `H ΔT / ℏ` adimensional. Identifica un Hamiltoniano elegido de prueba como tal.
4. Para relojes físicos comprueba monotonía, puntos de retorno, resolución,
   fluctuaciones, retroacción y restricciones. Un reloj cuadrático puede exigir
   ramas y no proporciona automáticamente evolución global en T.
5. Busca fallos con operadores no autoadjuntos y límites donde el reloj deje de
   servir. Declara qué falta para cambio de grafo, cierre de restricciones,
   regularización UV, materia y recuperación semiclásica de Einstein.

## Herramientas
`python3 -m uft team "LQG relational time constraints" --programme quantum_gravity`
selecciona perfiles sin ejecutarlos. `python3 -m uft cycle --output .uft/reloj-nuevo`
ejecuta modelos finitos y un comprobador separado. `--sympy` requiere `scipython`
disponible. Usa una salida nueva para preservar ejecuciones anteriores.

## Entregables
Estados, dinámica y observables definidos; cálculo reproducible con unidades;
caso de fallo; límites de reloj y de restricciones; siguiente prueba que acerque
el modelo al problema físico sin declarar cumplidos los hitos GQ1–GQ5.

## Aceptación
La afirmación central recibe revisión en otra ejecución. Se distingue evidencia
finita, demostración bajo hipótesis, verificación formal y contraste físico.
La discreción de área no se convierte en discreción temporal.

## Errores frecuentes
Confundir simetría con autoadjunción, usar la norma cinemática para soluciones
generalizadas, identificar Gauss con todas las restricciones o inventar que un
Hamiltoniano finito reproduce Einstein sin construir su límite.

## Colaboración
Requiere análisis funcional para dominios no acotados, relatividad para el
límite clásico y especialistas en LQG para restricciones y refinamiento de grafo.

## Ejemplo
Audita un nodo de cuatro espines 1/2 y un Hamiltoniano hermítico de prueba con
reloj ideal. Verifica conservación de norma y un contraejemplo no hermítico;
registra que esa prueba no establece la dinámica completa de LQG.
