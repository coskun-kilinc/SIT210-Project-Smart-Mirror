import requests
import os

# READ_API_KEY=os.getenv('THINGSPEAK_READ_API_KEY')
# CHANNEL_ID=os.getenv('THINGSPEAK_CHANNEL_ID')

READ_API_KEY = os.getenv('READ_API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID')


def read_feeds(feeds: int) -> list:
    resp_json = requests.get(
        url=f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results={feeds}").json()
    feeds = []
    for feed in resp_json['feeds']:
        feeds.append({
            "created_at": feed['created_at'],
            "entry_id": feed['entry_id'],
            "field1": feed['field1'],
            "field2": feed['field2']
        })
    return feeds
