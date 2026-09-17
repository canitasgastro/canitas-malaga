import os
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENES = os.path.join(BASE, "imagenes")
OUT_IMG = os.path.join(BASE, "assets", "img")
OUT_LOGO = os.path.join(BASE, "assets", "logos")
os.makedirs(OUT_IMG, exist_ok=True)
os.makedirs(OUT_LOGO, exist_ok=True)

def save_photo(src, dst, max_w, quality=78):
    im = Image.open(src)
    im = im.convert("RGB")
    if im.width > max_w:
        h = int(im.height * (max_w / im.width))
        im = im.resize((max_w, h), Image.LANCZOS)
    im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
    print(dst, im.size, os.path.getsize(dst) // 1024, "KB")

def save_logo_png(src, dst, max_w=600):
    im = Image.open(src)
    im = im.convert("RGBA")
    if im.width > max_w:
        h = int(im.height * (max_w / im.width))
        im = im.resize((max_w, h), Image.LANCZOS)
    im.save(dst, "PNG", optimize=True)
    print(dst, im.size, os.path.getsize(dst) // 1024, "KB")

photos = [
    (os.path.join(IMAGENES, "enelobbybar", "ESPACIOS - 37.jpg"), os.path.join(OUT_IMG, "ene-hero.jpg"), 1700),
    (os.path.join(IMAGENES, "canitas malaga", "CAÑITASMALAGA_TERRAZA - 13 (1).jpg"), os.path.join(OUT_IMG, "maite-hero.jpg"), 1700),
    (os.path.join(IMAGENES, "canitas malaga", "ESPACIOS - 48 (1).jpg"), os.path.join(OUT_IMG, "fresco-hero.jpg"), 1700),

    (os.path.join(IMAGENES, "enelobbybar", "ESPACIOS - 37.jpg"), os.path.join(OUT_IMG, "ene-detail.jpg"), 1300),
    (os.path.join(IMAGENES, "canitas malaga", "CAÑITASMALAGA_CHULETA - 1.jpg"), os.path.join(OUT_IMG, "maite-detail.jpg"), 1300),
    (os.path.join(IMAGENES, "canitas malaga", "CROQUETA - 1.jpg"), os.path.join(OUT_IMG, "maite-croqueta.jpg"), 1300),
    (os.path.join(IMAGENES, "alfresco-pool", "DSC_5077.jpg"), os.path.join(OUT_IMG, "fresco-detail.jpg"), 1300),
    (os.path.join(IMAGENES, "alfresco-pool", "GUACAMOLE.jpg"), os.path.join(OUT_IMG, "fresco-guacamole.jpg"), 1300),

    (os.path.join(IMAGENES, "canitas malaga", "Javi y Juan - 4.jpg"), os.path.join(OUT_IMG, "chefs.jpg"), 1400),
]

for src, dst, w in photos:
    if os.path.exists(src):
        save_photo(src, dst, w)
    else:
        print("MISSING", src)

logos = [
    (os.path.join(IMAGENES, "enelobbybar", "Capa 1-2 (3).png"), os.path.join(OUT_LOGO, "ene-cream.png")),
    (os.path.join(IMAGENES, "enelobbybar", "Capa 1-2.png"), os.path.join(OUT_LOGO, "ene-color.png")),
    (os.path.join(IMAGENES, "alfresco-pool", "CAÑITASALFRESCO.webp"), os.path.join(OUT_LOGO, "fresco-cream.png")),
    (os.path.join(IMAGENES, "alfresco-pool", "CAÑITASALFRESCOLOGO.webp"), os.path.join(OUT_LOGO, "fresco-color.png")),
]
for src, dst in logos:
    if os.path.exists(src):
        save_logo_png(src, dst)
    else:
        print("MISSING", src)

# Sample a swatch color from the al fresco logo (olive tone) for CSS
im = Image.open(os.path.join(IMAGENES, "alfresco-pool", "CAÑITASALFRESCOLOGO.webp")).convert("RGBA")
w, h = im.size
samples = []
for x in range(0, w, max(1, w // 40)):
    for y in range(0, h, max(1, h // 40)):
        r, g, b, a = im.getpixel((x, y))
        if a > 200 and not (r > 230 and g > 230 and b > 230) and not (r < 20 and g < 20 and b < 20):
            samples.append((r, g, b))
if samples:
    avg = tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
    print("Al fresco olive swatch approx:", "#%02x%02x%02x" % avg, "from", len(samples), "samples")

# Same for eñe orange
im2 = Image.open(os.path.join(IMAGENES, "enelobbybar", "Capa 1-2.png")).convert("RGBA")
w2, h2 = im2.size
samples2 = []
for x in range(0, w2, max(1, w2 // 40)):
    for y in range(0, h2, max(1, h2 // 40)):
        r, g, b, a = im2.getpixel((x, y))
        if a > 200 and not (r > 230 and g > 230 and b > 230):
            samples2.append((r, g, b))
if samples2:
    avg2 = tuple(sum(c[i] for c in samples2) // len(samples2) for i in range(3))
    print("Eñe orange swatch approx:", "#%02x%02x%02x" % avg2, "from", len(samples2), "samples")
