#! /usr/bin/env python

import os
import urllib
import sys
sys.path.append('..')

import mvfs
import mvfs.openers

def abspath(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)

def download_and_store(base_path, opener=False):
    store_path = abspath(base_path)
    if not os.path.exists(store_path):
        os.mkdir(store_path)

    if len(sys.argv) != 3:
        print 'Usage: %s <url> <path>' % sys.argv[0]
        sys.exit(1)

    url, dest = sys.argv[1:]

    storage = mvfs.Storage(store_path, opener=opener)
    with storage.open(dest, 'w') as f:
        f.write(urllib.urlopen(url).read())

    storage.cleanup(versions=10)


if __name__ == '__main__':
    download_and_store('store-default')
    download_and_store('store-plain', mvfs.openers.PlainFileOpener())

