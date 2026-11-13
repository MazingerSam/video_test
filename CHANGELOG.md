# 變更紀錄 (Changelog)

所有本專案的重要變更皆會記錄於此。

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

## [0.3.2] - 2026-11-13

### 新增 (Added)
- **Colab 斷線重啟標準 SOP 與自動化輔助工具**：
  - 新增本機輔助工具 [`connect.py`](file:///c:/Users/sam09/OneDrive/文件/AiAgent/video_test/connect.py) 與 [`restart_colab.bat`](file:///c:/Users/sam09/OneDrive/文件/AiAgent/video_test/restart_colab.bat)，支援自動開啟瀏覽器並引導輸入新網址。
  - 於 `colab-video-bridge` 技能中建立專屬〈Colab 重啟與重新連線 SOP〉，支援透過「全部執行 (Run all)」在 1 分鐘內重建遠端服務。

## [0.3.1] - 2026-11-13

### 變更 (Changed)
- 將 Colab 筆記本預設硬體加速器配置提升至 **NVIDIA L4 GPU** (24GB 顯存，Ada Lovelace 架構)，提升影片生成速度與畫質。
- 更新技能文件與說明文件，支援 L4 與 T4 雙規格無縫切換。

## [0.3.0] - 2026-11-04

### 新增 (Added)
- **Antigravity ➔ Colab 遠端 GPU 橋接架構**：
  - Colab 端：提供 FastAPI 背景服務與 `pycloudflared` 免費免註冊穿透，輸出公網專屬 Tunnel URL。
  - 模型顯存常駐：AnimateDiff 與 SVD-XT 預載於顯存，後續生成大幅提速至 30~60 秒。
  - 本地端：建立 [`src/colab_client.py`](file:///c:/Users/sam09/OneDrive/文件/AiAgent/video_test/src/colab_client.py) CLI，支援文字生影與圖片生影，完成後自動下載 MP4 檔案至 `outputs/`。

## [0.2.0] - 2026-11-04

### 新增 (Added)
- **100% 開源免金鑰工作流**：移除第三方 API 限制，完全基於 Google Colab 免費 GPU (T4)。
- **AnimateDiff (文字轉影片)** 與 **Stable Video Diffusion XT (圖片轉影片)**。

## [0.1.0] - 2026-11-04

### 新增 (Added)
- 初始化專案結構與 Git 儲存庫。
- 建立專案與 GitHub (`MazingerSam/video_test`) 關聯。
