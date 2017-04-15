from __future__ import print_function
import sys
import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib

app = Flask(__name__)

# Client Keys
CLIENT_ID='fae8bfaa041c4f29836254363cf7979f'
CLIENT_SECRET='c432e92887de4acf88f5c299f8a455a8'

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server side Parameters
CLIENT_SIDE_URL ='http://4270a667.ngrok.io'
PORT = 8080
REDIRECT_URI = "{}/callback".format(CLIENT_SIDE_URL)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

authorization_header = {}

query_params = {
    "response_type" : "code",
    "redirect_uri" : REDIRECT_URI,
    "scope" : SCOPE,
    "client_id": CLIENT_ID,
    "show_dialog": SHOW_DIALOG_str
}

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/authorize")
def authorize():
	# Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, urllib.quote(val)) for key,val in query_params.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    global authorization_header

    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = playlist_data["items"]
    return render_template("indexAlt.html",sorted_array=display_arr)

@app.route("/playlist")
def playlist():
    global authorization_header
    print(authorization_header)
    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)
    # Get playlist id
    playlist_id = request.args.get("id")
    # Get playlist songs
    playlist_songs_api_endpoint = "{}/playlists/{}/tracks".format(profile_data["href"], playlist_id)
    playlist_songs_response = requests.get(playlist_songs_api_endpoint, headers=authorization_header)
    playlist_songs_data = json.loads(playlist_songs_response.text)
    return render_template("playlist.html", sorted_array=playlist_songs_data)

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
