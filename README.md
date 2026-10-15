# Cañitas Málaga

Web de Cañitas Málaga (ME Málaga by Meliá): el restaurante Cañitas Málaga y el rooftop Cañitas al Fresco, en español e inglés.

La web es HTML/CSS/JS estático generado por un script de Python sin dependencias. La versión de GitHub Pages es una **vista previa** (lleva `noindex`); la web definitiva se monta en WordPress + Elementor con la exportación de `wordpress/`.

## Estructura

```
scripts/build.py           Generador: plantilla común, cabecera, pie, SEO, datos estructurados, exportación WordPress
scripts/pages.py           Textos de las páginas (ES / EN)
scripts/legal.py           Aviso legal, privacidad, cookies, condiciones de compra (datos de empresa en EMPRESA)
scripts/menus_data.py      Las cartas en HTML (platos y precios)
scripts/media.py           Catálogo de fotos: nombre SEO, foto original y texto alternativo ES / EN
scripts/process_images.py  Genera fotos, imágenes para redes, iconos y copia las cartas en PDF
css/styles.css             Estilos (índigo #28265a; Cañitas al Fresco en verde #647058 con Custard)
js/main.js                 Menú, cabecera al hacer scroll, parallax, acordeón y galería
assets/                    Fotos, fuentes, iconos, logos y cartas en PDF generados
wordpress/                 Exportación para WordPress (ver wordpress/LEEME.md)
imagenes/                  Material original sin optimizar (no se versiona)
```

Las páginas generadas (`index.html`, `en/`, `canitas-maite/`, `carta/`…) no se editan a mano.

## Cambiar algo

1. Edita el texto en `scripts/pages.py`, `scripts/legal.py` o `scripts/menus_data.py`.
2. Si cambian fotos o cartas: añade el original a `imagenes/`, regístralo en `scripts/media.py` y ejecuta
   `python3 scripts/process_images.py` (necesita `pip install pillow pymupdf`).
3. Genera la web y la exportación de WordPress:

```bash
python3 scripts/build.py
```

Configuración al principio de `scripts/build.py`: dominio definitivo (`SITE_URL`), ruta de la mediateca de WordPress (`WP_MEDIA`) y el proyecto de Adobe Fonts con Custard (`ADOBE_FONTS_KIT`).

## Desarrollo local

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080`.

## Despliegue

Cada `push` a `main` publica la vista previa en GitHub Pages (`.github/workflows/deploy.yml`): https://canitasgastro.github.io/canitas-malaga/
