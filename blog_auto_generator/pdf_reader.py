import os
import random
import pdfplumber


def extract_pdf_content(pdf_path: str) -> str:
    """PDF에서 전체 텍스트를 추출합니다."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        total_pages = len(pages)
        texts = []
        for page in pages:
            text = page.extract_text()
            if text:
                texts.append(text.strip())

    return "\n\n".join(texts), total_pages


def get_random_excerpt(pdf_path: str, num_chars: int = 2000) -> str:
    """PDF에서 랜덤 구간의 내용을 추출합니다 (매일 다른 주제 생성용)."""
    full_text, _ = extract_pdf_content(pdf_path)

    if len(full_text) <= num_chars:
        return full_text

    # 랜덤 시작점 (문장 단위로 끊기 위해 공백 기준)
    max_start = len(full_text) - num_chars
    start = random.randint(0, max_start)

    # 문장 시작점 찾기
    while start > 0 and full_text[start] not in ". \n":
        start -= 1

    excerpt = full_text[start : start + num_chars].strip()
    return excerpt
