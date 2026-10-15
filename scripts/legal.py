"""Páginas legales (ES / EN).

Los datos de empresa pendientes aparecen como <mark class="todo">[…]</mark> y se
ven resaltados en amarillo en la web. Cuando los tengas, rellena el diccionario
EMPRESA y vuelve a generar: python3 scripts/build.py
"""
from build import EMAIL, breadcrumb_ld, page_hero

UPDATED = {"es": "15 de octubre de 2026", "en": "15 October 2026"}

# Rellenar con los datos reales del titular de la web.
EMPRESA = {
    "razon_social": "CAÑITAS GASTRO, S.L.",
    "nif": "B24760928",
    "domicilio": "Travesía Molino, nº 2, 02200 Casas-Ibáñez (Albacete)",
    "registro": "",
    "email_privacidad": "",
    "dpo": "",
    "validez_bonos": "",
}


def d(key, label):
    v = EMPRESA.get(key)
    return v if v else f'<mark class="todo">[{label}]</mark>'


def legal_page(c, key, title, intro, sections, nav_title, seo_title, desc):
    t = c.t
    body = "\n".join(f'        <h2 id="s{i + 1}">{h}</h2>\n        {html}' for i, (h, html) in enumerate(sections))
    toc = "".join(f'<li><a href="#s{i + 1}">{h}</a></li>' for i, (h, _) in enumerate(sections))
    note = "" if c.lang == "es" else '<p class="legal-note">This English version is provided for convenience only. In the event of any discrepancy, the Spanish version shall prevail.</p>'
    hero = page_hero(c, t("Información legal", "Legal information"), title, intro, crumbs=[title], extra_cls="page-hero-compact")
    main = f"""{hero}

  <section class="section legal">
    <div class="section-inner legal-grid">
      <nav class="legal-toc" aria-label="{t('Índice', 'Contents')}">
        <p class="detail-eyebrow">{t('Índice', 'Contents')}</p>
        <ol>{toc}</ol>
      </nav>
      <article class="legal-body">
        <p class="legal-updated">{t('Última actualización', 'Last updated')}: {UPDATED[c.lang]}</p>
        {note}
{body}
      </article>
    </div>
  </section>"""
    return dict(nav_title=nav_title, title=seo_title, desc=desc, main=main, contact=False,
                schema=[breadcrumb_ld(c, title)])


def titular(c):
    t = c.t
    return f"""<ul class="legal-data">
          <li><strong>{t('Titular', 'Owner')}:</strong> {d('razon_social', t('RAZÓN SOCIAL', 'COMPANY NAME'))}</li>
          <li><strong>NIF:</strong> {d('nif', 'NIF / CIF')}</li>
          <li><strong>{t('Domicilio social', 'Registered office')}:</strong> {d('domicilio', t('DOMICILIO SOCIAL', 'REGISTERED ADDRESS'))}</li>
          <li><strong>{t('Datos registrales', 'Registration details')}:</strong> {d('registro', t('REGISTRO MERCANTIL, TOMO, FOLIO, HOJA', 'COMMERCIAL REGISTRY DETAILS'))}</li>
          <li><strong>{t('Establecimiento', 'Venue')}:</strong> Cañitas Málaga · Hotel ME Málaga by Meliá, Calle Victoria, 6, 29012 Málaga</li>
          <li><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>"""


