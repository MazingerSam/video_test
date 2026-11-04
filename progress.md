# 專案進度追蹤 (Progress Tracking)

## 里程碑 1：專案初始化與結構設定 (已完成 ✅)
- [x] 初始化 Git 儲存庫
- [x] 建立標準基礎檔案 (`.gitignore`, `requirements.txt`, `README.md`)
- [x] 連接 GitHub 儲存庫 (`MazingerSam/video_test`) 並配置 Open in Colab 一鍵啟動連結

## 里程碑 2：開源免金鑰雙工作流升級 (已完成 ✅)
- [x] 移除第三方付費 API 依賴，改為 100% 免費開源模型
- [x] 實作工作流 1：AnimateDiff (Text-to-Video 文字生影片)
- [x] 實作工作流 2：Stable Video Diffusion (SVD-XT 圖片生動態影片)
- [x] 完成 Colab T4 顯存最佳化 (VAE Slicing, CPU Offload，防 OOM)
- [x] 支援 Google Drive 自動雲端備份

## 里程碑 3：後續擴展功能 (待辦 ⏳)
- [ ] 加入 AnimateDiff-Lightning 4-step / 8-step 極速推論支援
- [ ] 支援本地 Gradio 互動介面
- [ ] 支援音樂與配樂自動合成
