"""Contenido de las páginas (ES / EN). Cada función recibe el contexto `c`
y devuelve el título SEO, la meta descripción, el HTML del <main> y los datos
estructurados de la página."""
from build import (BOOKING, EMAIL, HOTEL_URL, INSTAGRAM, MAPS, PHONE, PHONE_TEL, PREVIEW_URL,
                   breadcrumb_ld, esc, fresco_ld, logo_svg, page_hero, pdf_switch, restaurant_ld)
from menus_data import FRESCO_CARTA, MAITE_CARTA, MAITE_SET_MENUS


def price(c, n):
    return f"{n} €" if c.lang == "es" else f"€{n}"


def mailto(subject):
    from urllib.parse import quote
    return f"mailto:{EMAIL}?subject={quote(subject)}"


def gallery(c, items, cls=""):
    figs = "\n".join(
        f"""      <figure class="gallery-item">
        {c.img(name, sizes="(max-width: 700px) 92vw, (max-width: 1100px) 46vw, 380px")}
        <figcaption>{caption}</figcaption>
      </figure>""" for name, caption in items
    )
    return f'    <div class="gallery {cls}">\n{figs}\n    </div>'


def cta_band(c, title, text, actions, cls=""):
    return f"""  <section class="cta-band {cls}">
    <div class="cta-band-inner">
      <h2 class="cta-band-title">{title}</h2>
      <p>{text}</p>
      <div class="cta-band-actions">{actions}</div>
    </div>
  </section>"""


def set_menu_card(c, m):
    groups = []
    for g in m["groups"]:
        lis = "".join(f"<li>{c.t(es, en)}</li>" for es, en in g["items"])
        note = f'<p class="set-menu-note">*{c.t(*g["note"])}</p>' if g.get("note") else ""
        groups.append(f'<div class="set-menu-group"><h4>{c.t(g["es"], g["en"])}</h4><ul>{lis}</ul>{note}</div>')
    return f"""      <article class="set-menu">
        <header class="set-menu-head">
          <h3>{c.t(m["es_name"], m["en_name"])}</h3>
          <p class="set-menu-when">{c.t(m["es_when"], m["en_when"])}</p>
          <p class="set-menu-price">{price(c, m["price"])} <span>{c.t("por persona", "per person")}</span></p>
        </header>
        {"".join(groups)}
      </article>"""


def menu_sections(c, sections, level=3):
    out = []
    for s in sections:
        items = []
        for es, en, qes, qen, p in s["items"]:
            q = c.t(qes, qen)
            qty = f' <span class="menu-qty">({q})</span>' if q else ""
            items.append(f'<li><span class="menu-dish">{c.t(es, en)}{qty}</span><span class="menu-price">{price(c, p)}</span></li>')
        note = f'<p class="menu-note">{c.t(*s["note"])}</p>' if s.get("note") else ""
        out.append(f"""      <section class="menu-section">
        <h{level} class="menu-section-title">{c.t(s["es"], s["en"])}</h{level}>
        {note}
        <ul class="menu-list">{"".join(items)}</ul>
      </section>""")
    return "\n".join(out)


def faq_items(c):
    t = c.t
    return [
        (t("¿Cañitas Maite es un único restaurante o son varios?", "Is Cañitas Maite one restaurant or several?"),
         t("Es una misma casa repartida en dos plantas del hotel ME Málaga by Meliá: Cañitas Maite —el restaurante insignia— en la última planta y Cañitas al Fresco en la azotea. Cada espacio tiene su propio ambiente y horario, pero comparten la misma firma culinaria.",
           "It is one house spread over two floors of ME Málaga by Meliá: Cañitas Maite, the flagship restaurant, on the top floor, and Cañitas al Fresco on the rooftop. Each venue has its own atmosphere and opening hours, but both share the same culinary signature.")),
        (t("¿Cómo reservo mesa?", "How do I book a table?"),
         t(f'Las reservas son para el restaurante Cañitas Maite. Puedes reservar online desde la página <a href="{c.link("reservas")}">Reservar mesa</a>, eligiendo día, hora y número de comensales. Cañitas al Fresco no admite reservas: el acceso es por orden de llegada.',
           f'Bookings are for Cañitas Maite restaurant. You can book online on our <a href="{c.link("reservas")}">Book a table</a> page, choosing the day, time and number of guests. Cañitas al Fresco does not take reservations: entry is first come, first served.')),
        (t("Somos un grupo de 8 personas o más, ¿cómo funciona?", "We are a group of 8 or more. How does it work?"),
         t(f'Las mesas de 8 comensales o más cuentan con un servicio exclusivo de menú cerrado, sin carta libre. Escríbenos con antelación para organizar el menú del grupo; tienes toda la información en <a href="{c.link("grupos")}">Grupos y eventos</a>.',
           f'Tables of 8 or more guests are served an exclusive set menu instead of the à la carte menu. Please get in touch in advance so we can plan your group menu; you will find all the details on <a href="{c.link("grupos")}">Groups & events</a>.')),
        (t("¿Dónde está exactamente?", "Where exactly are you?"),
         t("En el Hotel ME Málaga by Meliá, Calle Victoria, 6, 29012 Málaga, en pleno Distrito Centro. A un minuto a pie de la Plaza de la Merced y a pocos minutos de la Alcazaba, el Museo Picasso Málaga y la Catedral.",
           "At ME Málaga by Meliá, Calle Victoria, 6, 29012 Málaga, right in the city centre. A one-minute walk from Plaza de la Merced and a few minutes from the Alcazaba, the Picasso Museum Málaga and the Cathedral.")),
        (t("¿Puedo ver la carta antes de ir?", "Can I see the menu before I go?"),
         t(f'Sí. Tienes la carta completa de los dos espacios en <a href="{c.link("carta")}">La carta</a>, y puedes descargarla en PDF en español o en inglés.',
           f'Yes. The full menus of both venues are on <a href="{c.link("carta")}">The menu</a> page, and you can download them as a PDF in English or Spanish.')),
        (t("¿Tenéis la carta en inglés?", "Do you have an English menu?"),
         t("Sí. Las cartas de Cañitas Maite y de Cañitas al Fresco están disponibles en inglés, y el sistema de reservas online también funciona en inglés.",
           "Yes. Both the Cañitas Maite and Cañitas al Fresco menus are available in English, and our online booking system works in English too.")),
        (t("¿Tenéis información sobre alérgenos?", "Do you have allergen information?"),
         t("Sí. La información sobre alérgenos está a disposición de todos nuestros clientes: pregunta al equipo de sala y te indicaremos los alérgenos de cada plato.",
           "Yes. Allergen information is available to all our guests: just ask our team and we will tell you the allergens in each dish.")),
        (t("¿Tenéis redes sociales?", "Are you on social media?"),
         t(f'Sí, puedes seguirnos en Instagram como <a href="{INSTAGRAM}" target="_blank" rel="noopener">@canitas_malaga</a>.',
           f'Yes, you can follow us on Instagram at <a href="{INSTAGRAM}" target="_blank" rel="noopener">@canitas_malaga</a>.')),
    ]


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


