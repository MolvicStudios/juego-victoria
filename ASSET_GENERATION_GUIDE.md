# 🎨 PinguPlay — Guía de Generación de Assets con Prompt2Image

> **Extensión**: Prompt2Image AI Generator (`maazsaboowala.prompt2image-ai-generator`)  
> **Motor**: Pollinations AI (gratuito, sin API key)  
> **Cómo usar**: `Ctrl+Shift+P` → `Prompt2Image: Generate Image` → pegar prompt → guardar en la ruta indicada

---

## 🗂️ ESTRUCTURA DE DESTINO

```
src/lib/assets/
├── characters/      ← Pingu y variantes
├── backgrounds/     ← Fondos de cada mundo
├── games/           ← Iconos de los 38 juegos
├── ui/              ← Botones, marcos, decoración
├── stickers/        ← Pegatinas del sistema de recompensas
└── avatars/         ← Avatares de perfil ilustrados
```

---

## 🔑 ESTILO BASE (incluir siempre en tus prompts)

Copia este fragmento al final de cualquier prompt si quieres consistencia de estilo:

```
flat cartoon illustration, vibrant bold colors, children's educational app art style, 
clean crisp outlines, cute friendly design, no text, no letters, no watermark, 
white background, isolated object
```

Para **fondos** (sin fondo blanco):
```
cartoon scene background, vibrant saturated colors, children's app illustration,
soft gradients, whimsical playful style, no text, no characters in foreground,
wide landscape format 16:9
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## FASE 3 — PERSONAJE PRINCIPAL (Pingu)
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> **Carpeta destino**: `src/lib/assets/characters/`  
> **Formato recomendado**: PNG 512×512

### 📌 CH-01 · `pingu-main.png`
**Uso**: Pantalla de inicio, sobre fondos

```
cute cartoon baby penguin standing upright, round body, big expressive dark eyes, 
tiny orange beak, small orange feet, friendly warm smile, looking forward, 
slightly tilted head, waving one flipper, flat 2D cartoon illustration, 
vibrant bold colors, clean outlines, white background, no text, no watermark, 
isolated character, children's educational app mascot style
```

---

### 📌 CH-02 · `pingu-happy.png`
**Uso**: Celebración, correct answer

```
cute cartoon baby penguin jumping for joy, arms raised up in the air, 
huge beaming smile showing teeth, sparkles and stars around it, 
round body black and white, tiny orange beak and feet, 
flat 2D cartoon illustration, vibrant bold colors, clean outlines, 
white background, no text, no watermark, isolated character, children's app style
```

---

### 📌 CH-03 · `pingu-thinking.png`
**Uso**: Pantalla de selección de nivel, loading

```
cute cartoon baby penguin thinking pose, one flipper touching chin thoughtfully, 
one eye slightly squinted, small thought bubble above head, 
round body black and white, tiny orange beak, 
flat 2D cartoon illustration, pastel background glow, clean outlines, 
white background, no text, no watermark, isolated character, children's app style
```

---

### 📌 CH-04 · `pingu-sad.png`
**Uso**: Wrong answer, intento fallido

```
cute cartoon baby penguin sad face, droopy eyes with small tear, 
slight frown, arms hanging down, small body slightly hunched, 
round body black and white, tiny orange beak and feet, 
flat 2D cartoon illustration, vibrant colors despite sad expression, 
clean outlines, white background, no text, no watermark, children's app style
```

---

### 📌 CH-05 · `pingu-excited.png`
**Uso**: Nuevo nivel desbloqueado, streak

```
cute cartoon baby penguin super excited, running forward with arms stretched back, 
huge smile, small motion lines showing speed, stars and confetti around it, 
round body black and white, tiny orange beak and feet, 
flat 2D cartoon illustration, vibrant bold colors, dynamic pose, 
white background, no text, no watermark, children's app character
```

---

### 📌 CH-06 · `pingu-sleeping.png`
**Uso**: Pantalla de descanso, modo noche

```
cute cartoon baby penguin sleeping, eyes closed with ZZZ floating bubbles, 
small pillow or cloud under head, peaceful smile, 
round body black and white, tiny orange beak and feet, nightcap optional, 
flat 2D cartoon illustration, soft pastel colors, 
white background, no text, no watermark, isolated, children's app style
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## FASE 3 — FONDOS DE MUNDO
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> **Carpeta destino**: `src/lib/assets/backgrounds/`  
> **Formato recomendado**: PNG 1280×800 (landscape tablet)

