"""Subpáginas SEO de desayunos y eventos (ES / EN). No están en la cabecera: se
enlazan desde su página madre (Desayunos o Eventos), entre sí y desde el sitemap.
Cada una responde a una búsqueda concreta, en español y para el público
internacional, sin carta ni precios.

  Desayunos
    brunch-malaga                       brunch Málaga / brunch in Málaga
    donde-desayunar-malaga-centro       dónde desayunar en Málaga centro / breakfast in Málaga old town
    desayuno-hotel-malaga-sin-alojarse  desayuno de hotel sin alojarse / hotel breakfast for non-guests
  Eventos
    cena-de-empresa-malaga              cena de empresa / company dinner Málaga
    cena-navidad-empresa-malaga         cena de Navidad de empresa / Christmas party Málaga
    rooftop-para-eventos-malaga         rooftop para eventos / rooftop event venue Málaga
    reuniones-coffee-break-malaga       reuniones y coffee break / meeting venue Málaga
"""
from build import EMAIL, MAPS, PHONE, PHONE_TEL, fresco_ld, page_hero, restaurant_ld
from landings import facts, faq_block, faq_ld, split
from pages import cta_band, gallery, mailto

# Texto de cada enlace (para los bloques de enlaces relacionados)
LABEL = {
    "brunch": lambda c: c.t("Brunch en Málaga", "Brunch in Málaga"),
    "desayunar": lambda c: c.t("Dónde desayunar en Málaga centro", "Breakfast in Málaga old town"),
    "hotelbreakfast": lambda c: c.t("Desayuno de hotel sin alojarse", "Hotel breakfast for non-guests"),
    "cenaempresa": lambda c: c.t("Cena de empresa en Málaga", "Company dinner in Málaga"),
    "navidad": lambda c: c.t("Cena de Navidad de empresa", "Christmas party in Málaga"),
    "rooftopeventos": lambda c: c.t("Rooftop para eventos", "Rooftop event venue"),
    "reuniones": lambda c: c.t("Reuniones y coffee break", "Meetings & coffee breaks"),
}
FAMILY = {
    "desayunos": ("brunch", "desayunar", "hotelbreakfast"),
    "eventos": ("cenaempresa", "navidad", "rooftopeventos", "reuniones"),
}


def breadcrumb3(c, parent, parent_name, name):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": c.t("Inicio", "Home"), "item": c.abs_url("home")},
            {"@type": "ListItem", "position": 2, "name": parent_name, "item": c.abs_url(parent)},
            {"@type": "ListItem", "position": 3, "name": name, "item": c.abs_url(c.key)},
        ],
    }


def hero3(c, parent, parent_name, name, eyebrow, h1, lead, photo, actions):
    """Cabecera con migas de tres niveles: Inicio › Desayunos/Eventos › página."""
    t = c.t
    html = page_hero(c, eyebrow, h1, lead, photo=photo, actions=actions, crumbs=[name])
    return html.replace(
        f'<li><a href="{c.link("home")}">{t("Inicio", "Home")}</a></li>',
        f'<li><a href="{c.link("home")}">{t("Inicio", "Home")}</a></li><li><a href="{c.link(parent)}">{parent_name}</a></li>', 1)


def tiles(items):
    lis = "\n".join(f'        <li class="tile"><h3>{h}</h3><p>{p}</p></li>' for h, p in items)
    return f'      <ul class="tiles">\n{lis}\n      </ul>'


def block(eyebrow, title, inner, tint=False):
    return f"""  <section class="section{' section-tint' if tint else ''}">
    <div class="section-inner">
      <div class="section-head">
        <p class="eyebrow eyebrow-dark">{eyebrow}</p>
        <h2 class="section-title">{title}</h2>
      </div>
{inner}
    </div>
  </section>"""


def family_links(c, parent):
    t = c.t
    parent_label = t("Desayunos y brunch", "Breakfast & brunch") if parent == "desayunos" else t("Eventos de empresa", "Corporate events")
    links = [(parent, parent_label)] + [(k, LABEL[k](c)) for k in FAMILY[parent] if k != c.key]
    if parent == "desayunos":
        links.append(("eventos", t("Desayunos de trabajo y eventos", "Working breakfasts & events")))
    else:
        links.append(("desayunos", t("Desayuno y brunch en el hotel", "Breakfast & brunch at the hotel")))
    lis = "".join(f'<li><a href="{c.link(k)}">{label}</a></li>' for k, label in links)
    title = t("Sigue leyendo", "Keep reading")
    return f"""  <section class="section">
    <div class="section-inner">
      <nav class="related" aria-label="{title}">
        <p class="eyebrow eyebrow-dark">{title}</p>
        <ul>{lis}</ul>
      </nav>
    </div>
  </section>"""


def build_page(c, parent, name, eyebrow, h1, lead, photo, actions, intro, facts_list, tiles_head, tiles_items,
               photos, faqs, cta, title, desc, og="og-canitas-malaga", theme=None, venue="restaurant"):
    t = c.t
    parent_name = t("Desayunos", "Breakfast") if parent == "desayunos" else t("Eventos de empresa", "Corporate events")
    parts = [
        hero3(c, parent, parent_name, name, eyebrow, h1, lead, photo, actions),
        split(c, intro[0], intro[1], intro[2], extra=facts(facts_list)),
        block(tiles_head[0], tiles_head[1], tiles(tiles_items), tint=True),
    ]
    if photos:
        parts.append(f"""  <section class="section">
    <div class="section-inner">
{gallery(c, photos)}
    </div>
  </section>""")
    parts += [faq_block(c, faqs), family_links(c, parent), cta_band(c, *cta)]
    out = dict(
        nav_title=name,
        title=title,
        desc=desc,
        main="\n\n".join(parts),
        og=og,
        schema=[fresco_ld(c) if venue == "fresco" else restaurant_ld(c), faq_ld(faqs), breadcrumb3(c, parent, parent_name, name)],
    )
    if theme:
        out["theme"] = theme
    return out


