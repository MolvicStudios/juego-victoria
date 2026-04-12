#!/usr/bin/env python3
"""
PinguPlay — Generador automático de assets con Leonardo.AI
Genera los 92 assets del juego y los guarda en src/lib/assets/

Uso:
  python generate_assets.py                       # Genera todo
  python generate_assets.py --category characters # Solo personajes
  python generate_assets.py --dry-run             # Preview sin generar
  python generate_assets.py --skip-existing       # Salta archivos ya existentes (default)
  python generate_assets.py --overwrite           # Sobreescribe existentes

API Key: variable de entorno LEONARDO_API_KEY
  export LEONARDO_API_KEY="tu_clave_aqui"
  o en el archivo .env del proyecto
"""

import os, sys, time, json, argparse, requests
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BASE_URL     = "https://cloud.leonardo.ai/api/rest/v1"
# Leonardo Phoenix 1.0 — mejor para ilustración cartoon
MODEL_ID     = "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3"
# styleUUID: Illustration
STYLE_UUID   = "645e4195-f63d-4715-a3f2-3fb1e6eb8c70"
CONTRAST     = 3.5   # requerido para Phoenix
POLL_INTERVAL = 4    # segundos entre polls
POLL_TIMEOUT  = 180  # máximo espera por generación
DELAY_BETWEEN = 3    # segundos entre generaciones (rate limit)

ASSETS_ROOT = Path(__file__).parent / "src" / "lib" / "assets"

# Sufijo de estilo base para iconos (256×256)
STYLE_ICON = (
    "flat cartoon illustration, vibrant bold colors, thick clean outlines, "
    "white background, no text, no letters, no numbers, no watermark, "
    "children's educational app icon, cute friendly style"
)
# Sufijo para personajes
STYLE_CHAR = (
    "flat 2D cartoon illustration, vibrant bold colors, clean outlines, "
    "white background, no text, no watermark, isolated character, "
    "children's educational app mascot style"
)
# Sufijo para fondos (1024×576)
STYLE_BG = (
    "cartoon scene background, vibrant saturated colors, children's app illustration, "
    "soft gradients, whimsical playful style, no text, no main character in foreground, "
    "wide landscape format"
)
# Sufijo para stickers
STYLE_STK = (
    "cute illustrated sticker, vibrant bold colors, thick cartoon outline, "
    "white background, no text, no watermark, children's reward sticker, "
    "flat cartoon illustration"
)


def p(prompt, suffix):
    """Une prompt con sufijo de estilo."""
    return f"{prompt}, {suffix}"


