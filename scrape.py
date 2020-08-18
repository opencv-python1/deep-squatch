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


def download_tweets(username=None, limit=None, include_replies=False, include_links=False, strip_usertags=False, strip_hashtags=False):
    """
    Given a username, download the tweets that abide by the parameters

    Note: limit must be a multiple of 20
    """

    print("Username: %s" % username)

    # better limit estimation
    found = False
    if limit:
        assert limit % 20 == 0, "limit is not a multiple of 20"
        found = True
    else:
        found = False

        for _ in range(0, 4):
            if not found:
                c = twint.Config()
                c.Username = username
                c.Store_object = True

                twint.run.Lookup(c)

                try:
                    users = twint.output.users_list
                    limit = users[0].tweets
                    found = True
                except:
                    found = False

                if not found:
                    sleep(15.0)
            else:
                continue

    if not found:
        limit = 2000

    print("Limit: %d" % limit)

    pattern = URL_PATTERN

    if strip_usertags:
        pattern += UNAME_PATTERN

    if strip_usertags:
        pattern += HASHTAG_PATTERN

    with open(".temp", "w", encoding="utf-8") as f:
        f.write(str(-1))

    with open("{}_tweets.csv".format(username), "w", encoding="utf-8") as f:
        w = csv.writer(f)

        # GPT-2 format expects a CSV header by default
        w.writerow(["tweets"])

        prog = tqdm(range(limit), desc="Scraping tweet progress")

        # looping of scraping and writing to CSV
        for i in range((limit // 20) - 1):
            tweet_data = []

            # try 5 times
            for _ in range(0, 4):
                if len(tweet_data) == 0:
                    config = twint.Config()
                    config.Store_object = True
                    config.Hide_output = True
                    config.Username = username
                    config.Limit = 40
                    config.Resume = ".temp"
                    config.Store_object_tweets_list = tweet_data

                    twint.run.Search(config)

                    if len(tweet_data) == 0:
                        sleep(15.0)
                else:
                    continue

            # if we fail, we fail
            if len(tweet_data) == 0:
                config = twint.Config()
                config.Store_object = True
                config.Hide_output = True
                config.Username = username
                config.Limit = 40
                config.Resume = ".temp"
                config.Store_object_tweets_list = tweet_data

            # case on the inputs
            if not include_replies:
                tweets = [re.sub(pattern, "", t.tweet).strip()
                          for t in tweet_data if not is_reply(t)]

                for t in tweets:
                    if t != "" and not t.startswith("@"):
                        w.writerow([t])
            else:
                tweets = [re.sub(pattern, "", t.tweet).strip()
                          for t in tweet_data]

                for t in tweets:
                    if t != "":
                        w.writerow([t])

            # update progress bar
            if i > 0:
                prog.update(20)
            else:
                prog.update(40)

    prog.close()
    os.remove(".temp")

    return


if __name__ == "__main__":
    fire.Fire(download_tweets)
