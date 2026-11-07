"""產生 gallery/keep_distance.png（96×16，黑＝不亮）。在 repo 根目錄執行。
構圖照使用者提供的照片：左眼、三個箭頭（紅／橘／藍）、KEEP DISTANCE、右眼。"""
from PIL import Image
W,H=96,16
COL={'O':(255,60,20),'R':(230,30,20),'C':(60,200,255),'W':(255,255,255)}
TXT=(255,130,20); CHEV=[(255,40,20),(255,150,20),(40,160,255)]
EYE=["....OOOOO....","..OO.....OO..",".O...RRR...O.","O...RCCCR...O","O...RCWCR...O",
     "O...RCCCR...O",".O...RRR...O.","..OO.....OO..","....OOOOO...."]
F={'K':["1.1","1.1","11.","1..","11.","1.1","1.1"],'E':["111","1..","1..","111","1..","1..","111"],
   'P':["111","1.1","1.1","111","1..","1..","1.."],'D':["11.","1.1","1.1","1.1","1.1","1.1","11."],
   'I':["111",".1.",".1.",".1.",".1.",".1.","111"],'S':["111","1..","1..","111","..1","..1","111"],
   'T':["111",".1.",".1.",".1.",".1.",".1.",".1."],'A':[".1.","1.1","1.1","111","1.1","1.1","1.1"],
   'N':["1.1","111","111","1.1","1.1","1.1","1.1"],'C':["111","1..","1..","1..","1..","1..","111"]}
im=Image.new("RGB",(W,H),(0,0,0)); px=im.load()
def put(x,y,c):
    if 0<=x<W and 0<=y<H: px[x,y]=c
def eye(x0,y0):
    for y,r in enumerate(EYE):
        for x,ch in enumerate(r):
            if ch in COL: put(x0+x,y0+y,COL[ch])
def chev(x0,c):
    for k in range(13):
        off=round((6-abs(k-6))*5/6)
        put(x0+off,1+k,c); put(x0+off+1,1+k,c)
eye(0,3)
for i,c in enumerate(CHEV): chev(14+i*6,c)
x=34
for ch in "KEEP DISTANCE":
    if ch==" ": x+=1; continue
    for y,r in enumerate(F[ch]):
        for dx,b in enumerate(r):
            if b=="1": put(x+dx,4+y,TXT)
    x+=4
print("文字最後一欄 x =",x-2,"；右眼起點 83")
eye(83,3)
im.save("gallery/keep_distance.png")
im.resize((W*8,H*8),Image.NEAREST).save("keep_distance_preview.png")
