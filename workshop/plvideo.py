import os
from googleapiclient.discovery import build
from workshop.video import Video


class PLVideo(Video):

    def __init__(self, video_id, pl_id):
        self.pl_id = pl_id
        super().__init__(video_id)

        self.pl = self.get_api_object().playlists().list(id=self.pl_id, part='contentDetails,snippet').execute()

        self.pl_name = self.pl['items'][0]['snippet']['title']

    def __str__(self):
        """выводит название видео и название плейлиста"""
        return f'{self.video_name} ({self.pl_name})'
