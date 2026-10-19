"""Desayunos/brunch y eventos de empresa (ES / EN); sus subpáginas SEO están en seo_pages.py. Están en la cabecera junto al
restaurante y el rooftop. No llevan la carta ni los precios: cuentan el plan y
llevan al contacto.

  desayunos-brunch-malaga   desayuno / brunch Málaga centro, abierto a quien no se aloja
  eventos-empresa-malaga    eventos de empresa, rooftop privatizable, salas interiores

Fuentes: DESAYUNOS_CAÑITASMAITEXMELIA.pdf, cartelitos y A5 de productores (desayunos);
EVENTOS2_CAÑITASMAITE.pdf y ALFRESCO_EVENTOS.pdf (eventos).
"""
from build import EMAIL, MAPS, PHONE, PHONE_TEL, breadcrumb_ld, page_hero, restaurant_ld
from landings import cards, facts, faq_block, faq_ld, split
from pages import cta_band, gallery, mailto



DESAYUNOS_SUB = ("brunch", "desayunar", "hotelbreakfast")
EVENTOS_SUB = ("cenaempresa", "navidad", "rooftopeventos", "reuniones")


def related_block(c, keys, title):
    """Enlaces a las subpáginas (fuera del menú) de desayunos o eventos."""
    import seo_pages
    lis = "".join(f'<li><a href="{c.link(k)}">{seo_pages.LABEL[k](c)}</a></li>' for k in keys)
    return f"""  <section class="section">
    <div class="section-inner">
      <nav class="related" aria-label="{title}">
        <p class="eyebrow eyebrow-dark">{title}</p>
        <ul>{lis}</ul>
      </nav>
    </div>
  </section>"""


def section(inner, tint=False, extra_cls=""):
    cls = "section" + (" section-tint" if tint else "") + (f" {extra_cls}" if extra_cls else "")
    return f"""  <section class="{cls}">
    <div class="section-inner">
{inner}
    </div>
  </section>"""


def head(eyebrow, title, intro=""):
    intro = f'\n        <p class="section-intro">{intro}</p>' if intro else ""
    return f"""      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{eyebrow}</p>
        <h2 class="section-title">{title}</h2>{intro}
      </div>"""


def tiles(items):
    """Lista de bloques con título y texto (estaciones del buffet, formatos de evento)."""
    lis = "\n".join(f'        <li class="tile"><h3>{h}</h3><p>{p}</p></li>' for h, p in items)
    return f'      <ul class="tiles">\n{lis}\n      </ul>'


