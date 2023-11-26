class MusicMetaData:
    def __init__(self, playlist_item) -> None:
        # Snippet is a part of playlistItem that has all relevant information
        snippet = playlist_item["snippet"]

        self.title = snippet["title"]
        self.position = snippet["position"]
        self.owner = snippet["videoOwnerChannelTitle"].removesuffix(" - Topic").strip()
        self.image_url = snippet["thumbnails"]["high"]["url"]

    def __repr__(self) -> str:
        return f"{self.title} by {self.owner}"

    def to_dict(self) -> dict:
        music_dict = {
            "title": self.title,
            "owner": self.owner,
            "image_url": self.image_url,
            "position": self.position,
        }
        return music_dict