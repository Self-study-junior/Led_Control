"""LED 友善的 GIF 編碼器：整份共用一份全域色表、每格都是完整 96×16 畫面、無局部色表、無透明。
與網頁 index.html 的 encodeGIF 同格式（網頁產生的跑馬燈在實機播放順暢）。
PIL 預設會每格各帶局部色表並只存變動區塊，11/08 實測多色時 LED 會卡頓跳格。"""
def _lzw(ix, min_code):
    clear=1<<min_code; eoi=clear+1; size=min_code+1; nxt=eoi+1; d={}
    out=bytearray(); cur=0; nb=0
    def emit(c):
        nonlocal cur,nb
        cur|=c<<nb; nb+=size
        while nb>=8: out.append(cur&255); cur>>=8; nb-=8
    emit(clear); pre=ix[0]
    for k in ix[1:]:
        key=(pre<<12)|k
        if key in d: pre=d[key]; continue
        emit(pre)
        if nxt<4096:
            d[key]=nxt; nxt+=1
            if nxt>(1<<size) and size<12: size+=1
        else:
            emit(clear); d={}; size=min_code+1; nxt=eoi+1
        pre=k
    emit(pre); emit(eoi)
    if nb>0: out.append(cur&255)
    return bytes(out)
def save(frames, delays_ms, path):
    """frames：同尺寸 RGB 的 PIL Image 清單；delays_ms：每格毫秒（int 或清單）。"""
    W,H=frames[0].size
    if isinstance(delays_ms,int): delays_ms=[delays_ms]*len(frames)
    pal={}; idx=[]
    for f in frames:
        px=list(f.convert("RGB").getdata()); row=[]
        for c in px:
            if c not in pal:
                if len(pal)>=256: raise ValueError("顏色超過 256 種")
                pal[c]=len(pal)
            row.append(pal[c])
        idx.append(row)
    bits=1
    while (1<<bits)<max(len(pal),2): bits+=1
    o=bytearray(b"GIF89a")+bytes([W&255,W>>8,H&255,H>>8,0xF0|(bits-1),0,0])
    cols=list(pal)+[(0,0,0)]*((1<<bits)-len(pal))
    for c in cols: o+=bytes(c)
    o+=bytes([0x21,0xFF,11])+b"NETSCAPE2.0"+bytes([3,1,0,0,0])
    mc=max(2,bits)
    for row,dl in zip(idx,delays_ms):
        d=round(dl/10)
        o+=bytes([0x21,0xF9,4,0x04,d&255,d>>8,0,0, 0x2C,0,0,0,0,W&255,W>>8,H&255,H>>8,0, mc])
        data=_lzw(row,mc)
        for p in range(0,len(data),255): s=data[p:p+255]; o+=bytes([len(s)])+s
        o+=b"\x00"
    o+=b"\x3B"; open(path,"wb").write(o)
    return len(pal)
