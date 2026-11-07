# UFT-QG: tiempo relacional en geometría de lazos

Versión 0.1 · 2026-11-06 · Programa condicionado con modelo finito calculado.
Objetivo: cuantizar RG con estados, observables, dinámica, control UV y límite
semiclásico. Nivel alcanzado: un intertwiner SU(2) con reloj ideal impuesto.
Los argumentos de G–H son **DERIVACIÓN PENDIENTE DE AUDITORÍA** hasta existir
registro separado. La salida del script es **EVIDENCIA SIMBÓLICA O NUMÉRICA**.

## A. Nombre de la teoría

**Programa de geometría de lazos con relojes relacionales controlados (GLRC).**
El nombre identifica una línea de investigación, no una solución de gravedad
cuántica ni novedad bibliográfica acreditada. La deparametrización y las redes
de espín tienen antecedentes: [Giesel–Thiemann](https://arxiv.org/abs/1206.3807)
y [De Pietri–Rovelli](https://arxiv.org/abs/gr-qc/9602023).

## B. Motivación física o matemática

Incorporar tiempo a LQG exige distinguir parámetro, reloj material y observable.
Un espectro geométrico discreto no proporciona por sí mismo un reloj. Elegimos
un banco calculable para reconstruir dinámica, auditar norma y detectar un fallo
antes de generalizar. Los relojes materiales estudiados en LQG son antecedentes;
nuestro Hamiltoniano no se identifica con sus Hamiltonianos gravitatorios.
([Giesel–Thiemann, §§2–4](https://arxiv.org/html/1206.3807v2))

El BRAIN conserva GQ1–GQ5: divergencias EPRL, planitud, recursiones, robustez de
truncaciones y restricciones topológicas. Este banco responde a la petición
específica sobre tiempo. **No sustituye ni cumple ninguno de esos hitos.**
Fuentes del objetivo: META.md y partes/meta_liston.json del BRAIN; esas fuentes
documentales no constituyen pruebas físicas de las propuestas importadas.

## C. Problema que resuelve

Pregunta: ¿hay evolución relacional unitaria en el subespacio singlete de cuatro
espines 1/2 para un Hamiltoniano explícito? Sí, bajo las elecciones siguientes.
Es una especialización de mecánica cuántica unitaria con comprobación exacta.
No resuelve la ligadura Hamiltoniana de RG, difeomorfismos espaciales, cambios
de grafo, materia realista ni recuperación de Einstein.

Éxito del banco: dos singletes independientes, cierre de Gauss, autoadjunción,
solución de la ligadura ideal y producto interno conservado. Cualquier fallo
invalida el banco correspondiente. Pasarlo no acredita dinámica gravitatoria.

## D. Postulados básicos

Seis entradas mínimas, distinguiendo sus clases lógicas.

| ID | Clase | Enunciado y función | Dominio y evaluación |
|---|---|---|---|
| QG-D1 | Definición | \(V=(\mathbb C^2)^{\otimes4}\), producto tensorial estándar; \(\mathcal H_\gamma=\mathrm{Inv}_{SU(2)}V\). | Un nodo, cuatro patas salientes; descomposición de representaciones y Gauss. |
| QG-A1 | Axioma matemático de representación | \(J^a=\sigma^a/2\), \([J^a,J^b]=i\epsilon^{ab}{}_cJ^c\). | Generadores adimensionales; comprobar matrices. |
| QG-P1 | Postulado del modelo | \(T\in\mathbb R\), \(p_T=-i\hbar\partial_T\), \(C=p_T+H_\gamma\). | Reloj ideal impuesto; falta derivación desde RG. |
| QG-P2 | Postulado del modelo | \(H_\gamma=\kappa q\), \(q=\epsilon_{abc}J_1^aJ_2^bJ_3^c\), \(\kappa\in\mathbb R\). | \([\kappa]=\) energía; espectro y simetrías verificables. |
| QG-H1 | Hipótesis auxiliar | Espines, grafo y acoplamiento fijos, sin otros nodos o materia. | No hay límite continuo ni error de truncación controlado. |
| QG-D2 | Definición física del banco | Producto interno de soluciones mediante evaluación en \(T_0\). | Su independencia del instante es consecuencia de autoadjunción. |

No hay aproximación numérica en la matriz. El reloj y la dinámica son elecciones
de modelo; no se ha demostrado una aproximación controlada de RG.

## E. Objetos matemáticos fundamentales

Orden tensorial \(|m_1m_2m_3m_4\rangle\), \(0=\uparrow\), \(1=\downarrow\),
\(\epsilon_{xyz}=+1\) y \(\sigma_y=\left(\begin{smallmatrix}0&-i\\i&0\end{smallmatrix}\right)\).
Gauss: \(G^a=\sum_{\ell=1}^4J_\ell^a\). La condición \(G^a\psi=0\) resuelve solo
rotaciones internas de este nodo, no las demás restricciones de RG.

Base ortonormal:
\[
b_0=\tfrac12(|0101\rangle-|0110\rangle-|1001\rangle+|1010\rangle),
\]
\[
b_1=\tfrac1{\sqrt3}\left[|0011\rangle+|1100\rangle
-\tfrac12(|0101\rangle+|0110\rangle+|1001\rangle+|1010\rangle)\right].
\]
El script usa \(u_0=b_0,u_1=\sqrt3b_1\), Gram \(G=\mathrm{diag}(1,3)\), para
aritmética exacta sobre \(\mathbb Q[i]\). Hermiticidad en esa base es
\(Q^\dagger G=GQ\), no \(Q^\dagger=Q\).

Reloj cinemático: \(\mathcal K=L^2(\mathbb R,dT)\otimes\mathcal H_\gamma\).
\(p_T\) es autoadjunto en \(H^1(\mathbb R)\otimes\mathcal H_\gamma\);
\(H_\gamma\) es acotado y autoadjunto, y la suma tiene ese dominio.
Las soluciones son funciones suaves generalizadas en \(T\); ninguna solución
no nula es normalizable en \(L^2(dT)\). Se introduce el producto físico por
evaluación, sin fingir un núcleo normalizable dentro de \(\mathcal K\).

Unidades: \(T\) tiempo, \(p_T\) energía y \(\hbar\) acción. Los \(J\) son momentos
angulares divididos por \(\hbar\); con momentos dimensionales,
\(q=\epsilon L_1L_2L_3/\hbar^3\). No hay métrica espacio-temporal del banco;
el destino aspiracional es 3+1 lorentziano \((-+++)\), todavía sin reconstrucción.

## F. Ecuaciones centrales

\[
Q_{\{u\}}=\begin{pmatrix}0&-3i/4\\i/4&0\end{pmatrix},\qquad
Q_{\{b\}}=\frac{\sqrt3}{4}\sigma_y,\qquad Q^2=\frac3{16}\mathbf1.
\tag{QG.1}
\]
\[
(-i\hbar\partial_T+H_\gamma)\Psi(T)=0,\qquad
\Psi(T)=e^{-iH_\gamma(T-T_0)/\hbar}\psi_0.
\tag{QG.2}
\]
\[
U=\cos\theta\,\mathbf1-i\sin\theta\,\sigma_y,\qquad
\theta=\frac{\kappa\sqrt3(T-T_0)}{4\hbar},\qquad
\langle\Psi,\Phi\rangle_{\rm phys}:=\langle\Psi(T_0),\Phi(T_0)\rangle.
\tag{QG.3}
\]

Como \(|q|=(\sqrt3/4)\mathbf1\), la magnitud de volumen proporcional a
\(\sqrt{|q|}\), con prefactores convencionales, es constante en este sector.
La prueba dinámica usa el proyector de canal \(P_1=|b_1\rangle\langle b_1|\).
Es invariante SU(2); falta identificarlo con un observable de RG completa.

## G. Teoremas principales

**UFT-QG-001, derivación pendiente de auditoría.** Hay exactamente dos singletes,
y los vectores anteriores forman una base ortonormal de Gauss.

**UFT-QG-002, derivación pendiente de auditoría.** \(q\) preserva ese subespacio,
es autoadjunto y cumple (QG.1); su espectro es \(\{\pm\sqrt3/4\}\).
No se fija aquí un operador de volumen completo ni su regularización.

**UFT-QG-003, derivación pendiente de auditoría.** Para todo Hamiltoniano
autoadjunto finito, evaluación en \(T_0\) identifica biunívocamente las soluciones
de (QG.2) con \(\mathcal H_\gamma\). El producto físico es positivo e independiente
de \(T_0\), y \(U\) es unitario. Esto no garantiza relojes globales en RG.

**UFT-QG-004, afirmación de control REFUTADA.** «Toda matriz Hamiltoniana finita
conserva la norma relacional» es falsa: \(K=i\kappa\mathbf1\), \(\kappa\ne0\),
produce \(\|\Psi(T)\|^2=e^{2\kappa(T-T_0)/\hbar}\|\psi_0\|^2\).

## H. Esbozo de demostraciones

Los argumentos son completos para estos enunciados; su aceptación interna
exige auditoría separada. Los pasos identifican Protocolos A y B.

1. **Premisas y dimensión (B1–B3).** De \(1/2\otimes1/2=0\oplus1\), al reagrupar
   (12)(34) solo \(0\otimes0\) y \(1\otimes1\) contienen un singlete, cada uno una
   vez. Los coeficientes escritos dan norma uno, producto cruzado cero y Gauss
   nulo. Dos vectores independientes abarcan el subespacio de dimensión dos.
2. **Operador y simetría (A3, B3).** Una rotación simultánea preserva \(\epsilon\);
   por tanto \(q\) conmuta con SU(2). Operadores de patas distintas conmutan y
   cada producto de tres es hermitiano. Multiplicar las seis permutaciones de
   \(x,y,z\), proyectar y aplicar Gram da (QG.1); su cuadrado es \(3/16\).
3. **Dinámica (A3, B3–B4).** Diagonalizar \(H\) por el teorema espectral finito
   reduce a \(i\hbar\dot\Psi_j=E_j\Psi_j\). Integración con condición inicial da
   \(e^{-iE_j(T-T_0)/\hbar}\Psi_j(T_0)\), única para todo \(T\).
4. **Norma (B4).** La derivada del producto interno de dos soluciones se anula
   por \(H=H^\dagger\); equivalentemente cada factor espectral tiene módulo uno.
   Evaluación es invertible por el paso 3. Una solución no nula tiene norma
   constante positiva, cuya integral en toda \(\mathbb R\) diverge.
5. **Verificaciones (A4–A7, B5).** \(\kappa\Delta T/\hbar\) es adimensional;
   \(\kappa\to0\) da \(U=\mathbf1\) y \(T\to T_0\) recupera la condición inicial.
   Cambiar orientación \(q\to-q\) invierte \(\theta\), conservando norma.
   Sustituir \(H\) por \(i\kappa\mathbf1\) da UFT-QG-004.
   No existe aquí un límite \(\hbar\to0\) que recupere RG con espines fijos.

## I. Interpretación física

Dentro del banco \(P_{0\to1}(T)=\sin^2\theta\), con preparación \(b_0\) y medición
del canal \(b_1\). Es una probabilidad condicional del modelo, no una predicción
astrofísica. Clásicamente \(\{T,C\}=1\); un lapse de signo fijo da monotonía
para este reloj lineal, sin probarla en otras teorías.

El reloj ideal tiene espectro continuo y \(p_T\) no acotado inferiormente.
No están especificadas resolución, fluctuaciones ni retroacción realistas.
No se deducen precisión infinita material, flecha termodinámica, discreción
temporal, causalidad local o independencia de la elección de reloj.

## J. Límites y casos especiales

| Caso | Resultado | Alcance |
|---|---|---|
| \(\kappa=0\) | Estado constante. | Banco sin dinámica. |
| Cambio unitario de base y observables | Mismas probabilidades. | Equivalencia en dimensión dos. |
| \(\theta=\pi/2\) | \(P_{0\to1}=1\), norma uno. | Test finito exacto. |
| \(C=p_T^2/(2M)+M\omega^2T^2/2+H-E\) | \(\{T,C\}=p_T/M=0\) en retornos. | La reducción lineal global deja de estar justificada. |
| Cambio de grafo/espines | No calculado. | Faltan compatibilidad, límite y error. |

## K. Predicciones observables

**No hay predicciones observacionales gravitatorias derivadas.** La ley de
dos niveles es contrastable si se implementan exactamente ese Hamiltoniano y
medición; un fallo cuestiona el banco o su implementación, no LQG o RG.
Para una predicción gravitatoria faltan reducción desde dinámica física,
calibración de \(\kappa\), observables relacionales y comparación con datos.

## L. Posibles experimentos o tests matemáticos

1. Reconstrucción independiente por Clebsch–Gordan; discrepancia de signo exige
   revisar orientación y base.
2. Hamiltoniano no hermitiano; exigir rechazo de conservación universal.
3. Reloj con retorno; localizar el fallo de monotonía.
4. Dos nodos, Gauss y álgebra de restricciones; detener la interpretación
   gravitatoria si no se fija el cierre de esa álgebra.
5. Reloj material concreto; comparar con el ideal incluyendo errores.

Reproducción: scipython scripts/science_examples.py --sympy --output
research/calculations/first_cycle.json. El núcleo funciona también con Python
estándar y aritmética racional; SymPy repite una identidad matricial.

## M. Relación con teorías existentes

La cinemática SU(2) pertenece al repertorio de LQG y el reloj lineal a sistemas
deparametrizados. Compartirlos no identifica \(\kappa q\) con la dinámica de
Einstein. Deben compararse restricciones y observables, además del espacio
de representaciones. Las fuentes sustentan los antecedentes; el cálculo
se ofrece aquí sin reclamar prioridad.
([De Pietri–Rovelli](https://arxiv.org/abs/gr-qc/9602023),
[Giesel–Thiemann](https://arxiv.org/abs/1206.3807))

No se establece puente físico con las otras propuestas. Compartir técnicas
cohomológicas es metodológico hasta construir un mapa compatible de complejos.

## N. Debilidades, riesgos y puntos abiertos

- \(\kappa\) es libre y no se identifica con una constante gravitatoria.
- Un nodo y espines fijos no contienen dinámica local completa de RG.
- El reloj ideal evita dificultades que debe afrontar uno físico.
- La dinámica depende de orientación; no se afirma invariancia bajo todas las
  permutaciones ni derivación desde una acción covariante.
- Una matriz acotada no prueba control UV de una teoría de campos.
- Faltan continuo, Einstein, materia, anomalías de difeomorfismos y predicciones.
- La revisión de otro proceso del mismo modelo es interna y puede compartir
  sesgos; la comparación Claude–Codex conserva su estado operativo real.

## O. Versión resumida en 10 líneas

1. GLRC es un programa condicionado sobre tiempo en geometría de lazos.
2. El objetivo final es cuantizar RG; el banco actual es finito.
3. Cuatro espines 1/2 tienen dos singletes.
4. El Hamiltoniano toy es \(\kappa\epsilon J_1J_2J_3\).
5. Su matriz y preservación de Gauss se calculan exactamente.
6. Se impone el reloj ideal \(p_T+H=0\).
7. El producto físico evalúa soluciones generalizadas.
8. La norma se conserva para \(H\) autoadjunto.
9. Una matriz no hermitiana da un contraejemplo controlado.
10. Continuo, Einstein, UV y predicciones gravitatorias siguen abiertos.
