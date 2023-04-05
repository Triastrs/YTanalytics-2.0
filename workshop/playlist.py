import datetime
import os
from googleapiclient.discovery import build
import isodate


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self._total_duration = None

        api_key: str = os.getenv('YTapiKey')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist = youtube.playlists().list(id=self.playlist_id, part='contentDetails, snippet').execute()

        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist["items"][0]["id"]}'

        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)
                                               ).execute()

    def show_best_video(self):
        """метод находит самое популярное видео из плейлиста по количеству лайков, выдаёт ссылку"""
        video_likes = [int(likes['statistics']['likeCount']) for likes in self.video_response['items']]
        most_likes = max(video_likes)
        for i in self.video_response['items']:
            if i['statistics']['likeCount'] == str(most_likes):
                print(f'https://www.youtube.com/watch?v={i["id"]}')
                break

    @property
    def total_duration(self):
        """метод подсчитывает общую длительность всех видео из плейлиста"""
        timing_list = []
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            timing_list.append(duration)
        self._total_duration = sum(timing_list, datetime.timedelta())
        return self._total_duration


