from __future__ import print_function
import sys
import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib
import copy

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
ids = []
sortedIds = []

query_params = {
    "response_type" : "code",
    "redirect_uri" : REDIRECT_URI,
    "scope" : SCOPE,
    "client_id": CLIENT_ID,
    "show_dialog": SHOW_DIALOG_str
}

def sortPeakSupport(attrValues):
        """
        Function: Sorts into a Peak shape.
        Returns: (List of) New order of values passed in.
        """

        count = 0
        z = copy.deepcopy(attrValues)
        z.sort()
        attrValuesHalf1 = []
        attrValuesHalf2 = []

        for i in range(len(z)):
                if count % 2:
                        attrValuesHalf1.append(z[-1])
                else:
                        attrValuesHalf2.append(z[-1])

                z.remove(z[-1])
                count+=1

        attrValuesHalf2 = attrValuesHalf2[::-1]
        z = attrValuesHalf2 + attrValuesHalf1

        return z


#-----------------------------------------------------------------------#


def sortPeakFunc(songIDs, attrValues):
        """
        Function: Sorts into a Peak shape.
        Returns: (List of) New order of song keys.
        """

        d = dict(zip(attrValues, songIDs))
        attrValuesMod = sortPeakSupport(attrValues)
        songIDsMod = []

        for i in range(len(attrValuesMod)):
                songIDsMod.append(d.get(attrValuesMod[i]))

        print(str(attrValuesMod))
        print(str(songIDsMod))
        return songIDsMod

def sortToGreatestFunc(songIDs, attrValues):
        """
        Function: Sorts to increasing value.
        Returns: (List of) New order of song keys.
        """
        d = dict(zip(attrValues, songIDs))
        attrValuesMod = list(sorted(attrValues))
        songIDsMod = []

        for i in range(len(attrValuesMod)):
                songIDsMod.append(d.get(attrValuesMod[i]))

        print(str(attrValuesMod))
        print(str(songIDsMod))
        return songIDsMod

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    f = open('helloworld.html','w')

    message = """<html>
    <head></head>
    <body><p>Hello World!</p></body>
    </html>"""

    f.write(message)
    f.close()
    return render_template("helloworld.html")

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

@app.route("/playlist", methods=['GET', 'POST'])
def playlist():
    global authorization_header, ids, sortedIds
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

    ids = []
    for item in playlist_songs_data["items"]:
        ids.append(item["track"]["id"])
        sys.stderr.write(str(item["track"]["id"]) + '\n')
    display_arr = playlist_songs_data["items"]
    return render_template("playlist.html", sorted_array=display_arr)


@app.route("/sort", methods=['GET', 'POST'])
def sort():
    if (request.method == 'GET'):
        return render_template("pickSortMethod.html")
    elif (request.method == 'POST'):
        global sortedIds
        global authorization_header
        global ids
        attribute = request.form['Attribute']
        method = request.form['Method']
        track_ids = str(ids[0])
        for i in range(len(ids)-1):
            track_ids += "," + str(ids[i+1])
        audio_features_endpoint = "{}/audio-features?ids={}".format(SPOTIFY_API_URL, track_ids)
        audio_features_response = requests.get(audio_features_endpoint, headers=authorization_header)
        audio_features_response_data = json.loads(audio_features_response.text)

        sys.stderr.write(str(attribute) + '\n')
        sys.stderr.write(str(method) + '\n')

        energy = []
        liveness = []
        tempo = []
        speechiness = []
        acousticness = []
        instrumentalness = []
        danceability = []
        loudness = []
        valence = []

        for i in audio_features_response_data["audio_features"]:
        	energy.append(i["energy"])
        	liveness.append(i["liveness"])
        	tempo.append(i["tempo"])

        	speechiness.append(i["speechiness"])
        	acousticness.append(i["acousticness"])
        	instrumentalness.append(i["instrumentalness"])

        	danceability.append(i["danceability"])
        	loudness.append(i["loudness"])
        	valence.append(i["valence"])

	sortedIds = []
	
	dictionary = {"energy": energy, "liveness": liveness, "temp": tempo, "speechiness": speechiness, "acousticness": acousticness, "instrumentalness": instrumentalness, "danceability": danceability, "loudness": loudness, "valence": valence}
	if method == peek:
		sortedIds = sortPeakFunc(ids, str(attribute))
		
	elif method == quickthenslowclimb:
		sortedIds = sortPeakFunc(ids, str(attribute))
		
	elif method == toleast:
		sortedIds = sortPeakFunc(ids, str(attribute))
		
	elif method == togreatest:
		sortedIds = sortPeakFunc(ids, str(attribute))
        

        # for i in sortedIds:
        #     sys.stderr.write(str(i) + "\n")

        display_arr = audio_features_response_data["audio_features"]
        return str(display_arr)

@app.route("/create")
def create():
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    content = "application/json"
    playlist_name = "sortedoutput"
    header = copy.deepcopy(authorization_header)
    header["Content-Type"] = "{}".format(content)

    data = {"name":"sortedoutput"}

    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlist_response = requests.post(playlist_api_endpoint, headers=header, data=json.dumps(data))
    playlist_data = json.loads(playlist_response.text)

    playlist_id = playlist_data["id"]
    uris = []
    for i in sortedIds:
        uris.append("spotify:track:"+i)
    body = {"uris":uris}
    playlist_songs_api_endpoint = "{}/playlists/{}/tracks".format(profile_data["href"], playlist_id)
    playlist_songs_response = requests.post(playlist_songs_api_endpoint, headers=header, data=json.dumps(body))
    playlist_songs_data = json.loads(playlist_songs_response.text)

    return str(playlist_songs_data)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
