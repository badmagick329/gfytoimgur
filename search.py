import sys
from pathlib import Path

from filedata import ImgurData

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))
IMGUR_DATA = BASE_DIR / "data" / "imgur.json"


def main():
    assert IMGUR_DATA.exists(), f"{IMGUR_DATA} does not exist"
    if not sys.argv[1:]:
        print(
            "Usage: python3 search.py <tags>\n",
            "Use commas to separate tags. Surround tags with quotes if they contain spaces\n",
            "To output all: python3 search.py -",
            sep="",
        )
        return
    tags = sys.argv[1]
    imgurdata = ImgurData(IMGUR_DATA)
    tags = [tag.strip().lower() for tag in tags.split(",") if tag.strip()]
    if not tags:
        return
    imgur_urls = list()
    if tags == ["-"]:
        for imgur in imgurdata.imgurs:
            imgur_urls.append(imgur.imgur_url)
        print("\n".join(imgur_urls))
        return
    for imgur in imgurdata.imgurs:
        if imgur.tags is None:
            continue
        saved_tags = [tag.lower() for tag in imgur.tags]
        if all(tag in saved_tags for tag in tags):
            imgur_urls.append(imgur.imgur_url)
    print("\n".join(imgur_urls))


if __name__ == "__main__":
    main()
