import csv
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Accessing credentials
with open(r"credentials.json") as file:
    data = json.load(file)
    spotify_client_id, spotify_client_secret = data["Spotify"].values()
    file.close()

# Connecting with spotify api
auth = SpotifyClientCredentials(spotify_client_id, spotify_client_secret)
sp = Spotify(auth_manager=auth)

# Playlist link
# playlist_link = input("Enter playlist link : ")
playlist_link = (
    "https://open.spotify.com/playlist/29CDHardEjqjwFkaTIXH5d?si=7a69a467e839450e"
)
playlist_data = sp.playlist(playlist_link)

# Data scraping
playlist_name = playlist_data["name"]
total_tracks = playlist_data["tracks"]["total"]

tracks = playlist_data["tracks"]
items = tracks["items"]

track_list = []
album_list = []
artist_list = []
offset = 0
for i in range(total_tracks):
    track_list.append(items[i - offset]["track"]["name"])
    album_list.append(items[i - offset]["track"]["album"]["name"])
    artist_list.append(items[i - offset]["track"]["artists"][0]["name"])
    if (i + 1) % 100 == 0:
        tracks = sp.next(tracks)
        items = tracks["items"]
        offset = i + 1

header = ("No", "Track Name", "Artist Name", "Album Name")
scraped_data = list(
    zip(range(1, total_tracks + 1), track_list, artist_list, album_list)
)

# Storing data in csv file
with open(f"{playlist_name}.csv", "w", newline="") as data:
    writer = csv.writer(data)
    writer.writerow(header)
    writer.writerows(scraped_data)
