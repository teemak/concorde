#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cli script for pulling details of all users in a Slack workspace"""

import os
import sys
import csv
import json
import argparse

from slackclient import SlackClient

parser = argparse.ArgumentParser(description='Fetch user details from a Slack workspace')
parser.add_argument('--bot-oauth-token')
parser.add_argument('--fields', nargs='*')
args = parser.parse_args()

token = (args.bot_oauth_token or
         os.environ['SLACK_CLIENT_TOKEN']
         if 'SLACK_CLIENT_TOKEN' in os.environ else None)
fields = args.fields

# >>>>> lukeb: perhaps this add a message to indicate what the problem could be?
#              (likewise for other asserts)
# e.g. assert token is not None, 'some message'
assert token is not None

available_fields = ['id', 'username', 'real_name', 'display_name', 'avatar', 'email']
if fields is None or len(fields) == 0:
    fields = available_fields
else:
    for field in fields:
        assert field in available_fields

slack = SlackClient(token)

response = slack.api_call('users.list')
writer = csv.writer(sys.stdout)

if 'members' not in response:
# >>>>> lukeb: maybe explain why the script exits here?
    print >> sys.stderr, json.dumps(response, indent=2)
    exit(1)

for user in response['members']:
# >>>>> lukeb: what about other bots? Should this be configurable?
    if user['is_bot'] or user['deleted'] or user['id'] == 'USLACKBOT':
        # Yeah; slackbot is not flagged is_bot so we have to check
        # the ID (which is always 'USLACKBOT')
        continue

    values = {'id': user['id'],
              'username': user['name'],
              'real_name': user['profile']['real_name_normalized'],
              'display_name': user['profile']['display_name_normalized'],
              'avatar': user['profile']['image_512'],
              'email': user['profile']['email']}

    row = []
    for field in fields:
        row.append(values[field])
    writer.writerow(row)

