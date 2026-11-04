import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
from .config import HF_KEY, OUTPUT_DIR, DEFAULT_IMAGE_MODEL, DEFAULT_VIDEO_MODEL
from .utils import download_file

class VideoWorkflowManager:
    """Higgsfield AI 影片與圖像工作流管理器。"""

    def __init__(self, api_key: Optional[str] = None, output_dir: Optional[Path] = None):
        self.api_key = api_key or HF_KEY or os.getenv("HF_KEY", "")
        if self.api_key:
            os.environ["HF_KEY"] = self.api_key
        self.output_dir = Path(output_dir) if output_dir else OUTPUT_DIR

    def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        resolution: str = "2K",
        model: str = DEFAULT_IMAGE_MODEL,
        save_local: bool = True
    ) -> Dict[str, Any]:
        """調用 Soul v2 生成高品質關鍵影格/起始圖像。"""
        import higgsfield_client

        args = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution
        }
        res = higgsfield_client.subscribe(model, arguments=args)
        
        # 取得圖片連結
        image_url = None
        if isinstance(res, dict) and "images" in res and len(res["images"]) > 0:
            image_url = res["images"][0].get("url")
            
        local_path = None
        if save_local and image_url:
            filename = f"img_{int(time.time())}.png"
            local_path = download_file(image_url, self.output_dir / filename)

        return {
            "raw": res,
            "url": image_url,
            "local_path": str(local_path) if local_path else None
        }

    def generate_video(
        self,
        prompt: str,
        image_url: Optional[str] = None,
        duration: int = 5,
        aspect_ratio: str = "16:9",
        model: str = DEFAULT_VIDEO_MODEL,
        save_local: bool = True
    ) -> Dict[str, Any]:
        """調用 Cinematic Studio 生成 Text-to-Video 或 Image-to-Video 動態影片。"""
        import higgsfield_client

        args = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration
        }
        if image_url:
            args["image_url"] = image_url

        res = higgsfield_client.subscribe(model, arguments=args)

        # 解析影片 URL
        video_url = None
        if isinstance(res, dict):
            video_url = res.get("video_url") or res.get("url")
            if not video_url and "videos" in res and len(res["videos"]) > 0:
                video_url = res["videos"][0].get("url")
        elif isinstance(res, str) and (res.startswith("http://") or res.startswith("https://")):
            video_url = res

        local_path = None
        if save_local and video_url:
            filename = f"video_{int(time.time())}.mp4"
            local_path = download_file(video_url, self.output_dir / filename)

        return {
            "raw": res,
            "url": video_url,
            "local_path": str(local_path) if local_path else None
        }
