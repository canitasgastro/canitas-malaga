"""Páginas de búsqueda local (ES / EN). No están en el menú principal: se enlazan
desde el pie y entre sí, y están en el sitemap. Cada una responde a una
intención de búsqueda distinta con contenido propio:

  restaurante-centro-malaga   restaurantes centro Málaga / restaurant Málaga old town
  donde-comer-en-malaga       dónde comer en Málaga / where to eat in Málaga
  donde-cenar-en-malaga       dónde cenar en Málaga / dinner in Málaga
  restaurante-con-vistas      restaurante con vistas Málaga / restaurant with a view
  rooftop-malaga              rooftop / azotea Málaga / rooftop bar Málaga
"""
from build import (EMAIL, MAPS, PHONE, hours_text, breadcrumb_ld, fresco_ld, page_hero, menu_lang, restaurant_ld)
from pages import cta_band, gallery, strip_tags


def faq_block(c, items, title=None):
    t = c.t
    rows = "\n".join(
        f"""        <details class="accordion-item"{" open" if i == 0 else ""}>
          <summary><span class="accordion-q"><span class="accordion-index">{i + 1:02d}</span>{q}</span></summary>
          <div class="accordion-body"><p>{a}</p></div>
        </details>""" for i, (q, a) in enumerate(items)
    )
    return f"""  <section class="faq">
    <div class="section-inner faq-grid">
      <div class="faq-intro">
        <p class="eyebrow eyebrow-dark">{t('Preguntas frecuentes', 'Frequently asked questions')}</p>
        <h2 class="section-title">{title or t('Lo que más nos preguntan', 'What people ask us')}</h2>
      </div>
      <div class="accordion">
{rows}
      </div>
    </div>
  </section>"""


def faq_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in items],
    }


def split(c, eyebrow, title, paragraphs, extra=""):
    ps = "\n".join(f"        <p>{p}</p>" for p in paragraphs)
    return f"""  <section class="section">
    <div class="section-inner split">
      <div>
        <p class="eyebrow eyebrow-dark">{eyebrow}</p>
        <h2 class="section-title">{title}</h2>
      </div>
      <div class="prose">
{ps}
        {extra}
      </div>
    </div>
  </section>"""


def facts(items):
    return '<ul class="facts">' + "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in items) + "</ul>"


def cards(c, items, tint=True):
    arts = "\n".join(
        f"""        <article class="info-card{' brand-fresco' if fresco else ''}">
          <h3>{h}</h3>
          <p>{p}</p>
          {f'<a class="detail-more" href="{href}">{label} →</a>' if href else ''}
        </article>""" for h, p, href, label, fresco in items
    )
    return f"""  <section class="section{' section-tint' if tint else ''}">
    <div class="section-inner">
      <div class="info-cards">
{arts}
      </div>
    </div>
  </section>"""


def more_links(c, current):
    t = c.t
    links = [
        ("centro", t("Restaurante en el centro de Málaga", "Restaurant in Málaga old town")),
        ("donde", t("Dónde comer en Málaga", "Where to eat in Málaga")),
        ("cenar", t("Dónde cenar en Málaga", "Dinner in Málaga")),
        ("vistas", t("Restaurante con vistas en Málaga", "Restaurant with a view in Málaga")),
        ("rooftop", t("Rooftop en Málaga", "Rooftop bar in Málaga")),
    ]
    lis = "".join(f'<li><a href="{c.link(k)}">{label}</a></li>' for k, label in links if k != current)
    return f"""  <section class="section">
    <div class="section-inner">
      <nav class="related" aria-label="{t('Más ideas en Málaga', 'More ideas in Málaga')}">
        <p class="eyebrow eyebrow-dark">{t('Más ideas en Málaga', 'More ideas in Málaga')}</p>
        <ul>{lis}</ul>
      </nav>
    </div>
  </section>"""


def book_actions(c, menu_anchor="canitas-malaga"):
    t = c.t
    return (f'<a class="btn btn-primary-light" href="{c.link("reservas")}">{t("Reservar mesa", "Book a table")}</a>'
            f'<a class="btn btn-ghost-light" href="{c.link("carta", anchor=menu_anchor)}">{t("Ver la carta", "See the menu")}</a>'
            f'<a class="btn btn-ghost-light" href="{c.link("carta", anchor="menus")}">{t("Ver menús", "Set menus")}</a>')


def walk_list(c):
    t = c.t
    return facts([
        ("Plaza de la Merced", t("1 minuto a pie", "1 minute's walk")),
        (t("Alcazaba y Teatro Romano", "Alcazaba and Roman Theatre"), t("3 minutos", "3 minutes")),
        (t("Museo Picasso Málaga", "Picasso Museum Málaga"), t("3 minutos", "3 minutes")),
        (t("Catedral de Málaga", "Málaga Cathedral"), t("5 minutos", "5 minutes")),
        ("Calle Larios", t("unos 8 minutos", "about 8 minutes")),
        (t("Horario", "Opening hours"), hours_text(c.lang, "maite") + "."),
    ])


