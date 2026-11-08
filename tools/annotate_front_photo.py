"""Annotate the building photo with the Unit 2B entrance and side stairs.
Usage: python3 annotate_front_photo.py source_photos/building-front.jpg "gallery/Unit 2B/00-building-front.jpg"
The stair path is an illustration: the real stairs are hidden behind the tree.
"""
import sys
from PIL import Image, ImageDraw, ImageFont
src, dst = sys.argv[1], sys.argv[2]
NAVY=(48,65,79); TAN=(212,163,115); WHITE=(255,255,255)
base = Image.open(src).convert("RGB"); W,H = base.size
SS = 3
ov = Image.new("RGBA", (W*SS, H*SS), (0,0,0,0)); d = ImageDraw.Draw(ov)
def s(pts): return [(round(x*SS), round(y*SS)) for x,y in pts]

def flight(x0, y0, x1, y1, n, thick=15):
    """Solid stair flight rising left->right from (x0,y0) to (x1,y1): step profile on top, slab underneath."""
    run, rise = (x1-x0)/n, (y0-y1)/n
    top = [(x0, y0)]
    for i in range(n):
        x, y = top[-1]
        top += [(x, y-rise), (x+run, y-rise)]
    slope = (x1-x0)/(y0-y1)
    return top + [(x1, y1+thick), (x0+thick*slope*0.3, y0+thick*0.2)]

def slab(xa, xb, y, thick=13):
    return [(xa, y), (xb, y), (xb, y+thick), (xa, y+thick)]

shapes = [
    flight(160, 800, 210, 730, 5),     # lower flight from the doormat
    slab(148, 214, 730),               # mid landing
    flight(150, 730, 200, 655, 6),     # upper flight (switchback, like the neighbor's)
    slab(138, 226, 655, 16),           # top landing: concrete slab at the Unit 2B door
]
# round concrete column under the top landing's outer corner (drawn first, behind the stairs)
cx0, cx1, ctop, cbot = 139, 151, 671, 806
d.rounded_rectangle(s([(cx0-3, ctop), (cx1+3, cbot)]), radius=8*SS, fill=NAVY+(255,))
d.rounded_rectangle(s([(cx0, ctop), (cx1, cbot)]), radius=6*SS, fill=(205,207,204,255), outline=WHITE+(255,), width=2*SS)

# solid concrete look: sweep each shape back toward the wall to give it width,
# then draw the front face light with the white outline over a navy edge
DEPTH, DX, DY = 12, -1.0, -0.45          # extrusion direction (back and up)
def shifted(poly, k): return [(x+DX*k, y+DY*k) for x, y in poly]
for poly in shapes:
    d.polygon(s(shifted(poly, DEPTH)), outline=NAVY+(255,), width=7*SS)
    d.polygon(s(poly), outline=NAVY+(255,), width=7*SS)
for poly in shapes:
    for k in range(DEPTH, 0, -1):
        d.polygon(s(shifted(poly, k)), fill=(150,156,160,255))
    d.polygon(s(shifted(poly, DEPTH)), outline=WHITE+(255,), width=2*SS)
    d.polygon(s(poly), fill=(226,226,222,255), outline=WHITE+(255,), width=3*SS)
# railing along the outer part of the top landing
for w, c in [(6, NAVY), (2.5, WHITE)]:
    d.line(s([(138, 633), (186, 633)]), fill=c+(255,), width=round(w*SS))
    for x in range(140, 188, 9):
        d.line(s([(x, 633), (x, 655)]), fill=c+(255,), width=round(w*SS*0.8))
# door on the side wall, under the awning
door = [(210,582),(224,582),(224,655),(210,655)]
d.polygon(s(door), outline=NAVY+(255,), width=6*SS)
d.polygon(s(door), fill=(255,255,255,120), outline=WHITE+(255,), width=3*SS)
# green awning over the landing (visible through the tree at ~200-220, 560-577)
awning = [(226,548),(214,550),(198,556),(184,566),(176,580),(226,580)]
d.polygon(s(awning), outline=NAVY+(255,), width=6*SS)
d.polygon(s(awning), fill=(14,140,130,215), outline=WHITE+(255,), width=3*SS)

# callout box over the tree, between the stairs and the front door
fb = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30*SS)
fr = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22*SS)
lines = [("Unit 2B entrance", fb, WHITE), ("Stairs on the left side", fr, (240,228,214)), ("of the building", fr, (240,228,214))]
bw = max(d.textlength(t, font=f) for t,f,_ in lines)/SS + 40; bh = 122
bx, by = 250, 625
d.rounded_rectangle(s([(bx,by),(bx+bw,by+bh)]), radius=14*SS, fill=NAVY+(235,), outline=TAN+(255,), width=3*SS)
y = by+12
for (t,f,c),dy in zip(lines,(42,30,30)):
    d.text((round((bx+20)*SS), round(y*SS)), t, font=f, fill=c); y += dy

# short arrow from the box to the upper flight
import math
x0, y0, x1, y1 = bx, by+52, 232, 620
ang = math.atan2(y1-y0, x1-x0)
for w, col in [(10, NAVY), (5, WHITE)]:
    d.line(s([(x0,y0),(x1,y1)]), fill=col, width=w*SS)
    L = 22 if w==10 else 17
    p1 = (x1 - L*math.cos(ang-0.5), y1 - L*math.sin(ang-0.5))
    p2 = (x1 - L*math.cos(ang+0.5), y1 - L*math.sin(ang+0.5))
    d.polygon(s([(x1,y1),p1,p2]), fill=col)

ov = ov.resize((W,H), Image.LANCZOS)
out = base.convert("RGBA"); out.alpha_composite(ov)
out.convert("RGB").save(dst, "JPEG", quality=90, optimize=True, progressive=True)
