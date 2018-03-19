#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
import hmac
import hashlib
import urllib
import argparse

parser = argparse.ArgumentParser(description='Generate a link to the account claim')
parser.add_argument('--migration-secret', required=True)
parser.add_argument('link_url')
parser.add_argument('mxid')
args = parser.parse_args()

assert args.link_url is not None
assert args.mxid is not None

mac = hmac.new(key=args.migration_secret,
               digestmod=hashlib.sha1)

mac.update(args.mxid)

params = urllib.urlencode({
    'mxid': args.mxid,
    'code': mac.hexdigest()
    })

print args.link_url + '?' + params
