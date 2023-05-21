import sys
from pathlib import Path

import requests

from conf import AUTH_TOKEN, MAX_UPLOADS, VIDEOS_DIR
from filedata import GfyData, Imgur, ImgurData

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))
# Expected format: list of dict
# Minimum required keys: imgur_url
# Optional keys: tags, gfy_id
IMGUR_DATA = BASE_DIR / "data" / "imgur.json"

# Expected format: list of dict
# Minimum required keys: gfy_id, title
# Optional keys: tags
GFY_DATA = BASE_DIR / "data" / "gfycat.json"


def main():
    gfydata = GfyData(GFY_DATA)
    imgurdata = ImgurData(IMGUR_DATA)
    videos = Path(VIDEOS_DIR).glob("*.mp4")
    upload_videos(videos, imgurdata, gfydata, max=MAX_UPLOADS)


def upload_video(video_path: Path | str, config: dict) -> dict:
    """
    Parameters
    ----------
    video_path : str
        Path to video to upload
    config : dict
        Configuration for video upload
        Can have keys: album, name, title, description
        All are optional

    Returns
    -------
    format:
        {'id': 'rZeJkfa', 'deletehash': 'eMKppQNCjkHg6Gj', 'account_id':
         0000000, 'account_url': 'accountname', 'ad_type': None, 'ad_url':
         None, 'title': 'Image Title', 'description': 'Image Description
         here', 'name': 'Image name', 'type': 'video/mp4', 'width': 750,
         'height': 1000, 'size': 0, 'views': 0, 'section': None, 'vote':
         None, 'bandwidth': 0, 'animated': True, 'favorite': False,
         'in_gallery': False, 'in_most_viral': False, 'has_sound': False,
         'is_ad': False, 'nsfw': None, 'link':
         'https://i.imgur.com/rZeJkfa.mp4', 'tags': [], 'mp4_size':
         4265442, 'processing': {'status': 'pending'}, 'datetime':
         1684616870, 'mp4': 'https://i.imgur.com/rZeJkfa.mp4', 'hls': ''}
    """
    assert isinstance(video_path, (Path, str)), "image_path must be Path or str"
    assert Path(video_path).exists(), f"{video_path} does not exist"
    config["disable_audio"] = "0"
    url = "https://api.imgur.com/3/upload"
    header = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    with open(video_path, "rb") as f:
        image_bytes = f.read()
    file = (
        "video",
        image_bytes,
    )
    response = requests.request("POST", url, headers=header, data=config, files=[file])
    response = response.json()
    if response["success"]:
        return response["data"]
    raise Exception(f"Failed to upload {video_path} - {response}")


def upload_videos(
    videos: list[Path], imgurdata: ImgurData, gfydata: GfyData, max: int = 1
):
    uploaded = 0
    errored = list()
    for video in videos:
        if uploaded >= max:
            break
        if imgurdata.is_uploaded(video):
            # print(f"Skipping {video} because it's already uploaded")
            continue
        gfy = gfydata.file_to_gfy(video)
        print(f"Uploading {video}")
        config = {
            "album": None,
            "title": gfy.title,
            "description": None,
            "name": gfy.title,
        }
        try:
            image = upload_video(str(video), config=config)
        except Exception as e:
            errored.append((video, e))
            break
        imgur = Imgur(image["link"], gfy.title, gfy.tags, gfy.gfy_id)
        imgurdata.imgurs.append(imgur)
        imgurdata.save(IMGUR_DATA)
        uploaded += 1
        print(image["link"])
    print(f"Uploaded {uploaded} videos")
    for video, e in errored:
        print(f"Failed to upload {video} - {e}")


if __name__ == "__main__":
    main()