def breakfast_actions(c):
    t = c.t
    return (f'<a class="btn btn-primary-light" href="{c.link("desayunos")}">{t("El desayuno", "The breakfast")}</a>'
            f'<a class="btn btn-ghost-light" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")} ↗</a>')


def events_actions(c):
    t = c.t
    dossier = t("Dossier de eventos — Cañitas Maite · ME Málaga", "Events brochure — Cañitas Maite · ME Málaga")
    return (f'<a class="btn btn-primary-light" href="{mailto(dossier)}">{t("Pide el dossier", "Request the brochure")}</a>'
            f'<a class="btn btn-ghost-light" href="tel:{PHONE_TEL}">{PHONE}</a>')


def events_cta(c, title_es, title_en):
    t = c.t
    subject = t("Evento de empresa — Cañitas Maite · ME Málaga", "Corporate event — Cañitas Maite · ME Málaga")
    return (t(title_es, title_en),
            t(f'Escríbenos a <a href="{mailto(subject)}">{EMAIL}</a> o llámanos al <a href="tel:{PHONE_TEL}">{PHONE}</a> con la fecha y el número de personas.',
              f'Email us at <a href="{mailto(subject)}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a> with your date and number of guests.'),
            events_actions(c))


def breakfast_cta(c):
    t = c.t
    return (t("Mañana, desayuno en el centro", "Tomorrow, breakfast in the centre"),
            t("Hotel ME Málaga by Meliá, Calle Victoria 6, a un minuto de la Plaza de la Merced. No hace falta alojarse.",
              "ME Málaga by Meliá, Calle Victoria 6, one minute from Plaza de la Merced. No need to be a hotel guest."),
            breakfast_actions(c))


BUFFET = lambda c: [
    (c.t("Panes de masa madre", "Sourdough breads"), c.t("Hogazas de fermentación lenta, tortas y molletes de obrador.", "Slow-fermented loaves, flatbreads and molletes from artisan bakeries.")),
    (c.t("Quesos y chacinas", "Cheese and charcuterie"), c.t("Quesos de granjas cercanas y embutidos de carnicerías de pueblo.", "Cheeses from nearby farms and cured meats from village butchers.")),
    (c.t("Fruta y aceite de aquí", "Local fruit and olive oil"), c.t("Fruta de temporada de la provincia y aceite de olivos centenarios.", "Seasonal fruit from the province and oil from century-old olive trees.")),
    (c.t("Huevos al momento", "Eggs cooked to order"), c.t("Huevos camperos de Coín: poché, fritos, benedict o en tortilla.", "Free-range Coín eggs: poached, fried, Benedict or as an omelette.")),
]


# ---------------------------------------------------------------------------
# Desayunos
# ---------------------------------------------------------------------------
def brunch(c):
    t = c.t
    name = LABEL["brunch"](c)
    faqs = [
        (t("¿Dónde hacer un buen brunch en el centro de Málaga?", "Where can I have a good brunch in central Málaga?"),
         t("En el hotel ME Málaga by Meliá, Calle Victoria 6: el desayuno de Cañitas Maite combina buffet de producto local con platos calientes hechos al momento, y está abierto a quien no se aloja en el hotel.",
           "At ME Málaga by Meliá, Calle Victoria 6: the Cañitas Maite breakfast pairs a local-produce buffet with hot dishes cooked to order, and it is open to non-guests.")),
        (t("¿Hay que estar alojado en el hotel?", "Do I have to be a hotel guest?"),
         t("No. Cualquiera puede venir a desayunar o hacer brunch.", "No. Anyone can come for breakfast or brunch.")),
        (t("¿Qué platos calientes hay?", "What hot dishes are there?"),
         t("Huevos camperos de Coín (poché, fritos, benedict o tortilla) y algunos especiales de la casa como huevos rotos con jamón Joselito, tortitas o bowl de açaí.",
           "Free-range Coín eggs (poached, fried, Benedict or omelette) and house specials such as broken eggs with Joselito ham, pancakes or açaí bowls.")),
        (t("¿Se puede venir en grupo?", "Can we come as a group?"),
         t(f"Sí. Para grupos, escríbenos a {EMAIL} o llámanos al {PHONE} y te lo preparamos.",
           f"Yes. For groups, email {EMAIL} or call {PHONE} and we will get everything ready.")),
    ]
    return build_page(
        c, "desayunos", name,
        t("Brunch · Málaga centro", "Brunch · Málaga old town"),
        t("Brunch en Málaga, sin prisa y con producto", "Brunch in Málaga, slow and produce-led"),
        t("Un brunch distinto en pleno centro: el desayuno largo de Cañitas Maite en el hotel ME Málaga, con buffet de pequeños productores y huevos hechos al momento.",
          "A different kind of brunch right in the old town: the long, unhurried Cañitas Maite breakfast at ME Málaga, with a small-producer buffet and eggs cooked to order."),
        "desayuno-platos-calientes-cazuelas", breakfast_actions(c),
        (t("El plan", "The plan"), t("El brunch que no esperas en un hotel", "The brunch you would not expect in a hotel"), [
            t("Lo que mucha gente busca cuando dice brunch —empezar tarde, comer bien y alargar la mesa— lo encuentras en el desayuno de Cañitas Maite: panes de masa madre, quesos de granja, chacinas de pueblo, fruta de la provincia y una cocina que hace los huevos al momento.",
              "What most people mean by brunch (a late start, good food and a long table) is exactly what the Cañitas Maite breakfast offers: sourdough bread, farm cheeses, village charcuterie, fruit from the province and a kitchen cooking eggs to order."),
            t("Está en el hotel ME Málaga by Meliá, a un minuto de la Plaza de la Merced, y la puerta está abierta para todos: vecinos, viajeros que duermen en otro sitio o quien quiere celebrar algo el fin de semana.",
              "It is at ME Málaga by Meliá, a minute from Plaza de la Merced, and the door is open to everyone: locals, travellers staying elsewhere or anyone celebrating at the weekend."),
        ]),
        [(t("Dónde", "Where"), "Calle Victoria 6, Málaga"), (t("Abierto a", "Open to"), t("todo el público.", "everyone, not only hotel guests.")),
         (t("Cocina", "Kitchen"), t("los chefs de Cañitas Maite.", "the Cañitas Maite chefs."))],
        (t("En la mesa", "On the table"), t("Lo que hace distinto este brunch", "What makes this brunch different")), BUFFET(c),
        [("desayuno-huevos-fritos-papada", t("Huevos fritos con puntilla y papada ibérica", "Crispy fried eggs with Iberian pork jowl")),
         ("desayuno-omelette-cremosa", t("Omelette hecha al momento", "Omelette cooked to order")),
         ("desayuno-bolleria-tradicional", t("Bollería de obrador", "Bakery pastries"))],
        faqs, breakfast_cta(c),
        t("Brunch en Málaga centro | Desayuno de producto en ME Málaga · Cañitas Maite", "Brunch in Málaga | Best Brunch in the Old Town · Cañitas Maite"),
        t("Brunch en el centro de Málaga, abierto a todos: buffet de productores locales y huevos al momento en el hotel ME Málaga, Calle Victoria 6.",
          "Brunch in Málaga old town, open to non-guests: a local-producer buffet and eggs cooked to order at ME Málaga, Calle Victoria 6."),
    )


