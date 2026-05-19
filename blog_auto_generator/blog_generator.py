import anthropic
from config import CLAUDE_MODEL


def generate_blog_post(
    api_key: str,
    pdf_excerpt: str,
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

    prompt = f"""당신은 건강 블로그 전문 작가입니다.
아래 두 가지 자료를 참고하여 네이버 블로그에 올릴 건강 정보 글을 작성해주세요.

[자담인 건강법 PDF 내용 발췌]
{pdf_excerpt}

{youtube_context}

다음 형식으로 작성해주세요:

제목: (흥미롭고 검색 친화적인 제목)

[서론]
독자의 관심을 끄는 도입부 (2~3문단)

[본문]
- 핵심 건강 정보 3~5가지 항목
- 각 항목마다 실천 방법 포함
- 자담인 건강법의 핵심 원리 반영

[실천 팁]
오늘 바로 실천할 수 있는 구체적인 방법 3가지

[마무리]
동기부여가 되는 마무리 문단

해시태그: #건강 #자담인건강법 #최송철TV #건강관리 #웰빙 (관련 태그 5~8개)

주의사항:
- 네이버 블로그 독자 친화적 문체로 작성
- 전문 의학 용어는 쉽게 풀어서 설명
- 총 1000~1500자 분량
- 따뜻하고 친근한 톤으로 작성
"""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
