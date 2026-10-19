"""Cartas en HTML (indexables por Google), transcritas de los PDF vigentes.

Fuente: CARTARESTAURANTE_CAÑITASXME.pdf / ENG-CARTARESTAURANTE_CAÑITASXME.pdf (12-09)
        CARTAPOOL_CAÑITASMAITEXMELIA.pdf / ENG_CARTAPOOL_CAÑITASMAITEXMELIA.pdf (22-09)

Cada plato: (texto ES, texto EN, cantidad ES, cantidad EN, precio en euros).
Cuando cambie la carta, actualiza aquí los platos y precios y vuelve a ejecutar
python3 scripts/build.py
"""

MAITE_SET_MENUS = [
    dict(
        es_name="Menú Classics", en_name="Classics Menu",
        es_when="Todo a compartir · de lunes a jueves", en_when="Everything to share · Monday to Thursday",
        price=39,
        groups=[
            dict(es="A compartir", en="To share", items=[
                ("Torta de aceite y alioli", "Olive oil flatbread and aioli"),
                ("El mejor tomate del momento", "The best tomato of the moment"),
                ("Ensaladilla de gamba blanca al ajillo", "White prawn Russian salad al ajillo"),
                ("Berenjena asada con burrata aliñada", "Roasted aubergine with dressed burrata"),
                ("Langostinos a la parrilla y jugo de pollo al ast", "Grilled king prawns with rotisserie chicken jus"),
                ("Muslo de pollito campero a la parrilla y limón quemao'", "Grilled free-range chicken thigh with charred lemon"),
            ]),
            dict(es="Postre para terminar", en="Dessert to finish", items=[
                ("Tarta de queso cremosa y suave (2 personas)", "Smooth, creamy cheesecake (for 2)"),
            ], note=("Añade la mejor croqueta del mundo por +4 €", "Add the best croquette in the world for +€4")),
        ],
    ),
    dict(
        es_name="Menú Hits", en_name="Hits Menu",
        es_when="Todos los días", en_when="Every day",
        price=69,
        groups=[
            dict(es="Entrantes a compartir", en="Starters to share", items=[
                ("Torta de aceite y alioli", "Olive oil flatbread and aioli"),
                ("Tomates de temporada", "Seasonal tomatoes"),
                ("La mejor croqueta del mundo 2021", "The Best Croquette in the World 2021"),
                ("Ensaladilla de gamba blanca al ajillo", "White prawn Russian salad al ajillo"),
                ("Alcachofa en carbonara ibérica de torreznos", "Artichoke in Iberian carbonara with pork crackling"),
                ("Navajas a la parrilla con escabeche de limón asado", "Grilled razor clams with roasted lemon escabeche"),
                ("Calamar de anzuelo a la parrilla con velouté de Jabugo", "Line-caught grilled squid with Jabugo ham velouté"),
            ]),
            dict(es="Principal a elegir y a compartir (cada 2 personas)", en="Main course to choose and share (per 2 guests)", items=[
                ("Lubina a la parrilla con pil pil de su colágeno", "Grilled sea bass with pil pil made from its own collagen"),
                ("Txuleta vasca asada y madurada 45 días", "Roasted Basque txuleta, dry-aged for 45 days"),
            ], note=("Acompañado de guarnición del día", "Served with the garnish of the day")),
            dict(es="Postre para terminar", en="Dessert to finish", items=[
                ("El flan de nata fresca de oveja", "Fresh sheep's cream flan"),
            ]),
        ],
    ),
]

