#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import os
import sys
import csv
import argparse

from slackclient import SlackClient

parser = argparse.ArgumentParser(description='Fetch user details from a Slack workspace')
parser.add_argument('--bot-oauth-token')
parser.add_argument('--fields', nargs='*')
args = parser.parse_args()

token = args.bot_oauth_token or os.environ['SLACK_CLIENT_TOKEN']
fields = args.fields

assert token is not None

available_fields = ['id', 'username', 'real_name', 'display_name', 'avatar', 'email']
if fields is None or len(fields) == 0:
    fields = available_fields
else:
    for field in fields:
        assert field in available_fields

slack = SlackClient(token)

users = slack.api_call('users.list')
writer = csv.writer(sys.stdout)

if 'members' not in users:
    print users
    exit(1)

for user in users['members']:
    if user['is_bot'] or user['deleted'] or user['id'] == 'USLACKBOT':
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
