# 變更紀錄 (Changelog)

所有本專案的重要變更皆會記錄於此。

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

## [0.2.0] - 2026-11-04

### 新增 (Added)
- **100% 開源免金鑰工作流**：移除第三方 API 限制，完全基於 Google Colab 免費 GPU (T4)。
- **AnimateDiff (文字轉影片)**：整合 Realistic Vision 與 Motion Adapter，文字直接產出動態影片。
- **Stable Video Diffusion XT (圖片轉影片)**：整合 Stability AI 官方 SVD-XT 模型，高畫質靜態圖轉 25 影格運鏡影片。
- **T4 顯存最佳化**：加入 VAE Slicing 與 Model CPU Offload，保證於免費 Colab 執行時不發生 CUDA OOM。

## [0.1.0] - 2026-11-04

### 新增 (Added)
- 初始化專案結構與 Git 儲存庫。
- 建立專案與 GitHub (`MazingerSam/video_test`) 關聯。
