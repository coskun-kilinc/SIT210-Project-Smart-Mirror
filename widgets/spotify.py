import datetime
import os
import requests

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
SPOTIFY_ACCESS_TOKEN = 'BQCv9WNWYHdnoesltItF6EKWmzJZhAALLAN7T2livcj1kcyQR0Qt9vDO882c5Cy5DmTu5OF6OjHQle7A8bok1adTkdHwIrj0SNNwrQ-Pp8oD4Gxcrwk46hj-9RwLWutZENN6EeSU_WMq0-BV-cub7osXRXruitk'


def get_current_track_info(access_token=SPOTIFY_ACCESS_TOKEN):
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
            "track": 'n/a',
            "artists": 'n/a',
            "duration":  'n/a',
            "progress":  'n/a',
            "percentage_complete": 'n/a'
        }

    return current_track_info


track_info = get_current_track_info()
print(track_info)