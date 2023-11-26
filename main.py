import os

from dotenv import load_dotenv
import googleapiclient.discovery

DAILY_PLAYLIST_ID = "PLXzLX2ct6ysab-Gy0b1Xrm9Ka-Pg-yqmR"

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

def fetch_all_playlist_items(client):
    all_items = []
    next_page_token = None

    while True:
        response = fetch_playlist_items(client, next_page_token)
        all_items.extend(response["items"])

        if "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
        else:
            break

    return all_items

def main():
    youtube = get_youtube_client()
    
    print(fetch_all_playlist_items(youtube))

if __name__ == "__main__":
    main()