# ---------------------------------------------------------------------------
def centro(c):
    t = c.t
    faqs = [
        (t("¿Dónde está exactamente Cañitas Málaga?", "Where exactly is Cañitas Málaga?"),
         t("En la última planta del hotel ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga, a un minuto a pie de la Plaza de la Merced.",
           "On the top floor of ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga, a one-minute walk from Plaza de la Merced.")),
        (t("¿Hay que reservar?", "Do I need to book?"),
         t(f'Para el restaurante Cañitas Málaga sí te recomendamos reservar, sobre todo en fin de semana: puedes hacerlo <a href="{c.link("reservas")}">online</a>. El rooftop Cañitas al Fresco no admite reservas.',
           f'For Cañitas Málaga we recommend booking, especially at weekends: you can do it <a href="{c.link("reservas")}">online</a>. The Cañitas al Fresco rooftop does not take reservations.')),
        (t("¿Cuánto cuesta comer en Cañitas Málaga?", "How much does a meal at Cañitas Málaga cost?"),
         t("Tienes el Menú Classics por 39 € por persona (de lunes a jueves) y el Menú Hits por 69 € por persona (todos los días). A la carta, los platos van de 8 € a 65 € y están pensados para compartir.",
           "There is the Classics Menu at €39 per person (Monday to Thursday) and the Hits Menu at €69 per person (every day). À la carte, dishes range from €8 to €65 and are made for sharing.")),
        (t("¿Tenéis carta en inglés?", "Do you have an English menu?"),
         t(f'Sí. Puedes consultarla en español o en inglés en <a href="{c.link("carta")}">la carta</a>.',
           f'Yes. You can read it in English or Spanish on <a href="{c.link("carta")}">the menu page</a>.')),
    ]
    hero = page_hero(c, "Calle Victoria, 6 · Plaza de la Merced",
                     t("Restaurante en el centro de Málaga", "Restaurant in Málaga old town"),
                     t("Cañitas Málaga está en pleno centro histórico, en la última planta del hotel ME Málaga by Meliá: a un paso de la Alcazaba, el Museo Picasso y la Catedral.",
                       "Cañitas Málaga sits in the heart of the old town, on the top floor of ME Málaga by Meliá: a short walk from the Alcazaba, the Picasso Museum and the Cathedral."),
                     photo="canitas-malaga-sala-restaurante", actions=book_actions(c),
                     crumbs=[t("Restaurante en el centro de Málaga", "Restaurant in Málaga old town")])
    main = "\n\n".join([
        hero,
        split(c, t("La ubicación", "The location"), t("En pleno centro histórico, junto a la Plaza de la Merced", "Right in the old town, next to Plaza de la Merced"), [
            t("Comer en el centro de Málaga sin renunciar a la buena cocina es fácil si sabes dónde subir. Cañitas Málaga ocupa la última planta del hotel ME Málaga by Meliá, en Calle Victoria 6, y desde sus mesas se ven la Alcazaba, Gibralfaro y los tejados del casco antiguo.",
              "Eating well in central Málaga is easy if you know where to go up. Cañitas Málaga takes up the top floor of ME Málaga by Meliá, at Calle Victoria 6, and its tables look out over the Alcazaba, Gibralfaro and the rooftops of the old town."),
            t("Es el sitio perfecto para comer después de visitar el Museo Picasso o la Alcazaba, o para cenar tras un paseo por calle Larios. Todo queda a pocos minutos a pie:",
              "It is the perfect place for lunch after visiting the Picasso Museum or the Alcazaba, or for dinner after a stroll down Calle Larios. Everything is a few minutes' walk away:"),
        ], extra=walk_list(c)),
        cards(c, [
            (t("La cocina", "The food"), t("Producto de La Mancha y del sur, parrilla y brasa: txuleta vasca madurada, lubina del Atlántico entera, calamar de anzuelo, gamba roja y la croqueta de jamón Joselito elegida la mejor del mundo en 2021.", "Produce from La Mancha and the south, grill and embers: dry-aged Basque txuleta, whole Atlantic sea bass, line-caught squid, red prawns and the Joselito ham croquette named the best in the world in 2021."), c.link("carta", anchor="canitas-malaga"), t("Ver la carta", "See the menu"), False),
            (t("Menús para compartir", "Sharing menus"), t("Menú Classics por 39 € por persona, de lunes a jueves, y Menú Hits por 69 € por persona, todos los días.", "Classics Menu at €39 per person, Monday to Thursday, and Hits Menu at €69 per person, every day."), c.link("maite", anchor="menus"), t("Ver los menús", "See the menus"), False),
            (t("Los chefs", "The chefs"), t("Javier Sanz y Juan Sahuquillo, de Cañitas Maite (Casas-Ibáñez, una estrella Michelin), firman toda la oferta gastronómica del hotel.", "Javier Sanz and Juan Sahuquillo of Cañitas Maite (Casas-Ibáñez, one Michelin star) run all the hotel's food offering."), c.link("proyecto"), t("Conoce el proyecto", "Read our story"), False),
            (t("Después, a la azotea", "Then, up to the rooftop"), t("Para la sobremesa o el atardecer, sube a Cañitas al Fresco, el rooftop del hotel. Sin reserva.", "For a long afternoon or sunset drinks, head up to Cañitas al Fresco, the hotel rooftop. No booking needed."), c.link("fresco"), "Cañitas al Fresco", True),
        ]),
        faq_block(c, faqs),
        more_links(c, "centro"),
        cta_band(c, t("Reserva en el centro de Málaga", "Book in Málaga old town"),
                 t("Elige día, hora y número de comensales y recibe la confirmación al momento.", "Choose the day, time and number of guests and get instant confirmation."),
                 book_actions(c)),
    ])
    return dict(
        nav_title=t("Restaurante en el centro de Málaga", "Restaurant in Málaga old town"),
        title=t("Restaurante en el centro de Málaga | Cañitas Málaga", "Restaurant in Málaga Old Town | Cañitas Málaga"),
        desc=t("Restaurante en el centro histórico de Málaga, junto a la Plaza de la Merced: producto y brasa con vistas a la Alcazaba. Menús desde 39 €. Reserva online.",
               "Restaurant in Málaga old town by Plaza de la Merced: grill and great produce with views of the Alcazaba. Sharing menus from €39. Book online."),
        main=main,
        schema=[restaurant_ld(c), faq_ld(faqs), breadcrumb_ld(c, t("Restaurante en el centro de Málaga", "Restaurant in Málaga old town"))],
    )


