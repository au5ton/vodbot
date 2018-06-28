from time import sleep
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from twitch import TwitchClient
import re
import argparse
from pprint import pprint

client = TwitchClient(os.environ["TWITCH_CLIENT_ID"])

# cli arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", action="store", dest="username", help="Get Twitch user ID from username")
parser.add_argument("-u", action="store", dest="userid") # Specify Twitch user ID
parser.add_argument("-i", action="store", dest="offset") # Specify video list offset (for pagination)
parser.add_argument("-O", action="store", dest="output_file_name", help="Output file name") # Specify output filename (for saving links to a text file)
parser.add_argument("-L", action="store", dest="limit", default="10", help="Limit results (max: 100)") # Specify how much vods to fetch per request
parser.add_argument("-t", action="store", dest="broadcast_type", help="Broadcast type: `archive`, `highlight`, `upload`, `archive,upload`, `archive,highlight`, `highlight,upload`")
parser.add_argument("-s", action="store", dest="sort", default="time", help="Sorting: `time`, `views`")
parser.add_argument("-V", action="store_true", default=False, dest="get_videos", help="Get videos") # Only get what specified
parser.add_argument("-A", action="store_true", default=False, dest="get_all_videos") # Specify this to loop through every vod available
args = parser.parse_args()

if(args.username is not None):
    users = client.users.translate_usernames_to_ids([args.username])
    for user in users:
        print(user.id)

if args.userid is not None:
    all_videos = []
    total_got = 0
    last_req_length = 1
    if args.get_all_videos:
        while last_req_length < 1:
            videos = client.channels.get_videos(channel_id=args.userid, limit=100, offset=total_got, broadcast_type=args.broadcast_type, sort=args.sort)
            total_got += len(videos)
            last_req_length = len(videos)
            all_videos += videos
        for video in all_videos:
            with open(args.output_file_name, "w") as text_file:
                text_file.write(video.url + "\n")
    else:
        videos = client.channels.get_videos(channel_id=args.userid, limit=int(args.limit), offset=args.offset+total_got, broadcast_type=args.broadcast_type, sort=args.sort)
    
        
    # 137512364