def desayunar(c):
    t = c.t
    name = LABEL["desayunar"](c)
    faqs = [
        (t("¿Dónde desayunar bien en el centro de Málaga?", "Where can I have a good breakfast in Málaga old town?"),
         t("En el hotel ME Málaga by Meliá, en Calle Victoria 6, junto a la Plaza de la Merced: el desayuno de Cañitas Maite es de producto local y está abierto a todo el mundo.",
           "At ME Málaga by Meliá, Calle Victoria 6, next to Plaza de la Merced: the Cañitas Maite breakfast is built on local produce and open to everyone.")),
        (t("¿Qué se desayuna en Málaga?", "What do people have for breakfast in Málaga?"),
         t("Lo típico es una tostada o un mollete con aceite de oliva, tomate o manteca colorá, acompañado de un café pedido a la malagueña (mitad, nube, sombra…). En el desayuno de Cañitas Maite encontrarás molletes, buen aceite y productos de la zona.",
           "The classic is toast or a mollete roll with olive oil, tomato or manteca colorá, with a coffee ordered the Málaga way (mitad, nube, sombra…). At the Cañitas Maite breakfast you will find molletes, great olive oil and local produce.")),
        (t("¿Está cerca de los monumentos?", "Is it close to the sights?"),
         t("Sí: la Alcazaba, el Teatro Romano y el Museo Picasso están a unos 3 minutos a pie, y la Catedral a 5. Es un buen punto de partida para el día.",
           "Yes: the Alcazaba, the Roman Theatre and the Picasso Museum are about 3 minutes' walk away, and the Cathedral 5. A great place to start the day.")),
        (t("¿Puedo desayunar sin estar alojado?", "Can I have breakfast without staying at the hotel?"),
         t("Sí, el desayuno está abierto a quien venga de fuera.", "Yes, breakfast is open to non-guests.")),
    ]
    return build_page(
        c, "desayunos", name,
        t("Plaza de la Merced · Calle Victoria 6", "Plaza de la Merced · Calle Victoria 6"),
        t("Dónde desayunar en el centro de Málaga", "Breakfast in Málaga old town"),
        t("A un minuto de la Plaza de la Merced y a tres de la Alcazaba: el desayuno de productores locales de Cañitas Maite, en el hotel ME Málaga, abierto a todos.",
          "One minute from Plaza de la Merced and three from the Alcazaba: the Cañitas Maite local-producer breakfast at ME Málaga, open to everyone."),
        "desayuno-buffet-productores-locales-malaga", breakfast_actions(c),
        (t("Antes de ver Málaga", "Before you explore Málaga"), t("El mejor punto de partida para el día", "The best place to start the day"), [
            t("Si vas a recorrer el centro histórico, empieza por un buen desayuno a un paso de todo. El hotel ME Málaga by Meliá está en Calle Victoria 6, junto a la Plaza de la Merced y la casa natal de Picasso, con la Alcazaba, el Teatro Romano y la Catedral a pocos minutos a pie.",
              "If you are exploring the historic centre, start with a proper breakfast a step away from everything. ME Málaga by Meliá is at Calle Victoria 6, next to Plaza de la Merced and Picasso's birthplace, with the Alcazaba, the Roman Theatre and the Cathedral a few minutes' walk away."),
            t("El desayuno es de los chefs de Cañitas Maite: masa madre, molletes, quesos de granja, chacinas de pueblo, fruta de temporada de la provincia y huevos camperos hechos al momento.",
              "Breakfast is by the Cañitas Maite chefs: sourdough, molletes, farm cheeses, village charcuterie, seasonal fruit from the province and free-range eggs cooked to order."),
        ]),
        [("Plaza de la Merced", t("1 minuto a pie", "1 minute's walk")), (t("Alcazaba y Museo Picasso", "Alcazaba and Picasso Museum"), t("3 minutos", "3 minutes")),
         (t("Catedral", "Cathedral"), t("5 minutos", "5 minutes")), ("Calle Larios", t("unos 8 minutos", "about 8 minutes"))],
        (t("El desayuno", "The breakfast"), t("Producto de aquí, a la manera de Cañitas", "Local produce, the Cañitas way")), BUFFET(c),
        [("desayuno-panes-masa-madre-malaga", t("Panes de masa madre", "Sourdough breads")),
         ("desayuno-fruta-quesos-locales", t("Fruta de temporada y quesos", "Seasonal fruit and cheeses")),
         ("desayuno-chacinas-embutidos", t("Chacinas de pueblo", "Village charcuterie"))],
        faqs, breakfast_cta(c),
        t("Dónde desayunar en Málaga centro | Junto a la Plaza de la Merced · Cañitas Maite", "Breakfast in Málaga Old Town | Near Plaza de la Merced · Cañitas Maite"),
        t("Desayuno en el centro de Málaga, junto a la Plaza de la Merced y a 3 minutos de la Alcazaba: producto local y huevos al momento en ME Málaga. Abierto a todos.",
          "Breakfast in Málaga old town by Plaza de la Merced, 3 minutes from the Alcazaba: local produce and eggs cooked to order at ME Málaga. Open to non-guests."),
    )


