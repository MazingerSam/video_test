# 🎬 AI Video Workflow (Google Colab & Python)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MazingerSam/video_test/blob/main/notebooks/colab_ai_video_workflow.ipynb)

本專案旨在提供於 **Google Colab** 雲端環境及本機中執行的 **AI 影片生成工作流**。整合了 Higgsfield AI 旗艦級擬真圖像模型（Soul v2）與電影級動態運鏡影片生成模型（Cinematic Studio），並支援雲端硬碟掛載、批次生成與互動式即時預覽。

---

## 🌟 核心特色

1. **Colab 一鍵運行**：提供完整的 Jupyter Notebook (`notebooks/colab_ai_video_workflow.ipynb`)，無須本機顯卡，透過 Colab 雲端即可執行。
2. **文字轉圖像 (Soul v2)**：生成超高解析度（2K）、自然擬真光影的人物與場景起始幀（Keyframe）。
3. **圖片/文字轉影片 (Cinematic Studio)**：流暢電影級鏡頭推拉（Dolly/Tracking/Pan/Zoom），呈現穩定動態效果。
4. **雲端硬碟自動備份**：支援 Google Drive 同步，影片生成後直接歸檔。
5. **模組化程式庫**：提供 `src/` 套件封裝，方便擴展為 CLI 或自動化批次腳本。

---

## 📂 目錄結構

```text
video_test/
├── notebooks/
│   └── colab_ai_video_workflow.ipynb   # Google Colab 互動式執行筆記本
├── src/
│   ├── __init__.py                     # 模組初始化
│   ├── config.py                       # 環境變數與模型設定
│   ├── video_generator.py              # 影像與影片生成工作流核心
│   └── utils.py                        # 下載與環境工具
├── .env.example                        # 環境變數範本
├── .gitignore                          # Git 忽略設定
├── CHANGELOG.md                        # 版本變更紀錄
├── progress.md                         # 任務與進度追蹤
├── README.md                           # 專案指南 (本文件)
└── requirements.txt                    # 相依套件清單
```

---

## 🚀 快速開始

### 方式 1：於 Google Colab 執行 (推薦)

1. 將 `notebooks/colab_ai_video_workflow.ipynb` 上傳至 [Google Colab](https://colab.research.google.com/)。
2. 在 Colab 左側工具列的 **🔑 密鑰 (Secrets)** 新增：
   - 名稱：`HF_KEY`
   - 值：你的 Higgsfield API Key (`key_id:key_secret`)
3. 依序執行儲存格即可完成：
   - 安裝環境
   - 文字生圖（Soul v2）
   - 圖片生成電影級影片（Cinematic Studio）
   - 即時在 Notebook 中播放與下載

### 方式 2：本機 Python 環境執行

1. **安裝依賴套件**：
   ```bash
   pip install -r requirements.txt
   ```
2. **配置環境變數**：
   複製 `.env.example` 為 `.env` 並填入憑證：
   ```env
   HF_KEY="your-key-id:your-key-secret"
   ```
3. **Python 程式範例**：
   ```python
   from src.video_generator import VideoWorkflowManager

   manager = VideoWorkflowManager()

   # 1. 生成起始圖像
   img_res = manager.generate_image("A futuristic city at sunset, cinematic lighting, 8k")
   print("Image saved:", img_res["local_path"])

   # 2. 以圖生影
   video_res = manager.generate_video(
       prompt="Drone camera soaring through skyscrapers",
       image_url=img_res["url"],
       duration=5
   )
   print("Video saved:", video_res["local_path"])
   ```

---

## 🔑 支援模型

| 模型識別碼 | 類型 | 說明 |
| :--- | :--- | :--- |
| `higgsfield-ai/soul/v2/standard` | Text-to-Image | 旗艦級擬真視覺模型，人物膚質與光影極佳 |
| `higgsfield-ai/soul/v2/turbo` | Text-to-Image | 低延遲、快速出圖 |
| `higgsfield-ai/cinematic_studio_2_5` | Text/Image-to-Video | 電影級運鏡影片生成 (支援 16:9, 9:16 等) |

---

## 📄 授權與維護
由 AI Agent 輔助建立與維護。
