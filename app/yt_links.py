import os
import glob
import json
import pandas as pd
from googleapiclient.discovery import build
import pytube
from pathlib import Path
import spotify_playlist

# Api info
service_name = "youtube"
api_version = "v3"

# Accessing credentials
with open(r"assets\credentials.json") as file:
    data = json.load(file)
    developer_key = data["Youtube"]["developer_key"]
    file.close()

# Connecting with youtube api
yt = build(service_name, api_version, developerKey=developer_key)

# Get path of csv file
path = os.getcwd() + r"\utils"
csv_files = glob.glob(os.path.join(path, "*.csv"))
tracks = pd.read_csv(csv_files[0])

# Fetching links
path_to_download_folder = (
    os.path.join(Path.home(), "Downloads") + "\\" + spotify_playlist.playlist_name
)
for track, artist in list(
    zip(
        list(tracks["Track Name"]),
        list(tracks["Artist Name"]),
    )
):
    query = track + artist
    # s = pytube.Search(query)
    # video_id = s.results[0].video_id
    request = yt.search().list(
        part="snippet",
        q=query,
        maxResults=1,
        order="viewCount",
        type="video",
    )
    response = request.execute()
    items = response["items"][0]
    video_id = items["id"]["videoId"]
    
    link = f"https://www.youtube.com/watch?v={video_id}"
    link = pytube.YouTube(link)
    audio = link.streams.filter(adaptive=True, only_audio=True).order_by("abr")
    audio[-1].download(path_to_download_folder, f"{track}.mp3")
