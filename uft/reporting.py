"""Portable evidence exports. Formatting never upgrades scientific states."""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from .inventory import utc_now, write_json

REPORT_SECTIONS = (
    "Pregunta y alcance", "Fuentes y materiales examinados", "Estado previo",
    "Análisis matemático", "Análisis físico", "Conexiones justificadas y propuestas",
    "Resultados y evidencia", "Objeciones y contraejemplos", "Impacto sobre los tres objetivos",
    "Actualizaciones de memoria y alertas", "Próxima comprobación prioritaria",
)
CRITERIA = {
    "mathematical_coherence": "Coherencia matemática", "testability": "Contrastabilidad",
    "correspondence": "Correspondencia", "operational_definitions": "Definiciones operacionales",
    "explanation_unification": "Explicación y unificación", "parsimony": "Parsimonia",
    "non_empirical": "Evaluación no empírica",
}


def as_rows(value) -> list[dict]:
    return list(value.values()) if isinstance(value, dict) else (value or [])


def render_scientific_report(record: dict) -> str:
    """Require scope, seven criteria and at most five actual discriminating tests."""
    sections = record.get("sections", {})
    if set(sections) != set(REPORT_SECTIONS) or not all(str(v).strip() for v in sections.values()):
        raise ValueError("Report needs all eleven nonempty scientific sections")
    criteria = record.get("criteria", {})
    if set(criteria) != set(CRITERIA):
        raise ValueError("Report needs exactly the seven evaluation criteria")
    tests = record.get("discriminating_tests", [])
    if not isinstance(tests, list) or len(tests) > 5:
        raise ValueError("Use at most five discriminating tests")
    allowed = {"Cumplido en el alcance declarado", "Parcial", "Pendiente", "Incumplido", "No aplicable, con justificación"}
    lines = ["# " + record["title"], "", f"ID: {record['id']} · {record.get('date', utc_now())}", ""]
    for index, name in enumerate(REPORT_SECTIONS, 1):
        lines += [f"## {index}. {name}", "", str(sections[name]), ""]
    lines += ["## Evaluación de los siete criterios", "", "| Criterio | Estado | Evidencia concreta | Limitaciones y siguiente comprobación |",
              "|---|---|---|---|"]
    escape = lambda x: str(x).replace("|", "\\|").replace("\n", " ")
    for key, label in CRITERIA.items():
        item = criteria[key]
        if item.get("status") not in allowed or not all(item.get(k) for k in ("evidence", "limitations", "next_check")):
            raise ValueError("Every criterion needs a valid state, evidence, limits and next check")
        lines.append("| " + " | ".join(map(escape, (label, item["status"], item["evidence"],
                                                   item["limitations"] + "; " + item["next_check"]))) + " |")
    lines += ["", "## Predicciones o pruebas discriminantes", ""]
    if not tests:
        if not record.get("prediction_gap"):
            raise ValueError("Absence of predictions must identify the gap and required work")
        lines.append(record["prediction_gap"])
    for item in tests:
        if not all(item.get(k) for k in ("test", "failure_questions", "scope")):
            raise ValueError("Each test must identify what failure would question and its scope")
        lines += [f"- {item['test']} Fallo cuestiona: {item['failure_questions']}. Alcance: {item['scope']}."]
    return "\n".join(lines) + "\n"


def export_snapshot(snapshot: dict, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "knowledge.json", snapshot)
    entities = as_rows(snapshot.get("entities"))
    coverage = as_rows(snapshot.get("coverage"))
    assessments = as_rows(snapshot.get("assessments"))
    for name, rows in (("entities", entities), ("coverage", coverage), ("assessments", assessments),
                       ("alerts", as_rows(snapshot.get("alerts"))), ("links", as_rows(snapshot.get("links")))):
        columns = sorted({k for row in rows for k in row}) or ["id"]
        with (output / (name + ".csv")).open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in row.items()})
    graph = ["digraph UFT {", '  rankdir="LR";']
    for row in entities:
        graph.append("  " + json.dumps(row["id"]) + " [label=" + json.dumps(row["id"] + "\\n" + row.get("status", "")) + "];")
    for link in as_rows(snapshot.get("links")):
        graph.append("  " + json.dumps(link["source"]) + " -> " + json.dumps(link["target"]) +
                     " [label=" + json.dumps(link.get("relation", "")) + "];")
    (output / "knowledge.dot").write_text("\n".join(graph + ["}", ""]), encoding="utf-8")
    (output / "dashboard.html").write_text(dashboard(snapshot), encoding="utf-8")
    return {"entities": len(entities), "coverage_cells": len(coverage), "criteria_assessments": len(assessments),
            "files": [str(output / name) for name in ("knowledge.json", "entities.csv", "coverage.csv", "assessments.csv", "alerts.csv", "links.csv", "knowledge.dot", "dashboard.html")]}


