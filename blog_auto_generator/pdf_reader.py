import os
import json
import random

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

PRINCIPLES_FILE = os.path.join(DATA_DIR, "자담인건강법_핵심원칙.txt")
TESTIMONIALS_FILE = os.path.join(DATA_DIR, "자담인_체험담.txt")
JANGCHEONG_FILE = os.path.join(DATA_DIR, "장청몸청_핵심내용.txt")
JANGCHEONG_FULL_FILE = os.path.join(DATA_DIR, "장청몸청_전체내용.txt")
HAPPY3DAYS_FILE = os.path.join(DATA_DIR, "행복한3일_핵심내용.txt")
HAPPY3DAYS_FULL_FILE = os.path.join(DATA_DIR, "행복한3일_전체내용.txt")
TOC_FILE = os.path.join(DATA_DIR, "자담인건강법_목차.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "blog_progress.json")


def _read_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def _get_random_sections(path: str, n: int = 1) -> str:
    text = _read_file(path)
    sections = [s.strip() for s in text.split("■") if s.strip()]
    if not sections:
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 100]
        if not paragraphs:
            return text
        chosen = random.sample(paragraphs, min(n, len(paragraphs)))
        return "\n\n".join(chosen)
    chosen = random.sample(sections, min(n, len(sections)))
    return "\n\n".join("■ " + s for s in chosen)


def load_toc() -> dict:
    """자담인건강법 목차 JSON을 로드합니다."""
    with open(TOC_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_progress() -> dict:
    """현재 진행 상황을 로드합니다."""
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_progress(progress: dict) -> None:
    """진행 상황을 저장합니다."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def get_current_chapter() -> dict:
    """현재 작성해야 할 챕터 정보를 반환합니다."""
    toc = load_toc()
    progress = load_progress()
    current_idx = progress.get("current_chapter", 1)
    total = toc["total_chapters"]

    # 모든 챕터를 다 썼으면 처음으로 순환
    if current_idx > total:
        current_idx = 1

    chapter = next(
        (c for c in toc["chapters"] if c["index"] == current_idx),
        toc["chapters"][0],
    )
    return chapter


def advance_chapter() -> int:
    """다음 챕터로 진행하고 새 챕터 번호를 반환합니다."""
    toc = load_toc()
    progress = load_progress()
    current = progress.get("current_chapter", 1)
    completed = progress.get("completed_chapters", [])

    if current not in completed:
        completed.append(current)

    next_chapter = current + 1
    if next_chapter > toc["total_chapters"]:
        next_chapter = 1

    from datetime import datetime
    progress["current_chapter"] = next_chapter
    progress["last_run"] = datetime.now().isoformat()
    progress["completed_chapters"] = completed
    save_progress(progress)
    return next_chapter


def get_principle_for_chapter(chapter: dict) -> str:
    """챕터 주제에 맞는 핵심 원칙 내용을 반환합니다."""
    topic_key = chapter.get("topic_key", "")
    source_section = chapter.get("source_section", "")

    # 자담인건강법 핵심원칙 파일에서 해당 섹션 찾기
    principles_text = _read_file(PRINCIPLES_FILE)
    sections = [s.strip() for s in principles_text.split("■") if s.strip()]

    # source_section의 키워드로 가장 관련 있는 섹션 찾기
    topic_words = topic_key.replace("_", " ").split()
    best_section = None
    best_score = 0
    for sec in sections:
        score = sum(1 for w in topic_words if w in sec)
        if score > best_score:
            best_score = score
            best_section = sec

    if best_section and best_score > 0:
        return "■ " + best_section

    # 장청몸청 / 행복한3일에서도 관련 내용 검색
    for fpath in [JANGCHEONG_FILE, HAPPY3DAYS_FILE, JANGCHEONG_FULL_FILE]:
        text = _read_file(fpath)
        secs = [s.strip() for s in text.split("■") if s.strip()]
        for sec in secs:
            score = sum(1 for w in topic_words if w in sec)
            if score > best_score:
                best_score = score
                best_section = sec

    return ("■ " + best_section) if best_section else _get_random_sections(PRINCIPLES_FILE, 1)


def get_random_testimonials(n: int = 2) -> str:
    """체험담 파일에서 랜덤으로 n개의 사례를 반환합니다."""
    text = _read_file(TESTIMONIALS_FILE)
    stories = [s.strip() for s in text.split("■") if s.strip() and "체험담" not in s[:10]]

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
    """현재 챕터 기반으로 블로그 글 생성에 필요한 내용을 반환합니다."""
    chapter = get_current_chapter()
    principle = get_principle_for_chapter(chapter)
    testimonials = get_random_testimonials(2)
    return {
        "chapter": chapter,
        "principle": principle,
        "testimonials": testimonials,
    }