### 🌤️ BG-01 · `bg-nubecitas.png`
**Mundo**: Nubecitas · Edad: 0-2 años · Color: `#A78BFA`

```
dreamy sky background for children's app, fluffy white cartoon clouds, 
soft lavender and baby blue sky gradient, tiny stars and sparkles, 
pastel rainbow faintly visible, 
cartoon flat illustration style, gentle and soothing, 
very soft colors pastel palette, no characters, no text, 
wide landscape format for tablet, children's educational app background
```

---

### 🌿 BG-02 · `bg-exploradores.png`
**Mundo**: Exploradores · Edad: 3-5 años · Color: `#4D9FEC`

```
colorful cartoon jungle and nature background for children's app, 
lush green trees and tropical leaves, bright blue sky with fluffy clouds, 
friendly cartoon animals peeking from foliage (birds, butterflies, caterpillars), 
rolling green hills, cartoon flat illustration style, 
vibrant primary colors, no main characters, no text, 
wide landscape format for tablet, children's educational app background
```

---

### ⚔️ BG-03 · `bg-aventureros.png`
**Mundo**: Aventureros · Edad: 6-8 años · Color: `#6BCB77`

```
colorful cartoon adventure landscape background for children's app, 
whimsical castle on green hill, forest with tall trees, 
friendly cartoon dragon flying in background, treasure chest, 
bright blue sky with cartoon sun, cartoon flat illustration style, 
vibrant bold colors, action adventure feel but friendly, no main characters, no text, 
wide landscape format for tablet, children's educational app background
```

---

### 🏆 BG-04 · `bg-maestros.png`
**Mundo**: Maestros · Edad: 9-12 años · Color: `#FF9F43`

```
colorful cartoon space and science background for children's app, 
night sky with stars planet earth and moon, cartoon rocket ship, 
floating books and stars, telescope, 
deep blue and purple gradient sky, bright stars and nebula, 
cartoon flat illustration style, vibrant colors, no main characters, no text, 
wide landscape format for tablet, children's educational app background
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## FASE 3 — ICONOS DE MUNDO (Selector de perfil)
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> **Carpeta destino**: `src/lib/assets/ui/`  
> **Formato recomendado**: PNG 256×256

### 🪧 WI-01 · `world-nubecitas.png`
```
cute cartoon cloud icon, fluffy white cloud with pastel purple border, 
tiny stars and sparkles on it, soft lavender glow, 
flat vector icon style, vibrant but soft colors, white background, 
no text, no watermark, children's app icon, 256x256
```

### 🪧 WI-02 · `world-exploradores.png`
```
cute cartoon globe icon, round earth cartoon style, 
green continents bright blue ocean, tiny leaf and magnifying glass overlaid, 
flat vector icon style, vibrant primary colors, white background, 
no text, no watermark, children's app icon, 256x256
```

### 🪧 WI-03 · `world-aventureros.png`
```
cute cartoon adventure icon, crossed cartoon sword and shield, 
bright colors red shield with star, golden sword, 
flat vector icon style, vibrant bold colors, white background, 
no text, no watermark, children's app icon, 256x256
```

### 🪧 WI-04 · `world-maestros.png`
```
cute cartoon trophy icon, gold trophy cup with star, 
bright gold and orange colors, sparkles around it, 
flat vector icon style, vibrant bold colors, white background, 
no text, no watermark, children's app icon, 256x256
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## FASE 3 — ICONOS DE JUEGOS (38 juegos)
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> **Carpeta destino**: `src/lib/assets/games/`  
> **Formato recomendado**: PNG 256×256  
> **Estilo base todos**: `flat cartoon game icon, vibrant bold colors, clean thick outlines, white background, no text, no letters, no numbers, no watermark, children's educational app icon, cute friendly style, 256x256`

