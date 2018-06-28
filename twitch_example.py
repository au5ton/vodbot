from time import sleep
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from twitch import TwitchClient
import re

client = TwitchClient(os.environ["TWITCH_CLIENT_ID"])

list_of_videos = ["https://www.twitch.tv/videos/275764362","https://www.twitch.tv/videos/275764844","https://www.twitch.tv/videos/275764989", "https://www.twitch.tv/videos/275765066"]
vid_ids = []
for s in list_of_videos:
    m = re.findall('videos/\d{9,9}', s, re.IGNORECASE)
    print(m[0][7:]) # cut off after `videos/`
    vid_ids.append(m[0][7:])

for n in vid_ids:
    video = client.videos.get_by_id(n)
    print(video["title"]+" ("+str(video["length"])+"s)")

