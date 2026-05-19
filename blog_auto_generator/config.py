import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# YouTube Data API v3 키 (없으면 자담인 내용만으로 생성)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# 최송철TV 채널 ID
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "UCxxxxx")

# Stability AI API 키 (없으면 이미지 프롬프트만 저장)
# https://platform.stability.ai/ 에서 발급
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")

# 출력 디렉토리
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# 스케줄 시간 (24시간 형식)
SCHEDULE_TIME = "09:30"

# Claude 모델
CLAUDE_MODEL = "claude-sonnet-4-6"
