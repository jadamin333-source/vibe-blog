import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# 최송철TV 채널 ID (YouTube URL에서 확인)
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "UCxxxxxxxxxxxxxxxxxxxxxx")

# 자담인 건강법 PDF 경로
PDF_PATH = os.getenv("PDF_PATH", "자담인건강법.pdf")

# 출력 디렉토리
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# 스케줄 시간 (24시간 형식)
SCHEDULE_TIME = "09:30"

# Claude 모델
CLAUDE_MODEL = "claude-sonnet-4-6"
