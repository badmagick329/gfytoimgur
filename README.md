A simple script for uploading videos downloaded from gfycat to imgur.
Note: You cannot upload more than 50 videos per hour

### Imgur App

You will need to register your app with imgur and get an auth token.
Step by step instructions can be found [here](https://apidocs.imgur.com/)
Save your authentication information in conf.py

### Gfycat data

`data/gfycat.json` - (Optional) This file is used to link videos to their
gfycat information. This is done by matching the video name with the title
value.

Expected format: list of dict
Minimum required keys: gfy_id, title
Optional keys: tags

### Imgur Data

`data/imgur.json` - This file will be created by the script. It is used to keep
track of what has been uploaded and linking gfys with their imgur counterparts
if gfycat.json is found

Expected format: list of dict
Minimum required keys: imgur_url
Optional keys: tags, gfy_id

### Search

`search.py` - Simple search script for searching uploaded imgurs based on the
tags read from gfycat.json

Usage: python3 search.py <tags>
Use commas to separate tags. Surround tags with quotes if they contain spaces
