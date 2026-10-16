"""Preguntas frecuentes (ES / EN): la página de referencia para buscadores con IA
(ChatGPT, Perplexity, Gemini, Copilot, Google AI Overviews…). Cada respuesta empieza
por el dato que se pregunta y se sostiene sola, sin depender del resto de la página,
para que se pueda citar tal cual. Los mismos datos alimentan llms.txt y llms-full.txt.
"""
from build import EMAIL, INSTAGRAM, MAPS, PHONE, breadcrumb_ld, fresco_ld, hours_text, page_hero, restaurant_ld
from landings import facts
from menus_data import FRESCO_CARTA, MAITE_CARTA, MAITE_SET_MENUS
from pages import cta_band, strip_tags


def price_range(sections):
    prices = [p for s in sections for *_, p in s["items"]]
    return min(prices), max(prices)


def key_facts(c):
    """Ficha rápida: los datos que más se preguntan, en una lista."""
    t = c.t
    lo, hi = price_range(MAITE_CARTA)
    flo, fhi = price_range(FRESCO_CARTA)
    eur = (lambda n: f"{n} €") if c.lang == "es" else (lambda n: f"€{n}")
    menus = ", ".join(f"{t(m['es_name'], m['en_name'])} {eur(m['price'])}" for m in MAITE_SET_MENUS)
    return [
        (t("Dirección:", "Address:"), "Hotel ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga"),
        ("Cañitas Málaga:", t(f"restaurante en la última planta. {hours_text('es', 'maite')}. Reserva online recomendada.",
                              f"restaurant on the top floor. {hours_text('en', 'maite')}. Booking recommended.")),
        ("Cañitas al Fresco:", t(f"rooftop bar en la azotea, abierto al público. {hours_text('es', 'fresco')}. Sin reserva.",
                                 f"rooftop bar, open to the public. {hours_text('en', 'fresco')}. No reservations.")),
        (t("Chefs:", "Chefs:"), t("Javier Sanz y Juan Sahuquillo (Cañitas Maite, Casas-Ibáñez, una estrella Michelin)",
                                  "Javier Sanz and Juan Sahuquillo (Cañitas Maite, Casas-Ibáñez, one Michelin star)")),
        (t("Cocina:", "Cuisine:"), t("española de producto, parrilla y brasa", "Spanish, produce-led, grill and embers")),
        (t("Precios:", "Prices:"), t(f"menús para compartir: {menus} por persona; a la carta, platos de {eur(lo)} a {eur(hi)}. Al Fresco: de {eur(flo)} a {eur(fhi)}.",
                                     f"sharing menus: {menus} per person; à la carte dishes {eur(lo)}–{eur(hi)}. Al Fresco: {eur(flo)}–{eur(fhi)}.")),
        (t("Contacto:", "Contact:"), f"{PHONE} · {EMAIL}"),
    ]