MAITE_CARTA = [
    dict(es="Para empezar con producto", en="To start, with the best produce", items=[
        ("Torta de aceite con AOVE del nuestro y alioli de ajo asado", "Olive oil flatbread with our own extra virgin olive oil and roasted garlic aioli", "2 pax", "for 2", 8),
        ("La Mejor Croqueta del Mundo 2021, de jamón Joselito", "The Best Croquette in the World 2021, made with Joselito ham", "2 uds", "2 pcs", 8),
        ("Boquerón gordo aliñado en casa con escabeche cítrico", "Plump fresh anchovies, house-marinated in citrus escabeche", "4 uds", "4 pcs", 9),
        ("Anchoa López sobada a mano con aceite y vinagre viejo", "López anchovies, hand-dressed with olive oil and aged vinegar", "2 uds", "2 pcs", 11),
        ("Gilda triple de bacalao con pan tomate a la brasa", "Triple salt-cod gilda with chargrilled tomato bread", "2 uds", "2 pcs", 14),
        ("Quisquilla en crudo con vinagreta de sus huevas", "Raw quisquilla shrimp with a vinaigrette of its own roe", "100 g", "100 g", 17),
        ("Atún rojo salvaje aliñado con jugo de piparra y manzanilla", "Wild bluefin tuna dressed with piparra pepper juice and manzanilla", "8 uds", "8 pcs", 19),
        ("Steak tartar de cadera de vaca madurada LyO", "LyO dry-aged beef rump steak tartare", "60 g", "60 g", 22),
        ("Cecina de wagyu japonés A5 cortada muy finita", "Japanese A5 wagyu cecina, very thinly sliced", "60 g", "60 g", 25),
    ]),
    dict(es="Verduras a nuestra manera", en="Vegetables, our way", items=[
        ("Patatitas mini asadas entre las ascuas con mayo picantita de adobo y romero quemao'", "Baby potatoes roasted in the embers with spicy adobo mayo and burnt rosemary", "", "", 14),
        ("Los mejores tomates del momento con aceite del bueno, sal en escamas y cebolleta fresca", "The best tomatoes of the moment with great olive oil, flaky salt and fresh spring onion", "", "", 16),
        ("Puerro confitado y asado a la llama con romesco de pipas de calabaza y almendritas fritas", "Confit, flame-roasted leek with pumpkin-seed romesco and fried almonds", "", "", 16),
        ("Berenjena ahumada en parrilla con burrata fresca, tomate seco en conserva y nueces tostadas", "Smoked grilled aubergine with fresh burrata, preserved dried tomatoes and toasted walnuts", "", "", 18),
        ("Alcachofas confitadas y fritas en carbonara ibérica de queso payoyo y torreznos de Soria", "Confit and fried artichokes in Iberian carbonara with Payoyo cheese and Soria pork crackling", "", "", 20),
        ("Setas silvestres de temporada a la parrilla con láminas de papada ibérica Joselito y trufa negra rallada", "Grilled seasonal wild mushrooms with slices of Joselito Iberian pork jowl and grated black truffle", "", "", 24),
    ]),
    dict(es="De concha y de cáscara", en="From the shell", items=[
        ("Ensaladilla de gamba blanca malagueña con jugo de piparras encurtidas y regañás artesanas", "Málaga white prawn Russian salad with pickled piparra juice and artisan regañá crackers", "", "", 17),
        ("Navajas de buceo a la parrilla con escabeche frío de limón asado y ralladura de limas frescas", "Hand-dived razor clams, grilled, with cold roasted-lemon escabeche and fresh lime zest", "8 uds", "8 pcs", 22),
        ("Langostinos del sur abiertos en mariposa y asados en parrilla con jugo de pollo al ast", "Southern king prawns, butterflied and grilled, with rotisserie chicken jus", "6 uds", "6 pcs", 24),
        ("Gambas rojas al ajillo a nuestra manera, patatitas chips super crujientes y dos huevos fritos con puntilla", "Red prawns al ajillo our way, with extra-crispy potato chips and two crispy-edged fried eggs", "9 uds", "9 pcs", 32),
    ]),
    dict(es="Carnes frescas del país", en="Fresh local meats", items=[
        ("Muslo de pollo campero criado en libertad con su caldito de asado y medio limón quemao'", "Free-range chicken thigh with its roasting juices and half a charred lemon", "", "", 22),
        ("Falda de cordero crujiente y melosa con su jugo reducido, aceite de hierbabuena y berros de agua", "Crispy, melting lamb flank with its reduced jus, mint oil and watercress", "", "", 32),
        ("Solomillo ibérico Joselito trinchado con salsa de pimienta a nuestra manera y patatitas chips", "Carved Joselito Iberian pork tenderloin with our pepper sauce and potato chips", "", "", 32),
        ("Molleja de ternera de leche con parmentier de coliflor tostada y salsa gravy de setas y mantequilla tostada", "Milk-fed veal sweetbreads with roasted cauliflower parmentier and mushroom brown-butter gravy", "~0,3 kg", "~0.3 kg", 36),
        ("Txuleta vasca de lomo bajo de vaca madurada 25 días, asada en parrilla abierta y laminada finita", "Basque txuleta: beef sirloin dry-aged for 25 days, grilled over an open fire and thinly sliced", "~0,7 kg", "~0.7 kg", 59),
    ]),
    dict(es="Pescados de una forma y de otra", en="Fish, one way or another", items=[
        ("Calamar de anzuelo entero a la parrilla y trinchado con velouté de mantequilla tostada y Jabugo", "Whole line-caught squid, grilled and carved, with brown butter and Jabugo ham velouté", "", "", 32),
        ("Medio pulpo gallego a la parrilla con chimichurri manchego y trinchat de patata y col a la gallega", "Half a Galician octopus, grilled, with Manchego chimichurri and Galician-style potato and cabbage", "", "", 34),
        ("Lenguado de estero asado en brasas, terminado con meunière tostada y cítrica y alcaparra frita", "Estuary sole roasted over embers, finished with a toasted citrus meunière and fried capers", "~0,6 kg", "~0.6 kg", 55),
        ("Lubina del Atlántico entera a la parrilla «sin trabajo» con pil pil de su colágeno y aceite de perejil", "Whole Atlantic sea bass, grilled and served “no work needed”, with pil pil from its own collagen and parsley oil", "~1 kg", "~1 kg", 65),
    ]),
]

