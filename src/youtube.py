import os
import logging

import googleapiclient.discovery

from music import MusicMetaData

DAILY_PLAYLIST_ID = "PLXzLX2ct6ysab-Gy0b1Xrm9Ka-Pg-yqmR"

def get_youtube_client():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ["YOUTUBE_API_KEY"]

    return googleapiclient.discovery.build(api_service_name, api_version, developerKey = api_key)

def _fetch_playlist_items(client, next_page_token):
    request = client.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=DAILY_PLAYLIST_ID,
        pageToken=next_page_token,
    )
    response = request.execute()

    return response

def _is_private_video(playlist_item):
    return playlist_item["snippet"]["title"] == "Private video"

def fetch_all_playlist_items(client) -> list[MusicMetaData]:
    all_items = []
    next_page_token = None

    # Loop to get all videos in the playlist
    while True:
        response = _fetch_playlist_items(client, next_page_token)
        all_items.extend(response["items"])

        # If there is next page, fetch next page, otherwise break and return all items
        if "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
        else:
            break

    all_musics = [MusicMetaData(item) for item in all_items if not _is_private_video(item)]
    logging.info("Successfully fetched items from the playlist.")

    return all_musics