# ---------------------------------------------------------------------------
# Inicio
# ---------------------------------------------------------------------------
def home(c):
    t = c.t
    faqs = faq_items(c)
    faq_html = "\n".join(
        f"""        <details class="accordion-item"{" open" if i == 0 else ""}>
          <summary><span class="accordion-q"><span class="accordion-index">{i + 1:02d}</span>{q}</span></summary>
          <div class="accordion-body"><p>{a}</p></div>
        </details>""" for i, (q, a) in enumerate(faqs)
    )
    main = f"""  <section class="chooser" id="top">
    <h1 class="chooser-caption">{t('Cañitas Maite Málaga · Restaurante y rooftop en ME Málaga by Meliá, Calle Victoria 6', 'Cañitas Maite Málaga · Restaurant and rooftop bar at ME Málaga by Meliá, Calle Victoria 6')}</h1>

    <div class="chooser-grid" id="espacios">
      <article class="chooser-card chooser-card-signature" data-parallax style="--card-color:#28265a;">
        {c.img("canitas-maite-malaga-comedor-privado", cls="chooser-photo", sizes="(max-width: 900px) 100vw, 50vw", loading="eager", extra="data-parallax-layer")}
        <span class="chooser-overlay" aria-hidden="true"></span>
        <span class="chooser-content">
          <span class="chooser-reveal chooser-reveal-top">
            <span class="chooser-floor">{t('Última planta', 'Top floor')}</span>
            <span class="chooser-tag">{t('El restaurante insignia, con vistas a la Alcazaba', 'The flagship restaurant, overlooking the Alcazaba')}</span>
          </span>
          {logo_svg("chooser-logo chooser-logo-svg", "Cañitas Maite")}
          <span class="chooser-reveal chooser-reveal-bottom">
            <span class="chooser-actions">
              <a class="btn btn-ghost-light btn-small" href="{c.link('reservas')}">{t('Reservar mesa', 'Book a table')}</a>
              <a class="btn btn-text-light btn-small" href="{c.link('carta', anchor='canitas-maite')}">{t('Ver carta', 'See menu')}</a>
            </span>
            <a class="chooser-more" href="{c.link('maite')}">{t('Descubre Cañitas Maite', 'Discover Cañitas Maite')} →</a>
          </span>
        </span>
      </article>

      <article class="chooser-card chooser-card-fresco" data-parallax style="--card-color:#647058;">
        {c.img("canitas-al-fresco-rooftop-piscina-malaga", cls="chooser-photo", sizes="(max-width: 900px) 100vw, 50vw", loading="eager", extra="data-parallax-layer")}
        <span class="chooser-overlay" aria-hidden="true"></span>
        <span class="chooser-content">
          <span class="chooser-reveal chooser-reveal-top">
            <span class="chooser-floor">{t('Azotea', 'Rooftop')}</span>
            <span class="chooser-tag">{t('Rooftop bar &amp; pool, atardeceres largos · sin reserva', 'Rooftop bar &amp; pool, long sunsets · no reservations')}</span>
          </span>
          <img class="chooser-logo" src="{c.asset('logos/logo-canitas-al-fresco-crema.png')}" alt="Cañitas al Fresco" width="260" height="135">
          <span class="chooser-reveal chooser-reveal-bottom">
            <span class="chooser-actions">
              <a class="btn btn-ghost-light btn-small" href="{c.link('carta', anchor='canitas-al-fresco')}">{t('Ver carta', 'See menu')}</a>
            </span>
            <a class="chooser-more" href="{c.link('fresco')}">{t('Descubre Cañitas al Fresco', 'Discover Cañitas al Fresco')} →</a>
          </span>
        </span>
      </article>
    </div>
  </section>

  <section class="details" aria-label="{t('Los espacios en detalle', 'The venues in detail')}">
    <div class="detail-row detail-row-reverse detail-row-signature" id="canitas-maite">
      <div class="detail-media">
        {c.img("txuleta-vasca-parrilla-canitas-maite-malaga", sizes="(max-width: 760px) 92vw, 45vw")}
      </div>
      <div class="detail-copy">
        <p class="detail-eyebrow">{t('Última planta · El restaurante insignia', 'Top floor · The flagship restaurant')}</p>
        <h2>Cañitas Maite</h2>
        <p>{t('La alta cocina del grupo en Málaga, con vistas directas a la Alcazaba y la Catedral. Producto de La Mancha y del sur leído con técnica contemporánea, sin perder la memoria de la cocina de casa que dio origen a Cañitas Maite en Casas-Ibáñez.', 'The group’s fine dining in Málaga, overlooking the Alcazaba and the Cathedral. Produce from La Mancha and the south, cooked with contemporary technique without losing the home cooking that gave birth to Cañitas Maite in Casas-Ibáñez.')}</p>
        <ul class="dish-list">
          <li><span>{t('Entrantes y croquetas', 'Starters and croquettes')}</span><small>{t('Incluida la croqueta de jamón Joselito, elegida la mejor del mundo en 2021.', 'Including our Joselito ham croquette, named the best in the world in 2021.')}</small></li>
          <li><span>{t('Pescados y carnes a la brasa', 'Fish and meat over the embers')}</span><small>{t('Txuleta madurada, lubina entera, calamar de anzuelo: producto de temporada a la parrilla.', 'Dry-aged txuleta, whole sea bass, line-caught squid: seasonal produce on the grill.')}</small></li>
          <li><span>{t('Menús para compartir', 'Sharing menus')}</span><small>{t('Menú Hits todos los días y Menú Classics de lunes a jueves.', 'Hits Menu every day and Classics Menu Monday to Thursday.')}</small></li>
        </ul>
        <div class="detail-actions">
          <a class="btn btn-primary" href="{c.link('reservas')}">{t('Reservar mesa', 'Book a table')}</a>
          <a class="btn btn-ghost" href="{c.link('carta', anchor='canitas-maite')}">{t('Ver la carta', 'See the menu')}</a>
        </div>
        {pdf_switch(c, "maite")}
        <a class="detail-more" href="{c.link('maite')}">{t('Más sobre Cañitas Maite', 'More about Cañitas Maite')} →</a>
      </div>
    </div>

    <div class="detail-row brand-fresco" id="fresco">
      <div class="detail-media">
        {c.img("bikini-trufado-patatas-canitas-al-fresco", sizes="(max-width: 760px) 92vw, 45vw")}
      </div>
      <div class="detail-copy">
        <p class="detail-eyebrow">{t('Azotea · Rooftop bar &amp; pool', 'Rooftop · Bar &amp; pool')}</p>
        <h2>Cañitas al Fresco</h2>
        <p>{t('Rooftop bar y piscina con el skyline de Málaga de fondo. Coctelería de autor y picoteo para sobremesas largas: la misma firma culinaria, en su versión más relajada.', 'Rooftop bar and pool with the Málaga skyline as a backdrop. Signature cocktails and sharing plates for long afternoons: the same culinary signature, in its most relaxed version.')}</p>
        <ul class="dish-list">
          <li><span>{t('Coctelería de autor', 'Signature cocktails')}</span><small>{t('Golden hour, barra y solárium.', 'Golden hour, bar and sun deck.')}</small></li>
          <li><span>{t('Entrantes top y bocatería fina', 'Top starters and gourmet sandwiches')}</span><small>{t('Guacamole casero, ensaladilla de gamba blanca, burger de vaca gallega…', 'Homemade guacamole, white prawn Russian salad, Galician beef burger…')}</small></li>
          <li><span>{t('Sin reserva', 'No reservations')}</span><small>{t('El acceso a la azotea es por orden de llegada.', 'Rooftop entry is first come, first served.')}</small></li>
        </ul>
        <div class="detail-actions">
          <a class="btn btn-primary" href="{c.link('carta', anchor='canitas-al-fresco')}">{t('Ver la carta', 'See the menu')}</a>
        </div>
        {pdf_switch(c, "fresco")}
        <a class="detail-more" href="{c.link('fresco')}">{t('Más sobre Cañitas al Fresco', 'More about Cañitas al Fresco')} →</a>
      </div>
    </div>
  </section>

  <section class="shop" id="tienda" aria-label="{t('Bonos regalo y experiencias', 'Gift vouchers and experiences')}">
    <div class="section-inner shop-grid">
      <div class="shop-copy">
        <p class="eyebrow eyebrow-dark">{t('Tienda online', 'Online shop')}</p>
        <h2 class="section-title">{t('Regala Cañitas Maite', 'Give Cañitas Maite')}</h2>
        <p>{t('Bonos regalo y experiencias gastronómicas pensadas para compartir: una comida en Cañitas Maite o un atardecer en Cañitas al Fresco. Muy pronto podrás comprarlos directamente desde aquí.', 'Gift vouchers and food experiences made for sharing: a meal at Cañitas Maite or a sunset at Cañitas al Fresco. Very soon you will be able to buy them right here.')}</p>
        <div class="shop-actions">
          <span class="shop-badge">{t('Próximamente', 'Coming soon')}</span>
          <a class="detail-more" href="{c.link('bonos')}">{t('Más información', 'Find out more')} →</a>
        </div>
      </div>
      <ul class="shop-list">
        <li><span class="shop-list-index">01</span><div><span class="shop-list-title">{t('Bonos regalo', 'Gift vouchers')}</span><small>{t('Válidos en los dos espacios: Cañitas Maite y Cañitas al Fresco.', 'Valid at both venues: Cañitas Maite and Cañitas al Fresco.')}</small></div></li>
        <li><span class="shop-list-index">02</span><div><span class="shop-list-title">{t('Experiencias gastronómicas', 'Food experiences')}</span><small>{t('Menús y maridajes diseñados por Javier Sanz y Juan Sahuquillo.', 'Menus and pairings designed by Javier Sanz and Juan Sahuquillo.')}</small></div></li>
        <li><span class="shop-list-index">03</span><div><span class="shop-list-title">{t('Envío digital al instante', 'Instant digital delivery')}</span><small>{t('Se reciben por email y se regalan en cualquier ocasión.', 'Delivered by email, ready to give on any occasion.')}</small></div></li>
      </ul>
    </div>
  </section>

  <section class="project" id="proyecto">
    <div class="section-inner">
      <div class="project-header">
        <div class="project-heading">
          <p class="eyebrow eyebrow-dark">{t('El proyecto', 'Our story')}</p>
          <h2 class="section-title">{t('De Casas-Ibáñez<br>al corazón de Málaga', 'From Casas-Ibáñez<br>to the heart of Málaga')}</h2>
        </div>
        <div>
          <p class="manifesto">{t('Cañitas Maite nace en Casas-Ibáñez, Albacete, de la mano de los chefs Javier Sanz y Juan Sahuquillo, con una cocina construida sobre el producto de La Mancha leído con técnica contemporánea. En 2026 desembarca en Málaga dentro del hotel de cinco estrellas ME Málaga by Meliá, asumiendo toda su oferta gastronómica: dos plantas completas, cada una con su propio concepto, ambiente y horario, bajo la misma firma culinaria.', 'Cañitas Maite was born in Casas-Ibáñez, Albacete, led by chefs Javier Sanz and Juan Sahuquillo, with cooking built on La Mancha produce and contemporary technique. In 2026 it arrives in Málaga inside the five-star ME Málaga by Meliá, taking over all of its food offering: two full floors, each with its own concept, atmosphere and hours, under one culinary signature.')}</p>
          <a class="btn btn-ghost-light project-more" href="{c.link('proyecto')}">{t('Conoce nuestra historia', 'Read our story')}</a>
        </div>
      </div>

      <div class="chefs">
        <div class="chefs-photo">
          {c.img("javier-sanz-juan-sahuquillo-chefs-canitas-maite")}
          <span class="chefs-photo-overlay" aria-hidden="true"></span>
          <span class="chefs-photo-caption">
            <span class="chefs-eyebrow">{t('Casas-Ibáñez, Albacete · Estrella Michelin', 'Casas-Ibáñez, Albacete · Michelin star')}</span>
            <span class="chefs-names">Javier Sanz <span class="amp">&amp;</span> Juan Sahuquillo</span>
          </span>
        </div>
      </div>

{hotel_block(c)}
    </div>
  </section>

  <section class="faq" id="faq">
    <div class="section-inner faq-grid">
      <div class="faq-intro">
        <p class="eyebrow eyebrow-dark">{t('Preguntas frecuentes', 'Frequently asked questions')}</p>
        <h2 class="section-title">{t('Antes de venir', 'Before you come')}</h2>
        <p class="faq-note">{t('¿No encuentras lo que buscas? Escríbenos a', 'Can’t find what you are looking for? Email us at')}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div class="accordion">
{faq_html}
      </div>
    </div>
  </section>"""

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs
        ],
    }
    site_ld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Cañitas Maite Málaga",
        "url": c.abs_url("home"),
        "inLanguage": c.lang,
    }
    return dict(
        nav_title=t("Inicio", "Home"),
        title=t("Cañitas Maite Málaga | Restaurante y rooftop en el centro",
                "Cañitas Maite Málaga | Restaurant & Rooftop Bar"),
        desc=t("Restaurante de Javier Sanz y Juan Sahuquillo y rooftop con piscina en ME Málaga by Meliá. Brasa, producto y vistas a la Alcazaba. Reserva online.",
               "Restaurant by chefs Javier Sanz & Juan Sahuquillo and a rooftop pool bar at ME Málaga by Meliá. Grill, great produce, Alcazaba views. Book online."),
        main=main,
        schema=[site_ld, restaurant_ld(c), fresco_ld(c), faq_ld],
    )


