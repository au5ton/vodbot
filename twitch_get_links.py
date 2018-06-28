from time import sleep
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from twitch import TwitchClient
import re

client = TwitchClient(os.environ["TWITCH_CLIENT_ID"])


