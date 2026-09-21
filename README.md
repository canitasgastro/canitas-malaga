# Cañitas Maite Málaga

Web de Cañitas Maite en Málaga (ME Málaga by Meliá): dos espacios —Cañitas Maite y Cañitas al Fresco— bajo una misma firma culinaria.

Sitio estático (HTML/CSS/JS, sin build ni dependencias).

## Estructura

```
index.html         Contenido de la página
css/styles.css      Estilos (identidad índigo #28265a + blanco, Federo/Archivo)
js/main.js          Menú, header al hacer scroll, parallax, acordeón de FAQ
assets/img/         Fotografías optimizadas para la web (JPEG comprimido)
assets/logos/       Logos de cada espacio en PNG con transparencia
assets/favicon.svg  Favicon
imagenes/           Material fuente sin optimizar (NO se sube al repo, ver .gitignore)
scripts/process_images.py  Genera assets/img y assets/logos a partir de imagenes/
.github/workflows/  Despliegue automático a GitHub Pages
```

### Actualizar fotos o logos

1. Añade el material nuevo dentro de `imagenes/<espacio>/` (no se versiona, solo vive en local).
2. Ajusta las rutas en `scripts/process_images.py` si cambian los nombres de archivo.
3. Ejecuta `python scripts/process_images.py` para regenerar `assets/img/` y `assets/logos/` ya redimensionados y comprimidos.
4. Haz commit solo de los archivos dentro de `assets/` (lo de `imagenes/` queda excluido automáticamente).

## Desarrollo local

Al ser HTML/CSS/JS estático, basta con abrir `index.html` en el navegador, o servirlo con cualquier servidor estático, por ejemplo:

```bash
python -m http.server 8000
```

y visitar `http://localhost:8000`.

## Despliegue

Cada `push` a `main` publica automáticamente el sitio en GitHub Pages mediante el workflow en `.github/workflows/deploy.yml`. Es necesario activar Pages una vez en el repositorio: **Settings → Pages → Source: GitHub Actions**.