def hotel_block(c):
    t = c.t
    slides = [
        "me-malaga-piscina-rooftop", "me-malaga-piscina-catedral", "me-malaga-terraza-alcazaba", "me-malaga-lobby-escalera",
    ]
    imgs = "\n".join(f"            {c.img(n, cls='hotel-gallery-slide', sizes='(max-width: 780px) 92vw, 55vw')}" for n in slides)
    return f"""      <div class="hotel">
        <div class="hotel-gallery">
          <div class="hotel-gallery-track">
{imgs}
          </div>
          <div class="hotel-gallery-controls">
            <button type="button" class="hotel-gallery-btn" data-dir="-1" aria-label="{t('Foto anterior', 'Previous photo')}">‹</button>
            <div class="hotel-gallery-dots" aria-hidden="true"></div>
            <button type="button" class="hotel-gallery-btn" data-dir="1" aria-label="{t('Foto siguiente', 'Next photo')}">›</button>
          </div>
        </div>
        <div class="hotel-info">
          <p class="eyebrow eyebrow-dark">{t('El hotel', 'The hotel')}</p>
          <h3 class="hotel-name">ME Málaga by Meliá</h3>
          <p>{t('Un hotel de cinco estrellas en pleno Distrito Centro, junto a la Plaza de la Merced y a un paso de la Alcazaba, el Museo Picasso Málaga y la Catedral. Su rooftop, con piscina infinity y vistas panorámicas, convive con obras de Picasso y Miró en el lobby. Cañitas Maite ocupa toda su oferta gastronómica, repartida en dos plantas.', 'A five-star hotel in the heart of the city centre, next to Plaza de la Merced and a short walk from the Alcazaba, the Picasso Museum Málaga and the Cathedral. Its rooftop, with an infinity pool and panoramic views, shares the building with works by Picasso and Miró in the lobby. Cañitas Maite runs all of its food offering across two floors.')}</p>
          <a class="btn btn-primary-light" href="{HOTEL_URL[c.lang]}" target="_blank" rel="noopener">{t('Conoce ME Málaga', 'Discover ME Málaga')} ↗</a>
        </div>
      </div>"""


