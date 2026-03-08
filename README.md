# 🐍 Snake Game - Web Version

Un juego clásico de Snake desarrollado con Flask y JavaScript, con sistema de puntuación, leaderboard y modo autoplay.

## 🎮 Características

- **Juego clásico de Snake**: Controla la serpiente para comer comida y crecer
- **Sistema de puntuación**: Gana puntos por cada comida que consumas
- **Leaderboard**: Guarda y muestra las mejores puntuaciones
- **Modo Autoplay**: Observa cómo la IA juega automáticamente
- **Diseño responsive**: Funciona en dispositivos móviles y de escritorio
- **Interfaz moderna**: UI limpia y atractiva con CSS moderno

## 🚀 Demostración

[Link al demo en Vercel](https://tu-app.vercel.app) - _(Reemplazar con tu URL de Vercel)_

## 📋 Requisitos

- Python 3.8+
- Flask

## 🛠️ Instalación y Ejecución Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/snake-game.git
cd snake-game
```

### 2. Crear entorno virtual

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

### 5. Abrir en el navegador

Visita `http://localhost:5000` en tu navegador.

## Cómo Jugar

### Controles

- **Flechas del teclado** o **WASD**: Mover la serpiente
- **Espacio**: Pausar/reanudar el juego
- **R**: Reiniciar el juego
- **Tecla 'A'**: Activar/desactivar modo autoplay

### Objetivo

Controla la serpiente para comer la comida (manzanas rojas) sin chocar contra:

- Las paredes del juego
- El propio cuerpo de la serpiente

Cada vez que comes, la serpiente crece y tu puntuación aumenta.

## 🏆 Leaderboard

El juego guarda automáticamente las mejores puntuaciones en `leaderboard.json`.
Las puntuaciones se muestran en orden descendiente, con el nombre del jugador y su puntuación.

## 🤖 Modo Autoplay

El modo autoplay utiliza un algoritmo simple que:

1. Calcula la distancia a la comida
2. Evita obstáculos (paredes y propio cuerpo)
3. Toma el camino más seguro hacia la comida

## 📁 Estructura del Proyecto

```
snake-game/
├── app.py                 # Aplicación principal Flask
├── static/
│   └── style.css         # Estilos CSS
├── templates/
│   └── index.html        # Plantilla HTML principal
├── autoplay_fix.js        # Lógica del modo autoplay
├── leaderboard.json       # Base de datos de puntuaciones
├── requirements.txt       # Dependencias de Python
├── vercel.json          # Configuración de Vercel
├── api/
│   └── index.py         # Función serverless para Vercel
└── README.md            # Este archivo
```

## 🚀 Despliegue en Vercel

### Método 1: Usando GitHub (Recomendado)

1. **Sube tu código a GitHub**
2. **Conecta tu repositorio con Vercel**
   - Ve a [vercel.com](https://vercel.com)
   - Importa tu repositorio de GitHub
   - Vercel detectará automáticamente que es una aplicación Python

3. **Configura las variables de entorno** (si es necesario)

4. **Despliega** - Vercel construirá y desplegará tu aplicación automáticamente

### Método 2: Usando Vercel CLI

1. **Instala Vercel CLI**

```bash
npm i -g vercel
```

2. **Inicia sesión en Vercel**

```bash
vercel login
```

3. **Despliega tu proyecto**

```bash
vercel
```

### Configuración Específica para Vercel

El proyecto incluye configuración específica para Vercel:

- `vercel.json`: Configura el servidor y las rutas
- `api/index.py`: Adaptador para que Flask funcione como función serverless
- `requirements.txt`: Dependencias optimizadas para producción

## 🔧 Configuración

### Variables de Entorno

- No se requieren variables de entorno para este proyecto

### Personalización

Puedes personalizar:

- Velocidad del juego en `app.py`
- Colores y estilos en `static/style.css`
- Tamaño del tablero en `templates/index.html`

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Error de módulo no encontrado**

   ```bash
   pip install flask
   ```

2. **Error de puerto en uso**
   - Cambia el puerto en `app.py` (línea `app.run(debug=True, port=5000)`)

3. **El leaderboard no guarda puntuaciones**
   - Asegúrate de que el archivo `leaderboard.json` tenga permisos de escritura

### En Vercel

1. **Error 500: Internal Server Error**
   - Revisa los logs en el dashboard de Vercel
   - Asegúrate de que `requirements.txt` esté completo

2. **La página no carga**
   - Verifica que `vercel.json` esté configurado correctamente
   - Comprueba que todos los archivos estén subidos

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Joseph** - _Desarrollador Full Stack_ - [GitHub](https://github.com/pochonski)

## 🙏 Agradecimientos

- Gracias a la comunidad de desarrolladores de Flask
- Inspirado en el juego clásico de Snake de Nokia
- Diseño UI inspirado en tendencias modernas de web design

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!

## 📞 Contacto

Si tienes preguntas o sugerencias:

- Email: joseph@19102005@gmail.com
- GitHub Issues: [Abre un issue aquí](https://github.com/tu-usuario/snake-game/issues)
