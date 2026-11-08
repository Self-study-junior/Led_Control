"""產生 gallery/slow_car.gif（96×16，黑＝不亮）。在 repo 根目錄執行。
跑馬燈：⚠ 前有慢車 🚗，請勿追尾閃燈 ⚠ ；兩個警示三角形約每 0.5 秒閃一次。
每格移 2px、90 ms（同圖庫其他跑馬燈），前面補 96px 黑。"""
from PIL import Image, ImageDraw, ImageFont
import sys
W,H=96,16; STEP=2; DELAY=90; BLINK=6   # 6 格≈0.54 秒切換一次
UF=ImageFont.truetype("/usr/share/fonts/opentype/unifont/unifont.otf",16)
YEL=(255,210,0); RED=(255,50,30); WHITE=(255,255,255)
CAR={'B':(40,140,255),'C':(160,225,255),'R':(255,30,20),'K':(130,130,130),'W':(255,255,255),'Y':(255,210,0)}
CAR_ART=["....BBBBBBBB.......",
         "...BCCCBBCCCB......",
         "..BCCCCBBCCCCB.....",
         "YBBBBBBBBBBBBBBBBR.",
         "BBBBBBBBBBBBBBBBBRR",
         "BBBBBBBBBBBBBBBBBBR",
         "..KKK........KKK...",
         ".KKWKK......KKWKK..",
         "..KKK........KKK..."]
def text(s,c):
    w=int(UF.getlength(s)); m=Image.new("1",(w,H),0); d=ImageDraw.Draw(m); d.fontmode="1"
    d.text((0,0),s,font=UF,fill=1); im=Image.new("RGB",(w,H),(0,0,0)); im.paste(Image.new("RGB",(w,H),c),(0,0),m); return im
def triangle(on):
    im=Image.new("RGB",(16,H),(0,0,0))
    if on:
        d=ImageDraw.Draw(im); d.polygon([(7,1),(14,14),(0,14)],outline=YEL); d.polygon([(7,2),(13,14),(1,14)],outline=YEL)
        for y in range(5,11): im.putpixel((7,y),RED)
        im.putpixel((7,12),RED)
    return im
def car():
    im=Image.new("RGB",(len(CAR_ART[0]),H),(0,0,0))
    for y,r in enumerate(CAR_ART):
        for x,ch in enumerate(r):
            if ch in CAR: im.putpixel((x,4+y),CAR[ch])
    return im
def gap(n): return Image.new("RGB",(n,H),(0,0,0))
def strip(on):
    parts=[triangle(on),gap(4),text("前有慢車",YEL),gap(4),car(),gap(2),text("，請勿追尾閃燈",RED),gap(4),triangle(on)]
    w=sum(p.width for p in parts); s=Image.new("RGB",(w,H),(0,0,0)); x=0
    for p in parts: s.paste(p,(x,0)); x+=p.width
    return s
S=[strip(False),strip(True)]; tw=S[0].width
full=[Image.new("RGB",(tw+W,H),(0,0,0)) for _ in S]
for f,s in zip(full,S): f.paste(s,(W,0))
frames=[]
for i,o in enumerate(range(0,tw+W,STEP)):
    on=(i//BLINK)%2==0
    frames.append(full[1 if on else 0].crop((o,0,o+W,H)))
pal=[f.convert("P",palette=Image.ADAPTIVE,colors=16) for f in frames]
pal[0].save("gallery/slow_car.gif",save_all=True,append_images=pal[1:],duration=DELAY,loop=0,optimize=False,disposal=1)
print(f"整條 {tw}px，{len(frames)} 格，一輪約 {len(frames)*DELAY/1000:.1f} 秒")
out=sys.argv[1] if len(sys.argv)>1 else "."
S[1].resize((tw*8,H*8),Image.NEAREST).save(f"{out}/slow_car_strip.png")
