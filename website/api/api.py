# -*- coding: utf-8 -*-
"""API to claim pre-registered accounts on a Matrix homeserver - these accounts
have been registered with generated passwords (a function of the mxid)."""
import json
import hmac
import hashlib
import yaml

from flask import Flask
from flask import request
from flask_cors import CORS
from concorde.integrations import Matrix
from matrix_client.errors import MatrixRequestError

app = Flask(__name__)
CORS(app)

config = yaml.load(open('config.yaml', 'r'))

HOMESERVER = config['homeserver']
PASSGEN_SECRET = config['passgen_secret']       # Used to generate passwords from mxid
MIGRATION_SECRET = config['migration_secret']   # Used to validate user was sent link by us

def response(code, message, error=None):
    """Format a standard API response body"""
    response_object = {
        'response_code': code,
        'message': message
        }
    if error:
        response_object['error'] = error
    return json.dumps(response_object)

SUCCESS = response(200,
                   'Your account has been successfully claimed!')
REQUEST_VALIDATION_FAILED = response(401,
                                     ('Your request to claim this account could not ' +
                                      'be validated - please contact your community ' +
                                      'administrator.'),
                                     'CODE_VALIDATION_FAILURE')
ALREADY_CLAIMED = response(401,
                           ('This account has already been claimed - ' +
                            'please speak to your community administrator.'),
                           'PASSWORD_ALREADY_RESET')

@app.route('/availability')
def availability():
    """Check we're deployed correctly"""
    return 'I\'m here!'

@app.route('/claim', methods=['POST'])
def claim():
    """Complete claim of a migrated account. Works by using the passgen_secret to try
    and log in as the user with the generated password and change their password to
    the requested new password.
    If we can't log in with the generated password we assume this means they've already
    changed their password successfully."""
    content = request.get_json()
    mxid = content['mxid'] if 'mxid' in content else ''
    code = content['code'] if 'code' in content else ''
    new_password = content['password']

    if not request_is_valid(mxid, code):
        return REQUEST_VALIDATION_FAILED

    matrix = Matrix(HOMESERVER)
    try:
        if matrix.claim_account(mxid, PASSGEN_SECRET, new_password):
            return SUCCESS
        else:
            return ALREADY_CLAIMED
    except MatrixRequestError as exception:
        if exception.code == 403:
            return ALREADY_CLAIMED
        else:
            return json.dumps({
                'response_code': exception.code,
                'message': 'This request failed - please try again later.',
                'error': 'GENERIC_FAILURE'
                })

def request_is_valid(mxid, code):
    """Validate that the code provided has been hashed using the secret shared
    with the link-generation cli script"""
    # Establish the validity of the request:
    if mxid == '' or code == '':
        return False

    mac = hmac.new(key=MIGRATION_SECRET,
                   digestmod=hashlib.sha1)
    mac.update(mxid)

    return mac.hexdigest() == code


if __name__ == '__main__':
    app.run()
