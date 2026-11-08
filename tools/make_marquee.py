from PIL import Image, ImageDraw, ImageFont
W,H=96,16
BLACK=(0,0,0); WHITE=(255,255,255); YEL=(230,230,60); RED=(230,30,30)
UF=ImageFont.truetype("/usr/share/fonts/opentype/unifont/unifont.otf",16)
def seg(s,c):
    w=int(UF.getlength(s)); m=Image.new("1",(w,16),0); d=ImageDraw.Draw(m); d.fontmode="1"
    d.text((0,0),s,font=UF,fill=1); im=Image.new("RGB",(w,16),BLACK); im.paste(Image.new("RGB",(w,16),c),(0,0),m); return im
def disc():
    # 紅色實心圓＋白色 1（16×16）
    im=Image.new("RGB",(16,16),BLACK); d=ImageDraw.Draw(im)
    d.ellipse([0,0,15,15],fill=RED)
    one=["0110","1110","0110","0110","0110","0110","0110","1111"]
    for y,r in enumerate(one):
        for x,b in enumerate(r):
            if b=="1": im.putpixel((6+x,4+y),WHITE)
    return im
def stamp():
    # 圓戳章：紅色圓環＋「卜」
    im=Image.new("RGB",(16,16),BLACK); d=ImageDraw.Draw(im)
    d.ellipse([0,0,15,15],outline=RED,width=2)
    for y in range(4,12): im.putpixel((7,y),RED)   # 直筆
    im.putpixel((8,7),RED); im.putpixel((9,8),RED); im.putpixel((10,8),RED)  # 右點
    return im
parts=[disc(),seg(" 桃園 黃世杰 ",WHITE),stamp(),seg(" 團杰 ",YEL),disc(),seg(" 2026.11.28 ",WHITE)]
tw=sum(p.width for p in parts)
strip=Image.new("RGB",(tw,H),BLACK); x=0
for p in parts: strip.paste(p,(x,0)); x+=p.width
full=Image.new("RGB",(tw+W,H),BLACK); full.paste(strip,(W,0))
frames=[full.crop((o,0,o+W,H)) for o in range(0,tw,2)]
import sys; sys.path.insert(0,"tools"); import gifenc
gifenc.save(frames,90,"gallery/marquee_taoyuan.gif")   # 全域色表、完整畫面（見 SKILL.md 製圖規範）
strip.resize((tw*8,H*8),Image.NEAREST).save("strip_preview.png")
print(tw,len(frames))