# ---------------------------------------------------------------------------
def donde(c):
    t = c.t
    faqs = [
        (t("¿Cuáles son los mejores restaurantes de Málaga?", "What are the best restaurants in Málaga?"),
         t("Depende de lo que busques. Para pescado frente al mar, los espetos de Pedregalejo y El Palo; para tapas, el centro histórico y el Soho; para cocina de producto y brasa con vistas a la Alcazaba, Cañitas Málaga, en la última planta del hotel ME Málaga by Meliá.",
           "It depends on what you are after. For fish by the sea, the sardine espetos of Pedregalejo and El Palo; for tapas, the old town and Soho; for produce-led grill cooking with views of the Alcazaba, Cañitas Málaga, on the top floor of ME Málaga by Meliá.")),
        (t("¿A qué hora se come en Málaga?", "What time do people eat in Málaga?"),
         t("Como en el resto de España, se come tarde: el almuerzo suele ser entre las 13:30 y las 16:00 y la cena a partir de las 20:30. En temporada alta conviene reservar.",
           "As in the rest of Spain, people eat late: lunch is usually between 1:30 pm and 4 pm, and dinner from 8:30 pm. In high season it is worth booking.")),
        (t("¿Qué es típico comer en Málaga?", "What is typical food in Málaga?"),
         t("Espetos de sardinas, boquerones (fritos o en vinagre), pescaíto frito, ensaladilla, ajoblanco y porra antequerana, todo ello acompañado de un vino dulce de Málaga.",
           "Sardine espetos, anchovies (fried or marinated), fried fish, Russian salad, ajoblanco and porra antequerana, all with a glass of sweet Málaga wine.")),
        (t("¿Hace falta reservar para comer en el centro?", "Do I need to book in the city centre?"),
         t(f'En los restaurantes más conocidos del centro, sí, especialmente en fin de semana. En Cañitas Málaga puedes <a href="{c.link("reservas")}">reservar online</a> y recibir la confirmación al momento.',
           f'At the best-known places in the centre, yes, especially at weekends. At Cañitas Málaga you can <a href="{c.link("reservas")}">book online</a> and get instant confirmation.')),
    ]
    zones = [
        (t("Centro histórico", "Old town"), t("Tapas clásicas, tabernas y cocina de autor entre la Catedral, la Plaza de la Merced y la Alcazaba. Aquí está Cañitas Málaga.", "Classic tapas, taverns and chef-driven cooking between the Cathedral, Plaza de la Merced and the Alcazaba. This is where Cañitas Málaga is."), c.link("centro"), t("Comer en el centro", "Eating in the centre"), False),
        (t("Soho y Muelle Uno", "Soho and Muelle Uno"), t("El barrio de las artes y el puerto: cocina más internacional, cafés y paseos junto al mar.", "The arts district and the port: more international food, cafés and seaside walks."), "", "", False),
        (t("Pedregalejo y El Palo", "Pedregalejo and El Palo"), t("Los barrios marineros del este: chiringuitos, espetos de sardinas y pescaíto frito con los pies en la arena.", "The old fishing quarters to the east: beach bars, sardine espetos and fried fish with your feet in the sand."), "", "", False),
        (t("Azoteas", "Rooftops"), t("Málaga se disfruta desde arriba. Para picar y tomar algo al atardecer con la Alcazaba enfrente, Cañitas al Fresco.", "Málaga is best seen from above. For sunset drinks and bites facing the Alcazaba, Cañitas al Fresco."), c.link("rooftop"), t("Rooftop en Málaga", "Rooftop bar in Málaga"), True),
    ]
    hero = page_hero(c, t("Guía de la casa", "Our guide"), t("Dónde comer en Málaga", "Where to eat in Málaga"),
                     t("Qué es típico, a qué hora se come, qué zonas merecen la pena y dónde encaja Cañitas Málaga si buscas cocina de producto en el centro.",
                       "What is typical, when people eat, which areas are worth it and where Cañitas Málaga fits in if you are looking for great produce in the city centre."),
                     photo="mejor-croqueta-del-mundo-jamon-joselito", actions=book_actions(c),
                     crumbs=[t("Dónde comer en Málaga", "Where to eat in Málaga")])
    main = "\n\n".join([
        hero,
        split(c, t("Lo típico", "Local classics"), t("Qué comer en Málaga", "What to eat in Málaga"), [
            t("Málaga es ciudad de mar y de producto. Lo imprescindible: los espetos de sardinas asados en barca sobre la arena, los boquerones (fritos o en vinagre), el pescaíto frito, la ensaladilla, el ajoblanco y la porra antequerana. Para acompañar, un vino dulce de Málaga o un moscatel.",
              "Málaga is a city of sea and great produce. The essentials: sardine espetos grilled in boats on the sand, anchovies (fried or marinated), fried fish, Russian salad, ajoblanco and porra antequerana. To go with them, a glass of sweet Málaga wine or moscatel."),
            t("En Cañitas Málaga esa tradición del sur se cruza con la cocina manchega de Javier Sanz y Juan Sahuquillo: ensaladilla de gamba blanca malagueña, boquerón aliñado en casa, gamba roja al ajillo y mucha brasa.",
              "At Cañitas Málaga that southern tradition meets the La Mancha cooking of Javier Sanz and Juan Sahuquillo: Málaga white prawn Russian salad, house-marinated anchovies, red prawns al ajillo and plenty of embers."),
        ], extra=facts([
            (t("Almuerzo", "Lunch"), t("de 13:30 a 16:00, aproximadamente.", "roughly 1:30 pm to 4 pm.")),
            (t("Cena", "Dinner"), t("a partir de las 20:30.", "from 8:30 pm.")),
            (t("Reserva", "Booking"), t("recomendable en fin de semana y temporada alta.", "recommended at weekends and in high season.")),
        ])),
        cards(c, zones),
        gallery(c, [
            ("txuleta-vasca-parrilla-canitas-malaga", t("Txuleta vasca madurada a la parrilla", "Dry-aged Basque txuleta on the grill")),
            ("ensaladilla-gamba-blanca-canitas-al-fresco", t("Ensaladilla de gamba blanca malagueña", "Málaga white prawn Russian salad")),
            ("lubina-parrilla-pil-pil-canitas-malaga", t("Lubina del Atlántico con pil pil", "Atlantic sea bass with pil pil")),
            ("berenjena-burrata-canitas-malaga", t("Berenjena ahumada con burrata", "Smoked aubergine with burrata")),
            ("guacamole-casero-canitas-al-fresco", t("Picoteo en la azotea", "Bites on the rooftop")),
            ("lenguado-brasas-canitas-malaga", t("Lenguado asado en brasas", "Ember-roasted sole")),
        ]).replace('    <div class="gallery', '  <section class="section"><div class="section-inner">\n    <div class="gallery', 1) + "\n  </div></section>",
        faq_block(c, faqs),
        more_links(c, "donde"),
        cta_band(c, t("¿Comemos en el centro?", "Lunch in the centre?"),
                 t("Reserva tu mesa en Cañitas Málaga, en la última planta de ME Málaga by Meliá.", "Book your table at Cañitas Málaga, on the top floor of ME Málaga by Meliá."),
                 book_actions(c)),
    ])
    return dict(
        nav_title=t("Dónde comer en Málaga", "Where to eat in Málaga"),
        title=t("Dónde comer en Málaga | Guía y restaurante en el centro", "Where to Eat in Málaga | Local Guide & Old Town Restaurant"),
        desc=t("Qué comer en Málaga, a qué hora y en qué zonas, y dónde probar cocina de producto y brasa con vistas a la Alcazaba en el centro. Guía de Cañitas Málaga.",
               "What to eat in Málaga, when and where, plus where to try grill-led cooking with Alcazaba views in the old town. A local guide by Cañitas Málaga."),
        main=main,
        schema=[faq_ld(faqs), breadcrumb_ld(c, t("Dónde comer en Málaga", "Where to eat in Málaga"))],
    )


