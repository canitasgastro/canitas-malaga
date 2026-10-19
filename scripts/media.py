"""Catálogo único de fotografías de la web.

Cada entrada define el nombre SEO del archivo final, la foto original (dentro
de imagenes/, que no se versiona) y el texto alternativo en español e inglés.
Lo usan scripts/process_images.py (para generar los JPG) y scripts/build.py
(para escribir los <img> y la tabla de textos alternativos de WordPress).
"""

M = "canitas malaga"
F = "alfresco-pool"
H = "hotel"
O = "otros"

PHOTOS = {
    # ---------- Cañitas Maite Restaurante: espacios ----------
    "canitas-malaga-comedor-privado": dict(
        src=(M, "COMEDOR PRIVADO - vertical.jpg"),
        es="Comedor privado de Cañitas Maite Restaurante con mesa vestida, estanterías azules y lámparas suspendidas",
        en="Private dining room at Cañitas Maite Restaurante with a laid table, blue shelving and pendant lamps"),
    "canitas-malaga-comedor-privado-horizontal": dict(
        src=(M, "ESPACIOS - 39 (1).jpg"),
        es="Comedor privado para grupos en el restaurante Cañitas Maite, en el centro de Málaga",
        en="Private dining room for groups at Cañitas Maite restaurant in Málaga city centre"),
    "canitas-malaga-sala-restaurante": dict(
        src=(M, "ESPACIOS - 23.jpg"),
        es="Sala del restaurante Cañitas Maite en ME Málaga by Meliá, con bancos corridos y paredes azules",
        en="Dining room of Cañitas Maite restaurant at ME Málaga by Meliá, with banquettes and blue walls"),
    "canitas-malaga-sala-mesas": dict(
        src=(M, "ESPACIOS - 21.jpg"),
        es="Mesas vestidas en la sala de Cañitas Maite Restaurante",
        en="Laid tables in the dining room of Cañitas Maite Restaurante"),
    "canitas-malaga-terraza": dict(
        src=(M, "CAÑITASMALAGA_TERRAZA - 13 (1).jpg"),
        es="Terraza acristalada de Cañitas Maite Restaurante con olivos y mesas de madera en la última planta del hotel",
        en="Glass-roofed terrace at Cañitas Maite Restaurante with olive trees and wooden tables on the hotel's top floor"),
    "canitas-malaga-terraza-mesas": dict(
        src=(M, "CAÑITASMALAGA_TERRAZA - 7.jpg"),
        es="Mesas de la terraza de Cañitas Maite Restaurante con vegetación y luz natural",
        en="Terrace tables at Cañitas Maite Restaurante with greenery and natural light"),

    # ---------- Cañitas Maite Restaurante: platos ----------
    "txuleta-vasca-parrilla-canitas-malaga": dict(
        src=(M, "CAÑITASMALAGA_CHULETA - 1.jpg"),
        es="Txuleta vasca madurada, asada a la parrilla y laminada en Cañitas Maite Restaurante",
        en="Dry-aged Basque txuleta steak, grilled and sliced, at Cañitas Maite Restaurante"),
    "lubina-parrilla-pil-pil-canitas-malaga": dict(
        src=(M, "CAÑITASMALAGA_LUBINA - 3 (1).jpg"),
        es="Lubina a la parrilla con pil pil de su colágeno en Cañitas Maite Restaurante",
        en="Grilled sea bass with pil pil made from its own collagen at Cañitas Maite Restaurante"),
    "lenguado-brasas-canitas-malaga": dict(
        src=(M, "CAÑITASMALAGA_LENGUADO - 2.jpg"),
        es="Lenguado asado en brasas con meunière cítrica y alcaparras fritas",
        en="Ember-roasted sole with citrus meunière and fried capers"),
    "mejor-croqueta-del-mundo-jamon-joselito": dict(
        src=(M, "CROQUETA - 1.jpg"),
        es="La mejor croqueta del mundo 2021, de jamón Joselito, de Cañitas Maite",
        en="The Best Croquette in the World 2021, made with Joselito ham, by Cañitas Maite"),
    "berenjena-burrata-canitas-malaga": dict(
        src=(M, "BERENJENA.jpg"),
        es="Berenjena ahumada a la parrilla con burrata fresca en Cañitas Maite Restaurante",
        en="Smoked grilled aubergine with fresh burrata at Cañitas Maite Restaurante"),
    "puerro-romesco-canitas-malaga": dict(
        src=(M, "PUERRO.jpg"),
        es="Puerro confitado y asado a la llama con romesco y almendras fritas",
        en="Confit, flame-roasted leek with romesco and fried almonds"),

    # ---------- Chefs ----------
    "javier-sanz-juan-sahuquillo-chefs-canitas-maite": dict(
        src=(M, "Javi y Juan - 4.jpg"),
        es="Javier Sanz y Juan Sahuquillo, chefs de Cañitas Maite, en el restaurante de Málaga",
        en="Javier Sanz and Juan Sahuquillo, chefs of Cañitas Maite, at the Málaga restaurant"),
    "chefs-canitas-maite-alcazaba-malaga": dict(
        src=(M, "Javi y Juan - 8.jpg"),
        es="Los chefs Javier Sanz y Juan Sahuquillo con la Alcazaba de Málaga al fondo",
        en="Chefs Javier Sanz and Juan Sahuquillo with the Alcazaba of Málaga behind them"),
    "chefs-cocina-canitas-malaga": dict(
        src=(M, "Javi y Juan - 5.jpg"),
        es="Javier Sanz y Juan Sahuquillo en la cocina de Cañitas Maite Restaurante",
        en="Javier Sanz and Juan Sahuquillo in the kitchen at Cañitas Maite Restaurante"),
    "javier-sanz-chef-canitas-maite": dict(
        src=(M, "Javier Sanz - 1.jpg"),
        es="El chef Javier Sanz en la sala de Cañitas Maite Restaurante",
        en="Chef Javier Sanz in the dining room at Cañitas Maite Restaurante"),
    "juan-sahuquillo-chef-canitas-maite": dict(
        src=(M, "Juan Sahuquillo - 4.jpg"),
        es="El chef Juan Sahuquillo emplatando en la cocina de Cañitas Maite Restaurante",
        en="Chef Juan Sahuquillo plating in the kitchen at Cañitas Maite Restaurante"),

    # ---------- Cañitas al Fresco ----------
    "canitas-al-fresco-rooftop-piscina-malaga": dict(
        src=(M, "ESPACIOS - 48 (1).jpg"),
        es="Rooftop y piscina de Cañitas al Fresco con la Alcazaba de Málaga al fondo",
        en="Cañitas al Fresco rooftop and pool with the Alcazaba of Málaga in the background"),
    "bikini-trufado-patatas-canitas-al-fresco": dict(
        src=(F, "DSC_5077.jpg"),
        es="Bikini trufado y sándwiches con patatas fritas caseras en Cañitas al Fresco",
        en="Truffled bikini toastie and sandwiches with homemade crisps at Cañitas al Fresco"),
    "guacamole-casero-canitas-al-fresco": dict(
        src=(F, "GUACAMOLE.jpg"),
        es="Guacamole casero con totopos crujientes en el rooftop Cañitas al Fresco",
        en="Homemade guacamole with crispy tortilla chips on the Cañitas al Fresco rooftop"),
    "hamburguesa-vaca-gallega-canitas-al-fresco": dict(
        src=(F, "HAMBURGUESA.jpg"),
        es="Burger de vaca gallega con bacon ahumado y patatas en Cañitas al Fresco",
        en="Galician beef burger with smoked bacon and crisps at Cañitas al Fresco"),
    "hummus-crudites-canitas-al-fresco": dict(
        src=(F, "HUMMUS.jpg"),
        es="Hummus con crudités encurtidos y torta de aceite en Cañitas al Fresco",
        en="Hummus with pickled crudités and olive oil flatbread at Cañitas al Fresco"),
    "ensalada-cesar-canitas-al-fresco": dict(
        src=(F, "ENSALADA CESAR.jpg"),
        es="Ensalada César de pollo campero servida en la azotea de Cañitas al Fresco",
        en="Free-range chicken Caesar salad served on the Cañitas al Fresco rooftop"),
    "ensaladilla-gamba-blanca-canitas-al-fresco": dict(
        src=(F, "ENSALADILLA.jpg"),
        es="Ensaladilla de gamba blanca junto a la piscina de Cañitas al Fresco",
        en="White prawn Russian salad by the pool at Cañitas al Fresco"),
    "tarta-de-queso-canitas-al-fresco": dict(
        src=(F, "TARTA DE QUESO.jpg"),
        es="Tarta de queso suave y cremosa con arándanos y confitura casera",
        en="Smooth, creamy cheesecake with blueberries and homemade jam"),

    # ---------- Hotel ME Málaga ----------
    "me-malaga-piscina-rooftop": dict(
        src=(H, "hotel-pool-1.jpg"),
        es="Piscina infinity en la azotea de ME Málaga by Meliá, con tumbonas y vistas a la ciudad",
        en="Infinity pool on the rooftop of ME Málaga by Meliá, with sun loungers and city views"),
    "me-malaga-piscina-catedral": dict(
        src=(H, "hotel-pool-2.jpg"),
        es="Piscina de ME Málaga con la Catedral y el casco histórico al fondo",
        en="ME Málaga pool with the Cathedral and the old town in the background"),
    "me-malaga-terraza-alcazaba": dict(
        src=(H, "hotel-terraza.jpg"),
        es="Terraza de ME Málaga al atardecer con la Alcazaba al fondo",
        en="ME Málaga terrace at sunset with the Alcazaba in the background"),
    "me-malaga-lobby-escalera": dict(
        src=(H, "hotel-lobby.jpg"),
        es="Escalera escultórica en el lobby del hotel ME Málaga by Meliá",
        en="Sculptural staircase in the lobby of ME Málaga by Meliá"),


    # ---------- Hotel ME Málaga: interior y habitaciones (fotos oficiales de Meliá) ----------
    "me-malaga-habitacion-vistas-catedral": dict(
        src=(H, "melia-4BjT7Rvf97X1KUN5vjb4.jpg"),
        es="Habitación de ME Málaga by Meliá con techo pintado y vistas a la Catedral de Málaga",
        en="Room at ME Málaga by Meliá with a painted ceiling and views of Málaga Cathedral"),
    "me-malaga-habitacion-techo-pintado": dict(
        src=(H, "melia-PrHWPw7oWbbvA3dsYzrp.jpg"),
        es="Dormitorio de ME Málaga con techo pintado a mano, maderas cálidas y cojines azules",
        en="ME Málaga bedroom with a hand-painted ceiling, warm wood and blue cushions"),
    "me-malaga-salon-biblioteca": dict(
        src=(H, "melia-yoyP4okSc51ij4KpBARx.jpg"),
        es="Salón con biblioteca de madera y sofás de diseño en el hotel ME Málaga by Meliá",
        en="Lounge with wooden library shelves and designer sofas at ME Málaga by Meliá"),
    "me-malaga-suite-salon-comedor": dict(
        src=(H, "melia-B1eRFtmzkf8beucPJYcB.jpg"),
        es="Salón y comedor de una suite de ME Málaga con vistas al centro de Málaga",
        en="Living and dining area of a suite at ME Málaga overlooking Málaga city centre"),
    "me-malaga-suite-bano-banera": dict(
        src=(H, "melia-Pdo3VnNQr6PturWtXiKy.jpg"),
        es="Baño de suite en ME Málaga con bañera exenta y ducha de azulejo verde",
        en="Suite bathroom at ME Málaga with a freestanding bath and green-tiled shower"),
    "me-malaga-suite-salon-arte": dict(
        src=(H, "melia-gGDFZ6pdifFFTCwX8W4P.jpg"),
        es="Salón de suite en ME Málaga con obra de arte contemporáneo y sofá",
        en="Suite living room at ME Málaga with contemporary artwork and a sofa"),

    # ---------- Desayunos ----------
    "desayuno-buffet-productores-locales-malaga": dict(
        src=(M, "DESAYUNOS - 25.jpg"),
        es="Buffet de desayuno de Cañitas Maite en ME Málaga, con productos de pequeños productores",
        en="Cañitas Maite breakfast buffet at ME Málaga, with produce from small local producers"),
    "desayuno-panes-masa-madre-malaga": dict(
        src=(M, "DESAYUNOS - 7.jpg"),
        es="Hogazas y panes de masa madre de obradores de Málaga en el desayuno de Cañitas Maite",
        en="Sourdough loaves from Málaga bakeries at the Cañitas Maite breakfast"),
    "desayuno-fruta-quesos-locales": dict(
        src=(M, "DESAYUNOS - 12.jpg"),
        es="Fruta de temporada de la provincia y quesos artesanos en el desayuno de ME Málaga",
        en="Seasonal fruit from the province and artisan cheeses at the ME Málaga breakfast"),
    "desayuno-chacinas-embutidos": dict(
        src=(M, "DESAYUNOS - 8.jpg"),
        es="Chacinas y embutidos de carnicerías de pueblo en el desayuno de Cañitas Maite",
        en="Cured meats and sausages from village butchers at the Cañitas Maite breakfast"),
    "desayuno-platos-calientes-cazuelas": dict(
        src=(M, "DESAYUNOS - 28.jpg"),
        es="Platos calientes en cazuelas de hierro en el desayuno brunch de Cañitas Maite",
        en="Hot dishes in cast-iron pots at the Cañitas Maite breakfast and brunch"),
    "desayuno-bolleria-tradicional": dict(
        src=(M, "DESAYUNOS - 10.jpg"),
        es="Bollería tradicional y panes de pequeños obradores para el desayuno en Málaga centro",
        en="Traditional pastries and breads from small bakeries for breakfast in central Málaga"),
    "desayuno-huevos-fritos-papada": dict(
        src=(M, "CAÑITASMALAGA_HUEVOS FRITOS CON PAPADA JOSELITO - 1.jpg"),
        es="Huevos fritos con puntilla y papada ibérica, uno de los platos especiales del desayuno",
        en="Crispy-edged fried eggs with Iberian pork jowl, one of the breakfast specials"),
    "desayuno-omelette-cremosa": dict(
        src=(M, "CAÑITASMALAGA_OMELETTE - 3.jpg"),
        es="Omelette cremosa hecha al momento en el desayuno de Cañitas Maite",
        en="Creamy omelette made to order at the Cañitas Maite breakfast"),

    # ---------- Eventos ----------
    "evento-empresa-rooftop-atardecer-malaga": dict(
        src=("eventos", "evento-rooftop-cocktail.jpg"),
        es="Evento de empresa al atardecer en el rooftop de ME Málaga, con vistas al centro de Málaga",
        en="Corporate event at sunset on the ME Málaga rooftop, overlooking Málaga city centre"),
    "evento-cocteles-alcazaba": dict(
        src=("eventos", "evento-cocteles.jpg"),
        es="Cócteles de bienvenida servidos frente a la Alcazaba en un evento de Cañitas Maite",
        en="Welcome cocktails served facing the Alcazaba at a Cañitas Maite event"),
    "evento-mesa-finger-food": dict(
        src=("eventos", "evento-finger-food.jpg"),
        es="Mesa de quesos, panes y finger food para un evento de empresa en Málaga",
        en="Table of cheeses, breads and finger food for a corporate event in Málaga"),
    "evento-croquetas-pase": dict(
        src=("eventos", "evento-croquetas.jpg"),
        es="Pase de la mejor croqueta del mundo 2021 en un cóctel de empresa",
        en="The Best Croquette in the World 2021 passed around at a corporate cocktail"),
    "evento-coffee-break": dict(
        src=("eventos", "evento-coffee-break.jpg"),
        es="Coffee break con bollería artesana para reuniones de empresa en ME Málaga",
        en="Coffee break with artisan pastries for business meetings at ME Málaga"),
    "me-malaga-lobby-bar": dict(
        src=("enelobbybar", "ESPACIOS - 37.jpg"),
        es="Lobby bar del hotel ME Málaga by Meliá, con barra circular y luz cálida",
        en="Lobby bar at ME Málaga by Meliá, with a round bar and warm lighting"),

    # ---------- Bonos regalo ----------
    "tarjeta-regalo-canitas-maite-malaga": dict(
        src=(O, "tarjeta-regalo-mockup.png"),
        es="Tarjeta regalo para 2 personas de Cañitas Maite Restaurante en ME Málaga",
        en="Gift card for 2 from Cañitas Maite Restaurante at ME Málaga"),

    # ---------- Mapa ----------
    "mapa-canitas-malaga-calle-victoria": dict(
        src=(O, "mapa-calle-victoria.jpg"),
        es="Mapa del centro de Málaga con la ubicación de Cañitas Maite Restaurante en Calle Victoria, 6",
        en="Map of Málaga city centre showing Cañitas Maite Restaurante at Calle Victoria, 6"),
}

# Imágenes para compartir en redes (Open Graph): foto + logo, 1200x630.
OG = {
    "og-canitas-malaga": dict(photo="canitas-malaga-sala-restaurante", logo="maite", focus=0.55),
    "og-canitas-al-fresco": dict(photo="canitas-al-fresco-rooftop-piscina-malaga", logo="fresco", focus=0.45),
}
