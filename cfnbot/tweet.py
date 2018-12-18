import os
import re
import twitter

CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'
ACCESS_TOKEN_KEY = os.environ['TWITTER_ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)


SERVICE_EXTRACT = re.compile(r'AWS::([^:]+)::')
def format_tweet(header, body, link, date):
    if link is None:
        link = ""

    service_hit = SERVICE_EXTRACT.search(header)
    if service_hit is not None:
        service_tag = "#" + service_hit.group(1).lower() + ' '
    else:
        service_tag = ""
        
        
    # First yield the most likely version.
    yield f"""{header}

{body}
{link} {service_tag}#cloudformation"""

    # Next, trim the body to the first sentence.
    first_sentence = body.split('. ')[0]
    if len(body) > len(first_sentence) and body[len(first_sentence)] == '.':
        first_sentence += '.'
    yield f"""{header}

{first_sentence}
{link} {service_tag}#cloudformation"""

    # Now truncate the first sentence at the most appropriate space
    chp = min(234 - len(header) - len(service_tag), len(body) - 1)
    while body[chp] != ' ':
        chp -= 1
        if chp == 0:
            return
    first_chunk = body[:chp]
    yield f"""{header}

{first_chunk}...
{link} {service_tag}#cloudformation"""
    

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
