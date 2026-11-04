---
name: colab-video-bridge
description: Google Colab 免費 GPU 遠端 AI 影片生成橋接工作流。讓本地 AI Agent (Antigravity、OpenCode、Claude 等) 透過 Cloudflare Tunnel 遠端調用 Colab 免費 T4 GPU，執行 AnimateDiff (文字生影) 與 Stable Video Diffusion (圖片生影)，並將生成的 MP4 自動下載回本地專案。
---

# Google Colab 遠端 GPU 影片生成技能指南 (Colab Video Bridge)

本技能提供本地 AI Agent（如 Antigravity、OpenCode 等）調用 **Google Colab 免費 T4 GPU** 進行開源 AI 影片生成的標準流程與操作規範。

---

## 1. 系統架構

```text
[ 本地 AI Agent (Antigravity / OpenCode) ]
       │ 1. 產生/最佳化提示詞，發送 API 請求
       ▼
[ Cloudflare Tunnel 穿透 ] (免註冊、免金鑰安全公網連線)
       ▼
[ Google Colab 雲端伺服器 (FastAPI + GPU) ]
       │ 2. GPU 顯存常駐模型推論運算:
       │    - AnimateDiff (Text-to-Video)
       │    - Stable Video Diffusion XT (Image-to-Video)
       ▼
[ 本地 AI Agent 自動下載 MP4 至 outputs/ ]
```

---

## 2. Colab 雲端伺服器啟動 SOP

當 Agent 需要指引用戶或確認 Colab 運作狀態時，遵循以下步驟：

1. **開啟 Notebook**：  
   使用專案筆記本：`https://colab.research.google.com/github/MazingerSam/video_test/blob/main/notebooks/colab_ai_video_workflow.ipynb`
2. **確認 GPU 加速**：  
   在 Colab 頂部選單點選 **「執行階段 (Runtime)」➔「變更執行階段類型」➔ 確認選擇「T4 GPU」**。
3. **依序執行步驟 0 ~ 3**：
   - 步驟 0：檢查顯卡 (`!nvidia-smi`)。
   - 步驟 1：安裝套件 (`diffusers`, `transformers`, `fastapi`, `uvicorn`, `pycloudflared` 等)。
   - 步驟 2：載入開源模型至 GPU 顯存常駐（AnimateDiff 與 SVD-XT）。
   - 步驟 3：啟動 FastAPI 與 Cloudflare Tunnel，終端會印出連線網址：
     ```text
     * Running on https://<tunnel-id>.trycloudflare.com
     ```
4. **取得連線網址**：  
   網址格式為 `https://xxxx.trycloudflare.com`。

---

## 3. 本地端 Agent 操作指令 (CLI)

本地工作目錄：`c:\Users\sam09\OneDrive\文件\AiAgent\video_test\`

### 3.1 連接伺服器並寫入環境變數
```bash
python src/colab_client.py connect https://<tunnel-id>.trycloudflare.com
```
*此指令會測試連線，並自動將網址持久化至專案 `.env` 中的 `COLAB_URL`。*

### 3.2 檢查伺服器健康狀態
```bash
python src/colab_client.py status
```
*成功時回傳：`{'status': 'online', 'gpu': 'Tesla T4', 'models_loaded': ['AnimateDiff', 'StableVideoDiffusion-XT']}`。*

### 3.3 文字生成影片 (Text-to-Video / AnimateDiff)
```bash
python src/colab_client.py t2v --prompt "masterpiece, 8k, astronaut walking on neon alien planet, cinematic lighting" --frames 16
```
- 產出檔案儲存於 `outputs/colab_t2v_<timestamp>.mp4`。
- 運算時間約 30~50 秒。

### 3.4 圖片生成動態影片 (Image-to-Video / SVD-XT)
```bash
python src/colab_client.py i2v --image "path/to/image.png" --frames 25
```
- 支援本機圖片路徑或網路圖片 URL。
- 自動縮放並對齊 1024x576 解析度進行運鏡推算。
- 產出檔案儲存於 `outputs/colab_i2v_<timestamp>.mp4`。

---

## 4. Python SDK 調用方式 (給 Agent 程式碼整合)

本地 Agent 可直接在 Python 代碼中引用客戶端模組：

```python
from src.colab_client import ColabVideoClient

client = ColabVideoClient()

# 1. 檢查 GPU 狀態
status = client.check_health()
print("GPU 裝置:", status["gpu"])

# 2. 文字生成影片
video_path = client.generate_text_video(
    prompt="A glowing futuristic cyber jellyfish floating in deep dark ocean, 4k",
    negative_prompt="blurry, distorted, low quality",
    num_frames=16
)
print("影片下載完成:", video_path)

# 3. 圖片生成運鏡影片
svd_video = client.generate_image_video(
    image_path_or_url="outputs/sample.png",
    num_frames=25
)
print("SVD 影片下載完成:", svd_video)
```

---

## 5. 提示詞工程最佳實踐 (Prompt Tips)

1. **AnimateDiff (文字生影)**：
   - 善用畫質觸發詞：`masterpiece, highly detailed, photorealistic, 4k, cinematic lighting`。
   - 動態描述：加入明確動態（如 `walking, hair fluttering in wind, water flowing, camera slow push in`）。
   - 負面提示詞（Negative Prompt）：預設已加入 `bad quality, blurry, deformed, watermark`，避免肢體崩壞。
2. **SVD-XT (圖片生影)**：
   - 圖片主體明確（人物、載具、建築或風景自然景深佳）。
   - `motion_bucket_id` 範圍 1~255（數值越大動作幅度越大，預設 127 為平衡運鏡）。

---

## 6. 排錯與注意事項 (Troubleshooting)

1. **連線逾時 (Connection Refused / Timeout)**：
   - 請檢查 Google Colab 瀏覽器分頁是否處於開啟狀態（防休眠）。
   - 若 Colab 重新整理或重連，Cloudflare Tunnel 網址會更新，需重新執行 `python src/colab_client.py connect <新網址>`。
2. **CUDA Out of Memory (顯存溢出)**：
   - 模型載入已啟用 `enable_model_cpu_offload()` 與 `enable_slicing()`。
   - 保持單次請求幀數在 16 幀（AnimateDiff）或 25 幀（SVD），符合 T4 15GB 顯存的最佳效能範圍。
