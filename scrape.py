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
