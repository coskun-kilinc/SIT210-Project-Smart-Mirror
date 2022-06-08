import datetime
import os
import requests

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
SPOTIFY_ACCESS_TOKEN = 'BQDDJXH7IqyATXrGm8HptslQ38KkaB6mmsPYgbjIjM_-LWFSDiKYr09yMYK6rZebcSqWH7PXk9CAPOsn_4ME21Cr4XWcimVNUrUFWd__ZtGYniAiTEzyjPRONeSsuTKsIcCFR2DoCF2eR7ROwmJ5x8O10berKLM'


def get_current_track_info(access_token=SPOTIFY_ACCESS_TOKEN, debug=False):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    try:
        resp_json = response.json()
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
            "percentage_complete": round(resp_json['progress_ms']/resp_json['item']['duration_ms'], 2)
        }
    except:
        current_track_info = {
            "track": ' ',
            "artists": ' ',
            "duration":  '00:00',
            "progress":  '00:00',
            "percentage_complete": '00:00/00:00'
        }
    if debug: print(current_track_info)
    return current_track_info