# ---------------------------------------------------------------------------
def desayunos(c):
    t = c.t
    subject = t("Desayuno en ME Málaga — Cañitas Maite", "Breakfast at ME Málaga — Cañitas Maite")
    actions = (f'<a class="btn btn-primary-light" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")} ↗</a>'
               f'<a class="btn btn-ghost-light" href="tel:{PHONE_TEL}">{t("Llámanos", "Call us")}</a>')
    hero = page_hero(c, t("Hotel ME Málaga · Calle Victoria 6", "ME Málaga hotel · Calle Victoria 6"),
                     t("Desayuno & brunch en el centro de Málaga", "Breakfast & brunch in Málaga old town"),
                     t("El desayuno de productores locales de Cañitas Maite, en el hotel ME Málaga by Meliá. Abierto a todo el mundo: no hace falta alojarse en el hotel para venir a desayunar.",
                       "The Cañitas Maite local-producer breakfast at ME Málaga by Meliá. Open to everyone: you don't need to stay at the hotel to come for breakfast."),
                     photo="desayuno-buffet-productores-locales-malaga", actions=actions,
                     crumbs=[t("Desayunos", "Breakfast")])
    stations = [
        (t("Panes de masa madre", "Sourdough breads"), t("Hogazas de fermentación lenta, tortas y molletes de obradores artesanos.", "Slow-fermented loaves, flatbreads and molletes from artisan bakeries.")),
        (t("Bollería y dulces de aquí", "Pastries and local sweets"), t("Bollería tradicional de pequeños obradores y los dulces típicos de la zona.", "Traditional pastries from small bakeries and the area's classic sweets.")),
        (t("Quesos de granja", "Farm cheeses"), t("Quesos artesanos de granjas de nuestro entorno.", "Artisan cheeses from farms close to home.")),
        (t("Chacinas de pueblo", "Village charcuterie"), t("Chacinas y embutidos caseros de las carnicerías de nuestros pueblos.", "Home-style cured meats and sausages from village butchers.")),
        (t("Fruta de la provincia", "Fruit from the province"), t("Fruta local de temporada, aceite de olivos centenarios, miel y complementos top.", "Local seasonal fruit, oil from century-old olive trees, honey and top condiments.")),
        (t("Bebidas hechas en casa", "House-made drinks"), t("Zumos, cafés e infusiones para empezar el día sin prisa.", "Juices, coffee and teas to start the day slowly.")),
        (t("Huevos de Coín al momento", "Coín eggs cooked to order"), t("Huevos camperos de Coín: poché, fritos, benedict o en tortilla, hechos en el momento.", "Free-range eggs from Coín: poached, fried, Benedict or as an omelette, cooked to order.")),
        (t("Lo que se les ocurra a los chefs", "Whatever the chefs come up with"), t("Una zona de calientes a nuestra manera y algunos caprichos: huevos rotos con jamón Joselito, tortitas, bowl de açaí…", "A hot station done our way and a few treats: broken eggs with Joselito ham, pancakes, açaí bowls…")),
    ]
    faqs = [
        (t("¿Puedo desayunar en el ME Málaga sin estar alojado?", "Can I have breakfast at ME Málaga if I'm not staying there?"),
         t("Sí. El desayuno de Cañitas Maite está abierto a todo el mundo, no solo a los huéspedes del hotel. Solo tienes que venir a Calle Victoria 6.",
           "Yes. The Cañitas Maite breakfast is open to everyone, not only hotel guests. Just come to Calle Victoria 6.")),
        (t("¿Qué tiene de especial este desayuno?", "What makes this breakfast special?"),
         t("Está hecho con pequeños productores: panes de masa madre, quesos de granjas locales, chacinas de carnicerías de pueblo, fruta de la provincia y bollería de obradores de la zona, más huevos camperos de Coín hechos al momento.",
           "It is built on small producers: sourdough breads, cheeses from local farms, charcuterie from village butchers, fruit from the province and pastries from local bakeries, plus free-range Coín eggs cooked to order.")),
        (t("¿Es un brunch?", "Is it a brunch?"),
         t("Es un desayuno largo y sin prisa, con buffet de producto y platos calientes al momento: lo que mucha gente busca cuando dice brunch, en pleno centro de Málaga.",
           "It is a long, unhurried breakfast with a produce buffet and hot dishes cooked to order: what many people mean by brunch, right in central Málaga.")),
        (t("¿Se puede regalar?", "Can I give it as a gift?"),
         t(f'Sí, tenemos tarjeta regalo de desayuno para dos personas. Mira <a href="{c.link("bonos")}">Bonos regalo</a> o escríbenos a {EMAIL}.',
           f'Yes, there is a breakfast gift card for two. See <a href="{c.link("bonos")}">Gift vouchers</a> or email us at {EMAIL}.')),
        (t("¿Venimos en grupo?", "Coming as a group?"),
         t(f'Escríbenos a <a href="{mailto(subject)}">{EMAIL}</a> o llámanos al {PHONE} y te lo preparamos. Para desayunos de trabajo y coffee breaks, mira <a href="{c.link("eventos")}">Eventos de empresa</a>.',
           f'Email us at <a href="{mailto(subject)}">{EMAIL}</a> or call {PHONE} and we will get it ready. For working breakfasts and coffee breaks, see <a href="{c.link("eventos")}">Corporate events</a>.')),
    ]
    main = "\n\n".join([
        hero,
        split(c, t("Un plan único en la ciudad", "One of a kind in the city"), t("No hace falta dormir aquí para desayunar aquí", "You don't need to sleep here to have breakfast here"), [
            t("Empezar el día en ME Málaga con el desayuno de Cañitas Maite es conocer nuestra casa: el cariño de Javier Sanz y Juan Sahuquillo puesto en un desayuno casero, de pequeños productores, como el que nos gustaría encontrar en cualquier ciudad.",
              "Starting the day at ME Málaga with the Cañitas Maite breakfast means getting to know our house: Javier Sanz and Juan Sahuquillo's care poured into a homemade breakfast from small producers, the kind we would love to find in any city."),
            t("Vecinos del centro, viajeros que duermen en otro sitio, gente que trabaja por la zona o quien quiere un brunch distinto el fin de semana: la puerta está abierta para todos, a un minuto de la Plaza de la Merced.",
              "Locals, travellers staying elsewhere, people working nearby or anyone after a different weekend brunch: the door is open to all, one minute from Plaza de la Merced."),
        ], extra=facts([
            (t("Dónde", "Where"), t("Hotel ME Málaga by Meliá, Calle Victoria 6, Málaga centro.", "ME Málaga by Meliá, Calle Victoria 6, Málaga old town.")),
            (t("Para quién", "Who for"), t("huéspedes y cualquiera que venga de fuera.", "hotel guests and anyone from outside.")),
            (t("Cocina", "Kitchen"), t("de los chefs de Cañitas Maite (Casas-Ibáñez, una estrella Michelin).", "by the Cañitas Maite chefs (Casas-Ibáñez, one Michelin star).")),
            ("MeliáRewards", t("puedes pagar con puntos.", "you can pay with points.")),
        ])),
        section(head(t("El buffet", "The buffet"), t("Lo que te espera por la mañana", "What awaits you in the morning"),
                     t("Un buffet de producto local y una cocina que hace los huevos al momento.", "A local-produce buffet and a kitchen cooking eggs to order.")) + "\n" + tiles(stations), tint=True),
        section(gallery(c, [
            ("desayuno-panes-masa-madre-malaga", t("Hogazas y panes de masa madre", "Sourdough loaves and breads")),
            ("desayuno-huevos-fritos-papada", t("Huevos fritos con puntilla y papada ibérica", "Crispy fried eggs with Iberian pork jowl")),
            ("desayuno-fruta-quesos-locales", t("Fruta de temporada y quesos de granja", "Seasonal fruit and farm cheeses")),
            ("desayuno-chacinas-embutidos", t("Chacinas y embutidos de pueblo", "Village charcuterie")),
            ("desayuno-platos-calientes-cazuelas", t("La zona de calientes", "The hot station")),
            ("desayuno-omelette-cremosa", t("Omelette hecha al momento", "Omelette cooked to order")),
        ])),
        related_block(c, DESAYUNOS_SUB, t("Más sobre el desayuno en Málaga", "More about breakfast in Málaga")),
        faq_block(c, faqs),
        cta_band(c, t("Mañana, desayuno en el centro", "Tomorrow, breakfast in the centre"),
                 t("Te esperamos en el hotel ME Málaga by Meliá, Calle Victoria 6, junto a la Plaza de la Merced.", "See you at ME Málaga by Meliá, Calle Victoria 6, next to Plaza de la Merced."),
                 f'<a class="btn btn-primary-light" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")} ↗</a>'
                 f'<a class="btn btn-ghost-light" href="{c.link("bonos")}">{t("Regalar un desayuno", "Give a breakfast")}</a>'),
    ])
    return dict(
        nav_title=t("Desayunos y brunch", "Breakfast & brunch"),
        title=t("Desayuno y brunch en Málaga centro | Cañitas Maite · ME Málaga",
                "Breakfast & Brunch in Málaga Old Town | Cañitas Maite · ME Málaga"),
        desc=t("Desayuno de productores locales en el hotel ME Málaga, abierto a todos: masa madre, quesos de granja, huevos de Coín al momento. Brunch en Calle Victoria 6.",
               "Local-producer breakfast at ME Málaga, open to non-guests: sourdough, farm cheeses, Coín eggs cooked to order. Brunch in Málaga old town, Calle Victoria 6."),
        main=main,
        schema=[restaurant_ld(c), faq_ld(faqs), breadcrumb_ld(c, t("Desayunos", "Breakfast"))],
    )


