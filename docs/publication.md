# Publicación en stevencabascango/UFT

El propietario autorizó publicar este proyecto en
<https://github.com/stevencabascango/UFT>. El repositorio remoto se inspeccionó
vacío antes de implementar. El script publica el commit revisado, comprueba la
identidad, la URL, el árbol limpio y el SHA remoto. No usa `force push` ni cambia
la configuración Git global.

```bash
cd /home/asus/UFT
python3 scripts/publish.py
```

Utiliza la autenticación GitHub CLI que ya existe en tu terminal. Si falta el CLI
o necesitas completar login desde un terminal interactivo, existe
`scripts/connect_and_publish.py`: conserva el ejecutable existente y verifica
SHA-256 de la distribución oficial cuando debe descargarlo. No se vuelven a
pedir códigos ni se solicitan tokens por chat.

Si GitHub contiene cambios posteriores a la inspección, el script se detiene o
exige una integración revisada. No sobrescribe contenidos remotos desconocidos.
Una salida `published:true` y un SHA confirmado acreditan publicación; tener un
ZIP, un origin o una cuenta autorizada no la acreditan.

## Restricciones detectadas durante la construcción

`git ls-remote` falló porque el sandbox no resuelve `github.com`. El intento de
escritura del conector produjo `403 Resource not accessible by integration`.
La cuenta puede tener permiso de push y el conector seguir careciendo de él.
No se interpreta ese fallo como credenciales personales inválidas ni se requiere
repetir OAuth. Ejecutar el comando anterior en el terminal WSL con conectividad
usa la autorización existente.

El ZIP y el Git bundle se generan desde el commit cerrado con
`python3 scripts/build_release.py --package`. Se publican fuera del checkout para
evitar archivos recursivos; el manifiesto SHA-256 identifica sus bytes exactos.
Antes de afirmar publicación se verifica otra vez el commit remoto.
