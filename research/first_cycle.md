# Ciclo UFT-001 — tres programas y un banco de tiempo relacional

Versión 0.1 · 2026-11-06 (America/Bogota).
Informe de investigación local; las auditorías separadas se conservan en
research/audits/. La procedencia de las afirmaciones y estados de entrada está
en research/items.json. Este informe no declara una teoría física completa.

## 1. Pregunta y alcance

¿Puede el programa distinguir un modelo calculable, una prueba matemática
delimitada y una aspiración de teoría física, detectar fallos concretos y
conservar sus dependencias? Se ejecuta un banco prioritario sobre tiempo
relacional en un intertwiner SU(2), acompañado de dos filtros algebraicos para
Googly y acoplamientos gauge. Los tres objetivos siguen siendo independientes;
solo se conecta una herramienta matemática con sus hipótesis explícitas.

El alcance cubre cuatro espines1/2, un reloj ideal, dos DGLA pequeñas y dos
tensores de acoplamiento. No cubre todos los modelos de gravedad ni constituye
una revisión exhaustiva de física y matemáticas. La prioridad de este banco
responde a la petición de incorporar tiempo/LQG; no reemplaza los hitos canónicos
GQ1–GQ5 ni los declara alcanzados.

## 2. Fuentes y materiales examinados

Se consultaron META.md y partes/meta_liston.json del BRAIN, y los manifiestos
compartidos objectives.md y conventions.md del Protocolo Maestro. Se preservan
como formulaciones documentales, con su versión y procedencia en el inventario.
No se accedió a los informes privados de una fase independiente abierta.
La formulación vigente de tres objetivos prevalece sobre el resumen antiguo
del manifiesto que enumera solo I–III.

Las referencias y alcance real de lectura están en
[physics_sources.json](../references/physics_sources.json): Giesel–Thiemann,
De Pietri–Rovelli, Manetti, Barnich–Henneaux, Mason–Skinner y Adamo.
Se verificaron metadatos y selecciones HTML indicadas, sin fingir lectura de
PDF completos o revisión humana. No se consultaron MathSciNet, Scopus o WoS.
La búsqueda exploratoria en OpenAI Math produjo cuatro coincidencias léxicas
sin título directamente pertinente; ninguna se usó como premisa.

Archivos propios examinados: las tres propuestas A–O, el script productor, sus
ocho tests y la salida research/calculations/first_cycle.json. Los antecedentes
de relojes materiales, MC y BV no se presentan como hallazgos nuevos.

## 3. Estado previo

META exige Googly, unificación al nivel de cuerdas/LQG y cuantización de RG.
Ningún componente importado acredita por sí mismo una solución de esos tres
problemas. Las fronteras refutadas se mantienen y los resultados condicionados
conservan sus condiciones. La prioridad de candidatas registrada se respeta
sin copiar sus espectros o premisas no revalidadas al nuevo modelo.

El catálogo contiene5.000 perfiles de diseño, cuya existencia no acredita
excelencia individual ni ejecución de5.000 agentes. La selección de un equipo
queda separada de las ejecuciones reales y sus aportes. El comando determinista
de este banco no ejecuta modelos LLM; las tareas de redacción y revisión de
agentes se registran aparte.

## 4. Análisis matemático

**UFT-QG-001/002.** La descomposición
\((1/2\otimes1/2)\otimes(1/2\otimes1/2)\) contiene dos singletes.
Los vectores y convenciones de
[QG§E–H](quantum_gravity/proposal.md) fijan el signo de
\(q=\epsilon_{abc}J_1^aJ_2^bJ_3^c\).
En base ortonormal \(q=\sqrt3\,\sigma_y/4\), de modo que \(q^2=3I/16\).
En la base racional del script, Gram es diag(1,3) y
\(q=\left(\begin{smallmatrix}0&-3i/4\\i/4&0\end{smallmatrix}\right)\).
Confundir esta última con una base ortonormal produciría un juicio erróneo
de hermiticidad.

**UFT-QG-003.** Para \(C=-i\hbar\partial_T+H\), \(H=H^\dagger\) finito,
\(\Psi(T)=e^{-iH(T-T_0)/\hbar}\psi_0\).
Las soluciones son generalizadas y no normalizables en \(L^2(\mathbb R,dT)\);
el producto físico se define por evaluación. El dominio cinemático de \(p_T\)
es \(H^1(\mathbb R)\) y la perturbación \(H\) es acotada.
Las pruebas se escriben en el documento; calcular una matriz no sustituye
el argumento sobre el dominio y el producto físico.

**UFT-GO-001/002.** MC sobre
\(\mathbb K[\epsilon,\eta]/(\epsilon^2,\eta^2)\) tiene coeficiente mixto
\(db+[a_+,a_-]\). Existe corrección si y solo si esa clase en \(H^2\) es cero.
Con \(dz=w,[x,y]=w\) se toma \(b=-z\); con \(d=0\) queda obstrucción \(w\).
La suficiencia vale para ese orden formal; no se infiere convergencia.

