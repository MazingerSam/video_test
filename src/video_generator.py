import time
from pathlib import Path
from typing import Optional, List
from PIL import Image
from .config import OUTPUT_DIR, DEFAULT_ANIMATEDIFF_MODEL, DEFAULT_ANIMATEDIFF_MOTION, DEFAULT_SVD_MODEL

class OpenSourceVideoWorkflow:
    """完全免金鑰、開源 AI 影片生成工作流 (AnimateDiff + Stable Video Diffusion)."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else OUTPUT_DIR

    def generate_text_to_video(
        self,
        prompt: str,
        negative_prompt: str = "bad quality, blurry, deformed, watermark",
        num_frames: int = 16,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 25,
        save_path: Optional[Path] = None
    ) -> Path:
        """使用 AnimateDiff 進行文字轉影片 (Text-to-Video)。"""
        import torch
        from diffusers import AnimateDiffPipeline, MotionAdapter, DDIMScheduler
        from diffusers.utils import export_to_video

        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        # 載入 Motion Adapter 與主 Pipeline
        adapter = MotionAdapter.from_pretrained(DEFAULT_ANIMATEDIFF_MOTION, torch_dtype=dtype)
        pipe = AnimateDiffPipeline.from_pretrained(
            DEFAULT_ANIMATEDIFF_MODEL,
            motion_adapter=adapter,
            torch_dtype=dtype
        )
        pipe.scheduler = DDIMScheduler.from_config(
            pipe.scheduler.config,
            beta_schedule="linear",
            clip_sample=False,
            timestep_spacing="linspace",
            steps_offset=1
        )

        # 顯存優化 (Colab T4 友好)
        if torch.cuda.is_available():
            if hasattr(pipe, "vae") and hasattr(pipe.vae, "enable_slicing"):
                pipe.vae.enable_slicing()
            elif hasattr(pipe, "enable_vae_slicing"):
                pipe.enable_vae_slicing()

            if hasattr(pipe, "enable_model_cpu_offload"):
                pipe.enable_model_cpu_offload()
            else:
                pipe.to(device)

        output = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_frames=num_frames,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=torch.Generator(device=device).manual_seed(42)
        )
        frames = output.frames[0]

        if not save_path:
            save_path = self.output_dir / f"animatediff_{int(time.time())}.mp4"

        export_to_video(frames, str(save_path), fps=8)
        return save_path

    def generate_image_to_video(
        self,
        image: Image.Image,
        num_frames: int = 14,
        fps: int = 7,
        motion_bucket_id: int = 127,
        decode_chunk_size: int = 8,
        save_path: Optional[Path] = None
    ) -> Path:
        """使用 Stable Video Diffusion (SVD) 進行圖片轉影片 (Image-to-Video)。"""
        import torch
        from diffusers import StableVideoDiffusionPipeline
        from diffusers.utils import export_to_video

        dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        pipe = StableVideoDiffusionPipeline.from_pretrained(
            DEFAULT_SVD_MODEL,
            torch_dtype=dtype,
            variant="fp16" if torch.cuda.is_available() else None
        )

        # 顯存優化
        if torch.cuda.is_available():
            if hasattr(pipe, "vae") and hasattr(pipe.vae, "enable_slicing"):
                pipe.vae.enable_slicing()
            elif hasattr(pipe, "enable_vae_slicing"):
                pipe.enable_vae_slicing()

            if hasattr(pipe, "enable_model_cpu_offload"):
                pipe.enable_model_cpu_offload()
            else:
                pipe.to("cuda")

        # 調整圖片尺寸為 1024x576 (SVD 最佳長寬比)
        image = image.resize((1024, 576))

        generator = torch.manual_seed(42)
        frames = pipe(
            image,
            decode_chunk_size=decode_chunk_size,
            generator=generator,
            motion_bucket_id=motion_bucket_id,
            num_frames=num_frames
        ).frames[0]

        if not save_path:
            save_path = self.output_dir / f"svd_{int(time.time())}.mp4"

        export_to_video(frames, str(save_path), fps=fps)
        return save_path
