# Led_Control 交接文件

最後更新：2026-11-08 00:15（台北）　上一手：A 帳號 Claude（2026-11-04 對話）

## 一句話現況

iPixel Color 96×16 LED 的繁中 Web Bluetooth 控制台**已實機可用**：iPhone 用 Bluefy 開
https://self-study-junior.github.io/Led_Control/ 。連線、開關、亮度、繁體跑馬燈、圖庫送出、存成節目都實測成功。
11/04 晚上加了「虛擬遙控器 20 鍵」與「送出方式（持續／插播一次／存節目）」，**使用者還沒實測**。

## 接手必做

1. `add_repo` 要用 `access: push`；Claude 帳號的 GitHub 連線必須是 **Self-study-junior** 帳號，否則會報 `you need push access`
2. **repo 已改名為 `Led_Control`（大小寫）**。clone 後執行
   `git remote set-url origin https://github.com/Self-study-junior/Led_Control.git`，
   否則 push 會回 `This repository moved` / `Internal Server Error`。GitHub 偶爾也會單純回 500，等 10～20 秒重推一次即可
3. 讀 `.claude/skills/led-control/SKILL.md`（協定、坑、工作流程）
4. **不要碰 `Self-study-junior/Junior`**

## 檔案

| 路徑 | 用途 |
|---|---|
| `index.html` | 整個控制台（單檔：協定、GIF 編碼器、UI） |
| `gallery/gallery.json` | 圖庫清單 `[{file,name}]` |
| `gallery/*.gif / *.png` | 圖庫內容，**一律 96×16** |
| `tools/make_marquee.py` | 產生 `gallery/marquee_taoyuan.gif`（repo 根目錄執行；需 Pillow＋Unifont；每格 90 ms） |
| `tools/make_keep_distance.py` | 產生 `gallery/keep_distance.png`（照使用者照片構圖重畫；文字 3×7 點陣） |
| `tools/make_keep_distance_2.py` | 產生 `gallery/keep_distance_2.png`（使用者第二張照片構圖） |
| `tools/make_keep_distance_anim.py` | 產生 `gallery/keep_distance_anim.gif`（4 格×2000 ms＝8 秒；A 字／B 》〉》《〈《 交替，雙眼固定） |
| `tools/static_to_black.py` | 靜態圖紅底換黑（找不到紅底會報錯退出） |
| `.claude/skills/led-control/SKILL.md` | 技能說明（含 App 反編譯結果） |
| `.nojekyll` | GitHub Pages 用 |

## 網頁功能一覽（由上到下）

1. **連線**：連線／開關／亮度／「遙控器動畫改回英文」（送語言碼 0）
2. **遙控器（虛擬按鍵）**：20 鍵，送 `06 00 07 80 k 00` ⚠️未實測
3. **繁體跑馬燈**：文字（`[#rrggbb]字[/]` 局部變色）、字色、底色、字型、模式、每格移、每格 ms；送出方式三選一
4. **圖庫**：送出方式三選一＋跑動速度 50%～200%（改 GIF 每格延遲，不動像素）
5. **節目表**：網頁自己記錄已存節目（localStorage `ledPrograms.v1`，只在該手機 Bluefy）；補登、匯出／匯入 JSON、每列「顯示」「刪除」⚠️刪除未實測；「顯示第 n 格」⚠️未實測
6. **送自己的圖片／GIF**：只有持續顯示（slot 0）
7. **紀錄**：所有成功／失敗都寫在這裡；保存最近 500 行（localStorage `ledLog.v1`，只在該手機），重新整理後還在；「複製紀錄」（含日期時間，給 Claude 看用）、「清除紀錄」。Chromium 實測 ✔，Bluefy 剪貼簿未實測（失敗會提示改手動選取）

送出方式：
- **持續顯示**＝slot 0，一直播到送別的東西；不存（✔ 實測）
- **插播一次**＝送 slot 0 → 網頁計時一輪（GIF 加總每格延遲；靜態圖用輸入秒數）→ 送 `[6+N,00,08,80,N_L,N_H,格號…]` 切回節目表全部格號 ⚠️切回指令未實測。節目表空就拒絕；等待中再插播則前一次不切回；結束時斷線報錯
- **存成節目第 n 格**＝slot n（✔ 實測可存、斷電後輪播）；收到完成碼才記進節目表

## 已驗證（實機）

