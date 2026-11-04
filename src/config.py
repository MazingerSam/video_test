import os
from pathlib import Path

# 基本路徑配置
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "outputs"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 預設開源模型識別碼 (HuggingFace)
DEFAULT_ANIMATEDIFF_MODEL = "SG161222/Realistic_Vision_V5.1_noVAE"
DEFAULT_ANIMATEDIFF_MOTION = "guoyww/animatediff-motion-adapter-v1-5-2"
DEFAULT_SVD_MODEL = "stabilityai/stable-video-diffusion-img2vid-xt"
