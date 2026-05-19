import os
import random

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

PRINCIPLES_FILE = os.path.join(DATA_DIR, "자담인건강법_핵심원칙.txt")
TESTIMONIALS_FILE = os.path.join(DATA_DIR, "자담인_체험담.txt")

# 핵심 원칙 섹션 목록
PRINCIPLES_SECTIONS = [
    "생명의 기원",
    "소화력은 자동차의 연비",
    "혈액의 질",
    "오토파지와 아포토시스",
    "질병의 주범",
    "호르몬의 교란",
    "건강식의 오해",
    "8가지 원칙 로드맵",
    "장청뇌청",
]


def _read_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def get_random_principle() -> str:
    """핵심 원칙 파일에서 랜덤 섹션을 반환합니다."""
    text = _read_file(PRINCIPLES_FILE)
    # ■ 로 구분된 섹션을 분리
    sections = [s.strip() for s in text.split("■") if s.strip()]
    if not sections:
        return text
    return "■ " + random.choice(sections)


def get_random_testimonials(n: int = 2) -> str:
    """체험담 파일에서 랜덤으로 n개의 사례를 반환합니다."""
    text = _read_file(TESTIMONIALS_FILE)
    stories = [s.strip() for s in text.split("■") if s.strip() and "체험담" not in s[:10]]
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
