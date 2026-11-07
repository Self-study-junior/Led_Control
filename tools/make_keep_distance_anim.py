"""產生 gallery/keep_distance_anim.gif（96×16，黑＝不亮）。在 repo 根目錄執行。
兩端固定一對對稱眼睛；中間「KEEP DISTANCE」與「》〉》 《〈《」每 2 秒交換。
4 格 × 2000 ms ＝ 8 秒一輪（A B A B），循環時也維持每 2 秒交換。"""
from PIL import Image
W,H=96,16; HOLD=2000
O=(255,70,20); C=(50,150,255); WH=(210,235,255); TXT=(255,140,30)
CH_OUT=(40,120,255); CH_IN=(255,40,20)
EYE=["....OOOOO....","..OO.....OO..",".O...CCC...O.","O...CWCCC...O",
     "O...CCCCC...O",".O...CCC...O.","..OO.....OO..","....OOOOO...."]
F={'K':["1..1","1..1","1.1.","11..","1.1.","1..1","1..1"],'E':["1111","1...","1...","111.","1...","1...","1111"],
   'P':["111.","1..1","1..1","111.","1...","1...","1..."],'D':["111.","1..1","1..1","1..1","1..1","1..1","111."],
   'I':["111",".1.",".1.",".1.",".1.",".1.","111"],'S':[".111","1...","1...",".11.","...1","...1","111."],
   'T':["111",".1.",".1.",".1.",".1.",".1.",".1."],'A':[".11.","1..1","1..1","1111","1..1","1..1","1..1"],
   'N':["1..1","11.1","11.1","1.11","1.11","1..1","1..1"],'C':[".111","1...","1...","1...","1...","1...",".111"]}
def base():
    im=Image.new("RGB",(W,H),(0,0,0)); px=im.load()
    for y,r in enumerate(EYE):
        for x,ch in enumerate(r):
            c={'O':O,'C':C,'W':WH}.get(ch)
            if c: px[x,4+y]=c; px[W-1-x,4+y]=c       # 右眼＝左眼鏡像
    return im,px
def text():
    im,px=base(); word="KEEP DISTANCE"
    w=sum(3 if ch==" " else len(F[ch][0])+1 for ch in word)-1
    x=(W-w)//2
    for ch in word:
        if ch==" ": x+=3; continue
        for y,r in enumerate(F[ch]):
            for dx,b in enumerate(r):
                if b=="1": px[x+dx,4+y]=TXT
        x+=len(F[ch][0])+1
    return im
def arrows():
    im,px=base()
    def chev(x0,c,flip):
        for k in range(11):                       # 11 高，y=2..12
            off=5-abs(k-5)
            for t in (0,1):
                x=x0+off+t if not flip else x0+(6-off-t)
                px[x,2+k]=c
    # 左：》〉》（朝右）；右：《〈《（朝左），左右鏡像
    L=[(14,CH_OUT),(17,CH_OUT),(26,CH_IN),(35,CH_OUT),(38,CH_OUT)]
    for x0,c in L:
        chev(x0,c,False); chev(W-7-x0,c,True)
    return im
A,B=text(),arrows()
frames=[A,B,A,B]
pal=[f.convert("P",palette=Image.ADAPTIVE,colors=8) for f in frames]
pal[0].save("gallery/keep_distance_anim.gif",save_all=True,append_images=pal[1:],duration=HOLD,loop=0,optimize=False,disposal=1)
import sys
out=sys.argv[1] if len(sys.argv)>1 else "."
for n,f in (("A",A),("B",B)): f.resize((W*8,H*8),Image.NEAREST).save(f"{out}/kda_{n}.png")
