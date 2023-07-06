import json
import sys
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


@dataclass
class Gfy:
    gfy_id: str
    title: str
    tags: list[str] | None

    def __init__(self, gfy_id: str | None, title: str, tags: list[str] | None) -> None:
        self.gfy_id = gfy_id
        self.title = title
        self.tags = tags


class GfyData:
    gfys: list[Gfy]

    def __init__(self, gfy_file: Path) -> None:
        gfys = list()
        loaded = load_json(gfy_file, ensure_exists=False)
        if loaded is None:
            loaded = list()
        for gfy in loaded:
            gfys.append(Gfy(gfy["gfy_id"], gfy["title"], gfy.get("tags", None)))
        self.gfys = gfys

    def file_to_gfy(self, file: Path | str) -> Gfy:
        file = Path(file)
        assert file.exists(), f"{file} does not exist"
        for gfy in self.gfys:
            if gfy.title.lower() in file.name.lower():
                return gfy
        return Gfy(None, file.stem, None)


@dataclass
class Imgur:
    imgur_url: str
    gfy_title: str
    imgur_title: str
    tags: list[str] | None
    gfy_id: str | None

    def __init__(
        self,
        imgur_url: str,
        gfy_title: str,
        imgur_title: str,
        tags: list[str] | None,
        gfy_id: str | None,
    ) -> None:
        self.imgur_url = imgur_url
        self.gfy_title = gfy_title
        self.imgur_title = imgur_title
        self.tags = tags
        self.gfy_id = gfy_id


class ImgurData:
    imgurs: list[Imgur]

    def __init__(self, imgur_file: Path) -> None:
        loaded = load_json(imgur_file, ensure_exists=True)
        if loaded is None:
            raise ValueError(f"Could not load {imgur_file}")
        imgurs = list()
        for imgur in loaded:
            imgurs.append(
                Imgur(
                    imgur["imgur_url"],
                    imgur["gfy_title"],
                    imgur["imgur_title"],
                    imgur.get("tags", None),
                    imgur.get("gfy_id", None),
                )
            )
        self.imgurs = imgurs

    def is_uploaded(self, video: Path | str) -> bool:
        video = Path(video)
        assert video.exists(), f"{video} does not exist"
        for imgur in self.imgurs:
            if imgur.imgur_title.lower() in video.name.lower():
                return True
        return False

    def save(self, imgur_file: Path):
        save_data = list()
        for imgur in self.imgurs:
            save_data.append(
                {
                    "imgur_url": imgur.imgur_url,
                    "gfy_title": imgur.gfy_title,
                    "imgur_title": imgur.imgur_title,
                    "tags": imgur.tags,
                    "gfy_id": imgur.gfy_id,
                }
            )
        save_json(imgur_file, save_data)


def load_json(json_file: Path, ensure_exists: bool = True) -> list[dict] | None:
    if ensure_exists and not json_file.exists():
        json_file.parent.mkdir(exist_ok=True, parents=True)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    elif not json_file.exists():
        return None
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print("Error reading file: ", e)
        sys.exit(1)


def save_json(json_file: Path | str, data: list[dict]):
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
