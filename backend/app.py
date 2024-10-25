
from flask import Flask, redirect, jsonify, request, session
from applToSpotify import get_songs_from_apple
from urllib.parse import urlencode
from base64 import b64encode
from dotenv import load_dotenv
from flask_cors import CORS
import logging
import os
import requests

app = Flask(__name__)
CORS(app, support_credentials=True)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('backend.log')
file_handler.setLevel(logging.INFO)

# Set formatter for both handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add both handlers to the Flask logger
app.logger.addHandler(console_handler)
app.logger.addHandler(file_handler)

load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
app.secret_key = "super secret key"
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')

@app.route('/')
def index():
    s = "Hai :3 </br></br>"
    if session['spotify_token']:
        s += session['spotify_token']
    return s


@app.route('/get-playlist-songs/<playlist_id>')
def get_songs(playlist_id):
    app.logger.info(f"get-playlist-songs:{playlist_id}")
    tracks = get_songs_from_apple(playlist_id)
    app.logger.debug(f"Fetched album: {tracks['name']}")
    app.logger.debug(f"Number of tracks : {len(tracks['tracks'])}")
    
    return tracks


@app.route('/spotify-auth')
def save_spotify_auth():
    scope = 'playlist-modify-public playlist-modify-private ugc-image-upload'
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        # Ensure this matches Spotify Dashboard
        'redirect_uri': 'http://localhost:5000/callback',
    })
    return redirect(auth_url)


@app.route("/callback")
def get_token():

    token = request.args.get('code')
    if not token:
        return jsonify({"error": "No token found"}), 400

    payload = {
        'code': token,
        'redirect_uri': 'http://localhost:5000/callback',
        'grant_type': 'authorization_code'
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization':  'Basic ' + b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')
    }
    res = requests.post('https://accounts.spotify.com/api/token',
                        headers=headers, data=payload)

    if res.status_code == 200:
        session['spotify_token'] = res.json()['access_token']
        app.logger.debug(
            f"Fetched Spotify access token: {res.json()['access_token']}")
        
        # Return the token as JSON if successful
        
        return redirect(frontend_url)
    else:
        return jsonify({"error": "Failed to get Spotify token", "details": res.json()}), res.status_code


if __name__ == '__main__':
    app.run(debug=True)
