import os
from pathlib import Path
from dotenv import load_dotenv

# 載入 .env 檔
load_dotenv()

# 基本路徑配置
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "outputs"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# API 認證資訊
HF_KEY = os.getenv("HF_KEY", "")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

# 支援模型預設值
DEFAULT_IMAGE_MODEL = "higgsfield-ai/soul/v2/standard"
DEFAULT_VIDEO_MODEL = "higgsfield-ai/cinematic_studio_2_5"