# ---------------------------------------------------------------------------
# Cañitas Maite
# ---------------------------------------------------------------------------
def maite(c):
    t = c.t
    actions = (
        f'<a class="btn btn-primary-light" href="{c.link("reservas")}">{t("Reservar mesa", "Book a table")}</a>'
        f'<a class="btn btn-ghost-light" href="{c.link("carta", anchor="canitas-maite")}">{t("Ver la carta", "See the menu")}</a>'
        + pdf_switch(c, "maite", light=True)
    )
    hero = page_hero(
        c, t("Última planta · ME Málaga by Meliá", "Top floor · ME Málaga by Meliá"), "Cañitas Maite Málaga",
        t("Restaurante de los chefs Javier Sanz y Juan Sahuquillo en el centro de Málaga: producto, parrilla y brasa con vistas a la Alcazaba y la Catedral.",
          "Restaurant by chefs Javier Sanz and Juan Sahuquillo in Málaga city centre: great produce, grill and embers, with views of the Alcazaba and the Cathedral."),
        photo="canitas-maite-malaga-sala-restaurante", actions=actions, crumbs=["Cañitas Maite"])
    menus = "\n".join(set_menu_card(c, m) for m in MAITE_SET_MENUS)
    dishes = gallery(c, [
        ("txuleta-vasca-parrilla-canitas-maite-malaga", t("Txuleta vasca madurada a la parrilla", "Dry-aged Basque txuleta on the grill")),
        ("lubina-parrilla-pil-pil-canitas-maite-malaga", t("Lubina del Atlántico con pil pil de su colágeno", "Atlantic sea bass with collagen pil pil")),
        ("lenguado-brasas-canitas-maite-malaga", t("Lenguado de estero asado en brasas", "Estuary sole roasted over embers")),
        ("mejor-croqueta-del-mundo-jamon-joselito", t("La mejor croqueta del mundo 2021", "The Best Croquette in the World 2021")),
        ("berenjena-burrata-canitas-maite-malaga", t("Berenjena ahumada con burrata fresca", "Smoked aubergine with fresh burrata")),
        ("puerro-romesco-canitas-maite-malaga", t("Puerro asado a la llama con romesco", "Flame-roasted leek with romesco")),
    ])
    main = f"""{hero}

  <section class="section">
    <div class="section-inner split">
      <div>
        <p class="eyebrow eyebrow-dark">{t('La cocina', 'The food')}</p>
        <h2 class="section-title">{t('Producto, brasa y cocina para compartir', 'Great produce, embers and dishes to share')}</h2>
      </div>
      <div class="prose">
        <p>{t('Cañitas Maite trae a la última planta del hotel ME Málaga by Meliá la cocina que nació en Casas-Ibáñez (Albacete): producto de La Mancha y del sur, leído con técnica contemporánea y sin perder la memoria de la cocina de casa.', 'Cañitas Maite brings the cooking born in Casas-Ibáñez (Albacete) to the top floor of ME Málaga by Meliá: produce from La Mancha and the south, cooked with contemporary technique without losing the soul of home cooking.')}</p>
        <p>{t('Aquí manda la parrilla: txuleta vasca madurada, lubina del Atlántico entera, calamar de anzuelo, gamba roja, solomillo ibérico Joselito. Para empezar, conservas y crudos de primera —quisquilla, atún rojo salvaje, anchoa López— y la croqueta de jamón Joselito elegida la mejor del mundo en 2021.', 'The grill is in charge here: dry-aged Basque txuleta, whole Atlantic sea bass, line-caught squid, red prawns and Joselito Iberian pork tenderloin. To start, top-quality raw and cured bites, from quisquilla shrimp and wild bluefin tuna to López anchovies, plus the Joselito ham croquette named the best in the world in 2021.')}</p>
        <p>{t('Una cocina pensada para compartir en el centro de la mesa, con vistas a la Alcazaba y a los tejados del casco histórico.', 'Food made for sharing at the centre of the table, overlooking the Alcazaba and the rooftops of the old town.')}</p>
      </div>
    </div>
  </section>

  <section class="section section-tint" id="menus">
    <div class="section-inner">
      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{t('Menús para compartir', 'Sharing menus')}</p>
        <h2 class="section-title">{t('Menú Hits y Menú Classics', 'Hits Menu and Classics Menu')}</h2>
        <p class="section-intro">{t('Dos formas de probar la casa, todo al centro de la mesa. También puedes pedir a la carta.', 'Two ways to taste the house, everything served to share. You can also order à la carte.')}</p>
      </div>
      <div class="set-menus">
{menus}
      </div>
      <div class="section-actions">
        <a class="btn btn-primary" href="{c.link('carta', anchor='canitas-maite')}">{t('Ver la carta completa', 'See the full menu')}</a>
        {pdf_switch(c, "maite")}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner">
      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{t('Platos de la casa', 'House dishes')}</p>
        <h2 class="section-title">{t('Lo que sale de la parrilla', 'Straight from the grill')}</h2>
      </div>
{dishes}
    </div>
  </section>

  <section class="section section-tint">
    <div class="section-inner">
      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{t('Los espacios', 'The spaces')}</p>
        <h2 class="section-title">{t('Sala, terraza y comedor privado', 'Dining room, terrace and private room')}</h2>
      </div>
      <div class="space-cards">
        <article class="space-card">
          {c.img("canitas-maite-malaga-sala-mesas", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('La sala', 'The dining room')}</h3>
          <p>{t('Bancos corridos, maderas cálidas y azules profundos: el corazón del restaurante.', 'Banquettes, warm wood and deep blues: the heart of the restaurant.')}</p>
        </article>
        <article class="space-card">
          {c.img("canitas-maite-malaga-terraza", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('La terraza', 'The terrace')}</h3>
          <p>{t('Acristalada, con olivos y luz natural sobre los tejados del centro de Málaga.', 'Glass-roofed, with olive trees and natural light over the rooftops of central Málaga.')}</p>
        </article>
        <article class="space-card">
          {c.img("canitas-maite-malaga-comedor-privado", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('El comedor privado', 'The private dining room')}</h3>
          <p>{t('Una mesa única para grupos y celebraciones, con menú cerrado.', 'A single table for groups and celebrations, with a set menu.')} <a href="{c.link('grupos')}">{t('Grupos y eventos', 'Groups & events')} →</a></p>
        </article>
      </div>
    </div>
  </section>

{cta_band(c, t('Reserva tu mesa en Cañitas Maite', 'Book your table at Cañitas Maite'),
          t('Elige día, hora y número de comensales y recibe la confirmación al momento. Para grupos de 8 o más, escríbenos.', 'Choose the day, time and number of guests and get instant confirmation. For groups of 8 or more, please email us.'),
          f'<a class="btn btn-primary-light" href="{c.link("reservas")}">{t("Reservar mesa", "Book a table")}</a><a class="btn btn-ghost-light" href="{c.link("grupos")}">{t("Grupos y eventos", "Groups & events")}</a>')}"""
    return dict(
        nav_title="Cañitas Maite",
        title=t("Cañitas Maite | Restaurante en Málaga centro con vistas",
                "Cañitas Maite | Restaurant in Málaga with Alcazaba Views"),
        desc=t("Restaurante de Javier Sanz y Juan Sahuquillo en ME Málaga: parrilla, producto, la mejor croqueta del mundo 2021 y menús para compartir.",
               "Javier Sanz & Juan Sahuquillo's restaurant at ME Málaga: grill, great produce, the Best Croquette in the World 2021 and sharing menus."),
        main=main,
        schema=[restaurant_ld(c), breadcrumb_ld(c, "Cañitas Maite")],
    )


