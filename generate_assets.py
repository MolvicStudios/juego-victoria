#!/usr/bin/env python3
"""
PinguPlay v3 — Generador de assets con Leonardo.AI
Usa solo stdlib (urllib) + Pillow para optimización.

Uso:
  python scripts/generate_assets.py                        # Genera todos
  python scripts/generate_assets.py --category characters  # Solo personajes
  python scripts/generate_assets.py --dry-run              # Preview sin generar
  python scripts/generate_assets.py --skip-existing        # Salta existentes (default)
  python scripts/generate_assets.py --overwrite            # Sobreescribe todos

La clave de API se pide de forma interactiva si no está en el entorno.
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("[AVISO] Pillow no instalado. Las imágenes no se optimizarán.")
    print("  pip install pillow\n")

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BASE_URL        = "https://cloud.leonardo.ai/api/rest/v1"
# Leonardo Phoenix 1.0 — óptimo para ilustración cartoon
MODEL_ID        = "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3"
STYLE_UUID      = "645e4195-f63d-4715-a3f2-3fb1e6eb8c70"  # Illustration
CONTRAST        = 3.5
POLL_INTERVAL   = 4    # segundos entre polls
POLL_TIMEOUT    = 180  # segundos máximo de espera
DELAY_BETWEEN   = 3    # segundos entre generaciones (rate limit)

STATIC_ROOT = Path(__file__).parent.parent / "static" / "assets"

# Sufijos de estilo reutilizables
STYLE_ICON = (
    "flat cartoon illustration, vibrant bold colors, thick clean outlines, "
    "white background, no text, no letters, no numbers, no watermark, "
    "children's educational app icon, cute friendly style"
)
STYLE_CHAR = (
    "flat 2D cartoon illustration, vibrant bold colors, clean outlines, "
    "white background, no text, no watermark, isolated character, "
    "children's educational app mascot style"
)
STYLE_BG = (
    "cartoon scene background, vibrant saturated colors, children's app illustration, "
    "soft gradients, whimsical playful style, no text, no main characters, "
    "wide landscape format"
)
STYLE_STICKER = (
    "cute sticker design, bold outlines, pastel colors, white background, "
    "no text, rounded corners, kawaii style, children's app reward sticker"
)
STYLE_UI = (
    "flat vector UI icon, minimal clean design, single color background, "
    "no text, children's app, bold legible shape, 2D illustration"
)

# ─── LISTA COMPLETA DE ASSETS ─────────────────────────────────────────────────
# Formato: (carpeta_destino, nombre_archivo, ancho, alto, prompt)
ASSETS = [
    # ── Personajes ──────────────────────────────────────────────────────────
    ("characters", "pingu-main.png",    400, 400,
     "cute cartoon penguin mascot standing upright, friendly expression, blue scarf, "
     + STYLE_CHAR),
    ("characters", "pingu-happy.png",   400, 400,
     "cute cartoon penguin mascot jumping with joy, big smile, arms raised, "
     + STYLE_CHAR),
    ("characters", "pingu-sad.png",     400, 400,
     "cute cartoon penguin mascot with droopy wings, small tear, sad expression, "
     + STYLE_CHAR),
    ("characters", "pingu-thinking.png",400, 400,
     "cute cartoon penguin mascot with finger on chin, thinking expression, "
     + STYLE_CHAR),
    ("characters", "pingu-excited.png", 400, 400,
     "cute cartoon penguin mascot super excited, star sparkles around, wide eyes, "
     + STYLE_CHAR),
    ("characters", "pingu-sleeping.png",400, 400,
     "cute cartoon penguin mascot sleeping, ZZZ bubbles, cute snore expression, "
     + STYLE_CHAR),

    # ── Fondos de mundo ─────────────────────────────────────────────────────
    ("backgrounds", "bg-nubecitas.jpg",    1024, 576,
     "dreamy sky with fluffy clouds, soft pastel purples and blues, rainbow, stars, "
     "magical nursery atmosphere, " + STYLE_BG),
    ("backgrounds", "bg-exploradores.jpg", 1024, 576,
     "bright sunny meadow with rolling green hills, colorful flowers, "
     "distant mountains, clear blue sky, " + STYLE_BG),
    ("backgrounds", "bg-aventureros.jpg",  1024, 576,
     "magical forest clearing with ancient trees, glowing fireflies, "
     "stone path, adventure atmosphere, " + STYLE_BG),
    ("backgrounds", "bg-maestros.jpg",     1024, 576,
     "cozy library interior with floating books, warm lighting, "
     "starry window background, academic atmosphere, " + STYLE_BG),

    # ── Avatares (12 opciones) ───────────────────────────────────────────────
    ("avatars", "av-penguin.png",  128, 128,
     "cute cartoon penguin face, round, " + STYLE_ICON),
    ("avatars", "av-bear.png",     128, 128,
     "cute cartoon teddy bear face, round, " + STYLE_ICON),
    ("avatars", "av-cat.png",      128, 128,
     "cute cartoon cat face, round, whiskers, " + STYLE_ICON),
    ("avatars", "av-dog.png",      128, 128,
     "cute cartoon dog face, round, floppy ears, " + STYLE_ICON),
    ("avatars", "av-fox.png",      128, 128,
     "cute cartoon fox face, round, orange fur, " + STYLE_ICON),
    ("avatars", "av-rabbit.png",   128, 128,
     "cute cartoon rabbit face, round, long ears, " + STYLE_ICON),
    ("avatars", "av-owl.png",      128, 128,
     "cute cartoon owl face, round, big glasses eyes, " + STYLE_ICON),
    ("avatars", "av-dino.png",     128, 128,
     "cute cartoon dinosaur face, round, green, " + STYLE_ICON),
    ("avatars", "av-unicorn.png",  128, 128,
     "cute cartoon unicorn face, round, horn, colorful mane, " + STYLE_ICON),
    ("avatars", "av-panda.png",    128, 128,
     "cute cartoon panda face, round, black and white markings, " + STYLE_ICON),
    ("avatars", "av-lion.png",     128, 128,
     "cute cartoon lion face, round, fluffy mane, " + STYLE_ICON),
    ("avatars", "av-elephant.png", 128, 128,
     "cute cartoon elephant face, round, big ears, trunk, " + STYLE_ICON),

    # ── Stickers de logro (20 stickers) ─────────────────────────────────────
    ("stickers", "stk-star.png",         200, 200,
     "golden star trophy sticker, shining, " + STYLE_STICKER),
    ("stickers", "stk-rocket.png",       200, 200,
     "colorful rocket ship sticker, going up, " + STYLE_STICKER),
    ("stickers", "stk-rainbow.png",      200, 200,
     "rainbow with clouds sticker, smiling sun, " + STYLE_STICKER),
    ("stickers", "stk-crown.png",        200, 200,
     "golden crown sticker, jewels, regal, " + STYLE_STICKER),
    ("stickers", "stk-medal-gold.png",   200, 200,
     "gold medal sticker, number 1, ribbon, " + STYLE_STICKER),
    ("stickers", "stk-medal-silver.png", 200, 200,
     "silver medal sticker, ribbon, " + STYLE_STICKER),
    ("stickers", "stk-medal-bronze.png", 200, 200,
     "bronze medal sticker, ribbon, " + STYLE_STICKER),
    ("stickers", "stk-heart.png",        200, 200,
     "pink heart sticker, sparkle, love, " + STYLE_STICKER),
    ("stickers", "stk-lightning.png",    200, 200,
     "yellow lightning bolt sticker, electric, " + STYLE_STICKER),
    ("stickers", "stk-gem.png",          200, 200,
     "blue diamond gem sticker, shining, precious, " + STYLE_STICKER),
    ("stickers", "stk-book.png",         200, 200,
     "open book sticker, colorful pages, knowledge, " + STYLE_STICKER),
    ("stickers", "stk-pencil.png",       200, 200,
     "yellow pencil sticker, writing, creative, " + STYLE_STICKER),
    ("stickers", "stk-globe.png",        200, 200,
     "cute globe sticker, world map, explorer, " + STYLE_STICKER),
    ("stickers", "stk-music.png",        200, 200,
     "musical notes sticker, colorful, melody, " + STYLE_STICKER),
    ("stickers", "stk-paint.png",        200, 200,
     "paint palette sticker, rainbow colors, artist, " + STYLE_STICKER),
    ("stickers", "stk-puzzle.png",       200, 200,
     "puzzle piece sticker, colorful, fitting perfectly, " + STYLE_STICKER),
    ("stickers", "stk-robot.png",        200, 200,
     "cute robot sticker, friendly face, technology, " + STYLE_STICKER),
    ("stickers", "stk-fire.png",         200, 200,
     "fire streak sticker, hot streak, orange flames, " + STYLE_STICKER),
    ("stickers", "stk-ice.png",          200, 200,
     "ice crystal sticker, cool blue, snowflake, " + STYLE_STICKER),
    ("stickers", "stk-champion.png",     200, 200,
     "champion cup trophy sticker, gold, winner, " + STYLE_STICKER),

    # ── UI Icons ─────────────────────────────────────────────────────────────
    ("ui", "star-filled.png",   64, 64,
     "solid gold star icon, 5-point, vibrant yellow, " + STYLE_UI),
    ("ui", "star-empty.png",    64, 64,
     "outlined grey star icon, 5-point, empty, " + STYLE_UI),
    ("ui", "coin.png",          64, 64,
     "gold coin icon, shiny, simple, " + STYLE_UI),
    ("ui", "heart-full.png",    64, 64,
     "red heart icon, life point, solid, " + STYLE_UI),
    ("ui", "heart-empty.png",   64, 64,
     "grey outlined heart icon, empty, " + STYLE_UI),
    ("ui", "trophy.png",        64, 64,
     "gold trophy icon, cup, achievement, " + STYLE_UI),
    ("ui", "lock.png",          64, 64,
     "padlock icon, locked level, blue, " + STYLE_UI),
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────

DEFAULT_API_KEY = "5314be47-33c5-40bb-8731-1469de403105"

def get_api_key():
    """Obtiene la API key: variable de entorno → .env → clave por defecto."""
    # 1. Variable de entorno
    key = os.environ.get("LEONARDO_API_KEY", "").strip()
    if key:
        return key
    # 2. Archivo .env junto al script
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("LEONARDO_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key
    # 3. Clave por defecto
    return DEFAULT_API_KEY


def api_request(method, path, data=None, api_key=""):
    """Realiza una petición HTTP a la API de Leonardo usando urllib."""
    url = BASE_URL + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        print(f"  [HTTP {e.code}] {body_text[:300]}")
        return None


def download_file(url, dest_path):
    """Descarga un archivo desde una URL pública."""
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            dest_path.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"  [DESCARGA ERROR] {e}")
        return False


def optimize_image(path, max_kb=150):
    """Optimiza la imagen con Pillow para mantenerla bajo max_kb."""
    if not HAS_PILLOW:
        return
    try:
        img = Image.open(path).convert("RGBA")
        orig_size = path.stat().st_size / 1024
        if orig_size <= max_kb:
            return

        ext = path.suffix.lower()
        quality = 85
        while quality >= 40:
            if ext in (".jpg", ".jpeg"):
                img.convert("RGB").save(path, "JPEG", quality=quality, optimize=True)
            else:
                img.save(path, "PNG", optimize=True)
            new_size = path.stat().st_size / 1024
            if new_size <= max_kb:
                print(f"    → Optimizado: {orig_size:.0f}KB → {new_size:.0f}KB (q={quality})")
                return
            quality -= 10
        print(f"    [AVISO] No se pudo reducir bajo {max_kb}KB (actual: {new_size:.0f}KB)")
    except Exception as e:
        print(f"    [OPTIMIZE ERROR] {e}")


def generate_image(prompt, width, height, api_key):
    """
    Genera una imagen con Leonardo.AI Phoenix.
    Devuelve la URL de la imagen generada o None si falla.
    """
    payload = {
        "modelId": MODEL_ID,
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_images": 1,
        "contrast": CONTRAST,
        "style_uuid": STYLE_UUID,
        "ultra": False,
        "photoReal": False,
    }
    result = api_request("POST", "/generations", data=payload, api_key=api_key)
    if not result:
        return None

    gen_id = result.get("sdGenerationJob", {}).get("generationId")
    if not gen_id:
        print(f"  [ERROR] No se obtuvo generationId: {result}")
        return None

    # Polling hasta que la generación esté lista
    elapsed = 0
    while elapsed < POLL_TIMEOUT:
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
        status = api_request("GET", f"/generations/{gen_id}", api_key=api_key)
        if not status:
            continue
        job = status.get("generations_by_pk", {})
        if job.get("status") == "COMPLETE":
            imgs = job.get("generated_images", [])
            if imgs:
                return imgs[0].get("url")
        elif job.get("status") == "FAILED":
            print("  [ERROR] Generación fallida.")
            return None

    print(f"  [TIMEOUT] La generación tardó más de {POLL_TIMEOUT}s.")
    return None


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generador de assets PinguPlay v3")
    parser.add_argument("--category", help="Solo generar categoría: characters|backgrounds|avatars|stickers|ui")
    parser.add_argument("--dry-run",  action="store_true", help="Mostrar lista sin generar")
    parser.add_argument("--overwrite", action="store_true", help="Sobreescribir archivos existentes")
    args = parser.parse_args()

    skip_existing = not args.overwrite

    # Filtrar por categoría si se especifica
    assets = ASSETS
    if args.category:
        assets = [a for a in assets if a[0] == args.category]
        if not assets:
            sys.exit(f"[ERROR] Categoría '{args.category}' no encontrada. Opciones: characters, backgrounds, avatars, stickers, ui")

    print(f"\n=== PinguPlay v3 — Asset Generator ===")
    print(f"Assets totales: {len(assets)}")
    if args.dry_run:
        print("\n[DRY RUN] Assets a generar:\n")
        for folder, name, w, h, prompt in assets:
            dest = STATIC_ROOT / folder / name
            status = "✓ existe" if dest.exists() else "→ generar"
            print(f"  [{status}] {folder}/{name} ({w}×{h}px)")
            print(f"           {prompt[:80]}...")
        return

    api_key = get_api_key()

    # Verificar acceso a la API
    print("\nVerificando credenciales...")
    me = api_request("GET", "/me", api_key=api_key)
    if not me:
        sys.exit("[ERROR] No se pudo conectar a Leonardo.AI — revisa la API key.")
    username = me.get("user_details", [{}])[0].get("user", {}).get("username", "desconocido")
    print(f"  Conectado como: {username}\n")

    ok_count = 0
    skip_count = 0
    error_count = 0

    for i, (folder, name, w, h, prompt) in enumerate(assets, 1):
        dest_dir = STATIC_ROOT / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / name

        print(f"[{i}/{len(assets)}] {folder}/{name} ({w}×{h})")

        if skip_existing and dest_path.exists():
            print(f"  ↷ Saltado (ya existe)")
            skip_count += 1
            continue

        url = generate_image(prompt, w, h, api_key)
        if not url:
            print(f"  ✗ Error generando imagen")
            error_count += 1
            continue

        if download_file(url, dest_path):
            optimize_image(dest_path)
            file_kb = dest_path.stat().st_size / 1024
            print(f"  ✓ Guardado → {dest_path} ({file_kb:.0f}KB)")
            ok_count += 1
        else:
            error_count += 1

        if i < len(assets):
            time.sleep(DELAY_BETWEEN)

    print(f"\n=== Resumen ===")
    print(f"  ✓ Generados : {ok_count}")
    print(f"  ↷ Saltados  : {skip_count}")
    print(f"  ✗ Errores   : {error_count}")
    print(f"  Destino     : {STATIC_ROOT}\n")


if __name__ == "__main__":
    main()
