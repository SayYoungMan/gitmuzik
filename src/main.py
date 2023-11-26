from youtube import get_youtube_client, fetch_all_playlist_items

def main():
    youtube = get_youtube_client()
    
    print(fetch_all_playlist_items(youtube))

if __name__ == "__main__":
    main()