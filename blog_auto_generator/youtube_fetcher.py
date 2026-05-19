import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled


def get_latest_videos(api_key: str, channel_id: str, max_results: int = 3) -> list[dict]:
    """채널의 최신 영상 목록을 가져옵니다."""
    youtube = build("youtube", "v3", developerKey=api_key)

    # 채널의 업로드 플레이리스트 ID 조회
    channel_resp = youtube.channels().list(
        part="contentDetails",
        id=channel_id,
    ).execute()

    if not channel_resp.get("items"):
        raise ValueError(f"채널을 찾을 수 없습니다: {channel_id}")

    uploads_id = channel_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # 최신 영상 목록 조회
    playlist_resp = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_id,
        maxResults=max_results,
    ).execute()

    videos = []
    for item in playlist_resp.get("items", []):
        snippet = item["snippet"]
        video_id = snippet["resourceId"]["videoId"]
        videos.append({
            "video_id": video_id,
            "title": snippet["title"],
            "description": snippet.get("description", "")[:500],
            "published_at": snippet["publishedAt"],
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })

    return videos


def get_video_transcript(video_id: str, language: str = "ko") -> str:
    """YouTube 영상의 자막(스크립트)을 가져옵니다."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language, "ko-KR"])
        full_text = " ".join(entry["text"] for entry in transcript_list)
        # 최대 3000자로 제한
        return full_text[:3000]
    except (NoTranscriptFound, TranscriptsDisabled):
        return ""
    except Exception:
        return ""


def get_latest_video_content(api_key: str, channel_id: str) -> dict:
    """최신 영상의 제목, 설명, 자막을 합쳐서 반환합니다."""
    videos = get_latest_videos(api_key, channel_id, max_results=1)
    if not videos:
        return {}

    video = videos[0]
    transcript = get_video_transcript(video["video_id"])
    video["transcript"] = transcript
    return video
