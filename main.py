import os

from dotenv import load_dotenv
import googleapiclient.discovery

DAILY_PLAYLIST_ID = "PLXzLX2ct6ysab-Gy0b1Xrm9Ka-Pg-yqmR"

class MusicMetaData:
    def __init__(self, playlist_item) -> None:
        # Snippet is a part of playlistItem that has all relevant information
        snippet = playlist_item["snippet"]

        self.title = snippet["title"]
        self.position = snippet["position"]
        self.owner = snippet["videoOwnerChannelTitle"].removesuffix(" - Topic").strip()
        self.image = snippet["thumbnails"]["high"]["url"]

    def __repr__(self) -> str:
        return f"{self.title} by {self.owner}"
    

def get_youtube_api_key() -> str:
    load_dotenv()
    return os.environ["YOUTUBE_API_KEY"]

def get_youtube_client():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = get_youtube_api_key()

    return googleapiclient.discovery.build(api_service_name, api_version, developerKey = api_key)

def fetch_playlist_items(client, next_page_token):
    request = client.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=DAILY_PLAYLIST_ID,
        pageToken=next_page_token,
    )
    response = request.execute()

    return response

def is_private_video(playlist_item):
    return playlist_item["snippet"]["title"] == "Private video"

def fetch_all_playlist_items(client) -> list[MusicMetaData]:
    all_items = []
    next_page_token = None

    # Loop to get all videos in the playlist
    while True:
        response = fetch_playlist_items(client, next_page_token)
        all_items.extend(response["items"])

        # If there is next page, fetch next page, otherwise break and return all items
        if "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
        else:
            break

    all_musics = [MusicMetaData(item) for item in all_items if not is_private_video(item)]

    return all_musics

def main():
    youtube = get_youtube_client()
    
    print(fetch_all_playlist_items(youtube))

if __name__ == "__main__":
    main()