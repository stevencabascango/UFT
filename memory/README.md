# Memoria científica portable

`claims.json` exporta las afirmaciones registradas en `ScientificMemory`, sus
revisiones e hipótesis. `exports/knowledge.json` añade objetivos, candidatos,
conexiones, criterios, cobertura, eventos, alertas e historial integrado.

El índice local SQLite está en `.uft/` y no se publica. Los archivos de cálculo y
auditoría se versionan junto con las fuentes del programa. Las rutas absolutas de
algunas ejecuciones documentan la máquina de origen; la reproducción usa los
scripts y rutas relativas del checkout.

`python3 scripts/seed_research.py` registra el ciclo sin inferir demostraciones.
La opción explícita `--apply-reviewed-audits` comprueba los hashes del arbitraje
interno cerrado y pasa por las puertas de auditoría de GENIUS. No sustituye una
revisión externa ni ejecuta un verificador formal. Un cambio de artefacto obliga
a obtener otra revisión.

Los nueve lemas confirmados están delimitados; las tres propuestas de teoría
completa no heredan ese estado. Los controles falsos conservan `refuted`.