def hotelbreakfast(c):
    t = c.t
    name = LABEL["hotelbreakfast"](c)
    faqs = [
        (t("¿Puedo desayunar en un hotel de Málaga sin estar alojado?", "Can I have breakfast at a hotel in Málaga without staying there?"),
         t("En el ME Málaga by Meliá, sí: el desayuno de Cañitas Maite está abierto a cualquiera que venga de fuera. Solo tienes que venir a Calle Victoria 6.",
           "At ME Málaga by Meliá, yes: the Cañitas Maite breakfast is open to anyone from outside the hotel. Just come to Calle Victoria 6.")),
        (t("¿Es un desayuno buffet?", "Is it a buffet breakfast?"),
         t("Sí, un buffet de producto local con panes, quesos, chacinas, fruta y bollería, más una cocina que prepara huevos y platos calientes al momento.",
           "Yes, a local-produce buffet with breads, cheeses, charcuterie, fruit and pastries, plus a kitchen preparing eggs and hot dishes to order.")),
        (t("¿Se puede pagar con puntos MeliáRewards?", "Can I pay with MeliáRewards points?"),
         t("Sí, el desayuno se puede pagar con puntos MeliáRewards.", "Yes, breakfast can be paid with MeliáRewards points.")),
        (t("¿Se puede regalar?", "Can I give it as a gift?"),
         t(f'Sí: hay tarjeta regalo de desayuno para dos. Mira <a href="{c.link("bonos")}">Bonos regalo</a>.',
           f'Yes: there is a breakfast gift card for two. See <a href="{c.link("bonos")}">Gift vouchers</a>.')),
    ]
    return build_page(
        c, "desayunos", name,
        t("Hotel cinco estrellas · ME Málaga by Meliá", "Five-star hotel · ME Málaga by Meliá"),
        t("Desayuno de hotel en Málaga, sin alojarte", "Hotel breakfast in Málaga, no stay required"),
        t("El desayuno de un hotel de cinco estrellas en pleno centro, abierto a quien no duerme en él: el buffet de productores locales de Cañitas Maite en ME Málaga.",
          "A five-star hotel breakfast in the heart of the city, open to people who are not staying there: the Cañitas Maite local-producer buffet at ME Málaga."),
        "desayuno-fruta-quesos-locales", breakfast_actions(c),
        (t("Abierto a todos", "Open to all"), t("Un desayuno de cinco estrellas, sin reserva de habitación", "A five-star breakfast, no room booking needed"), [
            t("Muchos hoteles reservan el desayuno a sus huéspedes. En ME Málaga by Meliá no: el desayuno de Cañitas Maite está abierto a vecinos, viajeros que se alojan en un apartamento y cualquiera que quiera empezar el día con calma en Calle Victoria 6.",
              "Many hotels keep breakfast for their guests only. Not ME Málaga by Meliá: the Cañitas Maite breakfast is open to locals, travellers staying in an apartment and anyone who wants a relaxed start at Calle Victoria 6."),
            t("Lo firman los chefs de Cañitas Maite (Casas-Ibáñez, una estrella Michelin): buffet de pequeños productores y huevos camperos de Coín hechos al momento, en un hotel lleno de arte contemporáneo.",
              "It is run by the Cañitas Maite chefs (Casas-Ibáñez, one Michelin star): a small-producer buffet and free-range Coín eggs cooked to order, in a hotel full of contemporary art."),
        ]),
        [(t("Hotel", "Hotel"), "ME Málaga by Meliá, 5*"), (t("Para", "For"), t("huéspedes y no huéspedes.", "guests and non-guests alike.")),
         ("MeliáRewards", t("puedes pagar con puntos.", "you can pay with points.")),
         (t("Regalo", "Gift"), t("tarjeta regalo de desayuno para dos.", "breakfast gift card for two."))],
        (t("El buffet", "The buffet"), t("Lo que te espera", "What awaits you")), BUFFET(c),
        [("desayuno-buffet-productores-locales-malaga", t("El buffet de desayuno", "The breakfast buffet")),
         ("me-malaga-salon-biblioteca", t("Interior del hotel ME Málaga", "Inside ME Málaga")),
         ("desayuno-bolleria-tradicional", t("Bollería tradicional", "Traditional pastries"))],
        faqs, breakfast_cta(c),
        t("Desayuno en hotel de Málaga sin alojarse | ME Málaga · Cañitas Maite", "Hotel Breakfast in Málaga for Non-Guests | ME Málaga · Cañitas Maite"),
        t("Desayuna en el hotel ME Málaga by Meliá aunque no te alojes: buffet de productores locales y huevos al momento en el centro. Se puede pagar con MeliáRewards.",
          "Have breakfast at ME Málaga by Meliá even if you are not staying: a local-producer buffet and eggs cooked to order in the old town. MeliáRewards accepted."),
    )


