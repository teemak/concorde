#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cli tool to register a Matrix user with a password generated (securely)
from their mxid"""
import argparse

from concorde.integrations import Matrix

parser = argparse.ArgumentParser(description='Register matrix users with a Matrix homeserver')
parser.add_argument('--homeserver', required=True)
parser.add_argument('--homeserver-secret', required=True)
parser.add_argument('--passgen-secret', required=True)
parser.add_argument('mxids', nargs='*')
args = parser.parse_args()

homeserver_secret = args.homeserver_secret
passgen_secret = args.passgen_secret
mxids = args.mxids

# >>>>> lukeb: perhaps a message saying "no mxids given, here's how to do it.."?
assert len(mxids) > 0

matrix = Matrix(args.homeserver)

for mxid in args.mxids:
# >>>> lukeb: we don't allow control of the `admin` flag. Should we?
# >>>> lukeb: also, won't it be strange to print "@user:bla True"? 
    print mxid, matrix.create_account(args.homeserver_secret, mxid, args.passgen_secret)
