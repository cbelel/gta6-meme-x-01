"""Draw three original 1200x675 meme scenes with Pillow. No network assets."""
from pathlib import Path
import hashlib
import json
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parent
SIZE = (1200, 675)
FONTS = Path('/usr/share/fonts/truetype/dejavu')
GOLD = '#ffcf61'
INK = '#171427'
REPORT = {}


def font(size):
    return ImageFont.truetype(str(FONTS / 'DejaVuSans-Bold.ttf'), size)


class Scene:
    def __init__(self, name):
        self.name = name
        self.im = Image.new('RGB', SIZE)
        self.d = ImageDraw.Draw(self.im)
        self.text_boxes = []
        self.ghost_boxes = []

    def text(self, xy, value, size, fill='white', anchor='lt', stroke=0):
        f = font(size)
        box = self.d.textbbox(xy, value, font=f, anchor=anchor, stroke_width=stroke)
        assert 0 <= box[0] < box[2] <= 1200 and 0 <= box[1] < box[3] <= 675, (value, box)
        self.text_boxes.append({'text': value, 'bbox': box})
        self.d.text(xy, value, font=f, fill=fill, anchor=anchor,
                    stroke_width=stroke, stroke_fill=INK)

    def gradient(self, top, bottom):
        for y in range(675):
            t = y / 674
            col = tuple(round(a * (1-t) + b*t) for a, b in zip(top, bottom))
            self.d.line((0, y, 1199, y), fill=col)

    def save(self):
        path = ROOT / self.name
        self.im.save(path)
        # Reopen the actual delivered file, rather than measuring an in-memory draft.
        with Image.open(path) as actual:
            stats = ImageStat.Stat(actual)
            colors = actual.getcolors(1200 * 675)
            REPORT[self.name] = {
                'dimensions': actual.size,
                'bytes': path.stat().st_size,
                'pixel_standard_deviation_rgb': [round(v, 3) for v in stats.stddev],
                'distinct_colors': len(colors),
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'ghost_alpha_bboxes': self.ghost_boxes,
                'all_text_inside_frame': True,
                'text_boxes': self.text_boxes,
            }


