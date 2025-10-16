from google.adk.agents import LlmAgent
from models import deepseek_model
from tools import ghost
from utilities import load_instruction
import os, time, mimetypes, requests, jwt

GHOST_URL = os.environ["GHOST_API_URL"].rstrip("/")
ADMIN_KEY = os.environ["GHOST_ADMIN_API_KEY"]


def _admin_jwt(aud="/admin/") -> str:
    key_id, secret = ADMIN_KEY.split(":")
    iat = int(time.time())
    payload = {"iat": iat, "exp": iat + 5 * 60, "aud": aud}
    return jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers={"kid": key_id})


def _guess_name_and_mime(src_url: str, content_type: str | None) -> tuple[str, str]:
    mime = (content_type or "").split(";")[0].strip() if content_type else ""
    if not mime:
        mime = mimetypes.guess_type(src_url)[0] or "image/png"
    ext = mimetypes.guess_extension(mime) or ".png"
    name = os.path.basename(src_url.split("?")[0]) or f"feature{ext}"
    if not os.path.splitext(name)[1]:
        name += ext
    return name, mime


def upload_image_from_url(src_url: str) -> str:
    r = requests.get(src_url, timeout=60)
    r.raise_for_status()
    content = r.content
    filename, mime = _guess_name_and_mime(src_url, r.headers.get("content-type"))
    token = _admin_jwt()
    files = {
        "file": (filename, content, mime),
    }
    u = f"{GHOST_URL}/ghost/api/admin/images/upload/"
    resp = requests.post(u, headers={"Authorization": f"Ghost {token}"}, files=files, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    print(data)

    image_url = data.get("images", [{}])[0].get("url") or data.get("url")
    if not image_url:
        raise RuntimeError(f"Unexpected upload response: {data}")
    return image_url


def _headers():
    return {"Authorization": f"Ghost {_admin_jwt()}", "Content-Type": "application/json"}


def _get_post_min(post_id: str) -> dict:
    url = f"{GHOST_URL}/ghost/api/admin/posts/{post_id}/?fields=id,updated_at,feature_image"
    r = requests.get(url, headers=_headers(), timeout=30)
    r.raise_for_status()
    posts = r.json().get("posts", [])
    if not posts:
        raise RuntimeError(f"Post not found: {post_id}")
    return posts[0]


def update_feature_image_with_lock(post_id: str, image_url: str, max_retries: int = 2) -> dict:
    """
    Updates feature_image with optimistic lock.
    Fetches latest updated_at, PUTs the change.
    """
    url = f"{GHOST_URL}/ghost/api/admin/posts/{post_id}/"
    last_err = None
    for attempt in range(max_retries + 1):
        post = _get_post_min(post_id)
        payload = {"posts": [{"id": post_id, "feature_image": image_url, "updated_at": post["updated_at"]}]}
        r = requests.put(url, headers=_headers(), json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 409:
            last_err = r
            continue
        try:
            body = r.json()
        except Exception:
            body = r.text
        raise requests.HTTPError(f"Ghost update failed ({r.status_code}): {body}", response=r)
    # If we exhausted retries, raise the last 409 with its body
    try:
        body = last_err.json()
    except Exception:
        body = last_err.text if last_err is not None else "(no response)"
    raise requests.HTTPError(f"Ghost update still conflicts after {max_retries + 1} attempts: {body}",
                             response=last_err)


def set_post_feature_image_from_remote(post_id: str, src_url: str) -> dict:
    ghost_url = upload_image_from_url(src_url)
    return update_feature_image_with_lock(post_id, ghost_url)


publish_agent = LlmAgent(
    name="publish_agent",
    model=deepseek_model.terminus,
    description=(
        "Agent to write prompt and generate a cover photo for the approved article"
    ),
    instruction=load_instruction('configs/publish.md'),
    tools=[
        ghost.ghost_toolset,
        set_post_feature_image_from_remote
    ],
    output_key="cover_photo_url",
)
