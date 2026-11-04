# 🎬 Open-Source AI Video Workflow (Google Colab 免費 GPU 專用)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MazingerSam/video_test/blob/main/notebooks/colab_ai_video_workflow.ipynb)

本專案提供於 **Google Colab 免費 T4 GPU** 運行的 **100% 免費、開源 AI 影片生成工作流**。  
**完全不需要申請或填入任何付費 API 金鑰**，所有模型權重直接在 Colab 雲端顯卡載入與運算！

---

## 🌟 核心開源雙工作流

1. **工作流 1：AnimateDiff (文字轉影片 / Text-to-Video)**
   - 輸入任意英文提示詞，自動生成生動、流暢的動態短影片。
   - 整合了 Realistic Vision V5.1 與 AnimateDiff Motion Adapter。
   - 針對 Colab T4 顯存最佳化（VAE Slicing + CPU Offload，防 OOM）。

2. **工作流 2：Stable Video Diffusion - SVD (圖片轉影片 / Image-to-Video)**
   - 由 Stability AI 開源的旗艦級圖像動態化模型（SVD-XT）。
   - 上傳任意靜態風景、人物或概念圖，自動生成高解析度電影感運鏡影片（1024x576，25 影格）。

---

## 📂 目錄結構

```text
video_test/
├── notebooks/
│   └── colab_ai_video_workflow.ipynb   # Google Colab 開源影片生成筆記本
├── src/
│   ├── __init__.py                     # 模組初始化
│   ├── config.py                       # 開源模型權重配置
│   ├── video_generator.py              # AnimateDiff 與 SVD 開源工作流封裝
│   └── utils.py                        # 下載與環境工具
├── .gitignore                          # Git 忽略設定
├── CHANGELOG.md                        # 版本變更紀錄
├── progress.md                         # 任務與進度追蹤
├── README.md                           # 專案指南 (本文件)
└── requirements.txt                    # 開源相依套件 (Diffusers, Transformers, PyTorch)
```

---

## 🚀 快速開始 (只需 2 步)

1. **一鍵開啟 Colab**：  
   點擊上方的 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MazingerSam/video_test/blob/main/notebooks/colab_ai_video_workflow.ipynb)。
2. **切換為 T4 GPU**：  
   在 Colab 選單選擇 **「執行階段」➔「變更執行階段類型」➔「T4 GPU」**。
3. **依序點擊執行儲存格**：  
   無須填入任何金鑰，即可直接在 Colab 內生成並播放您的 AI 影片！

---

## 🔑 開源模型一覽

| 模型 | 類型 | 來源庫 | 說明 |
| :--- | :--- | :--- | :--- |
| **AnimateDiff** | Text-to-Video | `guoyww/animatediff-motion-adapter-v1-5-2` | 經典開源文字生影片架構 |
| **Realistic Vision** | Base UNet | `SG161222/Realistic_Vision_V5.1_noVAE` | 寫實擬真風格底模 |
| **SVD-XT** | Image-to-Video | `stabilityai/stable-video-diffusion-img2vid-xt` | Stability AI 官方 25 影格長鏡頭圖生影 |

---

## 📄 授權與維護
由 AI Agent 輔助建立與維護。