---

### G1 · `g1-formas.png` — Formas (rojo `#FF6B6B`)
```
cartoon icon showing colorful geometric shapes arranged playfully, 
red circle blue triangle green square yellow star, 
each shape with thick cartoon outline and different bright color, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G2 · `g2-contar.png` — Contar (naranja `#FF9F43`)
```
cartoon icon showing five bright red apples being counted, 
small cartoon hand pointing at them, 
cheerful counting game feel, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, no numbers, children's app icon, 256x256
```

### G3 · `g3-letras.png` — Letras (amarillo `#FFD93D`)
```
cartoon icon showing large colorful letter A with decorative stars, 
bright yellow and orange colors, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, children's app icon only letter A visible, 256x256
```

### G4 · `g4-pintar.png` — Pintar (verde `#6BCB77`)
```
cartoon icon showing a paintbrush making a colorful stroke, 
rainbow paint splash, palette with vibrant colors, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G5 · `g5-memoria.png` — Memoria (azul `#4D9FEC`)
```
cartoon icon showing two matching playing cards face down with question mark, 
one card being flipped to reveal a colorful star, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, no numbers, children's app icon, 256x256
```

### G6 · `g6-piano.png` — Piano Mágico (morado `#A78BFA`)
```
cartoon icon showing miniature colorful piano keyboard, 
musical notes floating above the keys, 
white and black keys with bright colored notes, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G7 · `g7-numeros.png` — Números (rosa `#F472B6`)
```
cartoon icon showing colorful number blocks in sequence, 
bright colored cubes with numbers one two three on them, 
fun stacking arrangement, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, children's app icon, 256x256
```

### G8 · `g8-queves.png` — ¿Qué Ves? (teal `#2DD4BF`)
```
cartoon icon showing a cute cartoon lion face, 
big expressive friendly eyes, mane with bright colors, 
looking directly forward with curious expression, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G9 · `g9-puzle.png` — Mini Puzle (rojo `#FF6B6B`)
```
cartoon icon showing four colorful puzzle pieces fitting together, 
each piece a different bright color, one piece being placed, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G10 · `g10-colores.png` — Colores (azul `#4D9FEC`)
```
cartoon icon showing color wheel with six vibrant sections, 
rainbow wheel cartoon style alternating red orange yellow green blue purple, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G11 · `g11-sumas.png` — Sumas (verde `#6BCB77`)
```
cartoon icon showing two groups of colorful fruits separated by a plus sign, 
two red apples plus three oranges, cute fruit characters, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text no numbers, children's app icon, 256x256
```

### G12 · `g12-traza.png` — Traza Letras (morado `#A78BFA`)
```
cartoon icon showing a pencil tracing dotted lines forming a letter shape, 
dotted path guidelines, bright colored pencil leaving trail, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G13 · `g13-oyes.png` — ¿Qué Oyes? (rosa `#F472B6`)
```
cartoon icon showing a cute ear with colorful sound waves emanating from it, 
bright pink and blue sound waves, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G14 · `g14-laberinto.png` — Laberinto (teal `#2DD4BF`)
```
cartoon icon showing a small cute maze from above view, 
colorful walls and a tiny penguin at the start, star at the finish, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G15 · `g15-tamanos.png` — Grande/Pequeño (naranja `#FF9F43`)
```
cartoon icon showing a large cartoon elephant next to a tiny cartoon mouse, 
size comparison, both cute and friendly, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G16 · `g16-patrones.png` — Patrones (morado `#A78BFA`)
```
cartoon icon showing colored shapes in a repeating pattern sequence, 
red circle blue square red circle blue question mark, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no letters no text, children's app icon, 256x256
```

