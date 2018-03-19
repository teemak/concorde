#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
import argparse

from concorde.integrations import Matrix

parser = argparse.ArgumentParser(description='Register matrix users with a Matrix homeserver')
parser.add_argument('--homeserver')
parser.add_argument('--homeserver-secret')
parser.add_argument('--passgen-secret')
parser.add_argument('mxids', nargs='*')
args = parser.parse_args()

homeserver = args.homeserver
homeserver_secret = args.homeserver_secret
passgen_secret = args.passgen_secret
mxids = args.mxids

assert homeserver is not None
assert homeserver_secret is not None
assert passgen_secret is not None
assert len(mxids) > 0

matrix = Matrix(homeserver)

for mxid in mxids:
    print mxid, matrix.create_account(homeserver_secret, mxid, passgen_secret)
