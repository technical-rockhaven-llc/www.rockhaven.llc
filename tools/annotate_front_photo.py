import sys, math
from PIL import Image, ImageDraw, ImageFont
src, dst = sys.argv[1], sys.argv[2]
NAVY=(48,65,79); TAN=(212,163,115); WHITE=(255,255,255)
base = Image.open(src).convert("RGB"); W,H = base.size
SS = 3  # supersample overlay for smooth curves
ov = Image.new("RGBA", (W*SS, H*SS), (0,0,0,0)); d = ImageDraw.Draw(ov)
def s(*v): return [round(x*SS) for x in v]

# ring around mat + first steps
cx, cy, rx, ry = 182, 806, 58, 40
for w, col in [(9, NAVY), (5, WHITE)]:
    d.ellipse(s(cx-rx, cy-ry, cx+rx, cy+ry), outline=col, width=w*SS)

# callout box on the lawn, lower middle
fb = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30*SS)
fr = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22*SS)
l1, l2 = "Unit 2B entrance", "Stairs on the left side of the building"
w1 = d.textlength(l1, font=fb)/SS; w2 = d.textlength(l2, font=fr)/SS
bw = max(w1, w2) + 40; bh = 90
bx, by = 95, 612
d.rounded_rectangle(s(bx, by, bx+bw, by+bh), radius=14*SS, fill=NAVY+(235,), outline=TAN+(255,), width=3*SS)
d.text(s(bx+20, by+12), l1, font=fb, fill=WHITE)
d.text(s(bx+20, by+54), l2, font=fr, fill=(240,228,214))

# arrow from box toward ring
x0, y0 = bx+60, by+bh     # start at bottom edge of box
ang = math.atan2(cy+ry*0.55 - y0, cx+rx*0.75 - x0)
x1 = cx + rx*0.95*math.cos(ang+math.pi)*-1; 
x1, y1 = cx + (rx+6)*math.cos(ang+math.pi), cy + (ry+6)*math.sin(ang+math.pi)
for w, col in [(10, NAVY), (5, WHITE)]:
    d.line(s(x0, y0, x1, y1), fill=col, width=w*SS)
    L = 22 if w==10 else 17; spread = 0.5
    tip = (x1, y1)
    p1 = (x1 - L*math.cos(ang-spread)*-1, y1 - L*math.sin(ang-spread)*-1)
    p2 = (x1 - L*math.cos(ang+spread)*-1, y1 - L*math.sin(ang+spread)*-1)
    d.polygon(s(*tip, *p1, *p2), fill=col)

ov = ov.resize((W,H), Image.LANCZOS)
out = base.convert("RGBA"); out.alpha_composite(ov)
out.convert("RGB").save(dst, "JPEG", quality=90, optimize=True, progressive=True)
