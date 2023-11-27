class MusicMetaData:
    def __init__(self, music_dict) -> None:
        self.title = music_dict["title"]
        self.position = music_dict["position"]
        self.owner = music_dict["owner"]
        self.image_url = music_dict["image_url"]

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