# ---------------------------------------------------------------------------
# Cañitas al Fresco
# ---------------------------------------------------------------------------
def fresco(c):
    t = c.t
    actions = (
        f'<a class="btn btn-primary-light" href="{c.link("carta", anchor="canitas-al-fresco")}">{t("Ver la carta", "See the menu")}</a>'
        + pdf_switch(c, "fresco", light=True)
    )
    hero = page_hero(
        c, t("Azotea · ME Málaga by Meliá", "Rooftop · ME Málaga by Meliá"), "Cañitas al Fresco",
        t("Rooftop bar y piscina en el centro de Málaga, con la Alcazaba enfrente. Coctelería, picoteo y bocatería fina de Cañitas Maite para alargar la tarde.",
          "Rooftop bar and pool in Málaga city centre, facing the Alcazaba. Cocktails, sharing plates and gourmet sandwiches by Cañitas Maite to make the afternoon last."),
        photo="canitas-al-fresco-rooftop-piscina-malaga", actions=actions, crumbs=["Cañitas al Fresco"])

    def preview(section, n):
        lis = "".join(f'<li><span class="menu-dish">{t(es, en)}</span><span class="menu-price">{price(c, p)}</span></li>' for es, en, _, _, p in section["items"][:n])
        return f'<div class="menu-preview"><h3>{t(section["es"], section["en"])}</h3><ul class="menu-list">{lis}</ul></div>'

    previews = "\n".join(preview(s, n) for s, n in zip(FRESCO_CARTA, (5, 4, 3)))
    dishes = gallery(c, [
        ("guacamole-casero-canitas-al-fresco", t("Guacamole casero con totopos", "Homemade guacamole with tortilla chips")),
        ("hamburguesa-vaca-gallega-canitas-al-fresco", t("Burger de vaca gallega", "Galician beef burger")),
        ("ensaladilla-gamba-blanca-canitas-al-fresco", t("Ensaladilla de gamba blanca", "White prawn Russian salad")),
        ("hummus-crudites-canitas-al-fresco", t("Hummus, crudités y torta de aceite", "Hummus, crudités and olive oil flatbread")),
        ("ensalada-cesar-canitas-al-fresco", t("Ensalada César de pollo campero", "Free-range chicken Caesar salad")),
        ("tarta-de-queso-canitas-al-fresco", t("Tarta de queso con arándanos", "Cheesecake with blueberries")),
    ])
    main = f"""{hero}

  <section class="section">
    <div class="section-inner split">
      <div>
        <p class="eyebrow eyebrow-dark">{t('La azotea', 'The rooftop')}</p>
        <h2 class="section-title">{t('Atardeceres frente a la Alcazaba', 'Sunsets facing the Alcazaba')}</h2>
      </div>
      <div class="prose">
        <p>{t('En lo más alto del hotel ME Málaga by Meliá, Cañitas al Fresco es la versión más relajada de la casa: piscina, tumbonas, barra y una vista que va de la Alcazaba a la Catedral y al puerto.', 'At the very top of ME Málaga by Meliá, Cañitas al Fresco is the house in its most relaxed mood: pool, sun loungers, a bar and a view that sweeps from the Alcazaba to the Cathedral and the port.')}</p>
        <p>{t('Coctelería de autor y una carta pensada para picar y compartir: la croqueta de jamón Joselito, guacamole casero, ensaladilla de gamba blanca, tartar de atún rojo, bikini trufado o la burger de vaca gallega.', 'Signature cocktails and a menu made for grazing and sharing: the Joselito ham croquette, homemade guacamole, white prawn Russian salad, bluefin tuna tartare, the truffled bikini toastie or the Galician beef burger.')}</p>
        <ul class="facts">
          <li><strong>{t('Sin reserva', 'No reservations')}</strong> {t('El acceso es por orden de llegada.', 'Entry is first come, first served.')}</li>
          <li><strong>{t('Carta en inglés', 'English menu')}</strong> {t('Disponible en sala y en PDF.', 'Available on site and as a PDF.')}</li>
          <li><strong>{t('Alérgenos', 'Allergens')}</strong> {t('Información a disposición del cliente.', 'Information available on request.')}</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section section-tint">
    <div class="section-inner">
      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{t('La carta', 'The menu')}</p>
        <h2 class="section-title">{t('Para picar al sol', 'Plates for the sun')}</h2>
      </div>
      <div class="menu-previews">
{previews}
      </div>
      <div class="section-actions">
        <a class="btn btn-primary" href="{c.link('carta', anchor='canitas-al-fresco')}">{t('Ver la carta completa', 'See the full menu')}</a>
        {pdf_switch(c, "fresco")}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner">
      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{t('En la azotea', 'On the rooftop')}</p>
        <h2 class="section-title">{t('Picoteo y bocatería fina', 'Sharing plates and gourmet sandwiches')}</h2>
      </div>
{dishes}
    </div>
  </section>

{cta_band(c, t('Sube a la azotea', 'Come up to the rooftop'),
          t('Sin reserva: te esperamos por orden de llegada en la azotea de ME Málaga by Meliá, Calle Victoria 6.', 'No booking needed: just come up to the rooftop of ME Málaga by Meliá, Calle Victoria 6, first come, first served.'),
          f'<a class="btn btn-primary-light" href="{c.link("carta", anchor="canitas-al-fresco")}">{t("Ver la carta", "See the menu")}</a><a class="btn btn-ghost-light" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")} ↗</a>')}"""
    return dict(
        nav_title="Cañitas al Fresco",
        title=t("Cañitas al Fresco | Rooftop con piscina en Málaga centro",
                "Cañitas al Fresco | Rooftop Pool Bar in Málaga City Centre"),
        desc=t("Rooftop bar y piscina en ME Málaga by Meliá, frente a la Alcazaba: coctelería, picoteo y bocatería fina de Cañitas Maite. Sin reserva.",
               "Rooftop bar and pool at ME Málaga by Meliá, facing the Alcazaba: cocktails, sharing plates and gourmet sandwiches. No booking needed."),
        main=main,
        og="og-canitas-al-fresco",
        theme="brand-fresco",
        schema=[fresco_ld(c), breadcrumb_ld(c, "Cañitas al Fresco")],
    )


# ---------------------------------------------------------------------------
# La carta
# ---------------------------------------------------------------------------
def carta(c):
    t = c.t
    tabs = (
        f'<nav class="menu-tabs" aria-label="{t("Cartas", "Menus")}">'
        f'<a href="#canitas-maite">Cañitas Maite</a><a href="#canitas-al-fresco" class="menu-tab-fresco">Cañitas al Fresco</a></nav>'
    )
    hero = page_hero(c, t("Cañitas Maite · Cañitas al Fresco", "Cañitas Maite · Cañitas al Fresco"), t("La carta", "The menu"),
                     t("La carta de nuestros dos espacios en el hotel ME Málaga by Meliá. Descárgala en PDF en español o en inglés.",
                       "The menus of our two venues at ME Málaga by Meliá. Download them as a PDF in English or Spanish."),
                     photo="lenguado-brasas-canitas-maite-malaga", actions=tabs, crumbs=[t("La carta", "The menu")])
    sets = "\n".join(set_menu_card(c, m) for m in MAITE_SET_MENUS)
    main = f"""{hero}

  <section class="section menu-block" id="canitas-maite">
    <div class="section-inner">
      <header class="menu-block-head">
        <div>
          <p class="eyebrow eyebrow-dark">{t('Última planta', 'Top floor')}</p>
          <h2 class="section-title">{t('Carta de Cañitas Maite', 'Cañitas Maite menu')}</h2>
        </div>
        <div class="menu-block-actions">
          {pdf_switch(c, "maite")}
          <a class="btn btn-primary" href="{c.link('reservas')}">{t('Reservar mesa', 'Book a table')}</a>
        </div>
      </header>

      <h3 class="menu-group-title">{t('Menús para compartir', 'Sharing menus')}</h3>
      <div class="set-menus">
{sets}
      </div>

      <h3 class="menu-group-title">{t('A la carta', 'À la carte')}</h3>
      <div class="menu-columns">
{menu_sections(c, MAITE_CARTA, level=4)}
      </div>
      <p class="menu-footnote">{t('Información sobre alérgenos a disposición del cliente. Los pesos indicados son aproximados.', 'Allergen information available on request. Weights shown are approximate.')}</p>
    </div>
  </section>

  <section class="section section-tint menu-block brand-fresco" id="canitas-al-fresco">
    <div class="section-inner">
      <header class="menu-block-head">
        <div>
          <p class="eyebrow eyebrow-dark">{t('Azotea · sin reserva', 'Rooftop · no reservations')}</p>
          <h2 class="section-title">{t('Carta de Cañitas al Fresco', 'Cañitas al Fresco menu')}</h2>
        </div>
        <div class="menu-block-actions">
          {pdf_switch(c, "fresco")}
          <a class="btn btn-primary" href="{c.link('fresco')}">{t('Conoce la azotea', 'Discover the rooftop')}</a>
        </div>
      </header>
      <div class="menu-columns">
{menu_sections(c, FRESCO_CARTA, level=3)}
      </div>
      <p class="menu-footnote">{t('Información sobre alérgenos a disposición del consumidor.', 'Allergen information available on request.')}</p>
    </div>
  </section>"""
    return dict(
        nav_title=t("La carta", "The menu"),
        title=t("Carta | Cañitas Maite y Cañitas al Fresco, Málaga",
                "Menu | Cañitas Maite & Cañitas al Fresco, Málaga"),
        desc=t("Carta de Cañitas Maite (parrilla, Menú Hits y Menú Classics) y de Cañitas al Fresco, el rooftop de ME Málaga. PDF en español e inglés.",
               "Cañitas Maite menu (grill, Hits and Classics sharing menus) and the Cañitas al Fresco rooftop menu at ME Málaga. PDF in English and Spanish."),
        main=main,
        schema=[breadcrumb_ld(c, t("La carta", "The menu"))],
    )