# ─── DEFINICIÓN DE ASSETS ─────────────────────────────────────────────────────
# Cada asset: (categoria, filename, width, height, prompt)
ASSETS = [

    # ═══ PERSONAJES ═══════════════════════════════════════════════════════════
    ("characters", "pingu-main.png", 512, 512, p(
        "cute cartoon baby penguin standing upright, round body, big expressive dark eyes, "
        "tiny orange beak, small orange feet, friendly warm smile, looking forward, "
        "slightly tilted head, waving one flipper", STYLE_CHAR)),

    ("characters", "pingu-happy.png", 512, 512, p(
        "cute cartoon baby penguin jumping for joy, arms raised high, huge beaming smile, "
        "sparkles and stars around it, round black and white body, tiny orange beak and feet", STYLE_CHAR)),

    ("characters", "pingu-thinking.png", 512, 512, p(
        "cute cartoon baby penguin thinking pose, one flipper touching chin thoughtfully, "
        "one eye slightly squinted, small thought bubble above head, round black and white body", STYLE_CHAR)),

    ("characters", "pingu-sad.png", 512, 512, p(
        "cute cartoon baby penguin sad face, droopy eyes with small tear drop, "
        "slight frown, arms hanging down, round black and white body, tiny orange beak", STYLE_CHAR)),

    ("characters", "pingu-excited.png", 512, 512, p(
        "cute cartoon baby penguin super excited, running forward arms stretched back, "
        "huge smile, motion lines, stars and confetti around, round black and white body", STYLE_CHAR)),

    ("characters", "pingu-sleeping.png", 512, 512, p(
        "cute cartoon baby penguin sleeping peacefully, eyes closed, ZZZ bubbles floating, "
        "small pillow under head, peaceful smile, round black and white body, nightcap optional", STYLE_CHAR)),

    # ═══ FONDOS ═══════════════════════════════════════════════════════════════
    ("backgrounds", "bg-nubecitas.png", 1024, 576, p(
        "dreamy sky background, fluffy white cartoon clouds, soft lavender and baby blue sky gradient, "
        "tiny stars and sparkles, pastel rainbow faintly visible, very soft pastel palette", STYLE_BG)),

    ("backgrounds", "bg-exploradores.png", 1024, 576, p(
        "colorful cartoon jungle and nature background, lush green trees and tropical leaves, "
        "bright blue sky with fluffy clouds, friendly cartoon birds and butterflies peeking from foliage, "
        "rolling green hills, vibrant primary colors", STYLE_BG)),

    ("backgrounds", "bg-aventureros.png", 1024, 576, p(
        "colorful cartoon adventure landscape, whimsical castle on green hill, forest with tall trees, "
        "friendly cartoon dragon flying in background, treasure chest, bright blue sky with cartoon sun, "
        "vibrant bold colors, action adventure feel but friendly", STYLE_BG)),

    ("backgrounds", "bg-maestros.png", 1024, 576, p(
        "colorful cartoon space and science background, night sky with stars planet earth and moon, "
        "cartoon rocket ship, floating books and stars, telescope, "
        "deep blue and purple gradient sky, bright stars and nebula", STYLE_BG)),

    # ═══ ICONOS DE MUNDO ══════════════════════════════════════════════════════
    ("ui", "world-nubecitas.png", 512, 512, p(
        "cute cartoon cloud icon, fluffy white cloud with pastel purple border, "
        "tiny stars and sparkles, soft lavender glow", STYLE_ICON)),

    ("ui", "world-exploradores.png", 512, 512, p(
        "cute cartoon globe icon, round earth cartoon style, green continents bright blue ocean, "
        "tiny leaf and magnifying glass overlaid, vibrant primary colors", STYLE_ICON)),

    ("ui", "world-aventureros.png", 512, 512, p(
        "cute cartoon adventure icon, crossed cartoon sword and shield, "
        "bright red shield with star, golden sword, vibrant bold colors", STYLE_ICON)),

    ("ui", "world-maestros.png", 512, 512, p(
        "cute cartoon trophy icon, gold trophy cup with star, sparkles around it, "
        "vibrant gold and orange colors", STYLE_ICON)),

    # ═══ ICONOS DE JUEGOS (38) ════════════════════════════════════════════════
    ("games", "g1-formas.png", 512, 512, p(
        "cartoon icon showing colorful geometric shapes arranged playfully, "
        "red circle blue triangle green square yellow star, each with thick cartoon outline", STYLE_ICON)),

    ("games", "g2-contar.png", 512, 512, p(
        "cartoon icon showing five bright red apples being counted, "
        "small cartoon hand pointing at them, cheerful counting game feel", STYLE_ICON)),

    ("games", "g3-letras.png", 512, 512, p(
        "cartoon icon showing large colorful alphabet letter A decorated with stars, "
        "bright yellow and orange, single letter A prominently displayed", STYLE_ICON)),

    ("games", "g4-pintar.png", 512, 512, p(
        "cartoon icon showing a paintbrush making colorful stroke, "
        "rainbow paint splash, palette with vibrant colors", STYLE_ICON)),

    ("games", "g5-memoria.png", 512, 512, p(
        "cartoon icon showing two matching playing cards, one face down with question mark, "
        "one being flipped to reveal a colorful star", STYLE_ICON)),

    ("games", "g6-piano.png", 512, 512, p(
        "cartoon icon showing miniature colorful piano keyboard, "
        "musical notes floating above the keys, white and black keys", STYLE_ICON)),

    ("games", "g7-numeros.png", 512, 512, p(
        "cartoon icon showing colorful number blocks in sequence, "
        "bright colored cubes with numbers one two three, fun stacking arrangement", STYLE_ICON)),

    ("games", "g8-queves.png", 512, 512, p(
        "cartoon icon showing a cute cartoon lion face, big expressive friendly eyes, "
        "colorful mane, looking forward with curious expression", STYLE_ICON)),

    ("games", "g9-puzle.png", 512, 512, p(
        "cartoon icon showing four colorful puzzle pieces fitting together, "
        "each piece different bright color, one piece being placed", STYLE_ICON)),

    ("games", "g10-colores.png", 512, 512, p(
        "cartoon icon showing color wheel with six vibrant sections, "
        "rainbow wheel alternating red orange yellow green blue purple, cartoon style", STYLE_ICON)),

    ("games", "g11-sumas.png", 512, 512, p(
        "cartoon icon showing two groups of colorful fruits with plus sign between them, "
        "two red apples plus three oranges, cute fruit characters", STYLE_ICON)),

    ("games", "g12-traza.png", 512, 512, p(
        "cartoon icon showing a pencil tracing dotted lines forming a letter shape, "
        "dotted path guidelines, bright colored pencil leaving colorful trail", STYLE_ICON)),

    ("games", "g13-oyes.png", 512, 512, p(
        "cartoon icon showing a cute ear with colorful sound waves emanating from it, "
        "bright pink and blue sound waves, listening game feel", STYLE_ICON)),

    ("games", "g14-laberinto.png", 512, 512, p(
        "cartoon icon showing a small cute maze from above view, "
        "colorful walls and a tiny penguin at the start, star at the finish", STYLE_ICON)),

    ("games", "g15-tamanos.png", 512, 512, p(
        "cartoon icon showing a large cartoon elephant next to a tiny cartoon mouse, "
        "size comparison, both cute and friendly, vibrant colors", STYLE_ICON)),

    ("games", "g16-patrones.png", 512, 512, p(
        "cartoon icon showing colored shapes in repeating pattern sequence, "
        "red circle blue square red circle question mark, pattern recognition game", STYLE_ICON)),

    ("games", "g17-globos.png", 512, 512, p(
        "cartoon icon showing three colorful balloons floating up, "
        "red green and blue balloons with strings, sparkles and festive feel", STYLE_ICON)),

    ("games", "g18-animales.png", 512, 512, p(
        "cartoon icon showing cute cartoon animal paw print with small animal faces around it, "
        "colorful cat dog rabbit faces peeking from sides", STYLE_ICON)),

    ("games", "g19-silabas.png", 512, 512, p(
        "cartoon icon showing two cartoon hands clapping together enthusiastically, "
        "motion lines showing clapping rhythm, bright and energetic", STYLE_ICON)),

    ("games", "g20-rimas.png", 512, 512, p(
        "cartoon icon showing a cute microphone with musical notes and rhyming symbols, "
        "colorful sound waves forming heart shape, poetry and rhyme game", STYLE_ICON)),

    ("games", "g21-deletrear.png", 512, 512, p(
        "cartoon icon showing colorful letter tiles being arranged, "
        "scrambled cartoon alphabet blocks C A T forming a word, bright colored cubes", STYLE_ICON)),

    ("games", "g22-opuestos.png", 512, 512, p(
        "cartoon icon showing two arrows pointing in opposite directions, "
        "one left one right in bright contrasting colors, also small sun and moon", STYLE_ICON)),

    ("games", "g23-frase.png", 512, 512, p(
        "cartoon icon showing a speech bubble with a blank gap in the middle, "
        "dotted line where missing word goes, colorful friendly bubble", STYLE_ICON)),

    ("games", "g24-restas.png", 512, 512, p(
        "cartoon icon showing five colorful strawberries with three of them playfully crossed out, "
        "subtraction game, cute cartoon style", STYLE_ICON)),

    ("games", "g25-parimpar.png", 512, 512, p(
        "cartoon icon showing two groups of colored dots with faces, "
        "left side two paired dots, right side three dots one alone unpaired", STYLE_ICON)),

    ("games", "g26-mayormenor.png", 512, 512, p(
        "cartoon icon showing cartoon balance scale with different weights on each side, "
        "one side more colorful blocks than other, scale tilting, comparison game", STYLE_ICON)),

    ("games", "g27-monedas.png", 512, 512, p(
        "cartoon icon showing shiny cartoon coins stacked and scattered, "
        "gold and silver cartoon coins, small piggy bank in background", STYLE_ICON)),

    ("games", "g28-reloj.png", 512, 512, p(
        "cartoon icon showing a cute round analog clock with friendly smiling face, "
        "big numbers visible on clock face, clock hands pointing at three o'clock", STYLE_ICON)),

    ("games", "g29-intruso.png", 512, 512, p(
        "cartoon icon showing three matching cartoon apples and one banana among them, "
        "the odd banana highlighted with question mark, odd-one-out game", STYLE_ICON)),

    ("games", "g30-sombras.png", 512, 512, p(
        "cartoon icon showing bright cartoon star above and its dark shadow silhouette below, "
        "clean shadow matching outline of object, shadow matching game", STYLE_ICON)),

    ("games", "g31-secuencias.png", 512, 512, p(
        "cartoon icon showing colorful number-train blocks in sequence, "
        "colorful train cars connected, one car missing with question mark", STYLE_ICON)),

    ("games", "g32-categorias.png", 512, 512, p(
        "cartoon icon showing two colorful cartoon boxes being sorted, "
        "fruits going into one box animals into another, classification sorting game", STYLE_ICON)),

    ("games", "g33-sudoku.png", 512, 512, p(
        "cartoon icon showing small cute grid with colorful emoji in cells, "
        "two by two grid with star heart sun and moon symbols, puzzle grid game", STYLE_ICON)),

    ("games", "g34-ritmo.png", 512, 512, p(
        "cartoon icon showing colorful cartoon drum with music notes floating above, "
        "bright drumsticks hitting drum, sound waves visible, rhythm game", STYLE_ICON)),

    ("games", "g35-conecta.png", 512, 512, p(
        "cartoon icon showing numbered dots connected by bright colored lines forming star shape, "
        "dots being connected with glowing line, connect-the-dots game", STYLE_ICON)),

    ("games", "g36-espejo.png", 512, 512, p(
        "cartoon icon showing a cartoon mirror with butterfly on one side and its reflection, "
        "bright colorful mirror frame, symmetry mirror game", STYLE_ICON)),

    ("games", "g37-burbujas.png", 512, 512, p(
        "cartoon icon showing colorful cartoon bubbles floating up, "
        "each bubble different color red blue green, sparkling transparent bubbles", STYLE_ICON)),

    ("games", "g38-tangram.png", 512, 512, p(
        "cartoon icon showing colorful tangram pieces arranged to form a simple bird shape, "
        "geometric pieces in bright contrasting colors, tangram puzzle game", STYLE_ICON)),

    # ═══ ELEMENTOS UI ══════════════════════════════════════════════════════════
    ("ui", "medal-gold.png", 512, 512, p(
        "shiny golden cartoon medal with star in center, golden ribbon, sparkles and gleam, "
        "award winner first place medal", STYLE_ICON)),

    ("ui", "medal-silver.png", 512, 512, p(
        "shiny silver cartoon medal with star in center, silver ribbon, sparkles, "
        "second place award medal, bright silver colors", STYLE_ICON)),

    ("ui", "medal-bronze.png", 512, 512, p(
        "shiny bronze cartoon medal with star in center, copper brown ribbon, sparkles, "
        "third place award medal, warm bronze colors", STYLE_ICON)),

    ("ui", "trophy.png", 512, 512, p(
        "large shiny cartoon trophy cup, golden with stars and sparkles emanating, "
        "celebration confetti around it, tall ornate trophy", STYLE_ICON)),

    ("ui", "star-filled.png", 512, 512, p(
        "large bright five-pointed cartoon star, vibrant yellow and orange gradient, "
        "thick outline, inner glow, sparkles around it, reward star", STYLE_ICON)),

    ("ui", "star-empty.png", 512, 512, p(
        "five-pointed cartoon star outline only, light gray unfilled outline, "
        "clean simple outline star, waiting to be earned", STYLE_ICON)),

    ("ui", "confetti-burst.png", 512, 512, p(
        "colorful confetti explosion burst, rainbow colored confetti pieces flying outward, "
        "streamers and party poppers, celebration moment", STYLE_ICON)),

    ("ui", "lock.png", 512, 512, p(
        "cute cartoon padlock, friendly rounded shape, vibrant blue and gray colors, "
        "locked state, child-friendly lock icon", STYLE_ICON)),

    ("ui", "home-button.png", 512, 512, p(
        "cute cartoon house icon with friendly face window and door, "
        "vibrant blue roof orange walls, home navigation button", STYLE_ICON)),

    ("ui", "back-arrow.png", 512, 512, p(
        "cute rounded cartoon back arrow, thick friendly curved arrow shape, "
        "bright blue and white colors, child-friendly navigation", STYLE_ICON)),

    # ═══ STICKERS (20 hitos) ══════════════════════════════════════════════════
    ("stickers", "stk-flor.png", 512, 512, p(
        "cute cartoon pink cherry blossom flower with dewdrops, petals spreading out, "
        "soft pink and white colors, reward sticker at 5 stars", STYLE_STK)),

    ("stickers", "stk-unicornio.png", 512, 512, p(
        "magical cartoon unicorn with rainbow mane flying, sparkles and stars around it, "
        "colorful magical horse with horn, 10 stars reward", STYLE_STK)),

    ("stickers", "stk-corona.png", 512, 512, p(
        "shiny cartoon golden crown with colorful gems embedded, royalty crown, "
        "sparkles and gleam around it, 20 stars reward", STYLE_STK)),

    ("stickers", "stk-arcoiris.png", 512, 512, p(
        "bright cartoon rainbow emerging from fluffy clouds, "
        "colorful arc with white clouds at both ends, vibrant rainbow colors, 35 stars", STYLE_STK)),

    ("stickers", "stk-castillo.png", 512, 512, p(
        "magical cartoon castle with towers and colorful flags, fantasy rainbow bridge, "
        "fluffy clouds around it, fairy tale castle, 50 stars reward", STYLE_STK)),

    ("stickers", "stk-circo.png", 512, 512, p(
        "colorful cartoon circus tent with stars and lights, festive flags and balloons, "
        "big top tent in vibrant red white and yellow, 75 stars", STYLE_STK)),

    ("stickers", "stk-diamante.png", 512, 512, p(
        "sparkling cartoon diamond gem, light blue crystal with rainbow reflections, "
        "gleaming light blue diamond, 100 stars reward", STYLE_STK)),

    ("stickers", "stk-cohete.png", 512, 512, p(
        "cartoon rocket ship launching with bright flame trail, stars and planets around it, "
        "colorful space rocket blast off, 130 stars reward", STYLE_STK)),

    ("stickers", "stk-estrella-shoot.png", 512, 512, p(
        "giant cartoon shooting star with long sparkling tail across sky, "
        "bright gold and white glowing star, 170 stars reward", STYLE_STK)),

    ("stickers", "stk-carrousel.png", 512, 512, p(
        "magical cartoon merry-go-round with colorful horses and sparkling lights, "
        "festive carnival carousel, bright pastel colors, 200 stars", STYLE_STK)),

    ("stickers", "stk-mariposa.png", 512, 512, p(
        "beautiful cartoon butterfly with intricate colorful patterned wings, "
        "flowers and sparkles around it, vibrant rainbow wings, 250 stars", STYLE_STK)),

    ("stickers", "stk-trofeo.png", 512, 512, p(
        "grand cartoon championship trophy, golden with large stars and confetti explosion, "
        "biggest trophy award, 300 stars reward", STYLE_STK)),

    ("stickers", "stk-mascaras.png", 512, 512, p(
        "colorful cartoon theater comedy and drama masks side by side, "
        "stars and spotlights around them, performance theater, 400 stars", STYLE_STK)),

    ("stickers", "stk-princesa.png", 512, 512, p(
        "cute cartoon princess wearing sparkly dress and tiara, magic wand with stars, "
        "full character portrait, 500 stars reward", STYLE_STK)),

    ("stickers", "stk-planeta.png", 512, 512, p(
        "colorful cartoon planet Earth with visible continents, stars and space around it, "
        "friendly smiling planet, 650 stars reward", STYLE_STK)),

    ("stickers", "stk-fuegos.png", 512, 512, p(
        "colorful cartoon fireworks exploding in night sky, multiple colored bursts and sparkles, "
        "celebration fireworks display, 800 stars", STYLE_STK)),

    ("stickers", "stk-galaxia.png", 512, 512, p(
        "magical cartoon galaxy spiral, purple and blue cosmic swirl with bright stars, "
        "colorful nebula and stardust, 1000 stars reward", STYLE_STK)),

    ("stickers", "stk-unicornio2.png", 512, 512, p(
        "super magical cartoon unicorn with elaborate rainbow wings and jeweled crown, "
        "very sparkly magical horse, 1300 stars reward", STYLE_STK)),

    ("stickers", "stk-magico.png", 512, 512, p(
        "magical cartoon sparkling star burst with multiple layers of glowing light and glitter, "
        "ultimate magical sparkle explosion, 1700 stars reward", STYLE_STK)),

    ("stickers", "stk-medalla-oro.png", 512, 512, p(
        "ultimate golden first place cartoon medal with elaborate decorations, "
        "stars and laurel wreath, champion achievement medal, 2000 stars", STYLE_STK)),

    # ═══ AVATARES (10) ════════════════════════════════════════════════════════
    ("avatars", "av-unicornio.png", 512, 512, p(
        "cute cartoon unicorn head portrait, colorful rainbow horn and flowing mane, "
        "big friendly eyes, round face, profile avatar", STYLE_CHAR)),

    ("avatars", "av-princesa.png", 512, 512, p(
        "cute cartoon princess portrait, sparkly tiara, long colorful hair, "
        "friendly smile, round face, profile avatar", STYLE_CHAR)),

    ("avatars", "av-mariposa.png", 512, 512, p(
        "cute cartoon butterfly character portrait, colorful patterned wings as hair, "
        "friendly smile, round face, profile avatar", STYLE_CHAR)),

    ("avatars", "av-estrella.png", 512, 512, p(
        "cute cartoon star character portrait, golden star shaped head with big eyes and warm smile, "
        "sparkles around it, profile avatar", STYLE_CHAR)),

    ("avatars", "av-gato.png", 512, 512, p(
        "cute cartoon cat portrait, round face, big expressive eyes, "
        "soft pastel colors, pointy ears, profile avatar", STYLE_CHAR)),

    ("avatars", "av-perro.png", 512, 512, p(
        "cute cartoon dog portrait, floppy ears, big friendly eyes, "
        "warm brown and white colors, profile avatar", STYLE_CHAR)),

    ("avatars", "av-conejo.png", 512, 512, p(
        "cute cartoon bunny portrait, long floppy ears, pink button nose, "
        "white and pink soft colors, profile avatar", STYLE_CHAR)),

    ("avatars", "av-panda.png", 512, 512, p(
        "cute cartoon panda portrait, round black and white face, "
        "big circular eyes, bamboo leaf optional, profile avatar", STYLE_CHAR)),

    ("avatars", "av-zorro.png", 512, 512, p(
        "cute cartoon fox portrait, pointy ears, orange and white face, "
        "bushy tail visible, bright warm colors, profile avatar", STYLE_CHAR)),

    ("avatars", "av-oso.png", 512, 512, p(
        "cute cartoon bear portrait, round face, warm brown colors, "
        "honey drip optional, friendly smile, profile avatar", STYLE_CHAR)),
]

