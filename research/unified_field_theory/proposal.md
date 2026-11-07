# UFT-UF: acoplamientos locales, cohomología y contenido físico

Versión 0.1 · 2026-11-06 · Programa condicionado, con banco Yang–Mills conocido.
Objetivo: una teoría que relacione de forma dinámica gravedad, gauge y materia.
Nivel alcanzado: filtro BV de deformación y un ejemplo algebraico que pasa o
falla Jacobi. El modelo SU(2) es antecedente establecido, no una teoría original.
Los argumentos locales están en **DERIVACIÓN PENDIENTE DE AUDITORÍA** y los
residuos calculados son **EVIDENCIA SIMBÓLICA O NUMÉRICA**.

## A. Nombre de la teoría

**Programa de acoplamiento físico mediante obstrucciones locales (AFOL).**
Busca discriminar interacciones compatibles antes de afirmar unificación.
Un lenguaje cohomológico compartido no basta para integrar sectores físicos.
El enfoque de deformar la ecuación maestra tiene antecedentes explícitos.
([Barnich–Henneaux](https://arxiv.org/abs/hep-th/9304057))

## B. Motivación física o matemática

Una estructura común puede ocultar incompatibilidades en restricciones,
representaciones y signos cinéticos. El primer banco exige que el acoplamiento
cúbico de vectores sea prolongable sin romper la estructura gauge. Separamos
algebra local, espectro físico, estabilidad y contraste experimental.
Las obstrucciones BV pertenecen a funcionales **locales**: permitir no localidad
cambia el problema y no puede hacerse para evitar un contraejemplo sin avisar.
([Barnich–Henneaux, §§4–5](https://arxiv.org/html/hep-th/9304057v1))

Las candidatas K1–K4 y la prioridad vigente K3>K2>K1 se conservan como información
del proyecto. No se incorporan aquí sus acciones ni sus afirmaciones no
revalidadas como premisas. AFOL añade un banco independiente; no borra
contraejemplos ni convierte una EFT candidata en una teoría UV.

## C. Problema que resuelve

Pregunta mínima: ¿basta un tensor cúbico totalmente antisimétrico con métrica
interna positiva para construir un álgebra gauge de Lie? No. Un ejemplo de
dimensión cinco conserva esa métrica y falla Jacobi. Un control SU(2) sí pasa.
Esto localiza un requisito que la apariencia geométrica del acoplamiento
no garantiza. El programa de unificación requiere mucho más que superarlo.

Éxito futuro: acción con sectores identificados, representaciones de materia,
restricciones coherentes, régimen cuántico controlado, recuperación de Einstein
y gauge pertinente, y predicciones discriminantes. Ninguna de estas metas
completas se declara alcanzada por el filtro algebraico.

## D. Postulados básicos

| ID | Clase | Enunciado y función | Dominio y prueba |
|---|---|---|---|
| UF-D1 | Definición | \(d\) vectores reales \(A_\mu^a\) en Minkowski3+1, firma \((-+++)\), métrica interna \(\delta_{ab}\). | Banco sin gravedad dinámica ni materia. |
| UF-P1 | Postulado físico del banco | Límite desacoplado: suma de Maxwell, energía positiva tras reducir gauge. | Revisar cinética y polarizaciones físicas. |
| UF-H1 | Hipótesis auxiliar | Se buscan deformaciones locales polinómicas, con a lo sumo dos derivadas en el modelo Yang–Mills, analíticas formalmente en \(g\). | No se garantiza convergencia ni se permiten operadores no locales para eludir fallos. |
| UF-D2 | Definición | \(F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu+g f^a{}_{bc}A^b_\mu A^c_\nu\), \(f_{abc}=f_{[abc]}\). | La antisimetría garantiza métrica invariante; Jacobi es un test adicional. |
| UF-A1 | Axioma matemático BV | Funcionales locales módulo derivadas totales, antibracket de grado fantasma+1, \((S_0,S_0)=0\). | Campos/antifields y condiciones de contorno declaradas; \(s=(S_0,\cdot)\) nilpotente. |
| UF-P2 | Hipótesis del programa | Una extensión futura incorporaría gravedad y materia conservando cohomología física y ausencia de anomalías incompatibles. | Pendiente: construir la extensión y verificar su contenido; no se supone como resultado. |

Seis entradas organizan el banco y el destino. Jacobi, estabilidad y anomalías
son criterios que una candidata debe superar; no se añaden después de observar
fallos para declarar que toda candidata los cumplía.

## E. Objetos matemáticos fundamentales

El banco tiene vectores bosónicos reales, fantasmas impares \(c^a\),
antifields \(A^{*\mu}_a,c^*_a\), números fantasma
\(\mathrm{gh}(A,c,A^*,c^*)=(0,1,-1,-2)\).
En este banco puramente bosónico, la paridad de Grassmann coincide con el
número fantasma módulo dos. Esa hipótesis es necesaria para el desplazamiento
a una DGLA ordinaria que se usa abajo. Si se incorpora materia fermiónica de
número fantasma cero, hay que conservar una supergraduación adicional; no basta
desplazar el número fantasma para aplicar sin cambios ese argumento.
Se usan funcionales integrados con variaciones compactamente soportadas, de
modo que se identifican derivadas totales. Toda afirmación sobre cohomología
es en esta categoría local y con esa libertad gauge.

Con \(c=\hbar=1\), \([x]=-1\), \([A]=1\), \([F]=2\), \([g]=0\).
Una asignación compatible con BRST de dimensión cero es
\([c]=0,[A^*]=3,[c^*]=4\). Cada término de la densidad tiene dimensión cuatro.
Métrica interna positiva y constantes reales son condiciones de realidad.
Gravedad futura usaría \(e^I,\omega^{IJ}\) reales lorentzianos, pero esos
campos no existen en el banco ejecutado.

Grados de libertad: cuando \(f\) define Lie y se reduce gauge de Yang–Mills
sin masa, hay dos polarizaciones por generador en el régimen perturbativo
regular. El control SU(2) tiene seis polarizaciones; no incluye gravitones,
fermiones ni sectores del Modelo Estándar.

## F. Ecuaciones centrales

Definimos antibracket por la convención que hace \(s=(S_0,\cdot)\) y
\(s^2=0\). La ecuación maestra clásica y su expansión formal son
\[
\tfrac12(S,S)=0,\qquad S=S_0+gS_1+g^2S_2+\cdots,
\]
\[
sS_1=0,\qquad sS_2=-\tfrac12(S_1,S_1).
\tag{UF.1}
\]
Un representante consistente, **si \(f\) cumple Jacobi**, es
\[
S_{\rm YM}^{\rm BV}=\int d^4x\left[
-\tfrac14F^a_{\mu\nu}F_a^{\mu\nu}
+A^{*\mu}_a(D_\mu c)^a-\tfrac g2c^*_a f^a{}_{bc}c^bc^c\right],
\tag{UF.2}
\]
con \(D_\mu c^a=\partial_\mu c^a+g f^a{}_{bc}A_\mu^bc^c\).
Así \(S_0\) es Maxwell más \(A^*\partial c\); el término cúbico bosónico de
\(S_1\) es \(-\tfrac12f_{abc}F_0^{a\mu\nu}A_\mu^bA_\nu^c\).
La completitud de (UF.2) **no se afirma** para el tensor malo de dimensión cinco.

La condición algebraica que se calcula es
\[
J(e_i,e_j,e_k):=[e_i,[e_j,e_k]]+[e_j,[e_k,e_i]]+[e_k,[e_i,e_j]]=0.
\tag{UF.3}
\]
El ejemplo malo fija las únicas componentes independientes
\(f_{012}=1,\ f_{034}=1\), extendidas por antisimetría completa y cero en las
demás. Los índices de este ejemplo empiezan en cero.

## G. Teoremas principales

**UFT-UF-001, derivación pendiente de auditoría.** Para UF-A1, la obstrucción
de segundo orden es la clase de \((S_1,S_1)/2\) en cohomología local de grado
fantasma uno. Debe anularse para que exista un funcional **local** \(S_2\).
La afirmación se restringe al formalismo y grado indicados.
([Barnich–Henneaux, §4](https://arxiv.org/html/hep-th/9304057v1))

**UFT-UF-002, derivación pendiente de auditoría.** El tensor de cinco dimensiones
anterior da un corchete antisimétrico que preserva \(\delta\), pero
\(J(e_1,e_2,e_3)=-e_4\ne0\). No define álgebra de Lie. Por tanto no permite
presentar (UF.2) como la completación Yang–Mills asociada a ese corchete.

**UFT-UF-003, derivación pendiente de auditoría.** En dimensión tres,
\(f_{012}=1\) totalmente antisimétrico sí satisface Jacobi. Es el control
compacto \(\mathfrak{su}(2)\) con normalización de base apropiada.

**UFT-UF-004, afirmación de control REFUTADA.** «Toda forma cúbica totalmente
antisimétrica se extiende automáticamente a un álgebra gauge de Lie» falla
por UFT-UF-002. Esto no es un no-go para todas las teorías gauge superiores,
álgebras abiertas o extensiones con campos nuevos.

## H. Esbozo de demostraciones

1. **Premisas (B1, A1).** Se fija categoría de funcionales, antibracket y
   \(s^2=0\). La identidad de Jacobi graduada del antibracket implica
   \(s(S_1,S_1)=0\) cuando \(sS_1=0\).
2. **Obstrucción (B2–B4).** Expandir \((S,S)/2\) y agrupar potencias de \(g\)
   da UF.1. Una solución local \(S_2\) existe exactamente si el cociclo del
   lado derecho es una frontera local. Usar un primitivo no local viola
   UF-H1 y no demuestra el resultado solicitado.
3. **Contraejemplo (B3–B5).** Con la forma cúbica indicada,
   \([e_1,e_2]=e_0\), \([e_3,e_0]=-e_4\) y
   \([e_2,e_3]=[e_3,e_1]=0\). Sustituir en UF.3 da \(-e_4\).
   La invariancia métrica se comprueba por
   \(\langle[e_i,e_j],e_k\rangle+\langle e_j,[e_i,e_k]\rangle
   =f_{ijk}+f_{ikj}=0\). Son propiedades distintas.
4. **Control (B5).** Para dimensión tres el corchete es el producto vectorial
   de componentes, cuya Jacobi resulta de la contracción de dos símbolos
   \(\epsilon\). El script también comprueba todos los triples de base.
5. **Contenido físico (A3–A7).** Para una verdadera álgebra compacta,
   \(F\mapsto[F,c]\) y métrica invariante hacen gauge invariante la acción.
   La energía clásica de Yang–Mills es \(\int(E^2+B^2)/2\ge0\).
   Cada término de UF.2 tiene dimensión cuatro; \(g\to0\) recupera Maxwell.
   Ninguno de estos pasos introduce gravedad o materia.

No se ha ejecutado un resolvedor BV de la teoría completa: el script verifica
Jacobi y el ejemplo, no la clasificación exhaustiva de deformaciones locales.

## I. Interpretación física

Jacobi controla el cierre de la transformación gauge de Lie del banco. El
contraejemplo muestra que un tensor atractivo e invariante puede fallar una
condición dinámica de coherencia al construir la teoría. Añadir un
\(L_\infty\) puede reorganizar un problema distinto, pero exige declarar
campos, grados de libertad y mapa físico, sin proclamar unificación por el nombre.

Para incorporar gravedad, una primera referencia sería Einstein–Yang–Mills:
\[
\int d^4x\sqrt{-g}\left[\frac{M_{\rm Pl}^2}{2}R-\frac14F^a_{\mu\nu}F_a^{\mu\nu}\right].
\]
Es un acoplamiento conocido con un parámetro gravitatorio y otro gauge.
**No es una propuesta original ni unifica por sí mismo los parámetros,
representaciones y origen de sectores.** Aquí se usa solo como futuro blanco
de correspondencia; no se cuantiza ni se simula.

## J. Límites y casos especiales

| Régimen | Lo que se recupera | Lo pendiente |
|---|---|---|
| \(g=0\), métrica fija | Maxwell desacoplado. | No hay gravedad dinámica. |
| \(f=\epsilon\) en tres dimensiones internas | Control SU(2) de Yang–Mills. | Cuantización y observables no se calculan aquí. |
| \(f_{012}=f_{034}=1\) en cinco | Métrica invariante, Jacobi fallida. | Esa ansatz gauge de Lie debe rechazarse o modificarse explícitamente. |
| Adición de Einstein–Hilbert | Blanco conocido de acoplamiento. | No fija una unificación ni control UV. |
| Materia quiral | No incorporada. | Representaciones, anomalías, masas y parámetros. |

## K. Predicciones observables

**Sin predicciones nuevas de unificación.** El banco proporciona condiciones
matemáticas de rechazo, no nuevas constantes de acoplamiento ni masas. Las
predicciones de Yang–Mills conocido no se atribuyen al programa como hallazgos.
Para contrastar una extensión se deben derivar secciones eficaces, espectro,
parámetros y errores en un régimen comparado con datos.

## L. Posibles experimentos o tests matemáticos

1. Contracción independiente de Jacobi; el residuo \(-e_4\) debe reproducirse.
2. Comprobar invariancia de \(\delta\) por separado para detectar el razonamiento
   incorrecto «invariante implica Lie».
3. Construir un representante local BV \(S_1\) y la clase de \((S_1,S_1)/2\),
   sin cambiar a funcionales no locales cuando aparezca una obstrucción.
4. Incorporar una representación concreta de materia y auditar anomalías.
5. Establecer el límite Einstein–Yang–Mills, contando observables y restricciones.

## M. Relación con teorías existentes

El banco es Yang–Mills y su formulación BV, ambos antecedentes. No se propone
como sustituto de cuerdas, LQG ni del Modelo Estándar. El interés del programa
está en imponer filtros comunes a candidatas y conservar contraejemplos.
([Barnich–Henneaux](https://arxiv.org/abs/hep-th/9304057))

**Puente matemático con UFT-GO-001 (UFT-X-001).** Para funcionales locales
BV \(\mathcal F\) con paridad de Grassmann igual a número fantasma módulo dos
(como en el banco bosónico), definir \(L^n=\mathcal F^{\mathrm{gh}=n-1}\),
\(d=(S_0,\cdot)\), \([\, ,\, ]=(\, ,\, )\). El desplazamiento convierte el
antibracket de grado fantasma+1 en corchete de grado cohomológico cero.
Entonces dos vértices cerrados \(S_{1A},S_{1B}\) son elementos de \(Z^1(L)\);
la obstrucción mixta está en \(H^2(L)=H^1(\mathcal F,s)\).
Este mapa preserva diferencial, corchete y grado. Se aplica solo si los
vértices locales, categoría y condiciones de contorno cumplen las hipótesis.
No identifica el ejemplo finito de Googly con campos gravitatorios ni une
físicamente las metas. Su clasificación y revisión quedan registradas como
correspondencia matemática condicionada, nunca equivalencia física.

## N. Debilidades, riesgos y puntos abiertos

- No hay acción original que unifique gravedad, gauge y materia.
- Una obstrucción nula de segundo orden no garantiza todos los órdenes.
- La cohomología local depende de dimensión, derivadas y campos permitidos.
- Jacobi fallida refuta la ansatz gauge de Lie, no todas las extensiones posibles.
- No se han calculado renormalización, anomalías cuánticas ni consecuencias nuevas.
- No se importan sin auditar los espectros, fantasmas o cortes EFT de K3.
- La parsimonia actual refleja un banco pequeño; no se compara como superior
  a una teoría mucho más amplia.
- La aspiración de novedad exige construir y comparar algo que exceda estos
  resultados conocidos; ese paso sigue abierto.

## O. Versión resumida en 10 líneas

1. AFOL busca acoplamientos físicos mediante filtros locales.
2. El objetivo final relaciona gravedad, gauge y materia.
3. El banco actual solo contiene vectores de Yang–Mills.
4. BV organiza las deformaciones de la ecuación maestra.
5. El segundo orden exige una clase local exacta.
6. Antisimetría total garantiza una métrica invariante.
7. Esa propiedad no garantiza la identidad de Jacobi.
8. Un ejemplo de cinco dimensiones da residuo \(-e_4\).
9. SU(2) proporciona un control que sí satisface Jacobi.
10. Unificación dinámica, materia, UV y predicciones nuevas siguen pendientes.