FRESCO_CARTA = [
    dict(es="Entrantes top", en="Top starters", items=[
        ("La mejor croqueta del mundo", "The world's best croquette", "2 uds", "2 pcs", 8),
        ("Jamón ibérico con pan crujiente y tomate", "Iberian ham with crispy bread and tomato", "", "", 34),
        ("Guacamole casero con totopos crujientes", "Homemade guacamole with crispy tortilla chips", "", "", 19),
        ("Hummus, crudités encurtidos y torta de aceite", "Hummus, pickled crudités and olive oil flatbread", "", "", 19),
        ("Bowl de hojas verdes, aguacate y nueces", "Green leaf bowl with avocado and walnuts", "", "", 19),
        ("Ensaladilla de gambas blancas al ajillo y regañás", "White prawn Russian salad al ajillo with regañá crackers", "", "", 22),
        ("Tomate estilo caprese con burrata y pesto", "Caprese-style tomato with burrata and pesto", "", "", 22),
        ("Ensalada César de pollo campero y cherries", "Free-range chicken Caesar salad with cherry tomatoes", "", "", 22),
        ("Tartar de atún rojo, kimchi y arroz japonés", "Bluefin tuna tartare, kimchi and Japanese rice", "", "", 26),
        ("Pasta fresca con boloñesa y parmesano", "Fresh pasta with Bolognese and Parmesan", "", "", 26),
        ("Patatas crujientes hechas en casa (opción light, cocinadas en air fryer)", "Crispy homemade potatoes (light option, air-fried)", "", "", 14),
    ]),
    dict(es="Bocatería fina", en="Gourmet sandwiches",
         note=("Todos nuestros entrepanes vienen acompañados de patatas fritas.", "All our sandwiches are served with potato chips."), items=[
        ("Bikini trufado mixto con jamón cocido, queso fundido y lascas de parmesano", "Truffled ham and cheese bikini toastie with Parmesan shavings", "", "", 22),
        ("Sándwich vegetal con pan de semillas, aguacate, huevo cocido, lechuga y atún", "Veggie sandwich on seeded bread with avocado, boiled egg, lettuce and tuna", "", "", 24),
        ("Club sándwich versión Cañitas con huevo campero frito al momento y bacon crujiente", "Cañitas club sandwich with a freshly fried free-range egg and crispy bacon", "", "", 26),
        ("Brioche de pollo frito eco casero con lechuga picada finamente y pepino encurtido", "Homemade organic fried chicken brioche with shredded lettuce and pickled cucumber", "", "", 26),
        ("Burger de vaca gallega con bacon ahumado crujiente y sus toppings al gusto", "Galician beef burger with crispy smoked bacon and toppings of your choice", "", "", 28),
        ("Pizza de masa madre con jamón cocido del bueno, queso fundido, tomate y orégano fresco", "Sourdough pizza with premium cooked ham, melted cheese, tomato and fresh oregano", "", "", 28),
    ]),
    dict(es="Dulces", en="Sweets", items=[
        ("Fruta fresca de temporada sobre hielo pilé", "Fresh seasonal fruit on crushed ice", "", "", 16),
        ("Tarta de queso suave y cremosa con arándanos y confitura casera", "Smooth, creamy cheesecake with blueberries and homemade jam", "", "", 10),
        ("Torrija de panettone caramelizada al momento con helado de vainilla", "Panettone torrija, caramelised to order, with vanilla ice cream", "", "", 13),
    ]),
]
