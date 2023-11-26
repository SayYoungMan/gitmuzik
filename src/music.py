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