# Libraries
import os
import pytube
import webbrowser
from pathlib import Path
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from googleapiclient.discovery import build

import main

# Connecting with spotify api
load_dotenv()
auth = SpotifyClientCredentials(
    os.getenv("sp_client_id"),
    os.getenv("sp_client_secret"),
)
sp = Spotify(auth_manager=auth)

# Connecting with youtube api
yt = build(
    os.getenv("yt_service_name"),
    os.getenv("yt_api_version"),
    developerKey=os.getenv("yt_developer_key"),
)

# Playlist link
playlist_link = (
    "https://open.spotify.com/playlist/3ua7cas0riaebaixijDaoq?si=1dedb4f6e6e04ff4"
)
# playlist_link = (
#     "https://open.spotify.com/playlist/48R8WFVbjl8rO1iFfr9Hxs?si=a27673c96bb14ed1"
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

# Delete track data which are removed from spotify
track_artist_list = list(
    filter(
        lambda x: "".join(x).strip() not in [None, ""],
        track_artist_list,
    )
)

# List of queries
query_list = list(map(lambda x: " ".join(x[::-1]), track_artist_list))

# Download path
path_to_download_folder = os.path.join(Path.home(), "Downloads") + "\\" + playlist_name
print(f"Downloading your favorites songs at: {path_to_download_folder}")

# Fetching Links and downloading files
for i, query in enumerate(query_list):
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
    audio = link_data.streams.filter(only_audio=True).last()
    track_name = " by ".join(track_artist_list[i])
    audio.download(path_to_download_folder, f"{track_name}.mp3")
    print(f"Downloaded -> {track_name}")

# Open Folder
print("Opening your folder ...")
webbrowser.open(path_to_download_folder)
