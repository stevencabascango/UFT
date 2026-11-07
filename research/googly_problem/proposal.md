# UFT-GO: obstrucciones mixtas y reconstrucción twistorial

Versión 0.1 · 2026-11-06 · Programa matemático condicionado.
Objetivo: una formulación twistorial de gravedad de Einstein que permita ambos
sectores de helicidad con sus condiciones de realidad. Nivel alcanzado: lema
de deformación formal y dos ejemplos finitos; no hay reconstrucción de Einstein.
Pruebas propuestas: **DERIVACIÓN PENDIENTE DE AUDITORÍA**.
Cálculos guardados: **EVIDENCIA SIMBÓLICA O NUMÉRICA**.

## A. Nombre de la teoría

**Programa de obstrucciones mixtas para reconstrucción gravitatoria (OMRG).**
Es una estrategia de investigación con un filtro algebraico calculable.
No se reclama nueva teoría twistorial completa ni prioridad para el lema,
que pertenece a teoría de deformaciones.
([Manetti, §§1–3](https://arxiv.org/html/math/0507284v1))

## B. Motivación física o matemática

El problema abordado no es solo añadir una segunda variable: hay que conservar
integrabilidad, equivalencia gauge y reconstrucción de la dinámica gravitatoria.
Estudiamos primero cuándo dos deformaciones separadas admiten una corrección
mixta. Una obstrucción no nula puede descartar una ruta antes de atribuirle
contenido físico. El argumento no presume que todo el problema de Googly sea
controlado por una DGLA finita. La correspondencia gravitatoria perturbativa
existente debe compararse con su alcance preciso.
([Mason–Skinner, §§3,5](https://arxiv.org/html/0808.3907v2))

BRAIN UFT distingue mecanismos locales, perturbativos y globales y registra
fronteras refutadas. Importarlas conserva sus IDs y sus hipótesis; aquí no se
reasignan nombres a resultados ni se usa una frontera refutada como premisa.
META.md y el manifiesto compartido son antecedentes organizativos.

## C. Problema que resuelve

Pregunta mínima: para \(a_+,a_-\in Z^1(L)\), ¿se puede resolver Maurer–Cartan
sobre el anillo \(\mathbb K[\epsilon,\eta]/(\epsilon^2,\eta^2)\) con término
mixto \(\epsilon\eta b\)? La condición necesaria y suficiente en **ese orden**
es que \([a_+,a_-]\) sea exacto. Resolverla no prueba extensión a todos los
órdenes, convergencia analítica, realidad lorentziana o equivalencia con Einstein.

Éxito físico futuro: un diccionario explícito entre deformaciones y métricas
módulo gauge, compatible con helicidades, condiciones de realidad y dinámica,
con mapas de reconstrucción inversos en el dominio anunciado. El banco actual
no alcanza ese criterio y no debe clasificarse como solución de Googly.

## D. Postulados básicos

| ID | Clase | Enunciado y función | Evaluación y dominio |
|---|---|---|---|
| GO-D1 | Definición | \(L=\bigoplus L^n\) es DGLA sobre cuerpo \(\mathbb K\) de característica cero, graduación cohomológica. | Comprobar signos, Jacobi graduada, \(d^2=0\), regla de Leibniz. |
| GO-A1 | Axioma matemático | \(d:L^n\to L^{n+1}\), corchete grado cero, \([u,v]=-(-1)^{|u||v|}[v,u]\). | Contexto algebraico formal; no fija homogeneidad twistorial. |
| GO-H1 | Hipótesis auxiliar | \(a_\pm\in L^1\), \(da_\pm=0\). | Son direcciones cerradas; todavía no se identifican con helicidades físicas. |
| GO-D2 | Definición | \(A=\mathbb K[\epsilon,\eta]/(\epsilon^2,\eta^2)\), ideal maximal \(\mathfrak m=(\epsilon,\eta)\). | Artin local, dimensión cuatro sobre \(\mathbb K\), conserva \(\epsilon\eta\ne0\). |
| GO-P1 | Hipótesis de programa | Una futura DGLA o \(L_\infty\) relevante controlaría una formulación física delimitada. | Pendiente de construcción y comparación; no se deriva de GO-A1. |
| GO-D3 | Definición | Equivalencia infinitesimal \(a\sim a+du\), \(u\in L^0\); \(\mathrm{MC}\) satisface \(d\alpha+\frac12[\alpha,\alpha]=0\). | Gauge formal; no sustituye difeomorfismos sin un mapa. |

Seis entradas bastan para el banco. No se añade un axioma «equivalencia con
Einstein» porque sería precisamente la conclusión pendiente.

## E. Objetos matemáticos fundamentales

**Contexto físico de referencia, todavía no implementado por el ejemplo.**
En la convención de Mason–Skinner se trabaja con \(M_{\mathbb C}\simeq\mathbb C^4\),
\(PT'=\mathbb{CP}^3\setminus\mathbb{CP}^1\), coordenadas
\(Z=(\omega^\alpha,\pi_{\dot\alpha})\) e incidencia
\(\omega^\alpha=i x^{\alpha\dot\alpha}\pi_{\dot\alpha}\).
Los representantes lineales de helicidad \(-2,+2\) tienen pesos \(2,-6\);
esta identificación y sus convenciones se citan, no se extrapolan.
([Mason–Skinner, §3.1, ecuaciones22–24](https://arxiv.org/html/0808.3907v2))

En el banco \(L^1=\langle x,y,z\rangle\), \(L^2=\langle w\rangle\) y demás
grados cero. Se fija \([x,y]=[y,x]=w\), resto cero, con \(w\) central.
Se comparan \(L_{\rm exact}\) con \(dz=w\) y \(L_{\rm obst}\) con \(d=0\).
Ningún \(x,y,z,w\) lleva por ahora un peso de \(\mathcal O(k)\) ni una
identificación espinorial. Sus coeficientes son adimensionales.

| Requisito gravitatorio | Decisión o pendiente |
|---|---|
| Firma y realidad | Banco formal complejo o racional; no se impone una sección real lorentziana. |
| Orientación y dualidad | Referencia \((-+++)\), orientación fija, \(*^2=-1\) sobre2formas reales; sectores complejos de autovalor \(\pm i\). El banco no identifica sus dos generadores con esos sectores. |
| Cohomología | \(H^n(L)=\ker d/\mathrm{im}\,d\), cohomología del complejo; no confundir grado con peso proyectivo. |
| Gauge | \(L^0=0\) en los ejemplos; el lema general sí incluye cambios exactos. |
| Dominio y regularidad | Solo Artin formal truncado; no se prueban regularidad ni convergencia. |
| Helicidades y grados de libertad | No recuperados del banco; el contexto lineal citado contiene dos helicidades, no una reconstrucción propia. |
| Einstein y mapas | No hay mapa de métrica, solución gauge o inversa de reconstrucción para el banco. |

Si se ensaya el BF twistorial con \(h\) de peso2 y \(\tilde h\) de peso−6,
la medida holomorfa tiene peso4 y el corchete de Poisson peso−2. El peso total
del integrando \(\tilde h(\bar\partial h+\{h,h\}/2)\) es cero. Ese balance
es una condición necesaria, no dinámica de Einstein completa.
([Mason–Skinner, §5, ecuación81](https://arxiv.org/html/0808.3907v2))

## F. Ecuaciones centrales

\[
\alpha=\epsilon a_++\eta a_-+\epsilon\eta b,\qquad
d\alpha+\tfrac12[\alpha,\alpha]
=\epsilon da_++\eta da_-+\epsilon\eta\bigl(db+[a_+,a_-]\bigr).
\tag{GO.1}
\]
\[
\mathfrak o(a_+,a_-) := [[a_+,a_-]]\in H^2(L),\qquad
db=-[a_+,a_-].
\tag{GO.2}
\]
Los dobles corchetes de GO.2 significan clase de cohomología, no otro corchete
de Lie. El término mixto usa el hecho de que el corchete entre elementos de
grado uno es **simétrico**, por el signo de Koszul.

## G. Teoremas principales

**UFT-GO-001, derivación pendiente de auditoría.** Bajo GO-D1–D3 y GO-H1,
existe \(b\in L^1\) que hace \(\alpha\) Maurer–Cartan sobre \(A\) si y solo si
\(\mathfrak o(a_+,a_-)=0\). Su clase depende solo de \([a_+],[a_-]\in H^1(L)\).
El resultado no reclama novedad: se especializa el mecanismo de obstrucciones
del formalismo de deformaciones.
([Manetti, §3](https://arxiv.org/html/math/0507284v1))

**UFT-GO-002, derivación pendiente de auditoría.** En \(L_{\rm exact}\), tomar
\(a_+=x,a_-=y,b=-z\) resuelve GO.1 y \(H^2=0\). En \(L_{\rm obst}\),
\(H^2=\langle[w]\rangle\), de modo que esas direcciones no se extienden juntas.

**UFT-GO-003, afirmación de control REFUTADA.** «La resolución de dos sectores
por separado garantiza su combinación» es falsa en el contexto anterior.
Cada sector satisface MC individual, pero el término mixto en \(L_{\rm obst}\)
es \(\epsilon\eta w\ne0\).

## H. Esbozo de demostraciones

1. **Premisas (B1).** Característica cero permite \(1/2\); \(a_\pm\) cerrados,
   \(d\) derivación y \(\epsilon^2=\eta^2=0\). Los parámetros tienen grado cero.
2. **Expansión (B2–B3).** Los términos con \(\epsilon^2\), \(\eta^2\),
   \(\epsilon^2\eta\) o \(\epsilon\eta^2\) desaparecen; los dos corchetes cruzados
   coinciden, cancelando el factor \(1/2\). Se obtiene GO.1.
3. **Obstrucción (B3–B4).** Leibniz da
   \(d[a_+,a_-]=[da_+,a_-]-[a_+,da_-]=0\). Existe \(b\) exactamente cuando
   ese cociclo es una frontera; esto es GO.2 y equivale a clase nula.
4. **Independencia de representantes (B3).** Para \(a'_+=a_++du\),
   \(a'_-=a_-+dv\), \(u,v\in L^0\), la diferencia de corchetes es
   \[
   d\bigl([u,a_-]-[a_+,v]+[u,dv]\bigr),
   \]
   por Leibniz y \(d^2=0\); por tanto la clase no cambia.
5. **Ejemplos (B5).** En ambas DGLA, Jacobi graduada es cero porque todo
   corchete no nulo es central. \(d^2=0\), y Leibniz se cumple porque \(w\)
   es central. Con \(dz=w\), \(db=-w\); con \(d=0\) no existe tal frontera.
   Esto prueba el contraejemplo sin una búsqueda numérica.
6. **Protocolo A, alcance.** No se deriva una ley física nueva: dimensiones,
   helicidades, contorno y condiciones de realidad de Einstein no están
   representadas en el banco. Los pasos A2, A5–A7 quedan pendientes para la
   aplicación gravitatoria; no se fuerza un cumplimiento ficticio.

## I. Interpretación física

El lema proporciona un filtro: una ruta con obstrucción no nula debe revisarse
o abandonarse bajo esas hipótesis. Si la clase se anula solo se ha superado un
orden de la expansión. El mapa «\(x\) = una helicidad, \(y\) = la otra» **no se
ha construido**. Agregar una fuente, un nuevo campo o un álgebra \(L_\infty\)
no suple ese mapa ni reconstruye grados de libertad gravitatorios.

## J. Límites y casos especiales

| Caso | Consecuencia |
|---|---|
| \([a_+,a_-]=0\) estrictamente | \(b=0\) funciona en el anillo truncado. |
| Corchete exacto no nulo | Se requiere una corrección \(b\); suprimirla produce un fallo. |
| \(H^2(L)=0\) | Toda obstrucción de este orden desaparece; no prueba convergencia. |
| \(H^2(L)\ne0\) | No basta para obstruir toda ruta: hay que calcular la clase concreta. |
| Anillo de potencias completo | Aparecen órdenes superiores y, en modelos \(L_\infty\), corchetes superiores. |

## K. Predicciones observables

**No se han obtenido predicciones físicas.** Hay dos resultados matemáticos
discriminantes: residuo cero en el ejemplo exacto y residuo \(w\) en el
obstruido. Para predecir física falta primero el diccionario gravitatorio,
acción dinámica, realidad y observables. No se inventan probabilidades de
verdad ni se presenta consistencia formal como confirmación experimental.

## L. Posibles experimentos o tests matemáticos

1. Recalcular signos de grado uno y el coeficiente mixto sin consultar el código.
2. Eliminar \(z\) o poner \(dz=0\): la extensión conjunta debe fallar.
3. Sustituir representantes por exactos: la clase debe conservarse.
4. Construir el complejo físico con pesos2/−6 y un mapa de reconstrucción;
   rechazar toda identificación que no preserve los grados y la libertad gauge.
5. Tras el orden mixto, calcular un orden superior y buscar una obstrucción nueva.

## M. Relación con teorías existentes

El control de deformaciones por DGLA y las obstrucciones \(H^2\) son conocidos.
El aporte operativo es un banco pequeño que impide dar por buenas combinaciones
de sectores sin comprobar términos cruzados. Las acciones twistoriales
perturbativas existentes y sus resultados no son invalidados por este ejemplo.
([Manetti](https://arxiv.org/abs/math/0507284),
[Mason–Skinner](https://arxiv.org/abs/0808.3907))

El argumento abstracto sí se aplica al complejo BV local desplazado que
se define en UFT-X-001, UF§M, bajo su hipótesis de paridad y demás condiciones.
Eso es un puente de estructuras graduadas: no es un mapa desde el ejemplo
finito \(x,y,z,w\) hacia la gravedad. El diccionario entre datos twistoriales,
soluciones de Einstein y sus grados de libertad sigue pendiente. Las
conexiones físicas entre metas conservan el estado de **conexión propuesta**.

## N. Debilidades, riesgos y puntos abiertos

- La DGLA finita no es un modelo de espaciotiempo ni de grados gravitatorios.
- Vanishing de una obstrucción es local/formal y de orden limitado.
- No se han fijado realidad lorentziana, reconstrucción global o datos de contorno.
- No se ha demostrado que los sectores físicos admitan el complejo supuesto.
- La topología algebraica o geometría derivada solo se incorpora si resuelve
  una obstrucción identificada; no se fuerza por afinidad de nombres.
- No existe aquí un resultado nuevo que supere los antecedentes de teoría
  de deformaciones. Novedad y solución de Googly permanecen pendientes.

## O. Versión resumida en 10 líneas

1. OMRG estudia obstrucciones mixtas antes de afirmar reconstrucción.
2. El objetivo físico sigue siendo Einstein con ambas helicidades.
3. El banco es una DGLA en característica cero.
4. Se conservan dos parámetros nilpotentes y su producto mixto.
5. El coeficiente mixto de MC es \(db+[a_+,a_-]\).
6. La extensión existe en ese orden si la clase de \(H^2\) se anula.
7. Un ejemplo exacto admite \(b=-z\).
8. Un ejemplo con diferencial cero obstruye la combinación.
9. No se identifican los generadores con helicidades físicas.
10. Reconstrucción, realidad, órdenes superiores y globalidad siguen abiertos.