def faq_groups(c):
    """(título del grupo, [(pregunta, respuesta)]). Las respuestas pueden llevar enlaces."""
    t = c.t
    lo, hi = price_range(MAITE_CARTA)
    eur = (lambda n: f"{n} €") if c.lang == "es" else (lambda n: f"€{n}")
    hits, classics = MAITE_SET_MENUS
    return [
        (t("Lo básico", "The basics"), [
            (t("¿Qué es Cañitas Málaga?", "What is Cañitas Málaga?"),
             t("Cañitas Málaga es el restaurante de los chefs Javier Sanz y Juan Sahuquillo en la última planta del hotel ME Málaga by Meliá, en el centro de Málaga. Cocina española de producto, parrilla y brasa, con vistas a la Alcazaba. En la azotea del mismo hotel está su rooftop bar, Cañitas al Fresco.",
               "Cañitas Málaga is the restaurant of chefs Javier Sanz and Juan Sahuquillo on the top floor of ME Málaga by Meliá, in Málaga city centre. Spanish produce-led cooking over the grill and embers, with views of the Alcazaba. Its rooftop bar, Cañitas al Fresco, is on the roof of the same hotel.")),
            (t("¿Es lo mismo Cañitas Málaga que Cañitas Maite?", "Is Cañitas Málaga the same as Cañitas Maite?"),
             t("Son los mismos chefs. Cañitas Maite es su restaurante de origen en Casas-Ibáñez (Albacete), con una estrella Michelin. Cañitas Málaga es su casa en Málaga, en el hotel ME Málaga by Meliá, y también se conoce como Cañitas Maite Málaga.",
               "Same chefs. Cañitas Maite is their original restaurant in Casas-Ibáñez (Albacete), which holds one Michelin star. Cañitas Málaga is their Málaga venue at ME Málaga by Meliá, also known as Cañitas Maite Málaga.")),
            (t("¿Dónde está Cañitas Málaga?", "Where is Cañitas Málaga?"),
             t(f'En el Hotel ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga: en el centro histórico, a 1 minuto a pie de la Plaza de la Merced y a 3 minutos de la Alcazaba y del Museo Picasso. <a href="{MAPS}" target="_blank" rel="noopener">Ver en Google Maps</a>.',
               f'At ME Málaga by Meliá, Calle Victoria 6, 29012 Málaga: in the historic centre, a 1-minute walk from Plaza de la Merced and 3 minutes from the Alcazaba and the Picasso Museum. <a href="{MAPS}" target="_blank" rel="noopener">View on Google Maps</a>.')),
            (t("¿Qué horario tiene?", "What are the opening hours?"),
             t(f"El restaurante Cañitas Málaga abre {hours_text('es', 'maite').lower()}. El rooftop Cañitas al Fresco abre {hours_text('es', 'fresco').lower()}.",
               f"Cañitas Málaga restaurant is open {hours_text('en', 'maite').lower()}. The Cañitas al Fresco rooftop is open {hours_text('en', 'fresco').lower()}.")),
            (t("¿Abre todos los días?", "Is it open every day?"),
             t("Sí. Tanto el restaurante como el rooftop abren los siete días de la semana.",
               "Yes. Both the restaurant and the rooftop are open seven days a week.")),
        ]),
        (t("Reservas", "Bookings"), [
            (t("¿Cómo reservo mesa en Cañitas Málaga?", "How do I book a table at Cañitas Málaga?"),
             t(f'Online, en la página <a href="{c.link("reservas")}">Reservar mesa</a>: eliges día, hora y número de personas y recibes la confirmación al momento. También por teléfono en el {PHONE}.',
               f'Online, on the <a href="{c.link("reservas")}">Book a table</a> page: choose the day, time and party size and get instant confirmation. You can also call {PHONE}.')),
            (t("¿Se puede reservar en Cañitas al Fresco?", "Can I book at Cañitas al Fresco?"),
             t("No. Cañitas al Fresco no admite reservas: se entra por orden de llegada.",
               "No. Cañitas al Fresco does not take reservations: it is first come, first served.")),
            (t("¿Hace falta reservar en el restaurante?", "Do I need to book at the restaurant?"),
             t("Es lo recomendable, sobre todo para cenar y en fin de semana. Sin reserva te atenderemos si hay mesa libre.",
               "It is recommended, especially for dinner and at weekends. Without a booking we will seat you if a table is free.")),
            (t("Somos un grupo grande, ¿qué opciones hay?", "We are a large group. What are the options?"),
             t(f'Las mesas de 8 personas o más tienen menú cerrado y hay un comedor privado con una sola mesa en la última planta. Escríbenos a {EMAIL} o mira <a href="{c.link("grupos")}">Grupos y eventos</a>.',
               f'Tables of 8 or more have a set menu, and there is a private dining room with a single table on the top floor. Email {EMAIL} or see <a href="{c.link("grupos")}">Groups & events</a>.')),
        ]),
        (t("Carta y precios", "Menu and prices"), [
            (t("¿Cuánto cuesta comer en Cañitas Málaga?", "How much does it cost to eat at Cañitas Málaga?"),
             t(f"Hay dos menús para compartir: {classics['es_name']} a {eur(classics['price'])} por persona (de lunes a jueves) y {hits['es_name']} a {eur(hits['price'])} por persona (todos los días). A la carta, los platos van de {eur(lo)} a {eur(hi)}.",
               f"There are two sharing menus: the {classics['en_name']} at {eur(classics['price'])} per person (Monday to Thursday) and the {hits['en_name']} at {eur(hits['price'])} per person (every day). À la carte dishes range from {eur(lo)} to {eur(hi)}.")),
            (t("¿Qué platos son los más conocidos?", "What are the signature dishes?"),
             t("La Mejor Croqueta del Mundo 2021 (de jamón Joselito), la txuleta vasca madurada a la parrilla, la lubina entera con pil pil de su colágeno, la ensaladilla de gamba blanca al ajillo y el flan de nata fresca de oveja.",
               "The Best Croquette in the World 2021 (made with Joselito ham), the dry-aged Basque txuleta from the grill, whole sea bass with pil pil from its own collagen, white prawn Russian salad al ajillo and the fresh sheep's cream flan.")),
            (t("¿Puedo ver la carta antes de ir?", "Can I see the menu before I go?"),
             t(f'Sí: la carta completa con precios de los dos espacios está en <a href="{c.link("carta")}">La carta</a>, en español y en inglés.',
               f'Yes: the full menus of both venues, with prices, are on <a href="{c.link("carta")}">The menu</a>, in English and Spanish.')),
            (t("¿Hay opciones vegetarianas?", "Are there vegetarian options?"),
             t("Sí. La carta tiene una sección de verduras (berenjena con burrata, puerro asado con romesco, setas de temporada, tomates…) y en Cañitas al Fresco hay hummus, guacamole y ensaladas. Dinos tus preferencias al reservar.",
               "Yes. The menu has a vegetable section (aubergine with burrata, roasted leek with romesco, seasonal mushrooms, tomatoes…) and Cañitas al Fresco serves hummus, guacamole and salads. Let us know your preferences when booking.")),
            (t("¿Informáis de alérgenos?", "Do you provide allergen information?"),
             t("Sí. Pide la información de alérgenos al equipo de sala y te indicaremos los de cada plato.",
               "Yes. Ask our team for the allergen information and we will tell you the allergens in each dish.")),
            (t("¿Qué se puede pagar con tarjeta?", "Can I pay by card?"),
             t("Sí, se aceptan tarjetas de crédito y débito y pago con el móvil.",
               "Yes, credit and debit cards and mobile payments are accepted.")),
        ]),
        (t("El rooftop: Cañitas al Fresco", "The rooftop: Cañitas al Fresco"), [
            (t("¿Puede subir cualquiera al rooftop del ME Málaga?", "Can anyone go up to the ME Málaga rooftop?"),
             t("Sí. Cañitas al Fresco, el rooftop bar de la azotea, está abierto a todo el público, no solo a huéspedes del hotel. La piscina sí es exclusiva para los huéspedes.",
               "Yes. Cañitas al Fresco, the rooftop bar, is open to everyone, not only hotel guests. The pool, however, is for hotel guests only.")),
            (t("¿Qué se toma en Cañitas al Fresco?", "What is served at Cañitas al Fresco?"),
             t(f'Coctelería, vinos, cervezas y picoteo de la casa: la mejor croqueta del mundo, guacamole, ensaladilla, tartar de atún rojo, bocatería fina (bikini trufado, club sándwich, burger de vaca gallega) y postres. <a href="{c.link("carta", anchor="canitas-al-fresco")}">Ver la carta</a>.',
               f'Cocktails, wine, beer and sharing plates: the world’s best croquette, guacamole, Russian salad, bluefin tuna tartare, gourmet sandwiches (truffled bikini toastie, club sandwich, Galician beef burger) and desserts. <a href="{c.link("carta", anchor="canitas-al-fresco")}">See the menu</a>.')),
            (t("¿Qué se ve desde la azotea?", "What can you see from the rooftop?"),
             t("La Alcazaba y Gibralfaro de frente, la Catedral de Málaga y los tejados del centro histórico. Al atardecer es cuando más luce.",
               "The Alcazaba and Gibralfaro straight ahead, Málaga Cathedral and the rooftops of the old town. It is at its best at sunset.")),
            (t("¿A qué hora es mejor ir?", "What is the best time to go?"),
             t("Para el tardeo y la puesta de sol. Como no hay reservas, a primera hora de la tarde es más fácil encontrar sitio.",
               "Late afternoon and sunset. As there are no reservations, it is easier to get a spot early in the afternoon.")),
        ]),
        (t("Visitas y planes", "Visiting"), [
            (t("¿Es un buen restaurante para una cena especial?", "Is it a good place for a special dinner?"),
             t("Sí: la sala, la terraza acristalada de la última planta y las vistas a la Alcazaba iluminada lo hacen ideal para cenas en pareja y celebraciones.",
               "Yes: the dining room, the glass-roofed terrace on the top floor and the views of the floodlit Alcazaba make it ideal for dinners for two and celebrations.")),
            (t("¿Tenéis la carta y la web en inglés?", "Is the menu available in English?"),
             t("Sí. La carta, la web y el sistema de reservas están en español y en inglés.",
               "Yes. The menu, the website and the booking system are in English and Spanish.")),
            (t("¿Cómo llego?", "How do I get there?"),
             t(f'A pie desde cualquier punto del centro: Calle Victoria sale de la Plaza de la Merced. Más detalles en <a href="{c.link("contacto")}">Contacto y cómo llegar</a>.',
               f'On foot from anywhere in the centre: Calle Victoria starts at Plaza de la Merced. More details on <a href="{c.link("contacto")}">Contact & directions</a>.')),
            (t("¿Dónde puedo seguiros?", "Where can I follow you?"),
             t(f'En Instagram: <a href="{INSTAGRAM}" target="_blank" rel="noopener">@canitas_malaga</a>.',
               f'On Instagram: <a href="{INSTAGRAM}" target="_blank" rel="noopener">@canitas_malaga</a>.')),
        ]),
    ]