# ---------------------------------------------------------------------------
# Eventos
# ---------------------------------------------------------------------------
def cenaempresa(c):
    t = c.t
    name = LABEL["cenaempresa"](c)
    faqs = [
        (t("¿Dónde hacer una cena de empresa en el centro de Málaga?", "Where can we hold a company dinner in central Málaga?"),
         t("En el hotel ME Málaga by Meliá, Calle Victoria 6: Cañitas Maite organiza cenas de empresa en el restaurante de la última planta, en su comedor privado o en el rooftop.",
           "At ME Málaga by Meliá, Calle Victoria 6: Cañitas Maite hosts company dinners in the top-floor restaurant, its private dining room or on the rooftop.")),
        (t("¿Cena sentada o cóctel?", "Seated dinner or cocktail?"),
         t("Las dos: menú ejecutivo sentado, cena de gala con varios pases o cóctel de pie con finger food y estaciones.",
           "Both: a seated business menu, a multi-course gala dinner or a standing cocktail with finger food and food stations.")),
        (t("¿Tenéis menús vegetarianos?", "Do you have vegetarian menus?"),
         t("Sí, y se adaptan a veganos y a cualquier alergia.", "Yes, and they can be adapted for vegans and any allergy.")),
        (t("¿Con cuánta antelación hay que reservar?", "How far in advance should we book?"),
         t("Cuanto antes, sobre todo en temporada de Navidad. Escríbenos con la fecha y el número de personas.",
           "As early as possible, especially in the Christmas season. Send us your date and number of guests.")),
    ]
    return build_page(
        c, "eventos", name,
        t("Empresas · ME Málaga by Meliá", "Companies · ME Málaga by Meliá"),
        t("Cena de empresa en Málaga", "Company dinner in Málaga"),
        t("Cenas de empresa en pleno centro, con la cocina de brasa de Cañitas Maite: menú sentado, cena de gala o cóctel en el rooftop frente a la Alcazaba.",
          "Company dinners right in the city centre with Cañitas Maite grill cooking: a seated menu, a gala dinner or a rooftop cocktail facing the Alcazaba."),
        "canitas-malaga-comedor-privado-horizontal", events_actions(c),
        (t("La cena del equipo", "The team dinner"), t("Una cena de empresa que se recuerda", "A company dinner people remember"), [
            t("Cañitas Maite firma toda la gastronomía del hotel ME Málaga by Meliá. Para una cena de empresa eso significa producto de primera, parrilla y la mejor croqueta del mundo 2021 en la mesa, en un hotel de cinco estrellas a un minuto de la Plaza de la Merced.",
              "Cañitas Maite runs all the food at ME Málaga by Meliá. For a company dinner that means top produce, the grill and the Best Croquette in the World 2021 on the table, in a five-star hotel one minute from Plaza de la Merced."),
            t("Elegimos contigo el espacio según el grupo: el comedor privado para la dirección o los clientes, el restaurante y la terraza acristalada para equipos grandes, o el rooftop para empezar con un cóctel al atardecer.",
              "We choose the space with you depending on the group: the private dining room for management or clients, the restaurant and glass-roofed terrace for larger teams, or the rooftop to start with sunset cocktails."),
        ]),
        [(t("Formatos", "Formats"), t("menú ejecutivo, cena de gala o cóctel.", "business menu, gala dinner or cocktail.")),
         (t("Opciones", "Options"), t("vegetariana, vegana y menú infantil.", "vegetarian, vegan and children's menus.")),
         (t("Bebida", "Drinks"), t("packs de bodega y barra libre.", "wine packages and open bar."))],
        (t("Formatos", "Formats"), t("Cómo puede ser vuestra cena", "How your dinner can look")), [
            (t("Menú ejecutivo", "Business menu"), t("Entrante, principal a elegir y postre, servido en mesa en unos 90 minutos. Desde 40 personas.", "Starter, choice of main and dessert, served at the table in about 90 minutes. From 40 guests.")),
            (t("Cena de gala", "Gala dinner"), t("Varios pases con producto de primera y pescado y carne. Desde 40 personas.", "Several courses of top produce with fish and meat. From 40 guests.")),
            (t("Cóctel de pie", "Standing cocktail"), t("Bocados de la casa y estaciones de jamón, quesos u ostras. Desde 20 personas.", "House bites and ham, cheese or oyster stations. From 20 guests.")),
            (t("Grupos pequeños", "Smaller groups"), t(f'Para menos personas, el comedor privado o los <a href="{c.link("grupos")}">menús de grupo</a> del restaurante.', f'For smaller numbers, the private dining room or the restaurant\'s <a href="{c.link("grupos")}">group menus</a>.')),
        ],
        [("canitas-malaga-sala-mesas", t("La sala del restaurante", "The restaurant dining room")),
         ("evento-croquetas-pase", t("La mejor croqueta del mundo, en pase", "The world's best croquette, passed around")),
         ("txuleta-vasca-parrilla-canitas-malaga", t("Txuleta a la parrilla", "Grilled txuleta"))],
        faqs, events_cta(c, "¿Cuándo es vuestra cena?", "When is your dinner?"),
        t("Cena de empresa en Málaga centro | Restaurante y rooftop · Cañitas Maite", "Company Dinner in Málaga | Restaurant & Rooftop Venue · Cañitas Maite"),
        t("Cenas de empresa en el hotel ME Málaga: menú sentado, cena de gala o cóctel en el rooftop frente a la Alcazaba, con la cocina de Cañitas Maite. Pide el dossier.",
          "Company dinners at ME Málaga: seated menus, gala dinners or rooftop cocktails facing the Alcazaba, with Cañitas Maite cooking. Request our brochure."),
    )


