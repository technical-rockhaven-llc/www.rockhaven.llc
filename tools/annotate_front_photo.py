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

# --- Unit 2B stairs, seen straight on --------------------------------------
# One straight concrete flight running back from the doormat to a landing at the
# Unit 2B door, so from the street it reads as a stack of steps (like the front steps).
N_STEPS = 11
BOTTOM_Y, TOP_Y = 806, 659                   # bottom of first riser, top of last tread
BOTTOM_X = (148, 210)                        # stair width at the doormat
TOP_X = (156, 206)                           # slightly narrower farther back
RISER, TREAD = (176, 179, 178, 255), (230, 230, 226, 255)

def lerp(a, b, t): return a + (b - a) * t
step_h = (BOTTOM_Y - TOP_Y) / N_STEPS
steps = []
for i in range(N_STEPS):
    t = i / (N_STEPS - 1)
    xl, xr = lerp(BOTTOM_X[0], TOP_X[0], t), lerp(BOTTOM_X[1], TOP_X[1], t)
    yb = BOTTOM_Y - i * step_h; yt = yb - step_h
    steps.append((xl, xr, yt, yb))

# navy edge around the whole flight, then each step: lighter tread on top of a riser
outline = [(steps[0][0], steps[0][3]), (steps[0][1], steps[0][3]),
           (steps[-1][1], steps[-1][2]), (steps[-1][0], steps[-1][2])]
d.polygon(s(outline), outline=NAVY+(255,), width=7*SS)
for xl, xr, yt, yb in steps:
    tread_b = yt + step_h * 0.38
    d.rectangle(s([(xl, tread_b), (xr, yb)]), fill=RISER)
    d.rectangle(s([(xl, yt), (xr, tread_b)]), fill=TREAD)
    d.line(s([(xl, yt), (xr, yt)]), fill=WHITE+(255,), width=2*SS)
d.polygon(s(outline), outline=WHITE+(255,), width=3*SS)

# landing slab at the top, level and straight on
slab = [(138, 643), (226, 643), (226, 659), (138, 659)]
d.polygon(s(slab), outline=NAVY+(255,), width=7*SS)
d.polygon(s(slab), fill=(226,226,222,255), outline=WHITE+(255,), width=3*SS)

# railing along the outer part of the top landing
for w, c in [(6, NAVY), (2.5, WHITE)]:
    d.line(s([(138, 621), (186, 621)]), fill=c+(255,), width=round(w*SS))
    for x in range(140, 188, 9):
        d.line(s([(x, 621), (x, 643)]), fill=c+(255,), width=round(w*SS*0.8))
# door on the side wall, under the awning
door = [(210,578),(224,578),(224,643),(210,643)]
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
