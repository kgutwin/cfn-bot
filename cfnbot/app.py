from datetime import datetime, timedelta

from cfnbot import parser, tweet, store


def is_too_old(atom):
    post_date = datetime.strptime(atom[-1], '%B %d, %Y')
    return (datetime.now() - post_date) > timedelta(days=30)


def lambda_handler(event, context):
    rh = parser.get_release_history()
    atoms = parser.get_release_atoms(rh)
    for atom in atoms:
        if is_too_old(atom):
            continue
        
        if not store.has_atom(atom):
            print("Posting:", atom)
            result = tweet.post_tweet(atom)
            store.save_atom(atom)
            if result:
                print("SUCCESS")
            else:
                print("FAILED formatting, skipping")
            return

