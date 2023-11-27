import logging
import sys

from dotenv import load_dotenv

from music import MusicMetaData
from youtube import get_youtube_client, fetch_all_playlist_items
from mongodb import get_mongo_client, write_music_data_to_db, get_last_music_titles

def is_changed_today(last_music_dict: dict[str, bool], today_music_data: list[MusicMetaData]) -> bool:
    last_music_count = len(last_music_dict.keys())
    today_music_count = len(today_music_data)
    if last_music_count != today_music_count:
        logging.info("Number of songs today is different [last:%i, today:%i]", last_music_count, today_music_count)
        return True

    for music in today_music_data:
        if music.title not in last_music_dict:
            logging.info("There is a song whose title was not there yesterday: %s", music.title)
            return True
        
    logging.info("Nothing changed today.")
    return False

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    load_dotenv()

    youtube = get_youtube_client()
    mongo = get_mongo_client()

    last_music_dict = get_last_music_titles(mongo)
    today_music_data = fetch_all_playlist_items(youtube)

    if is_changed_today(last_music_dict, today_music_data):
        write_music_data_to_db(mongo, today_music_data)    

if __name__ == "__main__":
    main()