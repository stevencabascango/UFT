# Auditoría matemática independiente del primer ciclo UFT

ID: UFT-AUD-MATH-001 · versión 0.1 · 2026-11-06.
Autoría funcional: agente investigador-matematico, ejecución separada de la
productora. Es una **auditoría interna asistida por IA**, con reconstrucción
matemática y código independiente; no revisión externa ni verificación Lean.
El propietario solicitó la creación, revisión y publicación de estos materiales.
No hay encargo de una revista, decisión editorial ni afirmación de credenciales.

## 1. Pregunta y alcance

Se revisan tres afirmaciones delimitadas: un Hamiltoniano sobre el espacio de
intertwiners SU(2) de cuatro espines 1/2, una obstrucción de Maurer–Cartan de
orden mixto y un contraejemplo al cierre de un acoplamiento gauge. La pregunta
es si sus cálculos y conclusiones resisten una reconstrucción distinta y si se
mantienen los límites físicos declarados.

El banco de reloj no cumple por sí mismo GQ1–GQ5 ni produce una cuantización de
RG; la DGLA finita no proporciona datos twistoriales de Einstein; el tensor
cúbico no integra gravedad y materia. La auditoría confirma o refuta únicamente
los enunciados de la tabla de la sección 7.

## 2. Fuentes y materiales examinados

Material productor: scripts/science_examples.py, su salida
research/calculations/first_cycle.json y las propuestas de research/.
La reconstrucción inicial se completó **antes** de leer el código productor.
La segunda fase comparó sus valores exactos, convenciones y argumentos.
El SHA-256 del JSON productor y del auditor ejecutado se conservan en
evidence/science-independent.json. Cambiar una premisa o un artefacto requiere
una nueva revisión; el estado favorable no se transfiere a otra versión.

Fuentes primarias consultadas el 2026-11-06:

