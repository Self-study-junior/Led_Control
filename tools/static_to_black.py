"""把圖庫靜態圖的紅色底 (220,90,80) 換成黑色（黑＝不亮），其他顏色不動。
在 repo 根目錄執行：python3 tools/static_to_black.py
找不到紅底就報錯（避免對已轉過或別的圖安靜地什麼都沒做）。"""
import sys
from PIL import Image

BG = (220, 90, 80)
FILES = ["gallery/static_name_A.png", "gallery/static_taoyuan_B.png"]

for f in FILES:
    im = Image.open(f).convert("RGB")
    if im.size != (96, 16):
        sys.exit(f"{f} 不是 96×16：{im.size}")
    px = im.load()
    n = 0
    for y in range(16):
        for x in range(96):
            if px[x, y] == BG:
                px[x, y] = (0, 0, 0)
                n += 1
    if n == 0:
        sys.exit(f"{f} 找不到紅底 {BG}，未修改")
    im.save(f)
    print(f, "換掉", n, "px")
