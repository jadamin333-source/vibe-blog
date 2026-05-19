import os
import random

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

PRINCIPLES_FILE = os.path.join(DATA_DIR, "자담인건강법_핵심원칙.txt")
TESTIMONIALS_FILE = os.path.join(DATA_DIR, "자담인_체험담.txt")
JANGCHEONG_FILE = os.path.join(DATA_DIR, "장청몸청_핵심내용.txt")
JANGCHEONG_FULL_FILE = os.path.join(DATA_DIR, "장청몸청_전체내용.txt")
HAPPY3DAYS_FILE = os.path.join(DATA_DIR, "행복한3일_핵심내용.txt")
HAPPY3DAYS_FULL_FILE = os.path.join(DATA_DIR, "행복한3일_전체내용.txt")


def _read_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def _get_random_sections(path: str, n: int = 1) -> str:
    text = _read_file(path)
    sections = [s.strip() for s in text.split("■") if s.strip()]
    if not sections:
        # fall back to paragraph-based splitting for plain-text full content files
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 100]
        if not paragraphs:
            return text
        chosen = random.sample(paragraphs, min(n, len(paragraphs)))
        return "\n\n".join(chosen)
    chosen = random.sample(sections, min(n, len(sections)))
    return "\n\n".join("■ " + s for s in chosen)


def get_random_principle() -> str:
    """4개 원본 자료에서 랜덤으로 핵심 원칙 섹션을 반환합니다."""
    source = random.choice(["자담인건강법", "장청몸청", "장청몸청_전체", "행복한3일", "행복한3일_전체"])
    if source == "자담인건강법":
        text = _read_file(PRINCIPLES_FILE)
        sections = [s.strip() for s in text.split("■") if s.strip()]
        if sections:
            return "■ " + random.choice(sections)
    elif source == "장청몸청":
        return _get_random_sections(JANGCHEONG_FILE, 1)
    elif source == "장청몸청_전체":
        return _get_random_sections(JANGCHEONG_FULL_FILE, 1)
    elif source == "행복한3일":
        return _get_random_sections(HAPPY3DAYS_FILE, 1)
    else:
        return _get_random_sections(HAPPY3DAYS_FULL_FILE, 1)
    return _read_file(PRINCIPLES_FILE)


def get_random_testimonials(n: int = 2) -> str:
    """체험담 파일 또는 다른 자료에서 랜덤으로 n개의 사례를 반환합니다."""
    text = _read_file(TESTIMONIALS_FILE)
    stories = [s.strip() for s in text.split("■") if s.strip() and "체험담" not in s[:10]]

    # 장청몸청, 행복한3일 체험 섹션도 풀에 추가 (요약본 + 전체본)
    for fpath in [JANGCHEONG_FILE, JANGCHEONG_FULL_FILE, HAPPY3DAYS_FILE, HAPPY3DAYS_FULL_FILE]:
        extra = _read_file(fpath)
        for sec in extra.split("■"):
            sec = sec.strip()
            if sec and ("체험" in sec[:20] or "사례" in sec[:20]):
                stories.append(sec)

    if not stories:
        return text
    chosen = random.sample(stories, min(n, len(stories)))
    return "\n\n".join("■ " + s for s in chosen)


def get_content_for_blog() -> dict:
    """블로그 글 생성에 필요한 내용을 묶어서 반환합니다."""
    principle = get_random_principle()
    testimonials = get_random_testimonials(2)
    return {
        "principle": principle,
        "testimonials": testimonials,
    }