# ---------------------------------------------------------------------------
def eventos(c):
    t = c.t
    subject = t("Evento de empresa — Cañitas Maite · ME Málaga", "Corporate event — Cañitas Maite · ME Málaga")
    dossier = t("Dossier de eventos — Cañitas Maite · ME Málaga", "Events brochure — Cañitas Maite · ME Málaga")
    actions = (f'<a class="btn btn-primary-light" href="{mailto(dossier)}">{t("Pide el dossier", "Request the brochure")}</a>'
               f'<a class="btn btn-ghost-light" href="tel:{PHONE_TEL}">{PHONE}</a>')
    hero = page_hero(c, t("Empresas · ME Málaga by Meliá", "Companies · ME Málaga by Meliá"),
                     t("Eventos de empresa en Málaga", "Corporate events in Málaga"),
                     t("Reuniones, presentaciones, cócteles y cenas de gala en pleno centro, con la cocina de Cañitas Maite y un rooftop frente a la Alcazaba que preparamos solo para tu equipo.",
                       "Meetings, launches, cocktail receptions and gala dinners right in the city centre, with Cañitas Maite cooking and a rooftop facing the Alcazaba set up just for your team."),
                     photo="evento-empresa-rooftop-atardecer-malaga", actions=actions,
                     crumbs=[t("Eventos de empresa", "Corporate events")])
    spaces = f"""      <div class="space-cards space-cards-4">
        <article class="space-card brand-fresco">
          {c.img("evento-cocteles-alcazaba", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('El rooftop', 'The rooftop')}</h3>
          <p>{t('La azotea de Cañitas al Fresco, privatizada para tu empresa: cóctel al atardecer con la Alcazaba enfrente.', 'The Cañitas al Fresco rooftop, privatised for your company: sunset cocktails facing the Alcazaba.')}</p>
        </article>
        <article class="space-card">
          {c.img("canitas-malaga-terraza", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('Restaurante y terraza', 'Restaurant and terrace')}</h3>
          <p>{t('La sala y la terraza acristalada de la última planta, para menús sentados y cenas de gala.', 'The top-floor dining room and glass-roofed terrace, for seated menus and gala dinners.')}</p>
        </article>
        <article class="space-card">
          {c.img("canitas-malaga-comedor-privado", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('Comedor privado', 'Private dining room')}</h3>
          <p>{t('Una sola mesa a puerta cerrada para comités de dirección, comidas con clientes y reuniones discretas.', 'A single table behind closed doors for board lunches, client dinners and discreet meetings.')}</p>
        </article>
        <article class="space-card">
          {c.img("me-malaga-lobby-bar", sizes="(max-width: 860px) 92vw, 32vw")}
          <h3>{t('Salas interiores del hotel', 'Indoor hotel spaces')}</h3>
          <p>{t('Lobby bar y espacios interiores de ME Málaga para reuniones, coffee breaks y presentaciones.', 'The ME Málaga lobby bar and indoor spaces for meetings, coffee breaks and launches.')}</p>
        </article>
      </div>"""
    formats = [
        (t("Coffee break", "Coffee break"), t("Para reuniones y jornadas: café, zumos naturales y bollería de obrador, también en versión vegetariana. Desde 10 personas.", "For meetings and workshops: coffee, fresh juices and bakery pastries, with a vegetarian option too. From 10 guests.")),
        (t("Copa de bienvenida", "Welcome drinks"), t("Vinos, espumosos y aperitivo para abrir el evento, de 30 a 90 minutos. Desde 12 personas.", "Wines, sparkling wine and nibbles to open the event, 30 to 90 minutes. From 12 guests.")),
        (t("Cóctel y finger food", "Cocktail & finger food"), t("Bocados de la casa servidos de pie, con la mejor croqueta del mundo 2021. Desde 20 personas.", "House bites served standing, including the Best Croquette in the World 2021. From 20 guests.")),
        (t("Estaciones", "Food stations"), t("Vermutería, quesos de la zona, ibéricos con cortador, atún rojo, ostras o cocedero de marisco para completar el cóctel.", "Vermouth bar, local cheeses, Iberian ham carved on site, bluefin tuna, oysters or a seafood station to round off the cocktail.")),
        (t("Menús ejecutivos", "Business set menus"), t("Comida o cena sentada en 90 minutos, con opción vegetariana adaptable a veganos. Desde 40 personas.", "A seated lunch or dinner in 90 minutes, with a vegetarian option that can be made vegan. From 40 guests.")),
        (t("Cena de gala", "Gala dinner"), t("El gran formato: varios pases con producto de primera, menú vegetariano y menú infantil. Desde 40 personas.", "The full format: several courses of top produce, plus vegetarian and children's menus. From 40 guests.")),
        (t("Packs de bebida y barra libre", "Drinks packages & open bar"), t("Vinos de la casa, cerveza local y barra libre de dos horas para cerrar la noche. Barra libre desde 50 personas.", "House wines, local beer and a two-hour open bar to end the night. Open bar from 50 guests.")),
    ]
    faqs = [
        (t("¿Para cuántas personas organizáis eventos?", "How many guests can you host?"),
         t("Desde 10 personas en un coffee break hasta grandes cócteles y cenas de gala. Cuéntanos cuántos sois y te proponemos el espacio y el formato.",
           "From 10 guests for a coffee break up to large cocktail receptions and gala dinners. Tell us how many you are and we will suggest the space and format.")),
        (t("¿Se puede reservar el rooftop en exclusiva?", "Can we book the rooftop exclusively?"),
         t("Sí. Cañitas al Fresco se puede privatizar para eventos de empresa; consúltanos fechas y condiciones.",
           "Yes. Cañitas al Fresco can be privatised for corporate events; ask us about dates and conditions.")),
        (t("¿Tenéis opciones vegetarianas y veganas?", "Do you have vegetarian and vegan options?"),
         t("Sí: hay coffee break, cóctel, menú ejecutivo y cena de gala vegetarianos, y los menús se pueden adaptar a veganos y a cualquier alergia.",
           "Yes: there are vegetarian coffee breaks, cocktails, business menus and gala dinners, and menus can be adapted for vegans and any allergy.")),
        (t("¿Cómo se pide presupuesto?", "How do I get a quote?"),
         t(f'Escríbenos a <a href="{mailto(dossier)}">{EMAIL}</a> o llámanos al {PHONE} con la fecha, el número de personas y el tipo de evento. Te enviamos el dossier con todos los formatos y precios por persona, IVA incluido.',
           f'Email us at <a href="{mailto(dossier)}">{EMAIL}</a> or call {PHONE} with the date, number of guests and type of event. We will send you the brochure with every format and per-person prices, VAT included.')),
        (t("¿Los asistentes pueden alojarse en el hotel?", "Can attendees stay at the hotel?"),
         t("Sí, el evento se celebra en el hotel de cinco estrellas ME Málaga by Meliá, en Calle Victoria 6, en pleno centro de Málaga.",
           "Yes, the event takes place at the five-star ME Málaga by Meliá, Calle Victoria 6, right in the centre of Málaga.")),
    ]
    main = "\n\n".join([
        hero,
        split(c, t("Por qué aquí", "Why here"), t("Un evento que tu equipo va a recordar", "An event your team will remember"), [
            t("Cañitas Maite firma toda la oferta gastronómica del hotel ME Málaga by Meliá: la cocina de Javier Sanz y Juan Sahuquillo, con estrella Michelin en Casas-Ibáñez, al servicio de tu empresa en pleno centro de Málaga.",
              "Cañitas Maite runs all the food at ME Málaga by Meliá: the cooking of Javier Sanz and Juan Sahuquillo, Michelin-starred in Casas-Ibáñez, at your company's service in the heart of Málaga."),
            t("Preparamos el rooftop, la terraza, el comedor privado o los espacios interiores del hotel según el formato, y nos ocupamos de todo: cocina, bebida, servicio y tiempos.",
              "We set up the rooftop, the terrace, the private dining room or the hotel's indoor spaces to suit the format, and take care of everything: food, drinks, service and timings."),
        ], extra=facts([
            (t("Dónde", "Where"), t("Hotel ME Málaga by Meliá, Calle Victoria 6, a un minuto de la Plaza de la Merced.", "ME Málaga by Meliá, Calle Victoria 6, a minute from Plaza de la Merced.")),
            (t("Para", "For"), t("reuniones, presentaciones, incentivos, cenas de empresa y Navidad.", "meetings, launches, incentives, company dinners and Christmas parties.")),
            (t("Desde", "From"), t("10 personas.", "10 guests.")),
        ])),
        section(head(t("Los espacios", "The spaces"), t("Arriba, al aire libre o a puerta cerrada", "Up top, in the open air or behind closed doors")) + "\n" + spaces, tint=True),
        section(head(t("Formatos", "Formats"), t("Del primer café a la última copa", "From the first coffee to the last drink"),
                     t("Combina los formatos que necesites. Precios por persona con IVA incluido en el dossier.", "Mix and match the formats you need. Per-person prices, VAT included, in the brochure.")) + "\n" + tiles(formats)),
        section(gallery(c, [
            ("evento-mesa-finger-food", t("Mesa de quesos, panes y finger food", "Cheese, bread and finger food table")),
            ("evento-croquetas-pase", t("La mejor croqueta del mundo, en pase", "The world's best croquette, passed around")),
            ("evento-coffee-break", t("Coffee break con bollería de obrador", "Coffee break with bakery pastries")),
        ]), tint=True),
        f"""  <section class="section">
    <div class="section-inner">
{head(t('Cómo funciona', 'How it works'), t('Tu evento en tres pasos', 'Your event in three steps'))}
      <ol class="steps">
        <li><span class="steps-index">01</span><h3>{t('Cuéntanos', 'Tell us')}</h3><p>{t('Fecha, hora, número de personas y tipo de evento.', 'Date, time, number of guests and type of event.')}</p></li>
        <li><span class="steps-index">02</span><h3>{t('Recibe la propuesta', 'Get our proposal')}</h3><p>{t('Te enviamos el dossier con espacios, formatos y presupuesto.', 'We send the brochure with spaces, formats and a quote.')}</p></li>
        <li><span class="steps-index">03</span><h3>{t('Nosotros nos ocupamos', 'We handle the rest')}</h3><p>{t('Cerramos menú, tiempos, bebidas y alergias, y el día del evento solo tienes que disfrutar.', 'We finalise menu, timings, drinks and allergies; on the day, you just enjoy it.')}</p></li>
      </ol>
    </div>
  </section>""",
        related_block(c, EVENTOS_SUB, t("Más sobre eventos en Málaga", "More about events in Málaga")),
        faq_block(c, faqs),
        cta_band(c, t("¿Tienes una fecha?", "Got a date?"),
                 t(f'Escríbenos a <a href="{mailto(subject)}">{EMAIL}</a> o llámanos al <a href="tel:{PHONE_TEL}">{PHONE}</a>.',
                   f'Email us at <a href="{mailto(subject)}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a>.'),
                 f'<a class="btn btn-primary-light" href="{mailto(dossier)}">{t("Pide el dossier", "Request the brochure")}</a>'
                 f'<a class="btn btn-ghost-light" href="{c.link("grupos")}">{t("Grupos en el restaurante", "Groups at the restaurant")}</a>'),
    ])
    return dict(
        nav_title=t("Eventos de empresa", "Corporate events"),
        title=t("Eventos de empresa en Málaga | Rooftop y salas · Cañitas Maite",
                "Corporate Events in Málaga | Rooftop Venue · Cañitas Maite"),
        desc=t("Eventos de empresa en el hotel ME Málaga: rooftop privatizable frente a la Alcazaba, salas interiores, coffee breaks, cócteles y cenas de gala. Pide el dossier.",
               "Corporate events at ME Málaga: a private rooftop facing the Alcazaba, indoor spaces, coffee breaks, cocktail receptions and gala dinners. Request our brochure."),
        main=main,
        og="og-canitas-al-fresco",
        schema=[restaurant_ld(c), faq_ld(faqs), breadcrumb_ld(c, t("Eventos de empresa", "Corporate events"))],
    )


PAGES = {"desayunos": desayunos, "eventos": eventos}
