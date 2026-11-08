"""產生兩張幹話跑馬燈（96×16，黑＝不亮）。在 repo 根目錄執行；製圖規範見 SKILL.md。
- gallery/joke_distance.gif：😅 別貼這麼近，我們還不熟 😅（汗滴閃爍）
- gallery/joke_newbie.gif  ：🔰 新手駕駛，我也很怕我自己 😱（驚嚇臉左右抖）
每格移 2px、90 ms；兩種狀態每 6 格（約 0.54 秒）切換；用 tools/gifenc.py 存。"""
from PIL import Image, ImageDraw, ImageFont
import sys; sys.path.insert(0,"tools"); import gifenc
W,H=96,16; STEP=2; DELAY=90; SWAP=6
UF=ImageFont.truetype("/usr/share/fonts/opentype/unifont/unifont.otf",16)
C={'Y':(255,210,0),'B':(40,140,255),'G':(0,200,80),'W':(255,255,255)}
FACE_AWK=["....YYYYY....","..YYYYYYYYY..",".YYYYYYYYYYY.",".YY..YYY..YY.","YYY..YYY..YYY","YYYYYYYYYYYYY",
          "YYYYYYYYYYYYY","YYY.......YYY","YYYY.....YYYY",".YYYYYYYYYYY.",".YYYYYYYYYYY.","..YYYYYYYYY..","....YYYYY...."]
DROP=["..B",".BB","BBB","BBB",".B."]
FACE_SCARED=["....YYYYY....","..YYYYYYYYY..",".YYYYYYYYYYY.",".YY..YYY..YY.",".YY..YYY..YY.","YYYYYYYYYYYYY",
             "YYYYY...YYYYY","YYYY.....YYYY","YYYY.....YYYY",".YYYY...YYYY.",".YYYYYYYYYYY.","..YYYYYYYYY..","....YYYYY...."]
LEAF=["YY....GG","YYY..GGG","YYYYGGGG","YYYYGGGG","YYYYGGGG","YYYYGGGG","YYYYGGGG",".YYYGGG.","..YYGG..","...YG..."]
def art(rows,w=None,dx=0,dy=None,extra=None):
    w=w or len(rows[0]); dy=(H-len(rows))//2 if dy is None else dy
    im=Image.new("RGB",(w,H),(0,0,0))
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            if ch in C and 0<=x+dx<w: im.putpixel((x+dx,dy+y),C[ch])
    if extra:
        rows2,ox,oy=extra
        for y,r in enumerate(rows2):
            for x,ch in enumerate(r):
                if ch in C: im.putpixel((ox+x,oy+y),C[ch])
    return im
def text(s,c):
    w=int(UF.getlength(s)); m=Image.new("1",(w,H),0); d=ImageDraw.Draw(m); d.fontmode="1"
    d.text((0,0),s,font=UF,fill=1); im=Image.new("RGB",(w,H),(0,0,0)); im.paste(Image.new("RGB",(w,H),c),(0,0),m); return im
gap=lambda n: Image.new("RGB",(n,H),(0,0,0))
def join(parts):
    w=sum(p.width for p in parts); s=Image.new("RGB",(w,H),(0,0,0)); x=0
    for p in parts: s.paste(p,(x,0)); x+=p.width
    return s
def marquee(states, path, preview_dir):
    tw=states[0].width; assert all(s.width==tw for s in states)
    full=[]
    for s in states:
        f=Image.new("RGB",(tw+W,H),(0,0,0)); f.paste(s,(W,0)); full.append(f)
    frames=[full[(i//SWAP)%len(full)].crop((o,0,o+W,H)) for i,o in enumerate(range(0,tw+W,STEP))]
    n=gifenc.save(frames,DELAY,path)
    states[0].resize((tw*8,H*8),Image.NEAREST).save(f"{preview_dir}/{path.split('/')[-1]}.png")
    print(f"{path}：整條 {tw}px，{len(frames)} 格，一輪 {len(frames)*DELAY/1000:.1f} 秒，{n} 色")
out=sys.argv[1] if len(sys.argv)>1 else "."
# 1. 別貼這麼近，我們還不熟（尷尬臉，汗滴閃爍）
def awk(drop): return art(FACE_AWK,w=16,dy=2,extra=(DROP,13,0) if drop else None)
s1=[join([awk(d),gap(4),text("別貼這麼近，",C['Y']),text("我們還不熟",C['W']),gap(4),awk(d)]) for d in (True,False)]
marquee(s1,"gallery/joke_distance.gif",out)
# 3. 新手駕駛，我也很怕我自己（新手葉，驚嚇臉左右抖）
def scared(dx): return art(FACE_SCARED,w=15,dx=1+dx)
s3=[join([art(LEAF,w=8),gap(4),text("新手駕駛，",C['G']),text("我也很怕我自己",C['W']),gap(4),scared(dx)]) for dx in (-1,1)]
marquee(s3,"gallery/joke_newbie.gif",out)