def navidad(c):
    t = c.t
    name = LABEL["navidad"](c)
    faqs = [
        (t("¿Dónde celebrar la cena de Navidad de empresa en Málaga?", "Where can we hold a company Christmas party in Málaga?"),
         t("En el hotel ME Málaga by Meliá, en pleno centro: Cañitas Maite prepara cócteles navideños y menús de gala en mesa para empresas, con bodega incluida.",
           "At ME Málaga by Meliá, right in the centre: Cañitas Maite prepares Christmas cocktail receptions and seated gala menus for companies, with wine included.")),
        (t("¿Qué formatos de Navidad tenéis?", "Which Christmas formats do you offer?"),
         t("Cóctel navideño de pie (también vegetariano) y menú de gala en mesa con platos individuales. Todos incluyen bodega.",
           "A standing Christmas cocktail (vegetarian too) and a seated gala menu with individual dishes. All include wine.")),
        (t("¿Cuándo hay que reservar la cena de Navidad?", "When should we book the Christmas dinner?"),
         t("Lo antes posible: las fechas de diciembre son las primeras en llenarse.", "As early as possible: December dates are the first to fill up.")),
        (t("¿Hay opciones vegetarianas?", "Are there vegetarian options?"),
         t("Sí, hay cóctel navideño vegetariano y adaptamos los menús a alergias e intolerancias.", "Yes, there is a vegetarian Christmas cocktail and we adapt menus to allergies and intolerances.")),
    ]
    return build_page(
        c, "eventos", name,
        t("Navidad · Empresas", "Christmas · Companies"),
        t("Cena de Navidad de empresa en Málaga", "Company Christmas party in Málaga"),
        t("Cócteles navideños y menús de gala con bodega incluida, en el hotel ME Málaga by Meliá y con la cocina de Cañitas Maite. Reserva pronto las fechas de diciembre.",
          "Christmas cocktail receptions and gala menus with wine included, at ME Málaga by Meliá with Cañitas Maite cooking. Book your December date early."),
        "evento-mesa-finger-food", events_actions(c),
        (t("La Navidad del equipo", "The team Christmas"), t("Brindar por el año en el centro de Málaga", "Toast the year in central Málaga"), [
            t("La cena de Navidad es la cita del año para muchas empresas. En ME Málaga by Meliá la preparamos en el restaurante de la última planta, en el comedor privado o en el rooftop, con menús pensados para la ocasión y bodega incluida.",
              "The Christmas party is the event of the year for many companies. At ME Málaga by Meliá we host it in the top-floor restaurant, the private dining room or on the rooftop, with menus designed for the occasion and wine included."),
            t("Para grupos que prefieren moverse y charlar, el cóctel navideño; para una noche más formal, el menú de gala en mesa. Y para quien venga de fuera de Málaga, el hotel está en pleno centro histórico.",
              "For groups that like to mingle, the Christmas cocktail; for a more formal evening, the seated gala menu. And for anyone travelling in, the hotel is right in the historic centre."),
        ]),
        [(t("Formatos", "Formats"), t("cóctel navideño o menú de gala en mesa.", "Christmas cocktail or seated gala menu.")),
         (t("Bodega", "Wine"), t("incluida en los menús de Navidad.", "included in the Christmas menus.")),
         (t("Vegetariano", "Vegetarian"), t("cóctel navideño vegetariano.", "vegetarian Christmas cocktail."))],
        (t("Menús de Navidad", "Christmas menus"), t("Tres maneras de celebrarlo", "Three ways to celebrate")), [
            (t("Cóctel clásicos Cañitas", "Cañitas classics cocktail"), t("Los bocados de la casa, de la mejor croqueta del mundo al donut de rabo de toro.", "The house favourites, from the world's best croquette to the oxtail doughnut.")),
            (t("Cóctel navideño de producto", "Premium Christmas cocktail"), t("Ostras, quisquilla, atún rojo, carabinero y torrija de panettone.", "Oysters, quisquilla shrimp, bluefin tuna, red prawns and panettone torrija.")),
            (t("Menú de gala en mesa", "Seated gala menu"), t("Aperitivos, pescado y carne con platos individuales y postre de la casa.", "Appetisers, fish and meat as individual dishes and a house dessert.")),
        ],
        [("evento-cocteles-alcazaba", t("Cócteles en la azotea", "Cocktails on the rooftop")),
         ("evento-croquetas-pase", t("La mejor croqueta del mundo", "The world's best croquette")),
         ("canitas-malaga-comedor-privado", t("El comedor privado", "The private dining room"))],
        faqs, events_cta(c, "Reserva vuestra Navidad", "Book your Christmas party"),
        t("Cena de Navidad de empresa en Málaga | Cócteles y menús de gala · Cañitas Maite", "Christmas Party Venue in Málaga | Company Dinners · Cañitas Maite"),
        t("Cenas de Navidad de empresa en el hotel ME Málaga: cóctel navideño o menú de gala con bodega incluida, en el centro de Málaga. Pide el dossier de Navidad.",
          "Company Christmas parties at ME Málaga: Christmas cocktails or seated gala menus with wine included, in Málaga old town. Request our Christmas brochure."),
    )


