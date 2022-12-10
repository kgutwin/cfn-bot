import os
import re
import twitter

from cfnbot import formatter

CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'
ACCESS_TOKEN_KEY = os.environ['TWITTER_ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)


def post_tweet(atom):
    for message in formatter.format_post(*atom):
        try:
            api.PostUpdate(message, verify_status_length=True)
            return True
        except twitter.error.TwitterError as ex:
            if 'CHARACTER_LIMIT' not in str(ex):
                raise

    # None of the generated formats were sufficient
    return False