**UFT-UF-001/002/003.** La ecuación maestra BV exige
\(sS_2=-(S_1,S_1)/2\) en funcionales locales. Independientemente, el tensor
totalmente antisimétrico \(f_{012}=f_{034}=1\) en dimensión cinco falla
\(J(e_1,e_2,e_3)=-e_4\), aunque preserva la métrica delta. El control
tridimensional \(f_{012}=1\) satisface Jacobi. El script no resuelve la
clasificación BV completa: su comprobación es algebraica y finita.

## 5. Análisis físico

El banco QG solo impone Gauss de un nodo. No implementa restricciones de
difeomorfismos, Hamiltoniano gravitatorio de RG, límite continuo o estados
semiclásicos. \(H=\kappa q\) se postula como Hamiltoniano toy, con
\([\kappa]=\)energía y argumento \(\kappa\Delta T/\hbar\) adimensional.
El reloj ideal tiene momento no acotado inferiormente; resolución,
retroacción y comparación de relojes materiales quedan pendientes.

El proyector de canal es SU(2) invariante, y su probabilidad en el banco es
\(\sin^2[\kappa\sqrt3\Delta T/(4\hbar)]\). No es una predicción gravitatoria.
En este sector \(|q|\) es escalar: no se anuncia una oscilación de volumen.
Tampoco se deduce tiempo discreto de un espectro geométrico.

Googly: no existe mapa del ejemplo DGLA a ambas helicidades y ecuaciones de
Einstein. UF: el control es Yang–Mills conocido y no incorpora gravedad o materia.
Las tres propuestas precisan el trabajo que haría falta para alcanzar sus metas.

## 6. Conexiones justificadas y propuestas

**UFT-X-001, puente matemático condicionado.** Para el banco BV bosónico,
paridad de Grassmann=gh módulo2; poner
\(L^n=\mathcal F^{\mathrm{gh}=n-1}\), \(d=(S_0,\cdot)\) y corchete=antibracket
permite aplicar el lema abstracto de MC a dos vértices locales cerrados.
La obstrucción vive en \(H^2(L)=H^1_{\rm BV}\).

El test de conexión registra: mapa explícito de grados; hipótesis de localidad,
maestra clásica y cierre; signos compatibles; estado condicionado y pendiente
de auditoría; ausencia de uso de fronteras refutadas; ID y procedencia en
research/items.json. Con fermiones físicos hace falta conservar una
supergraduación adicional. La corrección de esta hipótesis fue solicitada
por la revisión separada y quedó incorporada.

El puente no identifica el ejemplo finito de Googly con una teoría gauge,
ni unifica físicamente las metas. La conexión física QG–Googly sigue abierta;
no se impone una arista artificial para evitar un componente aislado.

## 7. Resultados y evidencia

Ejecuciones reales: el productor sobre \(\mathbb Q[i]\) y el verificador
independiente son programas distintos. La salida y sus huellas están en
[cycle.json](../evidence/cycle-001-final/cycle.json).
Ese ciclo terminó satisfactoriamente con dos subprocesos y cero agentes LLM
ejecutados por el comando. No realizó promociones científicas.
La redacción de propuestas y las auditorías de agentes son actividades separadas.

El productor se ejecutó también con scipython y SymPy1.14.0; guardó la identidad
de unitariedad para todo theta real. Ocho tests científicos propios pasaron.
La salida exacta confirma cierre de Gauss, preservación del subespacio, q²,
obstrucción MC y el residuo Jacobi. Estas son comprobaciones finitas; el
argumento general permanece identificado y sujeto a su registro de auditoría.

La tabla evalúa el **banco y la evidencia del ciclo**, sin trasladar los estados
favorables a los objetivos completos.

| Criterio | Estado | Evidencia concreta | Limitaciones y siguiente comprobación |
|---|---|---|---|
| Coherencia matemática | Cumplido en el alcance declarado | Matrices exactas, argumentos QG§H/GO§H/UF§H y reconstrucción separada. | No es consistencia absoluta ni existencia de una teoría general; consultar auditorías e hipótesis. |
| Contrastabilidad | Parcial | Tres afirmaciones universales tienen contraejemplos explícitos; ley del modelo de dos niveles. | No hay predicciones nuevas de gravedad o unificación; derivar observables físicos. |
| Correspondencia | Parcial | \(g\to0\) da Maxwell y \(\kappa\to0\) evolución trivial del banco. | No se recuperan RG, continuo o Einstein no autodual. |
| Definiciones operacionales | Parcial | Preparación b0, proyector de canal, reloj ideal y producto físico definidos. | No hay protocolo gravitatorio material con resolución y retroacción. |
| Explicación y unificación | Pendiente | Un puente de complejos graduados explícito. | No constituye unificación dinámica ni equivalencia física. |
| Parsimonia | Parcial | Seis entradas por programa; solo un parámetro de escala libre en el Hamiltoniano toy. | Un banco pequeño no supera por sencillez una teoría de alcance mayor; estudiar extensiones comparables. |
| Evaluación no empírica | Pendiente | Búsqueda exploratoria y alternativas explícitas. | No se afirma ausencia de alternativas, metainducción favorable ni probabilidades de verdad. |

