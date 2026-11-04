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
- 讀裝置資訊／設語言 `08 00 01 80 時 分 秒 語言`；回應 byte[4]=132 → 96×16。**語言 0＝英文** ✔
- 圖片／GIF ✔：檔案切 12 KB 一段，每段：
  `[LEN_L LEN_H] [type 02=PNG|03=GIF, 00] [option 00首段|02後續] [size u32 LE] [CRC32 u32 LE] [GIF:02|PNG:00] [slot] [資料]`
  LEN＝整段長度（含 LEN 兩 byte）。每段等通知 `05 00 03 00 01`（收到段）／`… 03`（全部收完）。
- 顯示某格 `07 00 08 80 01 00 n`；節目輪播 `[4+N] 00 08 80 N_L N_H [格號…]`（未實測）
- 刪除某格、清 ROM 見 pypixelcolor `commands/delete.py`、`clear.py`（clear 會清掉設定，**不要用**）
- 警告：存進格子的資料若壞掉可能開機循環；先不存格測通再存

## 圖片製作規則

- 一律 96×16，黑色＝不亮
- 中文用 Unifont 16px 點陣（`/usr/share/fonts/opentype/unifont/unifont.otf`），不要用反鋸齒字型縮小
- 跑馬燈：前面補 96px 黑，每格移 2px、60ms、loop=0、≤8 色
- 新圖放 `gallery/`，登記到 `gallery/gallery.json`；產生程式放 `tools/`
- 交付前把整條放大 8 倍（NEAREST）自己看過再推

## Git

- 作者：`Self-study-junior <774630+Self-study-junior@users.noreply.github.com>`
- commit 訊息繁中；推 main
- 不要碰 `Self-study-junior/Junior`（兒子的複習網站）

## 使用者偏好

- 繁體中文、台灣用語；LED 上不要簡體字
- 先量再改、判準先寫、反向驗證、成功／失敗要在畫面上明確顯示（避免安靜失敗）
