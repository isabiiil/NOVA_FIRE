from flask import *
import requests
# from realtimeEmotion import RealtimeEmotion
# import json
# import importlib
# import requests
# from os import environ, urandom
# from .util.dbctrl import *
# from .util.decorators import *
# import datetime
# import hashlib

app = Flask(__name__)
app.secret_key = "HELLO"

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
SPOTIFY_GET_AUDIO_FEATURES = 'https://api.spotify.com/v1/audio-features/'
SPOTIFY_GET_SIMILAR_SONGS = 'https://api.spotify.com/v1/recommendations'
SPOTIFY_ACCESS_TOKEN = 'BQCzxOjda5PCqGL02wkyRlJ4war2zTRE4BTf2uPRUCRu3nwNBvYdpritlIbCgCW9r5L82p-Anpaa7ldGj8QzvaZHrW0ZFya7yYxilEopYGKDOzifJb2GfcZZoyqgKyIUtD2-KYGwVvTJZ-NQiP2b2iCFS6N9q2Ua3-Wnfa7UonPwnzvN-ceO0c-Mh6U2vW0ZecK1kVwCvUyQ7IQny6sPzHcDlQUu1iCWUL0PXjm01SmumVfkofeGYMxGGpSfRxntyfI7Q08geuJM2JKWdwtiOg'

# song = RealtimeEmotion(songID=['1TKYPzH66GwsqyJFKFkBHQ', '4iMO20EPodreIaEl8qW66y'])

song = '1TKYPzH66GwsqyJFKFkBHQ'

# def get_current_track(access_token):
#     response = requests.get(
#         SPOTIFY_GET_CURRENT_TRACK_URL,
#         headers={
#             "Authorization": f"Bearer {access_token}"
#         }
#     )
#     resp_json = response.json()

#     track_id = resp_json['id']
#     track_name = resp_json['name']
#     artists = resp_json['artists']
#     artists_name = ', '.join(
#         [artist['name'] for artist in artists]
#     )
#     link = resp_json['external_urls']['spotify']
    
#     current_track_info = {
#         "id": track_id,
#         "name": track_name,
#         "artists": artists_name,
#         "link": link
#     }

#     return current_track_info

def get_audio_features(access_token, song):
  response2 = requests.get(
    SPOTIFY_GET_AUDIO_FEATURES + song,
    headers = {
      "Authorization": f"Bearer {access_token}"
    }   
  )
  resp2_json = response2.json()

  track_danceability = resp2_json['danceability']
  track_energy = resp2_json['energy']
  track_key = resp2_json['key']
  track_valence = resp2_json['valence']
  track_tempo = resp2_json['tempo']
  
  current_audio_features = {
    "danceability": track_danceability,
    "energy": track_energy,
    "key": track_key,
    "valence": track_valence,
    "tempo": track_tempo,
  }
  
  return current_audio_features

def similar_song(access_token, song, current_audio_features):
  
  response3 = requests.get(
    SPOTIFY_GET_SIMILAR_SONGS,
    # seed_tracks = song,
    # target_danceability = current_audio_features['danceability'], 
    # target_energy = current_audio_features['energy'],
    # target_key = current_audio_features['key'],
    # target_valence = current_audio_features['valence'],
    # target_tempo = current_audio_features['tempo'],
    headers = {
      "Authorization": f"Bearer {access_token}"
    }   
  )
  resp3_json = response3.json()
  songData = {}
  for i in range(len(resp3_json['tracks'])):
    songData[i]['songID'] = resp3_json['tracks']['id']
    songData[i]['songTitle'] = resp3_json['tracks']['name']
    songData[i]['songURL'] = resp3_json['tracks']['external_urls']['spotify']
      
  return songData

@app.route('/', methods=['GET'])
def home():
  flash('aaron')
  # current_track_info = get_current_track(
  #   SPOTIFY_ACCESS_TOKEN
  # )
  current_audio_features = get_audio_features(
    SPOTIFY_ACCESS_TOKEN, song
  )
  current_song_data = similar_song(
    SPOTIFY_ACCESS_TOKEN, song, current_audio_features
  )
  flash(current_audio_features)
  return render_template('home.html')

if __name__ == "__main__":
	app.run(debug=True)

  