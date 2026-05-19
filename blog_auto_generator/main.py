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
from pdf_reader import get_content_for_blog
from youtube_fetcher import get_latest_video_content
from blog_generator import generate_blog_post

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
    log.info("블로그 글 생성 시작")

    # 1. 자담인 건강법 내용 로드
    content = get_content_for_blog()
    log.info(f"오늘의 원칙: {content['principle'][:40]}...")

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
    file_path = os.path.join(OUTPUT_DIR, f"blog_{date_str}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}\n")
        if youtube_video:
            f.write(f"참고 유튜브: {youtube_video.get('url', '')}\n")
        f.write("\n" + "=" * 60 + "\n\n")
        f.write(blog_content)

    log.info(f"파일 저장 완료: {file_path}")
    print(f"\n✓ 블로그 글이 저장되었습니다: {file_path}\n")


def main():
    # --now 옵션: 즉시 한 번 실행
    if "--now" in sys.argv:
        run_once()
        return

    log.info(f"자담인 블로그 자동 생성기 시작 — 매일 {SCHEDULE_TIME}에 실행됩니다.")
    schedule.every().day.at(SCHEDULE_TIME).do(run_once)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
