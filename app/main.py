# Libraries
import os
import json
import pytube
import webbrowser
from pathlib import Path
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build

# Youtube Data Api info
service_name = "youtube"
api_version = "v3"

# Accessing credentials for Spotify and Youtube
with open(r"assets\credentials.json") as file:
    data = json.load(file)
    spotify_client_id, spotify_client_secret = data["Spotify"].values()
    developer_key = data["Youtube"]["developer_key"]
    file.close()

# Connecting with spotify api
auth = SpotifyClientCredentials(spotify_client_id, spotify_client_secret)
sp = Spotify(auth_manager=auth)

# Connecting with youtube api
yt = build(service_name, api_version, developerKey=developer_key)

# Playlist link
playlist_link = (
    "https://open.spotify.com/playlist/3ua7cas0riaebaixijDaoq?si=1dedb4f6e6e04ff4"
)
# playlist_link = (
#     "https://open.spotify.com/playlist/29CDHardEjqjwFkaTIXH5d?si=c5e69af3a38c43f0"
# )
playlist_data = sp.playlist(playlist_link)

# Storing data
playlist_name = playlist_data["name"]
print(f"Fetching info from your playlist: {playlist_name}")
total_tracks = playlist_data["tracks"]["total"]
tracks = playlist_data["tracks"]
spotify_items = tracks["items"]

track_artist_list = []
offset = 0
for i in range(total_tracks):
    track_artist_list.append(
        [
            spotify_items[i - offset]["track"]["name"],
            spotify_items[i - offset]["track"]["artists"][0]["name"],
        ]
    )
    if (i + 1) % 100 == 0:
        tracks = sp.next(tracks)
        spotify_items = tracks["items"]
        offset = i + 1

# List of queries
query_list = set(
    filter(
        lambda x: x.strip() not in [None, ""],
        list(map(" ".join, track_artist_list)),
    )
)

# Download path
path_to_download_folder = os.path.join(Path.home(), "Downloads") + "\\" + playlist_name
print(f"Downloading your favorites songs at: {path_to_download_folder}")

# Fetching Links and downloading files
for query in query_list:
    # Fetching Links
    # Using Pytube
    s = pytube.Search(query)
    track_id = s.results[0].video_id
    # Using Youtube Data API
    # request = yt.search().list(
    #     part="snippet",
    #     q=query,
    #     maxResults=1,
    #     order="viewCount",
    #     type="video",
    # )
    # response = request.execute()
    # yt_items = response["items"][0]
    # track_id = yt_items["id"]["videoId"]
    link = f"https://www.youtube.com/watch?v={track_id}"

    # Downloading tracks
    link_data = pytube.YouTube(link)
    audio = link_data.streams.filter(adaptive=True, only_audio=True).order_by("abr")
    audio[-1].download(path_to_download_folder, f"{query}.mp3")
    print(f"Downloaded -> {query}")

print("Opening your folder ...")
webbrowser.open(path_to_download_folder)