# ---------------------------------------------------------------------------
def cenar(c):
    t = c.t
    faqs = [
        (t("¿Es un buen restaurante para una cena romántica en Málaga?", "Is it a good place for a romantic dinner in Málaga?"),
         t("Sí: la sala y la terraza de la última planta, la luz cálida y las vistas a la Alcazaba iluminada hacen de Cañitas Málaga un buen plan para cenar en pareja.",
           "Yes: the top-floor dining room and terrace, warm lighting and views of the floodlit Alcazaba make Cañitas Málaga a great choice for dinner for two.")),
        (t("¿Podemos cenar en grupo?", "Can we have dinner as a group?"),
         t(f'Sí. Las mesas de 8 o más tienen menú cerrado y disponemos de comedor privado. Mira <a href="{c.link("grupos")}">Grupos y eventos</a> o escríbenos a {EMAIL}.',
           f'Yes. Tables of 8 or more have a set menu and we have a private dining room. See <a href="{c.link("grupos")}">Groups & events</a> or email us at {EMAIL}.')),
        (t("¿Cuánto cuesta cenar?", "How much does dinner cost?"),
         t("El Menú Classics cuesta 39 € por persona (de lunes a jueves) y el Menú Hits 69 € por persona (todos los días). También puedes pedir a la carta.",
           "The Classics Menu is €39 per person (Monday to Thursday) and the Hits Menu €69 per person (every day). You can also order à la carte.")),
        (t("¿Cómo reservo para cenar?", "How do I book dinner?"),
         t(f'Desde la página <a href="{c.link("reservas")}">Reservar mesa</a>, eligiendo día, hora y número de comensales.',
           f'On our <a href="{c.link("reservas")}">Book a table</a> page, choosing the day, time and number of guests.')),
    ]
    hero = page_hero(c, t("Cenas en la última planta", "Dinner on the top floor"), t("Dónde cenar en Málaga centro", "Dinner in Málaga city centre"),
                     t("Cena con la Alcazaba iluminada enfrente, cocina de brasa y menús para compartir en la última planta del hotel ME Málaga by Meliá.",
                       "Dinner facing the floodlit Alcazaba, grill cooking and sharing menus on the top floor of ME Málaga by Meliá."),
                     photo="canitas-malaga-comedor-privado-horizontal", actions=book_actions(c),
                     crumbs=[t("Dónde cenar en Málaga", "Dinner in Málaga")])
    main = "\n\n".join([
        hero,
        split(c, t("La cena", "Dinner"), t("Una cena con vistas en el centro de Málaga", "Dinner with a view in central Málaga"), [
            t("Cuando cae la tarde, la Alcazaba y Gibralfaro se iluminan y la última planta de ME Málaga se convierte en uno de los sitios más especiales para cenar en el centro. La cocina de Cañitas Málaga manda en la mesa: crudos y conservas para empezar, verduras a la brasa, pescados enteros y carnes maduradas a la parrilla.",
              "As evening falls, the Alcazaba and Gibralfaro light up and the top floor of ME Málaga becomes one of the most special places for dinner in the centre. Cañitas Málaga cooking takes centre stage: raw and cured bites to start, ember-roasted vegetables, whole fish and dry-aged meat from the grill."),
            t("Para cenas entre semana, el Menú Classics (39 €, de lunes a jueves) es la forma más sencilla de probar la casa. Para una ocasión especial, el Menú Hits (69 €) incluye la croqueta, la lubina o la txuleta y el flan de nata de oveja.",
              "For midweek dinners, the Classics Menu (€39, Monday to Thursday) is the easiest way to taste the house. For a special occasion, the Hits Menu (€69) includes the croquette, the sea bass or the txuleta, and the sheep's cream flan."),
        ]),
        cards(c, [
            (t("Cena en pareja", "Dinner for two"), t("Sala cálida, terraza acristalada y vistas al casco histórico.", "A warm dining room, glass-roofed terrace and old-town views."), c.link("vistas"), t("Restaurante con vistas", "Restaurant with a view"), False),
            (t("Cena de grupo", "Group dinners"), t("Menú cerrado para 8 o más y comedor privado.", "Set menu for 8 or more and a private dining room."), c.link("grupos"), t("Grupos y eventos", "Groups & events"), False),
            (t("La carta", "The menu"), t("Parrilla, producto y menús para compartir, en español e inglés.", "Grill, great produce and sharing menus, in English and Spanish."), c.link("carta", anchor="canitas-malaga"), t("Ver la carta", "See the menu"), False),
        ]),
        faq_block(c, faqs),
        more_links(c, "cenar"),
        cta_band(c, t("Reserva tu cena", "Book your dinner"),
                 t("Mesa en la última planta de ME Málaga by Meliá, con confirmación al momento.", "A table on the top floor of ME Málaga by Meliá, with instant confirmation."),
                 book_actions(c)),
    ])
    return dict(
        nav_title=t("Dónde cenar en Málaga", "Dinner in Málaga"),
        title=t("Dónde cenar en Málaga centro | Cañitas Málaga", "Dinner in Málaga City Centre | Cañitas Málaga"),
        desc=t("Cena en el centro de Málaga con la Alcazaba iluminada: cocina de brasa, menús para compartir desde 39 € y comedor privado para grupos. Reserva online.",
               "Dinner in central Málaga facing the floodlit Alcazaba: grill cooking, sharing menus from €39 and a private dining room for groups. Book online."),
        main=main,
        schema=[restaurant_ld(c), faq_ld(faqs), breadcrumb_ld(c, t("Dónde cenar en Málaga", "Dinner in Málaga"))],
    )