def rooftopeventos(c):
    t = c.t
    name = LABEL["rooftopeventos"](c)
    faqs = [
        (t("¿Se puede alquilar un rooftop para eventos en Málaga?", "Can we hire a rooftop for an event in Málaga?"),
         t("Sí. El rooftop de Cañitas al Fresco, en la azotea del hotel ME Málaga by Meliá, se puede privatizar para eventos de empresa; consúltanos fechas y condiciones.",
           "Yes. The Cañitas al Fresco rooftop, on top of ME Málaga by Meliá, can be privatised for corporate events; ask us about dates and conditions.")),
        (t("¿Qué se ve desde el rooftop?", "What is the view like?"),
         t("La Alcazaba y Gibralfaro de frente, la Catedral y los tejados del centro histórico. Al atardecer es espectacular.",
           "The Alcazaba and Gibralfaro straight ahead, the Cathedral and the old-town rooftops. Sunset is spectacular.")),
        (t("¿Qué formato funciona mejor en la azotea?", "Which format works best on the rooftop?"),
         t("El cóctel de pie con finger food, una copa de bienvenida al atardecer o un cóctel seguido de barra libre.",
           "A standing cocktail with finger food, sunset welcome drinks, or a cocktail followed by an open bar.")),
        (t("¿Y si hace mal tiempo?", "What if the weather is bad?"),
         t("Tenemos espacios interiores en el hotel y el restaurante de la última planta como alternativa.",
           "We have indoor spaces in the hotel and the top-floor restaurant as a back-up.")),
    ]
    return build_page(
        c, "eventos", name,
        t("Azotea · ME Málaga by Meliá", "Rooftop · ME Málaga by Meliá"),
        t("Rooftop para eventos en Málaga", "Rooftop event venue in Málaga"),
        t("Privatiza la azotea de Cañitas al Fresco para tu evento: cóctel al atardecer frente a la Alcazaba, en el hotel ME Málaga by Meliá, en pleno centro.",
          "Privatise the Cañitas al Fresco rooftop for your event: sunset cocktails facing the Alcazaba at ME Málaga by Meliá, right in the old town."),
        "evento-empresa-rooftop-atardecer-malaga", events_actions(c),
        (t("La azotea", "The rooftop"), t("La Alcazaba como telón de fondo", "The Alcazaba as your backdrop"), [
            t("Pocos espacios de Málaga tienen la Alcazaba tan de frente. La azotea de Cañitas al Fresco, en lo más alto del hotel ME Málaga by Meliá, se convierte en un espacio privado para presentaciones, lanzamientos, incentivos o la fiesta del equipo.",
              "Few venues in Málaga face the Alcazaba so directly. The Cañitas al Fresco rooftop, at the top of ME Málaga by Meliá, becomes a private venue for launches, incentives, product presentations or the team party."),
            t("Cóctel, finger food y estaciones de la cocina de Cañitas Maite, copa de bienvenida al atardecer y barra libre para cerrar la noche. Ideal también para grupos internacionales que visitan Málaga.",
              "Cocktails, finger food and food stations by Cañitas Maite, sunset welcome drinks and an open bar to end the night. Also ideal for international groups visiting Málaga."),
        ]),
        [(t("Vistas", "Views"), t("Alcazaba, Gibralfaro y Catedral.", "Alcazaba, Gibralfaro and the Cathedral.")),
         (t("Formatos", "Formats"), t("copa de bienvenida, cóctel, estaciones y barra libre.", "welcome drinks, cocktail, food stations and open bar.")),
         (t("Alternativa", "Back-up"), t("espacios interiores del hotel.", "indoor hotel spaces."))],
        (t("Ideas", "Ideas"), t("Para qué se usa el rooftop", "What the rooftop is used for")), [
            (t("Presentaciones y lanzamientos", "Launches and presentations"), t("Un escenario con vistas para presentar producto o marca.", "A stage with a view to present a product or brand.")),
            (t("Incentivos y grupos internacionales", "Incentives and international groups"), t("Una noche en Málaga que el grupo no olvida.", "A Málaga night the group won't forget.")),
            (t("Fiesta del equipo", "Team party"), t("Cóctel al atardecer y barra libre de dos horas.", "Sunset cocktails and a two-hour open bar.")),
        ],
        [("evento-cocteles-alcazaba", t("Cócteles frente a la Alcazaba", "Cocktails facing the Alcazaba")),
         ("me-malaga-terraza-alcazaba", t("La Alcazaba desde la azotea", "The Alcazaba from the rooftop")),
         ("canitas-al-fresco-rooftop-piscina-malaga", t("La azotea de Cañitas al Fresco", "The Cañitas al Fresco rooftop"))],
        faqs, events_cta(c, "¿Subimos tu evento a la azotea?", "Shall we take your event up to the rooftop?"),
        t("Rooftop para eventos en Málaga | Azotea frente a la Alcazaba · Cañitas al Fresco", "Rooftop Event Venue in Málaga | Alcazaba Views · Cañitas al Fresco"),
        t("Alquila el rooftop de Cañitas al Fresco en el hotel ME Málaga para eventos de empresa: cóctel al atardecer frente a la Alcazaba, finger food y barra libre.",
          "Hire the Cañitas al Fresco rooftop at ME Málaga for corporate events: sunset cocktails facing the Alcazaba, finger food and an open bar."),
        og="og-canitas-al-fresco", venue="fresco",
    )


