from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import argparse
import os.path
import re
from twitch import TwitchClient

# cli arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", action="store", dest="file_name", help="Process a file of links line-by-line")
args = parser.parse_args()

# twitch stuff
client = TwitchClient(os.environ["TWITCH_CLIENT_ID"])
vid_ids = []

if (args.file_name is None):
    print("You must specify what file to read a list of links from with the -f argument.")
else:
    # make sure file exists
    if os.path.isfile(args.file_name):
        with open(args.file_name) as file:
            # each `lines` index is a line
            lines = [line.rstrip("\n") for line in file]
            for link in lines:
                m = re.findall("videos/\d{9,9}", link, re.IGNORECASE)
                # check if regex failed by type inferring m to a boolean, python mumbo jumbo: https://stackoverflow.com/questions/53513/how-do-i-check-if-a-list-is-empty
                if(not not m):
                    # regex is good
                    vid_ids.append(m[0][7:])

# for every id from a valid link
for n in vid_ids:
    video = client.videos.get_by_id(n)
    print(video["title"]+" ("+str(video["length"])+"s)")