def dashboard(snapshot: dict) -> str:
    data = json.dumps(snapshot, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
    return '''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>UFT · Evidencia y preguntas abiertas</title><style>
body{margin:0;background:#0d1726;color:#ecf2fa;font:16px system-ui}main{max-width:1250px;margin:auto;padding:2rem}
h1{font-size:2.4rem}a{color:#9cd8ff}input,select,button{padding:.7rem;border-radius:6px;border:1px solid #7086a0;background:#15283e;color:white}
.cards{display:flex;gap:1rem;flex-wrap:wrap}.card{padding:1rem;background:#17283e;border-radius:8px;flex:1;min-width:170px}
#items{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem}button.item{text-align:left;cursor:pointer;white-space:pre-wrap}
pre{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.5;background:#142337;padding:1rem}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:.5rem;border-bottom:1px solid #41546b}
.muted{color:#b1c3d7}svg{width:100%;min-height:300px;background:#122136}line{stroke:#627c9c}circle{fill:#63b6df}text{fill:white;font:12px system-ui}</style>
<main><p class="muted">GENIUS-5000 / Investigación integrada / Exportación local</p><h1>Tres programas. Evidencia explícita.</h1>
<p>Googly · Unificación · Gravedad cuántica, tiempo y LQG. Las conexiones requieren mapas e hipótesis. Una ficha o un cálculo finito no acredita una teoría completa.</p>
<div class="cards" id="stats"></div><h2>Mapa y registro</h2>
<label>Buscar <input id="query" placeholder="ID, enunciado o hipótesis"></label>
<label>Programa <select id="programme"><option value="">Todos</option><option>googly</option><option>unification</option><option>quantum_gravity</option></select></label>
<label>Estado <select id="state"><option value="">Todos</option></select></label><p id="count"></p>
<svg id="graph" viewBox="0 0 1100 500" role="img" aria-label="Mapa de los nodos filtrados, máximo 30. Las aristas conservan su tipo en el registro."></svg>
<div id="items"></div><h2>Detalle y procedencia</h2><pre id="detail">Selecciona un nodo para consultar sus hipótesis, evidencias y revisión.</pre>
<h2>Cobertura declarada</h2><p>Revisado, parcialmente revisado, pendiente, bloqueado o no aplicable con justificación. La revisión se limita al alcance de cada celda.</p><div id="coverage"></div>
<h2>Alertas</h2><pre id="alerts"></pre><p><a href="knowledge.json">JSON versionado</a> · <a href="coverage.csv">Cobertura CSV</a> · <a href="assessments.csv">Siete criterios CSV</a> · <a href="knowledge.dot">Grafo DOT</a></p>
<p class="muted">Instantánea exportada. Esta página no programa ejecuciones ni consulta modelos. Revisión interna y verificación formal son estados distintos.</p></main>
<script type="application/json" id="data">''' + data + '''</script><script>
const d=JSON.parse(document.getElementById('data').textContent),rows=x=>Array.isArray(x)?x:Object.values(x||{}),entities=rows(d.entities),links=rows(d.links);
const el=id=>document.getElementById(id),node=(t,s)=>{const x=document.createElement(t);x.textContent=s;return x};
for(const [label,n]of [['Entidades',entities.length],['Relaciones',links.length],['Celdas de cobertura',rows(d.coverage).length],['Alertas registradas',rows(d.alerts).length]]){const x=node('div',label+'\n'+n);x.className='card';el('stats').append(x)}
for(const s of [...new Set(entities.map(e=>e.status))].sort())el('state').append(node('option',s));
function render(){const q=el('query').value.toLowerCase(),p=el('programme').value,s=el('state').value;
const shown=entities.filter(e=>(!q||JSON.stringify(e).toLowerCase().includes(q))&&(!p||(e.objectives||[]).includes(p))&&(!s||e.status===s));
el('count').textContent=shown.length+' entidades; el grafo muestra las primeras 30.';el('items').replaceChildren();
for(const e of shown){const b=node('button',e.id+' · '+e.status+'\n'+e.statement);b.className='item';b.onclick=()=>el('detail').textContent=JSON.stringify(e,null,2);el('items').append(b)}
const g=el('graph');g.replaceChildren();const small=shown.slice(0,30),pos=new Map(small.map((e,i)=>[e.id,[85+(i%7)*150,60+Math.floor(i/7)*100]]));
const sv=(tag,attrs)=>{const x=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const[k,v]of Object.entries(attrs))x.setAttribute(k,v);g.append(x);return x};
for(const l of links){if(!pos.has(l.source)||!pos.has(l.target))continue;const a=pos.get(l.source),b=pos.get(l.target);const x=sv('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1]});x.append(node('title',l.relation+': '+l.source+' → '+l.target));}
for(const e of small){const[x,y]=pos.get(e.id);const c=sv('circle',{cx:x,cy:y,r:10,tabindex:0});const detail=()=>el('detail').textContent=JSON.stringify(e,null,2);c.onclick=detail;c.onkeydown=v=>{if(v.key==='Enter')detail()};sv('text',{x:x-60,y:y+28}).textContent=e.id.slice(0,23)}
}for(const id of ['query','programme','state'])el(id).addEventListener('input',render);
const counts={};for(const c of rows(d.coverage))counts[c.status]=(counts[c.status]||0)+1;
for(const[k,v]of Object.entries(counts))el('coverage').append(node('p',k+': '+v));el('alerts').textContent=JSON.stringify(rows(d.alerts),null,2);render();
</script></html>'''