### G17 · `g17-globos.png` — Globos (rosa `#F472B6`)
```
cartoon icon showing three colorful balloons floating up, 
red green and blue balloons with strings, 
sparkles and festive feel, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G18 · `g18-animales.png` — Animales (naranja `#FF9F43`)
```
cartoon icon showing cute cartoon animal paw print with small animal faces around it, 
colorful cat dog rabbit faces peeking, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G19 · `g19-silabas.png` — Sílabas (rojo `#FF6B6B`)
```
cartoon icon showing two cartoon hands clapping together, 
motion lines showing clapping rhythm, 
bright and energetic, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G20 · `g20-rimas.png` — Rimas (azul `#4D9FEC`)
```
cartoon icon showing a cute microphone with musical notes and rhyming symbols, 
colorful sound waves forming heart shape, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G21 · `g21-deletrear.png` — Deletrear (verde `#6BCB77`)
```
cartoon icon showing colorful letter tiles being arranged, 
scrambled cartoon alphabet blocks forming a word shape, 
bright colored cubes with single letters C A T, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, children's app icon, 256x256
```

### G22 · `g22-opuestos.png` — Opuestos (naranja `#FF9F43`)
```
cartoon icon showing two arrows pointing in opposite directions, 
one pointing left one pointing right, bright contrasting colors, 
also showing small sun and moon to illustrate opposites, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G23 · `g23-frase.png` — Completa Frase (morado `#A78BFA`)
```
cartoon icon showing a speech bubble with a blank space in the middle, 
dotted line where word goes, colorful friendly bubble, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G24 · `g24-restas.png` — Restas (rojo `#FF6B6B`)
```
cartoon icon showing five colorful strawberries with three of them crossed out playfully, 
minus sign between groups, cute cartoon style, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no numbers no text, children's app icon, 256x256
```

### G25 · `g25-parimpar.png` — Par o Impar (azul `#4D9FEC`)
```
cartoon icon showing two groups of colored dots, 
left side two matching paired dots, right side three dots one alone, 
cute cartoon dots with faces, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G26 · `g26-mayormenor.png` — Mayor/Menor (verde `#6BCB77`)
```
cartoon icon showing cartoon balance scale with different weights, 
one side with more colorful blocks than the other, scale tilting, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G27 · `g27-monedas.png` — Monedas (amarillo `#FFD93D`)
```
cartoon icon showing shiny cartoon coins stacked and scattered, 
gold and silver cartoon coins, small piggy bank in background, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text no numbers, children's app icon, 256x256
```

### G28 · `g28-reloj.png` — El Reloj (teal `#2DD4BF`)
```
cartoon icon showing a cute round analog clock with a friendly face, 
big numbers on clock face, clock hands pointing at three o'clock, 
smiling clock character, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, children's app icon, 256x256
```

