# Cañitas Maite Málaga

Web de Cañitas Maite en Málaga (ME Málaga by Meliá): tres espacios —Eñe Lobby Bar, Cañitas Maite y Cañitas al Fresco— bajo una misma firma culinaria.

Sitio estático (HTML/CSS/JS, sin build ni dependencias).

## Estructura

```
index.html        Contenido de la página
css/styles.css     Estilos (identidad índigo #28265a + blanco, Federo/Archivo)
js/main.js         Menú, header al hacer scroll, parallax, acordeón de FAQ
assets/            Favicon y recursos SVG
.github/workflows/ Despliegue automático a GitHub Pages
```

## Desarrollo local

Al ser HTML/CSS/JS estático, basta con abrir `index.html` en el navegador, o servirlo con cualquier servidor estático, por ejemplo:

```bash
python -m http.server 8000
```

y visitar `http://localhost:8000`.

## Despliegue

Cada `push` a `main` publica automáticamente el sitio en GitHub Pages mediante el workflow en `.github/workflows/deploy.yml`. Es necesario activar Pages una vez en el repositorio: **Settings → Pages → Source: GitHub Actions**.
