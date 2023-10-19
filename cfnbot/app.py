from datetime import datetime, timedelta

from cfnbot import parser, tweet, toot, store


def is_too_old(atom):
    post_date = datetime.strptime(atom[-1], '%B %d, %Y')
    return (datetime.now() - post_date) > timedelta(days=30)


def lambda_handler(event, context):
    rh = parser.get_release_history()
    atoms = parser.get_release_atoms(rh)
    print('Release history loaded')
    for atom in atoms:
        if is_too_old(atom):
            print('too old:', atom)
            return
        
        if not store.has_atom(atom):
            print("Posting:", atom)
            #result = tweet.post_tweet(atom)
            result = toot.post_toot(atom)
            store.save_atom(atom)
            if result:
                print("SUCCESS")
            else:
                print("FAILED formatting, skipping")
            return

        if context.get_remaining_time_in_millis() < 1000:
            print('leaving early... at:', atom)
            return
            