### G29 · `g29-intruso.png` — El Intruso (rojo `#FF6B6B`)
```
cartoon icon showing three matching cartoon fruits and one different item among them, 
three apples and one banana highlighted with question mark, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G30 · `g30-sombras.png` — Sombras (morado `#A78BFA`)
```
cartoon icon showing a bright cartoon star above and its dark shadow silhouette below, 
clean shadow matching outline of object, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G31 · `g31-secuencias.png` — Secuencias (azul `#4D9FEC`)
```
cartoon icon showing colored number train blocks in sequence, 
colorful train cars connected, one car missing with question mark, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G32 · `g32-categorias.png` — Categorías (verde `#6BCB77`)
```
cartoon icon showing two colorful cartoon boxes being sorted, 
fruits going into one box animals into another, 
classification sorting game feel, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G33 · `g33-sudoku.png` — Sudoku Mini (naranja `#FF9F43`)
```
cartoon icon showing a small cute grid with colorful emoji icons in cells, 
two by two grid with star heart and sun symbols, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G34 · `g34-ritmo.png` — Ritmo (rosa `#F472B6`)
```
cartoon icon showing colorful cartoon drums with music notes floating above, 
bright drumsticks hitting drum, sound waves visible, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G35 · `g35-conecta.png` — Conecta Puntos (teal `#2DD4BF`)
```
cartoon icon showing numbered dots connected by bright colored lines forming a star shape, 
dots being connected with glowing line, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G36 · `g36-espejo.png` — Espejo (morado `#A78BFA`)
```
cartoon icon showing a cartoon mirror with a simple shape on one side and its reflection on the other, 
butterfly mirror reflection, bright colorful mirror frame, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G37 · `g37-burbujas.png` — Burbujas (azul `#4D9FEC`)
```
cartoon icon showing colorful cartoon bubbles floating up, 
each bubble a different color red blue green, 
sparkling transparent bubbles with highlights, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

### G38 · `g38-tangram.png` — Tangram (naranja `#FF9F43`)
```
cartoon icon showing colorful tangram pieces arranged to form a simple bird or cat shape, 
geometric pieces in bright contrasting colors, 
flat cartoon game icon, vibrant bold colors, clean thick outlines, 
white background, no text, children's app icon, 256x256
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## FASE 3 — ELEMENTOS DE UI
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> **Carpeta destino**: `src/lib/assets/ui/`  
> **Formato recomendado**: PNG con transparencia o fondo blanco, 256×256 o 512×256

### UI-01 · `medal-gold.png`
```
shiny golden cartoon medal with star in center, golden ribbon, 
sparkles and gleam, award winner medal, 
flat cartoon illustration, vibrant gold and yellow colors, clean thick outlines, 
white background, no text, children's app reward icon, 256x256
```

### UI-02 · `medal-silver.png`
```
shiny silver cartoon medal with star in center, silver ribbon, 
sparkles, second place award medal, 
flat cartoon illustration, bright silver colors, clean thick outlines, 
white background, no text, children's app reward icon, 256x256
```

### UI-03 · `medal-bronze.png`
```
shiny bronze cartoon medal with star in center, brown copper ribbon, 
sparkles, third place award medal, 
flat cartoon illustration, warm bronze copper colors, clean thick outlines, 
white background, no text, children's app reward icon, 256x256
```

### UI-04 · `trophy.png`
```
large shiny cartoon trophy cup, golden with stars and sparkles emanating, 
celebration confetti around it, tall ornate trophy, 
flat cartoon illustration, vibrant gold colors, clean thick outlines, 
white background, no text, children's app achievement icon, 256x256
```

### UI-05 · `star-filled.png`
```
large bright five-pointed cartoon star, vibrant yellow and orange gradient, 
thick outline, inner glow, sparkles around it, 
flat cartoon illustration, vibrant yellow/gold colors, 
white background, no text, children's app icon, 256x256
```

### UI-06 · `star-empty.png`
```
five-pointed cartoon star outline, light gray unfilled, 
clean outline only, waiting to be filled, 
flat cartoon illustration, light gray outline, 
white background, no text, children's app icon, 256x256
```

### UI-07 · `confetti-burst.png`
```
colorful confetti explosion burst, rainbow colored confetti pieces flying outward, 
streamers and party poppers, celebration moment, 
flat cartoon illustration, vibrant rainbow colors, 
white background, no text, children's app celebration, 512x512
```

### UI-08 · `lock.png`
```
cute cartoon padlock, friendly rounded shape with small face, 
vibrant blue and gray colors, locked state, 
flat cartoon illustration, bold outlines, 
white background, no text, children's app UI icon, 256x256
```

### UI-09 · `home-button.png`
```
cute cartoon house icon with friendly face window and door, 
vibrant blue roof orange walls, 
flat cartoon illustration, bold outlines, 
white background, no text, children's navigation icon, 256x256
```

### UI-10 · `back-arrow.png`
```
cute rounded cartoon back arrow, thick friendly curved arrow shape, 
bright blue and white colors, child-friendly, 
flat cartoon illustration, bold thick outlines, 
white background, no text, children's navigation icon, 256x256
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## FASE 3 — SISTEMA DE STICKERS (20 hitos)
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> **Carpeta destino**: `src/lib/assets/stickers/`  
> **Formato recomendado**: PNG 256×256  
> **Estilo base**: `cute illustrated sticker, vibrant bold colors, thick cartoon outline, white background, no text, no watermark, children's reward sticker, flat cartoon illustration, 256x256`

