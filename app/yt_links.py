import os
import glob
import json
import pytube
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

# Make queries
# track_list = list(zip(list(tracks["Track Name"]), list(tracks["Artist Name"])))
# query_list = [" ".join(track) for track in track_list]

# # Fetching links
# links = []
# for query in query_list:
#     s = pytube.Search(query)
#     video_id = s.results[0].video_id
#     links.append(f"https://www.youtube.com/watch?v={video_id}")
# # for query in query_list:
# #     request = yt.search().list(
# #         part="snippet",
# #         q=query,
# #         maxResults=1,
# #         order="viewCount",
# #         type="video",
# #     )
# #     response = request.execute()
# #     items = response["items"][0]
# #     video_id = items["id"]["videoId"]
# #     video_url = f"https://www.youtube.com/watch?v={video_id}"
# #     links.append(video_url)

# # Download using links
# path_to_download_folder = (
#     os.path.join(Path.home(), "Downloads") + "\\" + spotify_playlist.playlist_name
# )
# for link, track in list(zip(links, spotify_playlist.track_list)):
#     link = pytube.YouTube(link)
#     audio = link.streams.filter(adaptive=True, only_audio=True).order_by("abr")
#     audio[-1].download(path_to_download_folder, f"{track}.mp3")
# print("Download successful")

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
    s = pytube.Search(query)
    video_id = s.results[0].video_id
    link = f"https://www.youtube.com/watch?v={video_id}"
    link = pytube.YouTube(link)
    audio = link.streams.filter(adaptive=True, only_audio=True).order_by("abr")
    audio[-1].download(path_to_download_folder, f"{track}.mp3")