# ---------------------------------------------------------------------------
def vistas(c):
    t = c.t
    faqs = [
        (t("¿Qué se ve desde Cañitas Málaga?", "What can you see from Cañitas Málaga?"),
         t("La Alcazaba y el castillo de Gibralfaro casi a la altura de la mesa, además de la Catedral y los tejados del centro histórico.",
           "The Alcazaba and Gibralfaro castle almost at table height, plus the Cathedral and the rooftops of the old town.")),
        (t("¿Cuándo es el mejor momento?", "When is the best time?"),
         t("Al atardecer y por la noche, cuando la Alcazaba se ilumina. Para comer, la terraza acristalada tiene luz natural todo el día.",
           "At sunset and at night, when the Alcazaba is floodlit. For lunch, the glass-roofed terrace has natural light all day.")),
        (t("¿Puedo pedir una mesa concreta?", "Can I request a specific table?"),
         t(f"Indícalo al hacer tu reserva o escríbenos a {EMAIL} y haremos lo posible.",
           f"Mention it when you book or email us at {EMAIL} and we will do our best.")),
        (t("¿También hay vistas sin reserva?", "Are there views without booking?"),
         t(f'Sí: <a href="{c.link("fresco")}">Cañitas al Fresco</a>, en la azotea, mira directamente a la Alcazaba y no admite reservas.',
           f'Yes: <a href="{c.link("fresco")}">Cañitas al Fresco</a>, on the rooftop, looks straight at the Alcazaba and does not take reservations.')),
    ]
    hero = page_hero(c, t("Última planta · ME Málaga by Meliá", "Top floor · ME Málaga by Meliá"), t("Restaurante con vistas a la Alcazaba", "Restaurant with Alcazaba views"),
                     t("Come o cena frente a la Alcazaba y Gibralfaro, en la última planta del hotel ME Málaga by Meliá, en el centro de Málaga.",
                       "Lunch or dinner facing the Alcazaba and Gibralfaro, on the top floor of ME Málaga by Meliá in Málaga city centre."),
                     photo="canitas-malaga-terraza", actions=book_actions(c),
                     crumbs=[t("Restaurante con vistas en Málaga", "Restaurant with a view in Málaga")])
    main = "\n\n".join([
        hero,
        split(c, t("Las vistas", "The views"), t("La Alcazaba, casi al alcance de la mano", "The Alcazaba, almost within reach"), [
            t("Pocos restaurantes de Málaga miran a la Alcazaba desde tan cerca. Desde la última planta de ME Málaga by Meliá, la fortaleza y el castillo de Gibralfaro aparecen casi a la altura de la mesa, con la Catedral y los tejados del centro histórico alrededor.",
              "Few restaurants in Málaga look at the Alcazaba from so close. From the top floor of ME Málaga by Meliá, the fortress and Gibralfaro castle appear almost at table height, with the Cathedral and the old-town rooftops all around."),
            t("De día, la terraza acristalada con olivos se llena de luz; de noche, la Alcazaba iluminada convierte la cena en el plan más especial del centro.",
              "By day, the glass-roofed terrace with its olive trees fills with light; at night, the floodlit Alcazaba makes dinner the most special plan in the centre."),
        ]),
        f"""  <section class="section section-tint">
    <div class="section-inner">
      <div class="space-cards">
        <article class="space-card">{c.img("canitas-malaga-terraza-mesas", sizes="(max-width: 860px) 92vw, 32vw")}<h3>{t('La terraza', 'The terrace')}</h3><p>{t('Acristalada, con olivos y luz natural.', 'Glass-roofed, with olive trees and natural light.')}</p></article>
        <article class="space-card">{c.img("me-malaga-terraza-alcazaba", sizes="(max-width: 860px) 92vw, 32vw")}<h3>{t('La Alcazaba', 'The Alcazaba')}</h3><p>{t('La fortaleza y Gibralfaro, frente a ti.', 'The fortress and Gibralfaro, right in front of you.')}</p></article>
        <article class="space-card brand-fresco">{c.img("canitas-al-fresco-rooftop-piscina-malaga", sizes="(max-width: 860px) 92vw, 32vw")}<h3>{t('La azotea', 'The rooftop')}</h3><p>{t('Cañitas al Fresco: vistas sin reserva.', 'Cañitas al Fresco: views with no booking needed.')} <a href="{c.link('rooftop')}">{t('Rooftop en Málaga', 'Rooftop bar in Málaga')} →</a></p></article>
      </div>
    </div>
  </section>""",
        faq_block(c, faqs),
        more_links(c, "vistas"),
        cta_band(c, t("Reserva una mesa con vistas", "Book a table with a view"),
                 t("Cañitas Málaga, última planta de ME Málaga by Meliá, Calle Victoria 6.", "Cañitas Málaga, top floor of ME Málaga by Meliá, Calle Victoria 6."),
                 book_actions(c)),
    ])
    return dict(
        nav_title=t("Restaurante con vistas en Málaga", "Restaurant with a view in Málaga"),
        title=t("Restaurante con vistas en Málaga | Alcazaba · Cañitas Málaga", "Restaurant with a View in Málaga | Alcazaba · Cañitas Málaga"),
        desc=t("Restaurante con vistas a la Alcazaba y Gibralfaro en el centro de Málaga: terraza en la última planta de ME Málaga by Meliá. Cocina de brasa. Reserva online.",
               "Restaurant with views of the Alcazaba and Gibralfaro in central Málaga: top-floor terrace at ME Málaga by Meliá. Grill cooking. Book online."),
        main=main,
        schema=[restaurant_ld(c), faq_ld(faqs), breadcrumb_ld(c, t("Restaurante con vistas en Málaga", "Restaurant with a view in Málaga"))],
    )