def reuniones(c):
    t = c.t
    name = LABEL["reuniones"](c)
    faqs = [
        (t("¿Dónde organizar una reunión de empresa en el centro de Málaga?", "Where can we hold a business meeting in central Málaga?"),
         t("En el hotel ME Málaga by Meliá, en Calle Victoria 6: espacios interiores, comedor privado y la cocina de Cañitas Maite para el coffee break, la comida o el cóctel.",
           "At ME Málaga by Meliá, Calle Victoria 6: indoor spaces, a private dining room and Cañitas Maite cooking for the coffee break, lunch or cocktail.")),
        (t("¿Para cuántas personas es el coffee break?", "How many people is the coffee break for?"),
         t("Desde 10 personas, con versión vegetariana y posibilidad de alargar el servicio.", "From 10 guests, with a vegetarian version and the option to extend the service.")),
        (t("¿Podemos combinar reunión, comida y cóctel?", "Can we combine a meeting, lunch and a cocktail?"),
         t("Sí: coffee break por la mañana, menú ejecutivo a mediodía y cóctel en el rooftop para cerrar la jornada.",
           "Yes: a morning coffee break, a business lunch at midday and a rooftop cocktail to close the day.")),
        (t("¿Y desayunos de trabajo?", "What about working breakfasts?"),
         t(f'También: el <a href="{c.link("desayunos")}">desayuno de Cañitas Maite</a> está abierto a quien no se aloja en el hotel, y para grupos lo preparamos a medida.',
           f'Yes: the <a href="{c.link("desayunos")}">Cañitas Maite breakfast</a> is open to non-guests, and we tailor it for groups.')),
    ]
    return build_page(
        c, "eventos", name,
        t("Jornadas de trabajo · ME Málaga by Meliá", "Workdays · ME Málaga by Meliá"),
        t("Reuniones y coffee break en Málaga", "Meeting venue & coffee breaks in Málaga"),
        t("Reuniones, jornadas y presentaciones en pleno centro, con coffee break de obrador, comida de trabajo y cóctel en el rooftop, en el hotel ME Málaga by Meliá.",
          "Meetings, workshops and presentations right in the old town, with bakery coffee breaks, working lunches and rooftop cocktails at ME Málaga by Meliá."),
        "evento-coffee-break", events_actions(c),
        (t("La jornada", "The workday"), t("De la primera reunión al último cóctel", "From the first meeting to the last cocktail"), [
            t("El hotel ME Málaga by Meliá está en pleno centro histórico, a un paso de todo y fácil de encontrar para quien viene de fuera. Sus espacios interiores y el comedor privado sirven para reuniones de dirección, formaciones y presentaciones a clientes.",
              "ME Málaga by Meliá sits in the heart of the old town, close to everything and easy to find for visitors. Its indoor spaces and private dining room work for board meetings, training sessions and client presentations."),
            t("Cañitas Maite se ocupa de la parte gastronómica: coffee breaks con bollería de obrador y zumos naturales, menús ejecutivos para la comida y cóctel en el rooftop frente a la Alcazaba para cerrar el día.",
              "Cañitas Maite handles the food: coffee breaks with bakery pastries and fresh juices, business set menus for lunch and a rooftop cocktail facing the Alcazaba to end the day."),
        ]),
        [(t("Coffee break", "Coffee break"), t("desde 10 personas.", "from 10 guests.")),
         (t("Comida de trabajo", "Working lunch"), t("menú ejecutivo en mesa.", "seated business menu.")),
         (t("Ubicación", "Location"), t("Calle Victoria 6, Málaga centro.", "Calle Victoria 6, Málaga old town."))],
        (t("Formatos", "Formats"), t("Para cada momento del día", "For every part of the day")), [
            (t("Coffee break", "Coffee break"), t("Café, zumos naturales y bollería de obrador; también salado y vegetariano.", "Coffee, fresh juices and bakery pastries; savoury and vegetarian options too.")),
            (t("Comida ejecutiva", "Business lunch"), t("Entrante, principal a elegir y postre en unos 90 minutos.", "Starter, choice of main and dessert in about 90 minutes.")),
            (t("Cóctel de cierre", "Closing cocktail"), t("Finger food y copa en el rooftop frente a la Alcazaba.", "Finger food and drinks on the rooftop facing the Alcazaba.")),
        ],
        [("evento-coffee-break", t("Coffee break de obrador", "Bakery coffee break")),
         ("me-malaga-lobby-bar", t("Lobby bar de ME Málaga", "ME Málaga lobby bar")),
         ("canitas-malaga-comedor-privado-horizontal", t("Comedor privado", "Private dining room"))],
        faqs, events_cta(c, "Organiza tu jornada", "Plan your workday"),
        t("Reuniones de empresa y coffee break en Málaga centro | ME Málaga · Cañitas Maite", "Meeting Venue in Málaga | Coffee Breaks & Business Lunches · Cañitas Maite"),
        t("Reuniones y jornadas en el hotel ME Málaga: coffee break de obrador, comida ejecutiva y cóctel en el rooftop, en el centro de Málaga. Pide el dossier.",
          "Meetings and workshops at ME Málaga: bakery coffee breaks, business lunches and rooftop cocktails in Málaga old town. Request our brochure."),
    )


PAGES = {
    "brunch": brunch, "desayunar": desayunar, "hotelbreakfast": hotelbreakfast,
    "cenaempresa": cenaempresa, "navidad": navidad, "rooftopeventos": rooftopeventos, "reuniones": reuniones,
}
