"""Genera todas las imágenes de la web a partir del material original.

Requiere Pillow y PyMuPDF (pip install pillow pymupdf).

  python scripts/process_images.py

Salidas:
  assets/img/<nombre>.jpg y <nombre>-800.jpg   fotos para la web (1600 px y 800 px)
  assets/img/og-*.jpg                          imágenes para compartir en redes (1200x630)
  assets/icons/                                favicon PNG, apple-touch-icon e iconos de la app
  assets/menus/                                cartas en PDF (ES / EN)
  wordpress/01-mediateca/                      todo lo anterior a tamaño grande para subir a WordPress
"""
import os
import shutil
import sys

import pymupdf
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from media import MENUS, OG, PHOTOS  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENES = os.path.join(BASE, "imagenes")
OUT_IMG = os.path.join(BASE, "assets", "img")
OUT_ICONS = os.path.join(BASE, "assets", "icons")
OUT_MENUS = os.path.join(BASE, "assets", "menus")
OUT_LOGOS = os.path.join(BASE, "assets", "logos")
OUT_WP = os.path.join(BASE, "wordpress", "01-mediateca")
# Carpeta de trabajo con las cartas originales (disco externo).
MENUS_SRC = os.environ.get("CANITAS_MENUS_SRC", "/Volumes/2TB SANDISK/TRABAJO/CAÑITAS MALAGA/MELIA MALAGA")

for d in (OUT_IMG, OUT_ICONS, OUT_MENUS, OUT_WP):
    os.makedirs(d, exist_ok=True)


def fit(im, long_edge):
    im = im.copy()
    im.thumbnail((long_edge, long_edge), Image.LANCZOS)
    return im


def save_jpg(im, dst, quality):
    im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"  {os.path.relpath(dst, BASE)}  {im.size[0]}x{im.size[1]}  {os.path.getsize(dst) // 1024} KB")


def open_photo(src):
    return ImageOps.exif_transpose(Image.open(src)).convert("RGB")


def render_svg(path, width):
    doc = pymupdf.open(path)
    page = doc[0]
    zoom = width / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=True)
    return Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)


print("Fotos")
for name, info in PHOTOS.items():
    src = os.path.join(IMAGENES, *info["src"])
    if not os.path.exists(src):
        print("  FALTA", src)
        continue
    im = open_photo(src)
    save_jpg(fit(im, 1600), os.path.join(OUT_IMG, f"{name}.jpg"), 80)
    save_jpg(fit(im, 800), os.path.join(OUT_IMG, f"{name}-800.jpg"), 78)
    save_jpg(fit(im, 2000), os.path.join(OUT_WP, f"{name}.jpg"), 82)

print("Imágenes para redes sociales")
for name, info in OG.items():
    photo = Image.open(os.path.join(OUT_IMG, f"{info['photo']}.jpg")).convert("RGB")
    ratio = 1200 / 630
    w, h = photo.size
    if w / h > ratio:
        nw = int(h * ratio)
        photo = photo.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / ratio)
        top = int((h - nh) * info["focus"])
        photo = photo.crop((0, top, w, top + nh))
    photo = photo.resize((1200, 630), Image.LANCZOS)
    shade = Image.linear_gradient("L").resize((1200, 630)).point(lambda v: int(v * 0.72))
    photo = Image.composite(Image.new("RGB", photo.size, (20, 19, 46)), photo, shade)
    if info["logo"] == "maite":
        logo = render_svg(os.path.join(OUT_LOGOS, "logo-canitas-maite-blanco.svg"), 420)
    else:
        logo = Image.open(os.path.join(OUT_LOGOS, "logo-canitas-al-fresco-crema.png")).convert("RGBA")
        logo = fit(logo, 400)
    photo.paste(logo, ((1200 - logo.width) // 2, 630 - logo.height - 60), logo)
    for out in (OUT_IMG, OUT_WP):
        save_jpg(photo, os.path.join(out, f"{name}.jpg"), 84)

print("Iconos")
fav = os.path.join(BASE, "assets", "favicon.svg")
for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
    icon = render_svg(fav, size).convert("RGB")
    icon.save(os.path.join(OUT_ICONS, name), "PNG", optimize=True)
    print(f"  assets/icons/{name}")
shutil.copy(os.path.join(OUT_ICONS, "icon-512.png"), os.path.join(OUT_WP, "icono-sitio-canitas-maite-512.png"))

print("Logos para la mediateca")
for f in ("logo-canitas-maite.svg", "logo-canitas-maite-blanco.svg"):
    shutil.copy(os.path.join(OUT_LOGOS, f), os.path.join(OUT_WP, f))
render_svg(os.path.join(OUT_LOGOS, "logo-canitas-maite.svg"), 1200).save(os.path.join(OUT_WP, "logo-canitas-maite.png"))
render_svg(os.path.join(OUT_LOGOS, "logo-canitas-maite-blanco.svg"), 1200).save(os.path.join(OUT_WP, "logo-canitas-maite-blanco.png"))
shutil.copy(os.path.join(OUT_LOGOS, "logo-canitas-al-fresco-crema.png"), OUT_WP)
shutil.copy(os.path.join(OUT_LOGOS, "logo-canitas-al-fresco-color.png"), OUT_WP)

print("Cartas en PDF")
for dst, src in MENUS.items():
    path = os.path.join(MENUS_SRC, src)
    if os.path.exists(path):
        shutil.copy(path, os.path.join(OUT_MENUS, dst))
        os.chmod(os.path.join(OUT_MENUS, dst), 0o644)
    else:
        print("  FALTA (se mantiene la copia actual)", path)
    if os.path.exists(os.path.join(OUT_MENUS, dst)):
        shutil.copy(os.path.join(OUT_MENUS, dst), os.path.join(OUT_WP, dst))
        print(f"  assets/menus/{dst}")
