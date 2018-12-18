import re
import pytest

from cfnbot import parser, tweet



def _sub_link(m):
    return re.sub(r'https?:\S+', 'https://t.co/0123456789', m)


def test_format_all():
    """Verify that all current tweets can be represented in at least 280 chars.
    """
    html = parser.get_release_history()
    for atom in parser.get_release_atoms(html):
        attempts = []
        for msg in tweet.format_tweet(*atom):
            msg = _sub_link(msg)
            attempts.append(msg)
            if len(msg) < 280:
                break
        else:
            for a in attempts:
                print(a)
            assert False, f'could not format {atom} in 280 chars'
