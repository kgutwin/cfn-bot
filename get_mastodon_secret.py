#!/usr/bin/env python3

import os
import getpass
import argparse
from mastodon import Mastodon

CLIENT_CRED = '.mastodon-clientcred.secret'

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--server', default='https://awscommunity.social')
    argparser.add_argument('--force-create-app', action='store_true',
                           default=False)
    argparser.add_argument('login_email')

    args = argparser.parse_args()

    if os.path.exists(CLIENT_CRED):
        # double-check that the server hasn't changed
        with open(CLIENT_CRED) as fp:
            # get the third line
            server = fp.readlines()[2].strip()
            if server != args.server:
                print('Server mismatch, forcing recreating client cred...')
                os.unlink(CLIENT_CRED)
    
    if (not os.path.exists(CLIENT_CRED)
        or args.force_create_app):
        print('Creating cfn-bot app on', args.server, '...')
        Mastodon.create_app('cfn-bot', api_base_url=args.server,
                            to_file=CLIENT_CRED)

    print('Signing in to', args.server, 'as', args.login_email)
    password = getpass.getpass()
    mastodon = Mastodon(client_id=CLIENT_CRED)
    access_token = mastodon.log_in(args.login_email, password)

    with open('.mastodon_keys', 'w') as fp:
        print(f'export MASTODON_ACCESS_TOKEN="{access_token}"', file=fp)
        print(f'export MASTODON_API_BASE_URL="{args.server}"', file=fp)

    print('Created .mastodon_keys - done!')


if __name__ == "__main__":
    main()