# ---------------------------------------------------------------------------
def aviso(c):
    t = c.t
    s = [
        (t("Datos identificativos", "Identification details"),
         f"<p>{t('En cumplimiento del artículo 10 de la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:', 'In accordance with Article 10 of Spanish Law 34/2002 on Information Society Services and Electronic Commerce (LSSI-CE), the owner of this website is:')}</p>\n        {titular(c)}"),
        (t("Objeto", "Purpose"),
         f"<p>{t('Este sitio web informa sobre los espacios gastronómicos Cañitas Málaga y Cañitas al Fresco, situados en el hotel ME Málaga by Meliá, y permite consultar sus cartas, reservar mesa a través de un sistema de un proveedor externo y contactar con el establecimiento.', 'This website provides information about the Cañitas Málaga and Cañitas al Fresco venues at ME Málaga by Meliá, and allows users to view their menus, book a table through a third-party booking system and contact the venue.')}</p>"),
        (t("Condiciones de uso", "Terms of use"),
         f"<p>{t('El acceso a este sitio web es gratuito y atribuye la condición de usuario, que acepta este aviso legal. El usuario se compromete a hacer un uso adecuado de los contenidos y a no emplearlos para actividades ilícitas o contrarias a la buena fe.', 'Access to this website is free of charge and makes you a user, who accepts this legal notice. Users undertake to make appropriate use of the content and not to use it for unlawful purposes or in bad faith.')}</p>\n        <p>{t('Los precios y platos publicados son orientativos y pueden variar según temporada y disponibilidad de producto. La carta vigente es la disponible en el establecimiento.', 'Prices and dishes shown are for guidance and may change with the season and the availability of produce. The menu in force is the one available at the venue.')}</p>"),
        (t("Propiedad intelectual e industrial", "Intellectual and industrial property"),
         f"<p>{t('Todos los contenidos de este sitio web —textos, fotografías, logotipos, marcas, diseño gráfico y código— son propiedad del titular o de terceros que han autorizado su uso, y están protegidos por la normativa de propiedad intelectual e industrial. Las marcas «Cañitas Maite», «Cañitas Málaga» y «Cañitas al Fresco», así como «ME Málaga by Meliá», pertenecen a sus respectivos titulares. Queda prohibida su reproducción, distribución o transformación sin autorización expresa.', 'All content on this website (texts, photographs, logos, trademarks, graphic design and code) belongs to the owner or to third parties who have authorised its use, and is protected by intellectual and industrial property law. The trademarks “Cañitas Maite”, “Cañitas Málaga” and “Cañitas al Fresco”, as well as “ME Málaga by Meliá”, belong to their respective owners. Reproduction, distribution or modification without express permission is prohibited.')}</p>\n        <p>{t('La cartografía del mapa de contacto procede de OpenStreetMap (© colaboradores de OpenStreetMap, licencia ODbL).', 'The contact map uses OpenStreetMap data (© OpenStreetMap contributors, ODbL licence).')}</p>"),
        (t("Responsabilidad", "Liability"),
         f"<p>{t('El titular no se hace responsable de los daños derivados de interrupciones del servicio, errores técnicos o del uso indebido de la web. El sistema de reservas es prestado por un proveedor externo (CoverManager), que se rige por sus propias condiciones.', 'The owner is not liable for damage arising from service interruptions, technical errors or misuse of the website. The booking system is provided by a third party (CoverManager) under its own terms.')}</p>"),
        (t("Enlaces externos", "External links"),
         f"<p>{t('Este sitio contiene enlaces a sitios de terceros (Google Maps, Instagram, Meliá, CoverManager). El titular no controla ni es responsable de sus contenidos ni de sus políticas de privacidad.', 'This site contains links to third-party websites (Google Maps, Instagram, Meliá, CoverManager). The owner has no control over and is not responsible for their content or privacy policies.')}</p>"),
        (t("Legislación aplicable y jurisdicción", "Governing law and jurisdiction"),
         f"<p>{t('Este aviso legal se rige por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales que correspondan conforme a la normativa vigente; si el usuario es consumidor, los de su domicilio.', 'This legal notice is governed by Spanish law. Any dispute shall be submitted to the courts that have jurisdiction under applicable law; where the user is a consumer, those of the consumer’s place of residence.')}</p>"),
    ]
    title = t("Aviso legal", "Legal notice")
    return legal_page(c, "aviso", title, t("Información sobre el titular de esta web y las condiciones de uso.", "Information about the owner of this website and the terms of use."),
                      s, title, t("Aviso legal | Cañitas Málaga", "Legal notice | Cañitas Málaga"),
                      t("Aviso legal del sitio web de Cañitas Málaga: datos del titular, condiciones de uso y propiedad intelectual.", "Legal notice for the Cañitas Málaga website: owner details, terms of use and intellectual property."))


