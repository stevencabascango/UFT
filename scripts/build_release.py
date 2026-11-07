#!/usr/bin/env python3
"""Build a real TeX/PDF guide and reproducible archives from a closed Git commit."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(*command, timeout=120):
    return subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True, timeout=timeout)


def build_pdf():
    compiler = shutil.which("texcompile")
    if not compiler:
        raise RuntimeError("texcompile unavailable; PDF remains pending, no fake artifact generated")
    checks = json.loads((ROOT / "evidence/checks.json").read_text())
    if not checks["passed"]:
        raise RuntimeError("Close successful checks before generating the release guide")
    tests = checks["tests"]["run"]
    tex = r'''\documentclass[11pt,a4paper]{article}
\usepackage[spanish]{babel}
\usepackage[margin=2.3cm]{geometry}
\usepackage{amsmath,amssymb,longtable,booktabs,hyperref}
\hypersetup{colorlinks=true,urlcolor=blue,linkcolor=blue}
\title{UFT --- GENIUS-5000\\Investigación integrada, evidencia y análisis incremental}
\author{Repositorio de investigación del propietario stevencabascango\\Elaboración y revisión asistidas por IA; sin afiliaciones atribuidas}
\date{Entrega reproducible --- noviembre de 2026}
\begin{document}\maketitle
\begin{abstract}
Infraestructura para investigar el problema de Googly, la unificación de campos
y la cuantización de relatividad general, incorporando tiempo relacional y LQG.
Se mantienen tres programas independientes y conexiones condicionadas. Esta
entrega contiene bancos finitos revisados y herramientas operativas: no es una
teoría física completa ni evidencia observacional nueva.
\end{abstract}
\tableofcontents\newpage
\section{Metas y fuentes vigentes}
Las metas iniciales se contrastaron con la META del BRAIN UFT y los manifiestos
compartidos del Protocolo Maestro. Se preservan los quince hitos G1--G5, U1--U5 y
GQ1--GQ5, sus criterios y antecedentes. Un resumen antiguo con tres objetivos de
organización no sustituye la meta añadida de cuantizar RG. Catorce fuentes se
inventariaron con SHA-256. Sus etiquetas reportadas no se importan como nuevas
demostraciones. La revisión es finita y su alcance está declarado.

\section{Tres programas y un puente condicionado}
\subsection{Googly}
La propuesta de obstrucciones mixtas estudia una pregunta matemática mínima antes
de identificarla con helicidades gravitatorias. Para una DGLA cohomológica sobre
característica cero y elementos cerrados $a_+,a_-\in L^1$, sobre
$k[\epsilon,\eta]/(\epsilon^2,\eta^2)$ se escribe
\[
 a=\epsilon a_++\eta a_-+\epsilon\eta b,\qquad
 da+\tfrac12[a,a]=0
 \quad\Longleftrightarrow\quad db+[a_+,a_-]=0.
\]
La clase de $[a_+,a_-]$ en $H^2(L)$ obstruye esta prolongación, únicamente en el
orden truncado indicado. Los dos ejemplos finitos conservan o eliminan una
primitiva. Faltan un complejo twistorial físico, pesos, realidad, gauge,
reconstrucción, ambas helicidades y la relación con Einstein. Ninguno de esos
pasos se deduce de un formalismo $L_\infty$ por sí solo.

\subsection{Unificación}
Se propone un filtro de obstrucciones locales de acoplamiento, con antecedentes
BV/BRST. Si $S=S_0+gS_1+g^2S_2+\cdots$ satisface la maestra clásica,
\[
 s S_1=0,\qquad sS_2+\tfrac12(S_1,S_1)=0,\qquad s=(S_0,\cdot).
\]
Es un criterio de segundo orden en funcionales locales, no un teorema cuántico
a todos los órdenes. Un tensor totalmente antisimétrico con $f_{012}=f_{034}=1$
en dimensión cinco conserva la métrica interna euclídea y falla Jacobi:
$J(e_1,e_2,e_3)=-e_4$. El control $\mathfrak{su}(2)$ sí pasa.
No se derivan gravedad dinámica, materia quiral, anomalías ni una unificación
física por superar ese control.

\subsection{Gravedad cuántica, tiempo y LQG}
Se usa $V=(\mathbb C^2)^{\otimes4}$ y el subespacio
$\mathcal H_\gamma=\mathrm{Inv}_{SU(2)}V$ de dimensión dos. Con
$J^a=\sigma^a/2$ y orientación $\epsilon_{xyz}=1$,
\[
 q=\epsilon_{abc}J_1^aJ_2^bJ_3^c,\qquad H=\kappa q.
\]
En la base racional no ortonormal declarada,
\[
 G=\begin{pmatrix}1&0\\0&3\end{pmatrix},\quad
 Q=\begin{pmatrix}0&-3i/4\\i/4&0\end{pmatrix},\quad
 Q^\dagger G=GQ,\quad Q^2=\tfrac3{16}I.
\]
El reloj ideal $T\in\mathbb R$ y la restricción impuesta $C=p_T+H$ dan
\[
 \Psi(T)=e^{-iH(T-T_0)/\hbar}\psi_0.
\]
El producto físico se define por evaluación y es independiente de $T_0$ bajo
autoadjunción de $H$. Las soluciones no nulas son generalizadas, no elementos
normales de $L^2(dT)$. $J,q$ son adimensionales, $[\kappa]$ es energía y
$[\hbar]$ es energía multiplicada por tiempo. La estructura de Gauss no equivale al conjunto
de restricciones de LQG. No se obtiene un reloj material, tratamiento UV,
límite continuo ni recuperación de Einstein. Área discreta no implica tiempo
discreto.

\subsection{Conexión admitida}
El corrimiento $L^n=\mathcal F^{\mathrm{gh}=n-1}$ relaciona el criterio BV con
Maurer--Cartan bajo hipótesis de localidad, contorno, grados y paridad. En el
banco bosónico la paridad Grassmann coincide con número fantasma módulo dos;
con fermiones físicos se necesita conservar graduación adicional. Este puente
abstracto no identifica el ejemplo finito con gravedad twistorial.

\section{Auditoría y estados}
Doce afirmaciones fueron revisadas: nueve confirmadas con hipótesis y tres
afirmaciones universales falsas refutadas por contraejemplos. El productor y el
comprobador independiente usan implementaciones distintas, comparan signos,
matrices y residuos exactos. Una reconstrucción adicional usa SymPy.
Las demostraciones escritas y el alcance físico se revisan por separado.
La revisión es interna, con posibles errores compartidos del mismo modelo;
no es revisión externa ni verificación Lean. No se evalúa competencia individual
de cinco mil agentes.

\begin{longtable}{p{.29\linewidth}p{.62\linewidth}}
\toprule Estado & Evidencia y límite\\\midrule
Establecido en una fuente & Fuente consultada y resultado usado, hipótesis conservadas.\\
Propuesta o conjetura & Construcción o enunciado pendiente, sin promoción implícita.\\
Evidencia simbólica o numérica & Código, entradas, entorno y salida; alcance finito.\\
Demostrado bajo hipótesis & Argumento delimitado y auditoría registrada para esa versión.\\
Verificado formalmente & Herramienta, archivos, dependencias y log; ninguno atribuido en este ciclo.\\
Refutado & Contraejemplo documentado; no puede ascender por consenso.\\
En revisión & Objeción o dependencia modificada, con impacto transitivo.\\\bottomrule
\end{longtable}

\section{Cobertura y siete criterios}
El inventario comprende 108 celdas de cobertura matemática, física, documental y
operativa. Hay 21 evaluaciones iniciales para las tres metas. Los programas
completos permanecen pendientes aunque un modelo finito cumpla un criterio en
su dominio. Los informes incluyen evidencia, límites y siguiente comprobación.
Los siete criterios son coherencia matemática, contrastabilidad, correspondencia,
definiciones operacionales, explicación/unificación, parsimonia y evaluación no
empírica. No se asignan probabilidades inventadas de verdad. Se registran los
argumentos metodológicos de Dawid y sus críticas separadamente de datos empíricos.

\section{Infraestructura reproducible}
El catálogo tiene exactamente 5.000 fichas en diez divisiones. Cada ficha distingue
capacidades objetivo, evaluadas y pendientes. Las 27 habilidades se comparten por
adaptadores conservadores Claude--Codex. Los equipos cubren siete funciones con
presupuestos, concurrencia, reintentos y condiciones de parada.
La memoria SQLite transaccional conserva historial y fuentes. El mapa tipa ocho
relaciones y registra mapas explícitos, hipótesis y revisión. La dirección de una
arista propagante es premisa a dependiente. Cambios de hipótesis o rechazo de una
arista invalidan los resultados afectados. Los eventos idempotentes conservan
fallos y permiten recuperación limitada.

La suite cerrada ejecutó TESTCOUNT pruebas con resultado satisfactorio. El detalle,
incluidas comprobaciones negativas, está en \texttt{evidence/checks.json}. Las
pruebas verifican el software y sus casos de referencia; no certifican teorías
completas ni excelencia científica de cada ficha.

\section{Actividad real, memoria y alertas}
El observador de catorce archivos compartidos ejecutó dos pasadas reales sin
cambios ni alertas. Opera por eventos y procesos acotados, sin llamadas de pago
ni modificación del BRAIN canónico. Se incluyen plantillas de programación;
el sandbox no pudo acceder a systemd de usuario ni crontab, por lo que no se
afirma vigilancia de fondo activa. Las alertas UFT tienen namespace propio y
se mantienen silenciosas sin cambios significativos.

Claude CLI se intentó con límite de quince segundos y terminó por timeout.
Falta su informe: la comparación Claude--Codex queda pendiente. No se sustituye
esa ausencia por un informe ficticio. Los informes actuales corresponden a
ejecuciones separadas de Codex con sus límites de independencia.

\section{Reproducir, inspeccionar y extender}
Desde el checkout con Python3.11 o posterior:
\begin{verbatim}
python3 -m uft validate
python3 -m uft init
python3 scripts/seed_research.py
python3 -m uft export
python3 -m uft cycle --output .uft/new-cycle
python3 scripts/check.py --output .uft/checks.json
\end{verbatim}
El replay opcional de auditorías usa \texttt{--apply-reviewed-audits} y comprueba
las huellas de los argumentos cerrados. Nunca deduce una prueba general de una
simulación. El panel \texttt{exports/dashboard.html} permite filtrar estados,
consultar nodos y ver enlaces sin servicios externos. JSON, CSV y DOT permiten
revisión y transferencia a otras herramientas.

\section{Siguientes pasos discriminantes}
\begin{enumerate}
\item Reproducir signo y hermiticidad métrica de $q$; un fallo invalida la fórmula
del banco y las transiciones derivadas, no refuta toda LQG.
\item Sustituir el Hamiltoniano por uno no autoadjunto; el cambio de norma
identifica una hipótesis esencial del reloj ideal.
\item Calcular la clase mixta de una DGLA candidata física con pesos y gauge
fijos; una obstrucción no nula impide esa prolongación en ese orden.
\item Verificar Jacobi y la obstrucción BV de un acoplamiento propuesto; fallar
cuestiona esa extensión local, no todas las estructuras gauge superiores.
\item Construir un reloj material con retroacción y una reducción semiclásica
controlada; la ausencia de ese paso impide llamar al banco cuantización de RG.
\end{enumerate}
No se han derivado predicciones observacionales nuevas de gravedad o unificación.
Obtenerlas requiere dinámica física adicional y un diccionario operacional.

\section{Mapa de lectura}
\begin{itemize}
\item \texttt{research/*/proposal.md}: tres propuestas completas A--O.
\item \texttt{research/first\_cycle.md}: informe obligatorio de once secciones.
\item \texttt{research/audits/}: reconstrucción matemática y revisión científica.
\item \texttt{data/}: metas vigentes y procedencia de fuentes.
\item \texttt{references/}: bibliografía verificada y límites de acceso.
\item \texttt{docs/}: arquitectura, instalación, requisitos y limitaciones.
\item \texttt{memory/}, \texttt{exports/}, \texttt{evidence/}: trazabilidad real.
\end{itemize}
Repositorio de destino: \url{https://github.com/stevencabascango/UFT}.
La publicación requiere comprobar el SHA remoto: un paquete local no equivale a
un push confirmado.
\end{document}
'''.replace("TESTCOUNT", str(tests))
    source = ROOT / "docs/UFT_guide.tex"
    source.write_text(tex, encoding="utf-8")
    result = run(compiler, str(source), timeout=180)
    candidates = [source.with_suffix(".pdf"), ROOT / "UFT_guide.pdf"]
    built = next((p for p in candidates if p.is_file()), None)
    if built is None:
        raise RuntimeError("Compiler returned without a PDF; inspect its actual log")
    target = ROOT / "Descargas/UFT_guide.pdf"
    shutil.copy2(built, target)
    return target


def package(output_dir: Path):
    if run("git", "status", "--porcelain").stdout.strip():
        raise RuntimeError("Review and commit every change before packaging")
    commit = run("git", "rev-parse", "HEAD").stdout.strip()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / "UFT-GENIUS5000.zip"
    bundle = output_dir / "UFT-GENIUS5000.bundle"
    run("git", "archive", "--format=zip", "--prefix=UFT/", "--output=" + str(archive), "HEAD")
    run("git", "bundle", "create", str(bundle), "--all")
    run("git", "bundle", "verify", str(bundle))
    manifest = output_dir / "UFT-GENIUS5000-SHA256SUMS.txt"
    manifest.write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n" for p in (archive, bundle)), encoding="utf-8")
    receipt = output_dir / "UFT-release.json"
    receipt.write_text(json.dumps({"commit": commit, "repository": "https://github.com/stevencabascango/UFT",
                                  "zip": str(archive), "bundle": str(bundle), "sha256_manifest": str(manifest),
                                  "publication": "Must be independently confirmed against remote SHA"}, ensure_ascii=False, indent=2) + "\n")
    return [archive, bundle, manifest, receipt]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--package", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=ROOT.parent)
    args = parser.parse_args()
    produced = []
    if args.pdf:
        produced.append(build_pdf())
    if args.package:
        produced += package(args.output_dir.resolve())
    print(json.dumps({"produced": [str(p) for p in produced]}, indent=2))


if __name__ == "__main__":
    main()
