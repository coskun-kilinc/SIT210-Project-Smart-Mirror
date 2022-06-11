import datetime
import os
from abc import ABC, abstractmethod
import spotipy
from spotipy.oauth2 import SpotifyOAuth

DEBUG = False

class GetCurrentTrack(ABC):
    @abstractmethod
    def get_current_track_info(self, debug=False):
        raise NotImplementedError

'''
Dummy music client, provides static track information for testing
'''
class DummyMusicClient(GetCurrentTrack):

    # overrides interface get_current_track method
    def get_current_track_info(self, debug=False):
        current_track_info =  {'track': 'Numb',
                               'artists': 'Linkin Park',
                               'duration': '03:05',
                               'progress': '01:42',
                               'image': {'height': 300,
                                          'url': 'https://i.scdn.co/image/ab67616d00001e02b4ad7ebaf4575f120eb3f193',
                                          'width': 300}}
        return current_track_info


'''
Spotify Client class, implements GetCurrentTrack interface
'''
class SpotifyClient(GetCurrentTrack):
    # parameters necessary for creating a spotify client
    # SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET are stored as environment variables, you must provide your own
    SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
    SCOPES = ['user-read-playback-state']
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = 'http://localhost:5000/'

    def __init__(self):   
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                                                            client_secret=self.SPOTIPY_CLIENT_SECRET,
                                                            redirect_uri=self.SPOTIPY_REDIRECT_URI,
                                                            scope=self.SCOPES))
    
    
    def get_current_track_info(self, debug=False):
        resp_json  = self.sp.current_playback()
        if resp_json != None:
            artists = resp_json['item']['artists']
            artists_name = ', '.join(
                [artist['name'] for artist in artists]
            )

            duration = str(datetime.timedelta(seconds=resp_json['item']['duration_ms']//1000))
            progress = str(datetime.timedelta(seconds=resp_json['progress_ms']//1000))

            current_track_info = {
                "track": resp_json['item']['name'],
                "artists": artists_name,
                "duration":  datetime.datetime.strptime(duration, '%H:%M:%S').strftime('%M:%S'),
                "progress":  datetime.datetime.strptime(progress, '%H:%M:%S').strftime('%M:%S'),
                "image": resp_json['item']['album']['images'][1] 
            }            
        else:
            current_track_info = {
                "track": '',
                "artists": '',
                "duration":  '00:00',
                "progress":  '00:00',
                "image": None
            }
        if DEBUG: print(current_track_info) 
        return current_track_info