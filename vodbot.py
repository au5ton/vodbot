from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import argparse
import os
import os.path
import re
from time import sleep
from twitch import TwitchClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# cli arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", action="store", dest="file_name", help="Process a file of links line-by-line")
args = parser.parse_args()

# twitch stuff
client = TwitchClient(client_id=os.environ["TWITCH_CLIENT_ID"], oauth_token=os.environ["TWITCH_OAUTH_TOKEN"])
vid_ids = []
real_links = []

# selenium stuff
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"]) # use already logged in user
options.add_argument('--log-level=3')
options.add_argument('--disable-logging')

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
                    real_links.append(link)

    if (not not vid_ids):
        print("Retrieved " + str(len(vid_ids)) + " video ids from links of " + str(len(lines)) + " lines total")
        print("Fetching info on videos...")
        # for every id from a valid link
        vid_lengths = []
        for n in vid_ids:
            video = client.videos.get_by_id(n) # fetch video via HTTP
            print("\t"+video["title"]+" ("+str(video["length"])+"s)")
            vid_lengths.append(video["length"])
        print("Total clip length: " + str(sum(vid_lengths)) + " seconds")
        print("Starting Chrome")
        driver = webdriver.Chrome(executable_path=os.environ["CHROMEDRIVER_LOCATION"], chrome_options=options)
        # for every clip (real_links, vid_ids, and vid_lengths should be same length)
        for i, val in enumerate(real_links):
            print("\tNavigating to: "+real_links[i])
            driver.get(real_links[i])
            print("\tWaiting " + str(vid_lengths[i] + int(os.environ["EXTRA_WATCH_TIME"])) + " seconds for video completition (" + os.environ["EXTRA_WATCH_TIME"] + " seconds extra to compensate for ads and delays)")
            sleep(vid_lengths[i] + int(os.environ["EXTRA_WATCH_TIME"]))
        print("Finished! Closing browser window.")
        driver.close()
    else:
        print("Couldn\'t find any valid video ids from that file.");    