# ---------------------------------------------------------------------------
# Reservas
# ---------------------------------------------------------------------------
def reservas(c):
    t = c.t
    main = f"""  <section class="reserve-hero">
    <div class="reserve-hero-inner">
      <nav class="breadcrumbs" aria-label="{t('Migas de pan', 'Breadcrumb')}"><ol><li><a href="{c.link('home')}">{t('Inicio', 'Home')}</a></li><li aria-current="page">{t('Reservar mesa', 'Book a table')}</li></ol></nav>
      <p class="eyebrow">{t('Última planta · ME Málaga by Meliá', 'Top floor · ME Málaga by Meliá')}</p>
      <h1 class="reserve-title">{t('Reserva tu mesa en Cañitas Maite', 'Book your table at Cañitas Maite')}</h1>
      <p class="reserve-lead">{t('Alta cocina manchega con vistas a la Alcazaba y la Catedral. Elige día, hora y número de comensales y recibirás la confirmación al momento.', 'Fine dining from La Mancha with views of the Alcazaba and the Cathedral. Choose the day, time and number of guests and you will receive instant confirmation.')}</p>
    </div>
  </section>

  <section class="reserve" id="reserva" aria-label="{t('Reservar mesa en Cañitas Maite', 'Book a table at Cañitas Maite')}">
    <div class="reserve-grid">
      <aside class="reserve-aside">
        <div class="reserve-photo">
          {c.img("canitas-maite-malaga-comedor-privado-horizontal", sizes="(max-width: 900px) 92vw, 40vw")}
        </div>
        <ul class="reserve-notes">
          <li><span>{t('Grupos de 8 o más', 'Groups of 8 or more')}</span><small>{t('Servicio exclusivo de menú cerrado.', 'Exclusive set menu service.')} <a href="{c.link('grupos')}">{t('Escríbenos con antelación', 'Please contact us in advance')}</a>.</small></li>
          <li><span>Cañitas al Fresco</span><small>{t('La azotea no admite reservas: el acceso es por orden de llegada.', 'The rooftop does not take reservations: entry is first come, first served.')}</small></li>
          <li><span>{t('Antes de venir', 'Before you come')}</span><small><a href="{c.link('carta', anchor='canitas-maite')}">{t('Consulta la carta de Cañitas Maite', 'See the Cañitas Maite menu')}</a></small></li>
        </ul>
        {pdf_switch(c, "maite")}
        <div class="reserve-contact">
          <p class="detail-eyebrow">{t('¿Prefieres hablar con nosotros?', 'Would you rather talk to us?')}</p>
          <a href="tel:{PHONE_TEL}">{PHONE}</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <address>Hotel ME Málaga by Meliá<br>Calle Victoria, 6 · 29012 Málaga</address>
        </div>
      </aside>

      <div class="reserve-widget">
        <iframe src="{BOOKING[c.lang]}" title="{t('Sistema de reservas de Cañitas Maite', 'Cañitas Maite booking system')}" loading="eager" allow="payment"></iframe>
        <p class="reserve-fallback">{t('¿No ves el formulario?', 'Can’t see the form?')} <a href="{BOOKING[c.lang]}" target="_blank" rel="noopener">{t('Abre la reserva en una ventana nueva', 'Open the booking page in a new window')} ↗</a></p>
      </div>
    </div>
  </section>"""
    return dict(
        nav_title=t("Reservar mesa", "Book a table"),
        title=t("Reservar mesa en Cañitas Maite Málaga | Reserva online",
                "Book a Table at Cañitas Maite Málaga | Online Booking"),
        desc=t("Reserva online tu mesa en Cañitas Maite, el restaurante de la última planta de ME Málaga by Meliá con vistas a la Alcazaba. Confirmación inmediata.",
               "Book your table online at Cañitas Maite, the top-floor restaurant at ME Málaga by Meliá overlooking the Alcazaba. Instant confirmation."),
        main=main,
        contact=False,
        schema=[breadcrumb_ld(c, t("Reservar mesa", "Book a table"))],
    )


# ---------------------------------------------------------------------------
# Grupos y eventos
# ---------------------------------------------------------------------------
def grupos(c):
    t = c.t
    subject = t("Grupos y eventos — Cañitas Maite Málaga", "Groups & events — Cañitas Maite Málaga")
    actions = (
        f'<a class="btn btn-primary-light" href="{mailto(subject)}">{t("Escríbenos", "Email us")}</a>'
        f'<a class="btn btn-ghost-light" href="tel:{PHONE_TEL}">{PHONE}</a>'
    )
    hero = page_hero(c, t("Cañitas Maite · Cañitas al Fresco", "Cañitas Maite · Cañitas al Fresco"), t("Grupos y eventos", "Groups & events"),
                     t("Comidas de grupo, celebraciones y eventos de empresa en el centro de Málaga, con la cocina de Cañitas Maite y un comedor privado en la última planta de ME Málaga by Meliá.",
                       "Group lunches and dinners, celebrations and corporate events in Málaga city centre, with Cañitas Maite cooking and a private dining room on the top floor of ME Málaga by Meliá."),
                     photo="canitas-maite-malaga-comedor-privado-horizontal", actions=actions, crumbs=[t("Grupos y eventos", "Groups & events")])
    main = f"""{hero}

  <section class="section">
    <div class="section-inner split">
      <div>
        <p class="eyebrow eyebrow-dark">{t('Mesas de 8 o más', 'Tables of 8 or more')}</p>
        <h2 class="section-title">{t('Un menú cerrado pensado para tu grupo', 'A set menu designed for your group')}</h2>
      </div>
      <div class="prose">
        <p>{t('Las mesas de 8 comensales o más cuentan con un servicio exclusivo de menú cerrado, sin carta libre, para que todo el grupo disfrute de lo mejor de la casa al mismo ritmo.', 'Tables of 8 or more guests enjoy an exclusive set menu instead of the à la carte menu, so the whole group can enjoy the best of the house at the same pace.')}</p>
        <p>{t('Cuéntanos la fecha, el número de personas y qué celebráis, y te enviaremos nuestras propuestas de menú.', 'Tell us the date, the number of guests and what you are celebrating, and we will send you our menu proposals.')}</p>
      </div>
    </div>
  </section>

  <section class="section section-tint">
    <div class="section-inner">
      <div class="space-cards">
        <article class="space-card">
          {c.img("canitas-maite-malaga-comedor-privado", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('Comedor privado', 'Private dining room')}</h3>
          <p>{t('Una sala reservada con una sola mesa, en la última planta de Cañitas Maite: ideal para comidas de empresa y celebraciones familiares.', 'A private room with a single table on the top floor at Cañitas Maite: ideal for business lunches and family celebrations.')}</p>
        </article>
        <article class="space-card">
          {c.img("canitas-maite-malaga-sala-mesas", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('Celebraciones en Cañitas Maite', 'Celebrations at Cañitas Maite')}</h3>
          <p>{t('Cumpleaños, aniversarios o comidas de equipo con la cocina de brasa y producto de Javier Sanz y Juan Sahuquillo.', 'Birthdays, anniversaries or team dinners with the grill-and-produce cooking of Javier Sanz and Juan Sahuquillo.')}</p>
        </article>
        <article class="space-card brand-fresco">
          {c.img("canitas-al-fresco-rooftop-piscina-malaga", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('Eventos en la azotea', 'Rooftop events')}</h3>
          <p>{t('Cócteles y eventos privados en Cañitas al Fresco, con la Alcazaba de fondo. Consúltanos disponibilidad.', 'Cocktail receptions and private events at Cañitas al Fresco, with the Alcazaba as a backdrop. Ask us about availability.')}</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner">
      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{t('Cómo funciona', 'How it works')}</p>
        <h2 class="section-title">{t('Organiza tu evento en tres pasos', 'Plan your event in three steps')}</h2>
      </div>
      <ol class="steps">
        <li><span class="steps-index">01</span><h3>{t('Escríbenos', 'Get in touch')}</h3><p>{t('Indícanos fecha, hora, número de personas y tipo de evento.', 'Tell us the date, time, number of guests and type of event.')}</p></li>
        <li><span class="steps-index">02</span><h3>{t('Recibe la propuesta', 'Receive our proposal')}</h3><p>{t('Te enviamos los menús disponibles y las opciones de espacio.', 'We send you the available menus and space options.')}</p></li>
        <li><span class="steps-index">03</span><h3>{t('Cerramos los detalles', 'We finalise the details')}</h3><p>{t('Confirmamos menú, horarios y cualquier necesidad especial o alergia.', 'We confirm the menu, timings and any special requirements or allergies.')}</p></li>
      </ol>
    </div>
  </section>

{cta_band(c, t('¿Tienes una fecha en mente?', 'Have a date in mind?'),
          t(f'Escríbenos a <a href="{mailto(subject)}">{EMAIL}</a> o llámanos al <a href="tel:{PHONE_TEL}">{PHONE}</a>.', f'Email us at <a href="{mailto(subject)}">{EMAIL}</a> or call us on <a href="tel:{PHONE_TEL}">{PHONE}</a>.'),
          f'<a class="btn btn-primary-light" href="{mailto(subject)}">{t("Solicitar propuesta", "Request a proposal")}</a>')}"""
    return dict(
        nav_title=t("Grupos y eventos", "Groups & events"),
        title=t("Restaurante para grupos en Málaga | Comedor privado",
                "Group Dining in Málaga | Private Room at Cañitas Maite"),
        desc=t("Comidas de grupo, celebraciones y eventos de empresa en Cañitas Maite y en la azotea Cañitas al Fresco, en ME Málaga by Meliá. Comedor privado y menús cerrados.",
               "Group dining, celebrations and corporate events at Cañitas Maite and the Cañitas al Fresco rooftop at ME Málaga by Meliá. Private dining room and set menus."),
        main=main,
        schema=[breadcrumb_ld(c, t("Grupos y eventos", "Groups & events"))],
    )


