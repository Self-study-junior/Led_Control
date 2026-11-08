import sys
def scan(path):
    b=open(path,'rb').read(); p=6
    w=b[p]|b[p+1]<<8; h=b[p+2]|b[p+3]<<8; f=b[p+4]; p+=7
    gct=(f&0x80) and 3*(1<<((f&7)+1)) or 0; p+=gct
    frames=[]; delay=None; disp=None
    while p<len(b):
        t=b[p]
        if t==0x21:
            lab=b[p+1]; p+=2
            if lab==0xF9: disp=(b[p+1]>>2)&7; delay=(b[p+2]|b[p+3]<<8)*10
            while b[p]: p+=b[p]+1
            p+=1
        elif t==0x2C:
            x=b[p+1]|b[p+2]<<8; y=b[p+3]|b[p+4]<<8; fw=b[p+5]|b[p+6]<<8; fh=b[p+7]|b[p+8]<<8; lf=b[p+9]; p+=10
            lct=(lf&0x80) and (1<<((lf&7)+1)) or 0; p+=3*lct; p+=1; sz=0
            while b[p]: sz+=b[p]; p+=b[p]+1
            p+=1; frames.append((x,y,fw,fh,lct,delay,disp,sz))
        elif t==0x3B: break
        else: raise Exception(hex(t))
    full=sum(1 for f in frames if f[2]==w and f[3]==h)
    print(f"{path}: {len(b)//1024}KB 全域色表={gct//3} 格數={len(frames)} 全幅={full} 局部色表格數={sum(1 for f in frames if f[4])} 局部色表最大={max(f[4] for f in frames)} 延遲={sorted(set(f[5] for f in frames))} disposal={sorted(set(f[6] for f in frames))}")
    return frames
for a in sys.argv[1:]: scan(a)