# Orden de prioridad para generar primero los más importantes
PRIORITY_ORDER = ["characters", "backgrounds", "ui", "games", "stickers", "avatars"]


# ─── COLORES TERMINAL ─────────────────────────────────────────────────────────
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

def log(msg, color=C.RESET):
    print(f"{color}{msg}{C.RESET}", flush=True)

def progress(current, total, label=""):
    bar_len = 30
    filled = int(bar_len * current / total)
    bar = "█" * filled + "░" * (bar_len - filled)
    pct = int(100 * current / total)
    print(f"\r{C.CYAN}[{bar}] {pct:3d}% ({current}/{total}) {label[:40]:<40}{C.RESET}", end="", flush=True)


# ─── CLIENTE LEONARDO AI ──────────────────────────────────────────────────────
class LeonardoClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}",
        }

    def create_generation(self, prompt: str, width: int, height: int) -> str:
        """Lanza una generación y devuelve el generationId."""
        payload = {
            "modelId": MODEL_ID,
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_images": 1,
            "contrast": CONTRAST,
            "styleUUID": STYLE_UUID,
        }
        resp = requests.post(
            f"{BASE_URL}/generations",
            headers=self.headers,
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        gen_id = data.get("sdGenerationJob", {}).get("generationId")
        if not gen_id:
            raise ValueError(f"No se recibió generationId: {data}")
        return gen_id

    def poll_generation(self, gen_id: str) -> list[str]:
        """Espera a que la generación termine y devuelve las URLs de imágenes."""
        deadline = time.time() + POLL_TIMEOUT
        while time.time() < deadline:
            resp = requests.get(
                f"{BASE_URL}/generations/{gen_id}",
                headers=self.headers,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json().get("generations_by_pk", {})
            status = data.get("status", "")

            if status == "COMPLETE":
                images = data.get("generated_images", [])
                urls = [img["url"] for img in images if img.get("url")]
                if urls:
                    return urls
                raise ValueError("Generación completa pero sin imágenes")
            elif status == "FAILED":
                raise ValueError(f"Generación fallida: generationId={gen_id}")

            time.sleep(POLL_INTERVAL)

        raise TimeoutError(f"Timeout ({POLL_TIMEOUT}s) esperando generationId={gen_id}")

    def download_image(self, url: str, dest_path: Path):
        """Descarga una imagen y la guarda en dest_path."""
        resp = requests.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

    def generate_and_save(self, prompt: str, width: int, height: int, dest_path: Path):
        """Flujo completo: genera → espera → descarga → guarda."""
        gen_id = self.create_generation(prompt, width, height)
        urls = self.poll_generation(gen_id)
        self.download_image(urls[0], dest_path)


# ─── LÓGICA PRINCIPAL ─────────────────────────────────────────────────────────
def load_api_key() -> str:
    """Carga la API key desde variable de entorno, archivo .env o valor por defecto."""
    key = os.environ.get("LEONARDO_API_KEY", "")
    if not key:
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("LEONARDO_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not key:
        key = "5314be47-33c5-40bb-8731-1469de403105"
    return key


def run(args):
    # ── Cargar API Key ──────────────────────────────────────────────────────
    api_key = args.api_key or load_api_key()
    if not api_key and not args.dry_run:
        log("✗ No se encontró LEONARDO_API_KEY.", C.RED)
        log("  Opciones:", C.YELLOW)
        log("  1) export LEONARDO_API_KEY='tu_clave'", C.YELLOW)
        log("  2) Añadir LEONARDO_API_KEY=tu_clave al archivo .env del proyecto", C.YELLOW)
        log("  3) Pasar --api-key tu_clave", C.YELLOW)
        sys.exit(1)

    client = LeonardoClient(api_key) if not args.dry_run else None

    # ── Filtrar por categoría ────────────────────────────────────────────────
    categories = args.category if args.category else PRIORITY_ORDER
    assets = [a for a in ASSETS if a[0] in categories]

    # Ordenar por prioridad
    assets.sort(key=lambda a: PRIORITY_ORDER.index(a[0]) if a[0] in PRIORITY_ORDER else 99)

    # ── Resumen inicial ──────────────────────────────────────────────────────
    log(f"\n{'━'*60}", C.BOLD)
    log(f"  🐧 PinguPlay — Generador de Assets con Leonardo.AI", C.BOLD)
    log(f"{'━'*60}", C.BOLD)
    log(f"  Categorías : {', '.join(categories)}")
    log(f"  Total      : {len(assets)} assets")
    log(f"  Destino    : {ASSETS_ROOT}")
    log(f"  Modelo     : Leonardo Phoenix 1.0")
    log(f"  Modo       : {'DRY RUN (sin generar)' if args.dry_run else 'REAL'}")
    log(f"{'━'*60}\n", C.BOLD)

    # ── Procesar assets ──────────────────────────────────────────────────────
    success = skipped = errors = 0
    total = len(assets)

    for i, (category, filename, width, height, prompt) in enumerate(assets, 1):
        dest = ASSETS_ROOT / category / filename
        label = f"{category}/{filename}"

        if args.dry_run:
            log(f"  [{i:2d}/{total}] DRY RUN → {label} ({width}×{height})", C.BLUE)
            log(f"           Prompt: {prompt[:80]}...", C.CYAN)
            success += 1
            continue

        # Skip si ya existe
        if dest.exists() and not args.overwrite:
            log(f"  [{i:2d}/{total}] ⊙ SKIP  → {label}", C.YELLOW)
            skipped += 1
            continue

        log(f"\n  [{i:2d}/{total}] ⟳ {label} ({width}×{height})", C.BLUE)

        try:
            client.generate_and_save(prompt, width, height, dest)
            size_kb = dest.stat().st_size // 1024
            log(f"  [{i:2d}/{total}] ✓ OK    → {label} ({size_kb} KB)", C.GREEN)
            success += 1
        except Exception as e:
            log(f"  [{i:2d}/{total}] ✗ ERROR → {label}: {e}", C.RED)
            errors += 1

        # Rate limiting entre generaciones
        if i < total:
            time.sleep(DELAY_BETWEEN)

    # ── Resumen final ────────────────────────────────────────────────────────
    log(f"\n{'━'*60}", C.BOLD)
    log(f"  ✓ Generados : {success}", C.GREEN)
    log(f"  ⊙ Saltados  : {skipped}", C.YELLOW)
    log(f"  ✗ Errores   : {errors}", C.RED if errors else C.RESET)
    log(f"{'━'*60}\n", C.BOLD)

    if errors:
        log("Para reintentar solo los fallidos, vuelve a ejecutar el script.", C.YELLOW)
        log("Los ya generados serán saltados automáticamente.\n", C.YELLOW)


# ─── ARGUMENTOS CLI ───────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="PinguPlay — Generador de assets con Leonardo.AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generate_assets.py
  python generate_assets.py --category characters backgrounds
  python generate_assets.py --category games --overwrite
  python generate_assets.py --dry-run
  python generate_assets.py --api-key tu_clave_aqui
        """,
    )
    parser.add_argument(
        "--category", "-c",
        nargs="+",
        choices=["characters", "backgrounds", "ui", "games", "stickers", "avatars"],
        help="Categorías a generar (por defecto: todas por orden de prioridad)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Muestra qué se generaría sin llamar a la API",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobreescribe archivos ya existentes (por defecto los salta)",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        default=True,
        help="Salta archivos ya generados (comportamiento por defecto)",
    )
    parser.add_argument(
        "--api-key",
        help="API Key de Leonardo.AI (alternativa a la variable de entorno)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista todos los assets que se generarían y sale",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.list:
        categories = args.category if args.category else PRIORITY_ORDER
        assets = [a for a in ASSETS if a[0] in categories]
        assets.sort(key=lambda a: PRIORITY_ORDER.index(a[0]) if a[0] in PRIORITY_ORDER else 99)
        current_cat = None
        for cat, fname, w, h, _ in assets:
            if cat != current_cat:
                print(f"\n{C.BOLD}── {cat.upper()} ──{C.RESET}")
                current_cat = cat
            dest = ASSETS_ROOT / cat / fname
            status = f"{C.GREEN}✓{C.RESET}" if dest.exists() else f"{C.YELLOW}○{C.RESET}"
            print(f"  {status}  {fname:<35} {w}×{h}")
        print(f"\nTotal: {len(assets)} assets\n")
        sys.exit(0)

    run(args)
