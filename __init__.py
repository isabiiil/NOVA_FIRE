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
SPOTIFY_ACCESS_TOKEN = 'BQAt1dKJzyOxfnb6VmprNozQwx5uWCtphszWunlj8TC1_LhJ71T-TSIAgkOUdU4AWtFvsT9dIsfXmahdB_g70hSeqhlAwYRXT6hPL6LpOJa9-G_5gbNwwucKVZ1HJns8Jy7e5FIps3-g5Okyzn-L3BfIi1kPz97Vkwld_5LHBcjKI0GFCiFjLAuh-QpnMnVu4nSm7VPlrV7Twby_AsmgA29KeapCXtdrKQ4Z4w5j6QlokglmR3ZJqtaK_4kacBOLJhoAFaOLX6EXdTSYz6RTaA'

# song = RealtimeEmotion(songID=['1TKYPzH66GwsqyJFKFkBHQ', '4iMO20EPodreIaEl8qW66y'])

song = '1TKYPzH66GwsqyJFKFkBHQ'

# def get_current_track(access_token):
#     response = requests.get(
#         SPOTIFY_GET_CURRENT_TRACK_URL,
#         headers={
#             "Content-Type": "application/json",
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
      "Content-Type": "application/json",
      "Authorization": f"Bearer {access_token}"
    }   
  )
  resp2_json = response2.json()

  current_audio_features = {
    "danceability": resp2_json['danceability'],
    "energy": resp2_json['energy'],
    "key": resp2_json['key'],
    "valence": resp2_json['valence'],
    "tempo": resp2_json['tempo'],
  }
  
  return current_audio_features

def similar_song(access_token, song, current_audio_features):
  dance = current_audio_features['danceability']
  energy = current_audio_features['energy']
  key = current_audio_features['key']
  valence = current_audio_features['valence']
  tempo = current_audio_features['tempo']

  url = f"https://api.spotify.com/v1/recommendations?seed_tracks={song}&limit=5&target_danceability={dance}&target_energy{energy}&target_key={key}&target_valence={valence}&target_tempo={tempo}"
  
  response3 = requests.get(
    # SPOTIFY_GET_SIMILAR_SONGS,
    url,
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {access_token}"
    }   
  )
  resp3_json = response3.json()
  songData = {}
  for i in range(len(resp3_json['tracks'])):
    songData.append(0)
    songData[i]['songID'] = resp3_json['tracks'][i]['id']
    songData[i]['songTitle'] = resp3_json['tracks'][i]['name']
    songData[i]['songURL'] = resp3_json['tracks'][i]['external_urls']['spotify']
      
  return songData
  # return resp3_json['tracks'][0]['id']

@app.route('/', methods=['GET'])
def home():
  # flash('aaron')
  # current_track_info = get_current_track(
  #   SPOTIFY_ACCESS_TOKEN
  # )
  current_audio_features = get_audio_features(
    SPOTIFY_ACCESS_TOKEN, song
  )
  current_song_data = similar_song(
    SPOTIFY_ACCESS_TOKEN, song, current_audio_features
  )
  flash(current_song_data)
  return render_template('home.html')

if __name__ == "__main__":
	app.run(debug=True)

  