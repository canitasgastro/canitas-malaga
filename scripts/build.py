"""Generador de la web de Cañitas Maite Restaurante (ES / EN).

  python3 scripts/build.py

Genera, sin dependencias externas:
  - La web estática completa (index.html, /en/, subpáginas, legales, 404,
    sitemap.xml, robots.txt, manifest) que se publica en GitHub Pages como vista previa.
  - wordpress/: la exportación para montar la web en WordPress + Elementor,
    página a página (ver wordpress/LEEME.md).

Todo el texto vive en scripts/pages.py, scripts/legal.py y scripts/menus_data.py.
"""
import csv
import html
import json
import os
import shutil
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import media  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
# Dominio definitivo de la web (WordPress). Cámbialo aquí y vuelve a generar.
SITE_URL = os.environ.get("CANITAS_SITE_URL", "https://canitasmalaga.com")
# Vista previa en GitHub Pages: se publica con noindex para no competir con la web real.
PREVIEW_URL = "https://canitasgastro.github.io/canitas-malaga"
# Ruta de la mediateca de WordPress donde quedarán las imágenes al subirlas.
WP_MEDIA = os.environ.get("CANITAS_WP_MEDIA", "/wp-content/uploads/2026/10/")
# Proyecto web de Adobe Fonts con la tipografía Custard (Cañitas al Fresco).
# Ejemplo: "abc1def". Mientras esté vacío se usa la tipografía de respaldo.
ADOBE_FONTS_KIT = os.environ.get("CANITAS_ADOBE_KIT", "uuw0ivw")

BOOKING = {
    "es": "https://www.covermanager.com/reservation/module_restaurant/canitas-maite-melia-me-malaga/spanish",
    "en": "https://www.covermanager.com/reservation/module_restaurant/canitas-maite-melia-me-malaga/english",
}
PHONE = "+34 682 10 89 03"
PHONE_TEL = "+34682108903"
EMAIL = "canitasmalaga@melia.com"
INSTAGRAM = "https://www.instagram.com/canitas_malaga/"
MAPS = "https://www.google.com/maps/search/?api=1&query=Hotel%20ME%20M%C3%A1laga%20by%20Meli%C3%A1%2C%20Calle%20Victoria%206%2C%2029012%20M%C3%A1laga"
GEO = (36.7230223, -4.4166819)
# Horarios (fuente: Google Maps, octubre 2026). Todos los días.
HOURS = {
    "maite": [("13:00", "15:30"), ("20:00", "22:30")],
    "fresco": [("11:00", "24:00")],
}


def hours_text(lang, key):
    if key == "maite":
        return ("Todos los días, de 13:00 a 15:30 y de 20:00 a 22:30" if lang == "es"
                else "Every day, 1–3:30 pm and 8–10:30 pm")
    return "Todos los días, de 11:00 a 24:00" if lang == "es" else "Every day, 11 am to midnight"


def hours_ld(key):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return [{"@type": "OpeningHoursSpecification", "dayOfWeek": days, "opens": a, "closes": "23:59" if b == "24:00" else b}
            for a, b in HOURS[key]]
HOTEL_URL = {
    "es": "https://www.melia.com/es/hoteles/espana/malaga/me-malaga",
    "en": "https://www.melia.com/en/hotels/spain/malaga/me-malaga",
}

# Rutas de cada página en los dos idiomas.
ROUTES = {
    "home": ("", "en/"),
    "maite": ("canitas-malaga/", "en/canitas-malaga/"),
    "fresco": ("canitas-al-fresco/", "en/canitas-al-fresco/"),
    "carta": ("carta/", "en/menu/"),
    "reservas": ("reservas/", "en/book-a-table/"),
    "grupos": ("grupos-y-eventos/", "en/groups-and-events/"),
    "bonos": ("bonos-regalo/", "en/gift-vouchers/"),
    "proyecto": ("el-proyecto/", "en/our-story/"),
    "contacto": ("contacto/", "en/contact/"),
    "faq": ("preguntas-frecuentes/", "en/faq/"),
    "desayunos": ("desayunos-brunch-malaga/", "en/breakfast-brunch-malaga/"),
    "eventos": ("eventos-empresa-malaga/", "en/corporate-events-malaga/"),
    # Subpáginas SEO de desayunos y eventos (fuera de la cabecera; enlazadas desde su página madre)
    "brunch": ("brunch-malaga/", "en/brunch-malaga/"),
    "desayunar": ("donde-desayunar-malaga-centro/", "en/breakfast-malaga-old-town/"),
    "hotelbreakfast": ("desayuno-hotel-malaga-sin-alojarse/", "en/hotel-breakfast-malaga-non-guests/"),
    "cenaempresa": ("cena-de-empresa-malaga/", "en/company-dinner-malaga/"),
    "navidad": ("cena-navidad-empresa-malaga/", "en/christmas-party-malaga/"),
    "rooftopeventos": ("rooftop-para-eventos-malaga/", "en/rooftop-event-venue-malaga/"),
    "reuniones": ("reuniones-coffee-break-malaga/", "en/meeting-venue-malaga/"),
    # Páginas de búsqueda local (fuera del menú, enlazadas desde el pie)
    "centro": ("restaurante-centro-malaga/", "en/restaurant-malaga-old-town/"),
    "donde": ("donde-comer-en-malaga/", "en/where-to-eat-in-malaga/"),
    "cenar": ("donde-cenar-en-malaga/", "en/dinner-in-malaga/"),
    "vistas": ("restaurante-con-vistas-malaga/", "en/restaurant-with-a-view-malaga/"),
    "rooftop": ("rooftop-malaga/", "en/rooftop-bar-malaga/"),
    "aviso": ("aviso-legal/", "en/legal-notice/"),
    "privacidad": ("politica-de-privacidad/", "en/privacy-policy/"),
    "cookies": ("politica-de-cookies/", "en/cookie-policy/"),
    "condiciones": ("condiciones-de-compra/", "en/terms-of-purchase/"),
}
LEGAL_KEYS = ("aviso", "privacidad", "cookies", "condiciones")


esc = html.escape


def jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        seg = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg
    return None