Para las metas completas, los siete criterios siguen en estado pendiente o
parcial según el inventario; ningún renglón acredita una teoría final.
La revisión es interna, no revisión externa ni verificación formal.

## 8. Objeciones y contraejemplos

1. **UFT-QG-004, refutado:** para \(K=i\kappa I\), la norma crece exponencialmente.
   Refuta la conservación universal sin autoadjunción, no la evolución unitaria.
2. **UFT-GO-003, refutado:** dos direcciones MC separadas no garantizan extensión
   mixta cuando \([x,y]\) no es frontera.
3. **UFT-UF-004, refutado:** antisimetría e invariancia métrica no garantizan Lie.

Objeciones abiertas: el Hamiltoniano no viene de RG; el reloj es ideal; no hay
diccionario twistorial ni materia incorporada. No se responden por consenso.
Si cambia una hipótesis de dominio, signo, grado o fuente, los resultados
afectados requieren revisión y no una promoción automática.

## 9. Impacto sobre los tres objetivos

| Objetivo | Aporte real | Lo que no autoriza |
|---|---|---|
| Gravedad cuántica y tiempo/LQG | Un banco que separa Gauss, reloj, dinámica toy y norma física. | Cuantización de RG, Einstein, UV, tiempo discreto o cumplimiento de GQ1–GQ5. |
| Googly | Un filtro de obstrucción mixta con contraejemplo calculable. | Segunda helicidad reconstruida, equivalencia física o extensión global. |
| Unificación | Un filtro local y contraejemplo de cierre algebraico. | Origen común de gravedad/gauge/materia o nuevas predicciones. |

No se presupone una única teoría final. Elegir teorías independientes ahora
evita transferencias físicas injustificadas y permite compartir herramientas
cuando exista el mapa y se verifiquen sus hipótesis.

## 10. Actualizaciones de memoria y alertas

La memoria portable de este trabajo es research/items.json, con enunciados,
hipótesis, evidencias, dependencias, estados y revisión. Las propuestas se
conservan separadas de los resultados. Tres afirmaciones de control están
refutadas y no pueden presentarse como demostradas.

Se enlazan auditoría matemática y revisión científica en research/audits/.
Los cambios de paridad del puente BV quedan explícitos en los documentos.
La memoria global BRAIN y sus Alertas no se modificaron desde esta tarea.
Sus alertas de avance decisivo tienen un umbral mayor que las alertas locales
de fallo o validación del banco; no se anuncia un descubrimiento por pasar tests.

El mecanismo operativo de ingestión/alertas documenta por separado diseño,
ejecución manual, configuración y última prueba satisfactoria. Este informe
no certifica que una automatización programada esté activa sin su evidencia.
Si falta un informe Claude o Codex sellado, la comparación permanece pendiente.

## 11. Próxima comprobación prioritaria

Prioridad: sustituir el reloj ideal impuesto por un reloj material concreto,
estableciendo restricciones, dominio y un régimen cuantitativo de aproximación
antes de transferir la dinámica al problema gravitatorio. En paralelo, los hitos
canónicos GQ1–GQ5 conservan sus criterios prerregistrados.

Hasta cinco pruebas discriminantes para la próxima iteración:

1. **Recoupling independiente:** debe recuperar signo, Gram y q²; un fallo
   cuestiona UFT-QG-002 o sus convenciones, no toda LQG.
2. **Reloj con retorno:** \(\{T,C\}=p_T/M\) debe identificar pérdida de monotonía;
   un fallo de reloj global invalida esa reducción temporal.
3. **Cambio de representantes MC:** la clase mixta debe permanecer igual;
   un fallo cuestiona la prueba de UFT-GO-001 o la DGLA propuesta.
4. **Segundo orden local BV:** construir S1 y una obstrucción local concreta;
   si no es exacta se rechaza esa ansatz o se modifica explícitamente su dominio.
5. **Transferencia con materia fermiónica:** comprobar la supergraduación;
   ignorarla invalida el uso automático de UFT-X-001.

**No hay predicciones observacionales nuevas derivadas.** Para obtenerlas falta
un vínculo dinámico con el régimen gravitatorio y observables materiales.
Skills aplicadas: metacognicion-operativa al controlar evidencia y acciones;
investigador-elite y colaborador-cientifico al delimitar física; colaborador-
matematica-pura en MC/BV; teoria-original en las tres estructuras A–O;
scientific-writing en trazabilidad; sympy en el contraste matricial opcional.