# ---------------------------------------------------------------------------
# Bonos regalo
# ---------------------------------------------------------------------------
def bonos(c):
    t = c.t
    subject = t("Bonos regalo — Cañitas Maite Málaga", "Gift vouchers — Cañitas Maite Málaga")
    hero = page_hero(c, t("Tienda online · Próximamente", "Online shop · Coming soon"), t("Bonos regalo", "Gift vouchers"),
                     t("Regala una comida en Cañitas Maite o un atardecer en Cañitas al Fresco. Muy pronto podrás comprar bonos regalo y experiencias gastronómicas desde esta página.",
                       "Give a meal at Cañitas Maite or a sunset at Cañitas al Fresco. Very soon you will be able to buy gift vouchers and food experiences on this page."),
                     photo="mejor-croqueta-del-mundo-jamon-joselito", crumbs=[t("Bonos regalo", "Gift vouchers")])
    main = f"""{hero}

  <section class="shop">
    <div class="section-inner shop-grid">
      <div class="shop-copy">
        <p class="eyebrow eyebrow-dark">{t('Qué podrás regalar', 'What you will be able to give')}</p>
        <h2 class="section-title">{t('Regala Cañitas Maite', 'Give Cañitas Maite')}</h2>
        <p>{t('Estamos preparando la tienda online. Mientras tanto, si quieres regalar una experiencia en Cañitas Maite, escríbenos y te contamos cómo hacerlo.', 'We are getting our online shop ready. In the meantime, if you would like to give a Cañitas Maite experience, email us and we will tell you how.')}</p>
        <div class="shop-actions">
          <span class="shop-badge">{t('Próximamente', 'Coming soon')}</span>
          <a class="btn btn-primary" href="{mailto(subject)}">{t('Escríbenos', 'Email us')}</a>
        </div>
      </div>
      <ul class="shop-list">
        <li><span class="shop-list-index">01</span><div><span class="shop-list-title">{t('Bonos regalo', 'Gift vouchers')}</span><small>{t('Válidos en los dos espacios: Cañitas Maite y Cañitas al Fresco.', 'Valid at both venues: Cañitas Maite and Cañitas al Fresco.')}</small></div></li>
        <li><span class="shop-list-index">02</span><div><span class="shop-list-title">{t('Experiencias gastronómicas', 'Food experiences')}</span><small>{t('Menús y maridajes diseñados por Javier Sanz y Juan Sahuquillo.', 'Menus and pairings designed by Javier Sanz and Juan Sahuquillo.')}</small></div></li>
        <li><span class="shop-list-index">03</span><div><span class="shop-list-title">{t('Envío digital al instante', 'Instant digital delivery')}</span><small>{t('Se reciben por email y se regalan en cualquier ocasión.', 'Delivered by email, ready to give on any occasion.')}</small></div></li>
      </ul>
    </div>
  </section>"""
    return dict(
        nav_title=t("Bonos regalo", "Gift vouchers"),
        title=t("Bonos regalo | Cañitas Maite Málaga",
                "Cañitas Maite Málaga Gift Vouchers | Give a Food Experience"),
        desc=t("Bonos regalo y experiencias gastronómicas de Cañitas Maite en Málaga, válidos en el restaurante y en el rooftop Cañitas al Fresco. Muy pronto, compra online.",
               "Gift vouchers and food experiences from Cañitas Maite in Málaga, valid at the restaurant and at the Cañitas al Fresco rooftop. Online shop coming soon."),
        main=main,
        schema=[breadcrumb_ld(c, t("Bonos regalo", "Gift vouchers"))],
    )


