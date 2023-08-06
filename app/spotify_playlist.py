import glob
import os
import csv
import json
import py_script
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Accessing credentials
with open(r"assets\credentials.json") as file:
    data = json.load(file)
    spotify_client_id, spotify_client_secret = data["Spotify"].values()
    file.close()

# Connecting with spotify api
auth = SpotifyClientCredentials(spotify_client_id, spotify_client_secret)
sp = Spotify(auth_manager=auth)

# Playlist link
# playlist_link = input("Enter playlist link : ")
# playlist_link = (
#     "https://open.spotify.com/playlist/29CDHardEjqjwFkaTIXH5d?si=7a69a467e839450e"
# )
# playlist_link = (
#     r"https://open.spotify.com/playlist/104xyMQrIE7qBKYWxo3G6Z?si=f83497997d544c3f"
# )
# playlist_link=r"https://open.spotify.com/playlist/3ua7cas0riaebaixijDaoq?si=6c6aafd7d2704ae9"
playlist_link = py_script.main()
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

# Deleting old csv files
path = os.getcwd() + "\\utils"
if csv_files := glob.glob(os.path.join(path, "*.csv")):
    for file_path in csv_files:
        os.remove(file_path)

# Storing data in csv file
with open(f"{path}\\{playlist_name}.csv", "w", newline="", encoding="utf-8") as data:
    writer = csv.writer(data)
    writer.writerow(header)
    writer.writerows(scraped_data)
