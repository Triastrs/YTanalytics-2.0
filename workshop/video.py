import os
from googleapiclient.discovery import build


class Video:

    def __init__(self, video_id):
        self.video_id = video_id

        self.video = self.get_api_object().videos().list(id=self.video_id, part='snippet,statistics').execute()
        try:
            self.video_name = self.video['items'][0]['snippet']['title']
            self.view_count = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']
        except Exception:
            self.video_name = None
            self.view_count = None
            self.like_count = None

    @staticmethod
    def get_api_object():
        """метод возвращает объект для работы с API ютуба"""
        api_key: str = os.getenv('YTapiKey')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        """выводит название видео"""
        return self.video_name