# ---------------------------------------------------------------------------
def privacidad(c):
    t = c.t
    priv_mail = d("email_privacidad", t("EMAIL DE PRIVACIDAD", "PRIVACY EMAIL"))
    rows = [
        (t("Reservas de mesa", "Table bookings"),
         t("Gestionar tu reserva, confirmarla y comunicarte cambios.", "To manage and confirm your booking and inform you of changes."),
         t("Ejecución de un contrato o medidas precontractuales (art. 6.1.b RGPD).", "Performance of a contract or pre-contractual steps (Art. 6(1)(b) GDPR)."),
         t("Hasta la celebración de la reserva y, después, durante los plazos legales de prescripción.", "Until the booking takes place and then for the legal limitation periods.")),
        (t("Consultas por email o teléfono", "Enquiries by email or phone"),
         t("Responder a tus preguntas.", "To answer your questions."),
         t("Consentimiento e interés legítimo en atender tu solicitud (art. 6.1.a y f RGPD).", "Consent and legitimate interest in answering your request (Art. 6(1)(a) and (f) GDPR)."),
         t("El tiempo necesario para resolver la consulta.", "As long as needed to resolve the enquiry.")),
        (t("Grupos y eventos", "Groups and events"),
         t("Preparar propuestas de menú y organizar tu evento.", "To prepare menu proposals and organise your event."),
         t("Medidas precontractuales y ejecución del contrato (art. 6.1.b RGPD).", "Pre-contractual steps and performance of the contract (Art. 6(1)(b) GDPR)."),
         t("Durante la relación y los plazos legales de conservación.", "For the duration of the relationship and legal retention periods.")),
        (t("Compra de bonos regalo (cuando esté disponible)", "Gift voucher purchases (when available)"),
         t("Gestionar la compra, el pago, el envío y el canje del bono.", "To process the purchase, payment, delivery and redemption of the voucher."),
         t("Ejecución del contrato y cumplimiento de obligaciones legales, fiscales y contables (art. 6.1.b y c RGPD).", "Performance of the contract and compliance with legal, tax and accounting obligations (Art. 6(1)(b) and (c) GDPR)."),
         t("Seis años según la normativa mercantil y fiscal.", "Six years under commercial and tax law.")),
        (t("Comunicaciones comerciales", "Marketing communications"),
         t("Enviarte novedades y promociones, solo si lo autorizas expresamente.", "To send you news and offers, only if you expressly agree."),
         t("Consentimiento (art. 6.1.a RGPD), que puedes retirar en cualquier momento.", "Consent (Art. 6(1)(a) GDPR), which you can withdraw at any time."),
         t("Hasta que retires tu consentimiento.", "Until you withdraw your consent.")),
        (t("Analítica web", "Web analytics"),
         t("Medir de forma agregada el uso de la web para mejorarla.", "To measure website usage in aggregate in order to improve it."),
         t("Consentimiento a través del banner de cookies (art. 6.1.a RGPD).", "Consent through the cookie banner (Art. 6(1)(a) GDPR)."),
         t("Según la política de cookies.", "As set out in the cookie policy.")),
    ]
    head = (t("Finalidad", "Purpose"), t("Para qué", "What for"), t("Base legal", "Legal basis"), t("Conservación", "Retention"))
    table = "<div class=\"table-wrap\"><table><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>" + "".join(
        "<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows) + "</tbody></table></div>"
    s = [
        (t("Responsable del tratamiento", "Data controller"), titular(c) + (f"\n        <p>{t('Delegado de protección de datos (si procede)', 'Data protection officer (if applicable)')}: {d('dpo', t('DATOS DEL DPO', 'DPO DETAILS'))}</p>")),
        (t("Qué datos tratamos", "What data we process"),
         f"<p>{t('Tratamos los datos que nos facilitas al reservar, escribirnos o comprar: nombre y apellidos, teléfono, email, número de comensales, fecha y hora, preferencias o alergias que nos indiques y, en su caso, datos de facturación. Los datos sobre alergias o intolerancias solo se usan para preparar tu servicio con seguridad.', 'We process the data you give us when booking, contacting us or making a purchase: name, phone number, email, number of guests, date and time, any preferences or allergies you tell us about and, where applicable, billing details. Allergy and intolerance information is used only to serve you safely.')}</p>"),
        (t("Finalidades, base legal y conservación", "Purposes, legal basis and retention"), table),
        (t("Destinatarios y encargados del tratamiento", "Recipients and processors"),
         f"<p>{t('No cedemos tus datos a terceros salvo obligación legal. Para prestar el servicio contamos con proveedores que actúan como encargados del tratamiento con contrato conforme al RGPD:', 'We do not share your data with third parties unless required by law. To provide our service we rely on providers acting as data processors under GDPR-compliant agreements:')}</p>\n        <ul><li>{t('CoverManager: sistema de reservas online.', 'CoverManager: online booking system.')}</li><li>{t('Proveedor de alojamiento web y del correo electrónico.', 'Web hosting and email providers.')}</li><li>{t('Adobe Fonts (Adobe Inc.): servicio de tipografías web.', 'Adobe Fonts (Adobe Inc.): web font service.')}</li><li>{t('Plataforma de pago (cuando se active la tienda de bonos regalo).', 'Payment platform (once the gift voucher shop goes live).')}</li></ul>\n        <p>{t('Comunicación de datos al hotel ME Málaga by Meliá', 'Disclosure of data to ME Málaga by Meliá')}: <mark class=\"todo\">[{t('INDICAR SI SE COMPARTEN DATOS CON EL HOTEL Y CON QUÉ FINALIDAD', 'STATE WHETHER DATA IS SHARED WITH THE HOTEL AND WHY')}]</mark></p>"),
        (t("Transferencias internacionales", "International transfers"),
         f"<p>{t('Si algún proveedor tratase datos fuera del Espacio Económico Europeo, lo hará con las garantías previstas en el RGPD, como decisiones de adecuación o cláusulas contractuales tipo de la Comisión Europea.', 'If any provider processes data outside the European Economic Area, it will do so with the safeguards required by the GDPR, such as adequacy decisions or the European Commission’s standard contractual clauses.')}</p>"),
        (t("Tus derechos", "Your rights"),
         f"<p>{t('Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, así como retirar tu consentimiento, escribiendo a', 'You can exercise your rights of access, rectification, erasure, objection, restriction of processing and portability, and withdraw your consent, by writing to')} {priv_mail} {t('e indicando el derecho que quieres ejercer.', 'stating which right you wish to exercise.')}</p>\n        <p>{t('Si consideras que no hemos atendido correctamente tu solicitud, puedes reclamar ante la Agencia Española de Protección de Datos', 'If you believe we have not handled your request properly, you can lodge a complaint with the Spanish Data Protection Agency')} (<a href=\"https://www.aepd.es\" target=\"_blank\" rel=\"noopener\">www.aepd.es</a>).</p>"),
        (t("Menores de edad", "Minors"),
         f"<p>{t('Los servicios de esta web no están dirigidos a menores de 14 años. Si eres menor, no nos facilites datos sin el consentimiento de tus padres o tutores.', 'The services on this website are not aimed at children under 14. If you are under 14, please do not give us any data without your parents’ or guardians’ consent.')}</p>"),
        (t("Seguridad", "Security"),
         f"<p>{t('Aplicamos las medidas técnicas y organizativas adecuadas para proteger tus datos frente a pérdida, uso indebido o acceso no autorizado.', 'We apply appropriate technical and organisational measures to protect your data against loss, misuse or unauthorised access.')}</p>"),
    ]
    title = t("Política de privacidad", "Privacy policy")
    return legal_page(c, "privacidad", title, t("Cómo tratamos tus datos personales cuando reservas, nos escribes o compras.", "How we handle your personal data when you book, contact us or buy from us."),
                      s, title, t("Política de privacidad | Cañitas Málaga", "Privacy policy | Cañitas Málaga"),
                      t("Política de privacidad de Cañitas Málaga: qué datos tratamos, para qué, durante cuánto tiempo y cómo ejercer tus derechos.", "Cañitas Málaga privacy policy: what data we process, why, for how long and how to exercise your rights."))


# ---------------------------------------------------------------------------
def cookies(c):
    t = c.t
    head = (t("Cookie / servicio", "Cookie / service"), t("Titular", "Provider"), t("Finalidad", "Purpose"), t("Tipo", "Type"), t("Duración", "Duration"))
    rows = [
        (t("Cookies técnicas de la web (WordPress)", "Website technical cookies (WordPress)"), t("Propia", "First party"),
         t("Funcionamiento básico de la web y del idioma elegido.", "Basic website operation and chosen language."), t("Técnica · exenta", "Technical · exempt"), t("Sesión", "Session")),
        (t("Cookie de consentimiento", "Consent cookie"), t("Propia", "First party"),
         t("Recordar tus preferencias de cookies.", "Remembers your cookie preferences."), t("Técnica · exenta", "Technical · exempt"), t("12 meses", "12 months")),
        ("CoverManager", "CoverManager",
         t("Funcionamiento del módulo de reservas integrado en la página Reservar mesa.", "Operation of the booking module embedded on the Book a table page."), t("Técnica de terceros", "Third-party technical"), t("Según CoverManager", "Set by CoverManager")),
        ("Google Analytics 4 (_ga, _ga_*)", "Google Ireland Ltd.",
         t("Estadísticas anónimas de uso. Solo se activan si las aceptas.", "Anonymous usage statistics. Only set if you accept them."), t("Analítica · requiere consentimiento", "Analytics · requires consent"), t("Hasta 24 meses", "Up to 24 months")),
    ]
    table = "<div class=\"table-wrap\"><table><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>" + "".join(
        "<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows) + "</tbody></table></div>"
    s = [
        (t("Qué son las cookies", "What cookies are"),
         f"<p>{t('Las cookies son pequeños archivos que una web guarda en tu navegador para que funcione correctamente, recordar tus preferencias o medir cómo se usa. Esta política explica cuáles usamos, conforme al artículo 22.2 de la LSSI-CE y a la guía sobre el uso de cookies de la Agencia Española de Protección de Datos.', 'Cookies are small files a website stores in your browser so that it works properly, remembers your preferences or measures how it is used. This policy explains which cookies we use, in accordance with Article 22.2 of the LSSI-CE and the Spanish Data Protection Agency’s guidance on cookies.')}</p>"),
        (t("Cookies que utilizamos", "Cookies we use"),
         f"{table}\n        <p>{t('Las tipografías Archivo y Federo se sirven desde nuestro propio servidor. La tipografía Custard se carga desde Adobe Fonts (Adobe Inc.), que no instala cookies pero recibe la dirección IP para servir la fuente y contabilizar su uso. El mapa de contacto es una imagen estática con enlace a Google Maps, por lo que no instala cookies.', 'The Archivo and Federo fonts are served from our own server. The Custard font is loaded from Adobe Fonts (Adobe Inc.), which does not set cookies but receives your IP address to serve the font and count its use. The contact map is a static image linking to Google Maps, so it sets no cookies.')}</p>\n        <p class=\"legal-note\">{t('La tabla se completará con la configuración definitiva de analítica y del gestor de consentimiento.', 'This table will be completed once analytics and the consent manager are fully configured.')}</p>"),
        (t("Cómo aceptar, rechazar o cambiar tu elección", "How to accept, reject or change your choice"),
         f"<p>{t('Al entrar en la web te mostramos un banner para aceptar, rechazar o configurar las cookies no técnicas. Rechazar es tan fácil como aceptar, y puedes cambiar tu elección en cualquier momento desde el enlace «Configurar cookies» del pie de página.', 'When you first visit the website, a banner lets you accept, reject or configure non-technical cookies. Rejecting is as easy as accepting, and you can change your choice at any time from the “Cookie settings” link in the footer.')}</p>\n        <p>{t('También puedes bloquear o borrar las cookies desde la configuración de tu navegador:', 'You can also block or delete cookies in your browser settings:')} <a href=\"https://support.google.com/chrome/answer/95647\" target=\"_blank\" rel=\"noopener\">Chrome</a>, <a href=\"https://support.apple.com/es-es/guide/safari/sfri11471/mac\" target=\"_blank\" rel=\"noopener\">Safari</a>, <a href=\"https://support.mozilla.org/es/kb/habilitar-y-deshabilitar-cookies-sitios-web-rastrear-preferencias\" target=\"_blank\" rel=\"noopener\">Firefox</a>, <a href=\"https://support.microsoft.com/es-es/microsoft-edge\" target=\"_blank\" rel=\"noopener\">Edge</a>.</p>"),
        (t("Más información", "More information"),
         f"<p>{t('Para saber cómo tratamos los datos personales consulta la', 'To find out how we handle personal data, see our')} <a href=\"{c.link('privacidad')}\">{t('política de privacidad', 'privacy policy')}</a>.</p>"),
    ]
    title = t("Política de cookies", "Cookie policy")
    return legal_page(c, "cookies", title, t("Qué cookies usa esta web y cómo puedes gestionarlas.", "Which cookies this website uses and how you can manage them."),
                      s, title, t("Política de cookies | Cañitas Málaga", "Cookie policy | Cañitas Málaga"),
                      t("Política de cookies de la web de Cañitas Málaga: qué cookies usamos y cómo aceptarlas, rechazarlas o configurarlas.", "Cañitas Málaga cookie policy: which cookies we use and how to accept, reject or configure them."))


# ---------------------------------------------------------------------------
def condiciones(c):
    t = c.t
    validez = d("validez_bonos", t("PLAZO DE VALIDEZ, p. ej. 12 MESES", "VALIDITY PERIOD, e.g. 12 MONTHS"))
    s = [
        (t("Vendedor", "Seller"), titular(c)),
        (t("Objeto", "Scope"),
         f"<p>{t('Estas condiciones regulan la compra online de bonos regalo y experiencias gastronómicas de Cañitas Málaga a través de esta web. La tienda online estará disponible próximamente.', 'These terms govern the online purchase of Cañitas Málaga gift vouchers and food experiences through this website. The online shop will be available soon.')}</p>"),
        (t("Precios y pago", "Prices and payment"),
         f"<p>{t('Los precios se indican en euros e incluyen el IVA aplicable. El pago se realiza en el momento de la compra mediante los medios de pago seguros que se muestren en el proceso de compra.', 'Prices are shown in euros and include applicable VAT. Payment is made at the time of purchase using the secure payment methods shown at checkout.')}</p>"),
        (t("Entrega", "Delivery"),
         f"<p>{t('El bono se envía por email a la dirección indicada en la compra, normalmente en pocos minutos. Si no lo recibes, revisa la carpeta de spam o escríbenos a', 'The voucher is sent by email to the address given at checkout, usually within minutes. If you do not receive it, check your spam folder or email us at')} <a href=\"mailto:{EMAIL}\">{EMAIL}</a>.</p>"),
        (t("Validez y uso", "Validity and use"),
         f"<ul><li>{t('Validez', 'Validity')}: {validez} {t('desde la fecha de compra.', 'from the date of purchase.')}</li><li>{t('Para canjearlo, indica el código del bono al reservar y preséntalo en el establecimiento.', 'To redeem it, quote the voucher code when booking and show it at the venue.')}</li><li>{t('No es canjeable por dinero ni acumulable a otras promociones, salvo que se indique lo contrario.', 'It cannot be exchanged for cash or combined with other offers unless stated otherwise.')}</li><li>{t('Recuerda que Cañitas al Fresco no admite reservas; consulta las condiciones de uso del bono en ese espacio.', 'Please note that Cañitas al Fresco does not take reservations; check the voucher terms for that venue.')}</li></ul>"),
        (t("Derecho de desistimiento", "Right of withdrawal"),
         f"<p>{t('Dispones de 14 días naturales desde la compra para desistir sin necesidad de justificación, siempre que el bono no se haya utilizado, conforme al Real Decreto Legislativo 1/2007 (TRLGDCU). Para ejercerlo, escríbenos a', 'You have 14 calendar days from purchase to withdraw without giving a reason, provided the voucher has not been used, in accordance with Spanish consumer law (Royal Legislative Decree 1/2007). To do so, email us at')} <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. {t('Te devolveremos el importe por el mismo medio de pago en un plazo máximo de 14 días.', 'We will refund you using the same payment method within 14 days.')}</p>"),
        (t("Atención al cliente y reclamaciones", "Customer service and complaints"),
         f"<p>{t('Para cualquier incidencia escríbenos a', 'For any issue, email us at')} <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. {t('El establecimiento dispone de hojas de reclamaciones oficiales de la Junta de Andalucía a disposición de los consumidores.', 'Official Andalusian Government complaint forms are available to consumers at the venue.')}</p>"),
        (t("Legislación aplicable", "Governing law"),
         f"<p>{t('Estas condiciones se rigen por la legislación española. Si eres consumidor, serán competentes los juzgados de tu domicilio.', 'These terms are governed by Spanish law. If you are a consumer, the courts of your place of residence shall have jurisdiction.')}</p>"),
    ]
    title = t("Condiciones de compra", "Terms of purchase")
    return legal_page(c, "condiciones", title, t("Condiciones de la compra online de bonos regalo y experiencias.", "Terms for buying gift vouchers and experiences online."),
                      s, title, t("Condiciones de compra | Cañitas Málaga", "Terms of purchase | Cañitas Málaga"),
                      t("Condiciones de compra de los bonos regalo y experiencias de Cañitas Málaga: precio, entrega, validez y desistimiento.", "Terms of purchase for Cañitas Málaga gift vouchers and experiences: price, delivery, validity and withdrawal."))


PAGES = {"aviso": aviso, "privacidad": privacidad, "cookies": cookies, "condiciones": condiciones}