- [Giesel y Thiemann, 1206.3807v2](https://arxiv.org/abs/1206.3807v2),
  *Scalar Material Reference Systems and Loop Quantum Gravity*, versión del
  24-06-2012, publicación CQG 32 (2015) 135015. Su ficha y resumen sitúan los
  relojes materiales en LQG; no identifican nuestro Hamiltoniano finito con el
  suyo. No se alega una reproducción de sus resultados completos.
- [Manetti, math/0507284v1](https://arxiv.org/abs/math/0507284v1),
  *Deformation theory via differential graded Lie algebras*, registro del
  14-07-2005; la ficha declara un texto expositivo escrito en 1999. Se verifica
  el antecedente de DGLA/Maurer–Cartan. La prueba mixta utilizada aquí se
  reconstruye explícitamente, sin atribuir al artículo una solución twistorial.
- [Barnich y Henneaux, hep-th/9304057v1](https://arxiv.org/abs/hep-th/9304057v1),
  *Consistent couplings between fields with a gauge freedom and deformations of
  the master equation*, Phys. Lett. B311 (1993) 123–129. La ficha y resumen
  documentan el papel de localidad y obstrucciones BRST; no justifican una
  equivalencia de cualquier álgebra finita con una teoría física unificada.

Alcance bibliográfico: esas fichas y resúmenes fueron consultados; este informe
no afirma una búsqueda exhaustiva ni prioridad científica. No se usaron bases
de pago, evidencia observacional, herramientas formales ni PDFs inaccesibles
para justificar las demostraciones siguientes.

## 3. Estado previo

Las derivaciones productoras estaban pendientes de auditoría; los archivos de
cálculo estaban clasificados como evidencia simbólica o numérica. Las
afirmaciones deliberadamente falsas se mantienen refutadas. La importación de
este informe a una memoria científica no puede saltarse sus controles de
versiones, hipótesis, dependencia y artefactos.

No se introducen teoremas nuevos de física fundamental. Los resultados son
especializaciones comprobables de teoría de representaciones, ecuaciones
diferenciales lineales, deformaciones y álgebra de Lie. El avance operativo es
tener una cadena reproducible de construcción, intento de refutación y revisión.

## 4. Análisis matemático

### 4.1. Dimensión del espacio de Gauss y base

**Premisas B1.** Se usa \(V=(\mathbb C^2)^{\otimes4}\), con producto tensorial
positivo estándar, orden (1,2,3,4), \(J_a=\sigma_a/2\), \(0=\uparrow\),
\(1=\downarrow\), \(\epsilon_{xyz}=+1\). El grupo SU(2) actúa diagonalmente.
No se identifican sus rotaciones internas con difeomorfismos ni con
helicidades gravitatorias.

**Conclusión B2.** \(\dim\operatorname{Inv}_{SU(2)}V=2\).
Se verifica por una vía distinta de la descomposición de Clebsch–Gordan
empleada por el productor.

**Prueba B3.** La condición \(G_z=0\) restringe a las seis cadenas de bits
0011, 0101, 0110, 1001, 1010, 1100. El operador
\(G_+=\sum_\ell J_{\ell,+}\) transforma ese espacio en el sector
\(m=1\), de base 0001, 0010, 0100, 1000. Su matriz exacta es

\[
A=\begin{pmatrix}
1&1&0&1&0&0\\
1&0&1&0&1&0\\
0&1&1&0&0&1\\
0&0&0&1&1&1
\end{pmatrix}.
\]

La reducción racional por filas, guardada en la salida del auditor, da rango
cuatro. Por rango–nulidad, su núcleo tiene dimensión dos. Para un vector de
\(m=0\), \(G_+\psi=0\) implica \(G_-\psi=0\), pues
\([G_+,G_-]=2G_z\), \(G_-^\dagger=G_+\) y
\(\|G_-\psi\|^2=\langle\psi,G_+G_-\psi\rangle=0\).
Queda aniquilado por los tres generadores y es SU(2)-invariante. Recíprocamente
todo invariante cumple esas condiciones.

Los vectores productores \(u_0=b_0\) y \(u_1=\sqrt3 b_1\) pertenecen al núcleo;
sus productos dan \(G=\operatorname{diag}(1,3)\). Son independientes y,
por la dimensión ya probada, abarcan el núcleo. En la base \(b_0,b_1\) el Gram
es la identidad. **B4–B5:** la positividad se usa para deducir \(G_-\psi=0\);
la conclusión es finita y específica de estos cuatro espines.

### 4.2. Operador triple mediante permutaciones

Para dos espines 1/2, la transposición satisface
\(P_{ij}=2\,J_i\cdot J_j+\tfrac12 I\): ambos operadores tienen autovalores
\(-1,+1\) en los canales singlete y triplete. Esta identidad transforma el
problema productor de seis productos de matrices de Pauli en un cálculo
independiente con dos matrices enteras de permutación.

Por el conmutador \([J_2^a,J_2^b]=i\epsilon^{ab}{}_cJ_2^c\),

\[
[J_1\cdot J_2,J_2\cdot J_3]
=i\epsilon_{abc}J_1^aJ_2^cJ_3^b=-i q,\qquad
q=\frac{i}{4}[P_{12},P_{23}].
\]

Evaluar las permutaciones da \(q u_0=(i/4)u_1\) y
\(q u_1=-(3i/4)u_0\). Por tanto

\[
Q_u=\begin{pmatrix}0&-3i/4\\i/4&0\end{pmatrix},\quad
Q_b=\frac{\sqrt3}{4}\sigma_y,\quad
Q_u^2=\frac3{16}I.
\]

La identidad \(Q_u^\dagger G=GQ_u\), no \(Q_u^\dagger=Q_u\), expresa la
autoadjunción en la base no ortonormal. El cálculo racional verifica también
que la imagen bajo \(q\) permanece en el subespacio de Gauss.
En dimensión finita, la hermiticidad en el dominio completo implica
autoadjunción. Los autovalores son \(\pm\sqrt3/4\); los estados correspondientes
son dos canales singlete, **no dos helicidades de Einstein**.

El signo importa: cambiarlo conserva \(q^2\) y las normas. Por eso el auditor
compara también \(Q_u\), y las pruebas de regresión demuestran que un cambio
de signo del productor es detectado aun conservando su cuadrado.
El signo acordado depende de base, orden de patas y orientación declaradas.

### 4.3. Reloj ideal, dominio y producto físico

**Premisas A1/B1.** \(T\in\mathbb R\), \(\hbar>0\),
\(\kappa\in\mathbb R\), \(H=\kappa Q_b\);
\(\mathcal K=L^2(\mathbb R,dT)\otimes\mathbb C^2\).
El operador \(C=-i\hbar\partial_T+H\) actúa sobre
\(H^1(\mathbb R,\mathbb C^2)\). No se deduce esa restricción de RG.

**Prueba A3/B3.** Diagonalizar la matriz hermitiana \(H\) y transformar Fourier
convierte \(C\) en dos multiplicadores reales \(\hbar k+E_j\).
Su dominio de autoadjunción coincide con \(H^1\), porque las dos traslaciones
de energía son finitas. La ecuación \(C\Psi=0\), fuera del núcleo cinemático
normalizable, equivale a

\[
i\hbar\partial_T\Psi=H\Psi,\qquad
\Psi(T)=e^{-iH(T-T_0)/\hbar}\psi_0.
\]

El teorema elemental de la EDO lineal, o la solución de cada componente
espectral, da existencia y unicidad para todo \(T\). Las soluciones suaves
acotadas también definen distribuciones temperadas.

**Punto decisivo.** El núcleo de \(C\) dentro de \(\mathcal K\) es cero:
una solución no nula tiene norma constante positiva, cuya integral sobre
\(\mathbb R\) diverge. Se construye **otro espacio**, el de soluciones
generalizadas, con
\(\langle\Psi,\Phi\rangle_{\rm phys}
=\langle\Psi(T_0),\Phi(T_0)\rangle_{\mathbb C^2}\).
Esta es una elección explícita de producto físico, no una restricción del
producto \(L^2(dT)\). Evaluación en \(T_0\) es una biyección; la
autoadjunción implica que el producto no depende de \(T_0\).

La evolución es
\(U=\cos\theta I-i\sin\theta\sigma_y\), con
\(\theta=\kappa\sqrt3(T-T_0)/(4\hbar)\).
De \(\sigma_y^2=I\) se obtiene \(U^\dagger U=I\) para todo \(\theta\) real.
El argumento prueba el resultado general finito; las muestras numéricas del
auditor son comprobaciones adicionales, no su demostración.

**A4–A7/B4–B5.** \(J,q,\theta\) son adimensionales, \([\kappa]=[p_T]\)
es energía y \([\hbar]\) es energía multiplicada por tiempo. \(T=T_0\) o \(\kappa=0\)
dan \(U=I\). El observable de canal
\(P_1=|b_1\rangle\langle b_1|\) produce, para preparación \(b_0\),
\(P_{0\to1}=\sin^2\theta\); falta un mapa a observables gravitatorios.
Espines fijos no proporcionan un límite \(\hbar\to0\) hacia Einstein.

### 4.4. La hipótesis de autoadjunción es necesaria

El productor propone \(K=i\kappa I\), cuyo propagador es
\(e^{\kappa(T-T_0)/\hbar}I\); la norma cuadrada varía como
\(e^{2\kappa(T-T_0)/\hbar}\). Es un contraejemplo correcto a «toda matriz
Hamiltoniana finita conserva la norma».

El auditor usa otro ejemplo: \(K=\begin{pmatrix}0&1\\0&0\end{pmatrix}\),
\(K^2=0\), en unidades adimensionales, y \(\psi_0=(0,1)\).
Entonces \(e^{-itK}\psi_0=(-it,1)\) y su norma cuadrada es \(1+t^2\),
distinta de uno para \(t\ne0\). Este caso independiente evita aceptar la
refutación solo porque el productor la etiquete como tal.

### 4.5. Obstrucción mixta de Maurer–Cartan

**B1.** Sea \((L,d,[\ ,\ ])\) una DGLA cohomológica sobre un cuerpo de
característica cero. Los elementos \(a,b,c\) tienen grado uno; \(\epsilon,\eta\)
tienen grado cero y pertenecen al anillo
\(R=k[\epsilon,\eta]/(\epsilon^2,\eta^2)\).
Defínase \(\alpha=\epsilon a+\eta b+\epsilon\eta c\).

Por antisimetría graduada, \([a,b]=[b,a]\). Expandir término a término da

\[
d\alpha+\tfrac12[\alpha,\alpha]
=\epsilon\,da+\eta\,db+\epsilon\eta\bigl(dc+[a,b]\bigr).
\]

**B2–B4.** Si \(da=db=0\), la identidad de derivación de \(d\) muestra que
\(d[a,b]=0\). Existe un \(c\) que resuelve Maurer–Cartan sobre este anillo si
y solo si \([a,b]\) es exacto, es decir, si su clase en \(H^2(L)\) se anula.
La condición es independiente de cambiar \(a,b\) por representantes
cohomólogos: los términos añadidos son diferenciales de corchetes con
elementos de grado cero.

En el ejemplo, \(L^1=\langle x,y,z\rangle\), \(L^2=\langle w\rangle\),
\([x,y]=[y,x]=w\), con \(w\) central y los demás corchetes nulos.
Si \(dz=w\), \(c=-z\) cancela el término mixto y \(H^2=0\).
Si \(d=0\), \(w\) no es exacto, \(H^2=\langle w\rangle\) y ninguna corrección
lo cancela. En ambos casos los datos separados \(\epsilon x,\eta y\) son
soluciones. El auditor reconstruye todos los coeficientes del anillo truncado,
incluido el factor \(1/2\), por una expansión distinta del residual escalar
del productor.

**B5–B6.** La equivalencia vale para ese problema de extensión y orden. En
una DGLA general no demuestra extensión a órdenes mayores, convergencia,
realidad, pesos twistoriales, existencia de curvas ni reconstrucción de
Einstein. No se ha construido un mapa que convierta \(a,b\) en las dos
helicidades físicas. El resultado es una herramienta de deformaciones; su
aplicación a Googly sigue condicionada.

### 4.6. Antisimetría y métrica invariante no bastan para Jacobi

Sobre \(\mathbb R^5\), con métrica euclídea y base ortonormal \(e_0,\dots,e_4\),
defínase \([e_i,e_j]=f_{ij}{}^k e_k\), \(f_{ijk}=f_{ij}{}^k\), y tómese la
3-forma totalmente antisimétrica con componentes independientes
\(f_{012}=f_{034}=1\). La antisimetría total garantiza la identidad métrica
\(\langle[x,y],z\rangle=\langle x,[y,z]\rangle\). Esto es una condición de
compatibilidad de un corchete, no prueba de que sea un álgebra de Lie.

En la convención \(J(x,y,z)=[x,[y,z]]+[y,[z,x]]+[z,[x,y]]\),

\[
J(e_1,e_2,e_3)=0+0+[e_3,e_0]=-e_4\ne0.
\]

La suma alternativa con corchetes exteriores a la derecha tiene el signo
opuesto; no es una discrepancia física si se declara esa convención.
El auditor enumera los triples no ordenados, y encuentra cuatro no nulos;
sus seis permutaciones dan los 24 residuos no nulos reportados por el
productor. El caso \(f_{012}=1\) en \(\mathbb R^3\) satisface Jacobi.

Para una deformación ordinaria Yang–Mills con constantes de estructura,
Jacobi es necesaria para el cierre del álgebra gauge. Superarla no comprueba
anomalías cuánticas, materia, gravedad, causalidad o una teoría completa.
El ejemplo malo refuta la suficiencia de la antisimetría métrica; el bueno es
un antecedente SU(2), no una nueva unificación.

### 4.7. Obstrucción BV y el puente de graduaciones

El criterio UFT-UF-001 se comprueba mediante una prueba separada del test de
Jacobi. Sean \(\mathcal F\) los funcionales locales módulo derivadas totales
en la categoría declarada, \((\ ,\ )\) un antibracket de grado fantasma \(+1\),
\(S_0\) par de grado fantasma cero con \((S_0,S_0)=0\), y
\(s=(S_0,\cdot)\). Jacobi graduada implica
\(s^2F=\tfrac12((S_0,S_0),F)=0\).
Si \(S_1\) es par, tiene grado fantasma cero y \(sS_1=0\), entonces
\((S_1,S_1)/2\) tiene grado fantasma uno y es \(s\)-cerrado.

Expandir la ecuación maestra para
\(S=S_0+gS_1+g^2S_2\) da, a orden \(g^2\),
\(sS_2=-(S_1,S_1)/2\). Un \(S_2\) **local** existe exactamente cuando el
lado derecho es exacto en el mismo complejo de funcionales locales. Es
necesario conservar campos permitidos, soporte de variaciones, dimensión y
clase de derivadas; una primitiva no local no es una solución de ese problema.
Esta prueba no resuelve una cohomología local de un modelo gravitatorio
concreto ni garantiza deformación a todos los órdenes.

Para UFT-X-001, defínase \(L^n=\mathcal F^{\mathrm{gh}=n-1}\), de modo que
\(|F|_L=\mathrm{gh}(F)+1\). El antibracket tiene grado cero en \(L\), y \(s\)
tiene grado uno. **Condición de signos:** se supone que la paridad Grassmann
de cada funcional es su número fantasma módulo dos. Esto se cumple en la
categoría polinómica puramente bosónica de Yang–Mills con sus fantasmas y
antifields declarados. Con esa hipótesis, la antisimetría y Jacobi impares del
antibracket pasan a los signos ordinarios de una DGLA cohomológica.
En particular

\[
s(F,G)=(sF,G)+(-1)^{|F|_L}(F,sG).
\]

Dos vértices cerrados de grado fantasma cero son elementos de \(Z^1(L)\);
su obstrucción mixta vive en
\(H^2(L)=H^{\mathrm{gh}=1}(\mathcal F,s)\).
Es la aplicación exacta del lema general de la sección 4.5 a otro complejo.
No es un morfismo construido desde la DGLA finita \(x,y,z,w\) hacia la
gravedad. Si se añade materia fermiónica física de grado fantasma cero, la
paridad ya no está codificada solo por \(\mathrm{gh}\); habrá que conservar
una supergraduación adicional o restringir el enunciado. No se extiende el
puente ordinario a ese caso sin justificar sus signos.

## 5. Análisis físico

La interpretación física se limita al banco de dos niveles con reloj continuo
ideal. El reloj tiene momento conjugado no acotado inferiormente; no se ha
modelado un aparato con resolución finita ni su retroacción. Monotonía clásica
\(\{T,p_T+H\}=1\) vale en esa reducción y con el parámetro gauge adecuadamente
orientado. Para
\(C=p_T^2/(2M)+M\omega^2T^2/2+H-E\), con \(M,\omega>0\), se tiene
\(\{T,C\}=p_T/M\). En trayectorias oscilantes con energía disponible positiva
aparecen retornos \(p_T=0\), de modo que el argumento lineal global falla.
La mera expresión de la restricción no afirma que toda trayectoria tenga
retorno: depende del sector energético y de las hipótesis anteriores.

No se observa aquí gravedad, una escala UV física ni un continuo. La
autoadjunción de una matriz finita no decide la unitariedad de QFT. Tampoco la
simetría SU(2) del nodo basta para imponer las restricciones restantes de
LQG. Los parámetros y observables del banco deben derivarse o calibrarse antes
de convertir sus probabilidades en predicciones gravitatorias.

## 6. Conexiones justificadas y propuestas

- **Justificada dentro del banco:** el mapa de inclusión de los dos singletes
  en \(V\) preserva el producto interno con su Gram y entrelaza la acción de
  \(q\). Evaluación en \(T_0\) identifica las soluciones generalizadas con el
  espacio físico finito elegido, bajo las hipótesis de la sección 4.3.
- **Correspondencia matemática delimitada:** las transposiciones y los
  productos de espines se relacionan por \(P_{ij}=2J_i\cdot J_j+I/2\).
  Sus matrices coinciden en todo \(V\); no solo en una muestra de estados.
- **Conexión propuesta:** usar el obstáculo cohomológico mixto para una
  reconstrucción twistorial física. Falta fijar el complejo, pesos, mapas,
  realidad y ecuaciones; no existe todavía transferencia de una solución.
- **Compatibilidad algebraica insuficiente:** una métrica positiva e invariante
  es compatible con el tensor antisimétrico malo, pero Jacobi lo descarta.
  Esa incompatibilidad debe permanecer en el mapa de conocimiento.

No se afirma una equivalencia entre los tres programas ni se impone un número
mínimo de conexiones. Las herramientas comunes no sustituyen un diccionario
físico.

## 7. Resultados y evidencia

**[REGISTRO DE AUDITORÍA] UFT-AUD-MATH-001.** Tipo: interno.
Proceso productor: agente uft_physics y cálculo science_examples.py.
Proceso revisor: agente uft_math_audit, reconstrucción escrita y
independent_science_audit.py. Los procesos comparten familia de modelo y
pueden compartir errores. No hay revisión externa ni verificación formal.
Los IDs de ejecuciones computacionales y hashes se guardan en el JSON de
evidencia; no deben confundirse con IDs de agentes LLM realmente ejecutados.

| Afirmación | Veredicto interno | Alcance y condición que acompaña al resultado |
|---|---|---|
| UFT-QG-001 | CONFIRMADO | Solo \(\operatorname{Inv}_{SU(2)}((\mathbb C^2)^{\otimes4})\), base y convención declaradas. |
| UFT-QG-002 | CONFIRMADO CON CONDICIONES | Matriz, orientación, Gram y normalización especificados; no operador gravitatorio completo. |
| UFT-QG-003 | CONFIRMADO CON CONDICIONES | \(H\) finito autoadjunto, reloj ideal lineal, soluciones generalizadas y producto físico elegido. |
| UFT-QG-004 | REFUTADO | La afirmación universal es falsa; ambos contraejemplos no hermitianos la invalidan. |
| UFT-GO-001 | CONFIRMADO CON CONDICIONES | Extensión MC sobre \(k[\epsilon,\eta]/(\epsilon^2,\eta^2)\); no reconstrucción de Einstein. |
| UFT-GO-002 | CONFIRMADO | Los dos ejemplos finitos tienen, respectivamente, obstáculo exacto y no exacto. |
| UFT-GO-003 | REFUTADO | La solución individual no garantiza la extensión mixta; UFT-GO-002 proporciona el contraejemplo. |
| UFT-UF-001 | CONFIRMADO CON CONDICIONES | Criterio de exactitud de la obstrucción BV de segundo orden en la categoría local especificada. |
| UFT-UF-002 | CONFIRMADO | El tensor cúbico malo viola Jacobi con el residual explícito; la afirmación de suficiencia queda REFUTADA. |
| UFT-UF-003 | CONFIRMADO | El control de dimensión tres satisface Jacobi con la normalización elegida. |
| UFT-UF-004 | REFUTADO | La extensión automática a un álgebra gauge de Lie queda descartada por UFT-UF-002; no es un no-go para todas las extensiones superiores. |
| UFT-X-001 | CONFIRMADO CON CONDICIONES | Corrimiento de grados del complejo BV con signos compatibles y paridad \(\mathrm{gh}\bmod2\); no equivalencia física entre las metas. |

Las derivaciones matemáticas escritas tienen argumentos bajo hipótesis
explícitas y revisión interna. Los archivos computacionales conservan su
categoría **EVIDENCIA SIMBÓLICA O NUMÉRICA**. La existencia de esta tabla no
autoriza una promoción automática ni cambia la clasificación de una
afirmación más amplia.

Comandos ejecutados:

~~~bash
scipython scripts/independent_science_audit.py \
  --output evidence/science-independent.json \
  --producer research/calculations/first_cycle.json
python3 -m unittest discover -s tests -p test_independent_audit.py -v
~~~

Los tres bloques independientes pasan y los diez tests del auditor pasan.
La versión del intérprete, timestamp, huella del productor y separación
quedan en el JSON. El auditor no importa science_examples.py.

## 8. Objeciones y contraejemplos

No se detectó un error central en los resultados finitos revisados.
Sí son condiciones esenciales, cuyo olvido produciría afirmaciones falsas:

- Confundir la base \(u\) con una base ortonormal cambia la comprobación de
  hermiticidad; usar el producto euclídeo sobre sus coordenadas es incorrecto.
- Verificar solo \(q^2\) no fija el signo de \(q\).
- Tratar las soluciones del reloj como vectores de \(L^2(dT)\) daría un espacio
  físico vacío; el producto de evaluación debe declararse por separado.
- Sustituir «autoadjunto» por «matriz finita» pierde la unitariedad.
- Cambiar el anillo de MC o pedir convergencia exige argumentos adicionales.
- Una 3-forma antisimétrica con métrica positiva puede fallar Jacobi.
- El ejemplo de retorno requiere condiciones energéticas que produzcan una
  órbita no trivial; no se generaliza a cualquier dato.

Los tests adversariales alteran el signo de \(q\), la dimensión declarada,
la existencia de solución mixta, el residual de Jacobi y el estado refutado.
Cada alteración es rechazada. Esto comprueba esas detecciones específicas,
no todos los errores posibles en literatura, código o razonamiento.

## 9. Impacto sobre los tres objetivos

**Gravedad cuántica:** se valida un banco para evaluar reloj ideal y una
dinámica finita gauge-invariante. Faltan restricciones completas, grados de
libertad locales, límite de grafos, UV y Einstein. No se cumple un hito GQ
por cambiar la etiqueta del banco.

**Googly:** se dispone de una prueba mínima para no confundir existencia en
dos sectores con extensión mixta. Sigue pendiente identificar un complejo
geométrico y reconstrucción física; el problema general no queda resuelto.

**Unificación:** se añade un filtro exacto de cierre gauge con un ejemplo
que lo falla. No se han obtenido espectro de materia, parámetros fijados,
dinámica gravitatoria o predicciones nuevas. No se altera la clasificación de
las candidatas K1–K4 del BRAIN.

## 10. Actualizaciones de memoria y alertas

Artefactos producidos por esta revisión:
scripts/independent_science_audit.py,
tests/test_independent_audit.py,
evidence/science-independent.json y el presente informe.
La memoria global y BRAIN permanecen sin modificaciones por este subagente.
La integración en el registro UFT corresponde al coordinador.

Alertas justificadas para UFT: refutaciones de controles deliberados, revisión
favorable interna de enunciados acotados y requisitos pendientes. No son
alertas de descubrimiento fundamental ni deben inyectarse automáticamente
como resultados confirmados en las fuentes canónicas.

Skills aplicadas: metacognicion-operativa para estados y comprobaciones;
colaborador-matematica-pura para representaciones y DGLA;
investigador-elite y colaborador-cientifico para dominio de operadores,
interpretación de LQG y Protocolos A/B; peer-review para separación
afirmación–evidencia, objeciones y límites del informe. La revisión es técnica
interna por encargo del propietario, no un dictamen editorial.
No se usó una herramienta formal ni se delegó otro subagente.

## 11. Próxima comprobación prioritaria

Antes de ampliar el banco, sustituir el reloj ideal por un sistema material
concreto, especificar sus restricciones y estimar resolución y retroacción
sobre el mismo sector finito. Una alternativa matemática barata es probar
dos nodos y describir el álgebra de restricciones elegida. Ninguna ampliación
debe llamarse recuperación de RG sin un mapa de dinámica y observables.

Para Googly y unificación, la prioridad es fijar el objeto físico del cual
se deriva el complejo de deformaciones; sin ese mapa, aumentar el tamaño de
las matrices o de los equipos no reduce la laguna principal.

## Evaluación de los siete criterios

El dominio evaluado son los tres ejemplos y las derivaciones finitas de este
informe. La evaluación de una teoría física completa permanece pendiente.

| Criterio | Estado | Evidencia concreta | Limitaciones y siguiente comprobación |
|---|---|---|---|
| Coherencia matemática | Cumplido en el alcance declarado | Pruebas de §4, reconstrucción exacta y contraejemplos reproducidos. | No consistencia absoluta ni prueba formal; comprobar un nuevo caso al ampliar el modelo. |
| Contrastabilidad | Parcial | Ley \(\sin^2\theta\) en el banco y tests algebraicos discriminantes. | No predicción gravitatoria; derivar un modelo físico y su calibración. |
| Correspondencia | Parcial | Recupera evolución unitaria finita; \(\kappa=0\), \(\Delta T=0\). | No RG ni QFT completa; construir un límite controlado y comparar observables. |
| Definiciones operacionales | Parcial | Preparación de canal y proyector \(P_1\) en un sistema de dos niveles. | Falta aparato material y observable gravitatorio; fijar protocolo de inferencia y errores. |
| Explicación y unificación | Parcial | Se aclaran un requisito del reloj y dos obstrucciones algebraicas. | No se unifican los sectores físicos; justificar un diccionario concreto. |
| Parsimonia | Parcial | Hamiltoniano y seis elecciones explícitas del banco; DGLAs mínimas. | \(\kappa\), reloj y truncación son libres; comparar alternativas de igual alcance. |
| Evaluación no empírica | Pendiente | Antecedentes identificados y alternativas malas descartadas con argumentos. | No búsqueda exhaustiva de alternativas ni metainducción; no asignar probabilidad de verdad. |

## Predicciones o pruebas discriminantes

No se han derivado predicciones observacionales nuevas de gravedad, Googly o
unificación. Las siguientes son pruebas matemáticas o del banco finito:

1. Reconstruir \(q\) cambiando de algoritmo y conservando las convenciones.
   Un desacuerdo de signo cuestionaría UFT-QG-002 o su implementación; el
   cuadrado aislado no resuelve la discrepancia.
2. Intentar conservar la norma para el Hamiltoniano nilpotente no hermitiano.
   Obtener norma constante para \((0,1)\) y \(t\ne0\) cuestionaría ese cálculo
   o el producto usado; no refutaría LQG.
3. Quitar \(dz=w\) e intentar cancelar el coeficiente mixto con cualquier
   \(c\in L^1\). Una cancelación cuestionaría la DGLA o las hipótesis de
   UFT-GO-001/002, sin establecer por sí misma una solución twistorial.
4. Evaluar Jacobi del tensor malo en \((e_1,e_2,e_3)\). Un residual cero
   cuestionaría UFT-UF-002, la convención o el código; superar el test no
   demostraría unificación física.
5. Construir una órbita oscilante no trivial del reloj cuadrático y examinar
   \(p_T=0\). Si el reloj fuese monótono a través del retorno sin cambiar
   descripción o rama, habría que revisar el análisis de gauge y la supuesta
   órbita, no atribuir globalidad al reloj ideal por analogía.