- 連線：裝置名 `LED_BLE_B5E91A84`，寫入 `fa02`、通知 `fa03`；Bluefy 必須用 128-bit UUID 字串
- 送 GIF：12 KB/段，每段回 `05 00 03 00 01`，最後 `05 00 03 00 03`＝收完；封包與 pypixelcolor 逐 byte 一致
- 開／關、亮度
- 語言碼 0＝英文動畫；1～5 全是簡體（6～255 未測）；**沒有繁體**
- slot 0 不存；slot ≥1 會存，**斷電重開自動依格號輪播**（n＝1 次斷電）
- 使用者已用網頁存了 4 格：1 舊紅底靜態 A、2 黑底跑馬燈、3 黑底靜態 A、4 黑底靜態 B（依使用者描述推定）
- iPixel App 節目列表**看不到**網頁存的節目（App 列表是 App 自己的紀錄）；App 刪除會作用在裝置上（刪了 006）
- 實體遙控器任一鍵＝插播韌體內建動畫，播完自動回節目輪播；**遙控器不能選節目格**
- 裝置讀不回已存內容（協定沒有讀取指令）

## iPixel Color App 反編譯（11/04，詳見 SKILL.md）

- 來源：使用者 Windows 電腦 `C:\UnAPK\iPixel+Color_3.8.1_APKPure\`（已解開的 XAPK）；jadx 靜態分析，未執行
- 本機遙控器是**汽車版 20 鍵**（App `RemoteControlActivity`）：只送 `06 00 07 80 k 語言`，動畫在韌體，App 也不能改
- App 介面語言含 zh 時語言 byte＝1 → App 每按一次虛擬鍵就把動畫切回簡體
- 9 鍵商店版遙控器（`BusinessRemoteControlActivity`）可自訂：按鍵＝格號 111～119，用一般送圖寫入；本機未必支援（未測）
- APK 內素材（遙控器 GIF、文字背景、邊框、表情）是廠商著作，**不可放進本 repo**（Pages 公開）

## 待驗證（使用者還沒回報）

1. **虛擬遙控鍵**：會不會播、是不是英文、播完會不會自己回輪播
2. **插播一次**（跑馬燈）：約 10 秒後 LED 是否切回節目輪播（驗證 08 80 多格清單）
3. **節目表補登**：使用者要在手機補登現有 1～4 格
4. **刪除第 n 格**：網頁刪一格 → 斷電重開，輪播少那格才算成功
5. **顯示第 n 格**：能否切到指定節目
6. **GIF 延遲**：90 ms 版是否比 60 ms 明顯慢；速度選單是否有效
7. **跑馬燈實機效果**：黑底、紅色號次「1」實心圓、紅圈「卜」；「卜」可能要調大小或改空心
8. （低機率實驗，使用者要求才做）GIF 寫進 slot 111，看遙控器第 1 鍵會不會變

## 2026-11-08 新增

- 圖庫第 4 張 `keep_distance.png`（左眼、紅橘藍三箭頭、KEEP DISTANCE、右眼）。使用者要存成**節目第 5 格**，由使用者在網頁圖庫選「存成節目」第 5 格送出 ⚠️未實測
- 圖庫第 5 張 `keep_distance_2.png`（使用者第二張照片：眼、KEEP DISTANCE、紅＋兩藍箭頭、眼）；兩版擇一存節目 5，使用者未決定
- 圖庫第 6 張 `keep_distance_anim.gif`：使用者要「約 6 秒、每 2 秒交換」；6 秒無法在循環時維持 2 秒交換，改做 8 秒（A B A B）。⚠️每格 2000 ms 的長延遲裝置是否照播未實測（同待驗證「GIF 延遲」）

## 下一步候選（等上面結果）

- 「送自己的圖片／GIF」區也加三種送出方式
- 勾選部分格輪播（08 80 清單），等第 2 項驗證後
- 依使用者需求新增圖庫圖片

## 踩過的坑

1. Bluefy 不吃 `0xfa00` 數字 UUID → 用完整 128-bit 字串
2. `[8,0,1,0x80,時,分,秒,語言]`（讀裝置資訊）會改語言 → 不放自動流程，只在「改回英文」按鈕送 0
3. iPixel App 一用就改回簡體；同時只能一方連 LED，用網頁前要完全關掉 App
4. GitHub Pages 由使用者在 Settings → Pages 開（main / root）
5. Bluefy 會快取圖庫圖片 → 圖庫已加 `cache:"no-store"` 與 `?t=`；Pages CDN 仍可能舊約 10 分鐘
6. JS 錯誤不能吞掉：async onclick 一律 try/catch 並寫到「紀錄」
7. 回報的實測要分清楚是「實體遙控器」還是「網頁虛擬鍵」，別把使用者的敘述／提問誤記成實測結果（11/04 曾誤記一次並更正）

## 使用者偏好

- **全程繁體中文、台灣用語**（回覆也是，11/04 曾誤用英文被糾正）；LED 上不出現簡體字，寧可英文
- 結論先行、精簡；但數字的 n、未驗證假設、已知限制一定要寫
- 先量再改、判準事先寫、反向驗證、避免安靜失敗（成功／失敗明確顯示在畫面上）
