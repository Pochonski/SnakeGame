# Snake Game

## Descripción

Snake Game es una implementación clásica del juego "Snake" que se ejecuta en el navegador. El proyecto incluye:

- Un frontend (HTML, CSS y JavaScript) que renderiza el tablero, gestiona la entrada del jugador (teclado) y controla la lógica del juego (movimiento de la serpiente, comida, colisiones, puntuación).
- Un backend mínimo en Flask (`app.py`) que se encarga únicamente de almacenar y servir una tabla de puntuaciones (leaderboard) mediante una API REST simple.

El objetivo del proyecto es ser un ejemplo sencillo y completo de una pequeña aplicación web con una parte interactiva en el cliente y una API en el servidor para persistir puntuaciones. Es ideal para aprender a conectar un juego frontend con un backend ligero y para experimentar con pequeñas mejoras (autoplay, almacenamiento en DB, autenticación, tests, etc.).

El frontend sirve la UI en `templates/index.html` y utiliza `autoplay_fix.js` si se activa una lógica de juego automática; el servidor expone endpoints para recuperar y enviar puntuaciones que se guardan en `leaderboard.json`.

Juego de Snake con frontend en HTML/JS/CSS y un backend ligero en Flask que mantiene una tabla de puntuaciones (leaderboard) en `leaderboard.json`.

## Estructura del proyecto

- `app.py` — servidor Flask: rutas para servir la página (`/`) y API para obtener/enviar puntuaciones (`/api/leaderboard`, `/api/score`).
- `templates/index.html` — página del juego (frontend HTML + JS).
- `static/style.css` — estilos CSS.
- `autoplay_fix.js` — script auxiliar para autoplay (si aplica en el frontend).
- `leaderboard.json` — almacenamiento local de puntuaciones (archivo JSON que lee/escribe la aplicación).

## Requisitos

- Python 3.8 o superior
- `pip`
- (Opcional) un entorno virtual

Dependencias principales:

```sh
pip install Flask
```

Para congelar dependencias:

```powershell
venv\Scripts\Activate.ps1
pip freeze > requirements.txt
```

## Cómo ejecutar (Windows PowerShell)

1. Clona o copia el repositorio y abre una terminal en la carpeta del proyecto (la que contiene `app.py`).

2. (Opcional) Crea y activa un entorno virtual:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Instala dependencias:

```powershell
pip install Flask
```

4. Ejecuta la aplicación:

```powershell
# Ejecutar directamente con Python
python app.py
```

La aplicación escuchará por defecto en `http://127.0.0.1:5000` (o en `0.0.0.0:5000` si accedes desde otra máquina).

Alternativa con Flask CLI:

```powershell
$env:FLASK_APP = 'app.py'
flask run --host=0.0.0.0 --port=5000
```

## Endpoints

- GET `/api/leaderboard` — devuelve el ranking actual en JSON:

  Ejemplo:

  ```sh
  curl http://127.0.0.1:5000/api/leaderboard
  ```

- POST `/api/score` — enviar una puntuación nueva. Payload JSON: `{ "name": "TuNombre", "score": 123 }`

  Ejemplo con `curl`:

  ```sh
  curl -X POST http://127.0.0.1:5000/api/score \
    -H "Content-Type: application/json" \
    -d '{"name":"Ana","score":120}'
  ```

  Respuestas de error comunes:

  - `400` con `{"error": "El nombre es obligatorio."}` si `name` está vacío.
  - `400` con `{"error": "La puntuación debe ser numérica."}` si `score` no es convertible a entero.

## Formato de `leaderboard.json`

La app guarda un objeto JSON simple con pares `nombre: puntuación`, por ejemplo:

```json
{
  "Ana": 120,
  "Pedro": 90
}
```

## Modo automático (Autoplay)

El juego incluye un modo automático inteligente en el cliente que intenta encontrar caminos seguros hacia la comida y evita colisiones cuando es posible.

- Cómo activar/desactivar: mientras la partida está en ejecución, pulsa `Ctrl+K` para alternar el modo automático.
- Botón en la UI: también puedes alternar Auto-Play con el botón `Auto-Play` junto al botón "Cambiar nombre".
- Cómo activar/desactivar: mientras la partida está en ejecución, pulsa `Ctrl+K` para alternar el modo automático.
- Indicador visual: cuando el modo automático está activo aparece en la esquina superior izquierda del canvas el texto `🧠 Auto-Play Inteligente ON`.
- Restricciones:

  - El modo automático sólo se activa si la partida ya está en ejecución y la serpiente tiene longitud inicial; si lo intentas antes de empezar la partida no hará nada.
  - Si el algoritmo no encuentra una ruta segura hacia la comida, puede desactivarse automáticamente.
  - Mientras `autoplay` está activo, la entrada manual (teclas de dirección o gestos táctiles) se ignora.

- Cambiar el comportamiento por defecto: para habilitar autoplay por defecto al iniciar una partida, edita `templates/index.html` y en la función `initGame()` cambia la llamada `setAutoPlay(false)` por `setAutoPlay(true)`. Ten en cuenta que esto hará que la IA controle la serpiente siempre que la partida esté activa.

Ejemplo (usar durante una partida):

1. Inicia el juego (abre `http://127.0.0.1:5000` y pulsa Comenzar).
2. Pulsa `Ctrl+K` para activar Auto-Play.
3. Observa el indicador y deja que la IA juegue. Puedes volver a pulsar `Ctrl+K` para recuperar el control manual.

Notas:

- Si `leaderboard.json` no existe, la app lo crea cuando recibe puntuaciones.
- Asegúrate de no introducir comentarios ni texto no-JSON en `leaderboard.json`, porque la lectura fallará.

## Consejos para subir a Git

- Ignora el entorno virtual y archivos locales en `.gitignore`. Un ejemplo mínimo de `.gitignore`:

```
venv/
__pycache__/
*.pyc
leaderboard.json
```

Observación: si quieres versionar `leaderboard.json` (por ejemplo, con datos de ejemplo), no lo ignores; pero en producción suele ser un archivo mutable y local, por eso se recomienda ignorarlo.

- Antes de subir, genera `requirements.txt`:

```powershell
venv\Scripts\Activate.ps1
pip freeze > requirements.txt
```

## Desarrollo y pruebas rápidas

- Abre `http://127.0.0.1:5000` en el navegador para jugar.
- Usa las llamadas `curl` anteriores o una herramienta como Postman para probar la API.

## Posibles mejoras (sugerencias)

- Añadir autenticación simple para evitar suplantación de nombre.
- Persistir el leaderboard en una base de datos (SQLite) para evitar problemas de concurrencia a largo plazo.
- Añadir tests automatizados para endpoints y carga básica.

## Contacto / Contribuciones

Si quieres que añada un `requirements.txt`, un `.gitignore` completo o un script de deploy, dímelo y lo añado.

---

Archivo generado automáticamente: instrucciones para ejecutar y publicar el proyecto.
