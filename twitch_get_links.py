from time import sleep
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from twitch import TwitchClient
import re
import argparse
from pprint import pprint
import csv
import json

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
parser.add_argument("-links", action="store_true", default=False, dest="get_all_videos") # Specify this to loop through every vod available
parser.add_argument("-csv", action="store_true", default=False, dest="make_csv") # Make a CSV of VOD data
args = parser.parse_args()

if(args.username is not None):
    users = client.users.translate_usernames_to_ids([args.username])
    for user in users:
        args.userid = user.id
        print(user.id)

if args.userid is not None:
    all_videos = []
    total_got = 0
    last_req_length = 1
    print("Getting ALL videos...")
    while last_req_length > 0:
        #print("\nGetting 100 more (if possible)...")
        videos = client.channels.get_videos(channel_id=args.userid, limit=100, offset=total_got, broadcast_type=args.broadcast_type, sort=args.sort)
        total_got += len(videos)
        last_req_length = len(videos)
        all_videos += videos
        print("\tTotal fetched: "+str(len(all_videos)))
    if args.get_all_videos:
        with open(args.output_file_name, "w") as text_file:
            for video in all_videos:
                text_file.write(video.url + "\n")
    elif args.make_csv:
        with open(args.output_file_name, "w") as csvfile:
            spam = csv.writer(csvfile, dialect='excel')
            # write headers
            spam.writerow(all_videos[0])
            # write data
            for vod in all_videos:
                row = []
                for attr in vod:
                    if type(vod[attr]) is not object:
                        row += [vod[attr]]
                    else:
                        row += json.dumps(vod[attr])
                spam.writerow(row)
    else:
        videos = client.channels.get_videos(channel_id=args.userid, limit=int(args.limit), offset=args.offset, broadcast_type=args.broadcast_type, sort=args.sort)
        with open(args.output_file_name, "w") as text_file:
            for video in videos:
                text_file.write(video.url + "\n")
        
    # 137512364