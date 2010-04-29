#! /usr/bin/env python

import os
import urllib
import sys
sys.path.append('..')

import mvfs

def abspath(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)

if __name__ == '__main__':
    store_path = abspath('store')
    if not os.path.exists(store_path):
        os.mkdir(store_path)

    if len(sys.argv) != 3:
        print 'Usage: %s <url> <path>' % sys.argv[0]
        sys.exit(1)

    url, dest = sys.argv[1:]

    storage = mvfs.Storage(store_path)
    with storage.open(dest, 'w') as f:
        f.write(urllib.urlopen(url).read())

    storage.cleanup(versions=10)

