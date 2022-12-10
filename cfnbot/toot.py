import os

from mastodon import Mastodon

from cfnbot import store, formatter

mastodon = Mastodon(
    access_token=os.environ['MASTODON_ACCESS_TOKEN'],
    api_base_url=os.environ['MASTODON_API_BASE_URL']
)


def post_toot(atom):
    for message in formatter.format_post(*atom, max_len=500):
        if len(message) > 500:
            continue
        
        mastodon.status_post(message, idempotency_key=store.hash_atom(atom))
        return True

    # None of the generated formats were sufficient
    return False
