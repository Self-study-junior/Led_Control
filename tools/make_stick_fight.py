"""產生 gallery/stick_fight.gif：兩個火柴人打架（96×16，黑＝不亮，約 10 秒）。在 repo 根目錄執行。
藍＝左邊、紅＝右邊；骨架用關節座標畫線，命中時出現黃色火花。每格 100 ms，用 tools/gifenc.py 存。
劇本：對峙彈跳 → 靠近 → 藍出拳命中 → 紅踢腿命中 → 互毆 → 藍飛踢 → 紅倒地冒星星、藍勝利跳 → 紅爬起、回到對峙（可循環）"""
from PIL import Image
import sys; sys.path.insert(0,"tools"); import gifenc
W,H=96,16; DELAY=100
BLUE=(40,140,255); RED=(255,50,30); YEL=(255,210,0); WHITE=(255,255,255)
HEAD=[".XX.","X..X","X..X",".XX."]          # 4×4，左上角＝(頭中心x-1, 頭頂y)
# 姿勢（面向右的局部座標；x＝0 在髖部正上方，y＝0 在畫布頂）：
# head＝頭頂中心, neck, hip, 前臂(肘,手), 後臂(肘,手), 前腳(膝,腳), 後腳(膝,腳)
P={
 "stance":dict(head=(0,0),neck=(0,4),hip=(0,9),fa=((2,6),(3,4)),ba=((-1,7),(1,6)),fl=((2,12),(3,15)),bl=((-1,12),(-2,15))),
 "bounce":dict(head=(0,1),neck=(0,5),hip=(0,10),fa=((2,7),(3,5)),ba=((-1,8),(1,7)),fl=((2,12),(3,15)),bl=((-1,12),(-2,15))),
 "walkA": dict(head=(0,0),neck=(0,4),hip=(0,9),fa=((2,6),(3,4)),ba=((-1,7),(1,6)),fl=((2,12),(4,15)),bl=((-1,12),(-3,15))),
 "walkB": dict(head=(0,0),neck=(0,4),hip=(0,9),fa=((2,6),(3,4)),ba=((-1,7),(1,6)),fl=((1,12),(1,15)),bl=((-1,12),(-1,15))),
 "punch": dict(head=(1,0),neck=(1,4),hip=(0,9),fa=((4,5),(7,5)),ba=((-1,7),(1,6)),fl=((3,12),(4,15)),bl=((-1,12),(-3,15))),
 "kick":  dict(head=(-1,0),neck=(-1,4),hip=(0,9),fa=((1,6),(3,5)),ba=((-3,6),(-5,5)),fl=((3,9),(7,8)),bl=((0,12),(-1,15))),
 "hit":   dict(head=(-2,1),neck=(-1,5),hip=(0,9),fa=((-3,5),(-4,3)),ba=((-2,7),(-5,7)),fl=((1,12),(2,15)),bl=((-1,12),(-3,15))),
 "jump":  dict(head=(0,0),neck=(0,4),hip=(0,8),fa=((2,5),(3,3)),ba=((-2,5),(-3,3)),fl=((2,10),(1,12)),bl=((-2,10),(-1,12))),
 "fkick": dict(head=(-2,1),neck=(-1,4),hip=(1,8),fa=((-2,5),(-4,4)),ba=((0,6),(-2,7)),fl=((4,8),(8,8)),bl=((0,11),(-1,13))),
 "win":   dict(head=(0,0),neck=(0,4),hip=(0,9),fa=((2,3),(3,1)),ba=((-2,3),(-3,1)),fl=((2,12),(3,15)),bl=((-2,12),(-3,15))),
 "kneel": dict(head=(1,4),neck=(1,8),hip=(0,11),fa=((3,10),(4,12)),ba=((0,10),(1,12)),fl=((3,12),(4,15)),bl=((-2,14),(-4,15))),
}
FALLEN=dict(head=(-8,12),body=((-5,13),(2,13)),limbs=[((2,13),(6,15)),((2,13),(6,12)),((-3,13),(-1,11)),((-3,13),(0,15))])
def line(px,a,b,c):
    (x0,y0),(x1,y1)=a,b; dx=abs(x1-x0); dy=-abs(y1-y0); sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1; e=dx+dy
    while True:
        put(px,x0,y0,c)
        if x0==x1 and y0==y1: break
        e2=2*e
        if e2>=dy: e+=dy; x0+=sx
        if e2<=dx: e+=dx; y0+=sy
def put(px,x,y,c):
    if 0<=x<W and 0<=y<H: px[x,y]=c
def head(px,cx,top,c):
    for y,r in enumerate(HEAD):
        for x,ch in enumerate(r):
            if ch=="X": put(px,cx-1+x,top+y,c)
