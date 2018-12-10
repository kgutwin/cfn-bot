import os
import twitter

CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'
ACCESS_TOKEN_KEY = os.environ['TWITTER_ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)


def format_tweet(header, body, link, date):
    if link is None:
        link = ""

    # First yield the most likely version.
    yield f"""{header}

{body}
{link}"""

    # Next, trim the body to the first sentence.
    first_sentence = body.split('. ')[0]
    yield f"""{header}

{first_sentence}
{link}"""

    # Now truncate the first sentence to no more than 200 characters
    chp = 200
    while first_sentence[chp] != ' ':
        chp -= 1
        if chp == 0:
            return
    first_chunk = first_sentence[:chp]
    yield f"""{header}

{first_chunk}...
{link}"""
    

def post_tweet(atom):
    for message in format_tweet(*atom):
        try:
            api.PostUpdate(message, verify_status_length=True)
            return True
        except twitter.error.TwitterError as ex:
            if 'CHARACTER_LIMIT' not in str(ex):
                raise

    # None of the generated formats were sufficient
    return False
