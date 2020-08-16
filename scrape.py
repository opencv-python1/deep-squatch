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


def scrape_uname(username=None, limit=None, include_replies=False, include_links=False, strip_usertags=False, strip_hashtags=False):
    """
    Given a username, download the tweets that abide by the parameters

    Note: limit must be a multiple of 20
    """

    if limit:
        assert limit % 20 == 0, "Limit must be a multiple of 20"
    else:
        config = twint.Config()
        config.Username = username
        config.Store_object = True

        if include_links:
            config.Links = "include"
        else:
            config.Links = "exclude"

        twint.run.Lookup(config)
        limit = twint.output.users_list[-1].tweets

    pattern = URL_PATTERN

    if strip_usertags:
        pattern += UNAME_PATTERN

    if strip_usertags:
        pattern += HASHTAG_PATTERN

    with open(".temp", "w", encoding="utf-8") as f:
        f.write(str(-1))

    print("Scraping tweets from @%s..." % username)

    with open("{}_tweets.csv".format(username), "w", encoding="utf-8") as f:
        w = csv.writer(f)

        # GPT-2 format expects a CSV header by default
        w.writerow(["tweets"])

        prog = tqdm(range(limit), desc="Oldest tweet from {}".format(username))

        # TODO looping of scraping and writing to CSV

    prog.close()
    os.remove(".temp")

    return


if __name__ == "__main__":
    fire.Fire(scrape_uname)
