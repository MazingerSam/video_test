import os
import requests
from pathlib import Path
from typing import Optional

def download_file(url: str, output_path: Path, chunk_size: int = 8192) -> Path:
    """下載網路媒體資源至本機或 Colab 目錄。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
    return output_path

def is_colab() -> bool:
    """判斷目前執行環境是否為 Google Colab。"""
    try:
        import google.colab
        return True
    except ImportError:
        return False