class Ctx:
    """Contexto de una página: idioma, modo (web estática o WordPress) y ruta."""

    def __init__(self, lang, mode, key):
        self.lang = lang
        self.mode = mode  # "static" | "wp"
        self.key = key
        self.path = ROUTES[key][0 if lang == "es" else 1]
        self.depth = self.path.count("/")

    # Texto según idioma
    def t(self, es, en):
        return es if self.lang == "es" else en

    @property
    def other(self):
        return "en" if self.lang == "es" else "es"

    # URLs
    def _root(self):
        if self.mode == "wp":
            return "/"
        return "../" * self.depth if self.depth else "./"

    def link(self, key, lang=None, anchor=""):
        lang = lang or self.lang
        target = ROUTES[key][0 if lang == "es" else 1]
        url = self._root() + target
        if self.mode == "static" and url == "./" and anchor:
            url = ""
        return url + (f"#{anchor}" if anchor else "")

    def asset(self, rel):
        if self.mode == "wp":
            return WP_MEDIA + os.path.basename(rel)
        return self._root() + "assets/" + rel

    def abs_url(self, key, lang=None):
        lang = lang or self.lang
        base = SITE_URL if self.mode == "wp" else PREVIEW_URL
        return base + "/" + ROUTES[key][0 if lang == "es" else 1]

    def abs_asset(self, rel):
        if self.mode == "wp":
            return SITE_URL + WP_MEDIA + os.path.basename(rel)
        return PREVIEW_URL + "/assets/" + rel

    def img(self, name, cls="", sizes="100vw", loading="lazy", alt=None, extra=""):
        info = media.PHOTOS[name]
        alt = alt if alt is not None else info[self.lang]
        size = jpeg_size(os.path.join(BASE, "assets", "img", f"{name}.jpg")) or (1600, 1067)
        attrs = [f'src="{self.asset("img/" + name + ".jpg")}"']
        if self.mode == "static" and os.path.exists(os.path.join(BASE, "assets", "img", f"{name}-800.jpg")):
            attrs.append(f'srcset="{self.asset("img/" + name + "-800.jpg")} 800w, {self.asset("img/" + name + ".jpg")} {size[0]}w"')
            attrs.append(f'sizes="{sizes}"')
        attrs.append(f'width="{size[0]}" height="{size[1]}"')
        attrs.append(f'alt="{esc(alt)}"')
        if loading == "eager":
            attrs.append('loading="eager" fetchpriority="high"')
        else:
            attrs.append('loading="lazy" decoding="async"')
        if cls:
            attrs.insert(0, f'class="{cls}"')
        if extra:
            attrs.append(extra)
        return "<img " + " ".join(attrs) + ">"


# ---------------------------------------------------------------------------
# Componentes compartidos
# ---------------------------------------------------------------------------
LOGO_PATHS = {}


def _logo(file, cls, label, viewbox):
    if file not in LOGO_PATHS:
        import re
        svg = open(os.path.join(BASE, "assets", "logos", file), encoding="utf-8").read()
        g = svg[svg.index("<g"):svg.rindex("</g>") + 4].replace("#28265a", "currentColor")
        LOGO_PATHS[file] = re.sub(r"\s*\n\s*", " ", g)
    aria = f'role="img" aria-label="{esc(label)}"' if label else 'aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="{viewbox}" fill="currentColor" {aria}>{LOGO_PATHS[file]}</svg>'


def logo_svg(cls, label=None):
    """Logo de Cañitas Málaga (el de la cabecera y el pie)."""
    return _logo("logo-canitas-malaga.svg", cls, label, "0 0 656.46 231.7")


def maite_logo_svg(cls, label=None):
    """Logo de Cañitas Maite («desde 1958»): el del restaurante."""
    return _logo("logo-canitas-maite.svg", cls, label, "0 0 3370.38 1280.46")


MENU_ANCHOR = {"maite": "canitas-malaga", "fresco": "canitas-al-fresco"}


def menu_lang(c, space, light=False):
    """Botones para ver la carta web en español o en inglés."""
    cls = "menu-lang menu-lang-light" if light else "menu-lang"
    anchor = MENU_ANCHOR[space]

    def a(lang, label):
        current = ' aria-current="true"' if lang == c.lang else ""
        return f'<a href="{c.link("carta", lang, anchor)}" hreflang="{lang}" lang="{lang}"{current}>{label}</a>'
    return (
        f'<div class="{cls}" role="group" aria-label="{c.t("Ver la carta en otro idioma", "See the menu in another language")}">'
        f'<span class="menu-lang-label">{c.t("Carta", "Menu")}</span>'
        f'{a("es", "Español")}{a("en", "English")}'
        f"</div>"
    )

def header(c):
    t = c.t
    nav = [
        ("maite", "Cañitas Maite Restaurante", "Cañitas Maite Restaurante"),
        ("fresco", "Al Fresco Rooftop", "Al Fresco Rooftop"),
        ("desayunos", "Desayunos", "Breakfast"),
        ("eventos", "Eventos", "Events"),
    ]
    pill = "\n".join(
        f'      <a href="{c.link(k)}"{" aria-current=\"page\"" if k == c.key else ""}>{t(es, en)}</a>' for k, es, en in nav
    )
    groups = [
        (t("Espacios", "Venues"), [
            ("maite", "Cañitas Maite Restaurante", "Cañitas Maite Restaurante"),
            ("fresco", "Cañitas al Fresco Rooftop", "Cañitas al Fresco Rooftop"),
            ("desayunos", "Desayunos y brunch", "Breakfast & brunch"),
            ("eventos", "Eventos de empresa", "Corporate events"),
        ]),
        (t("Reservas y cartas", "Bookings & menus"), [
            ("reservas", "Reservar mesa", "Book a table"),
            ("carta", "La carta y los menús", "Menus"),
            ("grupos", "Grupos de 8 o más", "Groups of 8 or more"),
        ]),
        (t("La casa", "About us"), [
            ("proyecto", "El proyecto", "Our story"),
            ("bonos", "Bonos regalo", "Gift vouchers"),
            ("faq", "Preguntas frecuentes", "FAQ"),
            ("contacto", "Contacto y cómo llegar", "Contact & directions"),
        ]),
    ]
    menu = "\n".join(
        f'        <div class="site-menu-group">\n          <p class="site-menu-title">{title}</p>\n          <ul>\n'
        + "\n".join(f'            <li><a href="{c.link(k)}"{" aria-current=\"page\"" if k == c.key else ""}>{t(es, en)}</a></li>' for k, es, en in items)
        + "\n          </ul>\n        </div>"
        for title, items in groups
    )
    other_label = "English" if c.lang == "es" else "Español"
    other_short = "EN" if c.lang == "es" else "ES"
    switch_title = t("Read this page in English", "Ver esta página en español")
    return f"""<header class="site-header" id="site-header">
  <div class="header-pill">
    <a href="{c.link('home')}" class="logo" aria-label="{t('Cañitas Málaga — Inicio', 'Cañitas Málaga — Home')}">
      {logo_svg("logo-mark")}
    </a>

    <nav class="pill-nav" aria-label="{t('Secciones', 'Sections')}">
{pill}
    </nav>

    <div class="header-actions">
      <a class="lang-switch" href="{c.link(c.key, c.other)}" hreflang="{c.other}" lang="{c.other}" title="{switch_title}">{other_short}</a>
      <a class="btn btn-primary-light btn-small btn-pill" href="{c.link('reservas')}">{t('Reservar mesa', 'Book a table')}</a>
      <button class="menu-toggle" id="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="{t('Abrir menú', 'Open menu')}">
        <span class="menu-icon" aria-hidden="true"><span></span><span></span><span></span></span>
      </button>
    </div>

    <nav class="site-menu" id="site-menu" aria-label="{t('Menú principal', 'Main menu')}" data-open="false">
      <div class="site-menu-groups">
{menu}
      </div>
      <div class="site-menu-foot">
        <a class="btn btn-primary-light btn-small btn-pill" href="{c.link('reservas')}">{t('Reservar mesa', 'Book a table')}</a>
        <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram ↗</a>
        <a href="{c.link(c.key, c.other)}" hreflang="{c.other}" lang="{c.other}">{other_label}</a>
      </div>
    </nav>
  </div>
</header>"""


