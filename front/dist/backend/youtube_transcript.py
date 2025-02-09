from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeTranscriptFetcher:
    def __init__(self, video_id):
        self.video_id = video_id

    def get_transcript(self):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
            return [
                f"[{round(entry['start'], 2)}s] {entry['text']}" for entry in transcript
            ]
        except Exception as e:
            return {"error": str(e)}