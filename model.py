"""Model
Creates an AI based on the GPT-2 355M model using data scraped by the
scrape class.
"""

import gpt_2_simple as gpt2
from datetime import datetime

TWEETS = "squatchssb_tweets.csv"

# Download 355M model
gpt2.download_gpt2(model_name="355M")

sess = gpt2.start_tf_sess()
gpt2.finetune(sess, dataset=TWEETS, model_name='355M', steps=2000, restore_from='fresh',
              run_name='run1', print_every=50, sample_every=500, save_every=500)
gpt2.generate(sess, length=140, temperature=1.21, prefix='<|startoftext|>',
              truncate='<|endoftext|>', include_prefix=False, nsamples=20, batch_size=20)
