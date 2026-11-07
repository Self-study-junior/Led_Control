"""產生 gallery/keep_distance_2.png（96×16，黑＝不亮）。在 repo 根目錄執行。
構圖照使用者第二張照片：左眼、KEEP DISTANCE、紅箭頭＋兩個藍箭頭、右眼（左右對稱）。"""
from PIL import Image
W,H=96,16
COL={'O':(255,70,20),'R':(230,25,15),'C':(50,150,255),'W':(200,230,255)}
TXT=(255,140,30); RED=(240,40,20); BLUE=(30,110,255)
EYE=["RRR..........",
     "....OOOOO....",
     "..OO.....OO..",
     ".O...CCC...O.",
     "O...CWCCC...O",
     "O...CCCCC...O",
     ".O...CCC...O.",
     "..OO.....OO..",
     "....OOOOO....",
     "..RRRRRRRRR.."]
F={'K':["1.1","1.1","11.","1..","11.","1.1","1.1"],'E':["111","1..","1..","111","1..","1..","111"],
   'P':["111","1.1","1.1","111","1..","1..","1.."],'D':["11.","1.1","1.1","1.1","1.1","1.1","11."],
   'I':["111",".1.",".1.",".1.",".1.",".1.","111"],'S':["111","1..","1..","111","..1","..1","111"],
   'T':["111",".1.",".1.",".1.",".1.",".1.",".1."],'A':[".1.","1.1","1.1","111","1.1","1.1","1.1"],
   'N':["1.1","111","111","1.1","1.1","1.1","1.1"],'C':["111","1..","1..","1..","1..","1..","111"]}
im=Image.new("RGB",(W,H),(0,0,0)); px=im.load()
def put(x,y,c):
    if 0<=x<W and 0<=y<H: px[x,y]=c
def eye(x0,y0,mirror=False):
    w=len(EYE[0])
    for y,r in enumerate(EYE):
        for x,ch in enumerate(r):
            if ch in COL: put(x0+(w-1-x if mirror else x),y0+y,COL[ch])
def chev(x0,c,thick):
    # 7 高的 >，從 y=4 到 y=10
    for k in range(7):
        off=3-abs(k-3)
        for t in range(thick): put(x0+off+t,4+k,c)
eye(0,3)
x=15
for ch in "KEEP DISTANCE":
    if ch==" ": x+=1; continue
    for y,r in enumerate(F[ch]):
        for dx,b in enumerate(r):
            if b=="1": put(x+dx,4+y,TXT)
    x+=4
end=x-2
chev(end+3,RED,1); chev(end+8,BLUE,2); chev(end+13,BLUE,2)
print("文字最後一欄",end,"；箭頭最後一欄",end+13+4,"；右眼起點 83")
eye(83,3,mirror=True)
im.save("gallery/keep_distance_2.png")
im.resize((W*8,H*8),Image.NEAREST).save("/tmp/claude-0/-home-claude/1ce103b4-e8e8-50c7-8c01-53f67f74ab9f/scratchpad/kd2_preview.png")