def contact_section(c, heading_level=2, with_id=True):
    t = c.t
    h = f"h{heading_level}"
    distances = [
        ("Plaza de la Merced", t("1 min a pie", "1 min walk")),
        (t("Alcazaba", "Alcazaba"), t("3 min a pie", "3 min walk")),
        (t("Museo Picasso Málaga", "Picasso Museum Málaga"), t("3 min a pie", "3 min walk")),
        (t("Catedral de Málaga", "Málaga Cathedral"), t("5 min a pie", "5 min walk")),
    ]
    dist = "\n".join(f"          <li><span>{a}</span><em>{b}</em></li>" for a, b in distances)
    sec_id = ' id="contacto"' if with_id else ""
    return f"""  <section class="contact"{sec_id} aria-label="{t('Contacto y cómo llegar', 'Contact and directions')}">
    <div class="section-inner contact-grid">
      <div class="contact-info">
        <p class="eyebrow">{t('Contacto', 'Contact')}</p>
        <{h} class="section-title-light">{t('Te esperamos en el centro de Málaga', 'See you in the heart of Málaga')}</{h}>

        <address>
          <p>Hotel ME Málaga by Meliá<br>Calle Victoria, 6 · 29012 Málaga<br>{t('Distrito Centro, junto a la Plaza de la Merced', 'City centre, next to Plaza de la Merced')}</p>
        </address>

        <dl class="contact-hours">
          <div><dt>Cañitas Maite Restaurante</dt><dd>{hours_text(c.lang, "maite")}</dd></div>
          <div><dt>Cañitas al Fresco</dt><dd>{hours_text(c.lang, "fresco")}</dd></div>
        </dl>

        <ul class="contact-lines">
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">@canitas_malaga</a></li>
        </ul>

        <div class="contact-actions">
          <a class="btn btn-primary-light" href="{c.link('reservas')}">{t('Reservar mesa', 'Book a table')}</a>
          <a class="btn btn-ghost-light" href="{MAPS}" target="_blank" rel="noopener">{t('Cómo llegar', 'Get directions')} ↗</a>
        </div>
      </div>

      <div class="contact-map-wrap">
        <figure class="map-card">
          <a class="map-card-link" href="{MAPS}" target="_blank" rel="noopener" aria-label="{t('Abrir la ubicación de Cañitas Maite Restaurante en Google Maps', 'Open Cañitas Maite Restaurante location in Google Maps')}">
            {c.img("mapa-canitas-malaga-calle-victoria", sizes="(max-width: 860px) 90vw, 460px")}
            <span class="map-card-pin" aria-hidden="true">Cañitas Maite Restaurante · ME Málaga</span>
            <span class="map-card-cta" aria-hidden="true">{t('Abrir en Google Maps', 'Open in Google Maps')} ↗</span>
          </a>
          <figcaption>© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors</figcaption>
        </figure>
        <ul class="distances">
{dist}
        </ul>
      </div>
    </div>
  </section>"""


def footer(c):
    t = c.t
    legal = [
        ("aviso", "Aviso legal", "Legal notice"),
        ("privacidad", "Privacidad", "Privacy"),
        ("cookies", "Cookies", "Cookies"),
        ("condiciones", "Condiciones de compra", "Terms of purchase"),
    ]
    legal_links = "\n".join(f'        <a href="{c.link(k)}">{t(es, en)}</a>' for k, es, en in legal)
    from landings import LABELS
    seo_links = "\n".join(f'    <a href="{c.link(k)}">{t(es, en)}</a>' for k, es, en in LABELS)
    return f"""<footer class="site-footer">
  <div class="footer-top">
    <div class="footer-brand">
      <a href="{c.link('home')}" class="logo logo-footer" aria-label="{t('Cañitas Málaga — Inicio', 'Cañitas Málaga — Home')}">
        {logo_svg("logo-mark logo-mark-footer")}
      </a>
      <p class="footer-tagline">{t('Un lugar donde el arte, la cultura, la gastronomía y la música se funden con el espíritu del sur.', 'A place where art, culture, food and music blend with the spirit of the south.')}</p>
      <p class="footer-address">Hotel ME Málaga by Meliá · Calle Victoria, 6 · 29012 Málaga<br><a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>

    <div class="footer-col">
      <h2 class="footer-col-title">{t('Espacios', 'Venues')}</h2>
      <a href="{c.link('maite')}">Cañitas Maite Restaurante</a>
      <a href="{c.link('fresco')}">Cañitas al Fresco Rooftop</a>
      <a href="{c.link('desayunos')}">{t('Desayunos y brunch', 'Breakfast & brunch')}</a>
      <a href="{c.link('eventos')}">{t('Eventos de empresa', 'Corporate events')}</a>
      <a href="{c.link('carta')}">{t('La carta', 'The menu')}</a>
    </div>

    <div class="footer-col">
      <h2 class="footer-col-title">{t('Información', 'Information')}</h2>
      <a href="{c.link('proyecto')}">{t('El proyecto', 'Our story')}</a>
      <a href="{c.link('grupos')}">{t('Grupos de 8 o más', 'Groups of 8 or more')}</a>
      <a href="{c.link('bonos')}">{t('Bonos regalo', 'Gift vouchers')}</a>
      <a href="{c.link('faq')}">{t('Preguntas frecuentes', 'FAQ')}</a>
      <a href="{c.link('contacto')}">{t('Contacto y cómo llegar', 'Contact & directions')}</a>
    </div>

    <div class="footer-col">
      <h2 class="footer-col-title">{t('Síguenos', 'Follow us')}</h2>
      <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a>
      <a href="{c.link(c.key, c.other)}" hreflang="{c.other}" lang="{c.other}">{'English version' if c.lang == 'es' else 'Versión en español'}</a>
      <a href="{c.link('reservas')}" class="footer-cta">{t('Reservar mesa', 'Book a table')} →</a>
    </div>
  </div>

  <nav class="footer-seo" aria-label="{t('Comer en Málaga', 'Eating in Málaga')}">
    <span class="footer-col-title">{t('Comer en Málaga', 'Eating in Málaga')}</span>
{seo_links}
  </nav>

  <div class="footer-bottom">
    <div class="footer-bottom-inner">
      <p class="footer-legal">© 2026 Cañitas Maite Restaurante · ME Málaga by Meliá</p>
      <nav class="footer-legal-links" aria-label="{t('Información legal', 'Legal information')}">
{legal_links}
      </nav>
    </div>
  </div>
</footer>"""