# ---------------------------------------------------------------------------
def rooftop(c):
    t = c.t
    faqs = [
        (t("¿Hay que reservar en Cañitas al Fresco?", "Do I need to book at Cañitas al Fresco?"),
         t("No. El rooftop no admite reservas: el acceso es por orden de llegada. Al atardecer es el momento con más ambiente, así que conviene subir con tiempo.",
           "No. The rooftop does not take reservations: entry is first come, first served. Sunset is the busiest time, so come up early.")),
        (t("¿Puedo usar la piscina?", "Can I use the pool?"),
         t("La piscina de la azotea es exclusiva para los huéspedes del hotel ME Málaga. El rooftop bar Cañitas al Fresco, en cambio, está abierto a todo el público.",
           "The rooftop pool is reserved for ME Málaga hotel guests. The Cañitas al Fresco rooftop bar, however, is open to everyone.")),
        (t("¿Se puede comer en la azotea?", "Can I eat on the rooftop?"),
         t(f'Sí. Hay entrantes, bocatería fina y dulces: guacamole casero, ensaladilla de gamba blanca, tartar de atún rojo, burger de vaca gallega… Mira <a href="{c.link("carta", anchor="canitas-al-fresco")}">la carta</a>.',
           f'Yes. There are starters, gourmet sandwiches and sweets: homemade guacamole, white prawn Russian salad, bluefin tuna tartare, Galician beef burger… See <a href="{c.link("carta", anchor="canitas-al-fresco")}">the menu</a>.')),
        (t("¿Dónde está?", "Where is it?"),
         t("En la azotea del hotel ME Málaga by Meliá, Calle Victoria 6, junto a la Plaza de la Merced, en el centro de Málaga.",
           "On the rooftop of ME Málaga by Meliá, Calle Victoria 6, next to Plaza de la Merced, in Málaga city centre.")),
        (t("¿La carta está en inglés?", "Is the menu in English?"),
         t("Sí, tenemos la carta en español y en inglés, en la azotea y en la web.", "Yes, the menu is available in English and Spanish, on the rooftop and online.")),
    ]
    hero = page_hero(c, t("Azotea · ME Málaga by Meliá", "Rooftop · ME Málaga by Meliá"), t("Rooftop en Málaga centro", "Rooftop bar in Málaga"),
                     t("Cañitas al Fresco es el rooftop del hotel ME Málaga by Meliá: cócteles, picoteo y atardeceres frente a la Alcazaba, en pleno centro. Sin reserva.",
                       "Cañitas al Fresco is the rooftop bar at ME Málaga by Meliá: cocktails, bites and sunsets facing the Alcazaba, right in the city centre. No booking needed."),
                     photo="canitas-al-fresco-rooftop-piscina-malaga",
                     actions=f'<a class="btn btn-primary-light" href="{c.link("carta", anchor="canitas-al-fresco")}">{t("Ver la carta", "See the menu")}</a>' + menu_lang(c, "fresco", light=True),
                     crumbs=[t("Rooftop en Málaga", "Rooftop bar in Málaga")])
    main = "\n\n".join([
        hero,
        split(c, t("La azotea", "The rooftop"), t("Atardeceres frente a la Alcazaba", "Sunsets facing the Alcazaba"), [
            t("Málaga se vive desde las azoteas, y pocas tienen la Alcazaba tan de frente. Cañitas al Fresco ocupa la azotea del hotel ME Málaga by Meliá, junto a la Plaza de la Merced: barra, mesas al aire libre y una vista que va de la fortaleza a la Catedral y al puerto.",
              "Málaga is best enjoyed from its rooftops, and few face the Alcazaba so directly. Cañitas al Fresco sits on the rooftop of ME Málaga by Meliá, next to Plaza de la Merced: a bar, open-air tables and a view that runs from the fortress to the Cathedral and the port."),
            t("Coctelería de autor y una carta para picar firmada por Cañitas Málaga: la croqueta de jamón Joselito, guacamole casero, ensaladilla de gamba blanca, bikini trufado o burger de vaca gallega.",
              "Signature cocktails and a grazing menu by Cañitas Málaga: the Joselito ham croquette, homemade guacamole, white prawn Russian salad, truffled bikini toastie or Galician beef burger."),
        ], extra=facts([
            (t("Horario", "Opening hours"), hours_text(c.lang, "fresco") + "."),
            (t("Sin reserva", "No booking"), t("abierto al público, por orden de llegada.", "open to the public, first come, first served.")),
            (t("Piscina", "Pool"), t("exclusiva para huéspedes del hotel.", "reserved for hotel guests.")),
            (t("Mejor momento", "Best time"), t("el atardecer.", "sunset.")),
            (t("Carta", "Menu"), t("en español e inglés.", "in English and Spanish.")),
        ])),
        gallery(c, [
            ("guacamole-casero-canitas-al-fresco", t("Guacamole casero con totopos", "Homemade guacamole with tortilla chips")),
            ("hamburguesa-vaca-gallega-canitas-al-fresco", t("Burger de vaca gallega", "Galician beef burger")),
            ("ensaladilla-gamba-blanca-canitas-al-fresco", t("Ensaladilla junto a la piscina", "Russian salad by the pool")),
            ("hummus-crudites-canitas-al-fresco", t("Hummus y torta de aceite", "Hummus and olive oil flatbread")),
            ("ensalada-cesar-canitas-al-fresco", t("Ensalada César", "Caesar salad")),
            ("tarta-de-queso-canitas-al-fresco", t("Tarta de queso", "Cheesecake")),
        ]).replace('    <div class="gallery', '  <section class="section section-tint"><div class="section-inner">\n    <div class="gallery', 1) + "\n  </div></section>",
        faq_block(c, faqs),
        more_links(c, "rooftop"),
        cta_band(c, t("Sube a la azotea", "Come up to the rooftop"),
                 t("Sin reserva: te esperamos en la azotea de ME Málaga by Meliá, Calle Victoria 6.", "No booking needed: see you on the rooftop of ME Málaga by Meliá, Calle Victoria 6."),
                 f'<a class="btn btn-primary-light" href="{c.link("fresco")}">Cañitas al Fresco</a><a class="btn btn-ghost-light" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")} ↗</a>'),
    ])
    return dict(
        nav_title=t("Rooftop en Málaga", "Rooftop bar in Málaga"),
        title=t("Rooftop en Málaga centro | Cañitas al Fresco", "Rooftop Bar in Málaga | Cañitas al Fresco, Alcazaba Views"),
        desc=t("Rooftop en el centro de Málaga frente a la Alcazaba: cócteles, picoteo y atardeceres en la azotea de ME Málaga by Meliá. Sin reserva. Carta en español e inglés.",
               "Rooftop bar in Málaga city centre facing the Alcazaba: cocktails, bites and sunsets on top of ME Málaga by Meliá. No booking needed. English menu."),
        main=main,
        og="og-canitas-al-fresco",
        theme="brand-fresco",
        schema=[fresco_ld(c), faq_ld(faqs), breadcrumb_ld(c, t("Rooftop en Málaga", "Rooftop bar in Málaga"))],
    )


PAGES = {"centro": centro, "donde": donde, "cenar": cenar, "vistas": vistas, "rooftop": rooftop}
LABELS = [
    ("centro", "Restaurante en el centro de Málaga", "Restaurant in Málaga old town"),
    ("donde", "Dónde comer en Málaga", "Where to eat in Málaga"),
    ("cenar", "Dónde cenar en Málaga", "Dinner in Málaga"),
    ("vistas", "Restaurante con vistas", "Restaurant with a view"),
    ("rooftop", "Rooftop en Málaga", "Rooftop bar in Málaga"),
]
