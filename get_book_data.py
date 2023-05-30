#!/usr/bin/env python3
from urllib import request

with request.urlopen('http://www.python.org/') as f:
    print(f.read())
