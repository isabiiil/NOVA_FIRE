from flask import *
import requests
from realtimeEmotion import RealtimeEmotion
import json
import importlib
import requests
from os import environ, urandom
from .util.dbctrl import *
from .util.decorators import *
import datetime
import hashlib

app = Flask(__name__)
app.secret_key = "HELLO"

client_id = '9898308b60a845e29c2c8f3cc9ceaa5c'
client_secret = '0ff597f00bf341c8a51b2de30a8ec29f'
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
SPOTIFY_GET_AUDIO_FEATURES = 'https://api.spotify.com/v1/audio-features/'
SPOTIFY_GET_SIMILAR_SONGS = 'https://api.spotify.com/v1/recommendations'
SPOTIFY_ACCESS_TOKEN = 'BQD3wRsr5m1pSAUe7vaXT10C-K4z7hJ9zPWs8I4F6aBKXjVGhBLbBxueeN9WXBCUuzumvYUcIsBXOaWxx-iNoKxIuWucNF77eXYVr338GjhJOJ8VwYFy3ODUJ1qkWMhfMAiSQydL-ol-o4rruleFwcduanMiaczl_OdGOBsCPojP7ZT_FfamJaXVcHDE0s2eBhrgFUeEnltcCbJbNqP1cgL6gOdd-Yp9ArNFzBUathPhRmm6kYWpFXpVGyAYcpYq-DHJgZ2G4rXaVrr6Rg'
SPOTIFY_GET_REFRESH_TOKEN = 'https://accounts.spotify.com/api/token'


song = RealtimeEmotion(path="./Training Data/", songID=['62AuGbAkt8Ox2IrFFb8GKV', '2AwZsT3CGlfBngDeA9fAIy', '3yrSvpt2l1xhsV9Em88Pul', '6zC0mpGYwbNTpk9SKwh08f', '4YOJFyjqh8eAcbKFfv88mV', '0elmUoU7eMPwZX1Mw1MnQo', '4bHsxqR3GMrXTxEPLuK5ue', '4W4wYHtsrgDiivRASVOINL', '1JyaAeaXVFnVv5ikwWQVQ4', '1SAkL1mYNJlaqnBQxVZrRl', '7cyBw7bpAOYhzyNv7yqW6y'])

# song = '1TKYPzH66GwsqyJFKFkBHQ'

# def get_refresh_token():
#   response = requests.get(
#     SPOTIFY_GET_REFRESH_TOKEN,
#     headers = {p
#       "Authorization": "Basic " + (client_id + ":" + client_secret),
#       grant_type: 'refresh_token'
#     }
#   )
  
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

  url = f"https://api.spotify.com/v1/recommendations?seed_tracks={song}&limit=5&target_danceability={dance}&target_energy{energy}&target_key={key}&target_valence={valence}&target_tempo={tempo}&market=CA"
  
  response3 = requests.get(
    url,
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {access_token}"
    }   
  )
  resp3_json = response3.json()
  
  songs = {}
  for i in range(len(resp3_json['tracks'])):
    for j in range(4):
      songData = {}
      songData['songID'] = resp3_json['tracks'][i]['id']
      songData['songTitle'] = resp3_json['tracks'][i]['name']
      songData['songURL'] = resp3_json['tracks'][i]['external_urls']['spotify']
      songData['songArtist'] = resp3_json['tracks'][i]['artists'][0]['name']
      songData['releaseDate'] = resp3_json['tracks'][i]['album']['release_date']
    songs[i] = songData
      
  return songs

@app.route('/', methods=['GET'])
def home():
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