# ---------------------------------------------------------------------------
# El proyecto
# ---------------------------------------------------------------------------
def proyecto(c):
    t = c.t
    hero = page_hero(c, t("El proyecto", "Our story"), t("De Casas-Ibáñez al corazón de Málaga", "From Casas-Ibáñez to the heart of Málaga"),
                     t("La historia de Cañitas Maite, la cocina de Javier Sanz y Juan Sahuquillo, y su llegada al hotel ME Málaga by Meliá.",
                       "The story of Cañitas Maite, the cooking of Javier Sanz and Juan Sahuquillo, and their arrival at ME Málaga by Meliá."),
                     photo="chefs-canitas-maite-alcazaba-malaga", crumbs=[t("El proyecto", "Our story")])
    main = f"""{hero}

  <section class="section">
    <div class="section-inner split">
      <div>
        <p class="eyebrow eyebrow-dark">{t('Los orígenes', 'Where it began')}</p>
        <h2 class="section-title">{t('Una cocina con memoria', 'Cooking with a memory')}</h2>
      </div>
      <div class="prose">
        <p>{t('Cañitas Maite nace en Casas-Ibáñez, Albacete, de la mano de los chefs Javier Sanz y Juan Sahuquillo. Su cocina se construye sobre el producto de La Mancha, leído con técnica contemporánea, sin perder la memoria de la cocina de casa que dio origen a la familia Cañitas Maite. Un trabajo reconocido con una estrella Michelin.', 'Cañitas Maite was born in Casas-Ibáñez, Albacete, led by chefs Javier Sanz and Juan Sahuquillo. Their cooking is built on La Mancha produce and contemporary technique, without losing the home cooking at the root of the Cañitas Maite family. Their work has been recognised with a Michelin star.')}</p>
        <p>{t('En 2026, Cañitas Maite desembarca en Málaga dentro del hotel de cinco estrellas ME Málaga by Meliá y asume toda su oferta gastronómica. No es un restaurante más de hotel, sino dos plantas completas —cada una con su propio concepto, ambiente y horario— bajo la misma firma culinaria.', 'In 2026, Cañitas Maite arrives in Málaga inside the five-star ME Málaga by Meliá and takes over all of its food offering. It is not just another hotel restaurant, but two full floors, each with its own concept, atmosphere and hours, under one culinary signature.')}</p>
      </div>
    </div>
  </section>

  <section class="section section-tint">
    <div class="section-inner">
      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{t('Los chefs', 'The chefs')}</p>
        <h2 class="section-title">Javier Sanz &amp; Juan Sahuquillo</h2>
      </div>
      <div class="chef-cards">
        <article class="space-card">
          {c.img("javier-sanz-chef-canitas-maite", sizes="(max-width: 860px) 92vw, 46vw")}
          <h3>Javier Sanz</h3>
          <p>{t('Cocinero y cofundador de Cañitas Maite. En Málaga, al frente de la cocina junto a Juan Sahuquillo.', 'Chef and co-founder of Cañitas Maite. In Málaga, he leads the kitchen alongside Juan Sahuquillo.')}</p>
        </article>
        <article class="space-card">
          {c.img("juan-sahuquillo-chef-canitas-maite", sizes="(max-width: 860px) 92vw, 46vw")}
          <h3>Juan Sahuquillo</h3>
          <p>{t('Cocinero y cofundador de Cañitas Maite. En Málaga, al frente de la cocina junto a Javier Sanz.', 'Chef and co-founder of Cañitas Maite. In Málaga, he leads the kitchen alongside Javier Sanz.')}</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner split split-media">
      <div class="split-photo">{c.img("mejor-croqueta-del-mundo-jamon-joselito", sizes="(max-width: 860px) 92vw, 46vw")}</div>
      <div class="prose">
        <p class="eyebrow eyebrow-dark">{t('Un clásico de la casa', 'A house classic')}</p>
        <h2 class="section-title">{t('La mejor croqueta del mundo', 'The best croquette in the world')}</h2>
        <p>{t('En 2021 nuestra croqueta de jamón Joselito fue elegida la mejor del mundo. Hoy es el primer bocado de casi todas las mesas, tanto en Cañitas Maite como en Cañitas al Fresco.', 'In 2021 our Joselito ham croquette was named the best in the world. Today it is the first bite at almost every table, both at Cañitas Maite and at Cañitas al Fresco.')}</p>
        <a class="detail-more" href="{c.link('carta')}">{t('Ver la carta', 'See the menu')} →</a>
      </div>
    </div>
  </section>

  <section class="project">
    <div class="section-inner">
{hotel_block(c)}
    </div>
  </section>

{cta_band(c, t('Dos espacios, una misma casa', 'Two venues, one house'),
          t('Cañitas Maite en la última planta y Cañitas al Fresco en la azotea.', 'Cañitas Maite on the top floor and Cañitas al Fresco on the rooftop.'),
          f'<a class="btn btn-primary-light" href="{c.link("maite")}">Cañitas Maite</a><a class="btn btn-ghost-light" href="{c.link("fresco")}">Cañitas al Fresco</a>')}"""
    return dict(
        nav_title=t("El proyecto", "Our story"),
        title=t("El proyecto | Javier Sanz y Juan Sahuquillo, Cañitas Maite",
                "Our Story | Javier Sanz & Juan Sahuquillo, Cañitas Maite"),
        desc=t("De Casas-Ibáñez a Málaga: la historia de Cañitas Maite, la cocina de Javier Sanz y Juan Sahuquillo (estrella Michelin) y su llegada a ME Málaga.",
               "From Casas-Ibáñez to Málaga: the story of Cañitas Maite, the Michelin-starred cooking of Javier Sanz and Juan Sahuquillo, and their move to ME Málaga."),
        main=main,
        schema=[breadcrumb_ld(c, t("El proyecto", "Our story"))],
    )


# ---------------------------------------------------------------------------
# Contacto
# ---------------------------------------------------------------------------
def contacto(c):
    t = c.t
    hero = page_hero(c, "Calle Victoria, 6 · Málaga", t("Contacto y cómo llegar", "Contact & directions"),
                     t("Estamos en el hotel ME Málaga by Meliá, en pleno centro histórico, junto a la Plaza de la Merced.",
                       "You will find us at ME Málaga by Meliá, in the heart of the old town, next to Plaza de la Merced."),
                     crumbs=[t("Contacto", "Contact")])
    main = f"""{hero}

  <section class="section">
    <div class="section-inner">
      <div class="info-cards">
        <article class="info-card">
          <h2>{t('Reservas', 'Bookings')}</h2>
          <p>{t('Reserva online tu mesa en Cañitas Maite y recibe la confirmación al momento.', 'Book your table at Cañitas Maite online and get instant confirmation.')}</p>
          <a class="detail-more" href="{c.link('reservas')}">{t('Reservar mesa', 'Book a table')} →</a>
        </article>
        <article class="info-card">
          <h2>{t('Grupos y eventos', 'Groups & events')}</h2>
          <p>{t('Para mesas de 8 o más, comedor privado y eventos, escríbenos.', 'For tables of 8 or more, the private dining room and events, email us.')}</p>
          <a class="detail-more" href="{c.link('grupos')}">{t('Más información', 'Find out more')} →</a>
        </article>
        <article class="info-card brand-fresco">
          <h2>Cañitas al Fresco</h2>
          <p>{t('La azotea no admite reservas: el acceso es por orden de llegada.', 'The rooftop does not take reservations: entry is first come, first served.')}</p>
          <a class="detail-more" href="{c.link('fresco')}">{t('Conoce la azotea', 'Discover the rooftop')} →</a>
        </article>
        <article class="info-card">
          <h2>{t('Teléfono y email', 'Phone and email')}</h2>
          <p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          <a class="detail-more" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram →</a>
        </article>
      </div>
    </div>
  </section>"""
    return dict(
        nav_title=t("Contacto", "Contact"),
        title=t("Contacto y cómo llegar | Cañitas Maite, Calle Victoria 6",
                "Contact & Directions | Cañitas Maite Málaga, Calle Victoria 6"),
        desc=t("Cañitas Maite y Cañitas al Fresco están en el hotel ME Málaga by Meliá, Calle Victoria 6, junto a la Plaza de la Merced. Teléfono, email, mapa y cómo llegar.",
               "Cañitas Maite and Cañitas al Fresco are at ME Málaga by Meliá, Calle Victoria 6, next to Plaza de la Merced. Phone, email, map and directions."),
        main=main,
        schema=[restaurant_ld(c), breadcrumb_ld(c, t("Contacto", "Contact"))],
    )


PAGES = {
    "home": home,
    "maite": maite,
    "fresco": fresco,
    "carta": carta,
    "reservas": reservas,
    "grupos": grupos,
    "bonos": bonos,
    "proyecto": proyecto,
    "contacto": contacto,
}


# ---------------------------------------------------------------------------
# Páginas especiales de la vista previa
# ---------------------------------------------------------------------------
def page_404():
    root = "/canitas-malaga/"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página no encontrada · Page not found — Cañitas Maite Málaga</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}css/styles.css">
</head>
<body>
<main class="not-found">
  <div class="not-found-inner">
    <a href="{root}" class="logo" aria-label="Cañitas Maite Málaga">{logo_svg("logo-mark logo-mark-footer")}</a>
    <p class="eyebrow">404</p>
    <h1 class="page-title">Esta página no existe</h1>
    <p class="page-lead" lang="en">This page doesn’t exist.</p>
    <div class="page-hero-actions">
      <a class="btn btn-primary-light" href="{root}">Ir al inicio</a>
      <a class="btn btn-ghost-light" href="{root}en/" lang="en">Go to homepage</a>
      <a class="btn btn-ghost-light" href="{root}reservas/">Reservar mesa</a>
    </div>
  </div>
</main>
</body>
</html>
"""


def redirect_page(target):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Reservar mesa — Cañitas Maite Málaga</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{PREVIEW_URL}/{target}">
<meta http-equiv="refresh" content="0; url={target}">
</head>
<body>
<p><a href="{target}">Reservar mesa en Cañitas Maite</a></p>
</body>
</html>
"""
