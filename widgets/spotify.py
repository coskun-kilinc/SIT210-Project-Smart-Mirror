import datetime
from lib2to3.pgen2 import token
import os
import time
from tkinter.messagebox import NO
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from flask import Flask, request, url_for, session, redirect

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
SCOPES = ['user-read-playback-state']
SPOTIPY_CLIENT_ID = 'e29d40e8d4124cfc8deaaf2e49fe60af'
SPOTIPY_CLIENT_SECRET = '82021a98453448feb364930b425fd37e'
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/'

DEBUG = True

class SpotifyClient(object):
    def __init__(self):   
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                            client_secret=SPOTIPY_CLIENT_SECRET,
                                                            redirect_uri=SPOTIPY_REDIRECT_URI,
                                                            scope=SCOPES))

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



sp_c = SpotifyClient()
sp_c.get_current_track_info()