def page_hero(c, eyebrow, title, lead, photo=None, actions="", crumbs=None, extra_cls=""):
    t = c.t
    crumb_html = ""
    if crumbs is not None:
        items = [f'<li><a href="{c.link("home")}">{t("Inicio", "Home")}</a></li>'] + [
            f'<li aria-current="page">{esc(x)}</li>' for x in crumbs
        ]
        crumb_html = f'<nav class="breadcrumbs" aria-label="{t("Migas de pan", "Breadcrumb")}"><ol>{"".join(items)}</ol></nav>'
    img = c.img(photo, cls="page-hero-photo", loading="eager") if photo else ""
    cls = "page-hero" + (" page-hero-photo-on" if photo else "") + (f" {extra_cls}" if extra_cls else "")
    return f"""  <section class="{cls}">
    {img}
    <div class="page-hero-inner">
      {crumb_html}
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="page-title">{title}</h1>
      <p class="page-lead">{lead}</p>
      {f'<div class="page-hero-actions">{actions}</div>' if actions else ''}
    </div>
  </section>"""


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def breadcrumb_ld(c, name):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": c.t("Inicio", "Home"), "item": c.abs_url("home")},
            {"@type": "ListItem", "position": 2, "name": name, "item": c.abs_url(c.key)},
        ],
    }


def address_ld():
    return {
        "@type": "PostalAddress",
        "streetAddress": "Calle Victoria, 6",
        "addressLocality": "Málaga",
        "addressRegion": "Málaga",
        "postalCode": "29012",
        "addressCountry": "ES",
    }


def restaurant_ld(c):
    return {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "@id": c.abs_url("maite", "es") + "#restaurant",
        "name": "Cañitas Maite Restaurante",
        "alternateName": ["Cañitas Maite Málaga", "Cañitas Maite Restaurante - Málaga", "Cañitas Málaga"],
        "description": c.t(
            "Restaurante de los chefs Javier Sanz y Juan Sahuquillo en la última planta del hotel ME Málaga by Meliá, en el centro de Málaga: cocina de producto, parrilla y brasa, terraza acristalada y comedor privado.",
            "Restaurant by chefs Javier Sanz and Juan Sahuquillo on the top floor of ME Málaga by Meliá, in Málaga city centre: produce-led cooking, grill and embers, a glass-roofed terrace and a private dining room.",
        ),
        "url": c.abs_url("maite"),
        "image": [c.abs_asset("img/canitas-malaga-sala-restaurante.jpg"), c.abs_asset("img/canitas-malaga-comedor-privado.jpg"), c.abs_asset("img/txuleta-vasca-parrilla-canitas-malaga.jpg")],
        "telephone": PHONE,
        "email": EMAIL,
        "address": address_ld(),
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "hasMap": MAPS,
        "servesCuisine": c.t(["Española", "Manchega", "Mediterránea", "Parrilla"], ["Spanish", "Manchego", "Mediterranean", "Grill"]),
        "priceRange": "€€€",
        "openingHoursSpecification": hours_ld("maite"),
        "acceptsReservations": c.abs_url("reservas"),
        "hasMenu": c.abs_url("carta"),
        "sameAs": [
            INSTAGRAM,
            "https://www.melia.com/es/hoteles/espana/malaga/me-malaga/restaurantes/canitas-maite",
            "https://www.tripadvisor.es/Restaurant_Review-g187438-d34364926-Reviews-Canitas_Maite-Malaga_Costa_del_Sol_Province_of_Malaga_Andalucia.html",
        ],
        "inLanguage": c.lang,
        "containedInPlace": {"@type": "Hotel", "name": "ME Málaga by Meliá", "url": HOTEL_URL[c.lang], "address": address_ld()},
    }


def fresco_ld(c):
    return {
        "@context": "https://schema.org",
        "@type": "BarOrPub",
        "@id": c.abs_url("fresco", "es") + "#bar",
        "name": "Cañitas al Fresco",
        "description": c.t(
            "Rooftop bar abierto al público en la azotea del hotel ME Málaga by Meliá, con vistas a la Alcazaba. Coctelería y picoteo de Cañitas Maite Restaurante. Sin reserva.",
            "Rooftop bar open to the public on top of ME Málaga by Meliá, with views of the Alcazaba. Cocktails and sharing plates by Cañitas Maite Restaurante. No reservations.",
        ),
        "url": c.abs_url("fresco"),
        "image": [c.abs_asset("img/canitas-al-fresco-rooftop-piscina-malaga.jpg")],
        "telephone": PHONE,
        "address": address_ld(),
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "hasMap": MAPS,
        "servesCuisine": c.t(["Tapas", "Mediterránea"], ["Tapas", "Mediterranean"]),
        "priceRange": "€€",
        "openingHoursSpecification": hours_ld("fresco"),
        "acceptsReservations": False,
        "hasMenu": c.abs_url("carta") + "#canitas-al-fresco",
        "sameAs": [INSTAGRAM],
        "inLanguage": c.lang,
        "containedInPlace": {"@type": "Hotel", "name": "ME Málaga by Meliá", "url": HOTEL_URL[c.lang], "address": address_ld()},
    }


