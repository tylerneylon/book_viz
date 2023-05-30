#!/usr/bin/env python3

# ______________________________________________________________________
# Imports

import base64
from pathlib import Path
from urllib import request


# ______________________________________________________________________
# Globals

test_url_1 = 'https://www.goodreads.com/review/list_rss/3534041?shelf=read'

# ______________________________________________________________________
# Functions

def get_w_cache(url):
    fname = Path('cache/' + base64.b32encode(url.encode()).decode())
    if fname.is_file():
        with fname.open() as f:
            return f.read()
    with request.urlopen(url) as f:
        data = f.read()
    with fname.open('wb') as f:
        f.write(data)
    return data


# ______________________________________________________________________
# Main

data = get_w_cache(test_url_1)
print(data[:20])
