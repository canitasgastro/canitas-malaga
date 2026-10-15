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
    # ---------- Cañitas Maite: espacios ----------
    "canitas-maite-malaga-comedor-privado": dict(
        src=(M, "COMEDOR PRIVADO - vertical.jpg"),
        es="Comedor privado de Cañitas Maite Málaga con mesa vestida, estanterías azules y lámparas suspendidas",
        en="Private dining room at Cañitas Maite Málaga with a laid table, blue shelving and pendant lamps"),
    "canitas-maite-malaga-comedor-privado-horizontal": dict(
        src=(M, "ESPACIOS - 39 (1).jpg"),
        es="Comedor privado para grupos en el restaurante Cañitas Maite, en el centro de Málaga",
        en="Private dining room for groups at Cañitas Maite restaurant in Málaga city centre"),
    "canitas-maite-malaga-sala-restaurante": dict(
        src=(M, "ESPACIOS - 23.jpg"),
        es="Sala del restaurante Cañitas Maite en ME Málaga by Meliá, con bancos corridos y paredes azules",
        en="Dining room of Cañitas Maite restaurant at ME Málaga by Meliá, with banquettes and blue walls"),
    "canitas-maite-malaga-sala-mesas": dict(
        src=(M, "ESPACIOS - 21.jpg"),
        es="Mesas vestidas en la sala de Cañitas Maite Málaga",
        en="Laid tables in the dining room of Cañitas Maite Málaga"),
    "canitas-maite-malaga-terraza": dict(
        src=(M, "CAÑITASMALAGA_TERRAZA - 13 (1).jpg"),
        es="Terraza acristalada de Cañitas Maite con olivos y mesas de madera en la última planta del hotel",
        en="Glass-roofed terrace at Cañitas Maite with olive trees and wooden tables on the hotel's top floor"),
    "canitas-maite-malaga-terraza-mesas": dict(
        src=(M, "CAÑITASMALAGA_TERRAZA - 7.jpg"),
        es="Mesas de la terraza de Cañitas Maite Málaga con vegetación y luz natural",
        en="Terrace tables at Cañitas Maite Málaga with greenery and natural light"),

    # ---------- Cañitas Maite: platos ----------
    "txuleta-vasca-parrilla-canitas-maite-malaga": dict(
        src=(M, "CAÑITASMALAGA_CHULETA - 1.jpg"),
        es="Txuleta vasca madurada, asada a la parrilla y laminada en Cañitas Maite Málaga",
        en="Dry-aged Basque txuleta steak, grilled and sliced, at Cañitas Maite Málaga"),
    "lubina-parrilla-pil-pil-canitas-maite-malaga": dict(
        src=(M, "CAÑITASMALAGA_LUBINA - 3 (1).jpg"),
        es="Lubina a la parrilla con pil pil de su colágeno en Cañitas Maite Málaga",
        en="Grilled sea bass with pil pil made from its own collagen at Cañitas Maite Málaga"),
    "lenguado-brasas-canitas-maite-malaga": dict(
        src=(M, "CAÑITASMALAGA_LENGUADO - 2.jpg"),
        es="Lenguado asado en brasas con meunière cítrica y alcaparras fritas",
        en="Ember-roasted sole with citrus meunière and fried capers"),
    "mejor-croqueta-del-mundo-jamon-joselito": dict(
        src=(M, "CROQUETA - 1.jpg"),
        es="La mejor croqueta del mundo 2021, de jamón Joselito, de Cañitas Maite",
        en="The Best Croquette in the World 2021, made with Joselito ham, by Cañitas Maite"),
    "berenjena-burrata-canitas-maite-malaga": dict(
        src=(M, "BERENJENA.jpg"),
        es="Berenjena ahumada a la parrilla con burrata fresca en Cañitas Maite Málaga",
        en="Smoked grilled aubergine with fresh burrata at Cañitas Maite Málaga"),
    "puerro-romesco-canitas-maite-malaga": dict(
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
    "chefs-cocina-canitas-maite-malaga": dict(
        src=(M, "Javi y Juan - 5.jpg"),
        es="Javier Sanz y Juan Sahuquillo en la cocina de Cañitas Maite Málaga",
        en="Javier Sanz and Juan Sahuquillo in the kitchen at Cañitas Maite Málaga"),
    "javier-sanz-chef-canitas-maite": dict(
        src=(M, "Javier Sanz - 1.jpg"),
        es="El chef Javier Sanz en la sala de Cañitas Maite Málaga",
        en="Chef Javier Sanz in the dining room at Cañitas Maite Málaga"),
    "juan-sahuquillo-chef-canitas-maite": dict(
        src=(M, "Juan Sahuquillo - 4.jpg"),
        es="El chef Juan Sahuquillo emplatando en la cocina de Cañitas Maite Málaga",
        en="Chef Juan Sahuquillo plating in the kitchen at Cañitas Maite Málaga"),

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

    # ---------- Mapa ----------
    "mapa-canitas-maite-malaga-calle-victoria": dict(
        src=(O, "mapa-calle-victoria.jpg"),
        es="Mapa del centro de Málaga con la ubicación de Cañitas Maite en Calle Victoria, 6",
        en="Map of Málaga city centre showing Cañitas Maite at Calle Victoria, 6"),
}

# Imágenes para compartir en redes (Open Graph): foto + logo, 1200x630.
OG = {
    "og-canitas-maite-malaga": dict(photo="canitas-maite-malaga-sala-restaurante", logo="maite", focus=0.55),
    "og-canitas-al-fresco": dict(photo="canitas-al-fresco-rooftop-piscina-malaga", logo="fresco", focus=0.45),
}

# Las cartas en PDF (origen en el disco de trabajo; se copian a assets/menus).
MENUS = {
    "carta-canitas-maite-malaga-es.pdf": "CARTARESTAURANTE_CAÑITASXME.pdf",
    "menu-canitas-maite-malaga-en.pdf": "ENG-CARTARESTAURANTE_CAÑITASXME.pdf",
    "carta-canitas-al-fresco-malaga-es.pdf": "ALFRESCO-POOL/CARTAPOOL_CAÑITASMAITEXMELIA.pdf",
    "menu-canitas-al-fresco-malaga-en.pdf": "ALFRESCO-POOL/ENG_CARTAPOOL_CAÑITASMAITEXMELIA.pdf",
}
