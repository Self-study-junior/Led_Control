---
name: led-control
description: 接續或修改 Led_Control（iPixel Color 96×16 LED 繁中 Web Bluetooth 控制台、圖庫圖片）時使用：先讀 HANDOFF.md，依本檔的協定、坑與工作流程動手。
---

# Led_Control 技能

## 開工順序

1. 讀 repo 根目錄 `HANDOFF.md`（現況、已驗證、待驗證）。
2. 問使用者「待驗證」那幾項的結果；沒有結果前，不做依賴它的功能。
3. 改完一律：JS 語法檢查 → commit → push main → 請使用者在 Bluefy 重新整理實測。
4. 收工前更新 `HANDOFF.md`（日期、已驗證／待驗證）。

## 硬體／環境

- iPixel Color 96×16，BLE 名稱 `LED_BLE_xxxxxxxx`
- 使用者在 iPhone 用 **Bluefy** 開 https://self-study-junior.github.io/Led_Control/
- Pages 由使用者自己開（main / root）

## 協定（依 pypixelcolor，MIT，已實機驗證的標 ✔）

- 寫入特徵 `0000fa02-0000-1000-8000-00805f9b34fb` ✔；通知 `0000fa03-…` ✔
- 服務 UUID 未知，`optionalServices` 放候選並**用完整 128-bit 字串** ✔（Bluefy 不吃數字）
- 每次寫入 ≤244 bytes，`writeValueWithResponse`
- 開／關 `05 00 07 01 01|00` ✔
- 亮度 `05 00 04 80 NN`（0–100）✔
- 讀裝置資訊／設語言 `08 00 01 80 時 分 秒 語言`；回應 byte[4]=132 → 96×16。**語言 0＝英文** ✔；1～5＝簡體 ✔（6～255 未測）；網頁固定送 0
- 圖片／GIF ✔：檔案切 12 KB 一段，每段：
  `[LEN_L LEN_H] [type 02=PNG|03=GIF, 00] [option 00首段|02後續] [size u32 LE] [CRC32 u32 LE] [GIF:02|PNG:00] [slot] [資料]`
  LEN＝整段長度（含 LEN 兩 byte）。每段等通知 `05 00 03 00 01`（收到段）／`… 03`（全部收完）。
- 顯示某格 `07 00 08 80 01 00 n`、節目清單 `[6+N] 00 08 80 N_L N_H [格號…]`：裝置回 `05 00 08 80 01`，但**都不能把 slot 0 內容切回輪播**（11/08）。切回輪播唯一有效＝藍牙斷線＋重連（只斷線無效；重連時 LED 會短暫顯示連線圖示）
- 遙控鍵 `06 00 07 80 k 語言`（k＝1～20，本機汽車版）✔：**裝置不回通知**，語言 0 播英文、播完自動回節目輪播。送出時不可等 ACK
- 刪除某格、清 ROM 見 pypixelcolor `commands/delete.py`、`clear.py`（clear 會清掉設定，**不要用**）
- 警告：存進格子的資料若壞掉可能開機循環；先不存格測通再存
- slot 0＝只顯示不存 ✔；slot ≥1＝存，開機依格號輪播 ✔；裝置讀不回內容，iPixel App 也看不到網頁存的 → 網頁節目表（localStorage）是唯一紀錄
- 遙控器只會插播內建動畫，不能選節目格 ✔；寫第 110+k 格、或先送 08 80 登記 111～119，按鍵仍播內建 ✔（11/08）→ 汽車版 20 鍵不能自訂

## iPixel Color 3.8.1 Android 反編譯結果（2026-11-04，jadx 靜態分析，未實測）

來源：使用者提供的 APKPure XAPK（`C:\UnAPK`），程式在 `com.wifiled.ipixels`。**廠商素材不可放進本 repo（Pages 公開）**。

- 遙控器 9 鍵＝裝置格號 **111～119**（`BusinessControlModel.autoSendChannel`）。App 的「遙控器」頁（`BusinessRemoteControlActivity`，96 寬機型有）可編輯每鍵內容（GIF／圖片／文字）後整批送出：
  1. 若 MCU 版本 > 4：先送 `[長度,00,08,80,9,00,111,112,…,119]`（同 show_slot／輪播的 08 80 格式，用途推測為登記遙控器格）。MCU 版本來自 App 的 OTA 伺服器查詢，BLE 讀不到
  2. 每鍵間隔 300 ms，用一般送圖封包存進 slot＝111+鍵號−1（尾巴 `[02, slot]`，與網頁 sendFile 相同）
- **本機（汽車版 20 鍵＋電源）走的是另一頁 `RemoteControlActivity`**：沒有編輯／上傳功能，按鍵只送 `06 00 07 80 k 語言`（k＝1～20）；預覽圖從雲端素材庫（category「驾驶」、label YK、file_lang cn/en）下載，只供顯示。→ 20 鍵動畫在 LED 韌體，App 也無法改。上面 111～119 那套是 9 鍵商店版，本機未必支援（未測）
- App 介面語言含 zh 時語言 byte＝1（簡體），所以繁中 App 每按一次虛擬鍵都會把動畫切回簡體
- 「恢復預設」＝把 APK 內建 `assets/remote/yk_anim_{en|cn}_16x96_{1..9}.gif` 再送一次（en 鍵 1 在 CID 0017／PID 01 機型改用 `_1_171.gif`）
- App 虛擬遙控器按鍵：`06 00 07 80 k 語言`（k＝1～9；語言＝App 介面是中文時 1，否則 0）→ 這可能就是 App 一用就把動畫改回簡體的原因
- 內建英文 9 鍵：BIG SALE、ON SALE、OPEN 24 HOURS、SHOP OPEN、WiFi FREE、QUICK BUY、WELCOME、DISCOUNTS、SHOPPING（96×16，0.8～4 秒）
- 其他 96×16 素材：`assets/gif/text_ani_bg_16_96_*`（10 個文字背景動畫）、`assets/border/ani_border_96_16_*`（24 個邊框）、`assets/emoji/text_emoji_16_*`（525 個 16px 表情）；「素材庫」其餘內容從 `app.heaton.cn` 下載，不在 APK

