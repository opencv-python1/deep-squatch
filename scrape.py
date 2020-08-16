"""Scrape
Scrape tweets from a given username
"""

# Modified from https://github.com/minimaxir/download-tweets-ai-text-gen

import os
import logging
import csv
import re
import twint
import fire
from datetime import datetime as dt
from time import sleep
from tqdm import tqdm


# Disable logging to get rid of any warnings
logger = logging.getLogger()
logger.disabled = True

# URL Pattern
URL_PATTERN = r"http\S+|pic\.\S+|\xa0|…"

# Username Pattern
UNAME_PATTERN = r"|@[a-zA-Z0-9_]+"

# Hashtag Pattern
HASHTAG_PATTERN = r"|#[a-zA-Z0-9_]+"


def is_reply(tweet_obj):
    """
    Check if input tweet object is a reply.

    This is achieved by looking at the number of replies versus the top level
    number of replies. Doing this comparison allows us to determine if the
    current tweet is a reply or not.
    """

    if len(tweet_obj.reply_to) == 1:
        return False

    reply_users = tweet_obj.reply_to[1:]
    convos = [u["username"] in tweet_obj.tweet for u in reply_users]

    if sum(convos) < len(reply_users):
        return True

    return False
