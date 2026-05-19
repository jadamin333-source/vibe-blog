import anthropic
from config import CLAUDE_MODEL


def generate_blog_post(
    api_key: str,
    content: dict,
    youtube_video: dict,
) -> str:
    """Claude API를 이용해 네이버 블로그 글을 생성합니다."""
    client = anthropic.Anthropic(api_key=api_key)

    youtube_context = ""
    if youtube_video:
        youtube_context = f"""
[최송철TV 최신 영상 참고]
제목: {youtube_video.get('title', '')}
내용 요약: {youtube_video.get('description', '')}
스크립트: {youtube_video.get('transcript', '')[:1500]}
영상 링크: {youtube_video.get('url', '')}
"""

    prompt = f"""당신은 자담인 건강법을 전파하는 건강 블로그 전문 작가입니다.
아래 자료를 참고하여 네이버 블로그에 올릴 건강 정보 글을 작성해주세요.

[오늘의 자담인 건강법 핵심 원칙]
{content['principle']}

[실제 체험 사례]
{content['testimonials']}

{youtube_context}

다음 형식으로 작성해주세요:

제목: (흥미롭고 검색 친화적인 제목 — 숫자나 구체적 효과 포함)

[도입부]
독자의 공감을 끄는 이야기로 시작 (2~3문단)
오늘 다룰 주제를 자연스럽게 소개

[핵심 건강 정보]
오늘의 원칙을 쉽고 친근하게 설명
- 왜 중요한지
- 어떤 원리인지
- 실제 사례와 연결

[실천 체험 이야기]
위에 제공된 체험담 중 1~2가지를 감동적으로 소개
(이름과 구체적인 변화 내용 포함)

[오늘 바로 실천하는 법]
구체적이고 쉬운 방법 3가지 (리스트 형식)

[마무리]
따뜻하고 희망적인 마무리 (1~2문단)

해시태그: #자담인건강법 #장청몸청 #자연치유 #건강관리 #다이어트 #장건강 (관련 태그 6~10개)

주의사항:
- 네이버 블로그 독자 친화적 문체 (따뜻하고 친근하게)
- 전문 용어는 쉽게 풀어서 설명
- 총 1200~1800자 분량
- 자담인 건강법의 핵심인 '따뜻하게, 비우고, 자연으로' 정신 반영
"""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