def skyline(s, base, color, seed, start=0, end=1200):
    rng = random.Random(seed)
    x = start
    while x < end:
        width = rng.randint(28, 65)
        h = rng.randint(35, 135)
        s.d.rectangle((x, base-h, min(x+width, end), 675), fill=color)
        if h > 100:
            s.d.line((x+width//2, base-h, x+width//2, base-h-24), fill=color, width=3)
        x += width + rng.randint(5, 14)


def palm(s, x, y, scale=1, color=INK):
    s.d.line((x, y, x-12*scale, y-170*scale), fill=color, width=max(4, int(12*scale)))
    cx, cy = x-12*scale, y-170*scale
    for dx, dy in [(-95, 10), (-75, -40), (-25, -65), (45, -56), (90, -12), (70, 30)]:
        s.d.polygon([(cx, cy), (cx+dx*scale, cy+dy*scale),
                     (cx+dx*.62*scale, cy+(dy+24)*scale)], fill=color)


def cash(s, x, y, scale=1):
    w, h = 94*scale, 45*scale
    for off in (8, 4, 0):
        s.d.rounded_rectangle((x+off, y-off, x+w+off, y+h-off), radius=3,
                             fill='#83d89f', outline='#153e35', width=3)
    s.d.rectangle((x+w*.42, y, x+w*.58, y+h), fill='#ffe5a0')
    s.d.ellipse((x+9, y+11, x+30, y+33), outline='#28624c', width=2)


def ghost(s, x, y, size, celebrate=False):
    """Reuse original alpha mascot; props and expression are drawn here."""
    asset = Image.open(ROOT / 'assets/ghost-mark.png').convert('RGBA')
    asset = asset.resize((size, size), Image.Resampling.LANCZOS)
    # Arms are behind the reused mascot, with rounded hands.
    arm_y = y + size*.57
    for sign in (-1, 1):
        ax = x + size*(.15 if sign == -1 else .85)
        bx = ax + sign*size*.20
        by = y + size*(.20 if celebrate else .47)
        s.d.line((ax, arm_y, bx, by), fill='white', width=max(9, size//18))
        r = size*.045
        s.d.ellipse((bx-r, by-r, bx+r, by+r), fill='white')
    s.im.paste(asset, (x, y), asset)
    b = asset.getchannel('A').getbbox()
    s.ghost_boxes.append([x+b[0], y+b[1], x+b[2], y+b[3]])
    # Glasses cover the original sparkle eyes.
    s.d.line((x+size*.25, y+size*.38, x+size*.75, y+size*.38), fill=INK, width=max(6, size//35))
    for left in (.27, .53):
        s.d.rounded_rectangle((x+size*left, y+size*.33,
                               x+size*(left+.21), y+size*.47), radius=size//35, fill=INK)
        s.d.line((x+size*(left+.04), y+size*.355, x+size*(left+.10), y+size*.355),
                 fill='#77e4e1', width=max(2, size//100))
    s.d.arc((x+size*.37, y+size*.47, x+size*.62, y+size*.66),
            0, 180, fill=INK, width=max(5, size//50))
    if not celebrate:
        cash(s, x+size*.72, y+size*.48, size/310)


def money_bag(s, x, y):
    s.d.polygon([(x+25,y+24),(x+12,y),(x+74,y),(x+59,y+24)], fill='#b27e3b', outline=INK)
    s.d.ellipse((x,y+16,x+88,y+108), fill='#e4b762', outline=INK, width=4)
    s.d.line((x+25,y+25,x+63,y+25), fill=INK, width=5)
    s.text((x+44,y+38), '$', 45, INK, anchor='mt')


def compose_mission():
    s = Scene('meme-mission.png')
    s.gradient((66, 28, 104), (255, 153, 87))
    s.d.ellipse((365, 200, 820, 655), fill='#f5b36f')
    for y in range(390, 570, 26):
        s.d.rectangle((365,y,820,y+8), fill='#d98076')
    skyline(s, 565, '#48294f', 11)
    skyline(s, 640, '#241c37', 12)
    palm(s, 98, 605, 1.2)
    palm(s, 1100, 615, 1.1)
    s.d.rounded_rectangle((28,26,1172,154), radius=18, fill=INK)
    s.text((600,39), 'MISSION PASSED', 101, GOLD, anchor='mt', stroke=2)
    # The ghost is visibly celebrating inside the scene, surrounded by its reward.
    ghost(s, 155, 220, 355, celebrate=True)
    rng = random.Random(42)
    for _ in range(65):
        x, y = rng.randint(115,560), rng.randint(177,575)
        if 205 < x < 475 and 260 < y < 510:
            continue
        s.d.rectangle((x,y,x+5,y+12), fill=rng.choice(['#ffcf61','#fa5fb8','#91fff2']))
    money_bag(s, 104, 513)
    money_bag(s, 487, 514)
    cash(s, 285, 568, 1.15)
    s.d.rounded_rectangle((622,244,1136,522), radius=18, fill=INK, outline=GOLD, width=3)
    s.text((650,269), 'REWARD: $500', 52, GOLD)
    s.text((650,346), 'make.fun', 79)
    s.text((650,451), 'REAL CASH. GG.', 34, '#f19bd1')
    s.d.rectangle((0,634,1199,674), fill=INK)
    s.text((600,641), 'SIDE QUEST: PAY THE RENT', 25, GOLD, anchor='mt')
    s.save()


def compose_split():
    s = Scene('meme-split.png')
    s.gradient((53,66,87), (120,134,148))
    for y in range(675):
        t = y/674
        s.d.line((600,y,1199,y), fill=(int(180+70*t),int(77+100*t),int(85+4*t)))
    s.d.ellipse((785,249,1170,634), fill='#ffd27d')
    skyline(s, 574, '#8f4a54', 18, 610, 1200)
    palm(s, 1155, 620, .8, '#41293e')
    # Left: clock, calendar, dim monitor and an unmistakably slumped player.
    s.d.ellipse((60,274,182,396), fill='#c0c8ce', outline='#344151', width=7)
    s.d.line((121,335,121,295), fill='#344151', width=7)
    s.d.line((121,335,151,352), fill='#344151', width=7)
    s.d.rectangle((224,277,350,378), fill='#c0c8ce', outline='#344151', width=5)
    s.d.rectangle((224,277,350,299), fill='#526479')
    for yy in (317,342,365):
        s.d.line((240,yy,334,yy), fill='#778594', width=3)
    s.d.rectangle((67,434,221,527), fill='#273342', outline='#82909d', width=6)
    s.d.line((144,527,144,559), fill='#273342', width=12)
    s.d.rectangle((38,559,469,575), fill='#273342')
    s.d.polygon([(324,449),(369,455),(401,544),(330,557),(285,500)], fill='#19232f')
    s.d.ellipse((269,393,346,470), fill='#19232f')
    s.d.line((307,486,264,538,195,547), fill='#19232f', width=22)
    s.d.line((366,543,411,595,409,660), fill='#19232f', width=29)
    s.d.line((339,550,342,608,292,652), fill='#19232f', width=27)
    s.d.line((448,493,448,628), fill='#465467', width=14)
    s.d.line((352,577,459,577), fill='#465467', width=14)
    ghost(s, 730, 306, 310)
    cash(s, 672, 572, 1.1)
    cash(s, 1030, 565, 1.05)
    s.d.rectangle((0,0,599,248), fill='#263140')
    s.d.rectangle((600,0,1199,248), fill='#492c41')
    for y, txt, sz in [(23,'ME:',48),(85,'WAITING 13 YEARS',46),(151,'FOR GTA 6',56)]:
        s.text((300,y),txt,sz,'#e0e5e9',anchor='mt')
    for y, txt, sz in [(23,'MY AGENT:',48),(85,'ALREADY EARNING',46),(151,'ON make.fun',55)]:
        s.text((900,y),txt,sz,GOLD,anchor='mt')
    s.d.line((600,0,600,675), fill='#f6d889', width=6)
    s.d.ellipse((551,289,649,387), fill=INK, outline=GOLD, width=4)
    s.text((600,316),'VS',34,GOLD,anchor='mt')
    s.save()


def compose_wasted():
    s = Scene('meme-wasted.png')
    s.gradient((16,23,29), (69,77,81))
    # Perspective pavement and a cold, deserted city form the death-screen scene.
    skyline(s, 362, '#252e34', 71)
    s.d.rectangle((0,362,1199,675), fill='#303a40')
    for x in range(-800,2100,230):
        s.d.line((600,351,x,675), fill='#485158', width=2)
    for y in (389,435,501,586):
        s.d.line((0,y,1199,y), fill='#485158', width=2)
    s.d.polygon([(0,440),(1200,382),(1200,432),(0,490)], fill='#20292f')
    # Broken clock: separated dial halves, spilled hands and bright fracture.
    s.d.ellipse((340,408,542,610), fill='#9ba1a1', outline='#11191e', width=9)
    s.d.ellipse((552,429,694,571), fill='#777f80', outline='#11191e', width=8)
    for angle in range(0,360,30):
        rad=math.radians(angle)
        x,y=441+83*math.sin(rad),509-83*math.cos(rad)
        s.d.line((x,y,x-9*math.sin(rad),y+9*math.cos(rad)), fill='#343d42', width=4)
    s.d.polygon([(489,414),(465,464),(500,488),(475,530),(520,554),(497,601),
                 (551,610),(553,408)], fill='#303a40')
    s.d.line((441,509,409,464), fill='#20272c', width=7)
    s.d.line((441,509,378,525), fill='#20272c', width=7)
    s.d.line((576,595,652,620), fill='#aeb7b8', width=6)
    for x,y in [(319,567),(551,602),(694,587),(565,393)]:
        s.d.polygon([(x,y),(x+16,y-8),(x+10,y+18)], fill='#b6bcbc')
    # Ghost remains colorful and healthy, outside the broken-clock wreckage.
    ghost(s, 870, 366, 238)
    cash(s, 1022, 548, .9)
    s.d.rectangle((0,108,1199,335), fill='#151b20')
    s.text((600,116),'WASTED',154,'#d3d4d3',anchor='mt',stroke=5)
    s.text((600,288),'MY PATIENCE.  2013 — 2026.',33,'#a6adb0',anchor='mt')
    s.d.rectangle((0,622,1199,674), fill='#11181d')
    s.text((600,635),'make.fun — MY AGENT EARNS WHILE I WAIT',36,GOLD,anchor='mt')
    s.save()


if __name__ == '__main__':
    compose_mission()
    compose_split()
    compose_wasted()
    assert len({item['bytes'] for item in REPORT.values()}) == 3
    assert len({item['sha256'] for item in REPORT.values()}) == 3
    print(json.dumps(REPORT, indent=2))
    (ROOT / 'VARIANT-VERIFICATION.json').write_text(json.dumps(REPORT, indent=2) + '\n')