# ---------------------------------------------------------------------------
# Documento completo
# ---------------------------------------------------------------------------
def head(c, page):
    t = c.t
    canonical = c.abs_url(c.key)
    alt_es = c.abs_url(c.key, "es")
    alt_en = c.abs_url(c.key, "en")
    og_img = c.abs_asset("img/" + page.get("og", "og-canitas-malaga") + ".jpg")
    robots = "noindex, nofollow" if c.mode == "static" else ("noindex, follow" if c.key in LEGAL_KEYS else "index, follow")
    adobe = f'\n<link rel="preconnect" href="https://use.typekit.net" crossorigin>\n<link rel="stylesheet" href="https://use.typekit.net/{ADOBE_FONTS_KIT}.css">' if ADOBE_FONTS_KIT else ""
    root = c._root()
    return f"""<!doctype html>
<html lang="{c.lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['desc'])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="es" href="{alt_es}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_es}">
<meta property="og:type" content="{'website' if c.key == 'home' else 'article'}">
<meta property="og:site_name" content="Cañitas Maite Restaurante">
<meta property="og:locale" content="{t('es_ES', 'en_GB')}">
<meta property="og:locale:alternate" content="{t('en_GB', 'es_ES')}">
<meta property="og:title" content="{esc(page.get('og_title', page['title']))}">
<meta property="og:description" content="{esc(page['desc'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#28265a">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{root}assets/icons/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{root}assets/icons/apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="preload" href="{root}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/federo-latin.woff2" as="font" type="font/woff2" crossorigin>{adobe}
<link rel="stylesheet" href="{root}css/styles.css">
</head>"""


def body(c, page):
    t = c.t
    schemas = "\n".join(ld(s) for s in page.get("schema", []))
    contact = ("\n\n" + contact_section(c)) if page.get("contact", True) else ""
    wrap_cls = "site" + (f" {page['theme']}" if page.get("theme") else "")
    if ADOBE_FONTS_KIT:
        wrap_cls += " fonts-custard"
    script = f'<script src="{c._root()}js/main.js" defer></script>' if c.mode == "static" else ""
    return f"""<div class="{wrap_cls}">
<a class="skip-link" href="#contenido">{t('Saltar al contenido', 'Skip to content')}</a>

{header(c)}

<main id="contenido">
{page['main']}{contact}
</main>

{footer(c)}
</div>
{schemas}
{script}"""


def render_static(c, page):
    return head(c, page) + "\n<body>\n" + body(c, page) + "\n</body>\n</html>\n"


def render_wp(c, page):
    note = f"<!-- Cañitas Maite Restaurante · {page['title']} · Pegar completo en un widget HTML de Elementor (plantilla Elementor Canvas). -->\n"
    return note + body(c, page) + "\n"


# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    import experiences
    import faq
    import landings
    import legal
    import pages

    builders = dict(pages.PAGES)
    builders.update(legal.PAGES)
    builders.update(landings.PAGES)
    builders.update(faq.PAGES)
    builders.update(experiences.PAGES)
    import seo_pages
    builders.update(seo_pages.PAGES)

    generated = []
    wp_rows = []
    seo_map = {}
    manifest = []
    for key in ROUTES:
        for lang in ("es", "en"):
            # Web estática (vista previa)
            c = Ctx(lang, "static", key)
            page = builders[key](c)
            write(os.path.join(BASE, c.path, "index.html"), render_static(c, page))
            generated.append((key, lang, c.path))

            # WordPress
            w = Ctx(lang, "wp", key)
            wpage = builders[key](w)
            slug = (c.path.rstrip("/").split("/")[-1] if c.path.strip("/") not in ("", "en") else ("inicio" if lang == "es" else "home"))
            fname = f"{lang}/{slug}.html"
            write(os.path.join(BASE, "wordpress", "03-paginas", fname), render_wp(w, wpage))
            seo_map["/" + c.path] = {
                "title": wpage["title"], "desc": wpage["desc"], "lang": lang,
                "canonical": SITE_URL + "/" + c.path,
                "es": SITE_URL + "/" + ROUTES[key][0], "en": SITE_URL + "/" + ROUTES[key][1],
                "og": SITE_URL + WP_MEDIA + wpage.get("og", "og-canitas-malaga") + ".jpg",
                "type": "website" if key == "home" else "article",
                "noindex": key in LEGAL_KEYS,
            }
            manifest.append({
                "key": key, "lang": lang, "path": "/" + c.path,
                "slug": (("inicio" if lang == "es" else "en") if key == "home" else c.path.rstrip("/").split("/")[-1]),
                "parent": "en" if (lang == "en" and key != "home") else "",
                "title": wpage["nav_title"] + ("" if lang == "es" or key == "home" else " (EN)"),
                "file": os.path.join(BASE, "wordpress", "03-paginas", fname),
            })
            wp_rows.append({
                "idioma": lang.upper(),
                "archivo": "03-paginas/" + fname,
                "url": "/" + c.path,
                "slug": slug if key != "home" else "(página de inicio)",
                "pagina_madre": "en" if (lang == "en" and key != "home") else "",
                "titulo_pagina_wordpress": wpage["nav_title"],
                "titulo_seo": wpage["title"],
                "meta_descripcion": wpage["desc"],
                "imagen_destacada_og": wpage.get("og", "og-canitas-malaga") + ".jpg",
                "traduccion_de": "/" + ROUTES[key][0] if lang == "en" else "",
                "indexar": "no (legal)" if key in LEGAL_KEYS else "sí",
            })

    # 404 y redirección de la antigua reservas.html
    c = Ctx("es", "static", "home")
    write(os.path.join(BASE, "404.html"), pages.page_404())
    # Página del QR de bebidas de Al Fresco
    write(os.path.join(BASE, "bebidas-al-fresco", "index.html"), pages.drinks_static())
    write(os.path.join(BASE, "wordpress", "03-paginas", "es", "bebidas-al-fresco.html"),
          "<!-- Cañitas al Fresco · Carta de bebidas (QR). Widget HTML de Elementor, plantilla Elementor Canvas. Sin indexar. -->\n"
          + pages.drinks_body(lambda rel: WP_MEDIA + os.path.basename(rel), lambda p: "/" + p) + "\n")
    write(os.path.join(BASE, "reservas.html"), pages.redirect_page("reservas/"))
    # Antiguas URLs de la vista previa (el restaurante se llamaba Cañitas Maite)
    for old, new in (("canitas-maite/", "canitas-malaga/"), ("en/canitas-maite/", "en/canitas-malaga/")):
        rel = "../" * old.count("/") + new
        write(os.path.join(BASE, old, "index.html"),
              f'<!doctype html><html lang="es"><head><meta charset="UTF-8"><meta name="robots" content="noindex">'
              f'<link rel="canonical" href="{PREVIEW_URL}/{new}"><meta http-equiv="refresh" content="0; url={rel}">'
              f'<title>Cañitas Maite Restaurante</title></head><body><a href="{rel}">Cañitas Maite Restaurante</a></body></html>\n')

    # sitemap, robots, manifest (vista previa)
    write(os.path.join(BASE, "robots.txt"), "# Vista previa en GitHub Pages: no indexar.\nUser-agent: *\nDisallow: /\n")
    write(os.path.join(BASE, "sitemap.xml"), sitemap(PREVIEW_URL))
    write(os.path.join(BASE, "site.webmanifest"), json.dumps({
        "name": "Cañitas Maite Restaurante",
        "short_name": "Cañitas Maite Restaurante",
        "start_url": "./",
        "display": "browser",
        "background_color": "#ffffff",
        "theme_color": "#28265a",
        "icons": [
            {"src": "assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, ensure_ascii=False, indent=2))

    export_wordpress(wp_rows)
    write(os.path.join(BASE, "wordpress", "02-estilos-y-script", "canitas-seo.php"), seo_php(seo_map))
    write(os.path.join(BASE, "wordpress", "paginas.json"), json.dumps(manifest, ensure_ascii=False, indent=1))
    print(f"{len(generated)} páginas generadas + exportación WordPress ({len(wp_rows)} páginas).")


def sitemap(base):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key, (es, en) in ROUTES.items():
        if key in LEGAL_KEYS:
            continue
        for path in (es, en):
            out.append("  <url>")
            out.append(f"    <loc>{base}/{path}</loc>")
            out.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{base}/{es}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{base}/{en}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{base}/{es}"/>')
            out.append("    <lastmod>2026-10-15</lastmod>")
            out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def export_wordpress(rows):
    wp = os.path.join(BASE, "wordpress")
    # Estilos y script globales
    css = open(os.path.join(BASE, "css", "styles.css"), encoding="utf-8").read()
    css = css.replace("../assets/fonts/", WP_MEDIA)
    write(os.path.join(wp, "02-estilos-y-script", "canitas.css"), css)
    shutil.copy(os.path.join(BASE, "js", "main.js"), os.path.join(wp, "02-estilos-y-script", "canitas.js"))
    fonts_dst = os.path.join(wp, "02-estilos-y-script", "canitas-fuentes")
    os.makedirs(fonts_dst, exist_ok=True)
    for f in os.listdir(os.path.join(BASE, "assets", "fonts")):
        shutil.copy(os.path.join(BASE, "assets", "fonts", f), fonts_dst)

    with open(os.path.join(wp, "paginas-y-seo.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(wp, "textos-alternativos-imagenes.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["archivo", "titulo", "texto_alternativo_es", "texto_alternativo_en"])
        for name, info in media.PHOTOS.items():
            w.writerow([f"{name}.jpg", name.replace("-", " ").capitalize(), info["es"], info["en"]])
        w.writerow(["og-canitas-malaga.jpg", "Cañitas Maite Restaurante", "Sala del restaurante Cañitas Maite con el logotipo", "Cañitas Maite Restaurante dining room with the logo"])
        w.writerow(["og-canitas-al-fresco.jpg", "Cañitas al Fresco", "Rooftop Cañitas al Fresco con la Alcazaba y el logotipo", "Cañitas al Fresco rooftop with the Alcazaba and the logo"])

    write(os.path.join(wp, "sitemap-referencia.xml"), sitemap(SITE_URL))
    write(os.path.join(wp, "robots-referencia.txt"), robots_txt(SITE_URL))
    write(os.path.join(wp, "llms.txt"), llms_txt(SITE_URL))
    write(os.path.join(wp, "llms-full.txt"), llms_full_txt(SITE_URL))


def seo_php(seo_map):
    """Fragmento PHP para WPCode: SEO de cada página (título, descripción, canonical,
    hreflang, Open Graph, robots), idioma del documento, sitemap, llms.txt, llms-full.txt,
    robots.txt para buscadores con IA, IndexNow y woff2.
    Los datos van en base64 para no depender de comillas ni heredocs."""
    import base64
    data = base64.b64encode(json.dumps(seo_map, ensure_ascii=False).encode("utf-8")).decode("ascii")
    llms = base64.b64encode(llms_txt(SITE_URL).encode("utf-8")).decode("ascii")
    php = r"""// Cañitas Maite Restaurante · SEO de las páginas (generado por scripts/build.py; no editar a mano)
$GLOBALS['canitas_seo'] = json_decode(base64_decode('__DATA__'), true);

if (!function_exists('canitas_seo_current')) {
function canitas_seo_current() {
    $uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/';
    $path = '/' . trim((string) wp_parse_url($uri, PHP_URL_PATH), '/') . '/';
    if ($path === '//') {
        $path = '/';
    }
    return isset($GLOBALS['canitas_seo'][$path]) ? $GLOBALS['canitas_seo'][$path] : null;
}
}

// Con Yoast SEO activo, Yoast gestiona título, descripción, canonical, Open Graph,
// robots y sitemap; este fragmento añade solo hreflang, idioma, llms.txt y fuentes.
if (!function_exists('canitas_yoast')) {
    function canitas_yoast() {
        return defined('WPSEO_VERSION');
    }
}

add_filter('pre_get_document_title', function ($title) {
    $s = canitas_seo_current();
    return ($s && !canitas_yoast()) ? $s['title'] : $title;
}, 99);

add_filter('language_attributes', function ($output) {
    $s = canitas_seo_current();
    return ($s && $s['lang'] === 'en') ? 'lang="en-GB"' : $output;
});

add_filter('wp_robots', function ($robots) {
    $s = canitas_seo_current();
    if ($s && $s['noindex'] && !canitas_yoast()) {
        return array('noindex' => true, 'follow' => true);
    }
    return $robots;
});

add_filter('jetpack_enable_open_graph', '__return_false');
add_filter('wpseo_locale', function ($locale) {
    $s = canitas_seo_current();
    return ($s && $s['lang'] === 'en') ? 'en_GB' : $locale;
});
add_action('wp', function () {
    if (!canitas_yoast()) {
        remove_action('wp_head', 'rel_canonical');
    }
});

add_action('wp_head', function () {
    $s = canitas_seo_current();
    if (!$s) {
        return;
    }
    $en = ($s['lang'] === 'en');
    $tags = array(
        array('meta', 'name', 'description', $s['desc']),
        array('link', 'canonical', '', $s['canonical']),
        array('alt', 'es', '', $s['es']),
        array('alt', 'en', '', $s['en']),
        array('alt', 'x-default', '', $s['es']),
        array('meta', 'property', 'og:type', $s['type']),
        array('meta', 'property', 'og:site_name', 'Cañitas Maite Restaurante'),
        array('meta', 'property', 'og:locale', $en ? 'en_GB' : 'es_ES'),
        array('meta', 'property', 'og:locale:alternate', $en ? 'es_ES' : 'en_GB'),
        array('meta', 'property', 'og:title', $s['title']),
        array('meta', 'property', 'og:description', $s['desc']),
        array('meta', 'property', 'og:url', $s['canonical']),
        array('meta', 'property', 'og:image', $s['og']),
        array('meta', 'property', 'og:image:width', '1200'),
        array('meta', 'property', 'og:image:height', '630'),
        array('meta', 'name', 'twitter:card', 'summary_large_image'),
        array('meta', 'name', 'theme-color', '#28265a'),
    );
    foreach ($tags as $t) {
        if (canitas_yoast() && $t[0] !== 'alt') {
            continue;
        }
        if ($t[0] === 'meta') {
            echo '<meta ' . $t[1] . '="' . esc_attr($t[2]) . '" content="' . esc_attr($t[3]) . '">' . "
";
        } elseif ($t[0] === 'link') {
            echo '<link rel="canonical" href="' . esc_url($t[3]) . '">' . "
";
        } else {
            echo '<link rel="alternate" hreflang="' . esc_attr($t[1]) . '" href="' . esc_url($t[3]) . '">' . "
";
        }
    }
}, 1);

// Sitemap de WordPress: solo páginas, sin usuarios ni taxonomías y sin las legales
add_filter('wp_sitemaps_add_provider', function ($provider, $name) {
    return in_array($name, array('users', 'taxonomies'), true) ? false : $provider;
}, 10, 2);
add_filter('wp_sitemaps_post_types', function ($types) {
    return array_intersect_key($types, array('page' => true));
});
add_filter('wp_sitemaps_posts_query_args', function ($args) {
    $ids = array();
    foreach ($GLOBALS['canitas_seo'] as $path => $s) {
        if ($s['noindex']) {
            $p = get_page_by_path(trim($path, '/'));
            if ($p) {
                $ids[] = $p->ID;
            }
        }
    }
    $args['post__not_in'] = array_merge(isset($args['post__not_in']) ? $args['post__not_in'] : array(), $ids);
    return $args;
});

// llms.txt, llms-full.txt (buscadores con IA) y clave de IndexNow en la raíz del dominio
add_action('init', function () {
    $uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';
    $files = array(
        '/llms.txt' => '__LLMS__',
        '/llms-full.txt' => '__LLMSFULL__',
        '/__INDEXNOW__.txt' => '__INDEXNOW_B64__',
    );
    $path = wp_parse_url($uri, PHP_URL_PATH);
    if (isset($files[$path])) {
        header('Content-Type: text/plain; charset=utf-8');
        header('X-Robots-Tag: noindex');
        echo base64_decode($files[$path]);
        exit;
    }
});

// robots.txt: paso explícito a los rastreadores de buscadores con IA
add_filter('robots_txt', function ($output, $public) {
    if (!$public) {
        return $output;
    }
    return base64_decode('__ROBOTS__');
}, 99, 2);

// IndexNow: avisa a Bing (y con él a Copilot y ChatGPT search) cada vez que se publica o actualiza una página
add_action('transition_post_status', function ($new, $old, $post) {
    if ($new !== 'publish' || $post->post_type !== 'page' || wp_is_post_revision($post)) {
        return;
    }
    wp_remote_post('https://api.indexnow.org/indexnow', array(
        'blocking' => false,
        'timeout' => 3,
        'headers' => array('Content-Type' => 'application/json; charset=utf-8'),
        'body' => wp_json_encode(array(
            'host' => wp_parse_url(home_url(), PHP_URL_HOST),
            'key' => '__INDEXNOW__',
            'keyLocation' => home_url('/__INDEXNOW__.txt'),
            'urlList' => array(get_permalink($post)),
        )),
    ));
}, 10, 3);

// Permitir subir las fuentes .woff2 a la mediateca
add_filter('upload_mimes', function ($m) {
    $m['woff2'] = 'font/woff2';
    return $m;
});
add_filter('wp_check_filetype_and_ext', function ($data, $file, $filename) {
    if (strtolower(pathinfo($filename, PATHINFO_EXTENSION)) === 'woff2') {
        $data['ext'] = 'woff2';
        $data['type'] = 'font/woff2';
    }
    return $data;
}, 10, 3);
"""
    b64 = lambda txt: base64.b64encode(txt.encode("utf-8")).decode("ascii")
    return (php.replace("__DATA__", data).replace("__LLMSFULL__", b64(llms_full_txt(SITE_URL))).replace("__LLMS__", llms)
            .replace("__ROBOTS__", b64(robots_txt(SITE_URL))).replace("__INDEXNOW_B64__", b64(INDEXNOW_KEY))
            .replace("__INDEXNOW__", INDEXNOW_KEY))


# Rastreadores de buscadores con IA a los que se da paso explícito en robots.txt
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
           "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot",
           "DuckAssistBot", "MistralAI-User", "Meta-ExternalAgent", "Amazonbot", "CCBot"]
# Clave de IndexNow (Bing, Copilot, ChatGPT search, Yandex…): avisa al instante de cada página publicada.
INDEXNOW_KEY = "c4n1745m4l4g4a7f3e9d2b18c6054e1f"


def robots_txt(base):
    bots = "\n".join(f"User-agent: {b}" for b in AI_BOTS)
    return (f"User-agent: *\nDisallow: /wp-admin/\nAllow: /wp-admin/admin-ajax.php\n\n"
            f"# Buscadores con IA: bienvenidos (resumen para ellos en /llms.txt)\n{bots}\nAllow: /\nDisallow: /wp-admin/\n\n"
            f"Sitemap: {base}/sitemap_index.xml\n")


def _md_links(html_text, base):
    """<a href="/x/">texto</a> → [texto](https://dominio/x/) y fuera el resto de etiquetas."""
    import re
    out = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>',
                 lambda m: f"[{m.group(2)}]({base + m.group(1) if m.group(1).startswith('/') else m.group(1)})", html_text)
    return re.sub(r"<[^>]+>", "", out)


def _facts_md(lang, base):
    import faq
    c = Ctx(lang, "wp", "faq")
    return "\n".join(f"- **{k.rstrip(':')}:** {_md_links(v, base)}" for k, v in faq.key_facts(c))


def _pages_md(lang, base):
    t = (lambda es, en: es if lang == "es" else en)
    i = 0 if lang == "es" else 1
    pages = [
        ("maite", t("el restaurante: cocina, sala, terraza y comedor privado", "the restaurant: food, dining room, terrace and private room")),
        ("fresco", t("el rooftop bar de la azotea, abierto al público y sin reserva", "the rooftop bar, open to the public, no reservations")),
        ("carta", t("carta completa con precios de los dos espacios", "full menus with prices for both venues")),
        ("faq", t("preguntas frecuentes: horario, reservas, precios, cómo llegar", "FAQ: opening hours, bookings, prices, directions")),
        ("reservas", t("reservar mesa online", "book a table online")),
        ("grupos", t("grupos de 8 o más, comedor privado y eventos", "groups of 8+, private dining room and events")),
        ("proyecto", t("la historia de los chefs y de Cañitas Maite", "the chefs and the Cañitas Maite story")),
        ("desayunos", t("desayuno y brunch de productores locales, abierto a quien no se aloja en el hotel", "local-producer breakfast and brunch, open to non-guests")),
        ("eventos", t("eventos de empresa: rooftop, salas interiores, cócteles, coffee breaks y cenas de gala", "corporate events: rooftop, indoor rooms, cocktails, coffee breaks and gala dinners")),
        ("brunch", t("brunch en el centro de Málaga", "brunch in Málaga old town")),
        ("desayunar", t("dónde desayunar en Málaga centro", "breakfast in Málaga old town")),
        ("hotelbreakfast", t("desayuno de hotel sin alojarse", "hotel breakfast for non-guests")),
        ("cenaempresa", t("cenas de empresa", "company dinners")),
        ("navidad", t("cenas de Navidad de empresa", "company Christmas parties")),
        ("rooftopeventos", t("rooftop para eventos frente a la Alcazaba", "rooftop event venue facing the Alcazaba")),
        ("reuniones", t("reuniones y coffee breaks", "meetings and coffee breaks")),
        ("contacto", t("contacto y cómo llegar", "contact and directions")),
        ("centro", t("restaurante en el centro de Málaga", "restaurant in Málaga old town")),
        ("donde", t("dónde comer en Málaga", "where to eat in Málaga")),
        ("cenar", t("dónde cenar en Málaga", "dinner in Málaga")),
        ("vistas", t("restaurante con vistas en Málaga", "restaurant with a view in Málaga")),
        ("rooftop", t("rooftop en Málaga", "rooftop bar in Málaga")),
    ]
    import experiences, faq, landings, pages as pg, seo_pages
    builders = dict(pg.PAGES, **landings.PAGES, **faq.PAGES, **experiences.PAGES, **seo_pages.PAGES)
    return "\n".join(f"- [{builders[k](Ctx(lang, 'wp', k))['nav_title']}]({base}/{ROUTES[k][i]}): {d}" for k, d in pages)


def llms_txt(base):
    return f"""# Cañitas Maite Restaurante

> Cañitas Maite Restaurante es el restaurante de los chefs Javier Sanz y Juan Sahuquillo (Cañitas Maite, Casas-Ibáñez, una estrella Michelin) en la última planta del hotel ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga (España): cocina española de producto, parrilla y brasa. En la azotea del mismo hotel está su rooftop bar, Cañitas al Fresco, abierto al público y con vistas a la Alcazaba. También sirven el desayuno/brunch de productores locales del hotel, abierto a quien venga de fuera, y organizan eventos de empresa.
>
> Cañitas Maite Restaurante is the restaurant of chefs Javier Sanz and Juan Sahuquillo (Cañitas Maite, Casas-Ibáñez, one Michelin star) on the top floor of ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga, Spain: Spanish produce-led cooking over the grill. Its rooftop bar, Cañitas al Fresco, is open to the public and faces the Alcazaba. They also run the hotel's local-producer breakfast/brunch, open to non-guests, and corporate events.

Nombre oficial: Cañitas Maite Restaurante (también «Cañitas Maite Málaga»; antes «Cañitas Málaga»). Es la casa de Málaga: no confundir con Cañitas Maite de Casas-Ibáñez (Albacete), el restaurante de origen de los mismos chefs, ni con Cañitas al Fresco de Casas-Ibáñez (cenas de verano, cerrado en invierno). La información completa, con carta y precios, está en [llms-full.txt]({base}/llms-full.txt).

## Datos clave (ES)
{_facts_md("es", base)}

## Key facts (EN)
{_facts_md("en", base)}

## Páginas (ES)
{_pages_md("es", base)}

## Pages (EN)
{_pages_md("en", base)}

## Otros perfiles
- Instagram: {INSTAGRAM}
- Meliá: https://www.melia.com/es/hoteles/espana/malaga/me-malaga/restaurantes/canitas-maite
"""


def llms_full_txt(base):
    """Todo lo que una IA necesita para responder sobre Cañitas Maite Restaurante: datos, preguntas
    frecuentes y cartas con precios, en español y en inglés."""
    import faq
    from menus_data import FRESCO_CARTA, MAITE_CARTA, MAITE_SET_MENUS

    def block(lang):
        c = Ctx(lang, "wp", "faq")
        t = c.t
        eur = (lambda n: f"{n} €") if lang == "es" else (lambda n: f"€{n}")
        out = [f"## {t('Datos clave', 'Key facts')}", _facts_md(lang, base), ""]
        for title, items in faq.faq_groups(c):
            out.append(f"## {t('Preguntas frecuentes', 'FAQ')}: {title}")
            for q, a in items:
                out += [f"### {q}", _md_links(a, base), ""]
        out.append(f"## {t('Carta de Cañitas Maite Restaurante', 'Cañitas Maite Restaurante menu')} ({base}/{ROUTES['carta'][0 if lang == 'es' else 1]})")
        for m in MAITE_SET_MENUS:
            out.append(f"### {t(m['es_name'], m['en_name'])}: {eur(m['price'])} {t('por persona', 'per person')} ({t(m['es_when'], m['en_when'])})")
            for g in m["groups"]:
                out.append(f"- {t(g['es'], g['en'])}: " + "; ".join(t(es, en) for es, en in g["items"]))
            out.append("")
        for title, sections in ((None, MAITE_CARTA), (t("Carta de Cañitas al Fresco (rooftop)", "Cañitas al Fresco menu (rooftop)"), FRESCO_CARTA)):
            if title:
                out.append(f"## {title}")
            for sec in sections:
                out.append(f"### {t(sec['es'], sec['en'])}")
                for es, en, qes, qen, p in sec["items"]:
                    q = t(qes, qen)
                    out.append(f"- {t(es, en)}{f' ({q})' if q else ''}: {eur(p)}")
                out.append("")
        out.append(t("Información sobre alérgenos a disposición del cliente. Precios con IVA incluido.",
                     "Allergen information available on request. Prices include VAT."))
        return "\n".join(out)

    return f"""# Cañitas Maite Restaurante · llms-full.txt

> Información completa de Cañitas Maite Restaurante y Cañitas al Fresco (rooftop bar) en el hotel ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga. Primero en español, después en inglés. Resumen: {base}/llms.txt
>
> Complete information about Cañitas Maite Restaurante and Cañitas al Fresco (rooftop bar) at ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga. Spanish first, then English.

# Español

{block("es")}

# English

{block("en")}
"""


if __name__ == "__main__":
    main()
