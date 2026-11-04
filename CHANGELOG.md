# 變更紀錄 (Changelog)

所有本專案的重要變更皆會記錄於此。

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

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
