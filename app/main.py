import os

if __name__ == "__main__":
    print("Fetching tracks from playlist")
    os.system("python app\\spotify_playlist.py")
    print("Dowloading tracks")
    os.system("python app\\yt_links.py")
    print("Download successful")
