import sys
from PIL import Image, ImageDraw, ImageChops, ImageFont
src, dst = sys.argv[1], sys.argv[2]
B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"; R = "/System/Library/Fonts/Supplemental/Arial.ttf"
NAVY=(48,65,79); GREEN=(115,145,115); INK=(35,35,35)
orig = Image.open(src).convert("RGB"); plan = orig.copy(); W, H = plan.size
d = ImageDraw.Draw(plan)

# font size matching the plan's own room labels ("Kitchen Unit #2B" is 273px wide)
size = 10
while ImageDraw.Draw(Image.new("L",(1,1))).textlength("Kitchen Unit #2B", font=ImageFont.truetype(B,size+1)) <= 273: size += 1
lab = ImageFont.truetype(B, size)

# 1. Family Room -> Living Room
d.rectangle([818,880,1192,924], fill=(255,255,255))
d.text(((823+1186)/2, 902), "Living Room Unit #2B", font=lab, fill=INK, anchor="mm")
# 2. bathroom: clear the garbled overlapping label, restore walls, redraw dimension, relabel
d.rectangle([786,1536,1113,1580], fill=(255,255,255))
for x0,x1 in [(770,786),(1114,1140)]: plan.paste(orig.crop((x0,1536,x1,1581)),(x0,1536))
d.text((815,1538), "2′10″", font=ImageFont.truetype(B,30), fill=GREEN)
d.multiline_text((1012,1478), "Bathroom\nUnit #2B", font=lab, fill=INK, anchor="mm", align="center", spacing=6)

# 3. shading
not2b = [[(157,157),(1772,157),(1772,292),(1838,405),(1846,520),(1834,605),(1805,683),(157,683)],
         [(1308,697),(1768,697),(1768,1138),(1308,1138)],
         [(1310,1152),(1530,1152),(1530,1208),(1310,1208)]]
shared = [[(160,697),(770,697),(770,990),(160,990)]]
def mask_of(polys):
    m = Image.new("L", plan.size, 0); md = ImageDraw.Draw(m)
    for p in polys: md.polygon(p, fill=255)
    return m
tint = Image.new("RGB", plan.size, (255,255,255))
tint.paste((222,224,227), mask=mask_of(not2b)); tint.paste((246,234,219), mask=mask_of(shared))
out = ImageChops.multiply(plan, tint)
hatch = Image.new("L", plan.size, 0); hd = ImageDraw.Draw(hatch)
for x in range(-H, W, 34): hd.line([(x,0),(x+H,H)], fill=255, width=5)
out.paste((178,184,190), mask=ImageChops.multiply(hatch, mask_of(not2b)))

# 4. frame: title, legend, note
top, bottom = 230, 260
canvas = Image.new("RGB", (W, H+top+bottom), (255,255,255)); canvas.paste(out, (0, top))
c = ImageDraw.Draw(canvas)
def ctext(y, s, f, fill): c.text(((W-c.textlength(s, font=f))/2, y), s, font=f, fill=fill)
ctext(55, "Unit 2B Floor Plan", ImageFont.truetype(B,78), NAVY)
ctext(150, "1 bedroom / 1 full bath  ·  approx. 600 sq ft  ·  2nd floor", ImageFont.truetype(R,50), (90,100,110))
fl = ImageFont.truetype(R,44); y0 = top+H+40; x = 170
for kind, text in [("hatch","Not part of Unit 2B"), ("shared","Shared stairway & hallway")]:
    sw = Image.new("RGB",(70,70),(222,224,227) if kind=="hatch" else (246,234,219))
    if kind=="hatch":
        sd = ImageDraw.Draw(sw)
        for k in range(-70,70,17): sd.line([(k,0),(k+70,70)], fill=(178,184,190), width=4)
    canvas.paste(sw,(x,y0)); c.rectangle([x,y0,x+69,y0+69], outline=(110,110,110), width=3)
    c.text((x+95,y0+10), text, font=fl, fill=(40,40,40)); x += 95+int(c.textlength(text,font=fl))+110
ctext(y0+120, "Measurements are approximate. Floor plan for illustration only.", ImageFont.truetype(R,38), (110,110,110))
canvas.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dst, optimize=True)
print("label font size", size, canvas.size)
