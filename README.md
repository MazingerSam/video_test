# 🎬 Antigravity ➔ Google Colab 遠端 GPU 影片生成中樞

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MazingerSam/video_test/blob/main/notebooks/colab_ai_video_workflow.ipynb)

本專案實現了 **「本地 Antigravity 撰寫提示詞指揮 ➔ 遠端 Google Colab 免費 T4 GPU 算力生成 ➔ 自動下載 MP4 至本地」** 的全自動化影片生成中樞！

---

## 🌟 核心架構與優勢

```text
[ 您在 Antigravity 聊天 ]
       │ "請幫我做一段太空人在霓虹星球漫步的影片"
       ▼
[ Antigravity Agent ] ──(發送 API 請求)──▶ [ Google Colab 雲端 T4 GPU 伺服器 ]
       ▲                                                    │
       │                                                    ▼
       └──────────(自動下載 MP4 至 outputs/)────────── [ AnimateDiff / SVD 模型推論 ]
```

1. **零成本、免付費 API**：直接利用 Google Colab 每日免費提供的 15GB T4 GPU。
2. **模型常駐顯存 (Warm-up)**：首次載入後常駐 GPU，後續每次生成只需 30~60 秒，無須重複下載權重。
3. **免設定穿透 (Cloudflare Tunnel)**：透過免註冊、免金鑰的穿透技術，一鍵在 Colab 產生外部安全連線網址。
4. **雙開源工作流支援**：
   - **文字轉影片 (Text-to-Video)**：AnimateDiff + Realistic Vision
   - **圖片轉影片 (Image-to-Video)**：Stable Video Diffusion XT (SVD-XT)

---

## 📂 目錄結構

```text
video_test/
├── notebooks/
│   └── colab_ai_video_workflow.ipynb   # Colab 遠端 GPU 伺服器核心筆記本
├── src/
│   ├── colab_client.py                 # Antigravity 本地連線與命令列客戶端
│   ├── video_generator.py              # 開源模型 Pipeline 封裝
│   ├── config.py                       # 模型與路徑配置
│   └── utils.py                        # 工具函式庫
├── outputs/                            # 生成完成之 MP4 本地儲存資料夾
├── .gitignore                          # Git 忽略設定
├── CHANGELOG.md                        # 變更紀錄
├── progress.md                         # 進度追蹤
├── README.md                           # 專案指南 (本文件)
└── requirements.txt                    # 相依套件
```

---

## 🚀 完整使用步驟 (只需 3 步)

### 步驟 1：在 Colab 啟動 GPU 伺服器
1. 點擊頂部的 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MazingerSam/video_test/blob/main/notebooks/colab_ai_video_workflow.ipynb) 開啟筆記本。
2. 確認執行階段類型為 **T4 GPU**。
3. 依序執行步驟 0、1、2、3 儲存格。完成後會輸出專屬連線網址：
   ```text
   🔗 專屬連線網址: https://xxxx-xxxx-xxxx.trycloudflare.com
   ```

### 步驟 2：將網址交給 Antigravity
在 Antigravity 聊天室貼上該網址（例如：`https://xxxx.trycloudflare.com`），或在本地執行：
```bash
python src/colab_client.py connect https://xxxx.trycloudflare.com
```

### 步驟 3：在 Antigravity 隨意生成影片！
伺服器連線成功後，只要跟 Antigravity 說：
- *「幫我生一段水下發光水母的影片」*
- *「把這張圖片轉成運鏡影片」*

Antigravity 就會自動調用 Colab GPU 生成，並在完成後把 MP4 檔案下載至 `outputs/` 並在聊天室呈現！
