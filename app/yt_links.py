import os
import glob
import json
import pandas as pd
from googleapiclient.discovery import build

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
track_list = list(zip(list(tracks["Track Name"]), list(tracks["Artist Name"])))
query_list = [" ".join(track) for track in track_list]

# Fetching links
links = []
for query in query_list:
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
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    links.append(video_url)

# Updating csv
tracks["Links"] = links
tracks.to_csv(csv_files[0], index=False)