def figure(px,pose,x0,face,c,dy=0):
    if pose=="fallen":
        T=lambda p:(x0+p[0]*face,p[1])
        head(px,T(FALLEN["head"])[0],FALLEN["head"][1]-1,c); line(px,T(FALLEN["body"][0]),T(FALLEN["body"][1]),c)
        for a,b in FALLEN["limbs"]: line(px,T(a),T(b),c)
        return
    p=P[pose]; T=lambda q:(x0+q[0]*face,q[1]+dy)
    hx,hy=T(p["head"]); head(px,hx,hy,c)
    line(px,T(p["neck"]),T(p["hip"]),c)
    sh=(p["neck"][0],p["neck"][1]+1)
    for e,h in (p["fa"],p["ba"]): line(px,T(sh),T(e),c); line(px,T(e),T(h),c)
    for k,f in (p["fl"],p["bl"]): line(px,T(p["hip"]),T(k),c); line(px,T(k),T(f),c)
def spark(px,x,y):
    for dx,dy in ((0,0),(-1,0),(1,0),(0,-1),(0,1),(-2,-2),(2,-2),(-2,2),(2,2)): put(px,x+dx,y+dy,YEL)
def stars(px,x,y,t):
    for k in range(3):
        put(px,x+((k*3+t)%7)-3,y+(k+t)%2,YEL)
# 劇本：(格數, 藍姿勢, 藍x起, 藍x迄, 紅姿勢, 紅x起, 紅x迄, 特效)
# 藍面向右(+1)、紅面向左(-1)；姿勢若是 list 依格輪流
S=[
 (10,["stance","stance","bounce","bounce"],28,28, ["bounce","bounce","stance","stance"],68,68, None),
 (10,["walkA","walkA","walkB","walkB"],28,40, ["walkB","walkB","walkA","walkA"],68,56, None),
 (3, "stance",40,40, "stance",56,56, None),
 (4, "punch",40,42, "stance",56,56, None),
 (5, "punch",42,42, "hit",56,59, ("spark",50,5)),
 (4, "stance",42,41, "stance",59,57, None),
 (4, "stance",41,41, "kick",57,57, None),
 (5, "hit",41,37, "kick",57,57, ("spark",48,8)),
 (4, "stance",37,40, "stance",57,55, None),
 (3, "punch",40,40, "hit",55,57, ("spark",48,5)),
 (3, "hit",40,38, "punch",57,55, ("spark",46,5)),
 (3, "punch",38,40, "hit",55,58, ("spark",48,5)),
 (3, "hit",40,38, "punch",58,56, ("spark",47,5)),
 (4, "stance",38,36, "stance",56,58, None),
 (3, "jump",36,40, "stance",58,58, None),
 (5, "fkick",40,47, "hit",58,60, ("spark",55,9)),
 (12,["win","win","stance","stance"],47,47, "fallen",66,66, ("stars",74,8)),
 (6, "stance",47,47, "kneel",62,62, None),
 (7, ["walkB","walkB","walkA","walkA"],47,28, ["walkA","walkA","walkB","walkB"],62,68, None),
]
frames=[]; t=0
for n,bp,bx0,bx1,rp,rx0,rx1,fx in S:
    for i in range(n):
        f=i/(n-1) if n>1 else 1
        bx=round(bx0+(bx1-bx0)*f); rx=round(rx0+(rx1-rx0)*f)
        bpose=bp[i%len(bp)] if isinstance(bp,list) else bp
        rpose=rp[i%len(rp)] if isinstance(rp,list) else rp
        im=Image.new("RGB",(W,H),(0,0,0)); px=im.load()
        dy=-2 if bpose in("jump","fkick") else (-1 if bpose=="win" and (t//2)%2==0 else 0)
        figure(px,bpose,bx,1,BLUE,dy); figure(px,rpose,rx,-1,RED)
        if fx and fx[0]=="spark" and i<3: spark(px,fx[1],fx[2])
        if fx and fx[0]=="stars": stars(px,fx[1],fx[2],t)
        frames.append(im); t+=1
n=gifenc.save(frames,DELAY,"gallery/stick_fight.gif")
print(f"{len(frames)} 格，{len(frames)*DELAY/1000:.1f} 秒，{n} 色")
out=sys.argv[1] if len(sys.argv)>1 else "."
sheet=Image.new("RGB",(W*4+12,(H+3)*((len(frames)+3)//4)),(60,60,60))
for k,f in enumerate(frames): sheet.paste(f,((k%4)*(W+4),(k//4)*(H+3)))
sheet.resize((sheet.width*3,sheet.height*3),Image.NEAREST).save(f"{out}/stick_sheet.png")
big=[f.resize((W*6,H*6),Image.NEAREST) for f in frames]
big[0].save(f"{out}/stick_fight_preview.gif",save_all=True,append_images=big[1:],duration=DELAY,loop=0)
