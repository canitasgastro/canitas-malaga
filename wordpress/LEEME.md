# Montar la web en WordPress + Elementor

Esta carpeta tiene todo lo necesario para subir la web de Cañitas Málaga página a página. Se regenera sola con `python3 scripts/build.py`, así que no la edites a mano: cualquier cambio de texto se hace en `scripts/` y se vuelve a generar.

```
01-mediateca/                 Todas las fotos, logos, imágenes para redes y cartas en PDF (ES/EN)
02-estilos-y-script/          canitas.css, canitas.js y las fuentes (canitas-fuentes/)
03-paginas/es/ y en/          Una página por archivo, lista para pegar en Elementor
paginas-y-seo.csv             Slug, título SEO, meta descripción e imagen de cada página
textos-alternativos-imagenes.csv   Texto alternativo (ES y EN) de cada foto
llms.txt                      Resumen de la web para buscadores con IA (ChatGPT, Perplexity…)
robots-referencia.txt         robots.txt recomendado
sitemap-referencia.xml        Sitemap de referencia (en WordPress lo genera Yoast / Rank Math)
```

## Antes de empezar: plugins

- **Elementor** (con la plantilla *Elementor Canvas*).
- **Polylang** (o WPML) para el inglés. Idioma por defecto: español sin prefijo; inglés con `/en/`.
- **Yoast SEO** o **Rank Math** para títulos, descripciones, sitemap y hreflang.
- **WPCode** para cargar el CSS, el JS y la fuente de Adobe en toda la web.
- Más adelante (lo configuramos juntos): banner de cookies y Google Analytics 4.

## 1. Subir la mediateca

1. Sube **todo** el contenido de `01-mediateca/` a *Medios → Añadir nuevo*, todo en el mismo día para que quede en la misma carpeta de uploads.
2. WordPress no permite subir los dos `.svg` (los logos): sáltatelos, tienes las versiones en PNG, o instala *Safe SVG*.
3. Comprueba la URL de una imagen. Las páginas esperan `/wp-content/uploads/2026/10/`. Si tu WordPress usa otra carpeta (otro mes o sin carpetas por fecha), avísame y regenero las páginas con la ruta correcta en un segundo.
4. Copia los textos alternativos desde `textos-alternativos-imagenes.csv`. Las páginas ya llevan el alt en el HTML, pero así la mediateca queda ordenada.

## 2. Fuentes

Las tipografías de la marca (Federo y Archivo) se sirven desde el propio servidor: no se llama a Google, lo que es mejor para el RGPD y la velocidad.

- Sube la carpeta `02-estilos-y-script/canitas-fuentes/` por FTP o desde el administrador de archivos del hosting a `/wp-content/uploads/canitas-fuentes/`. WordPress no deja subir `.woff2` desde la mediateca.

**Custard Regular (Cañitas al Fresco):** se carga desde tu proyecto web de Adobe Fonts (`uuw0ivw`), que solo incluye Custard Regular. Las páginas ya vienen preparadas para él. En WPCode añade un fragmento HTML en el `<head>` de toda la web con:

```html
<link rel="stylesheet" href="https://use.typekit.net/uuw0ivw.css">
```

## 3. CSS y JS globales (WPCode)

1. *Code Snippets → Añadir → CSS*, pega `canitas.css`, ubicación «En toda la web».
2. *Code Snippets → Añadir → JavaScript*, pega `canitas.js`, ubicación «Pie de página, en toda la web».

## 4. Crear cada página

Para cada archivo de `03-paginas/`:

1. *Páginas → Añadir nueva*. Título = columna `titulo_pagina_wordpress` del CSV.
2. Slug = columna `slug`. Las páginas en inglés van como hijas de su idioma con Polylang (la URL debe quedar como en la columna `url`).
3. Plantilla: **Elementor Canvas** (sin cabecera ni pie del tema: la página ya trae los suyos).
4. Editar con Elementor → un contenedor a **ancho completo, sin relleno ni márgenes** → un widget **HTML** → pega el archivo entero.
5. En Yoast / Rank Math: título SEO y meta descripción del CSV; imagen para redes = columna `imagen_destacada_og`.
6. Las 4 páginas legales: marca *No indexar* (columna `indexar`).
7. Con Polylang, enlaza cada página en inglés con su traducción en español (columna `traduccion_de`).
8. Página de inicio: *Ajustes → Lectura → Página estática* = «Inicio» (ES) y su traducción «Home» (EN).

## 5. SEO al publicar

- Dominio: **https://canitasmalaga.com** (sin www). En *Ajustes → Generales* pon la misma dirección en «Dirección de WordPress» y «Dirección del sitio», y haz que `www.canitasmalaga.com` y `http://` redirijan a ella (lo suele hacer el hosting).

- Comprueba que Yoast / Rank Math genera `sitemap_index.xml` con hreflang (Polylang lo añade) y envíalo a **Google Search Console** y **Bing Webmaster Tools**.
- Sustituye el `robots.txt` por `robots-referencia.txt` (Yoast → Herramientas → Editor de archivos).
- Sube `llms.txt` a la raíz del dominio.
- **Perfil de Empresa en Google** (Google Business Profile): crea o reclama la ficha de Cañitas Málaga y otra para Cañitas al Fresco. Pon la misma dirección, teléfono y web que la página, el horario, fotos y el enlace a la carta y a las reservas. Para un restaurante es la palanca de SEO local más importante.
- Pasa la página de inicio y la de Cañitas Málaga por https://search.google.com/test/rich-results para validar los datos estructurados (Restaurant, BarOrPub, FAQ y migas de pan).

## Pendiente de datos

- **Datos de empresa** para los textos legales: razón social, NIF, domicilio, registro mercantil, email de privacidad y validez de los bonos. Están resaltados en amarillo en las páginas legales.
- **Horario** de cada espacio (para la web, los datos estructurados y Google Business Profile).
