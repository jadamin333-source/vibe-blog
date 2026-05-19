import os
import sys
import logging
import schedule
import time
from datetime import datetime

from config import (
    ANTHROPIC_API_KEY,
    YOUTUBE_API_KEY,
    YOUTUBE_CHANNEL_ID,
    OUTPUT_DIR,
    SCHEDULE_TIME,
)
from pdf_reader import get_content_for_blog, advance_chapter, get_current_chapter
from youtube_fetcher import get_latest_video_content
from blog_generator import generate_blog_post
from image_generator import generate_blog_image

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.path.join(os.path.dirname(__file__), "generator.log"),
            encoding="utf-8",
        ),
    ],
)
log = logging.getLogger(__name__)


def run_once():
    """블로그 글 한 편을 생성하고 파일로 저장합니다."""
    chapter = get_current_chapter()
    log.info(
        f"블로그 글 생성 시작 — "
        f"[{chapter['index']}편] {chapter['title']}"
    )

    # 1. 현재 챕터 기반으로 자담인 건강법 내용 로드
    content = get_content_for_blog()

    # 2. 최송철TV 최신 영상 가져오기
    youtube_video = {}
    if YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID and not YOUTUBE_CHANNEL_ID.startswith("UCxxx"):
        try:
            youtube_video = get_latest_video_content(YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID)
            if youtube_video:
                log.info(f"유튜브 영상 수집 완료: {youtube_video.get('title', '')}")
            else:
                log.warning("유튜브 영상을 가져오지 못했습니다. 자담인 내용만으로 생성합니다.")
        except Exception as e:
            log.warning(f"유튜브 오류 (자담인 내용만 사용): {e}")
    else:
        log.info("YouTube 미설정 — 자담인 건강법 내용만으로 블로그 글을 생성합니다.")

    # 3. Claude API로 블로그 글 생성
    try:
        blog_content = generate_blog_post(ANTHROPIC_API_KEY, content, youtube_video)
        log.info("블로그 글 생성 완료")
    except Exception as e:
        log.error(f"블로그 글 생성 실패: {e}")
        return

    # 4. 파일 저장
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    chapter_num = str(chapter["index"]).zfill(2)
    file_path = os.path.join(OUTPUT_DIR, f"ch{chapter_num}_{date_str}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"시리즈: 자담인 건강법 완전 정복\n")
        f.write(f"챕터: {chapter['index']}편 — {chapter['title']}\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}\n")
        if youtube_video:
            f.write(f"참고 유튜브: {youtube_video.get('url', '')}\n")
        f.write("\n" + "=" * 60 + "\n\n")
        f.write(blog_content)

    log.info(f"파일 저장 완료: {file_path}")

    # 5. 이미지 생성
    image_prompt = chapter.get("image_prompt", "자담인 건강법, 따뜻하고 자연스러운 건강 일러스트")
    image_generated = generate_blog_image(image_prompt, file_path)
    if image_generated:
        log.info("블로그 이미지 생성 완료")
    else:
        log.info("이미지 프롬프트 저장 완료 (STABILITY_API_KEY 설정 시 자동 생성)")

    # 6. 챕터 진행 (다음 실행 때 다음 챕터 사용)
    next_ch = advance_chapter()
    log.info(f"다음 실행 챕터: {next_ch}편")

    print(f"\n✓ [{chapter['index']}편] {chapter['title']}")
    print(f"  블로그 글: {file_path}")
    print(f"  다음 편: {next_ch}편\n")


def main():
    # --now 옵션: 즉시 한 번 실행
    if "--now" in sys.argv:
        run_once()
        return

    # --chapter N 옵션: 특정 챕터로 이동 후 실행
    if "--chapter" in sys.argv:
        idx = sys.argv.index("--chapter")
        if idx + 1 < len(sys.argv):
            from pdf_reader import load_progress, save_progress
            progress = load_progress()
            progress["current_chapter"] = int(sys.argv[idx + 1])
            save_progress(progress)
            log.info(f"챕터를 {sys.argv[idx + 1]}편으로 설정했습니다.")
        run_once()
        return

    log.info(f"자담인 블로그 자동 생성기 시작 — 매일 {SCHEDULE_TIME}에 실행됩니다.")
    log.info("시리즈: 자담인 건강법 완전 정복 (총 16편, 순서대로 작성)")
    schedule.every().day.at(SCHEDULE_TIME).do(run_once)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