def all_faqs(c):
    return [qa for _, items in faq_groups(c) for qa in items]


def faq_page(c):
    t = c.t
    hero = page_hero(c, "Cañitas Málaga · Cañitas al Fresco", t("Preguntas frecuentes", "Frequently asked questions"),
                     t("Horarios, reservas, precios, la azotea y cómo llegar: todo lo que nos preguntan, con respuestas cortas.",
                       "Opening hours, bookings, prices, the rooftop and how to get here: everything people ask us, answered briefly."),
                     photo="canitas-malaga-sala-restaurante", crumbs=[t("Preguntas frecuentes", "FAQ")])
    blocks = []
    n = 0
    for title, items in faq_groups(c):
        rows = []
        for q, a in items:
            n += 1
            rows.append(f"""        <details class="accordion-item" open>
          <summary><span class="accordion-q"><span class="accordion-index">{n:02d}</span>{q}</span></summary>
          <div class="accordion-body"><p>{a}</p></div>
        </details>""")
        blocks.append(f"""  <section class="faq">
    <div class="section-inner faq-grid">
      <div class="faq-intro">
        <h2 class="section-title">{title}</h2>
      </div>
      <div class="accordion">
{chr(10).join(rows)}
      </div>
    </div>
  </section>""")
    main = f"""{hero}

  <section class="section section-tint">
    <div class="section-inner">
      <p class="eyebrow eyebrow-dark">{t('En resumen', 'At a glance')}</p>
      <h2 class="section-title">{t('Cañitas Málaga en 7 datos', 'Cañitas Málaga in 7 facts')}</h2>
      {facts(key_facts(c))}
    </div>
  </section>

{chr(10).join(blocks)}

{cta_band(c, t('¿Te esperamos?', 'Shall we save you a table?'),
          t('Reserva en el restaurante o sube sin reserva a la azotea.', 'Book the restaurant or come up to the rooftop, no booking needed.'),
          f'<a class="btn btn-primary-light" href="{c.link("reservas")}">{t("Reservar mesa", "Book a table")}</a>'
          f'<a class="btn btn-ghost-light" href="{c.link("carta")}">{t("Ver la carta", "See the menu")}</a>')}"""
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": c.lang,
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
                       for q, a in all_faqs(c)],
    }
    return dict(
        nav_title=t("Preguntas frecuentes", "FAQ"),
        title=t("Preguntas frecuentes | Cañitas Málaga y Cañitas al Fresco",
                "FAQ | Cañitas Málaga & Cañitas al Fresco rooftop"),
        desc=t("Horario, reservas, precios, carta, rooftop abierto al público y cómo llegar a Cañitas Málaga, en el hotel ME Málaga by Meliá (Calle Victoria 6).",
               "Opening hours, bookings, prices, menu, the public rooftop bar and directions to Cañitas Málaga at ME Málaga by Meliá (Calle Victoria 6)."),
        main=main,
        schema=[faq_ld, restaurant_ld(c), fresco_ld(c), breadcrumb_ld(c, t("Preguntas frecuentes", "FAQ"))],
    )


PAGES = {"faq": faq_page}
