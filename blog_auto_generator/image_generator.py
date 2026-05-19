import os
import urllib.request
import urllib.error
import json
import logging

log = logging.getLogger(__name__)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"


def generate_blog_image(prompt_ko: str, output_path: str) -> bool:
    """이미지를 생성하고 output_path에 저장합니다.

    Stability AI API 키가 있으면 실제 이미지를 생성하고,
    없으면 이미지 프롬프트를 txt 파일로 저장합니다.
    """
    if STABILITY_API_KEY:
        return _generate_via_stability(prompt_ko, output_path)
    else:
        _save_prompt_only(prompt_ko, output_path)
        return False


def _generate_via_stability(prompt_ko: str, output_path: str) -> bool:
    """Stability AI API로 이미지를 생성합니다."""
    # 한국어 프롬프트를 영어로 보완 (핵심 키워드 추가)
    english_hint = (
        "Korean health blog illustration, warm and educational style, "
        "clean and friendly infographic, soft colors"
    )
    full_prompt = f"{prompt_ko}, {english_hint}"

    payload = json.dumps({
        "text_prompts": [
            {"text": full_prompt, "weight": 1.0},
            {"text": "blurry, dark, scary, medical horror", "weight": -1.0},
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "steps": 30,
        "samples": 1,
    }).encode("utf-8")

    req = urllib.request.Request(
        STABILITY_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        import base64
        image_data = base64.b64decode(result["artifacts"][0]["base64"])
        img_path = output_path.replace(".txt", ".png")
        with open(img_path, "wb") as f:
            f.write(image_data)
        log.info(f"이미지 생성 완료: {img_path}")
        return True
    except Exception as e:
        log.warning(f"이미지 생성 실패: {e}")
        _save_prompt_only(prompt_ko, output_path)
        return False


def _save_prompt_only(prompt_ko: str, output_path: str) -> None:
    """이미지 프롬프트를 파일로 저장합니다 (API 키 없을 때 대체 동작)."""
    prompt_path = output_path.replace(".txt", "_image_prompt.txt")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write("=== 블로그 이미지 프롬프트 ===\n\n")
        f.write("아래 프롬프트를 DALL-E, Midjourney, 또는 Stable Diffusion에 사용하세요.\n\n")
        f.write(f"[한국어 프롬프트]\n{prompt_ko}\n\n")
        f.write("[영어 프롬프트 힌트]\n")
        f.write(
            "Korean health blog illustration, warm educational style, "
            "friendly infographic, soft warm colors, clean design\n"
        )
        f.write("\n[Stability AI 이미지 자동 생성 방법]\n")
        f.write(".env 파일에 STABILITY_API_KEY=your_key 를 추가하세요.\n")
        f.write("https://platform.stability.ai/ 에서 API 키를 발급받을 수 있습니다.\n")
    log.info(f"이미지 프롬프트 저장: {prompt_path}")
