import anthropic
from config import CLAUDE_MODEL

TOTAL_CHAPTERS = 16


def generate_blog_post(
    api_key: str,
    content: dict,
    youtube_video: dict,
) -> str:
    """Claude API를 이용해 교육적인 네이버 블로그 글을 생성합니다."""
    client = anthropic.Anthropic(api_key=api_key)

    chapter = content.get("chapter", {})
    chapter_index = chapter.get("index", 1)
    chapter_title = chapter.get("title", "자담인 건강법")
    next_index = chapter_index + 1 if chapter_index < TOTAL_CHAPTERS else 1

    youtube_context = ""
    if youtube_video:
        youtube_context = f"""
[최송철TV 최신 영상 참고]
제목: {youtube_video.get('title', '')}
내용 요약: {youtube_video.get('description', '')}
스크립트: {youtube_video.get('transcript', '')[:1500]}
영상 링크: {youtube_video.get('url', '')}
"""

    prompt = f"""당신은 자담인 건강법을 쉽고 친근하게 전파하는 건강 교육 전문 블로거입니다.
건강에 대해 아무것도 모르는 초보자도 완전히 이해할 수 있도록 자세하고 친절하게 설명해야 합니다.

(참고 자료: 자담인건강법, 장청몸청, 행복한3일평생건강다이어트, 자담인공저체험담)

【오늘의 시리즈 정보】
시리즈: 자담인 건강법 완전 정복 ({chapter_index}/{TOTAL_CHAPTERS}편)
오늘의 주제: {chapter_title}

[오늘의 핵심 건강 원칙]
{content['principle']}

[실제 체험 사례]
{content['testimonials']}

{youtube_context}

다음 형식으로 작성해주세요:

제목: 【자담인 건강법 {chapter_index}편】 {chapter_title}

🗂️ [시리즈 안내]
이 글은 '자담인 건강법 완전 정복' 시리즈 {chapter_index}번째 편입니다.
처음 오신 분도 바로 이해할 수 있도록 기초부터 설명합니다. (2문장)

💬 [도입부 — 이런 경험 있으신가요?]
많은 분들이 겪는 일상적인 건강 고민으로 시작 (2~3문단)
"혹시 이런 경험 있으신가요?" 형식으로 독자의 마음을 열기
오늘 다룰 주제가 왜 중요한지 자연스럽게 연결

🔬 [기초 지식 — 초보자도 이해하는 과학]
핵심 개념을 초등학생도 이해할 수 있는 비유로 설명
전문 용어가 나오면 반드시 괄호 안에 쉬운 말로 풀어 설명
예) "오토파지(자가포식 — 세포가 스스로 청소하는 것)"
단계별로 원리를 설명 (최소 3단계, 각 단계 충분히 설명)

🌿 [자담인 건강법의 관점]
자담인 건강법에서는 이 주제를 어떻게 다루는지
'따뜻하게, 비우고, 자연으로' 철학과 연결
실생활에서 이 원리가 어떻게 작동하는지

✨ [실제 변화 사례]
제공된 체험담에서 오늘 주제와 가장 관련 있는 사례 1~2개 소개
구체적인 수치와 변화 내용 포함 (몇 kg 감량, 약 끊음 등)
독자에게 희망을 주는 따뜻한 서술

✅ [오늘부터 바로 실천하는 방법]
구체적이고 실천 가능한 방법 4~5가지 (번호 목록)
각 방법에 "왜 효과가 있는지" 한 줄 이유 포함
초보자가 당장 시작할 수 있는 가장 쉬운 것부터 순서대로

❓ [자주 묻는 질문 & 주의사항]
이 원칙을 실천할 때 흔히 하는 실수 2~3가지 Q&A 형식

🎯 [마무리 & 다음 편 예고]
오늘 핵심 3줄 요약
다음 편 예고 한 줄 ({next_index}편 주제 힌트)
따뜻하고 격려하는 마무리

해시태그: #자담인건강법 #장청몸청 #자연치유 #건강교육 #건강초보자 (관련 태그 총 10~12개)

작성 원칙:
- 전문 용어는 반드시 괄호로 쉬운 말 풀이 추가
- 비유를 풍부하게 사용 (자동차, 요리, 청소 등 일상적 비유)
- 친근하고 따뜻한 말투 (독자를 가족처럼 대하는 느낌)
- 총 2000~2500자 분량
- 절대 어렵게 쓰지 않기 — "건강 초보자도 완전히 이해해야 한다"가 기준
- 자담인 건강법의 핵심인 '따뜻하게, 비우고, 자연으로' 정신 반영
"""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=3500,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