| # | Archivo | Hito | Prompt clave a añadir al estilo base |
|---|---------|------|--------------------------------------|
| 1 | `stk-flor.png` | 5⭐ | `cute cartoon pink cherry blossom flower with dewdrops, petals spreading out, soft pink colors` |
| 2 | `stk-unicornio.png` | 10⭐ | `magical cartoon unicorn with rainbow mane flying, sparkles and stars around it` |
| 3 | `stk-corona.png` | 20⭐ | `shiny cartoon golden crown with colorful gems, royalty crown, sparkles` |
| 4 | `stk-arcoiris.png` | 35⭐ | `bright cartoon rainbow emerging from clouds, colorful arc with fluffy white clouds at ends` |
| 5 | `stk-castillo.png` | 50⭐ | `magical cartoon castle with towers and flags, fantasy rainbow bridge, fluffy clouds` |
| 6 | `stk-circo.png` | 75⭐ | `colorful cartoon circus tent with stars and lights, festive flags and balloons` |
| 7 | `stk-diamante.png` | 100⭐ | `sparkling cartoon diamond gem, light blue crystal with rainbow reflections, gleaming` |
| 8 | `stk-cohete.png` | 130⭐ | `cartoon rocket ship launching with flame trail, stars and planets around it, colorful` |
| 9 | `stk-estrella.png` | 170⭐ | `giant cartoon shooting star with long sparkling tail, bright gold and white` |
| 10 | `stk-carrousel.png` | 200⭐ | `magical cartoon merry-go-round with colorful horses and lights, festive rotating` |
| 11 | `stk-mariposa.png` | 250⭐ | `beautiful cartoon butterfly with colorful patterned wings, flowers around it` |
| 12 | `stk-trofeo.png` | 300⭐ | `grand cartoon championship trophy, golden with stars and confetti` |
| 13 | `stk-mascaras.png` | 400⭐ | `colorful cartoon theater masks comedy and drama, stars and spotlights` |
| 14 | `stk-princesa.png` | 500⭐ | `cute cartoon princess with sparkly dress and tiara, magic wand and stars` |
| 15 | `stk-planeta.png` | 650⭐ | `colorful cartoon planet Earth with continents, stars and space around it` |
| 16 | `stk-fuegos.png` | 800⭐ | `colorful cartoon fireworks exploding, multiple colored bursts and sparkles` |
| 17 | `stk-galaxia.png` | 1000⭐ | `magical cartoon galaxy swirl, purple and blue cosmic spiral with stars and nebula` |
| 18 | `stk-unicornio2.png` | 1300⭐ | `super magical cartoon unicorn with elaborate rainbow wings and crown, very sparkly` |
| 19 | `stk-magico.png` | 1700⭐ | `magical cartoon sparkling star burst with multiple layers of light and glitter` |
| 20 | `stk-medalla-oro.png` | 2000⭐ | `ultimate golden first place cartoon medal with elaborate decorations, stars and laurels` |

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## FASE 3 — AVATARES DE PERFIL (10 avatares ilustrados)
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> **Carpeta destino**: `src/lib/assets/avatars/`  
> **Formato recomendado**: PNG 256×256  
> **Estilo base**: `cute cartoon avatar portrait, round friendly face, vibrant bold colors, thick outlines, white background, no text, children's app profile avatar, flat 2D illustration, 256x256`

