#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
import os
import argparse

from slackclient import SlackClient

parser = argparse.ArgumentParser(description='Send a DM to a Slack user')
parser.add_argument('--bot-oauth-token')
parser.add_argument('slack_id')
parser.add_argument('message')
args = parser.parse_args()

token = args.bot_oauth_token or os.environ['SLACK_CLIENT_TOKEN']
slack_id = args.slack_id
message = args.message

assert slack_id is not None
assert message is not None

slack = SlackClient(token)

slack.api_call('chat.postMessage',
               channel=slack_id,
               text=message,
               as_user=True)
