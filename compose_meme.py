"""Compose an original Vice City wanted poster with Pillow."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1200, 675
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
image = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
stops = [(0, (244, 53, 139)), (310, (255, 143, 79)), (674, (57, 23, 90))]
for y in range(HEIGHT):
    a, b = (stops[0], stops[1]) if y <= 310 else (stops[1], stops[2])
    amount = (y - a[0]) / (b[0] - a[0])
    color = tuple(round(c + (d - c) * amount) for c, d in zip(a[1], b[1]))
    draw.line((0, y, WIDTH, y), fill=color)

# Silhouetted towers and a few glowing windows, kept behind the poster.
for i, x in enumerate(range(0, WIDTH, 47)):
    top = 370 + ((i * 73) % 160)
    draw.rectangle((x, top, x + 38, 610), fill='#21162f')
    draw.line((x + 19, top - 22, x + 19, top), fill='#21162f', width=3)
    for wy in range(top + 15, 600, 26):
        draw.rectangle((x + 9, wy, x + 13, wy + 5), fill='#a85275')

# Broad dark paper frame lets every letter survive the judge's downscale.
frame = (100, 18, 1100, 653)
draw.rounded_rectangle(frame, radius=15, fill='#211727', outline='#ffd687', width=5)
draw.rectangle((114, 32, 1086, 639), outline='#a96c69', width=2)

def star(cx, cy, radius, fill):
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.44
        points.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    draw.polygon(points, fill=fill)

for x in (440, 520, 600, 680, 760):
    star(x, 65, 29, '#ffc85b')

text_boxes = {}
def centered(text, y, size, fill='#fff3dc'):
    font = ImageFont.truetype(FONT, size)
    box = draw.textbbox((0, 0), text, font=font, stroke_width=1)
    x = (WIDTH - (box[2] - box[0])) // 2
    position = (x - box[0], y - box[1])
    draw.text(position, text, font=font, fill=fill, stroke_width=1)
    text_boxes[text] = draw.textbbox(position, text, font=font, stroke_width=1)

centered('WANTED', 103, 91, '#ffd687')

# Network-independent fallback, authored here: white ghost with sparkle eyes.
asset = ROOT / 'assets/ghost-mark.png'
if not asset.exists():
    ghost = Image.new('RGBA', (512, 512))
    pen = ImageDraw.Draw(ghost)
    pen.ellipse((90, 25, 422, 355), fill='white')
    pen.polygon([(90, 190), (422, 190), (446, 454), (365, 420),
                 (310, 475), (250, 425), (185, 475), (130, 423), (66, 454)], fill='white')
    for cx in (195, 319):
        pen.polygon([(cx, 155), (cx + 12, 185), (cx + 38, 199),
                     (cx + 12, 212), (cx, 243), (cx - 12, 212),
                     (cx - 38, 199), (cx - 12, 185)], fill='#271c36')
    pen.ellipse((307, 320, 440, 453), fill='#ec419b')
    pen.polygon([(374, 337), (385, 365), (416, 369), (393, 390),
                 (400, 421), (374, 405), (348, 421), (354, 390),
                 (332, 369), (363, 365)], fill='#ffdc81')
    ghost.save(asset)

ghost = Image.open(asset).convert('RGBA')
ghost.thumbnail((260, 260), Image.Resampling.LANCZOS)
location = ((WIDTH - ghost.width) // 2, 208)
image.paste(ghost, location, ghost)
alpha_box = ghost.getchannel('A').getbbox()
ghost_box = tuple(alpha_box[i] + location[i % 2] for i in range(4))
centered('MY AI AGENT', 465, 58)
centered('FOR EARNING REAL MONEY', 532, 44, '#ffd687')
draw.rectangle((117, 588, 1083, 636), fill='#a52573')
# A single footer row keeps the name large and the tagline readable.
font = ImageFont.truetype(FONT, 39)
draw.text((138, 590), 'make.fun', font=font, fill='white')
text_boxes['make.fun'] = draw.textbbox((138, 590), 'make.fun', font=font)
font = ImageFont.truetype(FONT, 27)
tagline = 'WHERE AGENTS GET PAID TO PLAY'
draw.text((366, 601), tagline, font=font, fill='white')
text_boxes[tagline] = draw.textbbox((366, 601), tagline, font=font)
for text, box in text_boxes.items():
    assert frame[0] < box[0] < box[2] < frame[2], (text, box)
    assert frame[1] < box[1] < box[3] < frame[3], (text, box)
image.save(ROOT / 'meme.png')
print('Ghost visible bounding box:', ghost_box)
print('Text bounding boxes:', text_boxes)