## 製圖規範（11/08 實機驗證後定案；範本 `tools/make_slow_car.py`）

### 畫布與顏色
- 一律 **96×16**，背景純黑 `(0,0,0)`＝不亮燈；不要用深灰當底（LED 會微亮）
- 顏色用飽和純色、整數 RGB，**整張 GIF 合計 ≤8 色**（實機順播的三張都是 4～8 色）
- 慣用色：黃 `(255,210,0)`（提醒字）、紅 `(255,50,30)`（警告字）、白、藍 `(40,140,255)`、淺藍 `(160,225,255)`、灰 `(130,130,130)`
- 不要反鋸齒：畫字 `ImageDraw.fontmode="1"`；縮放一律 `Image.NEAREST`；從 canvas 來的要二值化

### 文字
- **中文：Unifont 16px 點陣**（`/usr/share/fonts/opentype/unifont/unifont.otf`，字寬 16、全高 16）。不要用一般字型縮小，16px 高的反鋸齒字在 LED 上會糊
- 英文大字：自訂點陣字 4×7（`tools/make_keep_distance_anim.py` 的 `F`），空間不夠才用 3×7；7 高的字放 y=4～10 置中
- 數字小字：3×5（`tools/make_marquee.py` 早期版本）
- 全形標點（，）會佔 16px 寬，排版要算進去

### 圖示
- 用字串陣列畫像素圖（每個字元一種顏色，`.`＝不亮），寫在產生程式裡，方便改
- 高度 ≤12、垂直置中；例：汽車 19×9（`CAR_ART`）、警示三角 16×14、眼睛 13×8、圈選章 16×16
- 圖示與文字之間留 2～4px 黑

### 動畫
- **跑馬燈**：整條內容先畫成一張長圖，前面補 96px 黑（從右邊捲入），每格移 **2px**、每格 **90 ms**（60 ms 使用者嫌快）、`loop=0`
- **閃爍**：畫「亮／暗」兩張長圖，依格數切換（`BLINK=6` 格≈0.54 秒）
- **交替畫面**：固定元素（如兩端眼睛）畫在底圖，中間內容 A／B 交換；每段停留用每格延遲（例 2000 ms）。循環接頭也要維持同樣的交換節奏（6 秒做不到 2 秒交換就做 8 秒）

### 存檔（重要）
- **GIF 一律用 `tools/gifenc.py`**：整份共用一份全域色表、每格都是完整 96×16 畫面、無局部色表、無透明
- **不要用 PIL `save_all`**：它會每格各帶局部色表並只存變動區塊。11/08 實機：小車段 8 色時卡住約 3 秒再跳過一段；改用 gifenc 後完整播放（n＝1）
- 靜態圖存 PNG（PIL 直接存即可，實機正常）
- 檔案大小參考：96×16 跑馬燈 150～170 格約 30 KB，送出 3 段、約 5 秒

### 交付前檢查（每張都做）
1. `python3 tools/gifscan.py gallery/新檔.gif`：確認 全域色表 ≤8、全幅＝格數、局部色表格數＝0、延遲正確
2. 整條長圖放大 8 倍（NEAREST）自己看過：字有沒有黏、圖示有沒有被裁
3. 只改編碼或速度時：新舊檔逐格解碼比對要完全相同（並故意改一格確認比對會失敗）
4. 放大版預覽（6 倍 GIF）傳給使用者看

### 登記
- 圖放 `gallery/`，產生程式放 `tools/make_*.py`（在 repo 根目錄執行），登記到 `gallery/gallery.json`（`{"file","name"}`，名稱寫內容＋型態，例「（跑馬燈・三角閃爍）」）
- 圖庫順序就是網頁編號；單次插播預設 01 指向檔名（`slow_car.gif`），改順序不影響
- 只改速度時用網頁速度選單或改每格延遲，不要重畫像素

## Git

- 作者：`Self-study-junior <774630+Self-study-junior@users.noreply.github.com>`
- commit 訊息繁中；推 main
- repo 已改名 `Led_Control`：clone 後先 `git remote set-url origin https://github.com/Self-study-junior/Led_Control.git`，不然 push 會被拒（`This repository moved`）；偶發 GitHub 500 等 10～20 秒重推
- 推送權限：Claude 帳號的 GitHub 連線要是 Self-study-junior
- 不要碰 `Self-study-junior/Junior`（兒子的複習網站）

## 使用者偏好

- 繁體中文、台灣用語；LED 上不要簡體字
- 先量再改、判準先寫、反向驗證、成功／失敗要在畫面上明確顯示（避免安靜失敗）
