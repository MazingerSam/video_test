import os
import sys
import time
import base64
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv, set_key

# 處理 Windows 終端編碼
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 載入 .env
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_FILE)

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class ColabVideoClient:
    """與遠端 Google Colab GPU 橋接伺服器通訊的客戶端。"""

    def __init__(self, colab_url: Optional[str] = None):
        self.colab_url = (colab_url or os.getenv("COLAB_URL", "")).rstrip("/")

    def set_colab_url(self, url: str, persist: bool = True):
        """設定並持久化 Colab 伺服器網址到 .env。"""
        self.colab_url = url.rstrip("/")
        if persist:
            if not ENV_FILE.exists():
                ENV_FILE.touch()
            set_key(str(ENV_FILE), "COLAB_URL", self.colab_url)
            print(f"[OK] 已將 COLAB_URL 儲存至 {ENV_FILE}")

    def check_health(self) -> Dict[str, Any]:
        """檢查 Colab 伺服器健康狀態與顯卡資訊。"""
        if not self.colab_url:
            raise ValueError("尚未設定 COLAB_URL！請先執行 connect 指令或在 .env 設定。")

        resp = requests.get(f"{self.colab_url}/health", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def generate_text_video(
        self,
        prompt: str,
        negative_prompt: str = "bad quality, blurry, distorted, lowres",
        num_frames: int = 16,
        num_inference_steps: int = 25,
        guidance_scale: float = 7.5,
        output_dir: Optional[Path] = None
    ) -> Path:
        """請求 Colab GPU 執行 AnimateDiff 文字生成影片。"""
        if not self.colab_url:
            raise ValueError("尚未設定 COLAB_URL！")

        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_frames": num_frames,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale
        }

        print(f"[*] 發送文字生影請求至 Colab GPU: {prompt}...")
        resp = requests.post(f"{self.colab_url}/generate/text2video", json=payload, timeout=600)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "success":
            raise RuntimeError(f"生成失敗: {data.get('error', '未知錯誤')}")

        video_bytes = base64.b64decode(data["video_base64"])
        out_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
        out_file = out_dir / f"colab_t2v_{int(time.time())}.mp4"
        with open(out_file, "wb") as f:
            f.write(video_bytes)

        print(f"[OK] 影片生成成功並已下載至本地: {out_file}")
        return out_file

    def generate_image_video(
        self,
        image_path_or_url: str,
        num_frames: int = 25,
        fps: int = 7,
        motion_bucket_id: int = 127,
        output_dir: Optional[Path] = None
    ) -> Path:
        """請求 Colab GPU 執行 Stable Video Diffusion 圖片生成影片。"""
        if not self.colab_url:
            raise ValueError("尚未設定 COLAB_URL！")

        # 讀取圖片並轉為 base64
        if image_path_or_url.startswith("http://") or image_path_or_url.startswith("https://"):
            img_resp = requests.get(image_path_or_url, timeout=15)
            img_resp.raise_for_status()
            img_b64 = base64.b64encode(img_resp.content).decode("utf-8")
        else:
            with open(image_path_or_url, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "image_base64": img_b64,
            "num_frames": num_frames,
            "fps": fps,
            "motion_bucket_id": motion_bucket_id
        }

        print("[*] 發送圖片生影請求至 Colab GPU (SVD-XT)...")
        resp = requests.post(f"{self.colab_url}/generate/image2video", json=payload, timeout=600)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "success":
            raise RuntimeError(f"生成失敗: {data.get('error', '未知錯誤')}")

        video_bytes = base64.b64decode(data["video_base64"])
        out_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
        out_file = out_dir / f"colab_i2v_{int(time.time())}.mp4"
        with open(out_file, "wb") as f:
            f.write(video_bytes)

        print(f"[OK] 影片生成成功並已下載至本地: {out_file}")
        return out_file


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity to Colab GPU Video Client")
    subparsers = parser.add_subparsers(dest="command")

    # connect 指令
    connect_p = subparsers.add_parser("connect", help="連接並設定 Colab 伺服器網址")
    connect_p.add_argument("url", type=str, help="Colab 產生的 public tunnel 網址 (如 https://xxx.trycloudflare.com)")

    # status 指令
    subparsers.add_parser("status", help="檢查 Colab 伺服器狀態與顯卡")

    # t2v 指令
    t2v_p = subparsers.add_parser("t2v", help="文字生成影片 (AnimateDiff)")
    t2v_p.add_argument("--prompt", required=True, type=str, help="影片英文提示詞")
    t2v_p.add_argument("--frames", default=16, type=int, help="幀數 (預設 16)")

    # i2v 指令
    i2v_p = subparsers.add_parser("i2v", help="圖片生成動態影片 (SVD)")
    i2v_p.add_argument("--image", required=True, type=str, help="本機圖片路徑或圖片 URL")
    i2v_p.add_argument("--frames", default=25, type=int, help="幀數 (預設 25)")

    args = parser.parse_args()
    client = ColabVideoClient()

    if args.command == "connect":
        client.set_colab_url(args.url)
        info = client.check_health()
        print("連線狀態:", info)
    elif args.command == "status":
        info = client.check_health()
        print("伺服器正常:", info)
    elif args.command == "t2v":
        out = client.generate_text_video(prompt=args.prompt, num_frames=args.frames)
        print("本地檔案路徑:", out)
    elif args.command == "i2v":
        out = client.generate_image_video(image_path_or_url=args.image, num_frames=args.frames)
        print("本地檔案路徑:", out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