| Archivo | Personaje actual | Prompt extra |
|---------|-----------------|--------------|
| `av-unicornio.png` | 🦄 | `cute cartoon unicorn head portrait, colorful rainbow horn and mane, big eyes` |
| `av-princesa.png` | 👸 | `cute cartoon princess portrait, sparkly tiara, long colorful hair` |
| `av-mariposa.png` | 🦋 | `cute cartoon butterfly character portrait, colorful wings, friendly smile` |
| `av-estrella.png` | 🌟 | `cute cartoon star character portrait, golden star with big eyes and smile` |
| `av-gato.png` | 🐱 | `cute cartoon cat portrait, round face, big eyes, soft pastel colors` |
| `av-perro.png` | 🐶 | `cute cartoon dog portrait, floppy ears, big friendly eyes, brown and white` |
| `av-conejo.png` | 🐰 | `cute cartoon bunny portrait, long floppy ears, pink nose, white and pink` |
| `av-panda.png` | 🐼 | `cute cartoon panda portrait, round black and white face, big eyes` |
| `av-zorro.png` | 🦊 | `cute cartoon fox portrait, pointy ears, orange and white face, bushy tail` |
| `av-oso.png` | 🐻 | `cute cartoon bear portrait, round face, warm brown colors, honey drip` |

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## RESUMEN DE PRODUCCIÓN
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Categoría | Cant. | Directorio | Prioridad |
|-----------|-------|------------|-----------|
| 🐧 Personaje Pingu | 6 | `characters/` | 🔴 Alta |
| 🌍 Fondos de mundo | 4 | `backgrounds/` | 🔴 Alta |
| 🌟 Iconos de mundo | 4 | `ui/` | 🔴 Alta |
| 🎮 Iconos de juego | 38 | `games/` | 🟡 Media |
| 🎨 Elementos UI | 10 | `ui/` | 🟡 Media |
| ✨ Stickers | 20 | `stickers/` | 🟢 Baja |
| 👤 Avatares | 10 | `avatars/` | 🟢 Baja |
| **TOTAL** | **92** | | |

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## PLAN TÉCNICO — FASES 4 y 5
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### FASE 4 — Mejoras de UX Infantil (tras tener assets)

**Archivos a modificar:**
- `src/lib/components/WorldHub.svelte` — usar `bg-{world}.png` como fondo
- `src/lib/components/GameShell.svelte` — usar `pingu-happy/sad/thinking.png`
- `src/routes/+page.svelte` — usar `pingu-main.png` + avatares ilustrados
- `src/app.css` — animación `invitePulse` en tarjetas + `wiggle` en errores

**Cambios clave:**
```svelte
<!-- WorldHub: fondo temático -->
<div class="scr on" style="background-image:url({bgUrl});background-size:cover">

<!-- GameShell: Pingu reactivo -->
{#if celebrationVisible}
  <img src="/assets/characters/pingu-happy.png" alt="" />
{:else if wrongAnswer}
  <img src="/assets/characters/pingu-sad.png" alt="" />
{/if}
```

---

### FASE 5 — Gamificación Visual Avanzada

**Cambios en `data.js`:**
- Añadir campo `img` a cada juego: `{ n:1, img:'g1-formas.png', ...}`
- Stickers: cambiar emojis por `<img>` de `stickers/`

**Cambios en `WorldHub.svelte`:**
```svelte
<!-- Iconos ilustrados en tarjetas -->
<img class="ico-img" src="/assets/games/{gm.img}" alt={gm.name} />
```

**Cambios en `progress.js` / celebración:**
- Sticker pop-up animado al desbloquear hito
- Mostrar imagen ilustrada del sticker ganado

**CSS nuevo:**
```css
.ico-img { width: var(--icon-size); height: var(--icon-size); object-fit: contain; }
.pingu-react { position: absolute; bottom: 0; right: 16px; 
  width: 120px; animation: pBounce 1.5s infinite; }
```

---

## 💡 TIPS PARA POLLINATIONS AI

- Si el resultado no es satisfactorio, añade: `high quality, detailed, professional`
- Para más contraste: `bold saturated colors, high contrast`
- Para estilo más uniforme entre assets: mantener siempre `flat cartoon illustration` como primer descriptor
- Tamaños recomendados en la extensión: **512×512** para caracteres, **1024×512** para fondos
- Si aparece texto no deseado: añadir `no letters, no numbers, no labels` al prompt
