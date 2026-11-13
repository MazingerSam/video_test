---
name: colab-video-bridge
description: Google Colab 免費 GPU 遠端 AI 影片生成橋接工作流。涵蓋 Colab L4 / T4 GPU 算力調用、AnimateDiff (文字生影)、Stable Video Diffusion (圖片生影)、自動下載 MP4、以及「Colab 斷線/休眠重啟 SOP (Run all 一鍵重啟與網址重連)」。當使用者要求生成影片、調用 Colab、或輸入「重啟 COLAB」、「重新啟動 COLAB」、「重啟」、「reconnect colab」時觸發。
---

# Google Colab 遠端 GPU 影片生成與重啟維護指南 (Colab Video Bridge)

本技能提供本地 AI Agent（如 Antigravity、OpenCode、Claude 等）調用 **Google Colab L4 / T4 GPU** 進行 AI 影片生成，以及在 **Colab 休眠/斷線後「一鍵重啟與自動重連」** 的標準工作流程。

---

## 1. 系統架構

```text
[ 本地 AI Agent (Antigravity / OpenCode) ]
       │ 1. 產生/最佳化提示詞，發送 API 請求
       ▼
[ Cloudflare Tunnel 穿透 ] (免註冊、免金鑰安全公網連線)
       ▼
[ Google Colab 雲端伺服器 (FastAPI + L4/T4 GPU) ]
       │ 2. GPU 顯存常駐模型推論運算:
       │    - AnimateDiff (Text-to-Video)
       │    - Stable Video Diffusion XT (Image-to-Video)
       ▼
[ 本地 AI Agent 自動下載 MP4 至 outputs/ ]
```

---

## 2. ⚡ Colab 重啟與重新連線 SOP (Restart Protocol)

> **觸發情境**：Colab 閒置斷線、每日配額重置、電腦重新開機、或使用者輸入「**重啟 COLAB**」、「**重新啟動 COLAB**」時，Agent **必須** 遵循以下 SOP 協助用戶在 1 分鐘內恢復運作：

### 步驟 1：檢測現有連線狀態
Agent 先在終端執行狀態檢查：
```bash
python src/colab_client.py status
```
- 若回傳 `online`，代表原本的 Colab 仍在運行中，直接告知使用者連線正常，可繼續生成影片。
- 若回傳連線失敗（ConnectionError / 404 / 502），進入步驟 2。

### 步驟 2：引導使用者重啟 Colab 實體
Agent 提供以下一鍵啟動資訊給使用者：
1. **點擊開啟 Colab 筆記本**：  
   👉 [**開啟 Colab AI Video Workflow**](https://colab.research.google.com/github/MazingerSam/video_test/blob/main/notebooks/colab_ai_video_workflow.ipynb)
2. **一鍵全部執行**：  
   在 Colab 頂部選單點選 **「執行階段 (Runtime)」➔「全部執行 (Run all)」**（快捷鍵 `Ctrl + F9`）。  
   *(此操作會全自動安裝套件、載入模型並重啟 Cloudflare Tunnel 伺服器，全程約 1.5~2 分鐘)*。
3. **複製新網址**：  
   滾動到最底部的步驟 3，複製終端輸出的專屬網址：  
   `* Running on https://<新-tunnel-id>.trycloudflare.com`。

### 步驟 3：綁定新網址
使用者將新網址貼在聊天室後，Agent 立即執行綁定：
```bash
python src/colab_client.py connect https://<新-tunnel-id>.trycloudflare.com
```
*綁定完成後自動驗證顯卡狀態（Tesla T4 或 L4），並通知使用者已恢復連線！*

> [!TIP]
> **本地捷徑工具**：使用者亦可直接在專案根目錄執行 `restart_colab.bat` 或 `python connect.py`，系統會自動在瀏覽器彈出 Colab 頁面並引導輸入新網址。

---

## 3. 本地端 Agent 操作指令 (CLI)

本地專案目錄：`c:\Users\sam09\OneDrive\文件\AiAgent\video_test\`

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `python src/colab_client.py status` | 檢查 Colab 連線與 GPU 狀態 | `python src/colab_client.py status` |
| `python src/colab_client.py connect <URL>` | 綁定並更新 Colab 連線網址至 `.env` | `python src/colab_client.py connect https://xxx.trycloudflare.com` |
| `python src/colab_client.py t2v` | 文字生成影片 (AnimateDiff) | `python src/colab_client.py t2v --prompt "astronaut in space, 4k" --frames 16` |
| `python src/colab_client.py i2v` | 圖片生成動態影片 (SVD-XT) | `python src/colab_client.py i2v --image "sample.png" --frames 25` |

產出檔案預設存入：`outputs/colab_t2v_<timestamp>.mp4` 或 `colab_i2v_<timestamp>.mp4`。

---

## 4. Python SDK 調用範例 (給 Agent 程式碼整合)

本地 Agent 可直接引用客戶端類別：

```python
from src.colab_client import ColabVideoClient

client = ColabVideoClient()

# 1. 檢查 GPU 狀態
status = client.check_health()
print(f"GPU 在線: {status['gpu']}, 模型: {status['models_loaded']}")

# 2. 文字生影 (Text-to-Video)
t2v_path = client.generate_text_video(
    prompt="A majestic cyber lion walking on a neon platform, 4k, cinematic lighting",
    negative_prompt="blurry, distorted, low quality, watermark",
    num_frames=16
)
print("文字影片儲存至:", t2v_path)

# 3. 圖片生影 (Image-to-Video)
i2v_path = client.generate_image_video(
    image_path_or_url="outputs/input.png",
    num_frames=25
)
print("運鏡影片儲存至:", i2v_path)
```

---

## 5. 提示詞工程最佳實踐 (Prompt Tips)

1. **AnimateDiff (文字生影)**：
   - 必備畫質詞：`masterpiece, best quality, highly detailed, photorealistic, 4k, cinematic lighting`。
   - 動態詞句：`walking, glowing lights, camera moving forward, gentle wind blowing`。
   - 負面提示詞（Negative Prompt）：`bad quality, blurry, deformed, watermark, lowres`。
2. **SVD-XT (圖片生影)**：
   - 最佳解析度為 1024x576，橫向寬景畫面運鏡最自然。
   - `motion_bucket_id` 設為 100~150 之間（預設 127），動作流暢不破圖。

---

## 6. 常見問題與排錯 (Troubleshooting)

1. **Colab 顯示 Session Timeout (休眠斷線)**：
   - 請依照「第 2 節：Colab 重啟與重新連線 SOP」操作。
   - 點擊選單「執行階段」➔「全部執行 (Run all)」即可一鍵復原。
2. **CUDA Out of Memory (顯存不足)**：
   - 若使用 T4 GPU，建議單次維持 16 幀（文字生影）或 25 幀（圖片生影）。
   - 若改用 L4 GPU（24GB 顯存），可穩定連續生成多個片段無須重啟。
