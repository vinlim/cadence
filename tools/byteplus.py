import base64
import mimetypes
import os, httpx, time
from typing import Dict, Any

ARK_API_KEY = os.environ["ARK_API_KEY"]
BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"

def _to_data_url(path: str) -> str:
    """Read a PNG/JPEG file and return a data: URL with base64 content."""
    mime = mimetypes.guess_type(path)[0] or "image/png"
    if mime not in ("image/png", "image/jpeg"):
        raise ValueError(f"Unsupported image type {mime}; only png/jpeg allowed.")
    if os.path.getsize(path) > 10 * 1024 * 1024:
        raise ValueError("Image must be <= 10MB.")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")  # no newlines
    return f"data:{mime};base64,{b64}"

def _post_json(payload: Dict, retries: int = 2) -> Any | None:
    for i in range(retries + 1):
        try:
            r = httpx.post(
                BASE_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {ARK_API_KEY}",
                },
                json=payload,
                timeout=60,
            )
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError:
            if i == retries:
                raise
            time.sleep(2 ** i)
    return None


def byteplus_generate(
    prompt: str,
) -> Dict:
    """
    Generate an image via BytePlus ARK.
    Returns: {"images":[{"url": str}], "provider":"byteplus","model": str}
    """
    model = "seedream-4-0-250828"
    data = _post_json({
        "model": model,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": "2K",
        "stream": False,
        "watermark": False,
        "image": _to_data_url('configs/example.png')
    })

    urls = [it["url"] for it in data.get("data", []) if "url" in it] or data.get("urls", [])
    return {"images": [{"url": u} for u in urls], "provider": "byteplus", "model": model}
