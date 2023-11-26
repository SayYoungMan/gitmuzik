import logging
import sys

from dotenv import load_dotenv

from youtube import get_youtube_client, fetch_all_playlist_items
from mongodb import get_mongo_client, write_music_data_to_db

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    load_dotenv()

    youtube = get_youtube_client()
    mongo = get_mongo_client()

    musics = fetch_all_playlist_items(youtube)
    write_music_data_to_db(mongo, musics)    

if __name__ == "__main__":
    main()